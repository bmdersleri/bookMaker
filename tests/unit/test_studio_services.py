"""Servis birim testleri - Faz 1 servis mimarisi."""
from __future__ import annotations

import json
from pathlib import Path


def _create_test_project(tmp_path: Path) -> Path:
    """Minimal test projesi olusturur. Dogrudan dosya yazar, proje import'lari kullanmaz."""
    root = tmp_path / "test-book"
    root.mkdir(parents=True)
    
    # book_profile.yaml
    profile = {
        "book": {"title": "Test Kitap", "author": "Test Yazar",
                 "language": "tr", "target_audience": "universite_1"},
        "chapters": [],
    }
    import yaml as _yaml
    (root / "book_profile.yaml").write_text(
        _yaml.dump(profile, allow_unicode=True), encoding="utf-8")

    # book_manifest.yaml
    manifest = {
        "book": {"title": "Test Kitap", "author": "Test Yazar"},
        "chapters": [],
    }
    (root / "book_manifest.yaml").write_text(
        _yaml.dump(manifest, allow_unicode=True), encoding="utf-8")

    # pipeline_state.yaml
    (root / "pipeline_state.yaml").write_text(
        _yaml.dump({"pipeline_id": "test", "current_stage": "authoring",
                    "chapters": {}}, allow_unicode=True), encoding="utf-8")

    # llm_config.json
    (root / "llm_config.json").write_text(
        json.dumps([{"provider": "deepseek", "api_key": "sk-test",
                     "model": "deepseek-chat"}]), encoding="utf-8")

    # Chapters dir
    ch_dir = root / "chapters" / "bolum-01" / "approved"
    ch_dir.mkdir(parents=True)
    (ch_dir / "bolum-01_v001.md").write_text(
        "# Test Chapter\n\nTest icerik.", encoding="utf-8")

    return root


# ================================================================
# MANIFEST SERVICE TESTS
# ================================================================

def test_manifest_get_project_info(tmp_path):
    root = _create_test_project(tmp_path)
    from bookmaker.studio.services import manifest_service
    info = manifest_service.get_project_info(root)
    assert info["title"] == "Test Kitap"
    assert info["chapters"] == 0
    assert "stage" in info


def test_manifest_load_manifest_returns_model(tmp_path):
    root = _create_test_project(tmp_path)
    from bookmaker.studio.services import manifest_service

    manifest = manifest_service.load_manifest(root)

    assert manifest.book.title == "Test Kitap"


def test_split_services_project_info_and_pipeline_state(tmp_path):
    root = _create_test_project(tmp_path)
    from bookmaker.studio.services import book_service, pipeline_service

    info = book_service.get_project_info(root)
    state = pipeline_service.get_pipeline_state(root)

    assert info["title"] == "Test Kitap"
    assert info["chapters"] == 0
    assert state["pipeline_id"] == "test"
    assert state["chapters"] == {}


def test_book_service_project_info_includes_flutter_profile(tmp_path):
    root = _create_test_project(tmp_path)
    (root / "book_manifest.yaml").write_text(
        "book:\n"
        "  title: Flutter Demo\n"
        "  alias: flutter-ile-mobil-uygulama-gelistirme\n"
        "  author: Test Yazar\n"
        "style:\n"
        "  code_language: dart\n"
        "  framework: flutter\n"
        "automation:\n"
        "  screenshot_required: true\n"
        "  qr_policy: dual\n"
        "chapters:\n"
        "  - alias: giris\n",
        encoding="utf-8",
    )
    from bookmaker.studio.services import book_service

    info = book_service.get_project_info(root)

    assert info["alias"] == "flutter-ile-mobil-uygulama-gelistirme"
    assert info["profile"] == "flutter"
    assert info["framework"] == "flutter"
    assert info["code_language"] == "dart"
    assert info["screenshot_required"] is True
    assert info["qr_policy"] == "dual"


