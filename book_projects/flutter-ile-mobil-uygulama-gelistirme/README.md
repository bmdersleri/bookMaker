# Flutter ile Mobil Uygulama Geliştirme

Bu klasör, güncel bookMaker project-based architecture standardına göre hazırlanmış bağımsız bir kitap projesidir. Framework dosyası içermez; kitaba ait manifest, prompt, bölüm içeriği, runtime state, log ve export çıktıları bu klasör içinde kalır.

---

## Kök dosyalar

```text
flutter-ile-mobil-uygulama-gelistirme/
├── book_manifest.yaml
├── pipeline_state.yaml
├── prompts/
│   ├── default_chapter.md
│   └── default_review.md
├── chapters/
├── exports/
└── logs/
```

- `book_manifest.yaml`: Kitabın ana konfigürasyonu, üretim parametreleri ve bölüm sıralaması.
- `pipeline_state.yaml`: Framework tarafından yönetilen runtime state, kalite skorları ve otomasyon bayrakları.
- `prompts/default_chapter.md`: Varsayılan bölüm üretim promptu.
- `prompts/default_review.md`: Gözlemci LLM kalite değerlendirme promptu.
- `chapters/<chapter-alias>/chapter_manifest.yaml`: Bölüm kapsamı ve yapılandırması.
- `chapters/<chapter-alias>/prompt.md`: Bölüme özel üretim promptu.
- `chapters/<chapter-alias>/content/draft.md`: Taslak bölüm metni.
- `chapters/<chapter-alias>/content/final.md`: Onaylı final bölüm metni.
- `exports/`: DOCX, PDF ve birleşik Markdown çıktıları.
- `logs/`: Üretim, hata ve review logları.

---

## Bölüm klasörü standardı

Her bölüm aynı yapıyı izler:

```text
chapters/<chapter-alias>/
├── chapter_manifest.yaml
├── prompt.md
└── content/
    ├── draft.md
    ├── final.md
    └── revisions/
        └── .gitkeep
```

Bölüm klasörü adı, `book_manifest.yaml` içindeki `chapters[].alias` değeriyle aynı olmalıdır.

---

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

---

## Kalite kontrol

Framework kökünden:

```powershell
bookmaker check book book_projects/flutter-ile-mobil-uygulama-gelistirme --json --verbose
```

Kitap proje kökünden:

```powershell
bookmaker check book --json --verbose
```

Tek bölüm taslağı için:

```powershell
bookmaker check chapter chapters/giris/content/draft.md
```

---

## Flutter üretim ilkeleri

- Kod örnekleri modern Dart/Flutter ve null-safety ile uyumlu olmalıdır.
- Çıkarılabilir/test edilebilir her kod bloğu `CODE_META` ile işaretlenmelidir.
- Her bölümde en az bir `SCREENSHOT_META` ve `[SCREENSHOT:...]` işareti bulunmalıdır.
- QR/GitHub export politikası bölüm manifestindeki `automation` alanıyla uyumlu olmalıdır.
- Bölüm dışı ileri konular erken bölümlere taşınmamalıdır.
