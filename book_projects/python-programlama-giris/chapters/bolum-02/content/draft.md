---
title: "Degiskenler ve Veri Tipleri"
subtitle: "Python Programlamaya Giris"
author: "Ismail Kirbas"
date: "2026"
lang: tr-TR
documentclass: report
toc: true
toc-depth: 3
numbersections: true
repo: bmdersleri
project-alias: python-programlama-giris
chapter-alias: bolum-02
chapter_id: bolum-02
chapter_type: core
automation_profile: academic_technical_book_v1
numbering: auto
github_slug: bolum-02
qr_policy: dual_for_code_examples
asset_policy: manual_override
---
# Değişkenler ve Veri Tipleri

## Öğrenme Yol Haritası

Bu bölümde, programlamanın en temel yapı taşlarından olan değişkenler ve veri tiplerini öğreneceksiniz. Bir programcının günlük hayatta en çok kullandığı kavramlar olan değişken tanımlama, veri tipleri, tip dönüşümleri ve string işlemlerini adım adım keşfedeceksiniz.

### Bu Bölümün Sonunda Şunları Yapabileceksiniz:
- Değişken tanımlama ve değer atama işlemlerini gerçekleştirebilecek
- Dört temel veri tipini (int, float, str, bool) ayırt edebilecek
- `type()` fonksiyonu ile veri tiplerini sorgulayabilecek
- Veri tipleri arasında dönüşüm yapabilecek
- `input()` fonksiyonu ile kullanıcıdan veri alabilecek
- String metodlarını kullanarak metin işlemleri yapabilecek
- f-string ile modern biçimlendirme yapabilecek
- `None` değerinin ne zaman ve nasıl kullanılacağını anlayabilecek

### Ön Bilgi Gereksinimleri
Bu bölüme başlamadan önce Python'ın temel kurulumunu yapmış ve ilk "Merhaba Dünya" programınızı çalıştırmış olmanız yeterlidir. Herhangi bir programlama deneyimi gerekmemektedir.


## 1. Değişken Tanımlama

### TANIM
Değişken (variable), program içinde veriyi saklamak için kullandığımız isimlendirilmiş bellek alanıdır. Bir kutuya benzetebiliriz: kutunun üzerine bir isim yazarız ve içine istediğimiz değeri koyarız.

### NEDEN VAR?
Değişkenler olmasaydı, her veriyi program içinde sabit bir değer olarak kullanmak zorunda kalırdık. Örneğin, bir kullanıcının adını 10 farklı yerde kullanacaksak, her seferinde aynı metni yazmak zorunda kalırdık. Değişkenler sayesinde veriyi bir kez tanımlar, istediğimiz kadar kullanırız.

**Günlük Hayat Analojisi:** Telefon rehberinizdeki kişileri düşünün. Her kişi için bir isim (değişken adı) ve telefon numarası (değer) vardır. "Ahmet" dediğinizde, rehberdeki Ahmet'in numarasına ulaşırsınız. Değişkenler de aynı şekilde çalışır.

### NASIL KULLANILIR?


```python
# Örnek 1: degisken_tanitimi.py - Değişken tanımlama ve temel veri tipleri

# --- Sayısal değişkenler ---
ogrenci_sayisi = 250  # Integer (tam sayı) tipinde değişken
okul_puani = 89.5     # Float (ondalıklı sayı) tipinde değişken

# --- Metinsel değişkenler ---
okul_adi = "Atatürk Ortaokulu"  # String (metin) tipinde değişken
sehir = "Ankara"                 # String tipinde değişken

# --- Mantıksal değişkenler ---
mezun_mu = True      # Boolean (mantıksal) tipinde değişken
aktif_mi = False     # Boolean tipinde değişken

# Değişkenlerin değerlerini ve türlerini yazdırma
print("Okul Adı:", okul_adi)
print("Öğrenci Sayısı:", ogrenci_sayisi)
print("Okul Puanı:", okul_puani)
print("Mezun mu?:", mezun_mu)
print("Aktif mi?:", aktif_mi)

# type() fonksiyonu ile veri tiplerini sorgulama
print("\n--- Veri Tipleri ---")
print("ogrenci_sayisi tipi:", type(ogrenci_sayisi))
print("okul_puani tipi:", type(okul_puani))
print("okul_adi tipi:", type(okul_adi))
print("mezun_mu tipi:", type(mezun_mu))

# Çıktı:
# Okul Adı: Atatürk Ortaokulu
# Öğrenci Sayısı: 250
# Okul Puanı: 89.5
# Mezun mu?: True
# Aktif mi?: False
#
# --- Veri Tipleri ---
# ogrenci_sayisi tipi: <class 'int'>
# okul_puani tipi: <class 'float'>
# okul_adi tipi: <class 'str'>
# mezun_mu tipi: <class 'bool'>
```


**Kod Açıklaması:**
1. **Satır 4-5:** İki sayısal değişken tanımlıyoruz. `ogrenci_sayisi` tam sayı (int), `okul_puani` ondalıklı sayı (float) içeriyor.
2. **Satır 8-9:** Metin (string) değişkenleri tanımlıyoruz. Tırnak işaretleri içinde yazılıyor.
3. **Satır 12-13:** Mantıksal (boolean) değişkenler tanımlıyoruz. Sadece `True` veya `False` değeri alabilir.
4. **Satır 16-19:** `print()` fonksiyonu ile değişkenlerin değerlerini ekrana yazdırıyoruz.
5. **Satır 22-25:** `type()` fonksiyonu ile her değişkenin veri tipini öğreniyoruz.

### NE ZAMAN TERCİH EDİLİR?
Değişkenler, aşağıdaki durumlarda mutlaka kullanılmalıdır:
- Bir değeri birden fazla yerde kullanmanız gerekiyorsa
- Değerin program çalışırken değişmesi gerekiyorsa
- Kullanıcıdan veri almanız gerekiyorsa
- Hesaplama sonuçlarını saklamanız gerekiyorsa

### ALTERNATİFLERİ
Değişken kullanmak yerine doğrudan değerleri kullanabilirsiniz (buna "sabit" veya "literal" denir). Ancak bu yaklaşım:
- Kodu okunaksız hale getirir
- Bakımı zorlaştırır
- Tekrar kullanımı engeller

