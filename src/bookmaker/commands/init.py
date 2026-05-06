# ruff: noqa: E501
from __future__ import annotations

from pathlib import Path
from typing import Annotated, Any

import typer
from rich.console import Console
from rich.panel import Panel
from ruamel.yaml import YAML

from bookmaker.core.time import now_iso
from bookmaker.manifest.models import BookManifest, PipelineState

console = Console()
_yaml = YAML()
_yaml.default_flow_style = False

PRESETS = ["flutter-mobil", "java-temelleri"]


FLUTTER_CHAPTERS: list[dict[str, Any]] = [
    {
        "alias": "giris",
        "title": "Flutter Ekosistemine Giriş ve İlk Uygulama",
        "topics": [
            "Flutter ve Dart ekosistemi",
            "Flutter SDK kurulumu",
            "IDE, emulator ve cihaz hazırlığı",
            "İlk Flutter projesi",
            "Hot reload ve hot restart",
            "Temel proje klasör yapısı",
        ],
        "objectives": [
            "Okuyucu Flutter’ın çapraz platform geliştirmedeki rolünü açıklayabilmeli.",
            "Flutter geliştirme ortamını kurup ilk uygulamayı çalıştırabilmeli.",
            "Hot reload ve hot restart farkını örnek üzerinden açıklayabilmeli.",
        ],
        "exclusions": ["State management ayrıntıları", "API kullanımı", "Yayınlama süreçleri"],
        "mini_project": "Kişisel karşılama kartı uygulaması",
    },
    {
        "alias": "dart-temelleri",
        "title": "Flutter İçin Dart Temelleri",
        "topics": ["Değişkenler", "Null-safety", "List/Map", "Fonksiyonlar", "Sınıflar", "Future ve async/await"],
        "objectives": [
            "Okuyucu Flutter için gerekli Dart yapılarını kullanabilmeli.",
            "Null-safety ve async/await mantığını örneklerle açıklayabilmeli.",
        ],
        "exclusions": ["Dart isolate", "Metaprogramlama", "Paket geliştirme"],
        "mini_project": "Model sınıfından beslenen basit liste ekranı",
    },
    {"alias": "widget-mantigi", "title": "Widget Mantığı ve Material Design"},
    {"alias": "layout-sistemi", "title": "Layout Sistemi: Row, Column, Stack ve Responsive Yapı"},
    {"alias": "etkilesim-formlar", "title": "Etkileşim, Formlar ve Kullanıcı Girdisi"},
    {"alias": "listeleme-dinamik-arayuzler", "title": "Listeleme, Kart Tasarımları ve Dinamik Arayüzler"},
    {"alias": "navigation-route", "title": "Navigation ve Route Yönetimi"},
    {"alias": "state-management", "title": "State Management: setState'ten Provider/Riverpod'a"},
    {"alias": "async-api-json", "title": "Async Programlama, REST API ve JSON"},
    {"alias": "yerel-veri-saklama", "title": "Yerel Veri Saklama: SharedPreferences, SQLite/Hive"},
    {"alias": "tema-responsive-erisilebilirlik", "title": "Tema, Responsive Tasarım ve Erişilebilirlik"},
    {"alias": "paketler-pluginler", "title": "Paketler, Plugin Kullanımı ve Cihaz Özellikleri"},
    {"alias": "bulut-tabanli-uygulama", "title": "Firebase/Supabase ile Bulut Tabanlı Uygulama"},
    {"alias": "test-debugging", "title": "Test, Debugging ve Hata Yönetimi"},
    {"alias": "performans-yayinlama", "title": "Performans, Yayınlama ve Dağıtım"},
    {"alias": "final-proje", "title": "Final Proje: Uçtan Uca Flutter Uygulaması"},
]


JAVA_CHAPTERS: list[dict[str, Any]] = [
    {"alias": "giris", "title": "Java Ekosistemine Giriş"},
    {"alias": "degiskenler", "title": "Değişkenler ve Veri Tipleri"},
    {"alias": "kontrol-yapilari", "title": "Kontrol Yapıları"},
    {"alias": "diziler", "title": "Diziler ve Koleksiyonlara Giriş"},
    {"alias": "metotlar", "title": "Metotlar"},
]


def _dump_yaml(path: Path, data: dict[str, Any], force: bool) -> None:
    if path.exists() and not force:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        _yaml.dump(data, f)


