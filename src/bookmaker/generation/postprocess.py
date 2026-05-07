"""Normalizasyon — LLM çıktısını yapılandırılmış bölüm dosyasına dönüştürür.
Hiçbir meta etiketi (CODE_META, SECTION_META) kullanılmaz.
Tüm format işlemleri Python kodu ile yapılır."""

from __future__ import annotations

import re
from pathlib import Path

from bookmaker.core.config import BookConfig
from bookmaker.generation.clean_text import TextCleaner

# ============================================================
# HEADING NORMALIZASYONU
# ============================================================

def normalize_headings(text: str) -> str:
    """Heading seviyelerini düzeltir:
    - İlk # H1 olarak kalır, sonraki tüm #'lar ## olur (H2)
    - H1 başlığından "Bölüm N:", "Chapter N:" öneki temizlenir
    - H2/H3 başlıklarından manuel numaralandırma temizlenir (örn. "5.1 xxx" → "xxx")
    - H3 ve H4 seviyeleri korunur
    - Front matter (---) atlanır
    - Kod blokları içi atlanır
    - LLM meta-yorum satırları temizlenir (örn. "Harika bir spesifikasyon!...")
    """
    lines = text.splitlines()
    result = []
    in_front_matter = text.lstrip().startswith("---")
    fm_dash_count = 0  # front matter icindeki --- sayaci
    in_code_block = False
    found_h1 = False
    front_matter_ended = False  # front matter kapandi, H1 oncesi meta temizligi aktif

    for line in lines:
        stripped = line.rstrip()

        # Front matter geçişi: ilk --- açar, ikinci --- kapatır
        if stripped == "---" and not in_code_block and not found_h1:
            if in_front_matter:
                fm_dash_count += 1
                if fm_dash_count >= 2:
                    in_front_matter = False
                    front_matter_ended = True
                result.append(line)
                continue
            elif front_matter_ended:
                # FM sonrasi --- : bunu atla (LLM'in ekledigi gereksiz separator)
                continue

        # Kod blokları
        if stripped.startswith("```"):
            in_code_block = not in_code_block
            result.append(line)
            continue

        if in_front_matter or in_code_block:
            result.append(line)
            continue

        # LLM meta-yorumu temizle: front matter'dan H1'e kadar
        # "harika", "işte" gibi geçiş cümlelerini ve boş satırları temizle
        if front_matter_ended and not found_h1:
            if not stripped:
                continue  # skip blank lines between FM and H1
            meta_patterns = [
                r'^Harika bir', r'^İşte', r'^Şimdi', r'^Harika!',
                r'^Mükemmel', r'^Tamam,', r'^Peki,', r'^Anlaşıldı',
                r'^Güzel,', r'^Evet,', r'^Doğru,',
            ]
            if any(re.match(p, stripped) for p in meta_patterns):
                continue  # skip meta-commentary, keep checking for H1

        # Heading düzeltme
        match = re.match(r"^(#{1,6})\s+", stripped)
        if match:
            level = len(match.group(1))
            heading_text = stripped[match.end():]

            if level == 1:
                if not found_h1:
                    found_h1 = True
                    front_matter_ended = False  # H1 bulundu, meta temizliğini kapat
                    # H1 başlığından "Bölüm N:", "Chapter N:" önekini temizle
                    cleaned = re.sub(
                        r'^(Bölüm|Chapter|Bolum)\s+\d+[:\-.]\s*',
                        '', heading_text, flags=re.IGNORECASE
                    ).strip()
                    if cleaned:
                        line = "# " + cleaned
                else:
                    # İkinci H1 → H2'ye düşür
                    line = "##" + line[line.index("#") + 1:]
            elif level >= 2:
                # H2/H3 başlıklarından manuel numaralandırmayı temizle
                # "5.1 String Sınıfı..." → "String Sınıfı..."
                # "1.7 StringTokenizer..." → "StringTokenizer..."
                cleaned = re.sub(
                    r'^\d+\.\d+\.?\s*', '', heading_text
                ).strip()
                if cleaned and cleaned != heading_text.strip():
                    line = "#" * level + " " + cleaned
            if level > 4:
                # H5/H6 → H4'e yükselt
                line = "####" + line[line.index("#") + len(match.group(1)):]

        result.append(line)

    return "\n".join(result)


