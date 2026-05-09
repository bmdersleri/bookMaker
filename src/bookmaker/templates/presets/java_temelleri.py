"""Java Temelleri kitap preseti — varsayılan yapıyı üretir."""
from __future__ import annotations

from bookmaker.models.book import (
    BookArchitecture,
    BookProfile,
    ChapterArchEntry,
    ChapterType,
    ExportTarget,
)

CHAPTER_TITLES = [
    (1,  "Java'ya Giris ve Gelistirme Ortami",        ChapterType.intro),
    (2,  "Degiskenler, Veri Tipleri ve Operatorler",   ChapterType.core),
    (3,  "Kontrol Yapilari",                           ChapterType.core),
    (4,  "Donguler",                                   ChapterType.core),
    (5,  "Diziler",                                    ChapterType.core),
    (6,  "Metotlar",                                   ChapterType.core),
    (7,  "Nesne Tabanli Programlama: Siniflar",        ChapterType.core),
    (8,  "Kalitim ve Cok Bicimlilik",                  ChapterType.core),
    (9,  "Arayuzler ve Soyut Siniflar",                ChapterType.core),
    (10, "Istisna Yonetimi",                           ChapterType.core),
    (11, "Koleksiyonlar: List, Set, Map",              ChapterType.core),
    (12, "Generics",                                   ChapterType.core),
    (13, "Lambdalar ve Fonksiyonel Programlama",       ChapterType.core),
    (14, "Stream API",                                 ChapterType.core),
    (15, "Dosya Islemleri ve I/O",                     ChapterType.core),
    (16, "Eslisimli Programlama: Thread ve Executor",  ChapterType.core),
    (17, "Ag Programlama",                             ChapterType.core),
    (18, "Veritabani: JDBC",                           ChapterType.core),
    (19, "Birim Testi: JUnit 5",                       ChapterType.core),
    (20, "Yapim Araclari: Maven ve Gradle",            ChapterType.core),
    (21, "Tasarim Kaliplari",                          ChapterType.core),
    (22, "Java Modulleri",                             ChapterType.core),
    (23, "Modern Java: Record, Sealed, Pattern",       ChapterType.core),
    (24, "Ek A: Java API Hizli Basvuru",              ChapterType.appendix),
    (25, "Ek B: Ortak Hatalar ve Cozumleri",          ChapterType.appendix),
    (26, "Ek C: Algoritmalar ve Veri Yapilari",       ChapterType.appendix),
    (27, "Ek D: Proje Ornekleri",                     ChapterType.appendix),
]


def make_book_profile(book_id: str, author: str = "") -> BookProfile:
    """Varsayilan Java Temelleri kitap profilini olusturur."""
    return BookProfile(
        book_id=book_id,
        title="Java Temelleri",
        subtitle="Akademik ve Uygulamali Programlamaya Giris",
        author=author,
        language="tr-TR",
        audience="Universite baslangic duzeyi / meslek yuksekokulu / programlamaya giris",
        level="beginner",
        domain="programming",
        primary_code_language="java",
        export_targets=[ExportTarget.docx, ExportTarget.mkdocs],
        quality_profile="academic_technical_book_v1",
    )


def make_book_architecture(book_id: str) -> BookArchitecture:
    """Varsayilan Java Temelleri kitap mimarisini olusturur."""
    chapters = [
        ChapterArchEntry(
            chapter_id=f"chapter_{order:02d}",
            order=order,
            title=title,
            chapter_type=chapter_type,
        )
        for order, title, chapter_type in CHAPTER_TITLES
    ]
    return BookArchitecture(book_id=book_id, chapters=chapters)