| Özellik | Değişken | Sabit (Literal) |
|---------|----------|-----------------|
| Değiştirilebilirlik | Evet | Hayır |
| Kod okunabilirliği | Yüksek | Düşük |
| Bakım kolaylığı | Kolay | Zor |
| Kullanım alanı | Dinamik veriler | Statik değerler |

### YAYGIN HATALAR

**Hata 1: Değişken adında boşluk kullanmak**


```python
# Yanlış:
ogrenci sayisi = 250  # SyntaxError: invalid syntax

# Doğru:
ogrenci_sayisi = 250  # Alt çizgi kullanılır
```


**Hata 2: Değişkeni tanımlamadan kullanmak**


```python
# Yanlış:
print(toplam)  # NameError: name 'toplam' is not defined

# Doğru:
toplam = 0
print(toplam)  # Çıktı: 0
```


## 2. Veri Tipleri (int, float, str, bool)

### TANIM
Veri tipleri, bir değişkenin hangi türde veri saklayabileceğini belirleyen sınıflandırmalardır. Python'da dört temel veri tipi vardır: int (tam sayı), float (ondalıklı sayı), str (metin) ve bool (mantıksal).

### NEDEN VAR?
Veri tipleri olmasaydı, bilgisayar bir sayıyla metni nasıl işleyeceğini bilemezdi. Örneğin, "5" + "3" işleminin sonucu "53" mü yoksa 8 mi olmalı? Veri tipleri bu karışıklığı önler.

**Günlük Hayat Analojisi:** Bir posta kutusu düşünün. Mektup kutusuna sadece mektup (string), fatura kutusuna sadece fatura (int), kargo kutusuna ise paket (float) koyabilirsiniz. Her kutu belirli bir türdeki öğeler için tasarlanmıştır.

### NASIL KULLANILIR?


```python
# Örnek 2: veri_tipleri_detay.py - Veri tiplerini detaylı inceleme

# --- Integer (int) ---
yas = 25                     # Pozitif tam sayı
sicaklik = -5                # Negatif tam sayı
buyuk_sayi = 1_000_000       # Alt çizgi ile okunabilir yazım (Python 3.6+)

# --- Float (float) ---
pi_sayisi = 3.14159          # Ondalıklı sayı
bilimsel_gosterim = 1.5e-3   # Bilimsel gösterim (0.0015)

# --- String (str) ---
isim = "Ayşe"                # Çift tırnak
soyisim = 'Yılmaz'           # Tek tırnak (Python her ikisini de destekler)
cok_satirli = """Bu bir
çok satırlı
metindir"""                  # Üç tırnak ile çok satırlı string

# --- Boolean (bool) ---
gunes_dogdu_mu = True        # Mantıksal doğru
yagmur_yagiyor_mu = False    # Mantıksal yanlış

# Her veri tipi için örnek işlemler
print("--- Integer İşlemleri ---")
print("Yaş:", yas)
print("Yaşın iki katı:", yas * 2)
print("Sıcaklık mutlak değer:", abs(sicaklik))

print("\n--- Float İşlemleri ---")
print("Pi sayısı:", pi_sayisi)
print("Yarıçap 5 olan dairenin alanı:", pi_sayisi * 5**2)

print("\n--- String İşlemleri ---")
tam_isim = isim + " " + soyisim  # String birleştirme
print("Tam isim:", tam_isim)
print("İsmin uzunluğu:", len(isim))  # len() ile karakter sayısı

print("\n--- Boolean İşlemleri ---")
print("Güneş doğdu mu?", gunes_dogdu_mu)
print("Yağmur yağıyor mu?", yagmur_yagiyor_mu)
print("Her ikisi de doğru mu?", gunes_dogdu_mu and yagmur_yagiyor_mu)

# Çıktı:
# --- Integer İşlemleri ---
# Yaş: 25
# Yaşın iki katı: 50
# Sıcaklık mutlak değer: 5
#
# --- Float İşlemleri ---
# Pi sayısı: 3.14159
# Yarıçap 5 olan dairenin alanı: 78.53975
#
# --- String İşlemleri ---
# Tam isim: Ayşe Yılmaz
# İsmin uzunluğu: 4
#
# --- Boolean İşlemleri ---
# Güneş doğdu mu? True
# Yağmur yağıyor mu? False
# Her ikisi de doğru mu? False
```


**Kod Açıklaması:**
1. **Satır 4-6:** Integer değişkenler tanımlıyoruz. Büyük sayıları okunabilir yapmak için alt çizgi kullanabiliriz.
2. **Satır 9-10:** Float değişkenler. Bilimsel gösterim (1.5e-3 = 0.0015) özellikle küçük/ büyük sayılar için kullanışlıdır.
3. **Satır 13-17:** String tanımlama yöntemleri. Python tek ve çift tırnağı eşit şekilde destekler.
4. **Satır 20-21:** Boolean değişkenler. Sadece `True` veya `False` değeri alabilir.
5. **Satır 28:** `abs()` fonksiyonu mutlak değer alır.
6. **Satır 33:** `**` operatörü üs alma işlemi yapar (5² = 25).
7. **Satır 36:** `+` operatörü string'leri birleştirir.
8. **Satır 37:** `len()` fonksiyonu string'in karakter sayısını verir.
9. **Satır 42:** `and` operatörü iki boolean değerin mantıksal VE'sini alır.

### NE ZAMAN TERCİH EDİLİR?
- **int:** Yaş, öğrenci sayısı, adım sayısı gibi tam sayı değerler için
- **float:** Para miktarı, sıcaklık, mesafe gibi ondalıklı değerler için
- **str:** İsim, adres, açıklama gibi metinsel veriler için
- **bool:** Evet/Hayır, Doğru/Yanlış gibi ikili durumlar için

### ALTERNATİFLERİ
Python'da ayrıca `complex` (karmaşık sayılar), `bytes`, `bytearray` gibi gelişmiş veri tipleri de vardır ancak temel programlama için dört ana tip yeterlidir.

| Veri Tipi | Örnek | Kullanım Alanı | Bellek Kullanımı |
|-----------|-------|----------------|------------------|
| int | 42, -7, 0 | Sayma, indeksleme | 28 byte (küçük sayılar) |
| float | 3.14, -0.5 | Bilimsel hesaplamalar | 24 byte |
| str | "Merhaba" | Metin işleme | Karakter başına 1 byte |
| bool | True, False | Karar mekanizmaları | 28 byte |

### YAYGIN HATALAR