# ============================================================
# FRONT MATTER
# ============================================================

def build_front_matter(chapter_id: str, title: str, config: BookConfig | None = None) -> str:
    """Manifest'teki bilgileri kullanarak YAML front matter olusturur.

    Args:
        chapter_id: Bolum kimligi (orn. bolum-16)
        title: Bolum basligi
        config: Kitap config (None = varsayilan degerler, str = uyari + varsayilan)

    Returns:
        YAML front matter blogu (--- ile cevrili)

    Not: config yanlislikla string gecilirse uyari verir, varsayilan degerlerle
    devam eder (cokmez). normalize() fonksiyonu icinden dogru cagrilir:
        ensure_front_matter(text, chapter_id, title, config)
        -> build_front_matter(chapter_id, title, config)
    """
    # Saglamlik: yanlislikla string gecilmisse uyar
    if isinstance(config, str):
        import warnings
        warnings.warn(
            f"build_front_matter: 'config' parametresine BookConfig yerine "
            f"string gecildi ('{config[:50]}...'). Varsayilan degerler kullaniliyor. "
            f"Dogru kullanim: build_front_matter(chapter_id, title, config)",
            UserWarning, stacklevel=2,
        )
        config = None

    # Config'ten degerleri al (yoksa varsayilan)
    author = config.author if config else "Ismail Kirbas"
    year = config.year if config else 2026
    subtitle = f'"{config.title}"' if config else '"Kitap"'
    project_alias = config.book_id if config else "kitap"

    return f"""---
title: "{title}"
subtitle: {subtitle}
author: "{author}"
date: "{year}"
lang: tr-TR
documentclass: report
toc: true
toc-depth: 3
numbersections: true
repo: bmdersleri
project-alias: {project_alias}
chapter-alias: {chapter_id}
chapter_id: {chapter_id}
chapter_type: core
automation_profile: academic_technical_book_v1
numbering: auto
github_slug: {chapter_id}
qr_policy: dual_for_code_examples
asset_policy: manual_override
---"""


def _build_legacy_frontmatter(chapter_id: str, title: str) -> str:
    return f"""---
title: "{title}"
chapter_id: {chapter_id}
chapter_spec: chapter_spec_v0_1
processing_stage: authoring_source
placeholder_policy: source_template
snippet_policy: non_meta_code_is_explanatory
---"""


def ensure_frontmatter(text: str, chapter_id: str, title: str) -> str:
    """Legacy front matter API'si."""
    if text.lstrip().startswith("---"):
        end = text.find("---", 3)
        if end != -1:
            return text
    return _build_legacy_frontmatter(chapter_id, title) + "\n" + text.lstrip("\n")


def fix_heading_hierarchy(text: str) -> str:
    """Legacy heading normalizer API'si."""
    return normalize_headings(text)


def _filename_from_code(code: str, index: int) -> str:
    match = re.search(r"//\s*(?:Dosya|D)\s*:\s*([^\r\n]+)", code)
    if match:
        return match.group(1).strip()
    return f"snippet_{index:02d}.java"


def auto_code_meta(text: str, chapter_id: str) -> str:
    """Legacy CODE_META injector API'si."""
    if "CODE_META" in text:
        return text

    pattern = re.compile(r"```(?P<language>[A-Za-z0-9_+\-.]*)\s*\n(?P<code>.*?```)", re.DOTALL)
    counter = 0

    def add_meta(match: re.Match[str]) -> str:
        nonlocal counter
        counter += 1
        language = match.group("language") or "text"
        code = match.group("code")
        filename = _filename_from_code(code, counter)
        meta = (
            "<!-- CODE_META\n"
            f"id: {chapter_id}_kod{counter:02d}\n"
            f"file: {filename}\n"
            f"language: {language}\n"
            "-->\n"
        )
        return meta + match.group(0)

    return pattern.sub(add_meta, text)