def test_chapter_service_creates_project_workspace(tmp_path):
    root = _create_test_project(tmp_path)
    from bookmaker.studio.services import chapter_service

    result = chapter_service.add_chapter(root, "bolum-02", "Yeni Bolum", 1)

    assert result["chapter_id"] == "bolum-02"
    assert (root / "chapters" / "bolum-02" / "chapter_manifest.yaml").exists()
    assert (root / "chapters" / "bolum-02" / "prompt.md").exists()
    assert (root / "chapters" / "bolum-02" / "content" / "draft.md").exists()
    assert (root / "chapters" / "bolum-02" / "content" / "final.md").exists()
    assert (root / "chapters" / "bolum-02" / "content" / "revisions").is_dir()


def test_chapter_list_exposes_project_content_flags(tmp_path):
    root = _create_test_project(tmp_path)
    from bookmaker.studio.services import chapter_service

    chapter_service.add_chapter(root, "bolum-02", "Yeni Bolum", 1)

    chapters = chapter_service.get_chapter_list(root)
    chapter = next(item for item in chapters if item["chapter_id"] == "bolum-02")
    assert chapter["draft_exists"] is True
    assert chapter["final_exists"] is True
    assert chapter["prompt_exists"] is True


def test_quality_service_reads_alias_only_project_chapter(tmp_path):
    root = _create_test_project(tmp_path)
    (root / "book_manifest.yaml").write_text(
        "book:\n"
        "  title: Alias Book\n"
        "chapters:\n"
        "  - alias: giris\n"
        "    title: Giriş\n",
        encoding="utf-8",
    )
    content_dir = root / "chapters" / "giris" / "content"
    content_dir.mkdir(parents=True)
    (content_dir / "final.md").write_text("# Giriş\n\nİçerik.", encoding="utf-8")
    from bookmaker.studio.services import quality_service

    content = quality_service.get_chapter_content(root, "giris")
    stats = quality_service.get_book_stats(root)

    assert content["chapter_id"] == "giris"
    assert content["path"].replace("\\", "/") == "chapters/giris/content/final.md"
    assert stats["word_distribution"][0]["chapter_id"] == "giris"


def test_quality_service_returns_book_quality_summary(tmp_path):
    from bookmaker.studio.services import quality_service, wizard_service

    result = wizard_service.create_book(
        tmp_path,
        {
            "project_name": "quality-demo",
            "title": "Quality Demo",
            "author": "Test Yazar",
            "chapters": ["giris", "kurulum"],
        },
    )
    assert "error" not in result
    root = tmp_path / "book_projects" / "quality-demo"

    report = quality_service.get_book_quality_report(root)

    assert report["chapter_id"] == "book"
    assert report["score"] == 100
    assert report["decision"] == "pass"
    assert report["report_path"].replace("\\", "/") == "logs/reviews/book_quality_report.json"
    assert [chapter["chapter_id"] for chapter in report["chapters"]] == ["giris", "kurulum"]
    assert all(chapter["report_path"].endswith("_quality_report.json")
               for chapter in report["chapters"])


def test_prompt_service_roundtrip(tmp_path):
    root = _create_test_project(tmp_path)
    from bookmaker.studio.services import chapter_service, prompt_service

    prompt_service.save_default_prompt(root, "Default prompt", "chapter")
    default_prompt = prompt_service.get_default_prompt(root, "chapter")

    chapter_service.add_chapter(root, "bolum-02", "Yeni Bolum", 1)
    prompt_service.save_chapter_prompt(root, "bolum-02", "Chapter prompt")
    chapter_prompt = prompt_service.get_chapter_prompt(root, "bolum-02")

    assert default_prompt["content"] == "Default prompt"
    assert default_prompt["path"].replace("\\", "/") == "prompts/default_chapter.md"
    assert chapter_prompt["content"] == "Chapter prompt"
    assert chapter_prompt["path"].replace("\\", "/") == "chapters/bolum-02/prompt.md"


def test_manifest_add_and_remove_chapter(tmp_path):
    root = _create_test_project(tmp_path)
    from bookmaker.studio.services import manifest_service

    r = manifest_service.add_chapter(root, "bolum-01", "Test Bolum", 1)
    assert r.get("chapter_id") == "bolum-01"

    chapters = manifest_service.get_chapter_list(root)
    assert len(chapters) == 1
    assert chapters[0]["title"] == "Test Bolum"

    r = manifest_service.remove_chapter(root, "bolum-01")
    assert r.get("deleted") is True

    chapters = manifest_service.get_chapter_list(root)
    assert len(chapters) == 0


