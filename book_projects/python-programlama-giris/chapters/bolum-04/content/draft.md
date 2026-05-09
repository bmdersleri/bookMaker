---
title: "Fonksiyonlar ve Moduller"
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
chapter-alias: bolum-04
chapter_id: bolum-04
chapter_type: core
automation_profile: academic_technical_book_v1
numbering: auto
github_slug: bolum-04
qr_policy: dual_for_code_examples
asset_policy: manual_override
---
***
# Fonksiyonlar ve Modüller

## Bölüme Hoş Geldiniz

Bu bölümde, Python programlamanın belkemiğini oluşturan iki temel yapı taşını keşfedeceğiz: **Fonksiyonlar** ve **Modüller**. Kodlarınızı daha düzenli, tekrar kullanılabilir ve yönetilebilir hale getirmeyi öğreneceksiniz.

### Ön Bilgi
Bu bölüme başlamadan önce aşağıdaki kavramlara hakim olmanız beklenir:
- Temel veri tipleri (int, float, str, bool)
- Listeler ve sözlükler
- `if/elif/else` koşul yapıları
- `for` ve `while` döngüleri

### Öğrenme Çıktıları
Bu bölümü tamamladığınızda aşağıdakileri yapabiliyor olacaksınız:
1. Kendi fonksiyonlarınızı `def` anahtar kelimesiyle tanımlayıp çağırabilecek,
2. Fonksiyonlara parametrelerle girdi verip `return` ile çıktı alabilecek,
3. Esnek fonksiyonlar yazmak için `*args` ve `**kwargs` kullanabilecek,
4. Kısa ve öz işlemler için `lambda` ifadeleri oluşturabilecek,
5. `map()` ve `filter()` fonksiyonlarıyla veri kümeleri üzerinde işlem yapabilecek,
6. Değişkenlerin görünürlük alanı (scope) kurallarını anlayıp doğru kullanabilecek,
7. Python'un zengin standart kütüphanesinden (`math`, `random`, `datetime`) modülleri içe aktarıp kullanabileceksiniz.


## Fonksiyonlar: Kodunuzu Paketleyin

### 1. `def` ile Fonksiyon Tanımlama

**1. TANIM:**
Fonksiyon, belirli bir işi yapmak için bir araya getirilmiş, adlandırılmış ve tekrar tekrar kullanılabilen kod bloklarıdır. `def` anahtar kelimesiyle tanımlanır.

**2. NEDEN VAR?**
Fonksiyonlar olmasaydı, aynı kod parçalarını programınızın her ihtiyacınız olduğunda kopyalayıp yapıştırmak zorunda kalırdınız. Bu, programınızı şişirir, okunmasını zorlaştırır ve en önemlisi, bir hata bulduğunuzda veya bir iyileştirme yapmak istediğinizde, kodun her kopyasını tek tek düzeltmeniz gerekirdi. Fonksiyonlar, "Bir kere yaz, her yerde kullan" prensibinin temelidir.

**Günlük Hayat Analojisi:**
Bir kahve makinesi düşünün. Her kahve yapmak istediğinizde, kahve çekirdeklerini öğütüp, suyu kaynatıp, filtreyi yerleştirip tüm işlemleri sıfırdan yapmazsınız. Sadece bir düğmeye basarsınız. İşte fonksiyon da bu düğme gibidir; karmaşık bir işlemi (kahve yapma) tek bir komutla (düğmeye basma) başlatmanızı sağlar.

**3. NASIL KULLANILIR?**


```python
# 01_ilk_fonksiyon.py

# 1. Fonksiyonumuzu tanımlıyoruz: 'selamla' adında, parametre almayan bir fonksiyon
def selamla():
    """
    Bu fonksiyon ekrana basit bir selamlama mesajı yazar.
    """
    print("Merhaba! Python fonksiyonlarına hoş geldiniz!")

# 2. Fonksiyonu çağırıyoruz. Bu, tanımlanan kodu çalıştırır.
selamla()

# 3. Fonksiyonu birden fazla kez çağırabiliriz.
selamla()
selamla()

# Çıktı:
# Merhaba! Python fonksiyonlarına hoş geldiniz!
# Merhaba! Python fonksiyonlarına hoş geldiniz!
# Merhaba! Python fonksiyonlarına hoş geldiniz!
```


**Kod Açıklaması:**
- `def selamla():` satırı, `selamla` isminde bir fonksiyon tanımlar. İki nokta üst üste (`:`) fonksiyonun kod bloğunun başlayacağını belirtir.
- `"""…"""` içindeki yorum satırı (docstring), fonksiyonun ne yaptığını açıklamak için kullanılır. Profesyonel kod yazımında önemlidir.
- `print(…)` ifadesi, fonksiyon çağrıldığında yapılacak olan tek işlemdir.
- `selamla()` yazdığımızda, Python yukarıda tanımladığımız fonksiyonun kod bloğuna gider ve içindeki tüm kodları çalıştırır.

**4. NE ZAMAN TERCİH EDİLİR?**
- Aynı kod bloğunu programınızda birden fazla kez kullanmanız gerektiğinde her zaman tercih edilir.
- Uzun ve karmaşık bir işlemi daha küçük, yönetilebilir parçalara bölmek (böl-ve-yönet taktiği) için idealdir.
- Kodunuzun okunabilirliğini artırmak için, bir işleme anlamlı bir isim vermek istediğinizde kullanılır.

**5. ALTERNATİFLERİ:**
Bir kod bloğunu tekrar kullanmanın alternatifi, kodu kopyala-yapıştır yapmaktır. Ancak bu yöntem, yukarıda da belirtildiği gibi, birçok dezavantaja sahiptir. Fonksiyonlar bu sorunları çözer.

| Özellik | Fonksiyon Kullanmak | Kodu Kopyala-Yapıştır |
|:--- |:--- |:--- |
| **Tekrar Kullanım** | Kolay, sadece ismini yazarsın | Zor, her seferinde bloğu bulup kopyalamalısın |
| **Bakım** | Çok kolay, sadece fonksiyonu değiştir | Çok zor, her kopyayı tek tek bulup değiştirmelisin |
| **Okunabilirlik** | Yüksek, anlamlı isimlerle | Düşük, kod şişer |
| **Hata Ayıklama** | Kolay, hata fonksiyonun içinde aranır | Zor, hata her kopyada olabilir |

**6. YAYGIN HATALAR:**
- **Hata:** Fonksiyonu tanımlamadan önce çağırmaya çalışmak.


```python
  # Hatalı Kullanım
  selamla()  # NameError: name 'selamla' is not defined

  def selamla():
      print("Merhaba")
```


  **Çözüm:** Python kodu yukarıdan aşağıya okur. Fonksiyonu çağırmadan önce mutlaka tanımlamış olmalısınız.

### 2. Parametreler ve Argümanlar

**1. TANIM:**
Fonksiyonlara dışarıdan veri göndermek için kullanılan araçlardır. **Parametreler**, fonksiyon tanımlanırken parantez içinde yazılan değişkenlerdir. **Argümanlar** ise fonksiyon çağrılırken bu parametrelere gönderilen gerçek değerlerdir.

**2. NEDEN VAR?**
Bir fonksiyon her çağrıldığında aynı işlemi yapıyorsa çok da kullanışlı değildir. Parametreler sayesinde fonksiyon, aldığı girdiye göre farklı çıktılar üretebilir. Bu, fonksiyonları esnek ve güçlü kılar.