def process(text: str, chapter_id: str, title: str) -> str:
    """Legacy postprocess pipeline API'si."""
    text = ensure_frontmatter(text, chapter_id, title)
    text = fix_heading_hierarchy(text)
    text = auto_code_meta(text, chapter_id)
    return text


def ensure_front_matter(text: str, chapter_id: str, title: str,
                        config: BookConfig | None = None) -> str:
    """Metnin başına front matter ekler (H1 başlığı korur)."""
    if text.lstrip().startswith("---"):
        # Mevcut front matter varsa koru
        end = text.find("---", 3)
        if end != -1:
            return text
    # Front matter yoksa başa ekle, H1'i koru
    fm = build_front_matter(chapter_id, title, config)
    return fm + "\n\n" + text.lstrip("\n")


# ============================================================
# BÖLÜM AYRIŞTIRMA
# ============================================================

def extract_sections(text: str) -> list[dict]:
    """Metni H2 başlıklarına göre bölümlere ayırır.

    Returns:
        [{'heading': 'Bölüm özeti', 'content': '...', 'order': 1}, ...]
    """
    in_front_matter = text.lstrip().startswith("---")
    in_code_block = False
    sections = []
    current_heading = None
    current_lines = []
    order = 0

    for line in text.splitlines():
        stripped = line.rstrip()

        # Front matter geçişi
        if in_front_matter and stripped == "---":
            in_front_matter = False
            continue
        if in_front_matter:
            continue

        # Kod blokları
        if stripped.startswith("```"):
            in_code_block = not in_code_block
            if current_heading is not None:
                current_lines.append(line)
            continue

        if in_code_block:
            if current_heading is not None:
                current_lines.append(line)
            continue

        # H1 başlık (front matter'dan hemen sonraki)
        if re.match(r"^#\s+", stripped):
            if current_heading is not None:
                sections.append({
                    "heading": current_heading,
                    "content": "\n".join(current_lines),
                    "order": order,
                })
                order += 1
            current_heading = "__title__"  # Özel: bölüm başlığı
            current_lines = []
            continue

        # H2 başlık
        if re.match(r"^##\s+", stripped):
            if current_heading is not None:
                sections.append({
                    "heading": current_heading,
                    "content": "\n".join(current_lines),
                    "order": order,
                })
                order += 1
            current_heading = stripped.lstrip("# ")
            current_lines = []
            continue

        if current_heading is not None:
            current_lines.append(line)

    # Son bölümü ekle
    if current_heading is not None and current_lines:
        sections.append({
            "heading": current_heading,
            "content": "\n".join(current_lines),
            "order": order,
        })

    return sections


# ============================================================
# EKSİK BÖLÜM TESPİTİ
# ============================================================
# Anahtarlar ASCII'dir (enrichment type_map ile uyumlu).
# Turkish arama terimleri başlıklarda Türkçe karakter eşleştirmesi için.

_STANDARD_END_SECTIONS = {
    "ozet": "özet",
    "sozluk": "sözlük",
    "soru": "soru",
    "alistirma": "alıştırma",
    "hata": "hata",
    "kopru": "köprü",
    "laboratuvar": "laboratuvar",
    "proje": "proje",
    "rubrik": "rubrik",
    "kaynak": "kaynak",
}

# Türkçe karakter normalizasyonu için eşleme
_TURKISH_CHARS = str.maketrans("öüşığçÖÜŞİĞÇ", "ousigcOUSIGC")


def _ascii_lower(s: str) -> str:
    """Türkçe karakterleri ASCII'ye indirgeyip küçük harf yapar."""
    return s.translate(_TURKISH_CHARS).lower()


def detect_missing_sections(text: str) -> list[dict]:
    """Hangi standart bölüm sonu yapılarının eksik olduğunu tespit eder.

    Returns:
        [{'key': 'ozet', 'title': 'Bölüm özeti', 'existing': False}, ...]
    """
    sections = extract_sections(text)
    existing_headings = [_ascii_lower(s["heading"]) for s in sections]

    missing = []
    for ascii_key, turkish_term in _STANDARD_END_SECTIONS.items():
        # Hem ASCII anahtarı hem Türkçe terimi başlıklarda ara
        found = any(
            ascii_key in h or turkish_term in h
            for h in existing_headings
        )
        # Başlık oluştur: Türkçe terimin ilk harfini büyüt
        title = turkish_term[0].upper() + turkish_term[1:] if turkish_term else ascii_key
        missing.append({
            "key": ascii_key,
            "title": title,
            "existing": found,
        })

    return missing