def _write_text(path: Path, content: str, force: bool) -> None:
    if path.exists() and not force:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _touch_gitkeep(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)
    gitkeep = path / ".gitkeep"
    if not gitkeep.exists():
        gitkeep.write_text("", encoding="utf-8")


def _default_sections() -> list[dict[str, str]]:
    return [
        {"title": "Bölümün Yol Haritası", "type": "text"},
        {"title": "Kavramsal Açıklama", "type": "text"},
        {"title": "Temel Örnek", "type": "text+code"},
        {"title": "Çalışan Mini Uygulama", "type": "text+code+screenshot"},
        {"title": "Sık Yapılan Hatalar", "type": "text"},
        {"title": "Bölüm Sonu Laboratuvarı", "type": "exercise"},
        {"title": "Özet", "type": "text"},
    ]


def _make_book_manifest(
    project_root: Path,
    preset: str,
    author: str,
    title: str,
    repo: str,
) -> dict[str, Any]:
    alias = project_root.name
    if preset == "flutter-mobil":
        chapters = FLUTTER_CHAPTERS
        book_title = title or "Flutter ile Mobil Uygulama Geliştirme"
        subtitle = "Dart Temellerinden Yayınlanabilir Mobil Uygulamaya"
        code_language = "dart"
        framework = "flutter"
        technical_profile = {
            "flutter_channel": "stable",
            "flutter_version": "3.x",
            "dart_version": "3.x",
            "material_design": "Material 3",
            "primary_platform": "android",
            "secondary_platforms": ["ios", "web"],
            "ide": ["Visual Studio Code", "Android Studio"],
            "state_management_main": "Provider veya Riverpod",
            "testing": ["flutter analyze", "flutter test", "widget test"],
        }
    elif preset == "java-temelleri":
        chapters = JAVA_CHAPTERS
        book_title = title or "Java'nın Temelleri"
        subtitle = "Programlamaya Girişten Uygulamalı Java Örneklerine"
        code_language = "java"
        framework = None
        technical_profile = {"jdk_version": "21 veya güncel LTS", "ide": ["Visual Studio Code", "IntelliJ IDEA"]}
    else:
        chapters = [{"alias": "giris", "title": "Giriş"}]
        book_title = title or alias
        subtitle = ""
        code_language = ""
        framework = None
        technical_profile = {}

    return {
        "book": {
            "title": book_title,
            "subtitle": subtitle,
            "author": author,
            "alias": alias,
            "repo": repo or f"https://github.com/bmdersleri/{alias}",
            "language": "tr",
            "version": "1.0.0",
            "edition": "1",
            "year": 2026,
        },
        "production": {
            "producer_model": "deepseek-chat",
            "observer_model": "deepseek-chat",
            "producer_params": {"temperature": 0.7, "max_tokens": 8000},
            "observer_params": {"temperature": 0.3, "max_tokens": 4000},
            "generation_mode": "chapter_based",
            "approval_required": True,
        },
        "style": {
            "target_audience": "Üniversite öğrencileri ve başlangıç-orta seviye geliştiriciler",
            "tone": "akademik ama sade, uygulama odaklı, öğrenci dostu",
            "code_language": code_language,
            "framework": framework,
            "terminology": "Türkçe açıklama + ilk geçtiği yerde İngilizce teknik terim",
            "chapter_pattern": [
                "Kavram",
                "Küçük örnek",
                "Çalışan uygulama",
                "Ekran çıktısı",
                "Kod açıklaması",
                "Sık hata",
                "Mini görev",
                "Bölüm sonu laboratuvarı",
            ],
        },
        "technical_profile": technical_profile,
        "automation": {
            "code_meta_required": True,
            "screenshot_required": preset == "flutter-mobil",
            "minimum_screenshots_per_chapter": 1 if preset == "flutter-mobil" else 0,
            "qr_policy": "dual",
            "github_code_export": True,
            "manual_asset_override": True,
        },
        "chapters": [{"alias": chapter["alias"]} for chapter in chapters],
    }