**Hata 1: String ile sayıyı toplamaya çalışmak**


```python
# Yanlış:
yas = 25
print("Yaşınız: " + yas)  # TypeError: can only concatenate str (not "int") to str

# Doğru:
print("Yaşınız: " + str(yas))  # str() ile dönüşüm yapılır
# veya
print(f"Yaşınız: {yas}")  # f-string kullanılır
```


**Hata 2: Ondalıklı sayıyı tam sayı sanmak**


```python
# Yanlış:
ortalama = 85.5
print(type(ortalama))  # <class 'float'> - beklenmedik olabilir

# Doğru: Veri tipini kontrol etmek için type() kullanılır
```


## 3. type() Fonksiyonu

### TANIM
`type()` fonksiyonu, bir değişkenin veya değerin veri tipini döndüren yerleşik bir Python fonksiyonudur.

### NEDEN VAR?
Program yazarken, özellikle hata ayıklama sırasında, bir değişkenin hangi tipte olduğunu bilmek kritik öneme sahiptir. `type()` sayesinde bu bilgiye anında ulaşabiliriz.

**Günlük Hayat Analojisi:** Bir hediye paketini düşünün. Paketin üzerinde "içinde ne var?" yazılı bir etiket olsa, paketi açmadan içindekini tahmin edebilirsiniz. `type()` fonksiyonu da aynı işlevi görür.

### NASIL KULLANILIR?


```python
# Örnek 3: type_fonksiyonu.py - type() ile veri tipi sorgulama

# Farklı veri tiplerini inceleme
sayi1 = 100
sayi2 = 3.14
metin = "Python Programlama"
mantik = True
bos_deger = None

print("=== type() Fonksiyonu Örnekleri ===\n")

# Her değişkenin tipini yazdırma
print(f"sayi1 ({sayi1}) tipi: {type(sayi1)}")
print(f"sayi2 ({sayi2}) tipi: {type(sayi2)}")
print(f"metin ({metin}) tipi: {type(metin)}")
print(f"mantik ({mantik}) tipi: {type(mantik)}")
print(f"bos_deger ({bos_deger}) tipi: {type(bos_deger)}")

# type() sonucunu karşılaştırma
print("\n=== Tip Karşılaştırmaları ===")
print("sayi1 int mi?", type(sayi1) == int)
print("sayi2 float mi?", type(sayi2) == float)
print("metin str mi?", type(metin) == str)
print("mantik bool mi?", type(mantik) == bool)

# isinstance() ile tip kontrolü (daha güvenli yöntem)
print("\n=== isinstance() ile Tip Kontrolü ===")
print("sayi1 int mi?", isinstance(sayi1, int))
print("sayi2 sayısal mı?", isinstance(sayi2, (int, float)))

# Çıktı:
# === type() Fonksiyonu Örnekleri ===
# 
# sayi1 (100) tipi: <class 'int'>
# sayi2 (3.14) tipi: <class 'float'>
# metin (Python Programlama) tipi: <class 'str'>
# mantik (True) tipi: <class 'bool'>
# bos_deger (None) tipi: <class 'NoneType'>
# 
# === Tip Karşılaştırmaları ===
# sayi1 int mi? True
# sayi2 float mi? True
# metin str mi? True
# mantik bool mi? True
# 
# === isinstance() ile Tip Kontrolü ===
# sayi1 int mi? True
# sayi2 sayısal mı? True
```


**Kod Açıklaması:**
1. **Satır 4-8:** Farklı veri tiplerinde değişkenler tanımlıyoruz.
2. **Satır 13-17:** `type()` fonksiyonu ile her değişkenin tipini yazdırıyoruz. Çıktı `<class 'int'>` şeklinde gelir.
3. **Satır 20-24:** `type()` sonucunu `==` operatörü ile karşılaştırarak tip kontrolü yapıyoruz.
4. **Satır 27-29:** `isinstance()` fonksiyonu, bir değişkenin belirtilen tipte olup olmadığını kontrol eder. Birden fazla tipi aynı anda kontrol edebiliriz.

### NE ZAMAN TERCİH EDİLİR?
- Hata ayıklama sırasında
- Kullanıcıdan alınan verinin tipini kontrol ederken
- Bir fonksiyona gönderilen parametrenin tipini doğrularken
- Veri dönüşümü öncesi tip kontrolü yaparken

### ALTERNATİFLERİ

| Yöntem | Kullanım | Avantaj | Dezavantaj |
|--------|----------|---------|------------|
| `type()` | `type(değişken)` | Basit, hızlı | Alt sınıfları algılamaz |
| `isinstance()` | `isinstance(değişken, tip)` | Alt sınıfları da algılar | Biraz daha yavaş |
| `__class__` | `değişken.__class__` | Doğrudan sınıfa erişim | Pythonic değil |

### YAYGIN HATALAR

**Hata: type() sonucunu string ile karşılaştırmak**


```python
# Yanlış:
if type(sayi) == "int":  # Her zaman False döner
    print("Bu bir integer")

# Doğru:
if type(sayi) == int:  # Tip sınıfı ile karşılaştırılır
    print("Bu bir integer")
# veya daha iyisi:
if isinstance(sayi, int):
    print("Bu bir integer")
```


## 4. Tip Dönüşümleri (Type Casting)

### TANIM
Tip dönüşümü, bir veri tipini başka bir veri tipine dönüştürme işlemidir. Python'da `int()`, `float()`, `str()` ve `bool()` fonksiyonları ile yapılır.

### NEDEN VAR?
Kullanıcıdan alınan veriler her zaman string tipindedir. Sayısal işlemler yapmak için bu verileri sayıya dönüştürmemiz gerekir. Ayrıca, bir sayıyı metin içinde kullanmak için string'e çevirmemiz gerekebilir.

**Günlük Hayat Analojisi:** Bir yabancı dilde yazılmış bir kitabı düşünün. Kitabı okuyabilmek için çeviri yapmanız gerekir. Tip dönüşümü de aynı işlevi görür: veriyi ihtiyacımız olan "dile" çevirir.

### NASIL KULLANILIR?


