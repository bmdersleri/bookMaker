Elbette, işte "Dosya İşlemleri ve Hata Yönetimi" bölümü için hazırladığım kendini değerlendirme soruları.

---

### Doğru/Yanlış Soruları

**Soru 1:** Java'da bir dosyadan veri okumak için `FileReader` sınıfı tek başına yeterlidir ve herhangi bir hata yönetimi gerektirmez.
- Cevap: Yanlış
- Açıklama: `FileReader` sınıfı, dosya bulunamazsa `FileNotFoundException` fırlatır, bu nedenle hata yönetimi (try-catch) zorunludur.

**Soru 2:** `finally` bloğu, bir hata oluşup oluşmadığına bakılmaksızın her zaman çalıştırılır.
- Cevap: Doğru
- Açıklama: `finally` bloğu, kaynakları serbest bırakmak gibi temizlik işlemleri için kullanılır ve her koşulda çalışır.

**Soru 3:** `try` bloğu içinde sadece bir tane `catch` bloğu kullanılabilir.
- Cevap: Yanlış
- Açıklama: Bir `try` bloğunu, farklı hata türlerini yakalamak için birden fazla `catch` bloğu takip edebilir.

**Soru 4:** Java'da bir metin dosyasına yazmak için `BufferedWriter` kullanmak, performansı artırabilir.
- Cevap: Doğru
- Açıklama: `BufferedWriter`, verileri bir tamponda biriktirip toplu olarak yazdığı için disk erişim sayısını azaltır ve performansı artırır.

**Soru 5:** `throws` anahtar kelimesi, bir hatayı oluşturmak (fırlatmak) için kullanılır.
- Cevap: Yanlış
- Açıklama: `throws` anahtar kelimesi, bir metodun belirli bir hatayı fırlatabileceğini bildirmek için kullanılır. Hatayı fırlatmak için `throw` kullanılır.

**Soru 6:** Bir dosyanın sonuna yeni veri eklemek (append) için `FileWriter` nesnesini oluştururken ikinci parametre olarak `true` değeri verilmelidir.
- Cevap: Doğru
- Açıklama: `new FileWriter("dosya.txt", true)` şeklinde oluşturulan `FileWriter`, dosyanın sonuna ekleme yapar.

**Soru 7:** `IOException`, Java'da işlenmesi zorunlu olmayan (unchecked) bir istisna sınıfıdır.
- Cevap: Yanlış
- Açıklama: `IOException` ve alt sınıfları, işlenmesi zorunlu (checked) istisnalardır. Derleyici, bu hataları ya `try-catch` ile yakalamamızı ya da `throws` ile bildirmemizi zorunlu kılar.

**Soru 8:** `Scanner` sınıfı sadece klavyeden veri okumak için kullanılır, dosya okumak için kullanılamaz.
- Cevap: Yanlış
- Açıklama: `Scanner` sınıfına bir `File` nesnesi vererek dosyadan da veri okunabilir.

### Boşluk Doldurma Soruları

**Soru 1:** Bir dosyayı satır satır okumak için `BufferedReader` ile birlikte kullanılan en uygun sınıf _________'dir.
- Cevap: FileReader
- Açıklama: `BufferedReader`, okuma performansını artırmak için bir `Reader` nesnesini (genelde `FileReader`) sarar.

**Soru 2:** Bir metodun hangi istisnaları fırlatabileceğini bildirmek için metod imzasında ________ anahtar kelimesi kullanılır.
- Cevap: throws
- Açıklama: `throws`, metodu çağıran kişiye bu hatayı yönetmesi gerektiğini bildirir.

**Soru 3:** Java 7 ile gelen ve otomatik kaynak yönetimi sağlayan try bloğuna ________ try bloğu denir.
- Cevap: try-with-resources
- Açıklama: Bu yapı, `AutoCloseable` arayüzünü uygulayan kaynakların (dosya, veritabanı bağlantısı gibi) otomatik olarak kapatılmasını sağlar.

**Soru 4:** Bir hatayı bilinçli olarak oluşturmak (fırlatmak) için ________ anahtar kelimesi kullanılır.
- Cevap: throw
- Açıklama: `throw` anahtar kelimesi, bir `Throwable` nesnesi (örneğin `new Exception()`) ile birlikte kullanılır.

**Soru 5:** Bir dosyaya yazma işlemi sırasında oluşabilecek hataları yakalamak için kullanılan en genel istisna sınıfı _________'tir.
- Cevap: IOException
- Açıklama: Dosya bulunamaması (`FileNotFoundException`), izin hatası gibi birçok dosya işlemi hatası `IOException`'ın alt sınıflarıdır.

**Soru 6:** Bir `File` nesnesinin bir dizin mi yoksa bir dosya mı olduğunu kontrol etmek için ________ metodu kullanılır.
- Cevap: isDirectory()
- Açıklama: `isDirectory()` metodu, `File` nesnesinin bir dizini temsil edip etmediğini `boolean` olarak döndürür.

**Soru 7:** Bir dosyadan okunan verileri geçici olarak hafızada tutarak daha büyük parçalar halinde okumayı sağlayan sınıf _________'dir.
- Cevap: BufferedReader
- Açıklama: `BufferedReader`, bir tampon (buffer) kullanarak okuma sayısını azaltır ve böylece performansı artırır.