"""Generation pipeline testleri."""

from pathlib import Path

from bookmaker.generation.prompts import book_prompt, chapter_prompt, outline_prompt


def test_outline_prompt_format() -> None:
    sys_p, user_p = outline_prompt("Java Giriş", "Temel kavramlar")
    assert "Java Giriş" in user_p
    assert "Temel kavramlar" in user_p
    assert "outline" in sys_p.lower()
    assert len(sys_p) > 50
    assert len(user_p) > 20


def test_chapter_prompt_format() -> None:
    sys_p, user_p = chapter_prompt(
        "Değişkenler", "# Giriş\n## Tipler\n## Örnekler",
        purpose="Veri tiplerini öğretmek",
        concepts=["int", "String", "double"],
    )
    assert "Değişkenler" in user_p
    assert "Giriş" in user_p
    assert "int" in user_p
    assert "CODE_META" in sys_p


def test_book_prompt_format() -> None:
    sys_p, user_p = book_prompt("Java Programlama", "tr-TR", "Başlangıç")
    assert "Java Programlama" in user_p
    assert "tr-TR" in user_p
    assert "Başlangıç" in user_p
    assert len(sys_p) > 50


def test_pipeline_not_ready(tmp_path: Path) -> None:
    from bookmaker.generation.pipeline import GenerationPipeline

    pipe = GenerationPipeline(tmp_path)
    assert not pipe.is_ready()

    try:
        pipe.generate_outline("test", "Test")
        assert False, "Should raise RuntimeError"
    except RuntimeError as e:
        assert "yapılandırılmamış" in str(e) or "configured" in str(e).lower()