```python
# Örnek 4: tip_donusum_ornekleri.py - Tüm tip dönüşümleri

print("=== TİP DÖNÜŞÜM ÖRNEKLERİ ===\n")

# --- String'ten Integer'a Dönüşüm ---
kullanici_yasi = input("Yaşınızı girin: ")  # Kullanıcı "25" yazdı
print(f"Girilen değerin tipi: {type(kullanici_yasi)}")  # <class 'str'>

yas_sayisi = int(kullanici_yasi)  # String'i integer'a çevir
print(f"Dönüşüm sonrası tip: {type(yas_sayisi)}")  # <class 'int'>
print(f"Gelecek yıl yaşınız: {yas_sayisi + 1}")  # Matematiksel işlem yapılabilir

# --- String'ten Float'a Dönüşüm ---
boy_metre = input("Boyunuzu metre cinsinden girin (örn: 1.75): ")
boy_sayisi = float(boy_metre)
print(f"Boyunuz santimetre cinsinden: {boy_sayisi * 100:.0f} cm")

# --- Sayıdan String'e Dönüşüm ---
ogrenci_no = 12345
ogrenci_no_str = str(ogrenci_no)
print(f"Öğrenci numarası: {ogrenci_no_str} (tip: {type(ogrenci_no_str)})")

# --- Float'tan Integer'a Dönüşüm (Kesme) ---
pi = 3.14159
pi_tam = int(pi)  # Ondalık kısım atılır
print(f"int({pi}) = {pi_tam}")  # 3

# --- Integer'dan Float'a Dönüşüm ---
sayi = 10
sayi_float = float(sayi)
print(f"float({sayi}) = {sayi_float}")  # 10.0

# --- Boolean Dönüşümleri ---
print("\n=== Boolean Dönüşümleri ===")
print(f"bool(1) = {bool(1)}")     # True
print(f"bool(0) = {bool(0)}")     # False
print(f"bool('') = {bool('')}")   # False (boş string)
print(f"bool('Merhaba') = {bool('Merhaba')}")  # True
print(f"bool(None) = {bool(None)}")  # False

# --- Hatalı Dönüşümler ve Çözümleri ---
print("\n=== Hatalı Dönüşüm Örnekleri ===")

# Hata 1: Alfabetik karakteri sayıya çevirmek
try:
    hatali_donusum = int("abc")
except ValueError as hata:
    print(f"Hata 1: '{hata}' - Alfabetik karakter sayıya çevrilemez")

# Hata 2: Ondalıklı sayıyı direkt integer'a çevirmek
try:
    hatali_donusum = int("3.14")  # Önce float'a çevirmek gerekir
except ValueError as hata:
    print(f"Hata 2: '{hata}' - Önce float() ile dönüştürün")
    # Doğru yöntem:
    dogru_donusum = int(float("3.14"))
    print(f"Doğru yöntem: int(float('3.14')) = {dogru_donusum}")

# Çıktı:
# === TİP DÖNÜŞÜM ÖRNEKLERİ ===
# 
# Yaşınızı girin: 25
# Girilen değerin tipi: <class 'str'>
# Dönüşüm sonrası tip: <class 'int'>
# Gelecek yıl yaşınız: 26
# Boyunuzu metre cinsinden girin (örn: 1.75): 1.75
# Boyunuz santimetre cinsinden: 175 cm
# Öğrenci numarası: 12345 (tip: <class 'str'>)
# int(3.14159) = 3
# float(10) = 10.0
# 
# === Boolean Dönüşümleri ===
# bool(1) = True
# bool(0) = False
# bool('') = False
# bool('Merhaba') = True
# bool(None) = False
# 
# === Hatalı Dönüşüm Örnekleri ===
# Hata 1: 'invalid literal for int() with base 10: 'abc'' - Alfabetik karakter sayıya çevrilemez
# Hata 2: 'invalid literal for int() with base 10: '3.14'' - Önce float'a dönüştürün
# Doğru yöntem: int(float('3.14')) = 3
```


**Kod Açıklaması:**
1. **Satır 6-10:** `input()` ile alınan string değeri `int()` ile integer'a çeviriyoruz.
2. **Satır 13-15:** String'i `float()` ile ondalıklı sayıya çeviriyoruz.
3. **Satır 18-20:** Sayıyı `str()` ile string'e çeviriyoruz.
4. **Satır 23-25:** `int()` float değerin ondalık kısmını atar (yuvarlama yapmaz).
5. **Satır 28-30:** `float()` integer'ı ondalıklı sayıya çevirir.
6. **Satır 33-38:** Boolean dönüşümleri: 0, boş string, None `False`; diğer değerler `True` döndürür.
7. **Satır 41-55:** Hatalı dönüşümleri `try-except` ile yakalıyoruz.

### Veri Türü Dönüşüm Akışı


```mermaid
flowchart TD
    A[Kullanıcı Girdisi\n(string)] --> B{int() dönüşümü}
    B -->|Sayısal mı?| C{float() dönüşümü}
    B -->|Değil| D[ValueError]
    C -->|Ondalıklı mı?| E{bool() dönüşümü}
    C -->|Değil| F[Başarılı int]
    E -->|Boş mu?| G[False]
    E -->|Değil| H[True]
    D --> I[Hata Yönetimi\n(try-except)]
    F --> J[Matematiksel İşlemler]
    G --> K[Mantıksal Kontroller]
    H --> K

    style A fill:#f9f,stroke:#333,stroke-width:2px
    style D fill:#ff6b6b,stroke:#333,stroke-width:2px
    style F fill:#51cf66,stroke:#333,stroke-width:2px
    style I fill:#ffd43b,stroke:#333,stroke-width:2px
```


**Diyagram Açıklaması:** Bu akış şeması, kullanıcıdan alınan string bir verinin hangi türlere dönüştürülebileceğini ve hangi durumlarda hata alınacağını gösterir. Mümkün olan dönüşümler yeşil, hatalı durumlar kırmızı, hata yönetimi ise sarı renkle işaretlenmiştir.

### NE ZAMAN TERCİH EDİLİR?
- **int():** Kullanıcıdan alınan yaş, adet gibi tam sayı değerleri için
- **float():** Para, sıcaklık gibi ondalıklı değerler için
- **str():** Sayısal değerleri metin içinde kullanmak için
- **bool():** Bir değerin "var" veya "yok" durumunu kontrol etmek için

### ALTERNATİFLERİ

