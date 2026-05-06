# Flutter ile Mobil Uygulama Geliştirme

Bu klasör, güncel bookMaker kitap proje yapısına göre bağımsız bir kitap projesidir. Framework dosyası içermez.

## Kök dosyalar

- `book_manifest.yaml`: Kitabın ana konfigürasyonu, üretim parametreleri ve bölüm sıralaması.
- `prompts/default_chapter.md`: Varsayılan bölüm üretim promptu.
- `prompts/default_review.md`: Gözlemci LLM kalite değerlendirme promptu.
- Her bölüm klasörü: `chapter_manifest.yaml`, `prompt.md`, `content/draft.md`, `content/final.md`, `content/revisions/`.
- `exports/`: DOCX, PDF ve birleşik Markdown çıktıları.
- `logs/`: Üretim, hata ve review logları.

## Bölüm alias listesi

1. `giris` — Flutter Ekosistemine Giriş ve İlk Uygulama
2. `dart-temelleri` — Flutter İçin Dart Temelleri
3. `widget-mantigi` — Widget Mantığı ve Material Design
4. `layout-sistemi` — Layout Sistemi: Row, Column, Stack ve Responsive Yapı
5. `etkilesim-formlar` — Etkileşim, Formlar ve Kullanıcı Girdisi
6. `listeleme-dinamik-arayuzler` — Listeleme, Kart Tasarımları ve Dinamik Arayüzler
7. `navigation-route` — Navigation ve Route Yönetimi
8. `state-management` — State Management: setState'ten Provider/Riverpod'a
9. `async-api-json` — Async Programlama, REST API ve JSON
10. `yerel-veri-saklama` — Yerel Veri Saklama: SharedPreferences, SQLite/Hive
11. `tema-responsive-erisilebilirlik` — Tema, Responsive Tasarım ve Erişilebilirlik
12. `paketler-pluginler` — Paketler, Plugin Kullanımı ve Cihaz Özellikleri
13. `bulut-tabanli-uygulama` — Firebase/Supabase ile Bulut Tabanlı Uygulama
14. `test-debugging` — Test, Debugging ve Hata Yönetimi
15. `performans-yayinlama` — Performans, Yayınlama ve Dağıtım
16. `final-proje` — Final Proje: Uçtan Uca Flutter Uygulaması
