"""
tests/production/test_mermaid_renderer.py
==========================================
Mermaid tema motoru için unit testler.
mmdc mock'lanır — gerçek mmdc kurulumu gerekmez.
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from bookmaker.production.mermaid_renderer import (
    _MERMAID_BLOCK_RE,
    MermaidRenderConfig,
    MermaidRenderer,
)
from bookmaker.production.mermaid_theme import (
    MermaidTheme,
    MermaidThemeManager,
)

# ---------------------------------------------------------------------------
# Sabitler
# ---------------------------------------------------------------------------

SIMPLE_FLOWCHART = """
graph TD
    A[Başla] --> B{Karar}
    B -- Evet --> C[Devam]
    B -- Hayır --> D[Dur]
""".strip()

SEQUENCE_DIAGRAM = """
sequenceDiagram
    Alice->>Bob: Merhaba
    Bob-->>Alice: Selam
""".strip()

MARKDOWN_WITH_TWO_BLOCKS = f"""
# Bölüm 1

Bir açıklama.

```mermaid
{SIMPLE_FLOWCHART}
```

Daha fazla açıklama.

```mermaid
{SEQUENCE_DIAGRAM}
```

Son paragraf.
"""


# ---------------------------------------------------------------------------
# MermaidTheme testleri
# ---------------------------------------------------------------------------

class TestMermaidTheme:
    def test_load_flutter_theme(self):
        theme = MermaidTheme.load("flutter")
        assert theme.name == "flutter"
        assert "themeVariables" in theme.config
        assert theme.config["themeVariables"]["primaryBorderColor"] == "#0175C2"

    def test_load_java_theme(self):
        theme = MermaidTheme.load("java")
        assert "#E65100" in theme.config["themeVariables"]["primaryBorderColor"]

    def test_load_python_theme(self):
        theme = MermaidTheme.load("python")
        assert "#3572A5" in theme.config["themeVariables"]["primaryBorderColor"]

    def test_load_missing_falls_back_to_default(self):
        theme = MermaidTheme.load("nonexistent_theme_xyz")
        assert theme.name == "default"
        assert "themeVariables" in theme.config

    def test_merge_overrides(self):
        theme = MermaidTheme.load("flutter")
        merged = theme.merge({"themeVariables": {"fontSize": "18px"}})
        assert merged.config["themeVariables"]["fontSize"] == "18px"
        # Orijinal değer korunmalı
        assert theme.config["themeVariables"].get("fontSize") != "18px"

    def test_merge_does_not_mutate_original(self):
        theme = MermaidTheme.load("default")
        original_font = theme.config["themeVariables"]["fontSize"]
        theme.merge({"themeVariables": {"fontSize": "99px"}})
        assert theme.config["themeVariables"]["fontSize"] == original_font

    def test_config_file_creates_and_cleans_up(self, tmp_path):
        theme = MermaidTheme.load("default")
        config_path_captured = None
        with theme.config_file() as cfg_path:
            config_path_captured = cfg_path
            assert cfg_path.exists()
            loaded = json.loads(cfg_path.read_text())
            assert loaded["theme"] == "base"
        # Context manager çıkınca silinmeli
        assert not config_path_captured.exists()


# ---------------------------------------------------------------------------
# MermaidThemeManager testleri
# ---------------------------------------------------------------------------

class TestMermaidThemeManager:
    @pytest.mark.parametrize("profile,expected_border", [
        ("flutter", "#0175C2"),
        ("dart", "#0175C2"),       # dart → flutter
        ("java", "#E65100"),
        ("python", "#3572A5"),
        ("react", "#00BCD4"),
        ("javascript", "#00BCD4"), # javascript → react
        ("typescript", "#00BCD4"),
        ("generic", None),         # generic → default
        ("FLUTTER", "#0175C2"),    # büyük harf insensitive
    ])
    def test_for_profile(self, profile, expected_border):
        theme = MermaidThemeManager.for_profile(profile)
        if expected_border:
            assert theme.config["themeVariables"]["primaryBorderColor"] == expected_border

    def test_for_profile_with_overrides(self):
        theme = MermaidThemeManager.for_profile(
            "flutter",
            overrides={"themeVariables": {"fontSize": "20px"}},
        )
        assert theme.config["themeVariables"]["fontSize"] == "20px"
        assert theme.config["themeVariables"]["primaryBorderColor"] == "#0175C2"

    def test_available_themes(self):
        themes = MermaidThemeManager.available_themes()
        assert "default" in themes
        assert "flutter" in themes
        assert "java" in themes
        assert "python" in themes
        assert "react" in themes

    def test_profile_to_theme(self):
        assert MermaidThemeManager.profile_to_theme("flutter") == "flutter"
        assert MermaidThemeManager.profile_to_theme("unknown") == "default"


# ---------------------------------------------------------------------------
# MermaidRenderConfig testleri
# ---------------------------------------------------------------------------

class TestMermaidRenderConfig:
    def test_defaults(self):
        config = MermaidRenderConfig()
        assert config.theme == "default"
        assert config.scale == 2
        assert config.background == "white"
        assert config.width == 900

    def test_from_manifest_full(self):
        manifest_data = {
            "theme": "flutter",
            "scale": 3,
            "background": "transparent",
            "width": 1200,
            "theme_overrides": {"themeVariables": {"fontSize": "16px"}},
        }
        config = MermaidRenderConfig.from_manifest(manifest_data)
        assert config.theme == "flutter"
        assert config.scale == 3
        assert config.background == "transparent"
        assert config.width == 1200

    def test_from_manifest_none(self):
        config = MermaidRenderConfig.from_manifest(None)
        assert config.theme == "default"

    def test_from_manifest_partial(self):
        config = MermaidRenderConfig.from_manifest({"theme": "java"})
        assert config.theme == "java"
        assert config.scale == 2  # varsayılan

    def test_resolve_theme(self):
        config = MermaidRenderConfig(theme="python")
        theme = config.resolve_theme()
        assert theme.config["themeVariables"]["primaryBorderColor"] == "#3572A5"


# ---------------------------------------------------------------------------
# Regex testleri
# ---------------------------------------------------------------------------

class TestMermaidBlockRegex:
    def test_finds_single_block(self):
        md = f"Metin\n\n```mermaid\n{SIMPLE_FLOWCHART}\n```\n\nSon"
        matches = _MERMAID_BLOCK_RE.findall(md)
        assert len(matches) == 1
        assert "graph TD" in matches[0]

    def test_finds_multiple_blocks(self):
        matches = _MERMAID_BLOCK_RE.findall(MARKDOWN_WITH_TWO_BLOCKS)
        assert len(matches) == 2

    def test_case_insensitive(self):
        md = "```MERMAID\ngraph TD\n    A-->B\n```"
        matches = _MERMAID_BLOCK_RE.findall(md)
        assert len(matches) == 1

    def test_no_false_positives(self):
        md = "```python\nprint('hello')\n```"
        matches = _MERMAID_BLOCK_RE.findall(md)
        assert len(matches) == 0


# ---------------------------------------------------------------------------
# MermaidRenderer testleri (mmdc mock'lu)
# ---------------------------------------------------------------------------

def _make_mock_proc(returncode=0, stderr="", stdout=""):
    mock = MagicMock()
    mock.returncode = returncode
    mock.stderr = stderr
    mock.stdout = stdout
    return mock


@pytest.fixture
def renderer():
    config = MermaidRenderConfig(theme="flutter", scale=2, width=900)
    with patch("shutil.which", return_value="/usr/bin/mmdc"):
        return MermaidRenderer(config)


class TestMermaidRenderer:

    @patch("subprocess.run")
    def test_process_markdown_renders_blocks(self, mock_run, renderer, tmp_path):
        """İki mermaid bloğu PNG'ye dönüşmeli."""
        assets_dir = tmp_path / "assets"

        # mmdc başarılı → PNG dosyasını elle oluştur
        def fake_run(cmd, **kwargs):
            out_path = Path(cmd[cmd.index("--output") + 1])
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_bytes(b"fake_png_data")
            return _make_mock_proc(returncode=0)

        mock_run.side_effect = fake_run

        result = renderer.process_markdown(
            md_content=MARKDOWN_WITH_TWO_BLOCKS,
            assets_dir=assets_dir,
            chapter_alias="bolum-01",
        )

        assert result.total == 2
        assert result.rendered == 2
        assert result.cached == 0
        assert result.failed == 0
        assert "![Şekil 1](assets/fig_bolum-01_01.png)" in result.output_md
        assert "![Şekil 2](assets/fig_bolum-01_02.png)" in result.output_md
        assert "```mermaid" not in result.output_md

    @patch("subprocess.run")
    def test_cache_hit_skips_render(self, mock_run, renderer, tmp_path):
        """İkinci çalıştırmada mevcut PNG'ler yeniden render edilmemeli."""
        assets_dir = tmp_path / "assets"
        assets_dir.mkdir()

        def fake_run(cmd, **kwargs):
            out_path = Path(cmd[cmd.index("--output") + 1])
            out_path.write_bytes(b"fake_png_data")
            return _make_mock_proc(returncode=0)

        mock_run.side_effect = fake_run

        # İlk çalıştırma
        result1 = renderer.process_markdown(
            md_content=MARKDOWN_WITH_TWO_BLOCKS,
            assets_dir=assets_dir,
            chapter_alias="bolum-01",
        )
        assert result1.rendered == 2

        # İkinci çalıştırma — cache'den gelmeli
        mock_run.reset_mock()
        mock_run.side_effect = None  # artık çağrılmamalı
        result2 = renderer.process_markdown(
            md_content=MARKDOWN_WITH_TWO_BLOCKS,
            assets_dir=assets_dir,
            chapter_alias="bolum-01",
        )
        assert result2.rendered == 0
        assert result2.cached == 2
        mock_run.assert_not_called()

    @patch("subprocess.run")
    def test_render_failure_keeps_original_block(self, mock_run, renderer, tmp_path):
        """mmdc hata verirse orijinal blok HTML yorumlu olarak kalmalı."""
        assets_dir = tmp_path / "assets"
        mock_run.return_value = _make_mock_proc(
            returncode=1, stderr="Parse error at line 2"
        )

        simple_md = f"```mermaid\n{SIMPLE_FLOWCHART}\n```"
        result = renderer.process_markdown(
            md_content=simple_md,
            assets_dir=assets_dir,
            chapter_alias="bolum-01",
        )

        assert result.failed == 1
        assert result.rendered == 0
        assert "MERMAID RENDER HATASI" in result.output_md
        assert "```mermaid" in result.output_md  # blok korunmalı

    @patch("subprocess.run")
    def test_cache_invalidated_when_source_changes(self, mock_run, renderer, tmp_path):
        """Mermaid kaynağı değişince cache geçersiz olmalı, yeniden render edilmeli."""
        assets_dir = tmp_path / "assets"
        assets_dir.mkdir()

        def fake_run(cmd, **kwargs):
            out_path = Path(cmd[cmd.index("--output") + 1])
            out_path.write_bytes(b"fake_png_data")
            return _make_mock_proc(returncode=0)

        mock_run.side_effect = fake_run
        md_v1 = "```mermaid\ngraph TD\n    A-->B\n```"
        renderer.process_markdown(md_v1, assets_dir, "ch")

        mock_run.side_effect = fake_run
        md_v2 = "```mermaid\ngraph TD\n    A-->B-->C\n```"  # farklı kaynak
        result = renderer.process_markdown(md_v2, assets_dir, "ch")

        assert result.rendered == 1  # cache miss → yeniden render
        assert result.cached == 0

    def test_cmd_contains_all_flags(self, renderer, tmp_path):
        """mmdc komut satırı doğru argümanlar içermeli."""
        src = tmp_path / "src.mmd"
        out = tmp_path / "out.png"
        cfg = tmp_path / "cfg.json"
        cmd = renderer._build_cmd(src, out, cfg)

        assert "--input" in cmd
        assert str(src) in cmd
        assert "--output" in cmd
        assert str(out) in cmd
        assert "--configFile" in cmd
        assert str(cfg) in cmd
        assert "--scale" in cmd
        assert "2" in cmd
        assert "--backgroundColor" in cmd
        assert "white" in cmd

    @patch("subprocess.run")
    def test_markdown_without_mermaid_unchanged(self, mock_run, renderer, tmp_path):
        """Mermaid bloğu olmayan Markdown değişmeden döndürülmeli."""
        assets_dir = tmp_path / "assets"
        md = "# Başlık\n\nSadece metin.\n\n```python\nprint('hello')\n```"
        result = renderer.process_markdown(md, assets_dir, "ch")

        assert result.total == 0
        assert result.output_md == md
        mock_run.assert_not_called()

    def test_cache_key_depends_on_theme(self, renderer):
        """Aynı kaynak, farklı tema → farklı cache key."""
        cfg_flutter = MermaidRenderConfig(theme="flutter")
        cfg_java = MermaidRenderConfig(theme="java")
        key_flutter = MermaidRenderer._cache_key(SIMPLE_FLOWCHART, cfg_flutter.cache_fingerprint())
        key_java = MermaidRenderer._cache_key(SIMPLE_FLOWCHART, cfg_java.cache_fingerprint())
        assert key_flutter != key_java

    def test_cache_key_consistent(self, renderer):
        """Aynı girdi → her zaman aynı hash."""
        cfg = MermaidRenderConfig(theme="python")
        k1 = MermaidRenderer._cache_key(SIMPLE_FLOWCHART, cfg.cache_fingerprint())
        k2 = MermaidRenderer._cache_key(SIMPLE_FLOWCHART, cfg.cache_fingerprint())
        assert k1 == k2

    def test_cache_key_changes_when_width_changes(self):
        """width değişince cache key değişmeli."""
        src = "flowchart TD\nA --> B"
        cfg1 = MermaidRenderConfig(theme="default", width=900)
        cfg2 = MermaidRenderConfig(theme="default", width=1200)

        key1 = MermaidRenderer._cache_key(src, cfg1.cache_fingerprint())
        key2 = MermaidRenderer._cache_key(src, cfg2.cache_fingerprint())

        assert key1 != key2

    def test_cache_key_changes_when_theme_overrides_change(self):
        """theme_overrides değişince cache key değişmeli."""
        src = "flowchart TD\nA --> B"
        cfg1 = MermaidRenderConfig(
            theme="default",
            theme_overrides={"themeVariables": {"fontSize": "15px"}},
        )
        cfg2 = MermaidRenderConfig(
            theme="default",
            theme_overrides={"themeVariables": {"fontSize": "18px"}},
        )

        assert MermaidRenderer._cache_key(src, cfg1.cache_fingerprint()) != (
            MermaidRenderer._cache_key(src, cfg2.cache_fingerprint())
        )

    @patch("subprocess.run")
    @patch("shutil.which", return_value="/usr/bin/mmdc")
    def test_timeout_value_passed_to_subprocess(self, mock_which, mock_run, tmp_path):
        """subprocess.run timeout argümanı config.timeout_seconds ile gelmeli."""
        cfg = MermaidRenderConfig(timeout_seconds=7)
        renderer = MermaidRenderer(cfg)

        # PNG oluştur
        def fake_run(cmd, **kwargs):
            out_path = Path(cmd[cmd.index("--output") + 1])
            out_path.write_bytes(b"fake_png_data")
            return _make_mock_proc(returncode=0)

        mock_run.side_effect = fake_run

        result = renderer.render_string(
            mermaid_src=SIMPLE_FLOWCHART,
            output_path=tmp_path / "test.png",
        )

        assert result.success
        # timeout argümanı 7 ile çağrılmış olmalı
        assert mock_run.call_args[1]["timeout"] == 7

    @patch("subprocess.run")
    @patch("shutil.which", return_value="/usr/bin/mmdc")
    def test_timeout_error_message_is_dynamic(self, mock_which, mock_run, tmp_path):
        """Timeout hata mesajı sabit değil, config değerini göstermeli."""
        cfg = MermaidRenderConfig(timeout_seconds=7)
        renderer = MermaidRenderer(cfg)

        mock_run.side_effect = subprocess.TimeoutExpired(cmd=["mmdc"], timeout=7)

        result = renderer.render_string(
            mermaid_src=SIMPLE_FLOWCHART,
            output_path=tmp_path / "test.png",
        )

        assert result.success is False
        assert "7 saniye" in result.error
