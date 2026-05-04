# bookMaker Geliştirme Yol Haritası

## Tamamlanan Fazlar

### Faz 0 — Proje İskeleti ✅
### Faz 1 — Veri Modelleri ve Depolama ✅
### Faz 2 — Chapter Validator ✅
### Faz 3 — Kod Smoke Test Motoru ✅
### Faz 4 — Manifest Editörü ✅
### Faz 5 — Authoring Pipeline ✅
### Faz 6 — Production Pipeline ✅
### Faz 7 — GitHub + Studio GUI ✅

## Aktif Çalışma

### LLM API + Generation Pipeline

#### Bölüm Üretimi

**Batch 1-2 (B7-B16):** ✅ Tamam
- [x] B7: Algoritmik Problem Çözme Desenleri
- [x] B8: Metotlar, Overloading ve Özyineleme
- [x] B9: Diziler ve Çok Boyutlu Veri Yapıları
- [x] B10: String İşlemleri ve Metin Problemleri
- [x] B11: Matematiksel Yardımcılar ve Rastgelelik
- [x] B12: Tarih ve Zaman İşlemleri
- [x] B13: Paketler, import Kullanımı ve Proje Düzeni
- [x] B14: Koleksiyonlar ve Dinamik Veri Yönetimi
- [x] B15: Hata Yönetimi ve Dayanıklı Programlama
- [x] B16: Dosya İşlemleri ve Kalıcı Veri Saklama

**Batch 3 (B17-B21):** 🔄 Devam
- [ ] B17: Sınıf, Nesne, Constructor ve Kapsülleme
- [ ] B18: Kalıtım ve Interface'e Kısa Ön Bakış
- [ ] B19: GUI Programlamaya Giriş ve Swing Arayüz Tasarımı
- [ ] B20: Temel Swing Bileşenleri, Olay Yönetimi ve Form Doğrulama
- [ ] B21: Liste, Tablo, Menü ve Diyaloglarla GUI Veri Sunumu

**Batch 4:** ⏳ Sırada
- [ ] B22: JDBC ile Veritabanı Programlamaya Giriş
- [ ] B23: Bütünleşik Uygulama ve Final Proje Rehberi
- [ ] Ek A: Sık Yapılan Java Hataları ve Çözüm Rehberi
- [ ] Ek B: JavaFX'e Kısa Bakış
- [ ] Ek C: Mini Proje Fikirleri ve Rubrikler
- [ ] Ek D: Java Programlama Kontrol Rehberi, Sık Hatalar ve Kod Kalitesi

#### İyileştirmeler
- [x] P1-P12 tüm optimizasyonlar batch_v2.py'de
- [x] postprocess.py: front matter fix, heading fix, CODE_META
- [x] pipeline.py: timeout 120→300
- [x] .gitignore: api.txt, llm_config.json

## Sıradaki Görevler

### Kısa Vade
- [ ] Batch 3 (B17-B21) tamamla
- [ ] Batch 4 (B22-B23 + Ek A-D) tamamla
- [ ] Tüm batch'leri commit + push et

### Orta Vade
- [ ] Mermaid diyagramı çıktısını doğrula (F-007)
- [ ] Bölüm uzunluğu tutarlılığını değerlendir (F-008)
- [ ] Kitap düzeyinde validasyon (`bookmaker check book`)
- [ ] DOCX/PDF çıktısı üret
- [ ] Kodları GitHub'a sync et

### Uzun Vade
- [ ] Faz 8: Kitap düzeyinde validasyon
- [ ] Studio GUI geliştirmeleri
- [ ] Paralel API çağrıları (birden fazla bölüm aynı anda)
- [ ] Farklı LLM sağlayıcı desteği
