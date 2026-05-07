**Alıştırma 1: Günlük Tutucu (Kolay)**

- **Amaç:** Bu alıştırmada, kullanıcıdan alınan metin girdisini bir dosyaya nasıl yazacağını ve dosyadan nasıl okuyacağını öğreneceksin. Ayrıca, dosya işlemleri sırasında oluşabilecek hataları (örneğin dosyanın bulunamaması) nasıl yöneteceğini kavrayacaksın.

- **Görev:** Kullanıcıya bir menü gösteren bir program yaz. Menüde şu seçenekler olsun:
    1. Yeni günlük girişi ekle (Kullanıcıdan metin al ve `gunluk.txt` dosyasının sonuna ekle).
    2. Tüm günlüğü oku (`gunluk.txt` dosyasının tüm içeriğini ekrana yazdır).
    3. Çıkış.
    Kullanıcı 1 veya 2'yi seçtiğinde, dosya işlemi sırasında oluşabilecek herhangi bir hatayı (`FileNotFoundException`, `IOException`) yakala ve kullanıcıya anlaşılır bir hata mesajı göster.

- **İpucu:** Dosyaya ekleme yapmak için `FileWriter`'ı `true` parametresiyle (append mode), okumak için `BufferedReader` ve `FileReader` kullanabilirsin. Hataları yakalamak için `try-catch` blokları kullanmayı unutma.

- **Beklenen Çıktı:**
    ```
    === Günlük Uygulaması ===
    1. Yeni giriş ekle
    2. Günlüğü oku
    3. Çıkış
    Seçiminiz: 1
    Günlük girişinizi yazın: Java öğrenmek çok eğlenceli!
    Giriş başarıyla eklendi.

    Seçiminiz: 2
    --- Günlük İçeriği ---
    Java öğrenmek çok eğlenceli!

    Seçiminiz: 3
    Program sonlandırıldı.
    ```

**Alıştırma 2: Öğrenci Not Ortalaması Hesaplayıcı (Orta)**

- **Amaç:** Bu alıştırmada, bir dosyadaki yapılandırılmış veriyi (CSV formatı) nasıl okuyacağını, bu veriyi işleyerek bir hesaplama yapmayı ve sonucu yeni bir dosyaya nasıl yazacağını öğreneceksin. Ayrıca, dosya formatı hataları gibi özel durumları nasıl ele alacağını da deneyimleyeceksin.

- **Görev:** `ogrenciler.txt` adında bir dosya oluştur. Dosyanın her satırı bir öğrenciyi temsil etsin ve şu formatta olsun: `öğrenciAdı,not1,not2,not3` (örneğin: `Ali,85,90,78`). Programın şunları yapsın:
    1. Bu dosyayı oku.
    2. Her satırı virgülden ayırarak öğrenci adını ve üç notu al.
    3. Her öğrencinin not ortalamasını hesapla.
    4. Sonuçları `ortalamalar.txt` dosyasına şu formatta yaz: `öğrenciAdı: ortalama`.
    5. Eğer dosya bulunamazsa veya bir satır beklenen formatta değilse (örneğin sayı yerine harf varsa), uygun bir hata mesajı göster ve programı sonlandırmadan diğer satırları işlemeye devam et.

- **İpucu:** Satırları ayırmak için `String.split(",")` metodunu kullanabilirsin. Sayısal dönüşümler için `Integer.parseInt()` veya `Double.parseDouble()` kullan. `NumberFormatException` hatasını yakalamak için ayrı bir `try-catch` bloğu kullan. Dosyayı satır satır okumak için `Scanner` veya `BufferedReader` tercih edebilirsin.

- **Beklenen Çıktı:**
    ```
    Program çalıştırıldığında konsolda bir çıktı olmayacak, ancak `ortalamalar.txt` dosyası oluşturulacak.
    ```

    `ogrenciler.txt` dosyası:
    ```
    Ali,85,90,78
    Ayse,92,88,95
    Mehmet,70,abc,80   // Hatalı veri
    Fatma,100,95,98
    ```

    `ortalamalar.txt` dosyası (beklenen içerik):
    ```
    Ali: 84.33
    Ayse: 91.67
    Fatma: 97.67
    ```
    *Not: Mehmet için hatalı veri olduğundan, program konsola "Hatalı veri satırı atlandı: Mehmet,70,abc,80" gibi bir mesaj yazdırabilir ve bu satırı işlemeden atlar. Bu, beklenen bir davranıştır.*