**Tarihsel Bağlam:**
Parametre kavramı, ilk programlama dillerinden beri vardır. Python'da varsayılan parametreler ve esnek argüman alma (`*args, **kwargs`) gibi özellikler, dilin zamanla kullanıcı dostu ve esnek hale gelmesiyle eklenmiştir.

**3. NASIL KULLANILIR?**


```python
## 01_ilk_fonksiyon.py (devamı)

## Parametre alan bir fonksiyon: 'kisiyeSelamVer' adında, 'isim' parametreli
def kisiyeSelamVer(isim):
    """
    Verilen ismi kullanarak kişiselleştirilmiş bir selamlama yazar.
    """
    print(f"Merhaba {isim}! Nasılsın?")

## Fonksiyonu farklı argümanlarla çağırıyoruz
kisiyeSelamVer("Ali")     # Argüman: "Ali"
kisiyeSelamVer("Ayşe")    # Argüman: "Ayşe"
kisiyeSelamVer("Mehmet")  # Argüman: "Mehmet"

## Çıktı:
## Merhaba Ali! Nasılsın?
## Merhaba Ayşe! Nasılsın?
## Merhaba Mehmet! Nasılsın?

## Varsayılan parametre kullanımı
def kisiyeSelamVerVarsayilan(isim, selam="Merhaba"):
    """
    Varsayılan bir selamlama ile fonksiyon.
    """
    print(f"{selam} {isim}!")

kisiyeSelamVerVarsayilan("Zeynep")          # Varsayılan selam kullanılır
kisiyeSelamVerVarsayilan("Ahmet", "Günaydın")  # Selam argümanı verilir

## Çıktı:
## Merhaba Zeynep!
## Günaydın Ahmet!
```


**Kod Açıklaması:**
- `def kisiyeSelamVer(isim):` satırında `isim` bir **parametredir**. Fonksiyonun içinde bir değişken gibi kullanılır.
- `kisiyeSelamVer("Ali")` satırında `"Ali"` bir **argümandır**. Bu değer, fonksiyon içindeki `isim` parametresine atanır.
- `def kisiyeSelamVerVarsayilan(isim, selam="Merhaba"):` satırında `selam` parametresine varsayılan bir değer (`"Merhaba"`) atanmıştır. Eğer fonksiyon çağrılırken bu parametre için bir argüman verilmezse, varsayılan değer kullanılır.

**4. NE ZAMAN TERCİH EDİLİR?**
- Fonksiyonun davranışını dışarıdan kontrol etmek istediğinizde parametre kullanırsınız.
- Varsayılan parametreler, çoğu durumda aynı değerle çalışan ancak nadiren özelleştirme gerektiren fonksiyonlar için idealdir. Örneğin, bir dosya açma fonksiyonu varsayılan olarak `"r"` (okuma) modunda çalışabilir.

**5. ALTERNATİFLERİ:**
Parametre kullanmamak, fonksiyonun sadece global değişkenlere bağımlı olması anlamına gelir. Bu, fonksiyonun bağımsızlığını ve tekrar kullanılabilirliğini ciddi şekilde kısıtlar. Parametreler, fonksiyonları "kara kutu" haline getirir; girdi verirsiniz, çıktı alırsınız.

**6. YAYGIN HATALAR:**
- **Hata:** Varsayılan parametreleri, varsayılan olmayan parametrelerin önüne koymak.


```python
  # Hatalı Kullanım
  def hataFonksiyonu(selam="Merhaba", isim):  # SyntaxError: non-default argument follows default argument
      print(f"{selam} {isim}")
```


  **Çözüm:** Python'da kural nettir: Varsayılan değeri olmayan parametreler (zorunlu olanlar) her zaman önce, varsayılan değeri olanlar (isteğe bağlı olanlar) ise sonra yazılmalıdır.

### 3. `return` ile Değer Döndürme

**1. TANIM:**
`return` ifadesi, bir fonksiyonun ürettiği sonucu, çağrıldığı yere geri göndermesini sağlar. Fonksiyon bu ifadeye geldiğinde çalışmasını durdurur ve belirtilen değeri döndürür.

**2. NEDEN VAR?**
`return` olmasaydı, fonksiyonlar sadece ekrana yazdırma (`print`) gibi yan etkiler oluşturabilirdi. Oysa bir fonksiyonun asıl gücü, bir hesaplama yapıp sonucu programın başka bir yerinde kullanılmak üzere döndürebilmesidir. `print` sadece ekrana gösterir, `return` ise değeri kullanılabilir hale getirir.

**Günlük Hayat Analojisi:**
Bir fırına gidip "Bana bir ekmek verir misiniz?" dersiniz. Fırıncı size ekmeği verir. İşte bu, `return` gibidir. Eğer fırıncı ekmeği yapıp sadece kendisi izleseydi ve size gösterseydi, bu `print` gibi olurdu. Siz ekmeği alamaz, yiyemez veya başkasına veremezdiniz.

**3. NASIL KULLANILIR?**


```python
# 01_ilk_fonksiyon.py (devamı)

# İki sayıyı toplayıp sonucu döndüren fonksiyon
def topla(sayi1, sayi2):
    """
    İki sayıyı toplar ve sonucu döndürür.
    """
    sonuc = sayi1 + sayi2
    return sonuc  # Hesaplanan sonucu dışarıya gönder

# Fonksiyonun döndürdüğü değeri bir değişkende saklıyoruz
toplamDegeri = topla(5, 3)
print(f"5 + 3'ün toplamı: {toplamDegeri}")

# Dönen değeri doğrudan da kullanabiliriz
print(f"10 + 20'nin toplamı: {topla(10, 20)}")

# Çıktı:
# 5 + 3'ün toplamı: 8
# 10 + 20'nin toplamı: 30

# return olmadan fonksiyon None döndürür
def sadeceYazdir(mesaj):
    print(mesaj)

donenDeger = sadeceYazdir("Bu bir test")
print(f"Fonksiyonun döndürdüğü değer: {donenDeger}")

# Çıktı:
# Bu bir test
# Fonksiyonun döndürdüğü değer: None
```


**Kod Açıklaması:**
- `return sonuc` ifadesi, `sonuc` değişkenindeki değeri (8) fonksiyonun çağrıldığı yere (`toplamDegeri = topla(5,3)`) geri gönderir.
- `toplamDegeri` değişkeni artık `8` değerini tutar.
- `sadeceYazdir` fonksiyonu `return` içermez. Bu tür fonksiyonlar, çağrıldıklarında özel bir değer olan `None`'ı döndürürler.

**4. NE ZAMAN TERCİH EDİLİR?**
- Bir hesaplama yapıp sonucu programın başka bir yerinde kullanacaksanız `return` kullanmalısınız.
- Sadece bir işlem yapıp (örneğin bir dosyaya yazmak, bir butonun rengini değiştirmek) herhangi bir değer döndürmeye gerek yoksa `return` kullanmazsınız.

**5. ALTERNATİFLERİ:**
`return`'ün alternatifi, sonucu global bir değişkende saklamaktır. Ancak bu, fonksiyonları bağımlı hale getirir ve hatalara yol açar. `return`, temiz ve güvenilir bir veri akışı sağlar.

**6. YAYGIN HATALAR:**
- **Hata:** `return`'den sonra kod yazmak.


```python
  def hataFonksiyonu():
      return "Bitti"
      print("Bu satır asla çalışmaz!")  # Ulaşılamaz kod (unreachable code)
```


  **Çözüm:** `return` ifadesi fonksiyonu sonlandırır. `return`'den sonra yazılan hiçbir kod çalışmaz.

