"""Otomatik kitap/bölüm üretim pipeline'ı."""

from __future__ import annotations

from pathlib import Path

from bookmaker.authoring.pipeline import AuthoringPipeline
from bookmaker.generation.postprocess import process as postprocess
from bookmaker.generation.prompts import book_prompt, chapter_prompt, outline_prompt
from bookmaker.llm.config import LLMConfig
from bookmaker.llm.openai import OpenAICompatibleClient


class GenerationPipeline:
    """LLM API kullanarak otomatik içerik üretimi."""

    def __init__(self, project_root: Path) -> None:
        self.root = project_root.resolve()
        self.config = LLMConfig(self.root)
        self.client: OpenAICompatibleClient | None = None
        self._init_client()

    def _init_client(self) -> None:
        if self.config.is_configured():
            self.client = OpenAICompatibleClient(
                api_key=self.config.api_key,
                model=self.config.model,
                base_url=self.config.base_url,
                timeout=300,
            )

    def is_ready(self) -> bool:
        return self.client is not None and self.config.is_configured()

    def generate_outline(self, chapter_id: str, topic: str, purpose: str = "") -> str:
        """LLM ile outline üretir ve AuthoringPipeline'a kaydeder."""
        if not self.client:
            raise RuntimeError(
                "LLM API yapılandırılmamış. 'bookmaker llm configure' çalıştır."
            )

        sys_prompt, user_prompt = outline_prompt(topic, purpose)
        outline = self.client.generate_text(sys_prompt, user_prompt)

        pipe = AuthoringPipeline(self.root)
        pipe.paste_outline(chapter_id, outline)
        pipe.advance(chapter_id, "outline_pasted")

        return outline

    def generate_chapter(
        self,
        chapter_id: str,
        chapter_title: str,
        purpose: str = "",
        concepts: list[str] | None = None,
    ) -> str:
        """LLM ile bölüm metni üretir ve AuthoringPipeline'a kaydeder."""
        if not self.client:
            raise RuntimeError("LLM API yapılandırılmamış.")

        pipe = AuthoringPipeline(self.root)
        outline_p = pipe.root / "chapters" / chapter_id / "outline_versions" / "v001.md"

        if not outline_p.exists():
            # Seed yoksa oluştur
            pipe.seed(chapter_id, purpose=purpose, mandatory_concepts=concepts or [])
            # Outline yoksa topic'ten üret
            outline = self.generate_outline(chapter_id, chapter_title, purpose)
        else:
            outline = outline_p.read_text(encoding="utf-8")

        sys_prompt, user_prompt = chapter_prompt(chapter_title, outline, purpose, concepts)
        chapter_text = self.client.generate_text(sys_prompt, user_prompt)

        # Post-process: front matter + heading fix + CODE_META
        chapter_text = postprocess(chapter_text, chapter_id, chapter_title)

        pipe.paste_draft(chapter_id, chapter_text)
        pipe.advance(chapter_id, "full_text_pasted")

        return chapter_text

    def generate_book_outline(self, topic: str, language: str = "tr-TR", audience: str = "") -> str:
        """LLM ile kitap outline'ı üretir."""
        if not self.client:
            raise RuntimeError("LLM API yapılandırılmamış.")

        sys_prompt, user_prompt = book_prompt(topic, language, audience)
        return self.client.generate_text(sys_prompt, user_prompt)

    def generate_full_book(self, topic: str, language: str = "tr-TR") -> dict:
        """Konudan kitap oluşturur: init → outline → bölümler."""
        if not self.client:
            raise RuntimeError("LLM API yapılandırılmamış.")

        result: dict = {"topic": topic, "outline": "", "chapters": []}

        # 1. Kitap outline'ı
        book_outline = self.generate_book_outline(topic, language)
        result["outline"] = book_outline

        # 2. Kitap profili oluştur
        from bookmaker.models.book import BookArchitecture, BookProfile

        profile = BookProfile(
            book_id=topic.lower().replace(" ", "_"),
            title=topic,
            language=language,
            quality_profile="academic_technical_book_v1",
        )
        profile.to_yaml(self.root / "book_profile.yaml")

        # 3. Preset oluştur ve init yap
        from bookmaker.commands.init import PRESETS
        if "custom" not in PRESETS:
            PRESETS.append("custom")

        arch = BookArchitecture(book_id=profile.book_id)
        arch.to_yaml(self.root / "book_architecture.yaml")

        # 4. Bölümleri üret
        pipe = AuthoringPipeline(self.root)
        for i in range(1, 4):  # İlk 3 bölümü otomatik üret
            cid = f"bolum_{i:02d}"
            title = f"Bölüm {i}: {topic} — Temel Kavramlar"
            pipe.seed(cid, purpose=f"{topic} temel kavramları")

            try:
                self.generate_chapter(cid, title, purpose=f"{topic} bolum {i}")
                result["chapters"].append({"id": cid, "title": title, "status": "generated"})
            except Exception as e:
                result["chapters"].append({"id": cid, "title": title, "status": f"error: {e}"})

        return result
