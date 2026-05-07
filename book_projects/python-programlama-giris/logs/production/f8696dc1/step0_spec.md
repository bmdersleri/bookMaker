# Bölüm Planı: Dosya İşlemleri ve Hata Yönetimi

## 1. KAVRAMLAR

### Dosya Açma Modları
- **Ne olduğu:** Bir dosyanın hangi amaçla (okuma, yazma, ekleme) ve hangi formatta (metin, ikili) açılacağını belirten parametreler
- **Zorluk:** ★★☆☆☆
- **Kod örneği:** Evet
- **Göstereceği:** `FileReader`, `FileWriter`, `BufferedReader`, `BufferedWriter` ile farklı mod kullanımı

### try-catch-finally Blokları
- **Ne olduğu:** Çalışma zamanı hatalarını yakalamak ve programın çökmesini engellemek için kullanılan yapı
- **Zorluk:** ★★★☆☆
- **Kod örneği:** Evet
- **Göstereceği:** `try`, `catch`, `finally` bloklarının sıralı çalışması

### checked vs unchecked İstisnalar
- **Ne olduğu:** Java'da derleme zamanında (IOException) ve çalışma zamanında (RuntimeException) oluşan hata türleri
- **Zorluk:** ★★★★☆
- **Kod örneği:** Evet
- **Göstereceği:** `throws` anahtar kelimesi ile checked istisna bildirimi

### throw Anahtar Kelimesi
- **Ne olduğu:** İstisna nesnesini manuel olarak fırlatmak için kullanılan ifade
- **Zorluk:** ★★★☆☆
- **Kod örneği:** Evet
- **Göstereceği:** Geçersiz dosya adı durumunda özel hata fırlatma

### Özel İstisna Sınıfları
- **Ne olduğu:** Exception sınıfından türetilerek oluşturulan, uygulamaya özgü hata sınıfları
- **Zorluk:** ★★★★☆
- **Kod örneği:** Evet
- **Göstereceği:** `DosyaBulunamadiException` gibi özel sınıf tanımı

### try-with-resources
- **Ne olduğu:** Otomatik kaynak yönetimi sağlayan, Java 7 ile gelen try bloğu
- **Zorluk:** ★★★☆☆
- **Kod örneği:** Evet
- **Göstereceği:** Dosyayı otomatik kapatma, finally bloğu ihtiyacını ortadan kaldırma

### BufferedReader ve BufferedWriter
- **Ne olduğu:** Karakter akışlarını tamponlayarak okuma/yazma performansını artıran sarmalayıcı sınıflar
- **Zorluk:** ★★☆☆☆
- **Kod örneği:** Evet
- **Göstereceği:** `readLine()`, `write()`, `newLine()` metotları

### PrintWriter
- **Ne olduğu:** Biçimlendirilmiş çıktı için kullanılan, `printf()` benzeri metotlar sunan yazma sınıfı
- **Zorluk:** ★★☆☆☆
- **Kod örneği:** Evet
- **Göstereceği:** `println()`, `printf()` ile dosyaya yazma

### File Sınıfı
- **Ne olduğu:** Dosya ve dizin yollarını temsil eden, dosya metaverilerine erişim sağlayan sınıf
- **Zorluk:** ★☆☆☆☆
- **Kod örneği:** Evet
- **Göstereceği:** `exists()`, `isDirectory()`, `listFiles()` metotları

### NIO.2 (Path ve Files Sınıfları)
- **Ne olduğu:** Java 7 ile gelen, daha modern ve esnek dosya işlemleri API'si
- **Zorluk:** ★★★☆☆
- **Kod örneği:** Evet
- **Göstereceği:** `Files.readAllLines()`, `Files.write()` ile kolay dosya okuma/yazma

---

## 2. KOD ÖRNEKLERİ

### Örnek 1: Temel Dosya Okuma (try-catch ile)
- **Kavram:** try-catch-finally, FileReader, BufferedReader
- **Dosya adı:** `ogrenciler.txt` (okunacak), `DosyaOkuyucu.java`
- **Satır sayısı:** ~25 satır
- **Java özellikleri:** try-catch-finally, FileReader, BufferedReader, IOException

