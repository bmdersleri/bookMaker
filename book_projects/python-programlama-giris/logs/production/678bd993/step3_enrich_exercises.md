**Alıştırma 1: Not Hesaplama Makinesi (Kolay)**

- Amaç: Bu alıştırmada, kullanıcıdan alınan bir sınav notunu if-else koşul yapıları ile değerlendirmeyi ve harf notuna çevirmeyi öğreneceksin.
- Görev: Kullanıcıdan 0 ile 100 arasında bir not değeri girmesini isteyen bir program yaz. Girilen notu aşağıdaki tabloya göre harf notuna çevir ve ekrana yazdır.
    - 90-100 arası: AA
    - 80-89 arası: BA
    - 70-79 arası: BB
    - 60-69 arası: CB
    - 50-59 arası: CC
    - 0-49 arası: FF (Kaldı)
- İpucu: `Scanner` sınıfını kullanarak kullanıcıdan sayısal girdi alabilirsin. Koşulları kontrol ederken `if`, `else if` ve `else` bloklarını sıralı olarak kullanmayı unutma. Ayrıca, kullanıcının geçerli bir not aralığı girdiğinden emin olmak için bir kontrol mekanizması ekleyebilirsin.
- Beklenen Çıktı:
    ```
    Notunuzu giriniz (0-100): 85
    Harf Notunuz: BA
    ```
    Veya hatalı giriş durumunda:
    ```
    Notunuzu giriniz (0-100): 105
    Geçersiz not! Lütfen 0 ile 100 arasında bir değer giriniz.
    ```

**Alıştırma 2: Çarpım Tablosu Oluşturucu (Orta)**

- Amaç: Bu alıştırmada, iç içe geçmiş `for` döngülerini kullanarak düzenli bir çarpım tablosu oluşturmayı ve tablo formatında çıktı almayı öğreneceksin.
- Görev: Kullanıcıdan 1 ile 10 arasında bir sayı (N) alan ve 1'den N'e kadar olan sayıların çarpım tablosunu ekrana yazdıran bir program yaz. Tablonun sütunları ve satırları düzgün bir şekilde hizalanmış olmalıdır. Program, kullanıcı 0 girene kadar yeni bir sayı istemeye devam etmelidir.
- İpucu: İlk döngü satırları (`i`), ikinci döngü ise sütunları (`j`) temsil etsin. Çarpım sonucunu `i * j` ile hesapla. Çıktıyı hizalamak için `System.out.printf("%4d", i * j);` yapısını kullanabilirsin. Sonsuz döngüden çıkmak için kullanıcıdan alınan değeri bir `while` döngüsü içinde kontrol et (örn. `while (sayi != 0)`).
- Beklenen Çıktı:
    ```
    Bir sayi giriniz (0=çıkış): 5
       1   2   3   4   5
       2   4   6   8  10
       3   6   9  12  15
       4   8  12  16  20
       5  10  15  20  25

    Bir sayi giriniz (0=çıkış): 0
    Program sonlandı.
    ```