def test_manifest_reorder_chapters(tmp_path):
    root = _create_test_project(tmp_path)
    from bookmaker.studio.services import manifest_service

    manifest_service.add_chapter(root, "bolum-01", "Bir", 1)
    manifest_service.add_chapter(root, "bolum-02", "Iki", 2)
    manifest_service.add_chapter(root, "bolum-03", "Uc", 3)

    r = manifest_service.reorder_chapters(
        root, ["bolum-03", "bolum-01", "bolum-02"])
    assert r["reordered"]
    assert r["count"] == 3

    chapters = manifest_service.get_chapter_list(root)
    assert chapters[0]["chapter_id"] == "bolum-03"


def test_manifest_update_chapter(tmp_path):
    root = _create_test_project(tmp_path)
    from bookmaker.studio.services import manifest_service

    manifest_service.add_chapter(root, "bolum-01", "Eski Baslik", 1)
    r = manifest_service.update_chapter(
        root, "bolum-01", {"title": "Yeni Baslik"})
    assert r.get("updated") is True

    chapters = manifest_service.get_chapter_list(root)
    assert chapters[0]["title"] == "Yeni Baslik"


def test_manifest_get_pipeline_state(tmp_path):
    root = _create_test_project(tmp_path)
    from bookmaker.studio.services import manifest_service
    state = manifest_service.get_pipeline_state(root)
    assert "pipeline_id" in state
    assert "current_stage" in state


# ================================================================
# LLM SERVICE TESTS
# ================================================================

def test_llm_get_status(tmp_path):
    root = _create_test_project(tmp_path)
    from bookmaker.studio.services import llm_service
    status = llm_service.get_status(root)
    assert "configured" in status
    assert status["provider"] == "deepseek"


def test_llm_configure(tmp_path):
    root = _create_test_project(tmp_path)
    from bookmaker.studio.services import llm_service
    r = llm_service.configure(root, "openai", "sk-new-key", "gpt-4o")
    assert r["status"] == "ok"
    assert r["model"] == "gpt-4o"

    status = llm_service.get_status(root)
    assert status["model"] == "gpt-4o"


# ================================================================
# QUALITY SERVICE TESTS
# ================================================================

def test_quality_validate_not_found(tmp_path):
    root = _create_test_project(tmp_path)
    from bookmaker.studio.services import quality_service
    r = quality_service.validate_chapter(root, "olmayan-bolum")
    assert "error" in r


# ================================================================
# PIPELINE SERVICE TESTS
# ================================================================

def test_pipeline_get_generator_no_llm(tmp_path):
    root = tmp_path / "empty-book"
    root.mkdir()
    from bookmaker.studio.services import pipeline_service
    gen = pipeline_service.get_generator(root)
    assert gen is None


def test_pipeline_get_chapter_info(tmp_path):
    root = _create_test_project(tmp_path)
    from bookmaker.studio.services import manifest_service, pipeline_service

    manifest_service.add_chapter(root, "bolum-01", "Test", 1)
    info = pipeline_service.get_chapter_info(root, "bolum-01")
    assert info is not None
    assert info["chapter_id"] == "bolum-01"


# ================================================================
# BUILD SERVICE TESTS
# ================================================================

def test_build_no_source(tmp_path):
    root = _create_test_project(tmp_path)
    from bookmaker.studio.services import build_service
    r = build_service.build_docx(root, "olmayan-bolum")
    assert "error" in r