### 4. `*args` ve `**kwargs` ile Esneklik

**1. TANIM:**
`*args` ve `**kwargs`, bir fonksiyonun tanımlandığından daha fazla sayıda argüman almasını sağlayan özel parametrelerdir. `*args` (arguments) fazladan gelen konumsal argümanları bir **tuple** olarak, `**kwargs` (keyword arguments) ise fazladan gelen anahtar-değer argümanlarını bir **sözlük** olarak toplar.

**2. NEDEN VAR?**
Bazen bir fonksiyonun kaç tane argüman alacağını önceden bilemeyiz. Örneğin, bir ortalama hesaplama fonksiyonu istediğiniz kadar sayıyı alabilmelidir. `*args` ve `**kwargs` bu tür durumlar için esneklik sağlar.

**Tarihsel Bağlam:**
`*args` ve `**kwargs` kullanımı Python'da uzun süredir vardır. `*` operatörünün bu şekilde kullanılması, fonksiyon imzalarını çok daha esnek hale getiren önemli bir dil özelliğidir.

**3. NASIL KULLANILIR?**


```python
## 03_ortalama_hesapla.py

## *args kullanımı: Değişken sayıda konumsal argüman alır
def ortalamaHesapla(*sayilar):
    """
    Verilen tüm sayıların ortalamasını hesaplar.
    *args, gelen tüm argümanları 'sayilar' adında bir tuple olarak toplar.
    """
    toplam = sum(sayilar)  # Tuple'ın toplamını al
    adet = len(sayilar)    # Tuple'ın uzunluğunu (eleman sayısını) al
    if adet == 0:
        return 0
    return toplam / adet

## Farklı sayıda argümanla çağırma
print(f"Ortalama (3, 5): {ortalamaHesapla(3, 5)}")
print(f"Ortalama (10, 20, 30, 40): {ortalamaHesapla(10, 20, 30, 40)}")
print(f"Ortalama (): {ortalamaHesapla()}")  # Hiç argüman yok

## Çıktı:
## Ortalama (3, 5): 4.0
## Ortalama (10, 20, 30, 40): 25.0
## Ortalama (): 0


## **kwargs kullanımı: Değişken sayıda anahtar-değer argümanı alır
def ogrenciBilgisi(**bilgiler):
    """
    Öğrenci bilgilerini yazdırır.
    **kwargs, gelen tüm anahtar-değer çiftlerini 'bilgiler' adında bir sözlük olarak toplar.
    """
    print("Öğrenci Bilgileri:")
    for anahtar, deger in bilgiler.items():
        print(f"  - {anahtar}: {deger}")

## Farklı anahtarlarla çağırma
ogrenciBilgisi(isim="Ali", yas=20, bolum="Bilgisayar Mühendisliği")
ogrenciBilgisi(okul="Anadolu Lisesi", sinif="12-A")

## Çıktı:
## Öğrenci Bilgileri:
##   - isim: Ali
##   - yas: 20
##   - bolum: Bilgisayar Mühendisliği
## Öğrenci Bilgileri:
##   - okul: Anadolu Lisesi
##   - sinif: 12-A
```


**Kod Açıklaması:**
- `*sayilar` parametresi, `ortalamaHesapla(3, 5)` çağrısında `(3, 5)` tuple'ını oluşturur.
- `**bilgiler` parametresi, `ogrenciBilgisi(isim="Ali", yas=20)` çağrısında `{"isim": "Ali", "yas": 20}` sözlüğünü oluşturur.

**4. NE ZAMAN TERCİH EDİLİR?**
- Fonksiyonun alacağı argüman sayısı kesin değilse `*args` kullanılır. (Örn: toplama, ortalama, birleştirme fonksiyonları)
- Fonksiyonun alacağı anahtar-değer çiftleri önceden bilinmiyorsa `**kwargs` kullanılır. (Örn: yapılandırma ayarları, opsiyonel veriler)

**5. ALTERNATİFLERİ:**
Alternatif, argümanları bir liste veya sözlük olarak tek bir parametrede göndermektir. Ancak bu, fonksiyonu çağıran kişi için daha az esneklik ve daha fazla iş yükü anlamına gelir.

**6. YAYGIN HATALAR:**
- **Hata:** `*args` ve `**kwargs`'ı aynı fonksiyonda yanlış sırada kullanmak.
  **Çözüm:** Doğru sıralama şudur: `normal_parametreler, *args, varsayilan_parametreler, **kwargs`.

### 5. `lambda` ile İsimsiz Fonksiyonlar

**1. TANIM:**
`lambda` ifadesi, küçük ve tek kullanımlık, isimsiz (anonim) fonksiyonlar oluşturmak için kullanılan bir anahtar kelimedir. Tek bir satırdan oluşur ve otomatik olarak sonucu döndürür.

**2. NEDEN VAR?**
Bazen bir fonksiyona çok basit bir işlem yaptırmak için onu `def` ile tanımlamak aşırı gelebilir. `lambda`, bu tür durumlar için kısa ve öz bir yol sunar. Özellikle `map`, `filter` gibi fonksiyonlarla birlikte kullanıldığında çok pratiktir.

**Günlük Hayat Analojisi:**
Bir arkadaşınızın evine gidip "Şu kumandayı uzatır mısın?" dersiniz. Bu basit bir istektir. Bunun için ayrı bir "Kumanda Uzatma Protokolü" yazmazsınız. `lambda` da bu kadar basit ve anlık işlemler içindir.

**3. NASIL KULLANILIR?**


```python
## 04_lambda_ornekleri.py

## Normal fonksiyon ile kare alma
def kareAlNormal(x):
    return x ** 2

## Lambda ifadesi ile kare alma
kareAlLambda = lambda x: x ** 2

print(f"Normal fonksiyon: {kareAlNormal(5)}")
print(f"Lambda ifadesi: {kareAlLambda(5)}")

## Çıktı:
## Normal fonksiyon: 25
## Lambda ifadesi: 25


## Lambda'nın asıl gücü: Başka bir fonksiyona argüman olarak vermek
## 'map' fonksiyonu: Bir listedeki her elemana bir fonksiyon uygular
sayilar = [1, 2, 3, 4, 5]
karelerListesi = list(map(lambda x: x ** 2, sayilar))
print(f"Sayıların kareleri: {karelerListesi}")

## 'filter' fonksiyonu: Bir listedeki elemanları bir koşula göre filtreler
ciftSayilar = list(filter(lambda x: x % 2 == 0, sayilar))
print(f"Çift sayılar: {ciftSayilar}")

## Çıktı:
## Sayıların kareleri: [1, 4, 9, 16, 25]
## Çift sayılar: [2, 4]
```


**Kod Açıklaması:**
- `lambda x: x ** 2` ifadesi, `x` parametresini alan ve `x ** 2` değerini döndüren bir fonksiyon oluşturur. `return` anahtar kelimesine gerek yoktur.
- `map(lambda x: x ** 2, sayilar)` ifadesi, `sayilar` listesindeki her bir `x` için `lambda` fonksiyonunu çalıştırır.
- `filter(lambda x: x % 2 == 0, sayilar)` ifadesi, `sayilar` listesindeki her bir `x` için `lambda` fonksiyonunu çalıştırır ve sadece sonucu `True` olanları (yani çift sayıları) alır.

**4. NE ZAMAN TERCİH EDİLİR?**
- Çok basit ve tek satırlık bir işlem için.
- Bir fonksiyonun başka bir fonksiyona argüman olarak verilmesi gerektiğinde (üst düzey fonksiyon - higher-order function).
- Kodun okunabilirliğini artırmak için (kısa ve öz olduğunda).