| Dönüşüm | Fonksiyon | Örnek | Sonuç | Not |
|---------|-----------|-------|-------|-----|
| String → Integer | `int()` | `int("42")` | 42 | Sadece sayısal string'ler için |
| String → Float | `float()` | `float("3.14")` | 3.14 | Ondalıklı sayıları da çevirir |
| String → Boolean | `bool()` | `bool("False")` | True | Boş olmayan string her zaman True |
| Integer → Float | `float()` | `float(5)` | 5.0 | Otomatik ondalık ekler |
| Float → Integer | `int()` | `int(3.9)` | 3 | Aşağı yuvarlar (keser) |
| Sayı → String | `str()` | `str(42)` | "42" | Her zaman başarılı |

### YAYGIN HATALAR

**Hata 1: Ondalıklı string'i direkt integer'a çevirmek**


```python
# Yanlış:
ogrenci sayisi = 250  # SyntaxError: invalid syntax

# Doğru:
ogrenci_sayisi = 250  # Alt çizgi kullanılır
```

0


0


**Hata 2: Boolean dönüşümünü yanlış anlamak**


```python
# Yanlış:
ogrenci sayisi = 250  # SyntaxError: invalid syntax

# Doğru:
ogrenci_sayisi = 250  # Alt çizgi kullanılır
```

1


1


## 5. input() Fonksiyonu

### TANIM
`input()` fonksiyonu, kullanıcıdan klavye aracılığıyla veri almayı sağlayan yerleşik bir Python fonksiyonudur. Aldığı veriyi her zaman string olarak döndürür.

### NEDEN VAR?
Programların çoğu kullanıcıyla etkileşim halindedir. Kullanıcıdan veri almak, programın dinamik ve kullanışlı olmasını sağlar. `input()` olmasaydı, her veriyi kod içinde sabit olarak tanımlamak zorunda kalırdık.

**Günlük Hayat Analojisi:** Bir ATM makinesini düşünün. Sizden şifre, miktar gibi bilgiler ister. Siz tuşlarla cevap verirsiniz. `input()` fonksiyonu da aynı şekilde programın size soru sormasını ve sizin cevap vermenizi sağlar.

### NASIL KULLANILIR?


```python
# Yanlış:
ogrenci sayisi = 250  # SyntaxError: invalid syntax

# Doğru:
ogrenci_sayisi = 250  # Alt çizgi kullanılır
```

2


2


**Kod Açıklaması:**
- **Satır 7-8:** `input()` fonksiyonu ile kullanıcıdan isim ve soyisim alıyoruz. Fonksiyonun içine yazdığımız mesaj, kullanıcıya soru olarak gösterilir.
- **Satır 11-12:** Kullanıcının girdiği yaş bilgisi string olarak gelir (`yas_str`). Bunu `int()` ile tam sayıya çeviriyoruz.
- **Satır 15-16:** Boy bilgisi de string olarak gelir. `float()` ile ondalıklı sayıya çeviriyoruz.
- **Satır 19-21:** f-string kullanarak kullanıcı bilgilerini güzel bir formatta yazdırıyoruz.
- **Satır 24-26:** `type()` fonksiyonu ile her değişkenin türünü kontrol ediyoruz.

### NE ZAMAN TERCİH EDİLİR?
- Kullanıcıdan veri alınması gereken her durumda
- Kullanıcı adı, şifre, arama sorgusu gibi metinsel girdiler için
- Sayısal hesaplamalar yapılacaksa, mutlaka tip dönüşümü ile birlikte kullanılmalı

### ALTERNATİFLERİ
Komut satırı argümanları (`sys.argv`) veya dosyadan okuma gibi alternatifler olsa da, `input()` en basit ve en yaygın kullanıcı etkileşimi yöntemidir.

### YAYGIN HATALAR

**Hata 1: input() çıktısını direkt sayı olarak kullanmak**


```python
# Yanlış:
ogrenci sayisi = 250  # SyntaxError: invalid syntax

# Doğru:
ogrenci_sayisi = 250  # Alt çizgi kullanılır
```

3


3


**Hata 2: Tip dönüşümünde hata yönetimini unutmak**


```python
# Yanlış:
ogrenci sayisi = 250  # SyntaxError: invalid syntax

# Doğru:
ogrenci_sayisi = 250  # Alt çizgi kullanılır
```

4


4


## 6. String Metodları

### TANIM
String metodları, metin verileri üzerinde işlem yapmak için kullanılan hazır fonksiyonlardır. Python'da string'ler değiştirilemez (immutable) olduğu için bu metodlar orijinal string'i değiştirmez, yeni bir string döndürür.

### NEDEN VAR?
Kullanıcı girdileri genellikle düzensizdir: fazladan boşluklar, büyük-küçük harf karışıklıkları içerebilir. String metodları, bu verileri temizlemek ve standartlaştırmak için kullanılır.

**Günlük Hayat Analojisi:** Bir posta kutusuna düşen mektupları düşünün. Bazı mektuplar buruşuk, bazılarının üzerinde fazladan etiketler olabilir. Postacı, mektupları düzeltir, etiketleri temizler ve okunaklı hale getirir. String metodları da aynı işi yapar.

### NASIL KULLANILIR?


```python
# Yanlış:
ogrenci sayisi = 250  # SyntaxError: invalid syntax

# Doğru:
ogrenci_sayisi = 250  # Alt çizgi kullanılır
```

5


5


**Kod Açıklaması:**
- **Satır 8-9:** Kullanıcıdan e-posta ve telefon bilgisi alıyoruz. Kullanıcılar genellikle fazladan boşluk bırakır.
- **Satır 12-13:** `.strip()` metodu ile baştaki ve sondaki tüm boşlukları temizliyoruz.
- **Satır 16:** `.lower()` ile tüm harfleri küçük harfe çeviriyoruz. E-posta adresleri büyük-küçük harf duyarlı olmadığı için bu önemlidir.
- **Satır 19:** `.replace(" ", "")` ile telefon numarasındaki tüm boşlukları kaldırıyoruz.
- **Satır 25-32:** Diğer yaygın string metodlarını gösteriyoruz. `.title()` her kelimenin ilk harfini büyük yapar, `.startswith()` ve `.endswith()` ise string'in belirli bir ifadeyle başlayıp başlamadığını kontrol eder.

### NE ZAMAN TERCİH EDİLİR?
- **.strip():** Kullanıcı girdilerini temizlerken her zaman kullanılmalı
- **.lower()/.upper():** Büyük-küçük harf duyarlılığını kaldırmak için (örneğin, arama işlemlerinde)
- **.replace():** Belirli karakterleri değiştirmek veya kaldırmak için
- **.startswith()/.endswith():** Dosya adı, URL gibi verileri kontrol ederken

