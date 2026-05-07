# Bölüm 4: Fonksiyonlar ve Modüller — PLAN

---

## 1. KAVRAMLAR

| Sıra | Kavram | Ne olduğu (1 cümle) | Zorluk (★) | Kod örneği? | Gösterilecek konu |
|------|--------|---------------------|------------|-------------|-------------------|
| 1 | Fonksiyon tanımlama (def) | İsimlendirilmiş, tekrar kullanılabilir kod bloğu oluşturma yapısı | ★★ | Evet | Bir fonksiyonun nasıl tanımlandığı, çağrıldığı ve yeniden kullanıldığı |
| 2 | Parametreler ve argümanlar | Fonksiyona girdi sağlama mekanizması (tanımda parametre, çağrıda argüman) | ★★ | Evet | Zorunlu, varsayılan, anahtar kelimeli argümanlar arasındaki fark |
| 3 | return ifadesi | Fonksiyonun ürettiği değeri çağrıldığı yere geri gönderme | ★★ | Evet | return olmadan fonksiyon None döndürür; erken çıkış için return kullanımı |
| 4 | *args ve **kwargs | Değişken sayıda pozisyonel/anahtar kelimeli argüman alma | ★★★★ | Evet | Esnek fonksiyon imzaları oluşturma, paketleme ve açma |
| 5 | Lambda fonksiyonları | Tek ifadeli, isimsiz, satır içi fonksiyon tanımlama | ★★★ | Evet | Kısa süreli işlemler için lambda'nın def'e alternatif olması |
| 6 | map() ve filter() | Bir fonksiyonu bir diziye uygulama (map) veya filtreleme (filter) | ★★★ | Evet | Liste dönüşümlerinde döngü yerine fonksiyonel yaklaşım |
| 7 | Scope kuralları (LEGB) | Değişkenlerin hangi alanlarda görünür olduğunu belirleyen hiyerarşi | ★★★★ | Evet | Local, Enclosing, Global, Built-in ayrımı ve global/nonlocal anahtar kelimeleri |
| 8 | import ve from | Başka modüllerdeki kodları mevcut alana getirme | ★ | Evet | import modül vs from modül import isim farkı |
| 9 | Standart kütüphane (math, random, datetime) | Python ile gelen hazır fonksiyon koleksiyonları | ★ | Evet | math: trigonometri, random: rastgele sayı, datetime: tarih/saat işlemleri |

---

## 2. KOD ÖRNEKLERİ

| Örnek # | Hangi kavram? | Dosya adı | Tahmini satır | Kullanılacak Java özellikleri |
|---------|---------------|-----------|---------------|------------------------------|
| 1 | def, parametre, return | FonksiyonTemelleri.py | 20-25 | Fonksiyon tanımı, parametre geçirme, return, None dönüşü |
| 2 | Varsayılan/anahtar kelimeli argüman | SiparisHesaplama.py | 25-30 | Varsayılan parametre, anahtar kelimeli çağrı, karışık sıralama |
| 3 | *args ve **kwargs | EsnekFonksiyon.py | 30-35 | Yıldız operatörü, tuple/dict paketleme, açma işlemleri |
| 4 | Lambda, map, filter | LambdaDonusum.py | 20-25 | Lambda ifadesi, map() liste dönüşümü, filter() koşullu seçim |
| 5 | Scope kuralları | DegiskenKapsami.py | 25-30 | İç içe fonksiyon, LEGB sırası, global/nonlocal anahtar kelimeleri |
| 6 | import, standart kütüphane | KutuphaneKullanimi.py | 20-25 | import math, from random import, datetime nesneleri |
| 7 | Tüm kavramlar (bütünleşik) | HesapMakinesiModulu.py | 40-50 | Modüler yapı, lambda callback, *args toplama, math kullanımı |

---

## 3. DİYAGRAMLAR

### Diyagram 1: Fonksiyon Çağrı Akışı
- **Tür:** Sequence diagram
- **Neyi görselleştirir?** Bir fonksiyon çağrıldığında parametrelerin nasıl aktarıldığı, işlemin yapılması ve return ile değerin geri dönmesi
- **Düğümler:** Ana program, fonksiyon tanımı, parametre kutusu, işlem bloğu, return değeri

### Diyagram 2: Scope Hiyerarşisi (LEGB)
- **Tür:** Flowchart (karar elmaslı)
- **Neyi görselleştirir?** Bir değişkene erişildiğinde Python'un hangi sırayla Local → Enclosing → Global → Built-in alanlarını taradığı
- **Düğümler:** Değişken kullanımı, Local bulundu mu?, Enclosing bulundu mu?, Global bulundu mu?, Built-in kontrol, NameError

### Diyagram 3: Modül İçe Aktarma Yolları
- **Tür:** Flowchart
- **Neyi görselleştirir?** import modül vs from modül import isim arasındaki fark, isim çakışması riski
- **Düğümler:** import math, math.sqrt(), from math import sqrt, sqrt() doğrudan, isim çakışması kontrolü, alias kullanımı

---

