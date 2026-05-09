"""Parser birim testleri."""

from pathlib import Path

import pytest

from bookmaker.chapter.parser import parse


class TestParseFrontmatter:
    def test_sample_chapter_has_frontmatter(self, sample_chapter: Path) -> None:
        parsed = parse(sample_chapter)
        assert parsed.frontmatter, "Sample chapter should have front matter"
        assert parsed.frontmatter["title"] == "Dosya İşlemleri ve Kalıcı Veri Saklama"
        assert parsed.frontmatter["chapter_id"] == "dosya_islemleri"
        assert parsed.frontmatter["lang"] == "tr-TR"
        assert parsed.frontmatter["repo"] == "bmdersleri"

    def test_missing_frontmatter(self, tmp_path: Path) -> None:
        f = tmp_path / "no_frontmatter.md"
        f.write_text("# Başlık\n\nİçerik", encoding="utf-8")
        parsed = parse(f)
        assert parsed.frontmatter == {}

    def test_invalid_frontmatter(self, tmp_path: Path) -> None:
        f = tmp_path / "invalid_fm.md"
        f.write_text("---\ninvalid: yaml\n  broken\n---\n# Başlık", encoding="utf-8")
        parsed = parse(f)
        # Geçersiz YAML -> fallback: boş dict
        assert isinstance(parsed.frontmatter, dict)


class TestParseHeadings:
    def test_sample_chapter_has_one_h1(self, sample_chapter: Path) -> None:
        parsed = parse(sample_chapter)
        h1 = [h for h in parsed.headings if h.level == 1]
        assert len(h1) == 1
        assert h1[0].title == "Dosya İşlemleri ve Kalıcı Veri Saklama"

    def test_headings_have_levels_and_lines(self, sample_chapter: Path) -> None:
        parsed = parse(sample_chapter)
        assert len(parsed.headings) > 5
        for h in parsed.headings:
            assert h.level in range(1, 7)
            assert h.title
            assert h.line > 0

    def test_heading_order(self, tmp_path: Path) -> None:
        f = tmp_path / "headings.md"
        f.write_text(
            "# H1\n\n## H2.1\n\n### H3\n\n## H2.2\n\n# Ikinci H1\n",
            encoding="utf-8",
        )
        parsed = parse(f)
        assert len(parsed.headings) == 5
        assert parsed.headings[0].title == "H1"
        assert parsed.headings[1].title == "H2.1"
        assert parsed.headings[4].title == "Ikinci H1"


class TestParseMetaBlocks:
    def test_sample_chapter_has_section_meta(self, sample_chapter: Path) -> None:
        parsed = parse(sample_chapter)
        section_blocks = [b for b in parsed.meta_blocks if b.kind == "SECTION_META"]
        assert len(section_blocks) > 0
        assert all(b.data.get("order") for b in section_blocks)

    def test_sample_chapter_has_code_meta(self, sample_chapter: Path) -> None:
        parsed = parse(sample_chapter)
        code_blocks = [b for b in parsed.meta_blocks if b.kind == "CODE_META"]
        assert len(code_blocks) > 0

    def test_meta_block_fields(self, sample_chapter: Path) -> None:
        parsed = parse(sample_chapter)
        for block in parsed.meta_blocks:
            assert block.kind in {"SECTION_META", "SUBSECTION_META", "CODE_META",
                                  "MERMAID_META", "ASSET_META", "SCREENSHOT_META"}
            assert block.line > 0
            assert block.end > 0

    def test_empty_file_meta(self, tmp_path: Path) -> None:
        f = tmp_path / "empty.md"
        f.write_text("", encoding="utf-8")
        parsed = parse(f)
        assert parsed.meta_blocks == []
        assert parsed.headings == []


class TestParseEdgeCases:
    def test_bom_handling(self, tmp_path: Path) -> None:
        f = tmp_path / "bom.md"
        # BOM + UTF-8 içerik (tek BOM baytları)
        f.write_bytes(b"\xef\xbb\xbf---\ntitle: BOM\n---\n# Baslik\n")
        parsed = parse(f)
        assert parsed.frontmatter.get("title") == "BOM"

    def test_encoding_error(self, tmp_path: Path) -> None:
        f = tmp_path / "bad_encoding.md"
        # Geçersiz UTF-8 baytları
        f.write_bytes(b"---\ntitle: Test\n---\n# \xff\xfe\x00Baslik\n")
        # UTF-8 decode hatası beklenir
        with pytest.raises((UnicodeDecodeError, UnicodeError)):
            f.read_text(encoding="utf-8")