**5. ALTERNATİFLERİ:**
`lambda`'nın ana alternatifi `def` ile tanımlanan normal fonksiyonlardır. Eğer işlem birden fazla satır gerektiriyorsa veya birden fazla yerde kullanılacaksa `def` tercih edilmelidir.

| Özellik | `lambda` | `def` |
|:--- |:--- |:--- |
| **İsim** | İsimsiz (anonim) | İsimli |
| **Yapı** | Tek satır | Çok satırlı |
| **Dönüş** | Otomatik (return gerekmez) | Açıkça `return` yazılmalı |
| **Kullanım** | Basit, tek seferlik işlemler | Karmaşık, tekrar kullanılacak işlemler |

**6. YAYGIN HATALAR:**
- **Hata:** `lambda` içinde birden fazla ifade veya değişken ataması yapmaya çalışmak.


```python
  # Hatalı Kullanım
  hatali_lambda = lambda x: x += 1; print(x)  # SyntaxError
```


  **Çözüm:** `lambda` sadece tek bir ifade içerebilir. Karmaşık işlemler için `def` kullanın.

### 6. `map()` ve `filter()` Fonksiyonları

**1. TANIM:**
- `map(fonksiyon, iterable)`: Verilen bir fonksiyonu, verilen bir iterable'ın (liste, demet vb.) her bir elemanına uygular ve sonuçları bir iterator olarak döndürür.
- `filter(fonksiyon, iterable)`: Verilen bir fonksiyonun `True` döndürdüğü elemanları, verilen bir iterable'dan seçer ve bir iterator olarak döndürür.

**2. NEDEN VAR?**
Bu fonksiyonlar, döngüler yazmak zorunda kalmadan, bir veri kümesi üzerinde toplu işlemler yapmanızı sağlar. Bu, kodunuzu daha okunabilir, daha az hata içeren ve daha "Pythonik" yapar.

**3. NASIL KULLANILIR? (Yukarıdaki örnekle birlikte)**


```python
# 04_lambda_ornekleri.py (devamı)

# map ve filter'ı normal fonksiyonlarla da kullanabiliriz
def ciftMi(x):
    return x % 2 == 0

sayilar = [1, 2, 3, 4, 5, 6]

# filter ile çift sayıları bulma (normal fonksiyon)
ciftSayilarNormal = list(filter(ciftMi, sayilar))
print(f"Normal fonksiyonla çift sayılar: {ciftSayilarNormal}")

# filter ile çift sayıları bulma (lambda)
ciftSayilarLambda = list(filter(lambda x: x % 2 == 0, sayilar))
print(f"Lambda ile çift sayılar: {ciftSayilarLambda}")

# Çıktı:
# Normal fonksiyonla çift sayılar: [2, 4, 6]
# Lambda ile çift sayılar: [2, 4, 6]


# map ile sayıların küplerini alma
kupler = list(map(lambda x: x ** 3, sayilar))
print(f"Sayıların küpleri: {kupler}")

# Çıktı:
# Sayıların küpleri: [1, 8, 27, 64, 125, 216]
```


**Kod Açıklaması:**
- `filter()` fonksiyonu, `ciftMi` veya `lambda` fonksiyonunu `sayilar` listesindeki her eleman için çalıştırır. Sadece `True` dönen elemanları (2, 4, 6) yeni bir iterator'a koyar.
- `map()` fonksiyonu, `lambda` fonksiyonunu `sayilar` listesindeki her eleman için çalıştırır ve sonuçları (1, 8, 27…) yeni bir iterator'a koyar.
- `list()` fonksiyonu, iterator'ı bir listeye dönüştürmek için kullanılır.

**4. NE ZAMAN TERCİH EDİLİR?**
- Bir listenin tüm elemanlarını dönüştürmek (örneğin, tüm sayıların karesini almak) için `map()` idealdir.
- Bir listeden belirli bir koşulu sağlayan elemanları seçmek (örneğin, sadece çift sayıları almak) için `filter()` idealdir.

**5. ALTERNATİFLERİ:**
Bu fonksiyonların en klasik alternatifi `for` döngüleri ve `if` koşullarıdır. Ancak `map` ve `filter`, özellikle `lambda` ile birleştiğinde çok daha kısa ve ifade edici bir yol sunar.

**6. YAYG

IN HATALAR:

- **Hata:** `map` ve `filter`'ın sonucunu doğrudan yazdırmaya çalışmak.


```python
  # Hatalı Kullanım
  selamla()  # NameError: name 'selamla' is not defined

  def selamla():
      print("Merhaba")
```

0


0


  **Çözüm:** `map` ve `filter` iterator döndürür. Sonuçları görmek için `list()` ile listeye çevirin.

### 7. Scope (Değişken Kapsamı) Kuralları

**1. TANIM:**
Scope (kapsam), bir değişkenin programın hangi bölümlerinden erişilebilir olduğunu belirleyen kurallar bütünüdür. Python'da değişkenler tanımlandıkları yere göre farklı kapsamlara sahiptir.

**2. NEDEN VAR?**
Scope kuralları, farklı kod bloklarında aynı isimde değişkenler kullanabilmemizi sağlar. Bu, büyük projelerde isim çakışmalarını önler ve kodun düzenli kalmasını sağlar. Örneğin, bir fonksiyon içinde tanımlanan `toplam` değişkeni, başka bir fonksiyondaki `toplam` değişkenini etkilemez.

**3. NASIL KULLANILIR? (Günlük hayattan analoji: Bir apartmandaki daireler)**

Bir apartman düşünün. Her daire (fonksiyon) kendi içinde bağımsızdır. Dairedeki eşyalar (lokal değişkenler) sadece o dairede yaşayanlar tarafından kullanılabilir. Apartmanın girişindeki posta kutusu (global değişken) ise herkes tarafından görülebilir ve kullanılabilir.


```python
  # Hatalı Kullanım
  selamla()  # NameError: name 'selamla' is not defined

  def selamla():
      print("Merhaba")
```

1


1


**Kod Açıklaması:**
- `mesaj` değişkeni en üst seviyede tanımlandığı için "global" bir değişkendir.
- `fonksiyon1` içinde aynı isimde bir `mesaj` değişkeni tanımlanır. Bu, global değişkeni etkilemez; sadece fonksiyon içinde geçerli olan yeni bir "lokal" değişken oluşturur.
- `fonksiyon2`, kendi içinde `mesaj` tanımlamadığı için global `mesaj` değişkenine erişir.
- `fonksiyon3`, `global mesaj` ifadesiyle Python'a "Bu fonksiyonda `mesaj` isimli global değişkeni kullanacağım" der. Bu sayede global değişkenin değerini değiştirebilir.

**4. NE ZAMAN TERCİH EDİLİR?**
- **Global değişkenler:** Programın her yerinden erişilmesi gereken sabitler (örneğin, pi sayısı, uygulama adı) için kullanılır.
- **Lokal değişkenler:** Bir fonksiyonun kendi iç işleyişi için geçici olarak ihtiyaç duyduğu değerler için kullanılır. Mümkün olduğunca lokal değişken tercih edilmelidir.

**5. ALTERNATİFLERİ:**
Scope kavramının alternatifi yoktur, ancak global değişken kullanımının alternatifleri vardır. Global değişkenler, fonksiyonlara parametre olarak geçirilebilir veya bir sınıfın (ileride göreceğiz) özelliği olarak saklanabilir. Genel kural: global değişkenlerden mümkün olduğunca kaçının; çünkü programın akışını takip etmeyi zorlaştırırlar.