def _chapter_manifest(chapter: dict[str, Any], order: int, chapters: list[dict[str, Any]], preset: str) -> dict[str, Any]:
    refs: list[dict[str, str]] = []
    if order > 1:
        refs.append({"alias": chapters[order - 2]["alias"], "relation": "prerequisite"})
    if order < len(chapters):
        refs.append({"alias": chapters[order]["alias"], "relation": "next"})

    default_topics = [chapter["title"]]
    default_objectives = [f"Okuyucu {chapter['title']} konusundaki temel kavramları açıklayabilmeli."]
    default_exclusions = ["Bölüm kapsamı dışındaki ileri konular"]
    validation_modes = (
        ["flutter_analyze", "flutter_test", "widget_test", "screenshot_only", "review_only"]
        if preset == "flutter-mobil"
        else ["review_only"]
    )

    return {
        "chapter": {
            "title": chapter["title"],
            "alias": chapter["alias"],
            "order": order,
            "references": refs,
        },
        "scope": {
            "topics": chapter.get("topics", default_topics),
            "objectives": chapter.get("objectives", default_objectives),
            "exclusions": chapter.get("exclusions", default_exclusions),
            "mini_project": chapter.get("mini_project", "Bölüm kapsamına uygun mini uygulama"),
        },
        "structure": {
            "sections": _default_sections(),
            "estimated_pages": 18,
            "code_examples_count": 4,
            "screenshot_examples_count": 1 if preset == "flutter-mobil" else 0,
        },
        "automation": {
            "code_meta_required": True,
            "screenshot_required": preset == "flutter-mobil",
            "default_code_language": "dart" if preset == "flutter-mobil" else "java",
            "default_framework": "flutter" if preset == "flutter-mobil" else None,
            "validation_modes": validation_modes,
            "github_export": True,
            "qr_policy": "dual",
        },
    }


def _default_chapter_prompt(preset: str) -> str:
    if preset == "flutter-mobil":
        return """# Varsayılan Bölüm Üretim Promptu — Flutter Kitabı

Sen, **Flutter ile Mobil Uygulama Geliştirme** kitabı için akademik ama uygulama odaklı bölüm üreten kıdemli bir teknik yazar ve Flutter eğitmenisin.

Üretimde sana ilgili `book_manifest.yaml`, `chapter_manifest.yaml` ve varsa `chapters/<alias>/prompt.md` içeriği verilecektir.

## Genel ilkeler

- Dil Türkçedir.
- Ton akademik, sade, uygulamalı ve öğrenci dostudur.
- Kodlar modern Dart/Flutter, null-safety ve Material 3 ile uyumlu olmalıdır.
- Çıkarılabilir/test edilebilir her kod bloğundan önce `CODE_META` kullanılmalıdır.
- Her bölümde en az bir `SCREENSHOT_META` ve buna bağlı `[SCREENSHOT:...]` işareti bulunmalıdır.
- Bölüm sonunda laboratuvar görevi ve değerlendirme rubriği bulunmalıdır.

## CODE_META örneği

```yaml
<!-- CODE_META
code_id: ch01_first_flutter_app
language: dart
framework: flutter
file: lib/main.dart
project_dir: apps/chapter_01_first_flutter_app
extract: true
test: flutter_analyze
github: true
qr_policy: dual
validation_mode: runnable
screenshot_required: true
-->
```

## SCREENSHOT_META örneği

```yaml
<!-- SCREENSHOT_META
id: ch01_01_first_app_home
chapter: giris
project_dir: apps/chapter_01_first_flutter_app
route: /
device: pixel_6
theme: light
output: assets/screenshots/ch01_01_first_app_home.png
caption: "İlk Flutter uygulamasının ana ekranı."
markdown_target: "[SCREENSHOT:ch01_01_first_app_home]"
-->
```

```markdown
[SCREENSHOT:ch01_01_first_app_home]
```
"""
    return """# Varsayılan Bölüm Üretim Promptu

İlgili `book_manifest.yaml` ve `chapter_manifest.yaml` kapsamına bağlı kalarak akademik, sade ve uygulamalı bir bölüm taslağı üret.

- Bölüm kapsamı dışına taşma.
- Kod varsa `CODE_META` kullan.
- Bölüm sonunda özet, sorular, alıştırmalar ve rubrik ver.
"""


def _default_review_prompt() -> str:
    return """# Varsayılan Review Promptu

Sen gözlemci/denetleyici LLM olarak görev yapıyorsun.

Üretilen bölüm taslağını ilgili `book_manifest.yaml` ve `chapter_manifest.yaml` dosyasına göre değerlendir.

## Değerlendirme boyutları

1. Kapsam uyumu
2. Pedagojik açıklık
3. Teknik doğruluk
4. Kod kalitesi
5. Güncellik
6. Ekran çıktısı/görsel yeterlilik
7. Alıştırma ve rubrik kalitesi
8. Bölümler arası tutarlılık
9. Akademik dil ve terminoloji
10. Otomasyon uyumu

## Çıktı formatı

```markdown
# Review Raporu

## Genel Skor
...

## Güçlü Yönler
...

## Kritik Sorunlar
...

## Revizyon Önerileri
...

## Onay Durumu
approved | revision_required | rejected
```
"""


