# Bölüm Planı: Python'a Giriş ve Kurulum

---

## 1. KAVRAMLAR

| Kavram | Ne Olduğu (1 cümle) | Zorluk (1-5★) | Kod Örneği? | Ne Gösterecek? |
|--------|---------------------|---------------|-------------|----------------|
| Python programlama dili | Yorumlanan, nesne yönelimli, yüksek seviyeli bir programlama dili | ★☆☆☆☆ (1) | Hayır | — |
| Python kurulumu | Python yorumlayıcısının bilgisayara kurulma süreci | ★★☆☆☆ (2) | Hayır | — |
| IDE seçimi | Kod yazmayı kolaylaştıran geliştirme ortamının seçilmesi | ★☆☆☆☆ (1) | Hayır | — |
| İlk program | Ekrana yazı yazdıran en temel Python programı | ★☆☆☆☆ (1) | Evet | print() fonksiyonu ile çıktı alma |
| print() | Ekrana metin veya değişken değeri yazdıran yerleşik fonksiyon | ★☆☆☆☆ (1) | Evet | Metin, sayı ve değişken yazdırma |
| REPL | Read-Eval-Print Loop: kod satır satır çalıştırma ortamı | ★★☆☆☆ (2) | Evet | Etkileşimli ortamda anlık kod çalıştırma |
| Sözdizimi (Syntax) | Python dilinin yazım kuralları | ★★☆☆☆ (2) | Evet | Girintileme, iki nokta, satır sonu kuralları |
| Yorum satırları | Kodun açıklaması için yazılan, çalıştırılmayan metinler | ★☆☆☆☆ (1) | Evet | Tek satır (#) ve çok satırlı (""" """) yorum |

---

## 2. KOD ÖRNEKLERİ

**Örnek 1: İlk Program**
- **Kavram:** İlk program + print()
- **Dosya adı:** `ilk_program.py`
- **Tahmini satır:** 3-5 satır
- **Kullanılacak özellikler:** print() fonksiyonu, string ifade

**Örnek 2: Print() Çeşitlemeleri**
- **Kavram:** print() fonksiyonu
- **Dosya adı:** `print_ornekleri.py`
- **Tahmini satır:** 8-12 satır
- **Kullanılacak özellikler:** print() içinde metin, sayı, değişken, birden çok parametre, sep ve end parametreleri

**Örnek 3: REPL Kullanımı**
- **Kavram:** REPL
- **Dosya adı:** `repl_ornekleri.py` (aslında terminalde gösterilecek)
- **Tahmini satır:** 5-8 satır (ekran görüntüsü olarak)
- **Kullanılacak özellikler:** >>> işareti, anlık hesaplama, değişken atama

**Örnek 4: Sözdizimi ve Yorum**
- **Kavram:** Sözdizimi + yorum satırları
- **Dosya adı:** `sozdizimi_ve_yorum.py`
- **Tahmini satır:** 10-15 satır
- **Kullanılacak özellikler:** # ile tek satır yorum, """ ile çok satırlı yorum, doğru/yanlış girintileme örnekleri

---

## 3. DİYAGRAMLAR

**Diyagram 1: Python Çalışma Akışı**
- **Görselleştirecek:** Python kodunun yazılmasından çalıştırılmasına kadar olan süreç
- **Tür:** Flowchart (akış diyagramı)
- **Düğümler:**
  1. Kod yaz (IDE veya metin editörü)
  2. Dosyayı kaydet (.py uzantısı)
  3. Python yorumlayıcısı kodu oku
  4. Sözdizimi hatası var mı? (karar elması)
    - Evet → Hata mesajı göster → Düzelt
    - Hayır → Devam et
  5. Kodu derle (bytecode)
  6. Sanal makinede çalıştır
  7. Çıktıyı ekrana yaz

**Diyagram 2: IDE vs REPL Karşılaştırması**
- **Görselleştirecek:** İki farklı çalıştırma ortamının akış farkı
- **Tür:** Sequence diagram (sıralı diyagram)
- **Düğümler:**
  1. Kullanıcı
  2. IDE (dosya tabanlı)
  3. REPL (etkileşimli)
  4. Python yorumlayıcı
  5. Çıktı ekranı

---

## 4. SÖZLÜK (12 terim)

1. Python
2. Yorumlayıcı (Interpreter)
3. IDE (Integrated Development Environment)
4. REPL
5. print()
6. Sözdizimi (Syntax)
7. Yorum satırı
8. Girintileme (Indentation)
9. String (metin)
10. Değişken
11. Hata ayıklama (Debugging)
12. Konsol / Terminal

---

## 5. DEĞERLENDİRME

**Doğru/Yanlış Soruları (8 adet) — Konular:**
1. Python yorumlanan bir dildir (D/Y)
2. Python kodları .java uzantısıyla kaydedilir (D/Y)
3. print() fonksiyonu kullanıcıdan veri alır (D/Y)
4. Python'da girintileme zorunludur (D/Y)
5. REPL ortamında kod satır satır çalıştırılır (D/Y)
6. Yorum satırları Python tarafından çalıştırılır (D/Y)
7. Python ücretsiz ve açık kaynaktır (D/Y)
8. Python'da değişken tanımlarken tür belirtmek zorunludur (D/Y)

**Boşluk Doldurma Soruları (8 adet) — Konular:**
1. Python kodları ______ uzantısıyla kaydedilir.
2. Ekrana yazı yazdırmak için ______ fonksiyonu kullanılır.
3. Python'da tek satır yorum ______ işaretiyle başlar.
4. REPL açılımı ______, ______, ______, ______'dir.
5. Python'da kod blokları ______ ile ayrılır.
6. IDE açılımı ______ ______ ______'dir.
7. Python'da çok satırlı yorum ______ veya ______ ile yapılır.
8. Python ilk olarak ______ yılında yayınlanmıştır.

---

## 6. ALIŞTIRMALAR

**Alıştırma 1: Kişisel Tanıtım**
- **Zorluk:** ★☆☆☆☆ (1)
- **Konu:** Adınızı, yaşınızı ve sevdiğiniz bir aktiviteyi ekrana yazdıran program yazın.

**Alıştırma 2: Hata Bulma**
- **Zorluk:** ★★☆☆☆ (2)
- **Konu:** Verilen hatalı bir Python kodundaki sözdizimi ve girintileme hatalarını bulup düzeltin.

**Alıştırma 3: REPL Deneyi**
- **Zorluk:** ★★☆☆☆ (2)
- **Konu:** REPL ortamında 3 farklı matematiksel işlem yapın, sonucu değişkene atayıp yazdırın.

---

## 7. SIK YAPILAN HATALAR

1. **Girintileme hatası:** Python'da kod blokları girintileme ile ayrılır; boşluk ve tab karıştırıldığında hata alınır.
2. **print() yazım hatası:** Fonksiyon adının "print" değil "print" olduğu unutulur veya parantez kullanılmaz.
3. **Dosya uzantısı hatası:** Kod .py uzantısıyla kaydedilmezse çalıştırılamaz.
4. **Yorum satırı karışıklığı:** # işaretinin sadece satır başında değil, kod içinde de kullanılabileceği unutulur.
5. **Türkçe karakter sorunu:** Python 2'de Türkçe karakterler sorun çıkarırken Python 3'te sorunsuzdur, sürüm farkı göz ardı edilir.

---

## 8. TABLOLAR

**Tablo 1: Python Sürümleri Karşılaştırması**
- **Karşılaştırılacak veriler:** Python 2 vs Python 3 — çıkış yılı, yazım farkı, print kullanımı, tamsayı bölmesi, Unicode desteği, güncel durum

**Tablo 2: Popüler IDE Karşılaştırması**
- **Karşılaştırılacak veriler:** PyCharm, VS Code, IDLE, Jupyter Notebook — ücret, platform, özellikler, başlangıç seviyesi uygunluğu

**Tablo 3: Yorum Türleri**
- **Karşılaştırılacak veriler:** Tek satır (#), çok satırlı (""" """), Inline yorum — kullanım amacı, örnek, avantaj/dezavantaj

---

**Not:** Bu plan tamamen tarif düzeyindedir. Bir sonraki aşamada her kavram için 6 adımlı zincir (Tanım → Neden Var → Nasıl Kullanılır → Ne Zaman Tercih Edilir → Alternatifleri → Yaygın Hatalar) uygulanarak kod ve diyagramlar yazılacaktır.