**6. YAYGIN HATALAR:**
- **Hata:** Bir fonksiyon içinde global bir değişkeni değiştirmeye çalışırken `global` anahtar kelimesini kullanmamak.


```python
  # Hatalı Kullanım
  selamla()  # NameError: name 'selamla' is not defined

  def selamla():
      print("Merhaba")
```

2


2


  **Çözüm:** Global değişkeni değiştirecekseniz `global sayac` ifadesini fonksiyonun başında kullanın.

### 8. Modül İçe Aktarma (import ve from)

**1. TANIM:**
Modül, Python kodlarını içeren bir dosyadır (.py uzantılı). `import` ifadesi, başka bir modüldeki (veya kütüphanedeki) kodları mevcut programınıza dahil etmenizi sağlar. `from… import…` ise bir modülden sadece belirli fonksiyonları veya sınıfları içe aktarmanıza olanak tanır.

**2. NEDEN VAR?**
Hiçbir programcı sıfırdan her şeyi yazmak zorunda değildir. Python'un zengin standart kütüphanesi (ve üçüncü taraf kütüphaneleri) sayesinde, karmaşık işlemleri (matematik, tarih, dosya işlemleri, web istekleri vb.) birkaç satır kodla gerçekleştirebiliriz. Modüller, kodun yeniden kullanılabilirliğini ve düzenini sağlar.

**3. NASIL KULLANILIR?**


```python
  # Hatalı Kullanım
  selamla()  # NameError: name 'selamla' is not defined

  def selamla():
      print("Merhaba")
```

3


3


**Kod Açıklaması:**
- `import math`: `math` modülündeki tüm fonksiyonlara `math.fonksiyonAdi()` şeklinde erişiriz.
- `from random import choice`: `random` modülünden sadece `choice` fonksiyonunu alırız. Doğrudan `choice()` olarak kullanabiliriz.
- `string.ascii_letters`: Tüm büyük ve küçük harfleri içeren bir string döndürür.
- `string.digits`: "0123456789" stringini döndürür.
- `choice(karakterler)`: Verilen string'den rastgele bir karakter seçer.