### Örnek 2: Dosyaya Yazma (PrintWriter ile)
- **Kavram:** PrintWriter, FileWriter, try-with-resources
- **Dosya adı:** `notlar.txt` (yazılacak), `DosyaYazici.java`
- **Satır sayısı:** ~20 satır
- **Java özellikleri:** try-with-resources, PrintWriter, FileWriter

### Örnek 3: Dosya Kopyalama (Buffered Stream)
- **Kavram:** BufferedInputStream, BufferedOutputStream
- **Dosya adı:** `kaynak.jpg` -> `hedef.jpg`, `DosyaKopyalayici.java`
- **Satır sayısı:** ~30 satır
- **Java özellikleri:** try-with-resources, BufferedInputStream, BufferedOutputStream, FileInputStream, FileOutputStream

### Örnek 4: Özel İstisna Sınıfı Kullanımı
- **Kavram:** Özel istisna sınıfları, throw
- **Dosya adı:** `DosyaIslemleri.java`, `GecersizDosyaAdiException.java`
- **Satır sayısı:** ~35 satır (iki sınıf)
- **Java özellikleri:** Exception mirası, throw, throws

### Örnek 5: Dizin Gezme ve Filtreleme (File Sınıfı)
- **Kavram:** File sınıfı, listFiles(), FilenameFilter
- **Dosya adı:** `DizinGezgini.java`
- **Satır sayısı:** ~25 satır
- **Java özellikleri:** File, FilenameFilter (lambda), isDirectory(), getName()

### Örnek 6: NIO.2 ile Modern Dosya İşlemleri
- **Kavram:** Path, Files, NIO.2
- **Dosya adı:** `NioDosyaIslemleri.java`
- **Satır sayısı:** ~30 satır
- **Java özellikleri:** Paths.get(), Files.readAllLines(), Files.write(), Files.copy()

### Örnek 7: Çoklu İstisna Yakalama ve finally
- **Kavram:** Çoklu catch blokları, finally
- **Dosya adı:** `CokluHataYonetimi.java`
- **Satır sayısı:** ~35 satır
- **Java özellikleri:** Birden çok catch bloğu (| operatörü ile), finally

---

## 3. DİYAGRAMLAR

### Diyagram 1: İstisna Hiyerarşisi (Class Diagram)
- **Amaç:** checked ve unchecked istisnalar arasındaki farkı görselleştirmek
- **Tür:** Class diagram
- **Düğümler:** Throwable, Exception, RuntimeException, IOException, FileNotFoundException, ArithmeticException, NullPointerException, checked/unchecked etiketleri

### Diyagram 2: try-catch-finally Akış Şeması (Flowchart)
- **Amaç:** İstisna oluştuğunda ve oluşmadığında program akışını göstermek
- **Tür:** Flowchart
- **Düğümler:** Başla, try bloğu, istisna oluştu mu? (elmas), catch bloğu (2 yol), finally bloğu, devam et, program sonu

### Diyagram 3: Dosya İşlemleri Akışı (Sequence Diagram)
- **Amaç:** try-with-resources ile kaynakların otomatik kapanma sırasını göstermek
- **Tür:** Sequence diagram
- **Düğümler:** Program, try-with-resources, FileReader, BufferedReader, close() çağrıları, kaynak serbest bırakma

---

## 4. SÖZLÜK (Terim Listesi)

1. İstisna (Exception)
2. Çalışma Zamanı İstisnası (RuntimeException)
3. Derleme Zamanı İstisnası (Checked Exception)
4. try bloğu
5. catch bloğu
6. finally bloğu
7. throw anahtar kelimesi
8. throws bildirimi
9. try-with-resources
10. Otomatik Kaynak Yönetimi (ARM)
11. Tamponlama (Buffering)
12. Karakter Akışı (Character Stream)
13. Bayt Akışı (Byte Stream)
14. Dosya Yolu (Path)
15. Closeable arayüzü

---

## 5. DEĞERLENDİRME

### Doğru/Yanlış Soruları (5-10 adet)

1. **Konsept:** Checked istisnalar zorunlu yakalama gerektirir
2. **Konsept:** finally bloğu her zaman çalışır (return olsa bile)
3. **Konsept:** try-with-resources, finally bloğu ihtiyacını ortadan kaldırır
4. **Konsept:** RuntimeException checked istisna sınıfıdır
5. **Konsept:** File sınıfı dosya içeriğini okumak için kullanılır
6. **Konsept:** Birden çok catch bloğu sıralı kontrol edilir
7. **Konsept:** throw ve throws aynı anlama gelir
8. **Konsept:** BufferedWriter, FileWriter'dan daha hızlıdır
9. **Konsept:** NIO.2 API'si Java 6 ile gelmiştir
10. **Konsept:** Özel istisna sınıfları Exception'dan türetilmelidir

