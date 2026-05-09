"""GUI_MANIFEST.md dosyasina yeni bolumler ekler."""
import sys
sys.stdout.reconfigure(encoding='utf-8')

path = r'D:\bookMaker_Deepseek\GUI_MANIFEST.md'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# ================================================================
# YENI BOLUMLER
# ================================================================
new_sections = """

---

## 7. Pipeline Progress — Grafiksel ve Istatistiksel Takip

### 7.1 Genel Bakis

Pipeline'in her asamasi, kullaniciya **grafiksel** (progress bar, zaman cizelgesi) ve **istatistiksel** (kelime sayisi, kod blogu, diyagram, tablo) olarak sunulur. Kullanici hicbir terminal/console ciktisina bakmadan tum sureci anlik takip edebilir.

### 7.2 Canli Progress Ekrani Tasarimi

```
+------------------------------------------------------------------+
|  Pipeline: bolum-04 — Kontrol Yapilari                           |
+------------------------------------------------------------------+
|  ++++++++++++++++++++++++                %62  (3/5 adim tamam)   |
|                                                                  |
|  +----------------------------------------------------------+   |
|  | OK SPEC    Spesifikasyon          1,518 kel |  28.5s | OK |   |
|  | OK SEED    Seed Uretimi           1,562 kel |  65.2s | OK |   |
|  | OK NORM    Normalizasyon          1,334 kel |  0.01s | OK |   |
|  | >> ENRICH  6 zenginlestirme       —         |  ----  | >> |   |
|  |   ├ OK Ozet                         82 kel |  6.4s  | OK |   |
|  |   ├ OK Sozluk                      201 kel | 10.5s  | OK |   |
|  |   ├ >> Sorular                   calisiyor | 25.3s  | >> |   |
|  |   ├ .. Alistirmalar              bekliyor   |  ----  | .. |   |
|  |   ├ .. Hatalar                   bekliyor   |  ----  | .. |   |
|  |   └ .. Kopru                     bekliyor   |  ----  | .. |   |
|  | .. ASSEMBLE Birlestirme          bekliyor   |  ----  | .. |   |
|  +----------------------------------------------------------+   |
|                                                                  |
|  Gecen: 2m 14s    |    Tahmini Kalan: 1m 10s                    |
|                                                                  |
|  +- Istatistikler (canli) ---------------------------------+   |
|  | Toplam Kelime: 4,414    | Kod Blogu: 16    | Tablo: 17   |   |
|  | Mermaid Diyagram: 2     | API Cagrisi: 5/11 | Hata: 0    |   |
|  +----------------------------------------------------------+   |
|                                                                  |
|  [Duraklat]  [Iptal Et]  [Logu Kopyala]                         |
+------------------------------------------------------------------+
```

### 7.3 Progress Bar Tipleri

| Bar Tipi | Gorunum | Kullanim Yeri |
|----------|---------|---------------|
| **Ana Bar** | Yatay, yuzde, gradient dolgu | Tum pipeline genel ilerlemesi |
| **Adim Bari** | Ince, animasyonlu | Her bir enrich adimi icin |
| **API Bari** | Dairesel, countdown | LLM API cagrisi sirasinda (tahmini bitis) |
| **Risk Bari** | Renk gecisli (yesil-sari-kirmizi) | Hata olasiligi gostergesi |

### 7.4 Zaman Gostergeleri

| Gosterge | Aciklama | Guncellenme Sikligi |
|----------|----------|-------------------|
| **Gecen Sure** | Pipeline baslangicindan itibaren | Her saniye |
| **Adim Suresi** | Her adimin kendi suresi | Adim tamamlaninca |
| **Tahmini Kalan** | Kalan adimlarin tahmini suresi | Her adim tamamlaninca yeniden hesaplanir |
| **API Bekleme** | API yaniti beklenen sure | 5 saniyede bir |
| **Toplam Tahmin** | Gecen + tahmini kalan | Her adim tamamlaninca |

**Tahmini Kalan Sure Hesaplama:**
```
tahmini_kalan = (kalan_adim_sayisi * ortalama_adim_suresi)
              + (kalan_api_cagrisi * ortalama_api_suresi)

ortalama_adim_suresi = tamamlanan_adimlarin_suresi / tamamlanan_adim_sayisi
```

### 7.5 Istatistik Paneli — Anlik Metrikler

Pipeline sirasinda ve sonrasinda gosterilen istatistikler:

| Metrik | Kaynak | Gosterim |
|--------|--------|----------|
| **Kelime Sayisi** | Her adimin ciktisi | Sayi + mini bar (hedefe gore %) |
| **Kod Blogu** | Regex: \\`\\`\\` sayisi / 2 | Sayi + ada gore dagilim |
| **Inline Kod** | Regex: \\`...\\` sayisi | Sayi |
| **Mermaid Diyagram** | Regex: \\`\\`\\`mermaid | Sayi + liste |
| **Tablo** | Regex: |...| satirlari | Sayi |
| **Baslik (H2/H3)** | Regex: ## / ### | Sayi + derinlik |
| **Bold Metin** | Regex: **...** | Sayi |
| **Liste Ogesi** | Regex: - / * / 1. | Sayi |
| **API Cagri Sayisi** | Backend'den gonderilir | X / Toplam |
| **Hata Sayisi** | Backend'den gonderilir | Kirmizi rozet |
| **Richness Skoru** | Hesaplanan: kod*5 + diyagram*3 + ... | Sayi + renk skalasi |

### 7.6 Pipeline Adim Detaylandirma (Accordion)

Her adim genisletilebilir (accordion) detay karti:

```
+-- OK SPEC: Spesifikasyon — 1,518 kelime, 28.5s --------------- v --+
|                                                                      |
|  Icerik Analizi                                                      |
|  ++++++++++++++++++++++++         Kavramlar (16/20)                  |
|  ++++++++++++++++++++++++++++    Kod Ornegi (9/10)                   |
|  ++++++++++++++++++              Diyagram (3/5)                      |
|                                                                      |
|  Prompt (istek):                                                     |
|  +-------------------------------------------------------------+    |
|  | ## Gorev: Bolum Spesifikasyonu Hazirla                      |    |
|  | **Bolum:** Kontrol Yapilari                                 |    |
|  | **Kapsanacak kavramlar:**                                   |    |
|  |   - if-else yapisi                                          |    |
|  |   - switch-case                                             |    |
|  | ...                               [Tamamini Gor ->]        |    |
|  +-------------------------------------------------------------+    |
|                                                                      |
|  Ham Cikti (ilk 200 karakter):                                       |
|  +-------------------------------------------------------------+    |
|  | 1. KAVRAMLAR                                                |    |
|  |   - if-else yapisi: Zorluk: Kolay, Kod ornegi: gerekli     |    |
|  |   - switch-case: Zorluk: Kolay, Kod ornegi: gerekli        |    |
|  | ...                               [Tamamini Gor ->]        |    |
|  +-------------------------------------------------------------+    |
+----------------------------------------------------------------------+
```

### 7.7 Adim Durum Simgeleri ve Anlamlari

| Simge | Durum | Aciklama |
|-------|-------|----------|
| .. | Bekliyor | Henuz baslamadi |
| >> | Calisiyor | API cagrisi devam ediyor |
| OK | Tamamlandi | Basariyla bitti |
| XX | Hata | Basarisiz oldu |
| !! | Uyarili Tamam | Tamamlandi ama uyari var |
| RD | Tekrar Deneniyor | Retry mekanizmasi aktif |
| SK | Atlaniyor | Kullanici tarafindan atlandi |

---

## 8. Hata Yonetimi ve Kullaniciya Yansitma

### 8.1 Hata Kategorileri

| Kategori | Ornek | Kullaniciya Yansima |
|----------|-------|-------------------|
| **API Baglanti** | Timeout, 401, 429 | Kirmizi toast + retry sayaci + oneri |
| **API Yanit** | Bos yanit, gecersiz JSON | Sari toast + fallback icerik |
| **Icerik Kalitesi** | Cok kisa cikti, eksik bolum | Uyari karti + duzeltme secenekleri |
| **Dosya Sistemi** | Yazma hatasi, disk dolu | Kirmizi modal + cozum onerisi |
| **Validasyon** | Mermaid syntax, kirik link | Sari rozet + otomatik duzelt butonu |
| **Build** | Pandoc hatasi, font eksik | Kirmizi toast + log goruntuleme |

### 8.2 Hata Gosterim Stratejisi

```
+------------------------------------------------------------------+
|  XX Pipeline Hatasi                                              |
+------------------------------------------------------------------+
|  Adim: SEED (Seed Uretimi)                                      |
|  Hata: API timeout (120s) — 3 retry denendi                     |
|                                                                  |
|  Retry Gecmisi:                                                  |
|  Deneme 1: XX Timeout (120.0s)                                   |
|  Deneme 2: XX Timeout (122.0s)  — 2.0s bekleme                  |
|  Deneme 3: XX Timeout (124.0s)  — 4.0s bekleme                  |
|                                                                  |
|  Oneriler:                                                       |
|  • Internet baglantinizi kontrol edin                            |
|  • API anahtarinizin gecerli oldugunu dogrulayin                 |
|  • Timeout suresini artirin (su an: 120s)                        |
|  • Daha kisa bir prompt deneyin                                  |
|                                                                  |
|  [Tekrar Dene]  [Bu Adimi Atla]  [Pipelinei Iptal Et]           |
+------------------------------------------------------------------+
```

### 8.3 Fallback Stratejisi

| Adim | Hata Durumunda Fallback |
|------|------------------------|
| **SPEC** | Bos spec ile devam et, SEED direkt prompt alir |
| **SEED** | Pipeline durur, kullaniciya sorulur |
| **ENRICH (tek)** | O enrich icin varsayilan metin: "Bu bolum hazirlaniyor..." |
| **ENRICH (tumu)** | Enrich olmadan ASSEMBLE'a gec, uyari goster |
| **ASSEMBLE** | Parcalari oldugu gibi birlestir, eksikleri isaretle |

### 8.4 Toast Mesaj Sistemi

3 seviye toast bildirimi:
- **Hata** (kirmizi): Kritik hatalar, islem durdu
- **Uyari** (sari): Kalite sorunlari, eksik icerik
- **Basarili** (yesil): Islem tamamlandi

Her toast'ta: mesaj, detay, aksiyon butonu (Kapat/Duzelt/Yoksay/Gor)

### 8.5 Kullanici Etkilesim Noktalari

| Durum | Kullaniciya Soru | Secenekler |
|-------|-----------------|------------|
| API timeout | "3 deneme basarisiz. Ne yapalim?" | Tekrar Dene / Atla / Iptal |
| Dusuk kelime sayisi | "Ozet 82 kelime (min 150 bekleniyor)" | Yenden Uret / Oldugu Gibi Kabul |
| Kaydetme hatasi | "Dosya yazilamadi. Disk dolu olabilir." | Tekrar Dene / Farkli Kaydet |
| Baglanti koptu | "WebSocket baglantisi koptu." | Yeniden Baglan / Sayfayi Yenile |
"""

# Teknoloji Yigini oncesine ekle
old_marker = '\n---\n\n## 7. Teknoloji Yığını'
if old_marker in content:
    content = content.replace(old_marker, new_sections + old_marker)
    print("Pipeline progress + hata yonetimi eklendi.")
else:
    print(f"HATA: '{old_marker[:30]}...' bulunamadi!")

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"Toplam: {len(content)} karakter")