# ============================================================
# KOD / MERMAID ÇIKARMA
# ============================================================

def extract_code_blocks(text: str, language: str = "java") -> list[dict]:
    """Belirtilen dildeki kod bloklarını çıkarır.

    Returns:
        [{'index': 0, 'code': '...', 'language': 'java', 'start': 100, 'end': 250}, ...]
    """
    pattern = re.compile(
        r"```" + language + r"\s*\n(.*?)```", re.DOTALL
    )
    return [
        {
            "index": i,
            "code": match.group(1).strip(),
            "language": language,
            "start": match.start(),
            "end": match.end(),
        }
        for i, match in enumerate(pattern.finditer(text))
    ]


def extract_mermaid_blocks(text: str) -> list[dict]:
    """Mermaid bloklarını çıkarır.

    Returns:
        [{'index': 0, 'code': '...', 'start': 100, 'end': 250}, ...]
    """
    pattern = re.compile(r"```mermaid\s*\n(.*?)```", re.DOTALL)
    return [
        {
            "index": i,
            "code": match.group(1).strip(),
            "start": match.start(),
            "end": match.end(),
        }
        for i, match in enumerate(pattern.finditer(text))
    ]


# ============================================================
# BİRLEŞTİRME
# ============================================================

def insert_section(text: str, section_title: str, section_content: str,
                  before_heading: str | None = None,
                  turkish_terms: list[str] | None = None) -> str:
    """Metne yeni bir H2 bölümü ekler. Mükerrer başlıkları önler.

    Args:
        text: Mevcut metin
        section_title: Eklenecek bölüm başlığı (sadece metin, ## eklenir)
        section_content: Bölüm içeriği (markdown)
        before_heading: Varsa bu başlıktan önce ekle
        turkish_terms: Bu terimler geçen başlık varsa ekleme (örn: ["özet", "ozet"])

    Returns:
        Güncellenmiş metin
    """
    # Mükerrer kontrolü: benzer başlık zaten var mı?
    if turkish_terms:
        existing_h2 = re.findall(r'^##\s+(.+)$', text, re.MULTILINE)
        for h2 in existing_h2:
            h2_lower = h2.lower().translate(
                str.maketrans("öüşığçÖÜŞİĞÇ", "ousigcOUSIGC")
            )
            for term in turkish_terms:
                if term.lower() in h2_lower:
                    # Benzer başlık zaten var, ekleme
                    return text

    new_section = f"\n\n## {section_title}\n\n{section_content.strip()}\n"

    if before_heading:
        pattern = rf"(^|\n)(##\s+{re.escape(before_heading)})"
        match = re.search(pattern, text, re.MULTILINE)
        if match:
            pos = match.start(2)
            return text[:pos] + new_section + "\n" + text[pos:]
        return text.rstrip() + new_section

    return text.rstrip() + new_section


# ============================================================
# ANA NORMALİZASYON FONKSİYONU
# ============================================================

def _normalize_code_blocks(text: str) -> str:
    """Kod bloklarinin ``` işaretlerini 0. sütuna hizalar."""
    lines = text.splitlines()
    result = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("```"):
            # ``` markers should be at column 0
            result.append(stripped)
        else:
            result.append(line)
    return "\n".join(result)


def _cleanup_whitespace(text: str) -> str:
    """Fazla boş satırları ve gereksiz --- separator'ları temizler."""
    lines = text.splitlines()
    result = []
    blank_count = 0
    in_front_matter = False
    fm_ended = False

    for i, line in enumerate(lines):
        stripped = line.rstrip()

        # Front matter takibi
        if stripped == "---" and not fm_ended:
            if not in_front_matter:
                in_front_matter = True
            else:
                in_front_matter = False
                fm_ended = True
                # Kapanış ---'ini koru
                blank_count = 0
                result.append(line)
                continue

        # Front matter kapandıktan sonraki yalnız --- satırlarını atla
        if fm_ended and stripped == "---" and not in_front_matter:
            continue

        # Boş satır
        if not stripped:
            blank_count += 1
            if blank_count <= 2 and not in_front_matter:
                result.append("")
            elif in_front_matter:
                result.append("")
            continue

        blank_count = 0
        result.append(line)

    # Sondaki boş satırları temizle
    while result and not result[-1]:
        result.pop()

    return "\n".join(result) + "\n"