### Boşluk Doldurma Soruları (5-10 adet)

1. **Konu:** try bloğunda oluşan hatayı yakalamak için ___ bloğu kullanılır
2. **Konu:** Kaynakların otomatik kapatılmasını sağlayan try çeşidi ___ olarak adlandırılır
3. **Konu:** IOException ___ istisna türüdür
4. **Konu:** Bir metodu çağırana istisna bildirmek için ___ anahtar kelimesi kullanılır
5. **Konu:** Dosyadan satır satır okumak için ___ sınıfının readLine() metodu kullanılır
6. **Konu:** İstisna fırlatmak için ___ anahtar kelimesi kullanılır
7. **Konu:** try bloğundan sonra her koşulda çalışan blok ___ bloğudur
8. **Konu:** Dosya yollarını temsil eden modern sınıf ___ sınıfıdır

---

## 6. ALIŞTIRMALAR

### Alıştırma 1: Öğrenci Not Defteri (Zorluk: ★★☆☆☆)
- **Konu:** Temel dosya okuma/yazma, try-catch kullanımı
- **Açıklama:** Kullanıcıdan alınan öğrenci adı ve not bilgilerini dosyaya yazan, ardından dosyadaki tüm kayıtları okuyan bir program

### Alıştırma 2: Log Sistemi (Zorluk: ★★★☆☆)
- **Konu:** Özel istisna sınıfları, throw, çoklu catch
- **Açıklama:** Uygulama hatalarını tarih ve saat bilgisiyle dosyaya kaydeden, belirli hata türleri için özel istisna sınıfları oluşturan bir log sistemi

### Alıştırma 3: Dosya Gezgini (Zorluk: ★★★★☆)
- **Konu:** File sınıfı, NIO.2, dizin işlemleri
- **Açıklama:** Belirtilen bir dizindeki tüm .txt dosyalarını bulan, her dosyanın boyutunu ve satır sayısını hesaplayan, sonuçları rapor dosyasına yazan bir program

---

## 7. SIK YAPILAN HATALAR

1. **Dosyayı kapatmayı unutmak:** finally bloğu yazılmazsa dosya kaynakları sızıntısı oluşur
2. **Yanlış istisna türü yakalamak:** FileNotFoundException yerine Exception yakalamak, daha spesifik hata bilgisini kaybettirir
3. **Catch sırasını yanlış ayarlamak:** Alt sınıf istisnayı üst sınıftan sonra yakalamak derleme hatası verir
4. **throw ve throws'u karıştırmak:** throw istisna fırlatır, throws ise bildirim yapar
5. **try-with-resources kullanmamak:** Java 7+ projelerinde eski usul finally ile kaynak yönetimi gereksiz kod kalabalığı yaratır

---

## 8. TABLOLAR

### Tablo 1: Dosya Açma Modları Karşılaştırması
- **Sütunlar:** Mod, Sınıf, Amaç, Dosya Varsa, Dosya Yoksa, Örnek
- **Satırlar:** Okuma (FileReader), Yazma (FileWriter), Ekleme (FileWriter append), İkili Okuma (FileInputStream), İkili Yazma (FileOutputStream)

### Tablo 2: checked vs unchecked İstisnalar
- **Sütunlar:** Özellik, Checked Exception, Unchecked Exception
- **Satırlar:** Zorunlu yakalama, Miras aldığı sınıf, Örnekler, Ne zaman kullanılır

### Tablo 3: IO Sınıfları Karşılaştırması
- **Sütunlar:** Sınıf, Tür, Tamponlama, Metotlar, Kullanım Alanı
- **Satırlar:** FileReader, FileWriter, BufferedReader, BufferedWriter, PrintWriter, FileInputStream, FileOutputStream

### Tablo 4: try Çeşitleri
- **Sütunlar:** Özellik, Geleneksel try, try-with-resources
- **Satırlar:** Kaynak yönetimi, Kod uzunluğu, Java sürümü, finally ihtiyacı