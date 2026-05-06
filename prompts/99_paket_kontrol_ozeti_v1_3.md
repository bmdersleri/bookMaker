# Java'nın Temelleri — Paket Kontrol Özeti v1.3

Bu paket, v1.2 prompt paketini otomasyon uyumlu üretim hattına taşımak için hazırlanmıştır.

## Paket kapsamı

- Başlık numaralarının build aşamasında atanması standarda bağlandı.
- `chapter_id` tabanlı kalıcı bölüm kimliği eklendi.
- Java kod blokları için `CODE_META` standardı eklendi.
- Mermaid diyagramları için `MERMAID_META` standardı eklendi.
- Görseller ve screenshot varlıkları için `ASSET_META` standardı eklendi.
- Manuel görsel önceliği politikası eklendi.
- QR üretimi GitHub URL manifestine bağlandı.
- Hatalı kod örnekleri için `broken_example`, `test: skip` politikası eklendi.
- `book_manifest.yaml`, `code_manifest.json`, `asset_manifest.json`, `qr_manifest.json` yapıları tanımlandı.
- Pipeline kalite kapıları ve raporlama dosyaları belirlendi.

## Temel kararlar

| Konu | v1.3 kararı |
|---|---|
| Bölüm başlıkları | Kaynak Markdown'da numarasız |
| Alt başlıklar | Kaynak Markdown'da numarasız |
| Bölüm numarası | Build sırasında manifest sırasına göre |
| Kod numarası | Build sırasında |
| Diyagram/şekil/tablo numarası | Build sırasında |
| Kalıcı kimlik | `chapter_id` |
| Java kod kimliği | `CODE_META.id` |
| Mermaid kimliği | `MERMAID_META.id` |
| Görsel önceliği | manual > locked > auto |
| GitHub yolu | `kodlar/{chapter_id}/kodNN/` |
| QR politikası | `CODE_META.qr` alanından |

## Kontrol listesi

- [x] Ana sistem promptu v1.3 hazırlandı.
- [x] Çıktı format standardı v1.3 hazırlandı.
- [x] Bölüm yapısı standardı v1.3 hazırlandı.
- [x] Bölüm girdi şablonu v1.3 hazırlandı.
- [x] Manifest standardı hazırlandı.
- [x] Manuel görsel önceliği politikası hazırlandı.
- [x] Pipeline kalite kapıları hazırlandı.
- [x] Örnek book manifest dosyası hazırlandı.
- [x] Örnek bölüm girdi dosyası hazırlandı.
- [x] Paket manifesti üretildi.
