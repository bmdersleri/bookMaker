# Bölüm 2: Değişkenler ve Veri Tipleri — PLAN

## 1. KAVRAMLAR

| # | Kavram | Ne olduğu (1 cümle) | Zorluk | Kod örneği? | Gösterilecek konu |
|---|--------|---------------------|--------|-------------|-------------------|
| 1 | Değişken tanımlama | Programda veri saklamak için bellek alanına isim verme işlemi | ★☆☆☆☆ | Evet | int yas = 25; ile değişken oluşturma ve değer atama |
| 2 | Veri tipleri (int) | Tam sayıları saklayan temel veri tipi | ★☆☆☆☆ | Evet | int sayi = 42; ile tamsayı işlemleri |
| 3 | Veri tipleri (float/double) | Ondalıklı sayıları saklayan veri tipleri | ★★☆☆☆ | Evet | double fiyat = 19.99; ile küsüratlı işlemler |
| 4 | Veri tipleri (String) | Metin dizilerini saklayan referans tipi | ★★☆☆☆ | Evet | String isim = "Ali"; ile metin işlemleri |
| 5 | Veri tipleri (boolean) | Doğru/yanlış değerlerini saklayan mantıksal tip | ★★☆☆☆ | Evet | boolean ogrenciMi = true; ile karar mekanizmaları |
| 6 | Tip dönüşümleri (casting) | Bir veri tipini başka bir veri tipine dönüştürme | ★★★☆☆ | Evet | int toplam = (int) 3.14; ile bilinçli/bilinçsiz dönüşüm |
| 7 | Scanner (input) | Kullanıcıdan klavye ile veri alma | ★★☆☆☆ | Evet | Scanner ile kullanıcıdan yaş alma ve işleme |
| 8 | String metodları | Metinler üzerinde işlem yapan hazır fonksiyonlar | ★★★☆☆ | Evet | length(), toUpperCase(), substring() kullanımı |
| 9 | String birleştirme (concatenation) | Birden çok metni veya değişkeni tek metinde birleştirme | ★★☆☆☆ | Evet | "Ad: " + isim + " Yaş: " + yas ile dinamik çıktı |
| 10 | null değeri | Bir referans değişkeninin hiçbir nesneyi göstermediği durum | ★★★★☆ | Evet | String mesaj = null; ile null kontrolü ve NullPointerException |
| 11 | final anahtar kelimesi | Değeri değiştirilemeyen sabit değişken tanımlama | ★★☆☆☆ | Evet | final double PI = 3.14159; ile sabit tanımlama |
| 12 | Değişken kapsamı (scope) | Değişkenin program içinde geçerli olduğu bölge | ★★★★☆ | Evet | Blok içi/blok dışı değişken erişimi örneği |

## 2. KOD ÖRNEKLERİ

| # | Kavram(lar) | Dosya adı | Tahmini satır | Kullanılacak Java özellikleri |
|---|-------------|-----------|---------------|------------------------------|
| 1 | Değişken tanımlama, int, double | DegiskenTanimlama.java | 15 | int, double değişken bildirimi, atama, System.out.println |
| 2 | String, boolean | MetinVeMantik.java | 18 | String, boolean, length(), isEmpty(), + operatörü |
| 3 | Tip dönüşümleri | TipDonusumleri.java | 25 | int→double (genişletme), double→int (daraltma), String→int (parseInt) |
| 4 | Scanner, input | KullaniciGirdisi.java | 20 | Scanner sınıfı, nextInt(), nextLine(), nextDouble() |
| 5 | String metodları | StringMetodlari.java | 30 | toUpperCase(), toLowerCase(), substring(), replace(), trim() |
| 6 | final, null | SabitVeNull.java | 22 | final değişken, null ataması, null kontrolü (if) |
| 7 | Kapsam (scope) | DegiskenKapsami.java | 20 | Blok scope, metod scope, sınıf scope karşılaştırması |
| 8 | Bütünleşik örnek | OgrenciBilgiSistemi.java | 40 | Scanner, String, int, double, final, tip dönüşümü, null — hepsi bir arada |

