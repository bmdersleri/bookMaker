**Alıştırma 1: Kişisel Tanıtım Kartı (Kolay)**
- Amaç: Bu alıştırmada `print()` fonksiyonunu kullanarak birden fazla satıra çıktı yazdırmayı ve metin içinde değişken kullanmayı öğreneceksin.
- Görev: Adını, soyadını, yaşını ve en sevdiğin programlama dilini içeren bir kişisel tanıtım kartı yazdıran bir Java programı yaz. Her bilgiyi ayrı bir `System.out.println()` çağrısı ile yazdır. Programın sonunda, tüm bu bilgileri tek bir `System.out.printf()` çağrısı ile tek satırda, virgüllerle ayırarak tekrar yazdır.
- İpucu: Metin ve değişkenleri birleştirmek için `+` operatörünü (`System.out.println("Ad: " + ad)`) veya `String.format()` ile `printf()` metodunu kullanabilirsin. Yaş için `int`, isimler için `String` veri tipi kullan.
- Beklenen Çıktı:
```
Ad: Ahmet
Soyad: Yılmaz
Yaş: 25
En sevdiği dil: Java
Ahmet, Yılmaz, 25, Java
```

**Alıştırma 2: Basit Hesap Makinesi Menüsü (Orta)**
- Amaç: Bu alıştırmada kullanıcıdan veri almayı (`Scanner` sınıfı), temel aritmetik işlemleri yapmayı ve sonuçları formatlı bir şekilde yazdırmayı öğreneceksin. Ayrıca yorum satırları ile kodu belgelemeyi pekiştireceksin.
- Görev: Kullanıcıdan iki tam sayı alan bir program yaz. Program, bu sayılar üzerinde toplama, çıkarma, çarpma ve bölme işlemlerini yapsın. Her işlemin sonucunu, işlemin adını da belirterek ekrana yazdırsın. Bölme işleminin sonucunu ondalıklı sayı olarak göstermek için sayılardan birini `double`'a dönüştür. Kodunun başına programın ne yaptığını açıklayan çok satırlı bir yorum (`/* ... */`) ekle.
- İpucu: Kullanıcıdan veri almak için `Scanner` sınıfını kullan. `Scanner`'ı kapatmayı unutma (`scanner.close()`). Bölme işleminde `(double) sayi1 / sayi2` dönüşümünü kullan. Çıktıyı formatlamak için `System.out.printf("%s: %.2f", "Toplam", sonuc)` yapısını dene.
- Beklenen Çıktı:
```
Birinci sayıyı giriniz: 10
İkinci sayıyı giriniz: 3
Toplama: 13
Çıkarma: 7
Çarpma: 30
Bölme: 3.33
```