### ALTERNATİFLERİ

| Metod | Ne Yapar? | Örnek | Sonuç | Alternatif |
|-------|-----------|-------|-------|------------|
| `.strip()` | Baş ve sondaki boşlukları siler | `" x ".strip()` | "x" | `.lstrip()`, `.rstrip()` |
| `.lower()` | Tüm harfleri küçültür | `"ABC".lower()` | "abc" | `.casefold()` (daha agresif) |
| `.upper()` | Tüm harfleri büyütür | `"abc".upper()` | "ABC" | `.capitalize()` (sadece ilk harf) |
| `.replace()` | Belirtilen karakterleri değiştirir | `"a b".replace(" ","")` | "ab" | Regex (ileri düzey) |
| `.split()` | String'i böler ve liste oluşturur | `"a b c".split()` | ["a","b","c"] | `.rsplit()` |

### YAYGIN HATALAR

**Hata 1: String metodlarının orijinal değişkeni değiştirdiğini sanmak**


```python
# Yanlış:
ogrenci sayisi = 250  # SyntaxError: invalid syntax

# Doğru:
ogrenci_sayisi = 250  # Alt çizgi kullanılır
```

6


6


**Hata 2: Zincirleme metod kullanımında sırayı karıştırmak**


```python
# Yanlış:
ogrenci sayisi = 250  # SyntaxError: invalid syntax

# Doğru:
ogrenci_sayisi = 250  # Alt çizgi kullanılır
```

7


7


## 7. f-string (Formatlı String)

### TANIM
f-string, Python 3.6 ile gelen, değişkenleri ve ifadeleri doğrudan string içine gömmeyi sağlayan modern bir biçimlendirme yöntemidir. String'in başına `f` veya `F` eklenerek kullanılır.

### NEDEN VAR?
Eski yöntemlerde (`%` operatörü veya `.format()`), değişkenleri string içine yerleştirmek için fazladan işlem yapmak gerekiyordu. f-string, değişkenleri doğrudan süslü parantez `{}` içinde kullanarak kodu daha okunabilir ve yazması daha kolay hale getirir.

**Günlük Hayat Analojisi:** Bir mektup yazdığınızı düşünün. Eski yöntemde, önce mektubu yazıp sonra boşluklara isimleri sonradan eklemeniz gerekirdi. f-string ise mektubu yazarken doğrudan isimleri yerine koymanızı sağlar.

### NASIL KULLANILIR?


```python
# Yanlış:
ogrenci sayisi = 250  # SyntaxError: invalid syntax

# Doğru:
ogrenci_sayisi = 250  # Alt çizgi kullanılır
```

8


8


**Kod Açıklaması:**
- **Satır 12:** f-string ile değişkenleri doğrudan string içine yerleştiriyoruz. Süslü parantez `{}` içine yazılan her şey Python tarafından değerlendirilir.
- **Satır 15-18:** Eski yöntemleri gösteriyoruz. `%` operatöründe tür belirteçleri (`%s` string, `%d` integer) kullanmak gerekir. `.format()` metodunda ise sıralı veya isimli parametreler kullanılır.
- **Satır 21-23:** f-string içinde doğrudan ifadeler kullanabiliyoruz. `{10 + 3}` gibi bir ifade, sonucu hesaplanarak string'e eklenir.
- **Satır 26-29:** Ondalık hassasiyeti belirlemek için `:.2f` gibi format belirteçleri kullanıyoruz.
- **Satır 32-35:** Hizalama için `<` (sola), `>` (sağa), `^` (orta) işaretlerini kullanıyoruz.

### NE ZAMAN TERCİH EDİLİR?
- Her zaman! f-string, Python 3.6 ve sonrasında string biçimlendirme için tercih edilen yöntemdir
- Özellikle birden fazla değişkenin string içinde kullanılması gerektiğinde
- Karmaşık ifadelerin string içinde değerlendirilmesi gerektiğinde

### ALTERNATİFLERİ

| Yöntem | Sürüm | Örnek | Okunabilirlik | Hız |
|--------|-------|-------|---------------|-----|
| f-string | Python 3.6+ | `f"Merhaba {isim}"` | ★★★★★ | En hızlı |
|.format() | Python 2.6+ | `"Merhaba {}".format(isim)` | ★★★☆☆ | Orta |
| % operatörü | Python 2.0+ | `"Merhaba %s" % isim` | ★★☆☆☆ | Yavaş |
| + birleştirme | Her zaman | `"Merhaba " + isim` | ★☆☆☆☆ | En yavaş |

### YAYGIN HATALAR

**Hata 1: f-string içinde süslü parantez kullanmak**


```python
# Yanlış:
ogrenci sayisi = 250  # SyntaxError: invalid syntax

# Doğru:
ogrenci_sayisi = 250  # Alt çizgi kullanılır
```

9


9


**Hata 2: Eski Python sürümlerinde kullanmak**


```python
# Yanlış:
print(toplam)  # NameError: name 'toplam' is not defined

# Doğru:
toplam = 0
print(toplam)  # Çıktı: 0
```

0


0


## 8. None Değeri

### TANIM
`None`, bir değişkenin henüz bir değere sahip olmadığını belirten özel bir sabittir. Kendi başına bir veri tipidir (`NoneType`) ve sadece bir tane değeri vardır: `None`.

### NEDEN VAR?
Bazen bir değişken tanımlamak isteriz ama henüz değerini bilmeyiz. Örneğin, bir kullanıcının doğum tarihini soracağız ama henüz sormadık. `None`, bu "henüz bilinmiyor" durumunu temsil etmek için kullanılır.

**Günlük Hayat Analojisi:** Bir otel rezervasyon sistemini düşünün. Müşteri henüz oda numarasını bilmiyor, bu yüzden sistem "oda_numarasi = None" olarak kaydeder. Müşteri check-in yapınca oda numarası atanır.

### NASIL KULLANILIR?


```python
# Yanlış:
print(toplam)  # NameError: name 'toplam' is not defined

# Doğru:
toplam = 0
print(toplam)  # Çıktı: 0
```

1


1