## 3. DİYAGRAMLAR

| # | Görselleştirilecek konu | Tür | Düğümler |
|---|------------------------|-----|----------|
| 1 | Java'da veri tiplerinin hiyerarşisi ve bellek kullanımı | Class diagram | İlkel tipler (8 adet), Referans tipleri (String, Diziler, Sınıflar), Bellek bölgeleri (Stack, Heap) — toplam ~12 düğüm |
| 2 | Tip dönüşümü karar akışı (otomatik mi, manuel mi?) | Flowchart | Başla → Tip nedir? → Genişletme mi? (elmas) → Evet: otomatik dönüş → Hayır: daraltma mı? (elmas) → Evet: explicit casting → Hayır: hata → String dönüşümü mü? (elmas) → parseInt/parseDouble → Bitir — toplam 8 düğüm |
| 3 | Scanner ile kullanıcı girdisi alma akışı | Sequence diagram | Kullanıcı, Scanner nesnesi, Program, nextInt() çağrısı, veri dönüşü, değişkene atama, işleme — toplam 6 katılımcı |
| 4 | Değişken kapsamı ve ömür süresi | Flowchart | Program başlangıcı → Sınıf değişkeni oluşur → Metod çağrısı → Yerel değişken oluşur → Blok açılır → Blok değişkeni oluşur → Blok kapanır (değişken yok olur) → Metod biter (yerel değişken yok olur) → Program biter (sınıf değişkeni yok olur) — toplam 10 düğüm |

## 4. SÖZLÜK (Terimler)

1. Değişken (Variable)
2. Veri Tipi (Data Type)
3. İlkel Tip (Primitive Type)
4. Referans Tipi (Reference Type)
5. Tip Dönüşümü (Type Casting)
6. Otomatik Dönüşüm (Widening/Automatic)
7. Daraltma Dönüşümü (Narrowing/Explicit)
8. String Birleştirme (String Concatenation)
9. Metod Çağrısı (Method Call)
10. null
11. final (Sabit)
12. Kapsam (Scope)
13. Scanner
14. Stack ve Heap (Bellek Bölgeleri)
15. Literal (Sabit Değer)

## 5. DEĞERLENDİRME

### Doğru/Yanlış Soruları (5-10 adet konu)

1. Java'da `int` tipi ondalıklı sayıları saklayabilir. (Yanlış)
2. `double` tipi `int` tipinden daha geniş bir değer aralığına sahiptir. (Doğru)
3. `String` bir ilkel (primitive) veri tipidir. (Yanlış)
4. Otomatik tip dönüşümünde veri kaybı olmaz. (Doğru)
5. `null` değeri herhangi bir ilkel tipe atanabilir. (Yanlış)
6. `final` ile tanımlanan değişkenin değeri program içinde değiştirilemez. (Doğru)
7. `Scanner` sınıfı `java.util` paketinin içindedir. (Doğru)
8. Blok içinde tanımlanan değişkene blok dışından erişilebilir. (Yanlış)

### Boşluk Doldurma Soruları (5-10 adet konu)

1. Tam sayıları saklamak için ____ veri tipi kullanılır. (int)
2. Java'da metin dizilerini saklamak için ____ sınıfı kullanılır. (String)
3. Bir `double` değeri `int` değere dönüştürürken ____ işleci kullanılır. ((int))
4. Kullanıcıdan klavye ile veri almak için ____ sınıfı kullanılır. (Scanner)
5. Değeri değiştirilemeyen değişkenler ____ anahtar kelimesi ile tanımlanır. (final)
6. Bir String'in uzunluğunu öğrenmek için ____ metodu kullanılır. (length())
7. Bir referans değişkeninin hiçbir nesneyi göstermediği durumda değeri ____ olur. (null)
8. String'leri birleştirmek için ____ operatörü kullanılır. (+)