## 4. SÖZLÜK (10-15 terim)

1. Fonksiyon
2. Parametre
3. Argüman
4. return
5. *args
6. **kwargs
7. Lambda ifadesi
8. map()
9. filter()
10. Scope (kapsam)
11. LEGB
12. global anahtar kelimesi
13. nonlocal anahtar kelimesi
14. Modül
15. import ifadesi
16. Alias (takma ad)
17. Standart kütüphane

---

## 5. DEĞERLENDİRME

### Doğru/Yanlış Soruları (5-10 konu)

1. Bir fonksiyon return ifadesi içermiyorsa otomatik olarak None döndürür. (D/Y)
2. *args parametresi anahtar kelimeli argümanları toplar. (D/Y)
3. Lambda fonksiyonları birden fazla ifade içerebilir. (D/Y)
4. map() fonksiyonu bir döngü yerine geçer ve her elemana işlem uygular. (D/Y)
5. İç içe fonksiyonlarda içteki fonksiyon dıştaki değişkenlere doğrudan erişemez. (D/Y)
6. global anahtar kelimesi olmadan fonksiyon içinde global değişken değiştirilebilir. (D/Y)
7. from math import * tüm math fonksiyonlarını doğrudan kullanıma sunar. (D/Y)
8. filter() fonksiyonu True döndüren elemanları seçer. (D/Y)

### Boşluk Doldurma Soruları (5-10 konu)

1. Fonksiyon tanımlamak için ______ anahtar kelimesi kullanılır.
2. Değişken sayıda pozisyonel argüman almak için parametre adının başına ______ konur.
3. Lambda fonksiyonunun gövdesi tek bir ______ içerebilir.
4. Bir fonksiyonun ürettiği değeri geri göndermek için ______ kullanılır.
5. Python'da değişken kapsamı sırası Local, Enclosing, ______, Built-in şeklindedir.
6. İç içe fonksiyonda dıştaki değişkeni değiştirmek için ______ anahtar kelimesi kullanılır.
7. Bir modülü kısaltılmış isimle içe aktarmak için ______ anahtar kelimesi kullanılır.
8. random modülünden sadece randint fonksiyonunu almak için ______ yazılır.

---

## 6. ALIŞTIRMALAR

| # | Konu | Zorluk | Tarif |
|---|------|--------|-------|
| 1 | Sipariş hesaplama fonksiyonu | ★★ | Kullanıcıdan ürün fiyatı ve adedi alan, KDV ve indirim hesaplaması yapan, varsayılan parametrelerle esnek bir fonksiyon yazılacak |
| 2 | Öğrenci not analizi (lambda+map+filter) | ★★★ | Öğrenci not listesini lambda ile harf notuna çeviren, filter ile geçen/kalan ayıran, map ile ortalama hesaplayan fonksiyonel bir çözüm |
| 3 | Basit bir modül paketi | ★★★★ | math, random, datetime kullanarak bir "Zaman ve İstatistik" modülü oluşturma; içinde rastgele sayı üretme, istatistik hesaplama, tarih farkı bulma fonksiyonları |

---

## 7. SIK YAPILAN HATALAR (3-5 başlık)

1. **return unutmak:** Fonksiyon içinde print() kullanıp return yazılmazsa fonksiyon None döndürür; öğrenci değerin geldiğini sanar.
2. ***args ile **kwargs karıştırmak:** *args pozisyonel argümanları tuple olarak alırken, **kwargs anahtar kelimelileri dict olarak alır; öğrenciler sıklıkla ikisini ters kullanır.
3. **global eksikliği:** Fonksiyon içinde global değişkeni değiştirmeye çalışmak ama global anahtar kelimesini unutmak; Python yeni bir local değişken oluşturur.
4. **Lambda aşırı kullanımı:** Karmaşık işlemleri lambda ile yapmaya çalışmak; okunabilirlik kaybı ve hata ayıklama zorluğu.
5. **import çakışması:** from math import sqrt yapıp aynı isimde başka bir sqrt değişkeni tanımlamak; son tanımlanan öncekini ezer.

---

## 8. TABLOLAR

### Tablo 1: Parametre Türleri Karşılaştırması
- **Sütunlar:** Parametre türü | Sözdizimi | Zorunlu mu? | Varsayılan değer | Sıralama kuralı
- **Satırlar:** Zorunlu parametre, Varsayılan parametre, *args, **kwargs, Anahtar kelimeli parametre

### Tablo 2: İçe Aktarma Yöntemleri
- **Sütunlar:** Yöntem | Sözdizimi | Kullanım | İsim çakışması riski | Performans
- **Satırlar:** import modül, from modül import isim, from modül import *, import modül as alias

### Tablo 3: Scope Türleri
- **Sütunlar:** Scope adı | Kapsam alanı | Değişken ömrü | Değiştirme yöntemi
- **Satırlar:** Local, Enclosing, Global, Built-in

---

**Not:** Bu plan yalnızca ne yapılacağını tarif eder. Kodlar, diyagramlar ve açıklamalar bir sonraki aşamada yazılacaktır.