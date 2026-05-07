from __future__ import annotations

from pathlib import Path


def test_save_chapter_writes_content_draft_and_revision(tmp_path: Path) -> None:
    from bookmaker.generation.pipeline import ChapterGenerator

    generator = ChapterGenerator(tmp_path)
    draft_path = generator._save_chapter("giris", "# Giriş\n\nİçerik.")

    assert draft_path == tmp_path / "chapters" / "giris" / "content" / "draft.md"
    assert draft_path.read_text(encoding="utf-8").startswith("# Giriş")

    revisions = list(
        (tmp_path / "chapters" / "giris" / "content" / "revisions").glob("draft_*.md")
    )
    assert len(revisions) == 1
    assert revisions[0].read_text(encoding="utf-8").startswith("# Giriş")


def test_sectioned_prompt_uses_manifest_code_language(tmp_path: Path) -> None:
    from bookmaker.generation.pipeline import ChapterGenerator

    (tmp_path / "book_manifest.yaml").write_text(
        "book:\n"
        "  title: Flutter Demo\n"
        "  alias: flutter-demo\n"
        "style:\n"
        "  code_language: dart\n"
        "chapters: []\n",
        encoding="utf-8",
    )

    prompts: list[str] = []

    class FakeClient:
        def generate_text(self, system: str, prompt: str) -> str:  # noqa: ARG002
            return "1. GİRİŞ\n2. KULLANIM\n3. KAPANIŞ"

        def generate_text_with_resume(self, system: str, prompt: str, max_tokens: int = 0) -> str:  # noqa: ARG002
            prompts.append(prompt)
            return "# Bölüm\n\n## Giriş\n\nİçerik.\n"

    generator = ChapterGenerator(tmp_path)
    generator.client = FakeClient()

    result = generator.generate_chapter_sectioned(
        "giris",
        "Giriş",
        ["kurulum", "temel"],
        save=False,
    )

    assert result["sections"]
    assert prompts
    assert all("```dart" in prompt for prompt in prompts)
    assert all("```java" not in prompt for prompt in prompts)