def normalize(
    text: str,
    chapter_id: str,
    title: str,
    config: BookConfig | None = None,
) -> str:
    """LLM çıktısını normalize eder: temizlik + başlıklar + front matter.

    Sıra:
    1. TextCleaner ile tırnak/boşluk/yazım düzelt (0 token)
    2. Heading seviyelerini düzelt
    3. Front matter ekle/koru
    4. Fazla boşlukları ve gereksiz separator'ları temizle

    Args:
        text: Ham LLM çıktısı
        chapter_id: Bölüm kimliği
        title: Bölüm başlığı
        config: Kitap config

    Returns:
        Normalize edilmiş bölüm metni
    """
    text = TextCleaner.clean(text)
    text = normalize_headings(text)
    text = _deduplicate_h2_sections(text)
    text = ensure_front_matter(text, chapter_id, title, config)
    text = _normalize_code_blocks(text)
    text = _cleanup_whitespace(text)
    return text.strip() + "\n"


# ============================================================
# MERMAID RENDER WRAPPER
# ============================================================


def normalize_with_mermaid(
    text: str,
    chapter_alias: str,
    chapter_content_dir: Path,
    manifest=None,
    chapter_id: str = "",
    title: str = "",
    config: BookConfig | None = None,
) -> str:
    """normalize() islemini uygular, ardindan mermaid bloklarini
    temali PNG'ye donusturur ve Markdown referanslarini gunceller.
    mmdc kurulu degilse sessizce mevcut normalize() sonucunu doner.
    """
    import shutil

    from bookmaker.production.mermaid_renderer import (
        MermaidRenderConfig,
        MermaidRenderer,
    )

    normalized = normalize(text, chapter_id, title, config)

    if shutil.which("mmdc") is None:
        return normalized

    mermaid_cfg = {}
    if manifest is not None:
        try:
            mermaid_cfg = manifest.mermaid.model_dump()
        except AttributeError:
            pass

    cfg = MermaidRenderConfig.from_manifest(mermaid_cfg)
    renderer = MermaidRenderer(cfg)

    result = renderer.process_markdown(
        md_content=normalized,
        assets_dir=chapter_content_dir / "assets",
        chapter_alias=chapter_alias,
    )
    return result.output_md


# ============================================================
# SCREENSHOT ENGINE WRAPPER
# ============================================================


def process_screenshots(
    text: str,
    chapter_alias: str,
    chapter_content_dir: Path,
    manifest=None,
) -> str:
    """Markdown icindeki isaretlenmis kod bloklarini (python plot,
    python console, jsx screenshot) ekran goruntusune donusturur.
    Playwright kurulu degilse sessizce gecer.
    """
    from bookmaker.production.screenshot_engine import ScreenshotEngine

    screenshots_cfg = {}
    if manifest is not None:
        try:
            screenshots_cfg = manifest.production.screenshots.model_dump()
        except AttributeError:
            pass

    engine = ScreenshotEngine.from_manifest(screenshots_cfg)
    if not engine.config.enabled:
        return text

    result = engine.process_markdown(
        md_content=text,
        assets_dir=chapter_content_dir / "assets",
        chapter_alias=chapter_alias,
    )
    return result.output_md


# ============================================================
# H2 BÖLÜM AYIKLAMA — Teorik derinleştirme için
# ============================================================

