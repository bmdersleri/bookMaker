# Yeni Klasör Yapısına Uyarlama Notları

Önceki taslakta Flutter kitabı `book_profile.yaml` ve `book_architecture.yaml` dosyalarıyla kurgulanmıştı. Güncel project-based architecture standardında bu yapı `book_manifest.yaml`, `pipeline_state.yaml` ve bölüm bazlı `chapter_manifest.yaml` dosyalarına dönüştürüldü.

---

## Dönüşüm Tablosu

| Eski yaklaşım | Yeni yaklaşım |
|---|---|
| `book_profile.yaml` | `book_manifest.yaml` içine taşındı |
| `book_architecture.yaml` | `book_manifest.yaml > chapters` listesi + `chapters/<chapter-alias>/chapter_manifest.yaml` yapısına bölündü |
| `chapters/<chapter_id>/seed/` | `chapters/<chapter-alias>/chapter_manifest.yaml` |
| `chapters/<chapter_id>/outline_versions/` | Üretim logları ve review çıktıları `logs/` altında |
| `chapters/<chapter_id>/draft_versions/v001.md` | `chapters/<chapter-alias>/content/draft.md` ve gerekirse `content/revisions/v001.md` |
| `chapters/<chapter_id>/approved/` | `chapters/<chapter-alias>/content/final.md` |
| `build/exports` | `exports/docx`, `exports/pdf`, `exports/md` |
| `build/reports` | `logs/reviews`, `logs/errors`, `logs/production` |
| Framework içi kitap projesi | Framework dosyası içermeyen bağımsız kitap klasörü |

---

## Korunan İlkeler

- Flutter/Dart teknik profili korunmuştur.
- Her bölümde `scope`, `structure` ve `automation` alanları vardır.
- Runtime state `chapter_manifest.yaml` içinde değil, `pipeline_state.yaml` içinde tutulur.
- Bölümler arası bağlantılar klasör yolu veya bölüm numarası yerine alias ile tanımlanır.
- Screenshot, CODE_META, QR ve GitHub export politikaları otomasyon alanlarında korunmuştur.

---

## Güncel Bölüm Yolu Standardı

Doğru yapı:

```text
chapters/<chapter-alias>/
├── chapter_manifest.yaml
├── prompt.md
└── content/
    ├── draft.md
    ├── final.md
    └── revisions/
```

Örnek:

```text
chapters/giris/chapter_manifest.yaml
chapters/giris/prompt.md
chapters/giris/content/draft.md
chapters/giris/content/final.md
```