## 6. ALIŞTIRMALAR

| # | Konu | Zorluk | Tarif |
|---|------|--------|-------|
| 1 | Kişisel bilgi kartı | ★☆☆☆☆ | Kullanıcıdan ad, soyad, yaş ve boy bilgilerini alan, bunları bir cümlede birleştirip ekrana yazdıran program. int, double, String ve Scanner kullanılacak. |
| 2 | Daire hesaplayıcı | ★★☆☆☆ | Kullanıcıdan yarıçap alan, dairenin alanını ve çevresini hesaplayan program. final double PI, double, Scanner, tip dönüşümü (sonucu int'e çevirme) içerecek. |
| 3 | Metin analizörü | ★★★☆☆ | Kullanıcıdan bir metin alan, metnin uzunluğunu, ilk ve son karakterini, büyük/küçük harf versiyonlarını, "merhaba" kelimesini içerip içermediğini bulan program. String metodları (length, charAt, toUpperCase, toLowerCase, contains, substring) kullanılacak. null durumu ve boş metin kontrolü eklenecek. |

## 7. SIK YAPILAN HATALAR

1. **İlkel tiplere null atama hatası:** `int sayi = null;` yazmak — ilkel tipler null alamaz, sadece referans tipleri alabilir.
2. **Daraltma dönüşümünde veri kaybını fark etmeme:** `double` değeri `int`'e çevirirken küsüratın kaybolduğunu bilmeden işlem yapmak.
3. **Scanner'da nextInt() sonrası nextLine() sorunu:** Sayı girdisinden sonra kalan newline karakterini okumadan yeni metin almaya çalışmak.
4. **String karşılaştırmada == kullanımı:** İki String'in içeriğini karşılaştırırken `==` yerine `equals()` kullanılması gerektiğini unutmak.
5. **null üzerinde metod çağırma:** `null` değerine sahip bir String üzerinde `length()` çağırmak — NullPointerException hatası.
6. **Değişken kapsamını ihlal etme:** Bir blok içinde tanımlanan değişkene blok dışından erişmeye çalışmak.
7. **final değişkene tekrar atama:** `final` olarak tanımlanan değişkene ikinci kez değer atamaya çalışmak.

## 8. TABLOLAR

### Tablo 1: Java İlkel Veri Tipleri Karşılaştırması
- Sütunlar: Tip adı, Boyut (byte), Varsayılan değer, Değer aralığı, Kullanım örneği
- Satırlar: byte, short, int, long, float, double, char, boolean

### Tablo 2: Otomatik vs Manuel Tip Dönüşümü
- Sütunlar: Dönüşüm türü, Yön, Operatör gerekiyor mu?, Veri kaybı riski?, Örnek
- Satırlar: int→double, double→int, String→int, int→String, char→int

### Tablo 3: Sık Kullanılan String Metodları
- Sütunlar: Metod adı, Dönüş tipi, Açıklama, Örnek kullanım, Örnek sonuç
- Satırlar: length(), charAt(), toUpperCase(), toLowerCase(), substring(), replace(), trim(), contains(), equals(), isEmpty()

### Tablo 4: Değişken Türlerine Göre Kapsam ve Ömür
- Sütunlar: Değişken türü, Tanımlandığı yer, Kapsam, Ömür, Varsayılan değer
- Satırlar: Yerel değişken (metod içi), Parametre değişkeni, Sınıf değişkeni (static), Örnek değişkeni (instance), Blok değişkeni

---

**Not:** Bu plan, Bölüm 2'nin tüm kavramlarını kapsamakta ve her bir kavram için 6 adımlı işleme zincirine uygun şekilde kod, diyagram, tablo ve alıştırma hazırlıklarını içermektedir. Sıradaki aşamada her kavram için belirtilen sırayla içerik üretilecektir.