def _deduplicate_h2_sections(text: str) -> str:
    """Mükerrer H2 başlıklarını temizler — aynı başlıktan ikinciyi kaldırır."""
    lines = text.splitlines()
    seen_headings: set[str] = set()
    result: list[str] = []
    skip_until_next_h2 = False
    in_code_block = False

    for i, line in enumerate(lines):
        stripped = line.strip()

        if stripped.startswith("```"):
            in_code_block = not in_code_block
            if skip_until_next_h2 and not in_code_block:
                skip_until_next_h2 = False
            result.append(line)
            continue

        if in_code_block:
            result.append(line)
            continue

        h2_match = re.match(r"^##\s+(.+)$", stripped)
        if h2_match:
            heading = h2_match.group(1).strip()
            norm_key = heading.lower().translate(
                str.maketrans("öüşığçÖÜŞİĞÇ", "ousigcOUSIGC")
            )
            if norm_key in seen_headings:
                skip_until_next_h2 = True
                continue
            seen_headings.add(norm_key)
            skip_until_next_h2 = False

        if skip_until_next_h2:
            continue

        result.append(line)

    return "\n".join(result)


def extract_h2_sections(text: str) -> list[dict[str, str]]:
    """Metni H2 başlıklarına göre bölümlere ayırır.

    Her bölüm: {"heading": "H2 başlığı", "content": "içerik"}
    H1 başlığından önceki kısım "__preamble__" olarak döner.

    Kod blokları içindeki ## işaretleri heading sayılmaz.
    """
    sections = []
    lines = text.splitlines()
    current_heading = "__preamble__"
    current_lines = []
    in_code_block = False

    for line in lines:
        stripped = line.strip()

        # Kod bloğu geçişi
        if stripped.startswith("```"):
            in_code_block = not in_code_block
            current_lines.append(line)
            continue

        if in_code_block:
            current_lines.append(line)
            continue

        # H2 başlık tespiti
        if re.match(r"^##\s+", stripped) and not re.match(r"^###+\s", stripped):
            # Önceki bölümü kaydet
            if current_lines:
                sections.append({
                    "heading": current_heading,
                    "content": "\n".join(current_lines).strip(),
                })
            current_heading = re.sub(r"^##\s+", "", stripped).strip()
            current_lines = [line]
            continue

        current_lines.append(line)

    # Son bölümü kaydet
    if current_lines:
        sections.append({
            "heading": current_heading,
            "content": "\n".join(current_lines).strip(),
        })

    return sections


def deepen_theory(
    sections: list[dict[str, str]],
    deepen_fn,
    chapter_title: str,
    min_chars: int = 500,
) -> list[dict[str, str]]:
    """Her H2 bölümünü LLM ile teorik olarak derinleştirir.

    Args:
        sections: extract_h2_sections() çıktısı
        deepen_fn: (section_heading, section_content) -> genişletilmiş içerik
                   dönen çağrılabilir (genellikle LLM çağrısı)
        chapter_title: Bölüm başlığı
        min_chars: Bu karakterden kısa bölümler atlanır (ön söz vs.)

    Returns:
        Derinleştirilmiş bölümler listesi (aynı yapıda)
    """
    deepened = []
    for sec in sections:
        if sec["heading"] == "__preamble__":
            deepened.append(sec)
            continue
        if len(sec["content"]) < min_chars:
            deepened.append(sec)
            continue
        try:
            expanded = deepen_fn(
                chapter_title=chapter_title,
                section_heading=sec["heading"],
                section_content=sec["content"],
            )
            if expanded and len(expanded) > len(sec["content"]) * 0.5:
                deepened.append({"heading": sec["heading"], "content": expanded})
                print(f"    [deepen] '{sec['heading'][:50]}': "
                      f"{len(sec['content'])} → {len(expanded)} karakter")
            else:
                deepened.append(sec)
                print(f"    [deepen] '{sec['heading'][:50]}': atlandı (yeterli genişleme yok)")
        except Exception as e:
            print(f"    [deepen] '{sec['heading'][:50]}': HATA — {e}")
            deepened.append(sec)
    return deepened


def reassemble_from_sections(sections: list[dict[str, str]]) -> str:
    """Derinleştirilmiş bölümleri tekrar birleştirir."""
    parts = []
    for sec in sections:
        if sec["heading"] == "__preamble__":
            parts.append(sec["content"])
        else:
            # Heading zaten content içinde ilk satır olarak var
            parts.append(sec["content"])
    return "\n\n".join(parts)

