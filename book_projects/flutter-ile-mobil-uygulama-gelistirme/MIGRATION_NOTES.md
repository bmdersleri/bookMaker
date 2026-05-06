# Yeni Klasör Yapısına Uyarlama Notları

Önceki taslakta Flutter kitabı `book_projects/flutter-ile-mobil-uygulama-gelistirme/` altında `book_profile.yaml` ve `book_architecture.yaml` dosyalarıyla kurgulanmıştı.

Güncel yapıya göre bu yaklaşım şu şekilde dönüştürüldü:

| Eski yaklaşım | Yeni yaklaşım |
|---|---|
| `book_profile.yaml` | `book_manifest.yaml` içine taşındı |
| `book_architecture.yaml` | `book_manifest.yaml` bölüm listesi + her bölümde `chapter_manifest.yaml` yapısına bölündü |
| `chapters/<chapter_id>/...` | `<chapter-alias>/chapter_manifest.yaml`, `<chapter-alias>/prompt.md`, `<chapter-alias>/content/...` |
| `build/exports` | `exports/docx`, `exports/pdf`, `exports/md` |
| `build/reports` | `logs/reviews`, `logs/errors`, `logs/production` |
| Framework içi kitap projesi | Tamamen bağımsız kitap klasörü |

## Korunan ilkeler

- Flutter/Dart teknik profil korunmuştur.
- Her bölümde scope, objectives, exclusions, structure, status ve quality alanları vardır.
- Bölümler arası bağlantılar klasör yolu veya bölüm numarası yerine alias ile tanımlanmıştır.
- Screenshot, CODE_META, QR ve GitHub export politikaları otomasyon alanlarında korunmuştur.
