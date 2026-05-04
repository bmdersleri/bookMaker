"""TextCleaner — LLM çıktısındaki yazım/tırnak/biçim hatalarını düzeltir.
Saf Python regex, 0 token, <10ms.

Kullanım:
    text = TextCleaner.clean(raw_text)
    text = TextCleaner.clean_code("some java code")
"""

from __future__ import annotations

import re
from typing import ClassVar


class TextCleaner:
    """Tüm yazım/tırnak/biçim düzeltmeleri. Hiç LLM çağırmaz."""

    # ----------------------------------------------------------
    # TIRNAK DÜZELTMELERİ
    # ----------------------------------------------------------

    QUOTE_FIXES: ClassVar[list[tuple[str, str]]] = [
        # Düz tırnak dengesi: """ ... " → çift tırnak iç içeyse düzelt
        (r'"(?=[^\s"])', '"'),          # Açılış " → "
        (r'(?<=[^\s"])"', '"'),         # Kapanış " → "
        # Tek tırnak dengesi
        (r"'(?=[^\s'])" , "'"),         # Açılış ' → '
        (r"(?<=[^\s'])'" , "'"),        # Kapanış ' → '
        # Ters tırnakları düzelt
        (r'[""]', '"'),                 # " → "
        (r'[""]', '"'),                 # " → "
        # Art arda 3+ tırnak → 1 çift
        (r'""""', '""'),
        (r"''''", "''"),
        # Kod içinde tırnak dengesi (önemli: String literal'ler)
        # Bu regex kod blokları dışında çalışır
    ]

    # ----------------------------------------------------------
    # BOŞLUK DÜZELTMELERİ
    # ----------------------------------------------------------

    SPACE_FIXES: ClassVar[list[tuple[str, str]]] = [
        # Çoklu boşluk → tek (heading ve kod blokları dışında)
        (r'(?<![#\n])  +', ' '),
        # Satır sonu boşlukları
        (r' +\n', '\n'),
        # Noktalama öncesi boşluk
        (r' +\.', '.'),
        (r' +\,', ','),
        (r' +\?', '?'),
        (r' +\!', '!'),
        (r' +\:', ':'),
        (r' +\;', ';'),
        # Noktalama sonrası boşluk
        # NOT: Java'daki System.out.println() bozulmasın diye
        # ".Kelime" → ". Kelime" dönüşümü KALDIRILDI
        # (Java dot notation ile çakışıyor)
        # BUNUN YERİNE: Java dot notation'daki boşlukları düzelt
        # System. out. println() → System.out.println()
        (r'(\w+)\.\s+(\w+)\.\s+(\w+)\s*\(', r'\1.\2.\3('),
        (r'\?([A-Za-z])', r'? \1'),
        (r'\!([A-Za-z])', r'! \1'),
        # Parantez içi boşluk
        (r'\(\s+', '('),
        (r'\s+\)', ')'),
        (r'\[\s+', '['),
        (r'\s+\]', ']'),
        # Art arda 3+'dan fazla newline → 2
        (r'\n{4,}', '\n\n\n'),
    ]

    # ----------------------------------------------------------
    # TİRE / ÇİZGİ DÜZELTMELERİ
    # ----------------------------------------------------------

    DASH_FIXES: ClassVar[list[tuple[str, str]]] = [
        # -- → uzun çizgi (—)
        (r' -- ', ' — '),
        # İki kelime arası kısa çizgi
        (r'(?<=\w)-(?=\w)', '-'),       # Zaten doğru
        # Liste işaretleri
        (r'^\* ', '* '),                # Zaten doğru
        (r'^- ', '- '),                 # Zaten doğru
    ]

    # ----------------------------------------------------------
    # BAŞLIK DÜZELTMELERİ
    # ----------------------------------------------------------

    HEADING_FIXES: ClassVar[list[tuple[str, str]]] = [
        # #Başlık → # Başlık
        (r'^#([^# \n])', r'# \1'),
        (r'^##([^# \n])', r'## \1'),
        (r'^###([^# \n])', r'### \1'),
        (r'^####([^# \n])', r'#### \1'),
        # Başlık sonrası fazla boşluk
        (r'^(#{1,6})\s{2,}', r'\1 '),
        # ### sonrası H4 gibi düzelt
        (r'^#{5,6}\s+', '#### '),       # H5/H6 → H4
    ]

    # ----------------------------------------------------------
    # KOD BLOK DÜZELTMELERİ
    # ----------------------------------------------------------

    CODE_FIXES: ClassVar[list[tuple[str, str]]] = [
        # ```den hemen sonra karakter varsa araya newline
        (r'```(\w+)([^\n])', r'```\1\n\2'),
        # ``` öncesi boşluk
        (r'[^\n]```', '\n```'),
        # Kapanış ``` sonrası boşluk
        (r'```\s+$', '```'),
        # Kod bloğu içinde satır sonu boşlukları
        # (kod blokları içinde çalışmamalı — ayrı modül)
    ]

    # ----------------------------------------------------------
    # TÜRKÇE KARAKTER NORMALİZASYONU
    # ----------------------------------------------------------

    TURKISH_FIXES: ClassVar[list[tuple[str, str]]] = [
        # Türkçe karakter düzeltmeleri
        # Not: Bu düzeltmeler metin içinde geçen yaygın hataları hedefler
        # Kod blokları otomatik olarak korunur (extract/restore mekanizması ile)
        (r'\bSik yapilan\b', 'Sık yapılan'),
        (r'\bSik karsilasilan\b', 'Sık karşılaşılan'),
        (r'\bonek\b', 'örnek'),
        (r'\bOrnek\b', 'Örnek'),
        (r'\bI\;lkel\b', 'İlkel'),
        (r'\bilkel\b', 'ilkel'),
        (r'\bKar\[Y\aYt\b', 'Karşılaştır'),
        (r'\bSecenek\b', 'Seçenek'),
        (r'\bsecenek\b', 'seçenek'),
        (r'\bUygulama\b', 'Uygulama'),
        # Genel: ı→i (sadece bazı durumlarda, fazla genelleme yapma)
        (r'\byanlis\b', 'yanlış'),
        (r'\bYanlis\b', 'Yanlış'),
        (r'\bogrenci\b', 'öğrenci'),
        (r'\bOgrenci\b', 'Öğrenci'),
    ]

    # ----------------------------------------------------------
    # DİĞER
    # ----------------------------------------------------------

    OTHER_FIXES: ClassVar[list[tuple[str, str]]] = [
        # ... → …
        (r'\.\.\.(\.)*', '…'),
        # 3+ boş satır → 2
        (r'\n\n\n\n+', '\n\n\n'),
        # Yalnızca boşluk içeren satırlar → tamamen boş
        (r'^[ \t]+\n', '\n', re.MULTILINE),
        # Sayfa sonu: \newpage → \newpage (zaten doğru)
        # Dos başı/sonu boşluk
        (r'^\s+', ''),
        (r'\s+$', ''),
    ]

    # ----------------------------------------------------------
    # ANA METOT: clean
    # ----------------------------------------------------------

    @classmethod
    def clean(cls, text: str) -> str:
        """Tüm düzeltmeleri sırayla uygula. 0 LLM, saf regex."""
        if not text:
            return text

        # Sıra önemli: önce kod bloklarını koru, sonra düzelt
        blocks = cls._extract_protected_blocks(text)
        text = blocks["clean"]

        # 1. Boşluk düzeltmeleri
        text = cls._apply(cls.SPACE_FIXES, text)

        # 2. Tırnak düzeltmeleri
        text = cls._apply(cls.QUOTE_FIXES, text)

        # 3. Başlık düzeltmeleri
        text = cls._apply(cls.HEADING_FIXES, text, re.MULTILINE)

        # 4. Kod blokları (blok dışındaki)
        text = cls._apply(cls.CODE_FIXES, text)

        # 5. Türkçe karakter
        text = cls._apply(cls.TURKISH_FIXES, text)

        # 6. Tire/çizgi
        text = cls._apply(cls.DASH_FIXES, text)

        # 7. Diğer
        text = cls._apply(cls.OTHER_FIXES, text)

        # Kod bloklarını geri yerleştir
        text = cls._restore_blocks(text, blocks["blocks"])

        return text.strip() + "\n"

    @classmethod
    def clean_code(cls, code: str) -> str:
        """Kod blokları için özel temizlik (Java kodu)."""
        if not code:
            return code
        # Satır sonu boşlukları
        code = re.sub(r' +\n', '\n', code)
        # Fazla boş satır
        code = re.sub(r'\n{3,}', '\n\n', code)
        # Baş sonu boşluk
        code = code.strip()
        return code

    @classmethod
    def clean_heading(cls, heading: str) -> str:
        """Başlık metnini temizle."""
        h = heading.strip()
        # Art arda boşlukları tek yap
        h = re.sub(r'  +', ' ', h)
        # Baştaki/sondaki noktalama
        h = h.strip('.,;:!? ')
        return h

    # ----------------------------------------------------------
    # YARDIMCILAR
    # ----------------------------------------------------------

    @classmethod
    def _apply(cls, fix_list: list, text: str,
               flags: int = 0) -> str:
        """Regex düzeltme listesini uygula."""
        for fix in fix_list:
            if len(fix) == 3:
                pattern, replacement, extra_flags = fix
                text = re.sub(pattern, replacement, text,
                              flags=flags | extra_flags)
            else:
                pattern, replacement = fix
                text = re.sub(pattern, replacement, text, flags=flags)
        return text

    PLACEHOLDER_PREFIX = "CODEBLOCK_PLACEHOLDER_"

    @classmethod
    def _extract_protected_blocks(cls, text: str) -> dict:
        """Kod bloklarını geçici olarak çıkar, yerine placeholder koy.

        Hem ```lang\n...``` hem de ```...``` (dil belirtilmemiş) formatını destekler.
        """
        blocks = []
        result_parts = []
        last_end = 0

        # Daha esnek pattern: ``` ardından isteğe bağlı dil, isteğe bağlı newline
        pattern = re.compile(r'```(\w*)\s*\n(.*?)```', re.DOTALL)
        for match in pattern.finditer(text):
            result_parts.append(text[last_end:match.start()])
            placeholder = f"\n\n{cls.PLACEHOLDER_PREFIX}{len(blocks)}\n\n"
            result_parts.append(placeholder)
            blocks.append(match.group(0))
            last_end = match.end()
        result_parts.append(text[last_end:])

        return {
            "clean": "".join(result_parts),
            "blocks": blocks,
        }

    @classmethod
    def _restore_blocks(cls, text: str, blocks: list[str]) -> str:
        """Placeholderlari asil kod bloklariyla degistir."""
        if not blocks:
            return text
        for i, block in enumerate(blocks):
            placeholder = f"{cls.PLACEHOLDER_PREFIX}{i}"
            if placeholder in text:
                text = text.replace(placeholder, f"\n\n{block}\n\n")
        return text


    @classmethod
    def quick_clean(cls, text: str) -> str:
        """Hızlı temizlik — sadece en kritik düzeltmeler.

        Üretim hattında son bir pas olarak kullanılır.
        Kod bloklarını korumaz, sadece metin temizliği yapar.
        """
        if not text:
            return text
        # Satır sonu boşluk
        text = re.sub(r' +\n', '\n', text)
        # Çoklu boşluk → tek
        text = re.sub(r'  +', ' ', text)
        # Nokta öncesi boşluk
        text = re.sub(r' \.', '.', text)
        # Art arda 3+ newline → 2
        text = re.sub(r'\n{4,}', '\n\n\n', text)
        # Baş-son boşluk
        text = text.strip()
        return text + "\n"
