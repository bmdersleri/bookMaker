"""Post-process testleri."""

from bookmaker.generation.postprocess import (
    auto_code_meta,
    ensure_frontmatter,
    fix_heading_hierarchy,
    process,
)


def test_ensure_frontmatter_adds_when_missing():
    text = "# Baslik\nIcerik.\n"
    result = ensure_frontmatter(text, "bolum-01", "Java Giris")
    assert result.startswith("---")
    assert "title: \"Java Giris\"" in result
    assert "chapter_id: bolum-01" in result
    assert "# Baslik" in result


def test_ensure_frontmatter_keeps_existing():
    text = "---\ntitle: Var\n---\n# Baslik\n"
    result = ensure_frontmatter(text, "bolum-01", "Yeni")
    assert result == text


def test_fix_heading_reduces_multiple_h1():
    text = "# Ilk\n## Ikinci\n# Ucuncu\n### Detay\n# Dorduncu\n"
    result = fix_heading_hierarchy(text)
    lines = result.splitlines()
    assert lines[0] == "# Ilk"
    assert lines[1] == "## Ikinci"
    assert lines[2] == "## Ucuncu"
    assert lines[3] == "### Detay"
    assert lines[4] == "## Dorduncu"


def test_auto_code_meta_adds_meta():
    chapter_id = "bolum-01"
    text = "Metin\n```java\n// Dosya: Ornek.java\npublic class Ornek {}\n```\n"
    result = auto_code_meta(text, chapter_id)
    assert "CODE_META" in result
    assert "bolum-01_kod01" in result
    assert "Ornek.java" in result


def test_auto_code_meta_skips_existing():
    text = "<!-- CODE_META\nid: var\n-->\n```java\n// D: var.java\nclass var {}\n```\n"
    result = auto_code_meta(text, "test")
    assert result.count("CODE_META") == 1


def test_process_runs_all():
    raw = "# Java\n# Alt\n```java\n// D: Test.java\npublic class Test {}\n```\n"
    result = process(raw, "bolum-01", "Java Giris")
    assert result.startswith("---")
    assert "title: \"Java Giris\"" in result
    assert "## Alt" in result
    assert "CODE_META" in result


def test_frontmatter_includes_all_required():
    text = "# Baslik\n"
    result = ensure_frontmatter(text, "bolum-01", "Test")
    assert "chapter_spec: chapter_spec_v0_1" in result
    assert "processing_stage: authoring_source" in result
    assert "placeholder_policy: source_template" in result
    assert "snippet_policy: non_meta_code_is_explanatory" in result