def init_command(
    path: Annotated[Path, typer.Option("--path", "-p", help="Kitap proje dizini")] = Path("."),
    preset: Annotated[str, typer.Option("--preset", help=f"Kitap preseti: {PRESETS}")] = "",
    author: Annotated[str, typer.Option("--author", help="Yazar adı")] = "",
    title: Annotated[str, typer.Option("--title", help="Kitap başlığı")] = "",
    repo: Annotated[str, typer.Option("--repo", help="Kitap repo URL'si")] = "",
    force: Annotated[bool, typer.Option("--force", help="Var olan dosyaların üzerine yaz")] = False,
) -> None:
    """Yeni project-based bookMaker kitap projesi oluşturur."""
    if preset and preset not in PRESETS:
        console.print(f"[red]Bilinmeyen preset: {preset}[/red]")
        console.print(f"Geçerli presetler: {', '.join(PRESETS)}")
        raise typer.Exit(1)

    project_root = path.resolve()
    project_root.mkdir(parents=True, exist_ok=True)

    selected_preset = preset or "empty"
    chapters = (
        FLUTTER_CHAPTERS
        if selected_preset == "flutter-mobil"
        else JAVA_CHAPTERS if selected_preset == "java-temelleri"
        else [{"alias": "giris", "title": "Giriş"}]
    )

    book_manifest_data = _make_book_manifest(
        project_root=project_root,
        preset=selected_preset,
        author=author,
        title=title,
        repo=repo,
    )
    _dump_yaml(project_root / "book_manifest.yaml", book_manifest_data, force=force)

    # Base dirs
    for subdir in [
        "prompts",
        "chapters",
        "exports/docx",
        "exports/pdf",
        "exports/md",
        "logs/production",
        "logs/errors",
        "logs/reviews",
    ]:
        _touch_gitkeep(project_root / subdir)

    _write_text(project_root / "prompts/default_chapter.md", _default_chapter_prompt(selected_preset), force)
    _write_text(project_root / "prompts/default_review.md", _default_review_prompt(), force)

    # Chapter workspaces
    for index, chapter in enumerate(chapters, start=1):
        chapter_root = project_root / "chapters" / chapter["alias"]
        content_dir = chapter_root / "content"
        revisions_dir = content_dir / "revisions"
        revisions_dir.mkdir(parents=True, exist_ok=True)
        _touch_gitkeep(revisions_dir)

        _dump_yaml(
            chapter_root / "chapter_manifest.yaml",
            _chapter_manifest(chapter, index, chapters, selected_preset),
            force=force,
        )
        _write_text(
            chapter_root / "prompt.md",
            f"""# Bölüm Özel Üretim Promptu — {chapter['title']}

Bu dosya, `{chapter['alias']}` bölümü için `prompts/default_chapter.md` üzerine ek bağlam sağlar.

## Bölüm amacı

`chapter_manifest.yaml` içindeki scope ve structure alanlarını izle.

## Üretim notu

- `chapter_manifest.yaml` içindeki `structure.sections` sırasını takip et.
- Kod bloklarında gerekiyorsa `CODE_META` kullan.
- Flutter bölümlerinde en az bir `SCREENSHOT_META` ve `[SCREENSHOT:...]` işareti kullan.
- Bölüm sonunda laboratuvar görevi ve değerlendirme rubriği bulunmalıdır.
""",
            force=force,
        )
        _write_text(content_dir / "draft.md", f"# {chapter['title']}\n\n> Taslak henüz üretilmedi.\n", force)
        _write_text(content_dir / "final.md", f"# {chapter['title']}\n\n> Final içerik henüz onaylanmadı.\n", force)

    manifest = BookManifest.load(project_root / "book_manifest.yaml")
    state = PipelineState.init_from_book_manifest(manifest, created_at=now_iso())
    state_path = project_root / "pipeline_state.yaml"
    if force or not state_path.exists():
        state.save(state_path)

    console.print(Panel(
        f"[green]Project-based kitap projesi oluşturuldu:[/green] {project_root}\n"
        f"Kitap alias : {manifest.book.alias}\n"
        f"Başlık      : {manifest.book.title}\n"
        f"Bölümler    : {len(manifest.chapters)}\n"
        f"Preset      : {selected_preset}",
        title="bookmaker init",
        border_style="green",
    ))