**Kod Açıklaması:**
- **Satır 6-7:** Değişkenlere `None` atayarak henüz değer almadıklarını belirtiyoruz.
- **Satır 13-14:** Kullanıcıdan bilgi aldıktan sonra değişkenlere gerçek değerleri atıyoruz.
- **Satır 20-24:** `is None` ifadesi ile bir değişkenin `None` olup olmadığını kontrol ediyoruz. `is` operatörü, `==` operatöründen farklı olarak, değerlerin aynı nesneyi gösterip göstermediğini kontrol eder.
- **Satır 27-30:** `None`'ın diğer "boş" değerlerle (0, False, boş string) karşılaştırılamayacağını gösteriyoruz. `None` kendine özgü bir değerdir.

### NE ZAMAN TERCİH EDİLİR?
- Bir değişkenin henüz değer almadığı durumlarda başlangıç değeri olarak
- Fonksiyonlarda "değer bulunamadı" durumunu belirtmek için
- Opsiyonel parametrelerin varsayılan değeri olarak

### ALTERNATİFLERİ

| Değer | Tür | Anlamı | Kullanım Yeri |
|-------|-----|--------|---------------|
| `None` | NoneType | Değer yok / bilinmiyor | Henüz atanmamış değişkenler |
| `0` | int | Sayısal sıfır | Matematiksel işlemler |
| `False` | bool | Mantıksal yanlış | Koşul ifadeleri |
| `""` | str | Boş string | Metin işlemleri |
| `[]` | list | Boş liste | Liste işlemleri |

### YAYGIN HATALAR

**Hata 1: None'ı 0 veya False ile karıştırmak**


```python
# Yanlış:
print(toplam)  # NameError: name 'toplam' is not defined

# Doğru:
toplam = 0
print(toplam)  # Çıktı: 0
```

2


2


**Hata 2: None'ı string işlemlerinde kullanmak**


```python
# Yanlış:
print(toplam)  # NameError: name 'toplam' is not defined

# Doğru:
toplam = 0
print(toplam)  # Çıktı: 0
```

3


3


## Bölüm Özeti

Bu bölümde, Python programlamanın temel yapı taşları olan değişkenler ve veri tiplerini detaylı bir şekilde inceledik. İşte öğrendiklerimizin kısa bir özeti:

1. **Değişkenler:** Programda verileri saklamak için kullanılan isimlendirilmiş bellek alanlarıdır. `degisken_adi = deger` şeklinde tanımlanır.

2. **Temel Veri Tipleri:**
  - `int` (tam sayı): `42`, `-5`, `1000`
  - `float` (ondalıklı sayı): `3.14`, `-0.5`, `2.0`
  - `str` (metin): `"Merhaba"`, `'Python'`
  - `bool` (mantıksal): `True`, `False`

3. **type() Fonksiyonu:** Bir değişkenin veri türünü öğrenmek için kullanılır.

4. **Tip Dönüşümleri:** `int()`, `float()`, `str()`, `bool()` fonksiyonları ile veri türleri arasında dönüşüm yapılır.

5. **input() Fonksiyonu:** Kullanıcıdan veri almak için kullanılır, her zaman string döndürür.

6. **String Metodları:** `.strip()`, `.lower()`, `.upper()`, `.replace()` gibi metodlarla metin verileri işlenir.

7. **f-string:** Python 3.6 ile gelen, değişkenleri string içine gömmek için kullanılan modern yöntemdir.

8. **None Değeri:** Bir değişkenin henüz değer almadığını belirtmek için kullanılır.


## Sözlük

| Terim | İngilizcesi | Açıklama |
|-------|-------------|----------|
| Değişken | Variable | Veri saklamak için kullanılan isimlendirilmiş bellek alanı |
| Veri Tipi | Data Type | Bir değişkenin alabileceği değerlerin kümesi |
| Integer | int | Tam sayıları temsil eden veri tipi |
| Float | float | Ondalıklı sayıları temsil eden veri tipi |
| String | str | Metin verilerini temsil eden veri tipi |
| Boolean | bool | Doğru/Yanlış değerlerini temsil eden veri tipi |
| Tip Dönüşümü | Type Casting | Bir veri tipini başka bir veri tipine dönüştürme |
| f-string | f-string | Değişkenleri string içine gömmeyi sağlayan biçimlendirme |
| NoneType | NoneType | "Değer yok" durumunu temsil eden özel tip |
| input() | input() | Kullanıcıdan veri almayı sağlayan fonksiyon |
| type() | type() | Değişkenin türünü döndüren fonksiyon |
| Atama Operatörü | Assignment Operator | `=` işareti, değişkene değer atamak için kullanılır |
| String Metodu | String Method | String'ler üzerinde işlem yapan hazır fonksiyonlar |
| Bellek Adresi | Memory Address | Değişkenin bilgisayar hafızasındaki konumu |
| Sabit | Literal | Kod içinde doğrudan yazılan değer (ör: `42`, `"Merhaba"`) |


## Değerlendirme Soruları

### Doğru/Yanlış Soruları

1. `3.14` değeri integer veri tipindedir. **Yanlış** (float)
2. `type(True)` çıktısı `<class 'bool'>` olur. **Doğru**
3. `"123" + 456` işlemi sonucu `"123456"` olur. **Yanlış** (TypeError)
4. `input()` fonksiyonu her zaman string döndürür. **Doğru**
5. `None` değeri bir boolean ifadesidir. **Yanlış** (NoneType)
6. f-string Python 3.6 ile gelmiştir. **Doğru**
7. `int(3.9)` işlemi sonucu 4 olur. **Yanlış** (3 - aşağı yuvarlar)
8. `"Merhaba".upper()` metodu orijinal stringi değiştirir. **Yanlış** (yeni string oluşturur)

### Boşluk Doldurma Soruları

1. Ondalıklı sayıları temsil eden veri tipi: **float**
2. Bir değişkenin türünü öğrenmek için **type()** fonksiyonu kullanılır
3. Kullanıcıdan veri almak için **input()** fonksiyonu kullanılır
4. Metin verileri **str** veri tipinde saklanır
5. Boş string `""` ifadesinin boolean karşılığı **False**'dur
6. f-string kullanmak için string'in başına **f** harfi eklenir
7. String'deki baş ve sondaki boşlukları silmek için **.strip()** metodu kullanılır
8. `None` değerinin veri tipi **NoneType**'dır


## Uygulama Alıştırmaları

### Alıştırma 1: Kişisel Bilgi Formu
Kullanıcıdan ad, soyad, doğum yılı ve şehir bilgilerini alan bir program yazın. Çıktıyı f-string kullanarak formatlayın.

