---
title: "Python'a Giris ve Kurulum"
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
chapter-alias: bolum-01
chapter_id: bolum-01
chapter_type: core
automation_profile: academic_technical_book_v1
numbering: auto
github_slug: bolum-01
qr_policy: dual_for_code_examples
asset_policy: manual_override
---
# Python'a Giriş ve Kurulum

## Öğrenme Çıktıları

Bu bölümü tamamladığınızda şunları yapabiliyor olacaksınız:

- Python programlama dilinin tarihçesini ve temel özelliklerini açıklayabilme
- Python'u bilgisayarınıza kurup çalıştırabilme
- İlk Python programınızı yazıp çalıştırabilme
- `print()` fonksiyonunu farklı şekillerde kullanabilme
- Python'da doğru girinti ve yorum satırı kullanımını kavrayabilme
- REPL ortamında etkileşimli kod yazabilme

## Ön Bilgi

Bu bölüm için herhangi bir programlama deneyimi gerekmez. Temel bilgisayar kullanımı (dosya kaydetme, terminal açma) yeterlidir.


## Python Programlama Dili

### TANIM

Python, Guido van Rossum tarafından 1991 yılında geliştirilmeye başlanan, genel amaçlı, yüksek seviyeli ve yorumlanan bir programlama dilidir. Okunabilirliği ön planda tutan sözdizimi sayesinde hem yeni başlayanlar hem de profesyoneller tarafından tercih edilir.

### NEDEN VAR?

Python, karmaşık programlama dillerinin (C, Java gibi) yarattığı zorlukları azaltmak için tasarlandı. Guido van Rossum, "Monty Python's Flying Circus" adlı komedi grubuna atıfta bulunarak dilin eğlenceli ve öğrenmesi kolay olmasını hedefledi. Python olmasaydı, veri bilimi, yapay zeka ve web geliştirme gibi alanlarda hızlı prototipleme yapmak çok daha zor olurdu.

**Günlük hayattan analoji:** Python'u, bir inşaat ustasının çok amaçlı çakısı gibi düşünün. Tek bir aletle hem ahşap kesebilir, hem vida sıkabilir hem de şişe açabilirsiniz. Python da tek bir dille web sitesi yapabilir, veri analizi yapabilir veya oyun geliştirebilirsiniz.

### NASIL KULLANILIR?

Python'u kullanmaya başlamak için önce bilgisayarınıza kurmanız gerekir. Aşağıdaki adımları izleyin:

**Windows için:**
1. [python.org](https://python.org) adresine gidin
2. "Downloads" menüsünden Windows için en son Python sürümünü indirin
3. İndirilen `.exe` dosyasını çalıştırın
4. **ÖNEMLİ:** "Add Python to PATH" kutucuğunu işaretleyin
5. "Install Now" butonuna tıklayın

**macOS için:**
1. Terminal'i açın (Cmd+Space, "terminal" yazın)
2. `brew install python3` komutunu çalıştırın (Homebrew yüklüyse)
3. Veya python.org'dan macOS yükleyicisini indirin

**Linux için:**
1. Terminal'i açın
2. `sudo apt update && sudo apt install python3` (Debian/Ubuntu)
3. Veya `sudo dnf install python3` (Fedora)

### NE ZAMAN TERCİH EDİLİR?

Python'u şu durumlarda tercih edin:
- Hızlı prototipleme yapmanız gerekiyorsa
- Veri bilimi, makine öğrenmesi veya yapay zeka projelerinde çalışıyorsanız
- Web geliştirme (Django, Flask ile) yapacaksanız
- Otomasyon ve script yazmanız gerekiyorsa
- Programlamaya yeni başlıyorsanız

### ALTERNATİFLERİ

| Dil | Python'a Göre Avantajı | Python'a Göre Dezavantajı |
|-----|------------------------|---------------------------|
| C | Çok daha hızlı çalışır | Öğrenmesi zordur, bellek yönetimi gerektirir |
| Java | Kurumsal projelerde yaygın | Daha fazla kod yazmayı gerektirir |
| JavaScript | Web tarayıcıda çalışır | Veri bilimi için zayıftır |
| Ruby | Web geliştirmede güçlü | Hız ve kütüphane desteği zayıftır |

### YAYGIN HATALAR

**Hata 1:** Python 2 ile Python 3'ü karıştırmak
- **Çözüm:** Python 2, 2020'de emekli oldu. Her zaman Python 3 kullanın. Terminal'de `python --version` ile kontrol edin.

**Hata 2:** PATH'e eklemeyi unutmak (Windows)
- **Çözüm:** Kurulum sırasında "Add Python to PATH" kutucuğunu işaretleyin. Unuttuysanız, Python'u kaldırıp yeniden yükleyin.


## IDE Seçimi

### TANIM

IDE (Entegre Geliştirme Ortamı), kod yazmayı, hata ayıklamayı ve proje yönetimini kolaylaştıran yazılımlardır. Python için birçok IDE seçeneği bulunur.

### NEDEN VAR?

Basit bir metin editörüyle kod yazmak mümkündür, ancak IDE'ler şu avantajları sağlar:
- Sözdizimi vurgulama (kod renklendirme)
- Otomatik tamamlama
- Hata ayıklama araçları
- Proje yönetimi
- Git entegrasyonu

**Günlük hayattan analoji:** IDE'yi, bir şefin mutfak robotu gibi düşünün. Normal bir bıçakla da sebze doğrayabilirsiniz, ama mutfak robotu işinizi çok daha hızlı ve kolay yapar.

### NASIL KULLANILIR?

**VS Code Kurulumu (Önerilen):**


```python
# 1. https://code.visualstudio.com adresinden VS Code'u indirin
# 2. Kurulumu tamamlayın
# 3. VS Code'u açın, sol menüden Extensions (Uzantılar) bölümüne girin
# 4. "Python" yazın ve Microsoft'un Python uzantısını yükleyin
# 5. Bir klasör oluşturun, içinde "ilk_program.py" dosyası açın
```


**PyCharm Kurulumu:**


```python
# 1. https://www.jetbrains.com/pycharm adresinden indirin
# 2. Community (ücretsiz) sürümü yeterlidir
# 3. Kurulum sihirbazını takip edin
# 4. Yeni proje oluşturun
```


### NE ZAMAN TERCİH EDİLİR?

- **VS Code:** Hafif, hızlı, çok amaçlı. Her seviye için uygun.
- **PyCharm:** Python odaklı, güçlü özellikler. Profesyonel projeler için.
- **IDLE:** Python'la birlikte gelir, basit. Yeni başlayanlar için yeterli.
- **Jupyter Notebook:** Veri bilimi ve eğitim için ideal.

### ALTERNATİFLERİ

| IDE | Avantaj | Dezavantaj |
|-----|---------|------------|
| VS Code | Ücretsiz, hafif, çok dilli | Python'a özel değil |
| PyCharm | Python odaklı, güçlü | Ağır, ücretli sürümü var |
| IDLE | Python'la gelir, basit | Sınırlı özellikler |
| Jupyter | Etkileşimli, görsel | Büyük projeler için uygun değil |

### YAYGIN HATALAR

**Hata 1:** Çok fazla uzantı yüklemek (VS Code)
- **Çözüm:** Sadece ihtiyacınız olan uzantıları yükleyin. Gereksiz uzantılar performansı düşürür.

**Hata 2:** Yanlış Python yorumlayıcısını seçmek
- **Çözüm:** VS Code'da `Ctrl+Shift+P` → "Python: Select Interpreter" ile doğru yorumlayıcıyı seçin.


## İlk Program: "Merhaba Dünya"

### TANIM

"Merhaba Dünya" programı, her programlama dilinde yazılan ilk örnektir. Python'da bu, `print()` fonksiyonu ile yapılır.

### NEDEN VAR?

Bu program, dilin temel sözdizimini, çıktı verme mekanizmasını ve çalışma ortamını test etmek için kullanılır. Başarıyla çalıştığında, kurulumun doğru yapıldığını ve kod yazmaya hazır olduğunuzu gösterir.

**Günlük hayattan analoji:** İlk program, bir araba satın aldıktan sonra yaptığınız ilk sürüş gibidir. Arabanın çalıştığını, direksiyonun ve pedalların işlevsel olduğunu test edersiniz.

### NASIL KULLANILIR?

**Örnek 1:** `ilk_program.py`


```python
# İlk Python programımız: Merhaba Dünya
# Bu program ekrana "Merhaba Dünya!" yazdırır

print("Merhaba Dünya!")  # print() fonksiyonu ile metin yazdırma
# // Çıktı: Merhaba Dünya!

# Farklı veri tiplerini yazdırma
print(42)                # Sayı yazdırma
# // Çıktı: 42

print(3.14)              # Ondalıklı sayı yazdırma
# // Çıktı: 3.14

print("Python", 3, "sürümü")  # Birden çok değer yazdırma
# // Çıktı: Python 3 sürümü
```


**Kod Açıklaması:**
- `print()`: Python'da ekrana çıktı vermek için kullanılan yerleşik fonksiyondur
- `"Merhaba Dünya!"`: Tırnak içinde yazılan metinler string (metin) olarak adlandırılır
- `42` ve `3.14`: Tırnak kullanılmaz, doğrudan sayı yazılır
- `print("Python", 3, "sürümü")`: Virgülle ayırarak birden çok değer yazdırabiliriz

**Çalıştırma:**
1. Kodu `ilk_program.py` olarak kaydedin
2. Terminal'de `python ilk_program.py` yazın
3. Enter'a basın

### NE ZAMAN TERCİH EDİLİR?

- Yeni bir dil öğrenmeye başlarken
- Kurulumu test etmek için
- Basit çıktılar almak gerektiğinde

### ALTERNATİFLERİ

`print()` dışında çıktı verme yöntemleri de vardır, ancak en yaygın ve kolay olanı `print()`'tir.

### YAYGIN HATALAR

**Hata 1:** Tırnakları kapatmayı unutmak


```python
# Yanlış:
print("Merhaba Dünya)  # Hata: eksik tırnak

# Doğru:
print("Merhaba Dünya")
```


**Hata 2:** Büyük/küçük harf hatası


```python
# Yanlış:
Print("Merhaba")  # Hata: Print büyük harfle başlamış

# Doğru:
print("Merhaba")
```


## print() Fonksiyonu Detaylı Kullanımı

### TANIM

`print()`, Python'da ekrana çıktı vermek için kullanılan en temel fonksiyondur. Metin, sayı, değişken gibi farklı veri tiplerini yazdırabilir ve çıktı formatını özelleştirebilir.

### NEDEN VAR?

Program yazarken sonuçları görmek, hataları bulmak ve kullanıcıya bilgi vermek gerekir. `print()` bu işlemler için en basit ve etkili yöntemdir.

**Günlük hayattan analoji:** `print()` fonksiyonunu, bir okulun anons sistemi gibi düşünün. Tek bir merkezden herkese aynı anda mesaj iletebilirsiniz.

### NASIL KULLANILIR?

**Örnek 2:** `print_ornekleri.py`


```python
# print() fonksiyonunun farklı kullanım şekilleri

# 1. Birden çok argüman yazdırma
print("Ad:", "Ahmet", "Yaş:", 25)
# // Çıktı: Ad: Ahmet Yaş: 25

# 2. sep parametresi ile ayırıcı belirleme
print("Ad", "Soyad", "Yaş", sep=" | ")
# // Çıktı: Ad | Soyad | Yaş

# 3. end parametresi ile satır sonu karakterini değiştirme
print("Birinci satır", end=" --- ")
print("İkinci satır")
# // Çıktı: Birinci satır --- İkinci satır

# 4. Kaçış karakterleri kullanma
print("Satır 1\nSatır 2")  # \n ile yeni satır
# // Çıktı:
# // Satır 1
# // Satır 2

print("Ad\tSoyad\tYaş")  # \t ile sekme
# // Çıktı: Ad    Soyad    Yaş

# 5. Özel karakterler kullanma
print("Merhaba \"Dünya\"")  # Tırnak içinde tırnak kullanma
# // Çıktı: Merhaba "Dünya"

print("C:\\Users\\Ahmet")  # Windows yolu yazdırma
# // Çıktı: C:\Users\Ahmet
```


**Kod Açıklaması:**
- `sep` parametresi: Birden çok argüman arasına ne konulacağını belirler (varsayılan: boşluk)
- `end` parametresi: Yazdırma sonunda ne ekleneceğini belirler (varsayılan: `\n`)
- `\n`: Yeni satıra geçme
- `\t`: Sekme (tab) boşluğu bırakma
- `\"`: Tırnak karakterini yazdırma
- `\\`: Ters bölü işaretini yazdırma

### NE ZAMAN TERCİH EDİLİR?

- Hata ayıklama için değişken değerlerini görmek istediğinizde
- Kullanıcıya bilgi vermek gerektiğinde
- Program akışını takip etmek için

### ALTERNATİFLERİ

| Yöntem | Kullanım | Avantaj |
|--------|----------|---------|
| `print()` | Basit çıktı | Kolay, hızlı |
| `f-string` | f"Metin {değişken}" | Değişken ekleme kolay |
| `format()` | "Metin {}".format(değişken) | Esnek formatlama |
| `logging` | logging.info() | Profesyonel loglama |

### YAYGIN HATALAR

**Hata 1:** sep ve end parametrelerini yanlış yazmak


```python
# Yanlış:
print("a", "b", seperator=",")  # Hata: parametre adı yanlış

# Doğru:
print("a", "b", sep=",")  # sep parametresi doğru
```


**Hata 2:** Kaçış karakterlerini yanlış kullanmak


```python
# Yanlış:
print("Satır 1/nSatır 2")  # /n yanlış, \n olmalı

# Doğru:
print("Satır 1\nSatır 2")  # \n doğru kullanım
```


## Python Sözdizimi ve Girinti

### TANIM

Python'da kod blokları, diğer dillerdeki gibi süslü parantezlerle değil, girinti (boşluk veya tab) ile belirtilir. Bu, Python kodunun okunabilirliğini artırır.

### NEDEN VAR?

Girinti zorunluluğu, tüm Python kodlarının tutarlı ve okunabilir olmasını sağlar. Bu özellik, özellikle büyük projelerde kodun anlaşılmasını kolaylaştırır.

**Günlük hayattan analoji:** Bir kitabın içindekiler bölümünü düşünün. Ana başlıklar, alt başlıklar ve alt-alt başlıklar farklı girintilerle gösterilir. Python'daki girinti de aynı işlevi görür.

### NASIL KULLANILIR?

**Örnek 3:** `girinti_ornegi.py`


```python
# Python'da girinti kullanımı
# Doğru girintili kod örneği

yas = 18  # Kullanıcının yaşı

if yas >= 18:  # Eğer yaş 18 veya daha büyükse
    print("Yetişkinsiniz")  # Bu satır if bloğunun içinde
    print("Oy kullanabilirsiniz")  # Aynı girinti seviyesi
else:  # Değilse (yaş 18'den küçükse)
    print("Reşit değilsiniz")  # Bu satır else bloğunun içinde
    print("Büyümeniz gerekiyor")  # Aynı girinti seviyesi

print("Program bitti")  # Bu satır dışarıda, her zaman çalışır

# // Çıktı (yas = 18 için):
# // Yetişkinsiniz
# // Oy kullanabilirsiniz
# // Program bitti

# // Çıktı (yas = 15 için):
# // Reşit değilsiniz
# // Büyümeniz gerekiyor
# // Program bitti
```


**Kod Açıklaması:**
- `if` ve `else` blokları, 4 boşluk girinti ile belirtilir
- Aynı blok içindeki satırlar aynı girinti seviyesinde olmalıdır
- Girinti bittiğinde, blok da biter
- Python'da standart girinti 4 boşluktur (tab da kullanılabilir ama karıştırmayın)

### NE ZAMAN TERCİH EDİLİR?

- Her zaman! Python'da girinti zorunludur
- Kodun okunabilirliğini artırmak için
- Hataları önlemek için (yanlış girinti hata verir)

### ALTERNATİFLERİ

Diğer dillerde girinti isteğe bağlıdır, Python'da zorunludur:

| Dil | Blok Belirleme | Girinti Zorunlu mu? |
|-----|----------------|---------------------|
| Python | Girinti | Evet |
| Java | {} | Hayır |
| C | {} | Hayır |
| JavaScript | {} | Hayır |

### YAYGIN HATALAR

**Hata 1:** Girinti ve tab karıştırmak


```python
# Yanlış:
if True:
    print("Doğru")  # 4 boşluk
	print("Yanlış")  # Tab (Hata!)

# Doğru:
if True:
    print("Doğru")  # 4 boşluk
    print("Doğru")  # 4 boşluk
```


**Hata 2:** Girinti seviyesini bozmak


```python
# 1. https://www.jetbrains.com/pycharm adresinden indirin
# 2. Community (ücretsiz) sürümü yeterlidir
# 3. Kurulum sihirbazını takip edin
# 4. Yeni proje oluşturun
```

0


0


## Yorum Satırları

### TANIM

Yorum satırları, Python yorumlayıcısı tarafından dikkate alınmayan, sadece kodu açıklamak için yazılan metinlerdir. Tek satırlık yorumlar `#` ile, çok satırlı yorumlar `"""` ile başlar.

### NEDEN VAR?

Kod yazarken, belirli bölümlerin ne işe yaradığını, neden öyle yazıldığını veya hangi mantıkla çalıştığını açıklamak gerekir. Yorumlar, kodu daha sonra okuyan kişiler (veya kendiniz) için yol göstericidir.

**Günlük hayattan analoji:** Bir yemek tarifinde, malzemelerin yanında yazılı olan "taze olmalı", "iri doğranmış" gibi notlar yorum satırları gibidir. Tarifin kendisini değiştirmez, ancak uygulamayı kolaylaştırır.

### NASIL KULLANILIR?

**Örnek 4:** `yorum_satirlari.py`


```python
# 1. https://www.jetbrains.com/pycharm adresinden indirin
# 2. Community (ücretsiz) sürümü yeterlidir
# 3. Kurulum sihirbazını takip edin
# 4. Yeni proje oluşturun
```

1


1


**Kod Açıklaması:**
- `#` işareti: Satır başında veya kod sonunda kullanılabilir
- `"""…"""`: Çok satırlı yorum veya docstring için kullanılır
- Docstring: Özel bir yorum türüdür, fonksiyon ve sınıfların belgelendirmesinde kullanılır
- Geçici devre dışı bırakma: Kodun başına `#` ekleyerek çalışmasını engelleyebilirsiniz

### NE ZAMAN TERCİH EDİLİR?

- Karmaşık mantıkları açıklamak için
- Kodun amacını belirtmek için
- Geçici olarak kodları devre dışı bırakmak için
- Fonksiyon ve sınıfların belgelendirmesi için (docstring)

### ALTERNATİFLERİ

| Yöntem | Kullanım | Ne Zaman? |
|--------|----------|-----------|
| `#` | Tek satır | Kısa açıklamalar |
| `"""` | Çok satır | Uzun açıklamalar, docstring |
| `'''` | Çok satır | `"""` ile aynı işlev |

### YAYGIN HATALAR

**Hata 1:** Yorumları gereksiz yere kullanmak


```python
# 1. https://www.jetbrains.com/pycharm adresinden indirin
# 2. Community (ücretsiz) sürümü yeterlidir
# 3. Kurulum sihirbazını takip edin
# 4. Yeni proje oluşturun
```

2


2


**Hata 2:** Yorumları güncellemeyi unutmak


```python
# 1. https://www.jetbrains.com/pycharm adresinden indirin
# 2. Community (ücretsiz) sürümü yeterlidir
# 3. Kurulum sihirbazını takip edin
# 4. Yeni proje oluşturun
```

3


3


## REPL (Read-Eval-Print Loop)

### TANIM

REPL (Read-Eval-Print Loop), Python kodunu satır satır çalıştırabileceğiniz etkileşimli bir kabuk ortamıdır. "Oku-Değerlendir-Yazdır-Döngü" anlamına gelir.

### NEDEN VAR?

REPL, küçük kod parçalarını hızlıca test etmek, hata ayıklamak veya yeni bir kavramı denemek için idealdir. Her seferinde tam bir dosya oluşturmak zorunda kalmazsınız.

**Günlük hayattan analoji:** REPL'i, bir aşçının yemek yaparken ara ara tadına bakması gibi düşünün. Tüm yemeği pişirmeden önce tuzu kontrol eder, baharatı ayarlar.

### NASIL KULLANILIR?

**Örnek 5:** REPL oturumu örneği


```python
# 1. https://www.jetbrains.com/pycharm adresinden indirin
# 2. Community (ücretsiz) sürümü yeterlidir
# 3. Kurulum sihirbazını takip edin
# 4. Yeni proje oluşturun
```

4


4


**Kod Açıklaması:**
- `>>>`: REPL'in komut beklediğini gösteren işaret (prompt)
- Her komut yazıldıktan sonra Enter'a basılır
- Sonuç hemen alt satırda görünür
- Değişkenler oturum boyunca bellekte kalır
- `exit()` veya `quit()` ile çıkılır

### NE ZAMAN TERCİH EDİLİR?

- Küçük kod parçalarını test etmek için
- Yeni bir kavramı öğrenirken denemeler yapmak için
- Hata ayıklama için
- Matematiksel hesaplamalar için

### ALTERNATİFLERİ

| Ortam | Kullanım | Avantaj |
|-------|----------|---------|
| REPL | Terminal | Hızlı, hafif |
| IPython | Gelişmiş REPL | Otomatik tamamlama, geçmiş |
| Jupyter Notebook | Web tabanlı | Görsel, paylaşılabilir |
| Python dosyası |.py dosyası | Tekrar kullanılabilir |

### YAYGIN HATALAR

**Hata 1:** REPL'de çok satırlı kod yazmaya çalışmak


```python
# 1. https://www.jetbrains.com/pycharm adresinden indirin
# 2. Community (ücretsiz) sürümü yeterlidir
# 3. Kurulum sihirbazını takip edin
# 4. Yeni proje oluşturun
```

5


5


**Hata 2:** REPL'de yazılan kodu kaydetmeyi unutmak
- **Çözüm:** Test ettiğiniz kodu bir dosyaya kopyalayın. REPL'de yazılanlar oturum sonunda kaybolur.


## Diyagramlar

### Diyagram 1: Python Kurulum Süreci


```python
# 1. https://www.jetbrains.com/pycharm adresinden indirin
# 2. Community (ücretsiz) sürümü yeterlidir
# 3. Kurulum sihirbazını takip edin
# 4. Yeni proje oluşturun
```

6


6


**Açıklama:** Bu diyagram, Python kurulum sürecini adım adım gösterir. İşletim sistemi seçimiyle başlayan süreç, kurulum, PATH kontrolü ve test aşamalarından geçer. Herhangi bir sorun durumunda, ilgili adıma geri dönülür.

### Diyagram 2: Kod Çalıştırma Süreci


```python
# 1. https://www.jetbrains.com/pycharm adresinden indirin
# 2. Community (ücretsiz) sürümü yeterlidir
# 3. Kurulum sihirbazını takip edin
# 4. Yeni proje oluşturun
```

7


7


**Açıklama:** Bu sequence diyagramı, bir Python programının yazılmasından çalıştırılmasına kadar geçen süreci gösterir. Kullanıcı kodu yazar, kaydeder, Python yorumlayıcısı dosyayı okur, sözdizimini kontrol eder, bayt koduna çevirir ve sanal makinede çalıştırarak sonucu konsola gönderir.


## Özet

Bu bölümde Python programlama dilinin temellerini öğrendik:

- **Python nedir?** Genel amaçlı, yorumlanan, yüksek seviyeli bir programlama dili
- **Kurulum:** python.org'dan indirip, PATH'e ekleyerek kurulum yapılır
- **IDE Seçimi:** VS Code, PyCharm, IDLE gibi araçlar kod yazmayı kolaylaştırır
- **İlk Program:** `print("Merhaba Dünya!")` ile başlanır
- **print() Fonksiyonu:** sep, end parametreleri ve kaçış karakterleriyle özelleştirilebilir
- **Girinti:** Python'da kod blokları girintiyle belirtilir, 4 boşluk standarttır
- **Yorum Satırları:** `#` ile tek satır, `"""` ile çok satırlı yorum yapılır
- **REPL:** Terminal'de `python` yazarak etkileşimli kod çalıştırılır


## Sözlük

| Terim | Açıklama |
|-------|----------|
| **Interpreter (Yorumlayıcı)**

| **Interpreter (Yorumlayıcı)** | Python kodunu satır satır okuyup çalıştıran program |
| **IDE** | Kod yazmayı kolaylaştıran entegre geliştirme ortamı |
| **REPL** | Read-Eval-Print Loop: Kod satır satır çalıştıran etkileşimli kabuk |
| **Sözdizimi (Syntax)** | Kod yazma kuralları bütünü |
| **Girinti (Indentation)** | Kod bloklarını belirtmek için kullanılan boşluklar |
| **Yorum Satırı (Comment)** | Kod açıklaması yapan, çalıştırılmayan satırlar |
| **String** | Metin veri tipi |
| **Literal** | Doğrudan yazılan değişmez değer |
| **Konsol** | Kod çıktısının görüntülendiği terminal ekranı |
| **Argüman** | Fonksiyona gönderilen değer |
| **Parametre** | Fonksiyonun tanımlandığı değişken |
| **Fonksiyon** | Belirli bir işi yapan kod bloğu |
| **Kaçış Karakteri** | Özel anlam taşıyan karakterler (\n, \t) |
| **Docstring** | Fonksiyonları belgelendirmek için kullanılan çok satırlı yorum |
| **PATH** | İşletim sisteminin programları bulmak için kullandığı dizin listesi |


## Sorular

### Doğru/Yanlış

1. **Python yorumlanan bir dildir.** (D)
  - *Açıklama:* Python kodu satır satır yorumlanarak çalıştırılır.

2. **print() fonksiyonu sayıları yazdıramaz.** (Y)
  - *Açıklama:* `print(42)` ile sayılar da yazdırılabilir.

3. **Python'da kod blokları süslü parantezle belirtilir.** (Y)
  - *Açıklama:* Python'da kod blokları girintiyle belirtilir.

4. **Yorum satırları Python tarafından çalıştırılır.** (Y)
  - *Açıklama:* Yorum satırları tamamen göz ardı edilir.

5. **REPL, kod satır satır çalıştırmaya olanak tanır.** (D)
  - *Açıklama:* REPL'de her satır yazıldığı anda çalıştırılır.

### Boşluk Doldurma

1. Ekrana çıktı vermek için **print()** fonksiyonu kullanılır.
2. Python'da tek satır yorum **#** işareti ile başlar.
3. Python kod bloklarını belirlemek için **girinti** kullanılır.
4. Python'u etkileşimli olarak çalıştırmak için terminale **python** yazılır.
5. Python 3'ün ilk kararlı sürümü **2008** yılında yayımlanmıştır.


## Alıştırmalar

### Alıştırma 1: Kişisel Tanıtım Programı (★☆☆☆☆)
Kullanıcının adını, yaşını ve şehrini `print()` ile ekrana yazdıran bir program yazın. Her bilgi ayrı satırda olacak.

**Beklenen Çıktı:**


```python
# 1. https://www.jetbrains.com/pycharm adresinden indirin
# 2. Community (ücretsiz) sürümü yeterlidir
# 3. Kurulum sihirbazını takip edin
# 4. Yeni proje oluşturun
```

8


8


**İpucu:** Üç ayrı `print()` çağrısı yapabilir veya tek `print()` içinde `\n` kullanabilirsiniz.


### Alıştırma 2: Şiir Yazdırma (★★☆☆☆)
Sevdiğiniz bir şiirin 4 dizesini `print()` ile yazdırın. Kodun başına yorum satırı ekleyerek şiirin adını ve şairini belirtin.

**Beklenen Çıktı:**


```python
# 1. https://www.jetbrains.com/pycharm adresinden indirin
# 2. Community (ücretsiz) sürümü yeterlidir
# 3. Kurulum sihirbazını takip edin
# 4. Yeni proje oluşturun
```

9


9


**İpucu:** Her dizeyi ayrı `print()` ile yazdırabilir veya tek `print()` içinde `\n` kullanabilirsiniz.


### Alıştırma 3: Hesap Makinesi Çıktısı (★★☆☆☆)
Aşağıdaki matematik işlemlerinin sonuçlarını `print()` ile ekrana yazdırın:
- 15 + 3
- 20 - 8
- 6 * 7
- 42 / 2
- 2 ** 10 (üs alma)

**Beklenen Çıktı:**


```python
# İlk Python programımız: Merhaba Dünya
# Bu program ekrana "Merhaba Dünya!" yazdırır

print("Merhaba Dünya!")  # print() fonksiyonu ile metin yazdırma
# // Çıktı: Merhaba Dünya!

# Farklı veri tiplerini yazdırma
print(42)                # Sayı yazdırma
# // Çıktı: 42

print(3.14)              # Ondalıklı sayı yazdırma
# // Çıktı: 3.14

print("Python", 3, "sürümü")  # Birden çok değer yazdırma
# // Çıktı: Python 3 sürümü
```

0


0


**İpucu:** `print("15 + 3 =", 15+3)` şeklinde metin ve işlemi birleştirebilirsiniz.


### Alıştırma 4: Girinti Hatalarını Düzeltme (★★★☆☆)
Aşağıdaki hatalı kodu düzeltin:


```python
# İlk Python programımız: Merhaba Dünya
# Bu program ekrana "Merhaba Dünya!" yazdırır

print("Merhaba Dünya!")  # print() fonksiyonu ile metin yazdırma
# // Çıktı: Merhaba Dünya!

# Farklı veri tiplerini yazdırma
print(42)                # Sayı yazdırma
# // Çıktı: 42

print(3.14)              # Ondalıklı sayı yazdırma
# // Çıktı: 3.14

print("Python", 3, "sürümü")  # Birden çok değer yazdırma
# // Çıktı: Python 3 sürümü
```

1


1


**Beklenen Çıktı:**


```python
# İlk Python programımız: Merhaba Dünya
# Bu program ekrana "Merhaba Dünya!" yazdırır

print("Merhaba Dünya!")  # print() fonksiyonu ile metin yazdırma
# // Çıktı: Merhaba Dünya!

# Farklı veri tiplerini yazdırma
print(42)                # Sayı yazdırma
# // Çıktı: 42

print(3.14)              # Ondalıklı sayı yazdırma
# // Çıktı: 3.14

print("Python", 3, "sürümü")  # Birden çok değer yazdırma
# // Çıktı: Python 3 sürümü
```

2


2


**İpucu:** İçteki `if` bloğu 4 boşluk, onun içindeki `print()` 8 boşluk girintili olmalı.


### Alıştırma 5: REPL Denemeleri (★★☆☆☆)
Terminalde Python REPL'i açın ve aşağıdaki işlemleri sırayla yapın:
1. `3 + 5` yazın
2. `"Merhaba " + "Dünya"` yazın
3. `10 * 2` yazın
4. `print("REPL'deyim!")` yazın
5. `exit()` ile REPL'den çıkın

**Beklenen Çıktı (her satır için):**


```python
# İlk Python programımız: Merhaba Dünya
# Bu program ekrana "Merhaba Dünya!" yazdırır

print("Merhaba Dünya!")  # print() fonksiyonu ile metin yazdırma
# // Çıktı: Merhaba Dünya!

# Farklı veri tiplerini yazdırma
print(42)                # Sayı yazdırma
# // Çıktı: 42

print(3.14)              # Ondalıklı sayı yazdırma
# // Çıktı: 3.14

print("Python", 3, "sürümü")  # Birden çok değer yazdırma
# // Çıktı: Python 3 sürümü
```

3


3


## Sık Yapılan Hatalar ve Çözümleri

| Hata | Neden | Çözüm |
|------|-------|-------|
| **SyntaxError: invalid syntax** | Yanlış sözdizimi (tırnak, parantez eksik) | Tırnak ve parantezlerin eşleştiğini kontrol edin |
| **IndentationError: unexpected indent** | Gereksiz veya yanlış girinti | Kod bloklarının hizasını kontrol edin |
| **NameError: name '…' is not defined** | Tanımlanmamış değişken veya fonksiyon | Değişken/fonksiyon adını doğru yazdığınızdan emin olun |
| **TypeError: can only concatenate str to str** | Farklı tipleri birleştirmeye çalışmak | Sayıyı `str()` ile metne çevirin |
| **Python bulunamadı hatası** | PATH ayarı yapılmamış | Python'u yeniden yükleyin veya PATH'i manuel ekleyin |


## Kaynaklar ve İleri Okuma

1. **Resmi Python Belgeleri:** [docs.python.org/3/tutorial/](https://docs.python.org/3/tutorial/)
2. **Python.org İndirme Sayfası:** [python.org/downloads/](https://www.python.org/downloads/)
3. **VS Code Python Eklentisi:** [marketplace.visualstudio.com/items? itemName=ms-python.python](https://marketplace.visualstudio.com/items? itemName=ms-python.python)
4. **PyCharm İndirme:** [jetbrains.com/pycharm/download/](https://www.jetbrains.com/pycharm/download/)
5. **Python 3'ün Tarihçesi:** [python.org/doc/versions/](https://www.python.org/doc/versions/)
6. **Türkçe Kaynak:** Python 3 için Türkçe Kaynak - İstanbul Kodluyoruz


## Bölüm Sonu Rubrik

| Kriter | Başlangıç (1) | Gelişmekte (2) | Yeterli (3) | İleri (4) |
|--------|---------------|----------------|-------------|-----------|
| Python Kurulumu | İndiremedi | İndirdi ama kuramadı | Başarıyla kurdu | Farklı işletim sistemlerinde kurabilir |
| İlk Program | Kod yazamadı | Yazdı ama çalıştıramadı | "Merhaba Dünya" yazdırdı | print() parametrelerini kullanabilir |
| Girinti Kullanımı | Girinti hatası alıyor | Bazen doğru kullanıyor | Her zaman doğru girintiliyor | İç içe blokları yönetebiliyor |
| Yorum Satırları | Hiç yorum eklemiyor | Sadece tek satır yorum | Çok satırlı yorum kullanıyor | Docstring ile belgelendirme yapıyor |
| REPL Kullanımı | REPL'i açamıyor | Sadece basit işlemler | print() kullanabiliyor | Karmaşık ifadeler deneyebiliyor |


## Köprü: Bir Sonraki Bölüme Hazırlık

Bu bölümde Python'un temel yapı taşlarını öğrendiniz. Artık bir Python programı yazabilir, çalıştırabilir ve hataları ayıklayabilirsiniz. Bir sonraki bölümde **Değişkenler ve Veri Tipleri** konusuna geçeceğiz. Orada:

- Değişkenlerin nasıl tanımlandığını ve kullanıldığını
- Sayılar (int, float), metinler (str) ve mantıksal değerler (bool) gibi temel veri tiplerini
- Tip dönüşümlerini ve tip kontrolünü
- Değişken isimlendirme kurallarını

öğreneceksiniz. Hazır mısınız? Python maceranız daha yeni başlıyor!