def test_export_service_uses_project_exports_and_alias_sources(tmp_path):
    root = _create_test_project(tmp_path)
    (root / "book_manifest.yaml").write_text(
        "book:\n"
        "  title: Flutter Demo\n"
        "  alias: flutter-demo\n"
        "style:\n"
        "  code_language: dart\n"
        "  framework: flutter\n"
        "chapters:\n"
        "  - alias: giris\n",
        encoding="utf-8",
    )
    content_dir = root / "chapters" / "giris" / "content"
    content_dir.mkdir(parents=True)
    (content_dir / "final.md").write_text(
        "# Giriş\n\n```dart\nvoid main() {}\n```\n",
        encoding="utf-8",
    )

    from bookmaker.studio.services import export_service

    targets = export_service.get_export_targets(root)
    assert targets["root"] == "exports"
    assert targets["code_language"] == "dart"
    assert targets["targets"]["docx"].replace("\\", "/") == "exports/docx"

    assembled = export_service.assemble_book(root)
    assert assembled["chapters"] == 1
    assert assembled["path"].replace("\\", "/") == "exports/md/kitap_birlestirilmis.md"

    extracted = export_service.extract_code(root, "giris")
    assert extracted["language"] == "dart"
    assert extracted["total_extracted"] == 1
    assert extracted["output_dir"].replace("\\", "/") == "exports/code/dart"


def test_wizard_creates_project_based_book(tmp_path):
    from bookmaker.manifest.models import BookManifest, PipelineState
    from bookmaker.studio.services import wizard_service

    result = wizard_service.create_book(
        tmp_path,
        {
            "project_name": "flutter-demo",
            "title": "Flutter Demo",
            "author": "Test Yazar",
            "language": "tr",
            "chapter_count": 1,
            "appendix_count": 0,
            "chapters": ["giris"],
        },
    )

    assert "error" not in result
    project = tmp_path / "book_projects" / "flutter-demo"
    assert (project / "book_manifest.yaml").exists()
    assert (project / "pipeline_state.yaml").exists()
    assert (project / "prompts" / "default_chapter.md").exists()
    assert (project / "prompts" / "default_review.md").exists()
    assert (project / "chapters" / "giris" / "chapter_manifest.yaml").exists()
    assert (project / "chapters" / "giris" / "prompt.md").exists()
    assert (project / "chapters" / "giris" / "content" / "draft.md").exists()
    assert (project / "chapters" / "giris" / "content" / "final.md").exists()
    assert not (project / "book_profile.yaml").exists()
    assert not (project / "book_architecture.yaml").exists()
    assert not (project / "chapters" / "giris" / "approved").exists()

    manifest = BookManifest.load(project / "book_manifest.yaml")
    state = PipelineState.load(project / "pipeline_state.yaml")
    assert manifest.book.alias == "flutter-demo"
    assert manifest.chapter_aliases() == ["giris"]
    assert state.pipeline.book_alias == "flutter-demo"


def test_wizard_accepts_chapter_plan_titles(tmp_path):
    from bookmaker.manifest.models import BookManifest, ChapterManifest
    from bookmaker.studio.services import wizard_service

    result = wizard_service.create_book(
        tmp_path,
        {
            "project_name": "custom-plan",
            "title": "Custom Plan",
            "author": "Test Yazar",
            "chapters": [
                {"alias": "giris", "title": "Giriş"},
                {"chapter_id": "kurulum", "title": "Kurulum"},
            ],
        },
    )

    assert "error" not in result
    project = tmp_path / "book_projects" / "custom-plan"
    manifest = BookManifest.load(project / "book_manifest.yaml")
    chapter_manifest = ChapterManifest.load(
        project / "chapters" / "giris" / "chapter_manifest.yaml"
    )
    assert manifest.chapter_aliases() == ["giris", "kurulum"]
    assert manifest.chapters[0].title == "Giriş"
    assert chapter_manifest.chapter.title == "Giriş"
    assert (project / "chapters" / "giris" / "content" / "draft.md").read_text(
        encoding="utf-8"
    ).startswith("# Giriş")


def test_wizard_uses_parent_book_projects_when_active_book_is_project(tmp_path):
    from bookmaker.studio.services import wizard_service

    active_project = tmp_path / "book_projects" / "current-book"
    active_project.mkdir(parents=True)
    (active_project / "book_manifest.yaml").write_text(
        "book:\n  alias: current-book\nchapters: []\n",
        encoding="utf-8",
    )

    result = wizard_service.create_book(
        active_project,
        {
            "project_name": "new-book",
            "title": "New Book",
            "author": "Test Yazar",
            "chapters": ["giris"],
        },
    )

    assert "error" not in result
    assert (tmp_path / "book_projects" / "new-book" / "book_manifest.yaml").exists()
    assert not (active_project / "book_projects" / "new-book").exists()