**İpucu:** `input()` ile veri alın, doğum yılı için `int()` dönüşümü yapın.

### Alıştırma 2: Veri Temizleme
Kullanıcıdan bir e-posta adresi alın ve aşağıdaki işlemleri yapın:
- Baş ve sondaki boşlukları temizleyin
- Tüm harfleri küçültün
- "@" işaretinden sonraki kısmı kontrol edin (geçerli domain mi?)

**İpucu:** `.strip()`, `.lower()`, `.split("@")` metodlarını kullanın.

### Alıştırma 3: Tip Dönüşümleri
Kullanıcıdan iki sayı alın ve aşağıdaki işlemleri yapın:
- Toplama, çıkarma, çarpma, bölme
- Sonuçları f-string ile formatlayın
- Bölme işleminin sonucunu 2 ondalık basamakla gösterin

**İpucu:** `float()` dönüşümü kullanın, `:2f` formatını deneyin.

### Alıştırma 4: None Kontrolü
Bir listede (henüz öğrenmediyseniz, basitçe 3 değişken tanımlayın) bazı değerler None olsun. None olan değerleri tespit edip kullanıcıdan doldurmasını isteyin.

**İpucu:** `is None` ve `is not None` kontrollerini kullanın.


## Sık Yapılan Hatalar ve Çözümleri

| Hata | Açıklama | Çözüm |
|------|----------|-------|
| TypeError: can only concatenate str | String ile sayıyı birleştirmeye çalışmak | Sayıyı `str()` ile string'e çevirin veya f-string kullanın |
| ValueError: invalid literal for int() | Sayısal olmayan bir değeri int'e çevirmeye çalışmak | `try-except` ile hata yönetimi yapın |
| NameError: name 'x' is not defined

| NameError: name 'x' is not defined | Kullanılmadan önce değişkene değer atanmamış | Değişkeni kullanmadan önce tanımlayın ve değer atayın |
| AttributeError: 'int' object has no attribute 'lower' | Sayısal bir değişkende string metodu kullanmaya çalışmak | Metodu kullanmadan önce `str()` ile dönüşüm yapın |
| SyntaxError: f-string: unmatched '(' | f-string içinde parantez dengesizliği | Tüm parantezlerin eşleştiğinden emin olun |


## Değerlendirme Rubriği

| Kriter | Başlangıç (1 puan) | Gelişmekte (2 puan) | Yeterli (3 puan) | İleri (4 puan) |
|--------|-------------------|-------------------|------------------|----------------|
| **Değişken Tanımlama** | Değişken tanımlayamıyor | Basit değişken tanımlayabiliyor | Farklı türlerde değişken tanımlayabiliyor | Dinamik tip kullanımını anlıyor |
| **Veri Tipleri** | Sadece bir türü biliyor | int ve str'yi ayırt edebiliyor | Dört temel türü de biliyor | Tip dönüşümlerini yapabiliyor |
| **input() Kullanımı** | input() fonksiyonunu bilmiyor | input() ile veri alabiliyor | Veriyi uygun türe dönüştürebiliyor | Hatalı girdileri yönetebiliyor |
| **String Metodları** | String metodu bilmiyor | Bir-iki metodu kullanabiliyor | Temel metodları kullanabiliyor | Metod zinciri oluşturabiliyor |
| **f-string** | f-string kullanmıyor | Basit f-string yazabiliyor | İfadeleri f-string'e gömebiliyor | Karmaşık formatlama yapabiliyor |
| **Hata Yönetimi** | Hataları fark etmiyor | Hata mesajını okuyabiliyor | Basit hataları düzeltebiliyor | try-except kullanabiliyor |


## Kaynaklar ve İleri Okuma

### Python Resmi Dokümantasyonu
- [Python Veri Tipleri](https://docs.python.org/3/library/stdtypes.html)
- [Python Yerleşik Fonksiyonlar](https://docs.python.org/3/library/functions.html)
- [f-string Kullanımı](https://docs.python.org/3/reference/lexical_analysis.html#f-strings)

### Çevrimiçi Kaynaklar
- **W3Schools Python Tutorial:** Başlangıç seviyesinde interaktif örnekler
- **Real Python:** Detaylı makaleler ve uygulamalı örnekler
- **Python.org Beginners Guide:** Yeni başlayanlar için rehber

### Pratik Platformları
- **HackerRank Python:** Problem çözerek pratik yapın
- **LeetCode:** Algoritma problemleri ile becerilerinizi geliştirin
- **Codewars:** Farklı zorluk seviyelerinde görevler


## Köprüler (Önceki ve Sonraki Bölümlere)

### Önceki Bölüm: Python'a Giriş ve Kurulum
Bu bölümde öğrendiğiniz değişkenler ve veri tipleri, Python programlama dilinin temel yapı taşlarıdır. Bir önceki bölümde Python'u kurmayı ve ilk programınızı yazmayı öğrenmiştiniz. Şimdi, bu temel kavramlarla programlarınıza veri ekleyip işleyebilir hale geldiniz.

### Sonraki Bölüm: Operatörler ve İfadeler
Bir sonraki bölümde, bu bölümde öğrendiğiniz veri tipleri üzerinde matematiksel, karşılaştırma ve mantıksal işlemler yapmayı öğreneceksiniz. Değişkenlerinizle nasıl hesaplamalar yapacağınızı ve kararlar alacağınızı keşfedeceksiniz.


## Bölüm Sonu Notu

Programlamayı öğrenmek, yeni bir dil öğrenmek gibidir. İlk başta kelimeler ve gramer kuralları karmaşık gelebilir, ancak pratik yaptıkça her şey yerine oturur. Bu bölümde öğrendiğiniz kavramları günlük hayatınızdaki problemlere uygulamaya çalışın. Örneğin, bir alışveriş listesi oluşturmak, arkadaşlarınızın yaşlarını hesaplamak veya bir metni düzenlemek gibi basit görevleri Python ile yapmayı deneyin.

Unutmayın: Hata yapmak öğrenmenin doğal bir parçasıdır. Her hata, yeni bir şey öğrenme fırsatıdır. Python'un hata mesajları size neyin yanlış gittiğini söyler; onları okuyun, anlayın ve düzeltin. Zamanla, hataları daha hızlı fark edecek ve daha az hata yapacaksınız.

Bir sonraki bölümde görüşmek üzere, mutlu kodlamalar!
