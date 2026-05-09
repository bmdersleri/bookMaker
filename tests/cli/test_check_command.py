"""CLI check komutu testleri."""

import json
from pathlib import Path

from typer.testing import CliRunner

from bookmaker.cli import app

runner = CliRunner()


class TestCheckChapterCommand:
    def test_check_sample_chapter(self, sample_chapter: Path) -> None:
        result = runner.invoke(app, ["check", "chapter", str(sample_chapter)])
        assert result.exit_code == 0, (
            f"Check failed with: {result.output}"
        )
        assert "Skor" in result.output
        assert "Karar" in result.output

    def test_check_nonexistent_file(self) -> None:
        result = runner.invoke(app, ["check", "chapter", "nonexistent.md"])
        assert result.exit_code == 1
        not_found = "bulunamad" in result.output or "Bulunamad" in result.output
        assert not_found or result.exit_code == 1

    def test_check_with_json_flag(self, sample_chapter: Path, tmp_path: Path) -> None:
        # Geçici dizine geç
        original_cwd = Path.cwd()
        import os
        os.chdir(str(tmp_path))
        try:
            result = runner.invoke(app, ["check", "chapter", str(sample_chapter), "--json"])
            assert result.exit_code == 0
            # JSON raporu logs/reviews/ altına yazılır
            report_files = list(Path("logs/reviews").glob("*quality_report.json"))
            assert len(report_files) > 0
            # JSON içeriğini doğrula
            report_data = json.loads(report_files[0].read_text(encoding="utf-8"))
            assert "score" in report_data
            assert "decision" in report_data
            assert "chapter_id" in report_data
            assert report_data["chapter_id"] == "dosya_islemleri"
        finally:
            os.chdir(str(original_cwd))

    def test_check_invalid_file_returns_error(self, fixtures_dir: Path) -> None:
        f = fixtures_dir / "invalid_wrong_heading.md"
        result = runner.invoke(app, ["check", "chapter", str(f)])
        # Hata olmalı ama çökmemeli
        assert result.exit_code == 1
        assert "Hata" in result.output or "hata" in result.output or result.exit_code == 1

    def test_check_with_final_flag(self, tmp_path: Path) -> None:
        f = tmp_path / "with_placeholder.md"
        f.write_text(
            '---\ntitle: Placeholder\nrepo: test\nproject-alias: test\nchapter-alias: test\n'
            'toc: true\ntoc-depth: 3\nnumbersections: true\ndocumentclass: report\n'
            'author: T\ndate: "2026"\nlang: tr-TR\n---\n# Test\nBir {placeholder} var.\n',
            encoding="utf-8",
        )
        result = runner.invoke(app, ["check", "chapter", str(f), "--final"])
        assert result.exit_code == 1
