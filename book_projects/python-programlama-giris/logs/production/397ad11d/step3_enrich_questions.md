# Bölüm 4: Fonksiyonlar ve Modüller - Kendini Değerlendirme Soruları

## Doğru/Yanlış Soruları

**Soru 1:** Python'da bir fonksiyon tanımlarken `def` anahtar kelimesi kullanılır.
- Cevap: Doğru
- Açıklama: Python'da fonksiyon tanımlamak için `def` anahtar kelimesi zorunludur.

**Soru 2:** `*args` parametresi, fonksiyona sadece bir tane argüman geçilmesini sağlar.
- Cevap: Yanlış
- Açıklama: `*args` bir demet (tuple) olarak birden fazla konumsal argüman almayı sağlar.

**Soru 3:** Lambda fonksiyonları `def` ile tanımlanan fonksiyonların yerini her durumda alabilir.
- Cevap: Yanlış
- Açıklama: Lambda fonksiyonları tek ifadeli ve anonimdir; karmaşık işlemler için `def` kullanılmalıdır.

**Soru 4:** LEGB kuralına göre, bir değişken önce Local (yerel) kapsamda aranır.
- Cevap: Doğru
- Açıklama: LEGB (Local, Enclosing, Global, Built-in) sırasıyla değişken araması yapılır.

**Soru 5:** Bir modül içindeki tüm fonksiyonları içe aktarmak için `import *` kullanımı önerilir.
- Cevap: Yanlış
- Açıklama: `import *` ad çakışmalarına yol açabileceği için önerilmez; belirli fonksiyonları içe aktarmak daha iyidir.

**Soru 6:** `**kwargs` parametresi, anahtar-değer çiftleri şeklinde argümanlar alır.
- Cevap: Doğru
- Açıklama: `**kwargs` sözlük (dictionary) olarak anahtar-değer çiftlerini toplar.

**Soru 7:** `global` anahtar kelimesi olmadan bir fonksiyon içinde global değişken değiştirilebilir.
- Cevap: Yanlış
- Açıklama: Global değişkeni değiştirmek için `global` anahtar kelimesi kullanılmalıdır; aksi halde yerel değişken oluşturulur.

**Soru 8:** `map()` fonksiyonu, bir listenin her elemanına belirtilen fonksiyonu uygular.
- Cevap: Doğru
- Açıklama: `map()` fonksiyonu, bir iterable'ın her elemanına fonksiyon uygulayarak yeni bir iterable döndürür.

**Soru 9:** Bir paket, içinde `__init__.py` dosyası bulunan bir dizindir.
- Cevap: Doğru
- Açıklama: `__init__.py` dosyası, bir dizini Python paketi olarak işaretler (Python 3.3+ sonrası opsiyonel).

**Soru 10:** `filter()` fonksiyonu, koşulu sağlayan elemanları filtreler ve liste döndürür.
- Cevap: Yanlış
- Açıklama: `filter()` bir iterable döndürür; listeye çevirmek için `list()` kullanılmalıdır.

---

## Boşluk Doldurma Soruları

**Soru 1:** Python'da bir fonksiyon tanımlamak için _______ anahtar kelimesi kullanılır.
- Cevap: def
- Açıklama: `def` anahtar kelimesi fonksiyon tanımlamanın temel yapı taşıdır.

**Soru 2:** Değişken sayıda konumsal argüman almak için parametre olarak _______ kullanılır.
- Cevap: *args
- Açıklama: `*args` tüm konumsal argümanları bir demet (tuple) olarak toplar.

**Soru 3:** LEGB kuralındaki "E" harfi _______ kapsamını temsil eder.
- Cevap: Enclosing (sarmalayan)
- Açıklama: Enclosing kapsam, iç içe fonksiyonlarda dış fonksiyonun kapsamıdır.

**Soru 4:** Bir modülü içe aktarmak için _______ ifadesi kullanılır.
- Cevap: import
- Açıklama: `import` ifadesi, başka bir modülün içeriğini kullanılabilir hale getirir.

**Soru 5:** Anahtar-değer çiftleri şeklinde değişken sayıda argüman almak için _______ kullanılır.
- Cevap: **kwargs
- Açıklama: `**kwargs` anahtar-değer çiftlerini sözlük (dictionary) olarak toplar.

**Soru 6:** Bir fonksiyon içinde global değişkeni değiştirmek için _______ anahtar kelimesi kullanılır.
- Cevap: global
- Açıklama: `global` anahtar kelimesi, yerel kapsamda global değişkene erişim ve değişiklik yapmayı sağlar.

**Soru 7:** Tek ifadeli anonim fonksiyonlar _______ fonksiyonları olarak adlandırılır.
- Cevap: lambda
- Açıklama: Lambda fonksiyonları, tek satırda tanımlanan ve isimsiz olan fonksiyonlardır.

**Soru 8:** Bir listenin her elemanına belirtilen fonksiyonu uygulamak için _______ fonksiyonu kullanılır.
- Cevap: map()
- Açıklama: `map()` fonksiyonu, bir iterable'ın her elemanına fonksiyon uygular.

**Soru 9:** Bir dizini Python paketi yapmak için içine _______ dosyası eklenir.
- Cevap: __init__.py
- Açıklama: `__init__.py` dosyası, dizini bir paket olarak tanımlar (Python 3.3+ sonrası opsiyonel).

**Soru 10:** Bir fonksiyonun kendini çağırmasına _______ denir.
- Cevap: özyineleme (recursion)
- Açıklama: Özyineleme, bir fonksiyonun doğrudan veya dolaylı olarak kendini çağırmasıdır.