**4. NE ZAMAN TERCİH EDİLİR?**
- `import modul`: Bir modüldeki birçok farklı fonksiyonu kullanacaksanız tercih edilir. Kodun okunabilirliğini artırır (örneğin, `math.sqrt` ifadesi, `sqrt`'nin nereden geldiğini açıkça belirtir).
- `from modul import fonksiyon`: Bir modülden sadece bir veya iki fonksiyon kullanacaksanız tercih edilir. Daha kısa ve öz bir kullanım sağlar.

**5. ALTERNATİFLERİ:**
- `from modul import *`: Modüldeki tüm isimleri içe aktarır. **Kesinlikle önerilmez.** Hangi fonksiyonun nereden geldiğini takip etmeyi zorlaştırır ve isim çakışmalarına yol açabilir.
- Modülü takma adla içe aktarma: `import numpy as np` (yaygın bir kullanım). Uzun modül isimlerini kısaltmak için kullanılır.

**6. YAYGIN HATALAR:**
- **Hata:** `import` edilen modülün veya fonksiyonun ismini yanlış yazmak.


```python
  # Hatalı Kullanım
  selamla()  # NameError: name 'selamla' is not defined

  def selamla():
      print("Merhaba")
```

4


4


  **Çözüm:** Modül adını doğru yazdığınızdan emin olun. Python büyük/küçük harfe duyarlıdır.

### 9. Standart Kütüphane (math, random, datetime)

**1. TANIM:**
Python'un Standart Kütüphanesi, Python ile birlikte gelen, sık kullanılan görevler için hazır fonksiyonlar ve modüller koleksiyonudur. `math`, `random` ve `datetime` bu kütüphanenin en popüler modüllerinden sadece birkaçıdır.

**2. NEDEN VAR?**
Tekerleği yeniden icat etmemek için. Standart kütüphane, geliştiricilere güvenilir, test edilmiş ve optimize edilmiş araçlar sunar. Bu, geliştirme süresini kısaltır ve hata olasılığını azaltır.

**3. NASIL KULLANILIR? (Tarih ve zaman işlemleri)**


```python
  # Hatalı Kullanım
  selamla()  # NameError: name 'selamla' is not defined

  def selamla():
      print("Merhaba")
```

5


5


**Kod Açıklaması:**
- `datetime.now()`: Bilgisayarınızın sistem saatinden anlık tarih ve saati alır.
- `strftime()`: Bir `datetime` nesnesini istenilen formatta bir string'e dönüştürür. `%d` gün, `%m` ay, `%Y` yıl, `%H` saat, `%M` dakika, `%S` saniye anlamına gelir.
- `timedelta`: İki tarih arasındaki farkı temsil eder. Gün, saat, dakika, saniye cinsinden bir süre belirtmek için kullanılır.
- `fark.days`: İki tarih arasındaki toplam gün farkını verir.

**4. NE ZAMAN TERCİH EDİLİR?**
- **`math` modülü:** Karmaşık matematiksel işlemler (trigonometri, logaritma, sabitler) gerektiğinde.
- **`random` modülü:** Rastgele sayı üretimi, bir listeden rastgele eleman seçimi, bir diziyi karıştırma gerektiğinde.
- **`datetime` modülü:** Tarih ve saat ile ilgili her türlü işlem (hesaplama, karşılaştırma, formatlama) gerektiğinde.

**5. ALTERNATİFLERİ:**
Bu modüllerin alternatifleri yoktur; standart kütüphanenin bir parçasıdırlar. Ancak daha spesifik ihtiyaçlar için (örneğin, daha karmaşık tarih işlemleri için `dateutil` veya bilimsel hesaplamalar için `numpy`) üçüncü taraf kütüphaneler kullanılabilir.

**6. YAYGIN HATALAR:**
- **Hata:** `datetime` modülü ile tarih hesaplarken yanlış birim kullanmak.


```python
  # Hatalı Kullanım
  selamla()  # NameError: name 'selamla' is not defined

  def selamla():
      print("Merhaba")
```

6


6


  **Çözüm:** Tarih hesaplamalarında `timedelta` nesnesini kullanın. `simdi + timedelta(days=7)`.


## Diyagramlar

### 1. Fonksiyon Çalışma Akışı

Aşağıdaki Mermaid diyagramı, bir fonksiyonun çağrılmasından sonuç döndürmesine kadar geçen süreci görselleştirmektedir. Bu akış, programlama dillerinin temel mantığını anlamak için kritik öneme sahiptir.


```python
  # Hatalı Kullanım
  selamla()  # NameError: name 'selamla' is not defined

  def selamla():
      print("Merhaba")
```

7


7


**Açıklama:** Bu diyagram, bir fonksiyonun nasıl çalıştığını adım adım gösterir. En önemli karar noktası (elmas), fonksiyonun bir `return` ifadesi içerip içermediğidir. Eğer `return` varsa, fonksiyon belirtilen değeri döndürür; yoksa varsayılan olarak `None` döndürür.

### 2. Scope Katmanları (LEGB Kuralı)

Aşağıdaki sequence diyagramı, Python'da bir değişkene erişmeye çalıştığınızda hangi kapsamların hangi sırayla tarandığını (LEGB Kuralı) göstermektedir.


```python
  # Hatalı Kullanım
  selamla()  # NameError: name 'selamla' is not defined

  def selamla():
      print("Merhaba")
```

8


8


**Açıklama:** Bu diyagram, Python'un bir değişkenin değerini ararken izlediği hiyerarşik yapıyı (LEGB) açıklar. Önce fonksiyonun kendi içine (Local), sonra onu kapsayan fonksiyona (Enclosing), ardından programın ana gövdesine (Global) ve en son Python'un yerleşik fonksiyonlarına (Built-in) bakar. Hiçbir yerde bulamazsa `NameError` hatası verir.

### 3. Modül Yükleme Süreci

Aşağıdaki flowchart, Python'da bir modülü `import` ettiğinizde arka planda neler olduğunu göstermektedir.


```python
  # Hatalı Kullanım
  selamla()  # NameError: name 'selamla' is not defined

  def selamla():
      print("Merhaba")
```

9


9


**Açıklama:** `import math` yazdığınızda Python, `sys.path` listesinde tanımlı olan dizinlerde `math.py` dosyasını arar. Bulduğunda, dosyayı daha hızlı çalıştırmak için önce bytecode'a (`__pycache__` klasöründe `.pyc` dosyasına) çevirir, ardından çalıştırarak modülün isim alanını oluşturur. Eğer modül bulunamazsa `ModuleNotFoundError` hatası alırsınız.


## Entegrasyon Örneği: Basit Şifre Yöneticisi

Artık öğrendiğimiz tüm kavramları birleştirerek, basit ama işlevsel bir şifre yöneticisi programı yazalım. Bu program, kullanıcının girdiği bir ana şifre ile korunan, rastgele şifreler üreten ve bunları bir sözlükte saklayan bir uygulama olacak.


```python
## 01_ilk_fonksiyon.py (devamı)

## Parametre alan bir fonksiyon: 'kisiyeSelamVer' adında, 'isim' parametreli
def kisiyeSelamVer(isim):
    """
    Verilen ismi kullanarak kişiselleştirilmiş bir selamlama yazar.
    """
    print(f"Merhaba {isim}! Nasılsın?")

## Fonksiyonu farklı argümanlarla çağırıyoruz
kisiyeSelamVer("Ali")     # Argüman: "Ali"
kisiyeSelamVer("Ayşe")    # Argüman: "Ayşe"
kisiyeSelamVer("Mehmet")  # Argüman: "Mehmet"

## Çıktı:
## Merhaba Ali! Nasılsın?
## Merhaba Ayşe! Nasılsın?
## Merhaba Mehmet! Nasılsın?

## Varsayılan parametre kullanımı
def kisiyeSelamVerVarsayilan(isim, selam="Merhaba"):
    """
    Varsayılan bir selamlama ile fonksiyon.
    """
    print(f"{selam} {isim}!")

kisiyeSelamVerVarsayilan("Zeynep")          # Varsayılan selam kullanılır
kisiyeSelamVerVarsayilan("Ahmet", "Günaydın")  # Selam argümanı verilir

## Çıktı:
## Merhaba Zeynep!
## Günaydın Ahmet!
```

0


0


**Kod Açıklaması:**
Bu entegrasyon örneği, bölüm boyunca öğrendiğimiz tüm kavramları bir araya getirir:
- **Fonksiyon tanımlama:** `sifre_uret()`, `sifre_ekle()`, `sifre_goster()`, `ana_menu()` fonksiyonları.
- **Parametreler ve varsayılan değerler:** `sifre_uret(uzunluk=8,…)`.
- **`return`:** `sifre_uret()` fonksiyonu oluşturduğu şifreyi döndürür.
- **`lambda`, `map`, `filter`:** Bu örnekte kullanılmamış olsa da, şifrelerin listelenmesi gibi işlemlerde kullanılabilir.
- **Scope:** `sifreler` ve `ana_sifre` global değişkenlerdir ve tüm fonksiyonlar tarafından erişilebilir.
- **Modüller:** `string`, `random.choice`, `datetime` modülleri kullanılmıştır.
- **Standart kütüphane:** Tarih formatlama, rastgele karakter seçimi gibi işlemler için kullanılmıştır.


## Bölüm Özeti

Bu bölümde, Python programlamanın temel yapı taşlarından olan fonksiyonlar ve modüller konusunu derinlemesine inceledik. İşte öğrendiklerimizin kısa bir özeti:

1. **Fonksiyon Tanımlama (`def`):** Kod bloklarını adlandırarak tekrar kullanılabilir hale getirdik. Fonksiyonlar, kodumuzu daha düzenli, okunabilir ve yönetilebilir kılar.

2. **Parametreler ve Argümanlar:** Fonksiyonlara girdi vermeyi öğrendik. Varsayılan parametreler sayesinde esnek fonksiyonlar yazabildik.

3. **`return` İfadesi:** Fonksiyonların ürettiği sonuçları dışarıya göndermeyi öğrendik. `return` olmadan fonksiyonların `None` döndürdüğünü gördük.

4. **`*args` ve `**kwargs`:** Belirsiz sayıda parametre alabilen esnek fonksiyonlar yazmayı öğrendik. Bu, özellikle veri miktarının önceden bilinmediği durumlarda çok kullanışlıdır.

5. **Lambda İfadeleri:** Tek satırlık, isimsiz fonksiyonlar oluşturmayı öğrendik. Özellikle `map()` ve `filter()` gibi fonksiyonlarla birlikte kullanıldığında çok güçlüdür.

6. **`map()` ve `filter()`:** Bir fonksiyonu bir diziye uygulama ve filtreleme araçlarını öğrendik. Bu fonksiyonlar, döngüler yazmak zorunda kalmadan veri kümeleri üzerinde toplu işlemler yapmamızı sağlar.

7. **Scope Kuralları:** Değişkenlerin hangi bölgelerde erişilebilir olduğunu belirleyen LEGB kuralını öğrendik. Global ve lokal değişkenler arasındaki farkı ve `global` anahtar kelimesinin kullanımını gördük.

8. **Modül İçe Aktarma (`import` ve `from`):** Başka dosyalardaki veya kütüphanelerdeki kodları kullanmayı öğrendik. `import math` ve `from random import choice` arasındaki farkı anladık.

9. **Standart Kütüphane:** Python ile birlikte gelen hazır araçları (`math`, `random`, `datetime`) kullanmayı öğrendik. Bu modüller sayesinde karmaşık işlemleri birkaç satır kodla gerçekleştirebildik.


## Sözlük

| Terim | Açıklama |
|:--- |:--- |
| **Fonksiyon** | Belirli bir görevi yerine getiren, adlandırılmış kod bloğu. |
| **Parametre** | Fonksiyon tanımlanırken parantez içinde belirtilen, fonksiyonun alacağı girdi değişkeni. |
| **Argüman** | Fonksiyon çağrılırken parametrelere gönderilen gerçek değer. |
| **Return Değeri** | Fonksiyonun işlem sonucunda döndürdüğü değer. |
| **Varsayılan Parametre** | Fonksiyon tanımlanırken bir parametreye atanan, çağrı sırasında değer verilmezse kullanılacak ön tanımlı değer. |
| **`*args`** | Fonksiyona değişken sayıda konumsal argüman göndermeyi sağlayan özel parametre. Argümanları bir demet (tuple) olarak alır. |
| **`**kwargs`** | Fonksiyona değişken sayıda anahtar-değer (keyword) argümanı göndermeyi sağlayan ö

zel parametre. Argümanları bir sözlük (dict) olarak alır. |
| **Lambda İfadesi** | Tek satırlık, isimsiz fonksiyon oluşturma yöntemi. |
| **Global Değişken** | Fonksiyon dışında, tüm programın erişebileceği şekilde tanımlanan değişken. |
| **Lokal Değişken** | Bir fonksiyon içinde tanımlanan ve sadece o fonksiyon içinde erişilebilen değişken. |
| **Scope (Kapsam)** | Bir değişkenin program içinde erişilebilir olduğu bölge. |
| **Modül** | İçinde Python kodları (fonksiyonlar, sınıflar, değişkenler) bulunan `.py` uzantılı dosya. |
| **Kütüphane (Paket)** | Birbiriyle ilişkili modüllerin bir araya getirildiği koleksiyon. |
| **İsim Alanı (Namespace)** | Değişken, fonksiyon gibi isimlerin tanımlandığı ve birbirinden ayırt edildiği ortam. |
| **LEGB Kuralı** | Python'un bir değişkenin değerini ararken sırasıyla Local, Enclosing, Global, Built-in kapsamlarına bakması kuralı. |


## Değerlendirme Soruları

### Doğru / Yanlış Soruları

Aşağıdaki ifadelerin doğru (D) ya da yanlış (Y) olduğunu belirtin.

1. **D/Y:** `return` ifadesi olmayan bir fonksiyon, `None` değerini döndürür. (**Cevap: D**)
2. **D/Y:** `*args` parametresi, fonksiyona gönderilen tüm konumsal argümanları bir sözlük (dict) olarak toplar. (**Cevap: Y** - Demet (tuple) olarak toplar.)
3. **D/Y:** Lambda fonksiyonları, tek bir ifadeden oluşmalıdır ve birden çok satır içeremez. (**Cevap: D**)
4. **D/Y:** Bir fonksiyonun içinde, `global` anahtar kelimesini kullanmadan global bir değişkenin değerini değiştirebiliriz. (**Cevap: Y** - Değiştiremeyiz, sadece okuyabiliriz.)
5. **D/Y:** `map()` fonksiyonu, uygulandığı orijinal listeyi kalıcı olarak değiştirir. (**Cevap: Y** - Orijinal listeyi değiştirmez, yeni bir `map` nesnesi (iterator) döndürür.)
6. **D/Y:** `import math` ile `from math import sqrt` ifadeleri, `sqrt` fonksiyonuna erişim açısından aynı sonucu verir. (**Cevap: Y** - İlkinde `math.sqrt(4)`, ikincisinde `sqrt(4)` şeklinde kullanılır, farklıdır.)
7. **D/Y:** Bir fonksiyon tanımlanırken, varsayılan değere sahip parametreler, varsayılan değeri olmayan parametrelerden önce gelmelidir. (**Cevap: Y** - Tam tersi, varsayılan parametreler sonda olmalıdır.)
8. **D/Y:** `filter()` fonksiyonu, kendisine verilen koşul fonksiyonunun `True` döndürdüğü elemanları seçer. (**Cevap: D**)

### Boşluk Doldurma Soruları

Aşağıdaki cümlelerdeki boşlukları uygun terimlerle doldurun.

1. Bir fonksiyon tanımlamak için kullanılan anahtar kelime **\_\_\_\_\_\_**'dir. (**Cevap: def**)
2. Fonksiyona değişken sayıda konumsal argüman göndermek için **\_\_\_\_\_\_** parametresi kullanılır. (**Cevap: *args**)
3. Tek satırlık, isimsiz bir fonksiyon oluşturmak için **\_\_\_\_\_\_** ifadesi kullanılır. (**Cevap: lambda**)
4. Bir fonksiyon içinde global bir değişkenin değerini değiştirmek için **\_\_\_\_\_\_** anahtar kelimesi kullanılmalıdır. (**Cevap: global**)
5. Python'da başka bir dosyadaki kodu kullanmak için **\_\_\_\_\_\_** ifadesi kullanılır. (**Cevap: import**)
6. `random` modülünde, 0.0 ile 1.0 arasında rastgele bir ondalıklı sayı üreten fonksiyon **\_\_\_\_\_\_**'dir. (**Cevap: random()**)
7. `datetime` modülünde, bulunduğumuz anın tarih ve saatini almak için kullanılan fonksiyon **\_\_\_\_\_\_**'dir. (**Cevap: datetime.now()**)
8. Pi sayısı (`π`), `math` modülünde **\_\_\_\_\_\_** sabiti olarak tanımlanmıştır. (**Cevap: math.pi**)

### Kısa Cevaplı Sorular

1. **Soru:** `selamla()` adında, kendisine verilen bir ismi parametre olarak alıp "Merhaba, [isim]!" yazdıran bir fonksiyon yazın. Eğer isim verilmezse "Merhaba, Misafir!" yazdırsın.
  **Cevap:**


```python
## 01_ilk_fonksiyon.py (devamı)

## Parametre alan bir fonksiyon: 'kisiyeSelamVer' adında, 'isim' parametreli
def kisiyeSelamVer(isim):
    """
    Verilen ismi kullanarak kişiselleştirilmiş bir selamlama yazar.
    """
    print(f"Merhaba {isim}! Nasılsın?")

## Fonksiyonu farklı argümanlarla çağırıyoruz
kisiyeSelamVer("Ali")     # Argüman: "Ali"
kisiyeSelamVer("Ayşe")    # Argüman: "Ayşe"
kisiyeSelamVer("Mehmet")  # Argüman: "Mehmet"

## Çıktı:
## Merhaba Ali! Nasılsın?
## Merhaba Ayşe! Nasılsın?
## Merhaba Mehmet! Nasılsın?

## Varsayılan parametre kullanımı
def kisiyeSelamVerVarsayilan(isim, selam="Merhaba"):
    """
    Varsayılan bir selamlama ile fonksiyon.
    """
    print(f"{selam} {isim}!")

kisiyeSelamVerVarsayilan("Zeynep")          # Varsayılan selam kullanılır
kisiyeSelamVerVarsayilan("Ahmet", "Günaydın")  # Selam argümanı verilir

## Çıktı:
## Merhaba Zeynep!
## Günaydın Ahmet!
```

1


1


2. **Soru:** `*args` kullanarak, kendisine gönderilen tüm sayıların çarpımını hesaplayıp döndüren `carpim_hesapla` adında bir fonksiyon yazın.
  **Cevap:**


```python
## 01_ilk_fonksiyon.py (devamı)

## Parametre alan bir fonksiyon: 'kisiyeSelamVer' adında, 'isim' parametreli
def kisiyeSelamVer(isim):
    """
    Verilen ismi kullanarak kişiselleştirilmiş bir selamlama yazar.
    """
    print(f"Merhaba {isim}! Nasılsın?")

## Fonksiyonu farklı argümanlarla çağırıyoruz
kisiyeSelamVer("Ali")     # Argüman: "Ali"
kisiyeSelamVer("Ayşe")    # Argüman: "Ayşe"
kisiyeSelamVer("Mehmet")  # Argüman: "Mehmet"

## Çıktı:
## Merhaba Ali! Nasılsın?
## Merhaba Ayşe! Nasılsın?
## Merhaba Mehmet! Nasılsın?

## Varsayılan parametre kullanımı
def kisiyeSelamVerVarsayilan(isim, selam="Merhaba"):
    """
    Varsayılan bir selamlama ile fonksiyon.
    """
    print(f"{selam} {isim}!")

kisiyeSelamVerVarsayilan("Zeynep")          # Varsayılan selam kullanılır
kisiyeSelamVerVarsayilan("Ahmet", "Günaydın")  # Selam argümanı verilir

## Çıktı:
## Merhaba Zeynep!
## Günaydın Ahmet!
```

2


2


3. **Soru:** `map()` fonksiyonunu kullanarak, `[1, 2, 3, 4, 5]` listesindeki her sayının küpünü alıp yeni bir liste oluşturan bir kod parçası yazın (lambda kullanarak).
  **Cevap:**


```python
## 01_ilk_fonksiyon.py (devamı)

## Parametre alan bir fonksiyon: 'kisiyeSelamVer' adında, 'isim' parametreli
def kisiyeSelamVer(isim):
    """
    Verilen ismi kullanarak kişiselleştirilmiş bir selamlama yazar.
    """
    print(f"Merhaba {isim}! Nasılsın?")

## Fonksiyonu farklı argümanlarla çağırıyoruz
kisiyeSelamVer("Ali")     # Argüman: "Ali"
kisiyeSelamVer("Ayşe")    # Argüman: "Ayşe"
kisiyeSelamVer("Mehmet")  # Argüman: "Mehmet"

## Çıktı:
## Merhaba Ali! Nasılsın?
## Merhaba Ayşe! Nasılsın?
## Merhaba Mehmet! Nasılsın?

## Varsayılan parametre kullanımı
def kisiyeSelamVerVarsayilan(isim, selam="Merhaba"):
    """
    Varsayılan bir selamlama ile fonksiyon.
    """
    print(f"{selam} {isim}!")

kisiyeSelamVerVarsayilan("Zeynep")          # Varsayılan selam kullanılır
kisiyeSelamVerVarsayilan("Ahmet", "Günaydın")  # Selam argümanı verilir

## Çıktı:
## Merhaba Zeynep!
## Günaydın Ahmet!
```

3


3


## Alıştırmalar

1. **Temel Fonksiyon:** Kullanıcıdan alınan bir dikdörtgenin kısa ve uzun kenarını parametre olarak alıp, dikdörtgenin alanını ve çevresini hesaplayarak ekrana yazdıran bir fonksiyon yazın.

2. **Varsayılan Parametre:** `daire_hesapla(yaricap, pi=3.14)` şeklinde bir fonksiyon yazın. Bu fonksiyon, dairenin çevresini ve alanını hesaplayarak bir sözlük olarak döndürsün (`{"cevre":…, "alan":…}`).

3. **`*args` Kullanımı:** `ortalama_hesapla()` adında bir fonksiyon yazın. Bu fonksiyon, kendisine gönderilen tüm sayısal argümanların ortalamasını hesaplasın. Eğer hiç argüman gönderilmezse, `0` değerini döndürsün.

4. **Lambda ve `filter()`:** `filter()` fonksiyonu ve bir lambda ifadesi kullanarak, `[-5, 12, 0, -3, 8, -1, 7]` listesinden sadece pozitif sayıları seçip yeni bir liste oluşturun.

5. **Modüller:** `datetime` modülünü kullanarak, kullanıcıdan doğum yılını alan ve o kişinin bu yılki yaşını hesaplayan bir program yazın. (İpucu: `datetime.now().year` ile geçerli yılı alabilirsiniz.)

6. **Kapsamlı Uygulama:** "Kişisel Not Defteri" adında basit bir konsol uygulaması yazın. Bu uygulama aşağıdaki özellikleri içermelidir:
  * `not_ekle(baslik, icerik)`: Yeni bir not ekler. Notları bir sözlük listesinde saklayın.
  * `notlari_listele()`: Tüm notların başlıklarını ve eklenme tarihini (datetime kullanarak) listeler.
  * `not_sil(baslik)`: Başlığı verilen notu siler.
  * `not_ara(anahtar_kelime)`: Başlık veya içerikte anahtar kelimeyi arar ve eşleşen notları listeler.
  * Menü: Kullanıcının yukarıdaki işlemleri seçebileceği bir döngü oluşturun.


## Sık Yapılan Hatalar ve Çözümleri

| Hata | Açıklama | Çözüm |
|:--- |:--- |:--- |
| **`return` unutmak** | Fonksiyon bir hesaplama yapar ancak sonucu `return` ile döndürmez. Fonksiyon çağrıldığında `None` alınır. | Fonksiyonun amacı bir değer üretmekse, mutlaka `return` ifadesi ile bu değeri döndürün. |
| **Global değişkeni değiştirmek** | Bir fonksiyon içinde global bir değişkene değer atamaya çalışmak (örneğin `sayac = 5`). Bu, aslında aynı isimde yeni bir lokal değişken oluşturur. | Global değişkeni değiştirmek istiyorsanız, fonksiyon içinde `global sayac` ifadesini kullanın. Ancak bu yöntemi mümkün olduğunca az kullanın; bunun yerine değeri `return` ile döndürün. |
| **Varsayılan parametre sırası** | Varsayılan değeri olan bir parametreyi, varsayılan değeri olmayan bir parametrenin önüne koymak. | Varsayılan parametreler her zaman parametre listesinin sonunda yer almalıdır. |
| **`*args` ve `**kwargs` karıştırmak** | `*args`'ın bir sözlük, `**kwargs`'ın bir demet olarak düşünülmesi. | `*args` konumsal argümanları bir **demet (tuple)**, `**kwargs` ise anahtar-değer argümanlarını bir **sözlük (dict)** olarak alır. |
| **`map()` ve `filter()` sonuçlarını yanlış kullanmak** | Bu fonksiyonların doğrudan bir liste döndürmediğini unutmak. `print(map(…))` yazmak yerine `print(list(map(…)))` yazmak gerekir. | `map()` ve `filter()` bir `map` veya `filter` nesnesi (iterator) döndürür. Sonuçları bir liste olarak görmek veya kullanmak istiyorsanız `list()` fonksiyonu ile sarmanız gerekir. |


## Kaynaklar ve İleri Okuma

* **Python Resmi Dokümantasyonu - Fonksiyonlar:** [https://docs.python.org/3/tutorial/controlflow.html#defining-functions](https://docs.python.org/3/tutorial/controlflow.html#defining-functions)
* **Python Resmi Dokümantasyonu - Modüller:** [https://docs.python.org/3/tutorial/modules.html](https://docs.python.org/3/tutorial/modules.html)
* **Python Resmi Dokümantasyonu - Standart Kütüphane:** [https://docs.python.org/3/library/](https://docs.python.org/3/library/)
* **Real Python - Fonksiyonlar:** [https://realpython.com/defining-your-own-python-function/](https://realpython.com/defining-your-own-python-function/)
* **Real Python - Python Scope & the LEGB Rule:** [https://realpython.com/python-scope-legb-rule/](https://realpython.com/python-scope-legb-rule/)

Bu bölümde öğrendiğiniz fonksiyonlar ve modüller, Python'da daha büyük ve karmaşık projeler geliştirmenin temelini oluşturur. Bir sonraki bölümde, bu bilgileri kullanarak daha ileri seviye konulara geçeceğiz.

## Bir sonraki bolume kopru

Bu bölümde öğrendiğiniz fonksiyon ve modül yapıları, kodunuzu yeniden kullanılabilir ve düzenli hale getirmenin temel taşlarıdır. Bir sonraki bölümde, bu yapı taşlarını kullanarak daha büyük projeleri nasıl yöneteceğinizi, dosyalarla nasıl çalışacağınızı ve hataları profesyonelce nasıl ele alacağınızı keşfedeceksiniz. Artık küçük kod parçalarını birleştirip anlamlı uygulamalar inşa etmeye hazırsınız.
