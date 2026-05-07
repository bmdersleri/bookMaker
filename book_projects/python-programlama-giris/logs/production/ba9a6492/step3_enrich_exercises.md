**Alıştırma 1: Not Ortalaması Hesaplayıcı (Kolay)**

- Amaç: Bu alıştırmada, kullanıcıdan alınan iki sınav notunu kullanarak basit bir ortalama hesaplamayı, `Scanner` sınıfı ile veri almayı ve `final` anahtar kelimesi ile sabit tanımlamayı öğreneceksin.
- Görev: Kullanıcıdan iki adet sınav notu (vize ve final) isteyen bir Java programı yaz. Vize notunun %40’ını, final notunun %60’ını alarak ortalamayı hesapla. Ortalama 50 ve üzeri ise “Geçti”, değilse “Kaldı” yazdır. Vize ve final ağırlıklarını `final` değişken olarak tanımla. Notları `double` veri tipinde al.
- İpucu: Kullanıcıdan veri almak için `Scanner` sınıfını kullan. Ağırlıkları `final double VIZE_AGIRLIK = 0.4;` şeklinde tanımla. Ortalama hesaplarken tip dönüşümüne dikkat et.
- Beklenen Çıktı:
```
Vize notunuzu giriniz: 60
Final notunuzu giriniz: 70
Ortalamaniz: 66.0
Gecti
```

**Alıştırma 2: Kişisel Bilgi Kartı Oluşturucu (Orta)**

- Amaç: Bu alıştırmada, farklı veri tiplerini (`String`, `int`, `double`, `char`, `boolean`) kullanmayı, `String` metodları ile metin işlemeyi (`toUpperCase`, `length`, `trim`) ve `null` değerini anlamayı öğreneceksin.
- Görev: Kullanıcıdan ad, soyad, yaş, boy (metre cinsinden, örn: 1.75) ve medeni hal (evli için 'E', bekar için 'B') bilgilerini alan bir program yaz. Alınan bilgileri şu kurallara göre işleyip ekrana yazdır:
    1. Ad ve soyadı büyük harfe çevir.
    2. Ad ve soyadın toplam karakter sayısını bul.
    3. Yaş ile boyu toplayıp sonucu yazdır (tip dönüşümüne dikkat et).
    4. Kullanıcının adını başında ve sonunda boşluk olacak şekilde al (`" Ismail "` gibi), sonra `trim()` ile temizle.
    5. Eğer medeni hal 'E' ise "Evli", 'B' ise "Bekar" yazdır. Eğer kullanıcı bu soruyu boş geçerse (`null` veya boş String), "Bilinmiyor" yazdır.
- İpucu: `Scanner.nextLine()` ile String alırken, sayısal bir değer aldıktan sonra oluşan satırsonu sorununu çözmek için fazladan bir `nextLine()` ekle. `isEmpty()` veya `isBlank()` metodları ile boş kontrolü yap. `char` tipini kontrol etmek için `==` operatörünü kullan.
- Beklenen Çıktı:
```
Adinizi giriniz (basinda ve sonunda bosluk olabilir):   Ismail   
Soyadinizi giriniz: Kirbas
Yasinizi giriniz: 30
Boyunuzu giriniz (metre): 1.75
Medeni haliniz (E/B): E

--- Kisisel Bilgi Kartiniz ---
Ad Soyad: ISMAIL KIRBAS
Karakter Sayisi: 12
Yas + Boy: 31.75
Medeni Durum: Evli
```