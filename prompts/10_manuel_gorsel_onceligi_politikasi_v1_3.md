# Java'nın Temelleri — Manuel Görsel Önceliği Politikası v1.3

Bu belge, otomasyon tarafından üretilen görseller ile kullanıcı tarafından elle düzenlenen görseller arasında hangi dosyanın final DOCX/PDF üretiminde kullanılacağını tanımlar.

---

## 1. Temel ilke

Aynı görsel ID'sine sahip kullanıcı düzenlemesi varsa final çıktıda otomatik görsel yerine kullanıcı düzenlemesi kullanılmalıdır.

Öncelik sırası:

1. `assets/manual/`
2. `assets/locked/`
3. `assets/auto/`
4. kaynak tanım

---

## 2. Klasör rolleri

| Klasör | Amaç | Otomasyon silebilir mi? |
|---|---|---:|
| `assets/auto/` | Otomatik üretilen görseller | Evet |
| `assets/manual/` | Kullanıcının elle düzenlediği görseller | Hayır |
| `assets/locked/` | Finalde kilitlenmiş görseller | Hayır |
| `assets/final/` | DOCX/PDF içine girecek seçilmiş görseller | Evet, yeniden oluşturulabilir |

---

## 3. Eşleşme kuralı

Eşleşme `asset_id` veya dosya adı üzerinden yapılır.

```text
assets/auto/mermaid/karar-yapilari_diyagram01.png
assets/manual/mermaid/karar-yapilari_diyagram01.png
assets/final/mermaid/karar-yapilari_diyagram01.png
```

Bu durumda `manual` dosyası final klasörüne kopyalanır.

---

## 4. resolve-assets aşaması

Pandoc/DOCX üretiminden önce şu komut çalışmalıdır:

```bash
python tools/book_pipeline.py resolve-assets
```

Bu aşama:

1. `MERMAID_META` ve `ASSET_META` kayıtlarını okur.
2. Otomatik üretilen dosyaları kontrol eder.
3. Aynı ID'ye sahip manuel veya locked dosya var mı kontrol eder.
4. En yüksek öncelikli dosyayı `assets/final/` altına kopyalar.
5. `asset_resolution_report.md` üretir.

---

## 5. QR istisnası

QR kod görsellerinin matrisi manuel değiştirilmemelidir. Çünkü küçük bir görsel düzenleme bile QR içeriğini bozabilir.

QR için izin verilen işlemler:

- QR etiketini sayfada konumlandırmak,
- QR çevresine açıklama yazmak,
- QR görselinin Word içindeki boyutunu/stilini ayarlamak.

QR matrisi otomatik üretilmeli ve doğrulanmalıdır.

---

## 6. Güvenlik kuralı

`--force`, `clean`, `rebuild` veya `release` komutları çalıştırılsa bile şu klasörler silinmemelidir:

```text
assets/manual/
assets/locked/
chapters/
config/
templates/
```
