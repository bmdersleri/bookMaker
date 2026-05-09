---
title: "Dosya Islemleri ve Hata Yonetimi"
subtitle: "Python Programlamaya Giris"
author: "Ismail Kirbas"
date: "2026"
lang: tr-TR
documentclass: report
toc: true
toc-depth: 3
numbersections: true
repo: bmdersleri
project-alias: javanintemelleri
chapter-alias: bolum-05
chapter_id: bolum-05
chapter_type: core
automation_profile: academic_technical_book_v1
numbering: auto
github_slug: bolum-05
qr_policy: dual_for_code_examples
asset_policy: manual_override
---
# Dosya İşlemleri ve Hata Yönetimi

## Bölüme Giriş

Bu bölümde, Java'da dosyalarla nasıl çalışacağınızı ve programınızın beklenmedik durumlarla (örneğin, bir dosyanın bulunamaması) nasıl başa çıkacağını öğreneceksiniz. Dosya işlemleri, verileri kalıcı olarak saklamak, yapılandırma dosyalarını okumak veya kullanıcıdan gelen verileri kaydetmek için olmazsa olmazdır. Hata yönetimi ise programınızın çökmesini engelleyerek daha sağlam ve güvenilir yazılımlar geliştirmenizi sağlar.

**Ön Bilgi:** Bu bölümü anlamak için temel Java sözdizimine (değişkenler, döngüler, koşullar) ve sınıf kavramına hakim olmanız beklenir.

**Öğrenme Çıktıları:**
Bu bölümü tamamladığınızda aşağıdakileri yapabiliyor olacaksınız:
1. `FileReader`, `FileWriter`, `BufferedReader`, `BufferedWriter` ve `PrintWriter` sınıflarını kullanarak metin dosyalarını okuyup yazabilmek.
2. `try-catch-finally` blokları ile istisnaları (exception) yakalayıp yönetebilmek.3.Checked(denetlenen) ve unchecked (denetlenmeyen) istisnalar arasındaki farkı açıklayabilmek.
4. `throw` anahtar kelimesiyle kendi istisnanızı fırlatabilmek ve `throws` ile bildirebilmek.
5. `Exception` sınıfından türeterek kendi özel istisna sınıflarınızı oluşturabilmek.
6. `try-with-resources` (Kaynakla Dene) yapısı ile kaynakları otomatik olarak yönetebilmek.
7. `File` sınıfını kullanarak dosya ve dizin bilgilerine erişebilmek.
8. Java NIO.2 kütüphanesi (`Path` ve `Files` sınıfları) ile daha modern ve esnek dosya işlemleri yapabilmek.


## 1. Dosya İşlemlerinin Temelleri

Bu bölümde, Java'nın en temel dosya okuma/yazma sınıflarını inceleyeceğiz.

### `FileReader` ve `FileWriter` ile Basit Dosya İşlemleri

#### 1. TANIM
`FileReader`, karakter tabanlı bir dosyayı okumak için kullanılan bir sınıftır. `FileWriter` ise karakter tabanlı bir dosyaya veri yazmak için kullanılır. İkisi de Java'nın `java.io` paketinin bir parçasıdır.

#### 2. NEDEN VAR?
Dosyalarla çalışmak, programın çalışması bittikten sonra da verilerin kalıcı olmasını sağlar. `FileReader` ve `FileWriter` olmasaydı, herhangi bir metin dosyasını okumak veya yazmak için işletim sistemi seviyesinde karmaşık işlemler yapmak zorunda kalırdık. Bu sınıflar, bu karmaşıklığı soyutlayarak bize basit bir arayüz sunar.

**Günlük Hayat Analojisi:** Bir kütüphanede kitap okumak gibidir. `FileReader`, kitabı (dosyayı) açıp sayfalarını (karakterleri) okumanızı sağlayan bir gözlük gibidir. `FileWriter` ise boş bir deftere (dosyaya) kalemle yazı yazmanızı sağlayan bir araçtır.

#### 3. NASIL KULLANILIR?
Aşağıdaki örnek, `ogrenciler.txt` adlı bir dosyayı okuyup konsola yazdırır.


```java
import java.io.FileReader;
import java.io.BufferedReader;
import java.io.IOException;

public class DosyaOkuyucu {
    public static void main(String[] args) {
        // Dosya yolunu ve BufferedReader referansını tanımlıyoruz
        String dosyaYolu = "ogrenciler.txt";
        BufferedReader okuyucu = null;

        try {
            // FileReader ile dosyayı açıyoruz
            FileReader fileReader = new FileReader(dosyaYolu);
            // BufferedReader ile okuma işlemini hızlandırıyoruz (tamponlama)
            okuyucu = new BufferedReader(fileReader);

            String satir;
            // readLine() metodu null dönene kadar satır satır okuyoruz
            while ((satir = okuyucu.readLine()) != null) {
                System.out.println(satir);
            }
        } catch (IOException e) {
            // Dosya bulunamazsa veya okuma hatası olursa bu blok çalışır
            System.err.println("Dosya okunurken bir hata oluştu: " + e.getMessage());
        } finally {
            // Kaynakları serbest bırakmak için finally bloğunu kullanıyoruz
            try {
                if (okuyucu != null) {
                    okuyucu.close(); // BufferedReader'ı kapatıyoruz
                }
            } catch (IOException ex) {
                System.err.println("Okuyucu kapatılırken hata oluştu: " + ex.getMessage());
            }
        }
    }
}
// Çıktı (ogrenciler.txt dosyasının içeriğine göre değişir):
// Ahmet Yılmaz, 101
// Ayşe Demir, 102
// Mehmet Kaya, 103
```


**Kod Açıklaması:**
* `FileReader fileReader = new FileReader(dosyaYolu);`: Belirtilen yoldaki dosyayı açar. Dosya yoksa `FileNotFoundException` (bir `IOException` alt türü) fırlatır.
* `BufferedReader okuyucu = new BufferedReader(fileReader);`: `FileReader`'ı bir `BufferedReader` ile sarar. Bu, okuma hızını artırır.
* `while ((satir = okuyucu.readLine())!= null)`: `readLine()` metodu bir sonraki satırı okur. Dosyanın sonuna gelindiğinde `null` döner.
* `catch (IOException e)`: Olası G/Ç (Giriş/Çıkış) hatalarını yakalar.
* `finally {… }`: İstisna olsun veya olmasın, her zaman çalışan bloktur. Burada dosyayı kapatmak için kullanılır.

#### 4. NE ZAMAN TERCİH EDİLİR?
`FileReader` ve `FileWriter` küçük boyutlu metin dosyalarıyla çalışırken veya hızlı bir prototip oluştururken idealdir. Ancak, büyük dosyalar için performans sorunları yaşanabilir.

#### 5. ALTERNATİFLERİ
| Sınıf | Açıklama | Ne Zaman Kullanılır? |
|:--- |:--- |:--- |
| `FileReader`/`FileWriter` | Karakter tabanlı, basit okuma/yazma. | Küçük metin dosyaları. |
| `BufferedReader`/`BufferedWriter` | Tamponlama ile performansı artırır. | Büyük metin dosyaları, satır satır işleme. |
| `Scanner` | Metin ayrıştırma (parsing) için idealdir. | Dosyadan belirli bir formatta (örneğin CSV) veri okuma. |
| `PrintWriter` | Biçimlendirilmiş çıktı için kullanılır. | Dosyaya `printf()` benzeri formatlı veri yazma. |

#### 6. YAYGIN HATALAR
* **Hata:** Dosyanın var olduğundan emin olmadan `FileReader` ile açmaya çalışmak.
  * **Çözüm:** Dosyayı açmadan önce `File` sınıfının `exists()` metodunu kullanarak dosyanın varlığını kontrol edin.
* **Hata:** `finally` bloğunda dosyayı kapatmayı unutmak. Bu, kaynak sızıntısına (resource leak) neden olur.
  * **Çözüm:** Java 7 ve sonrasında `try-with-resources` yapısını kullanın. (Bkz. Bölüm 2.4)


### `BufferedReader` ve `BufferedWriter` ile Performanslı İşlemler

#### 1. TANIM
`BufferedReader` ve `BufferedWriter`, karakter akışlarına bir tampon (buffer) ekleyerek okuma ve yazma işlemlerinin verimliliğini artıran sarmalayıcı (wrapper) sınıflardır. `BufferedReader` `readLine()` metodu ile satır satır okuma yaparken, `BufferedWriter` `newLine()` metodu ile platformdan bağımsız satır sonu karakteri ekler.

#### 2. NEDEN VAR?
Her bir karakter okuma/yazma işlemi, işletim sistemine bir çağrı yapılmasını gerektirir. Bu çağrılar, özellikle büyük dosyalar için çok maliyetlidir. Tamponlama, verileri bir kerede büyük bir blok halinde okuyarak/yazarak bu sistem çağrılarının sayısını önemli ölçüde azaltır ve performansı artırır.

**Günlük Hayat Analojisi:** Bir markete tek tek ürün almaya gitmek (tamponsuz okuma) ile haftalık alışverişi bir kerede yapmak (tamponlu okuma) arasındaki fark gibidir. Tamponlu yöntem çok daha verimlidir.

#### 3. NASIL KULLANILIR?
Aşağıdaki örnek, `kaynak.txt` dosyasını okuyup her satırın başına bir sıra numarası ekleyerek `hedef.txt` dosyasına yazar.


```java
import java.io.*;

public class TamponluDosyaKopyalama {
    public static void main(String[] args) {
        String kaynakDosya = "kaynak.txt";
        String hedefDosya = "hedef.txt";

        // try-with-resources ile kaynaklar otomatik kapatılır
        try (BufferedReader okuyucu = new BufferedReader(new FileReader(kaynakDosya));
             BufferedWriter yazici = new BufferedWriter(new FileWriter(hedefDosya))) {

            String satir;
            int satirNumarasi = 1;
            // Dosya sonuna kadar satır satır oku
            while ((satir = okuyucu.readLine()) != null) {
                // Satır numarası ve iki nokta ekleyerek hedef dosyaya yaz
                yazici.write(satirNumarasi + ": " + satir);
                yazici.newLine(); // Platformdan bağımsız yeni satır ekle
                satirNumarasi++;
            }
            System.out.println("Dosya başarıyla kopyalandı.");
        } catch (IOException e) {
            System.err.println("Dosya işlemi sırasında hata: " + e.getMessage());
        }
    }
}
// Çıktı (hedef.txt dosyası):
// 1: kaynak.txt'nin ilk satırı
// 2: kaynak.txt'nin ikinci satırı
```


**Kod Açıklaması:**
* `try (BufferedReader okuyucu =…; BufferedWriter yazici =…)`: Bu, `try-with-resources` yapısıdır. Parantez içinde tanımlanan kaynaklar (`BufferedReader` ve `BufferedWriter`), `try` bloğu bittiğinde otomatik olarak kapatılır. Artık `finally` bloğuna gerek kalmaz.
* `yazici.write(satirNumarasi + ": " + satir);`: `write()` metodu ile bir metin parçası dosyaya yazılır.
* `yazici.newLine();`: İşletim sistemine göre uygun satır sonu karakterini (Windows'ta `\r\n`, Linux'ta `\n`) ekler.

#### 4. NE ZAMAN TERCİH EDİLİR?
Her zaman `FileReader` veya `FileWriter` yerine `BufferedReader` veya `BufferedWriter` kullanmak daha iyi bir performans sağlar. Özellikle büyük dosyalar (birkaç MB'den büyük) veya ağ üzerinden dosya okuma gibi G/Ç yoğun işlemlerde tercih edilmelidir.

#### 5. ALTERNATİFLERİ
* **`Scanner`**: Metin ayrıştırma için daha uygundur ancak `BufferedReader`'dan daha yavaştır.
* **`Files.newBufferedReader()` (NIO.2)**: Daha modern ve kullanımı kolay bir alternatiftir.

#### 6. YAYGIN HATALAR
* **Hata:** `BufferedWriter`'ı oluştururken, yazılacak dosyanın üzerine yazılmasını istemediğiniz halde varsayılan olarak dosyayı sıfırlaması (`FileWriter`'ın varsayılan davranışı).
  * **Çözüm:** `FileWriter`'ın ikinci parametresine `true` değerini vererek ekleme (append) modunda açın: `new FileWriter("dosya.txt", true)`.


## 2. Hata Yönetimi (Exception Handling)

Hata yönetimi, profesyonel Java programlamanın en kritik konularından biridir.

### `try-catch-finally` Blokları

#### 1. TANIM
`try-catch-finally` yapısı, çalışma zamanında (runtime) oluşabilecek hataları (istisnaları) yakalamak ve programın çökmesini engellemek için kullanılan bir mekanizmadır.

#### 2. NEDEN VAR?
Bir program çalışırken bir dosyanın silinmesi, ağ bağlantısının kopması veya geçersiz bir kullanıcı girişi gibi birçok beklenmedik durumla karşılaşabilir. Bu durumlar için önlem alınmazsa program aniden sonlanır ve kullanıcıya anlamsız hata mesajları gösterir. `try-catch-finally` bu hataları yönetmemizi sağlar.

**Günlük Hayat Analojisi:** Bir yemek tarifi uyguluyorsunuz. Tarifin bir adımında "fırını 180 dereceye ayarla" yazar (`try` bloğu). Fırın bozuksa ve ısınmıyorsa, bu bir hatadır (`catch` bloğu). Bu durumda "Fırın arızalı, tamir çağır" gibi bir mesaj gösterirsiniz. Ne olursa olsun, son adımda "fırını kapat" (`finally` bloğu) işlemini yaparsınız.

#### 3. NASIL KULLANILIR?


```java
import java.io.FileReader;
import java.io.IOException;

public class TryCatchFinallyOrnegi {
    public static void main(String[] args) {
        FileReader okuyucu = null;
        try {
            // Hata oluşma potansiyeli olan kod
            okuyucu = new FileReader("varolmayan_dosya.txt");
            int karakter = okuyucu.read();
            System.out.println("Okunan karakter: " + (char) karakter);
        } catch (IOException e) {
            // try bloğunda IOException oluşursa bu blok çalışır
            System.err.println("Dosya okuma hatası: " + e.getMessage());
        } finally {
            // Her durumda (hata olsa da olmasa da) çalışan blok
            try {
                if (okuyucu != null) {
                    okuyucu.close();
                    System.out.println("Dosya başarıyla kapatıldı.");
                }
            } catch (IOException e) {
                System.err.println("Dosya kapatılırken hata: " + e.getMessage());
            }
        }
    }
}
// Çıktı:
// Dosya okuma hatası: varolmayan_dosya.txt (No such file or directory)
// Dosya başarıyla kapatıldı.
```


**Kod Açıklaması:**
1. **`try` bloğu:** İstisna fırlatma potansiyeli olan kod bu bloğa yazılır.
2. **`catch` bloğu:** `try` bloğunda belirtilen türden bir istisna oluşursa, bu blok çalışır. Birden fazla `catch` bloğu olabilir.
3. **`finally` bloğu:** İsteğe bağlıdır. İstisna oluşup oluşmadığına bakılmaksızın her zaman çalışır. Genellikle dosya, ağ bağlantısı gibi kaynakları kapatmak için kullanılır.

#### 4. NE ZAMAN TERCİH EDİLİR?
Bir kaynağı (dosya, veritabanı bağlantısı, ağ soketi) manuel olarak yönetmeniz gerektiğinde ve kaynağı serbest bırakma işleminin her koşulda gerçekleşmesi gerektiğinde `finally` bloğu kullanılır. Ancak Java 7'den beri `try-with-resources` bu durumu büyük ölçüde basitleştirmiştir.

#### 5. ALTERNATİFLERİ
* **`try-with-resources`**: `AutoCloseable` arayüzünü uygulayan kaynaklar için `finally` bloğuna olan ihtiyacı ortadan kaldırır.
* **`throws` anahtar kelimesi**: Metot, istisnayı kendisi yakalamak yerine çağıran metoda fırlatabilir.

#### 6. YAYGIN HATALAR
* **Hata:** Boş bir `catch` bloğu yazmak (hata mesajını yazdırmamak veya loglamamak). Bu, hatayı gizler ve hata ayıklamayı çok zorlaştırır.
  * **Çözüm:** Her `catch` bloğunda en azından hatayı konsola yazdırın (`e.printStackTrace()` veya `System.err.println(e.getMessage())`).


### Checked vs Unchecked İstisnalar

#### 1. TANIM
Java'da istisnalar iki ana kategoriye ayrılır: **Checked (Denetlenen)** ve **Unchecked (Denetlenmeyen)**. Checked istisnalar derleme zamanında kontrol edilirken, unchecked istisnalar çalışma zamanında kontrol edilir.

#### 2. NEDEN VAR?
Bu ayrım, programcıyı belirli hata türlerini ele almaya zorlamak için yapılmıştır. Örneğin, bir dosyayı açarken `FileNotFoundException` oluşabileceği çok açıktır. Checked istisna olması, programcının bu durumu ele almasını (try-catch veya throws ile) garanti eder. Unchecked istisnalar ise genellikle programlama hatalarından kaynaklanır (null pointer, dizinin sınırlarını aşma gibi) ve bunları ele almaya zorlamak anlamsızdır, çünkü kodun düzeltilmesi gerekir.

**Günlük Hayat Analojisi:**
* **Checked (Denetlenen):** Araba kullanmak için ehliyet almak zorunda olmanız gibidir. Bu, yasal ve beklenen bir zorunluluktur.
* **Unchecked (Denetlenmeyen):** Araba kullanırken aniden frene basmanız gerekmesi gibidir. Bu beklenmedik bir durumdur ve sürücünün refleksine bağlıdır.

#### 3. NASIL KULLANILIR?


```java
import java.io.*;

public class CheckedUncheckedOrnegi {

    // Checked istisna: IOException'i ele almak ZORUNDAYIZ
    public static void checkedIstisnaOrnegi() throws IOException {
        FileReader reader = new FileReader("dosya.txt"); // FileNotFoundException fırlatabilir
        reader.close();
    }

    // Unchecked istisna: ArithmeticException'i ele almak ZORUNDA DEĞİLİZ
    public static void uncheckedIstisnaOrnegi() {
        int sonuc = 10 / 0; // ArithmeticException fırlatır (RuntimeException alt sınıfı)
        System.out.println(sonuc);
    }

    public static void main(String[] args) {
        // Checked istisnayı ele almak için try-catch veya throws kullanmalıyız
        try {
            checkedIstisnaOrnegi();
        } catch (IOException e) {
            System.err.println("Checked istisna yakalandı: " + e.getMessage());
        }

        // Unchecked istisnayı ele almak zorunda değiliz ama program çöker.
        // Bu yüzden genellikle onları da try-catch ile yakalarız.
        try {
            uncheckedIstisnaOrnegi();
        } catch (ArithmeticException e) {
            System.err.println("Unchecked istisna yakalandı: " + e.getMessage());
        }
    }
}
// Çıktı:
// Checked istisna yakalandı: dosya.txt (No such file or directory)
// Unchecked istisna yakalandı: / by zero
```


**Kod Açıklaması:**
* `checkedIstisnaOrnegi()` metodu `throws IOException` ile bir checked istisna fırlatabileceğini bildirir. Bu metodu çağıran kod ya bu istisnayı `try-catch` ile yakalamalı ya da kendisi `throws IOException` ile bildirmelidir.
* `uncheckedIstisnaOrnegi()` metodu bir `ArithmeticException` (RuntimeException'ın alt sınıfı) fırlatır. Bu metodu çağıran kodun bu istisnayı yakalaması zorunlu değildir. Eğer yakalanmazsa program çöker.

#### 4. NE ZAMAN TERCİH EDİLİR?
* **Checked İstisnalar:** Harici bir kaynağa (dosya, ağ, veritabanı) erişirken, kullanıcının yapabileceği hataları (yanlış dosya adı) veya sistem kaynaklı sorunları temsil eder. Programcının bu durumlara karşı bir önlem alması beklenir.
* **Unchecked İstisnalar:** Genellikle programlama hatalarıdır (`NullPointerException`, `ArrayIndexOutOfBoundsException`, `IllegalArgumentException`). Bunların kaynağı genellikle kodun kendisidir ve düzeltilmelidir.

#### 5. ALTERNATİFLERİ
Bu bir sınıflandırmadır, alternatifi yoktur. Ancak kendi özel istisna sınıflarınızı oluştururken, hata türüne göre `Exception` (checked) veya `RuntimeException` (unchecked) sınıflarından birini miras almayı seçebilirsiniz.

#### 6. YAYGIN HATALAR
* **Hata:** Bir metot içinde checked bir istisnayı yakalayıp hiçbir şey yapmadan yutmak (örneğin, boş bir `catch` bloğu).
  * **Çözüm:** Hatayı en azından loglayın. Eğer hatayı bu seviyede çözemiyorsanız, istisnayı tekrar fırlatın (`throw e;`) veya uygun bir unchecked istisnaya sararak fırlatın (`throw new RuntimeException(e);`).


### `throw` ve `throws` Anahtar Kelimeleri

#### 1. TANIM
`throw` anahtar kelimesi, bir istisna nesnesini manuel olarak fırlatmak için kullanılır. `throws` anahtar kelimesi ise bir metodun hangi checked istisnaları fırlatabileceğini bildirmek için metot imzasında kullanılır.

#### 2. NEDEN VAR?
Her zaman hazır Java istisnaları yeterli olmayabilir. Örneğin, bir dosya adının belirli bir formatta olmasını istiyorsanız ve kullanıcı geçersiz bir ad girerse, kendi özel hata durumunuzu yaratmak için `throw` kullanırsınız. `throws` ise, bir metodun içinde oluşan bir checked istisnayı kendisinin yakalamak yerine, onu çağıran metoda bildirmesini sağlar. Bu, sorumluluğu üst seviyeye devretmek gibidir.

**Günlük Hayat Analojisi:**
* `throw`: Bir restoranda garson yemeğinize yabancı bir cisim karıştığını fark eder ve hemen şefi çağırır (istisnayı fırlatır).
* `throws`: Bir bürokrata bir evrak verirsiniz. O, evrakı inceler, bir sorun görürse "Bu evrakı müdürüm imzalamalı" der (sorumluluğu bir üst seviyeye atar).

#### 3. NASIL KULLANILIR?


```java
import java.io.*;

public class ThrowThrowsOrnegi {

    // throws ile bu metodun checked bir istisna (IOException) fırlatabileceğini bildiriyoruz
    public static void dosyaOku(String dosyaAdi) throws IOException {
        if (dosyaAdi == null || dosyaAdi.isEmpty()) {
            // throw ile manuel olarak bir istisna fırlatıyoruz
            throw new IllegalArgumentException("Dosya adı geçersiz!");
        }

        FileReader reader = new FileReader(dosyaAdi);
        BufferedReader bufferedReader = new BufferedReader(reader);
        System.out.println(bufferedReader.readLine());
        bufferedReader.close();
    }

    public static void main(String[] args) {
        try {
            dosyaOku(""); // Geçersiz dosya adı
        } catch (IllegalArgumentException e) {
            System.err.println("Hata: " + e.getMessage());
        } catch (IOException e) {
            System.err.println("Dosya okuma hatası: " + e.getMessage());
        }
    }
}
// Çıktı:
// Hata: Dosya adı geçersiz!
```


**Kod Açıklaması:**
* `public static void dosyaOku(String dosyaAdi) throws IOException`: Metot, `FileReader`'ın fırlatabileceği `FileNotFoundException` (bir `IOException`) dışında, kendisi de `IllegalArgumentException` fırlatabilir. `IllegalArgumentException` unchecked olduğu için `throws` ile bildirilmesine gerek yoktur.
* `throw new IllegalArgumentException("Dosya adı geçersiz!");`: Bu satır, bir `IllegalArgumentException` nesnesi oluşturur ve onu fırlatır. Bu, metodun akışını durdurur ve uygun `catch` bloğuna gidilmesini sağlar.

#### 4. NE ZAMAN TERCİH EDİLİR?
* `throw`: Bir metot, iş mantığı gereği bir hata durumuyla karşılaştığında (örneğin, geçersiz parametre, yetersiz bakiye) kullanılır.
* `throws`: Bir metot, kendi içinde checked bir istisnayı ele almak istemiyorsa ve bu sorumluluğu çağıran metoda bırakmak istiyorsa kullanılır.

#### 5. ALTERNATİFLERİ
`throw` ve `throws`'un doğrudan alternatifleri yoktur, bunlar temel dil yapılarıdır. Ancak, bir hatayı fırlatmak yerine, hata durumunu temsil eden özel bir dönüş değeri (null, -1 gibi) kullanmak da bir alternatiftir. Ancak bu, hata yönetimini zorlaştırabilir ve "null pointer" gibi başka hatalara yol açabilir.

#### 6. YAYGIN HATALAR
* **Hata:** `throws` ile bildirilen bir checked istisnayı, metodu çağıran yerde yakalamamak veya bildirmemek.
  * **Çözüm:** Derleme hatası alırsınız. Metodu çağıran kodun ya `try-catch` ile istisnayı yakalaması ya da kendisinin `throws` ile bildirmesi gerekir.
* **Hata:** Bir checked istisnayı `try-catch` ile yakalayıp, yakalanan istisnayı hiçbir işlem yapmadan tekrar fırlatmak (`throw e;`). Bu, genellikle anlamsızdır ve hatayı loglamak gibi bir işlem yapılmadıysa hatayı gizler.


### `try-with-resources` (Kaynakla Dene)

#### 1. TANIM
Java 7 ile gelen `try-with-resources` yapısı, `AutoCloseable` arayüzünü uygulayan kaynakların (dosya, veritabanı bağlantısı, ağ soketi) otomatik olarak kapatılmasını sağlar. Bu, `finally` bloğuna olan ihtiyacı ortadan kaldırır ve kodu daha okunabilir ve güvenli hale getirir.

#### 2. NEDEN VAR?
`finally` bloğunda kaynakları kapatmak, özellikle birden fazla kaynakla çalışırken hataya açıktır. Kapatma işleminin unutulması kaynak sızıntısına (resource leak) neden olur. `try-with-resources`, bu sorunu otomatik olarak çözer. Kaynaklar, `try` bloğu sona erdiğinde (normal veya istisna ile) otomatik olarak `close()` metodu çağrılarak kapatılır.

**Günlük Hayat Analojisi:** Bir otel odası kiraladığınızda, odadan çıkarken anahtarı resepsiyona teslim etmeniz gerekir (`finally`). `try-with-resources` ise, odadan çıktığınızda anahtarın otomatik olarak bir robota teslim edilmesi gibidir. Sizin hatırlamanıza gerek kalmaz.

#### 3. NASIL KULLANILIR?


```java
import java.io.*;

public class TryWithResourcesOrnegi {
    public static void main(String[] args) {
        // Kaynaklar try anahtar kelimesinden sonra parantez içinde tanımlanır
        try (BufferedReader okuyucu = new BufferedReader(new FileReader("girdi.txt"));
             BufferedWriter yazici = new BufferedWriter(new FileWriter("cikti.txt"))) {

            String satir;
            while ((satir = okuyucu.readLine()) != null) {
                yazici.write(satir);
                yazici.newLine();
            }
            System.out.println("Dosya başarıyla kopyalandı.");
        } catch (IOException e) {
            // try bloğunda veya kaynak kapatılırken oluşan hatalar burada yakalanır
            System.err.println("Hata oluştu: " + e.getMessage());
        }
        // finally bloğuna gerek yok! okuyucu ve yazici otomatik kapatıldı.
    }
}
```


**Kod Açıklaması:**
* `try (BufferedReader okuyucu = new BufferedReader(…); BufferedWriter yazici = new BufferedWriter(…))`: Birden fazla kaynak noktalı virgül (`;`) ile ayrılarak tanımlanabilir.
* Tanımlanan tüm kaynaklar (`BufferedReader` ve `BufferedWriter`), `try` bloğu bittiğinde (blok normal sonlansa veya bir istisna fırlatılsa bile) `close()` metotları otomatik olarak çağrılarak kapat

ıldı.

**Kod Açıklaması (Devam):**
* `catch (IOException e)`: Eğer okuma, yazma veya kaynakların kapatılması sırasında bir hata oluşursa bu blok çalışır.
* `// finally bloğuna gerek yok!`: `try-with-resources` sayesinde `finally` bloğu ihtiyacı tamamen ortadan kalkar.

#### 4. NE ZAMAN TERCİH EDİLİR?
* **`try-with-resources` tercih edilir:** `AutoCloseable` arayüzünü uygulayan herhangi bir kaynak (dosya, veritabanı bağlantısı, ağ soketi) ile çalışırken her zaman tercih edilmelidir. Kodun daha kısa, okunabilir ve güvenli olmasını sağlar.
* **`try-catch-finally` tercih edilir:** Kaynak kapatma işleminin özel bir mantığa ihtiyacı varsa veya Java 7 öncesi bir sürümle çalışmanız gerekiyorsa.

#### 5. ALTERNATİFLERİ

| Özellik | `try-with-resources` (Java 7+) | `try-catch-finally` |
|:--- |:--- |:--- |
| **Kaynak Yönetimi** | Otomatik (`AutoCloseable` ile) | Manuel (`finally` bloğunda `close()`) |
| **Kod Karmaşıklığı** | Düşük (kısa ve öz) | Yüksek (iç içe bloklar) |
| **Hata Riski** | Kaynak sızıntısı riski çok düşük | Kaynak sızıntısı riski yüksek (unutulabilir) |
| **Okunabilirlik** | Yüksek | Düşük |
| **Kullanım Alanı** | Java 7 ve sonrası | Java 6 ve öncesi, özel kapatma mantığı |

#### 6. YAYGIN HATALAR
* **Hata:** `try-with-resources` bloğunda tanımlanan kaynağı `catch` veya `finally` bloğu içinde kullanmaya çalışmak.
  * **Çözüm:** Kaynak, `try` bloğunun kapsamı (scope) içindedir. Blok dışında kullanılamaz. Eğer kaynağa blok dışında da ihtiyacınız varsa, geleneksel `try-catch-finally` yapısını kullanmalısınız.
* **Hata:** `try-with-resources` içinde tanımlanan kaynağın referansını `final` veya effectively final olarak düşünmemek. (Aslında bu bir hata değil, bilinmesi gereken bir detaydır. Kaynak değişkeni blok içinde değiştirilemez.)


### `throw` Anahtar Kelimesi

#### 1. TANIM
`throw` anahtar kelimesi, bir istisna nesnesini manuel olarak fırlatmak için kullanılır. Program akışını bilinçli olarak kesmek ve hatayı çağrı yapan metoda bildirmek istediğimizde kullanırız.

#### 2. NEDEN VAR?
Bazen Java'nın otomatik olarak fırlattığı istisnalar yeterli olmayabilir. Örneğin, bir dosyanın adı geçersiz karakterler içeriyorsa, bu durumu özel bir istisna ile bildirmek isteyebiliriz. `throw` sayesinde kendi hata durumlarımızı tanımlayabilir ve yönetebiliriz.

**Günlük Hayat Analojisi:** Bir fabrikada kalite kontrol elemanısınız. Ürün hatalıysa, onu banttan alıp "Hatalı Ürün" etiketiyle özel bir kutuya atarsınız. Bu, `throw` ile istisna fırlatmaya benzer.

#### 3. NASIL KULLANILIR?


```java
import java.io.*;

public class ThrowOrnegi {
    // Dosya adını kontrol eden bir metot
    public static void dosyaAdiniKontrolEt(String dosyaAdi) throws IllegalArgumentException {
        // Dosya adı null veya boş ise özel bir hata fırlat
        if (dosyaAdi == null || dosyaAdi.isEmpty()) {
            throw new IllegalArgumentException("Dosya adı boş olamaz!"); // İstisna fırlatılıyor
        }
        // Dosya adı geçersiz karakter içeriyorsa (örneğin: / \ : * ? " < > |)
        if (dosyaAdi.contains(":") || dosyaAdi.contains("*")) {
            throw new IllegalArgumentException("Dosya adı geçersiz karakterler içeriyor!");
        }
        System.out.println("Dosya adı geçerli: " + dosyaAdi);
    }

    public static void main(String[] args) {
        try {
            dosyaAdiniKontrolEt("test*.txt"); // Bu satır hata fırlatacak
        } catch (IllegalArgumentException e) {
            System.err.println("Hata: " + e.getMessage());
        }

        try {
            dosyaAdiniKontrolEt("girdi.txt"); // Bu satır başarılı olacak
        } catch (IllegalArgumentException e) {
            System.err.println("Hata: " + e.getMessage());
        }
    }
}
// Çıktı:
// Hata: Dosya adı geçersiz karakterler içeriyor!
// Dosya adı geçerli: girdi.txt
```


**Kod Açıklaması:**
* `throw new IllegalArgumentException(…)`: `throw` ile `IllegalArgumentException` türünde yeni bir istisna nesnesi oluşturup fırlatıyoruz.
* `throws IllegalArgumentException`: Metot imzasında, bu metodun `IllegalArgumentException` fırlatabileceğini bildiriyoruz. (Unchecked olduğu için zorunlu değil, ancak iyi bir pratiktir.)
* Çağrı yapan kod (`main` metodu), bu istisnayı `try-catch` ile yakalıyor.

#### 4. NE ZAMAN TERCİH EDİLİR?
* **`throw` tercih edilir:** Bir metodun girdi parametrelerinin geçerliliğini kontrol ederken (validation), iş mantığı gereği belirli bir durumda işlemin devam etmemesi gerektiğinde veya kendi özel istisna sınıflarınızı fırlatmak istediğinizde.
* **Alternatif:** Bir hata durumunda `return` ile özel bir değer döndürmek (örneğin `-1` veya `null`). Ancak bu, hata yönetimini zorlaştırır ve hata ayıklamayı güçleştirir.

#### 5. ALTERNATİFLERİ
`throw`'un alternatifi, hata durumunda özel bir dönüş değeri kullanmaktır. Ancak bu yöntem, istisna mekanizmasının sağladığı avantajları (hata ayıklama bilgisi, çağrı zincirinin korunması) sunmaz.

#### 6. YAYGIN HATALAR
* **Hata:** `throw` ile fırlatılan istisnayı yakalamamak veya bildirmemek (checked istisnalar için).
  * **Çözüm:** Checked bir istisna fırlatıyorsanız, ya metot imzasına `throws` ekleyin ya da `try-catch` ile yakalayın.
* **Hata:** Bir `catch` bloğu içinde yakalanan istisnayı hiçbir işlem yapmadan tekrar fırlatmak (`throw e;`). Bu genellikle anlamsızdır ve hatayı gizler.


### Özel İstisna Sınıfları (Custom Exceptions)

#### 1. TANIM
Java'da `Exception` sınıfından veya onun alt sınıflarından türeterek oluşturduğumuz, uygulamaya özgü hata durumlarını temsil eden sınıflardır. Bu sayede hataları daha anlamlı ve spesifik hale getirebiliriz.

#### 2. NEDEN VAR?
Java'nın standart istisna sınıfları (örneğin `IOException`, `IllegalArgumentException`) genel amaçlıdır. Bir uygulamada "Dosya bulunamadı" hatası ile "Dosya adı çok uzun" hatasını ayırt etmek için özel sınıflar oluşturmak, hata yönetimini daha net ve okunabilir kılar.

**Günlük Hayat Analojisi:** Bir hastanede "Hasta" sınıfından türeyen "KardiyolojiHastasi", "OrtopediHastasi" gibi alt sınıflar oluşturmak gibidir. Her hasta bir hastadır, ancak uzmanlık alanına göre daha spesifik bilgiler taşır.

#### 3. NASIL KULLANILIR?


```java
import java.io.*;

// Özel istisna sınıfımız
class GecersizDosyaAdiException extends Exception {
    // Yapıcı metot, hata mesajını alır
    public GecersizDosyaAdiException(String mesaj) {
        super(mesaj); // Üst sınıfın (Exception) yapıcısını çağır
    }

    // İsteğe bağlı: Hata kodu gibi ek bilgiler tutabilir
    public GecersizDosyaAdiException(String mesaj, int hataKodu) {
        super(mesaj);
        this.hataKodu = hataKodu;
    }

    private int hataKodu;

    public int getHataKodu() {
        return hataKodu;
    }
}

public class OzelIstisnaOrnegi {
    public static void dosyaIsle(String dosyaAdi) throws GecersizDosyaAdiException {
        if (dosyaAdi == null || dosyaAdi.isEmpty()) {
            throw new GecersizDosyaAdiException("Dosya adı boş olamaz!", 1001);
        }
        if (dosyaAdi.length() > 100) {
            throw new GecersizDosyaAdiException("Dosya adı çok uzun!", 1002);
        }
        System.out.println("Dosya işleniyor: " + dosyaAdi);
    }

    public static void main(String[] args) {
        try {
            dosyaIsle(""); // Boş dosya adı
        } catch (GecersizDosyaAdiException e) {
            System.err.println("Hata Kodu: " + e.getHataKodu() + " - " + e.getMessage());
        }

        try {
            dosyaIsle("gecerliDosya.txt"); // Geçerli dosya adı
        } catch (GecersizDosyaAdiException e) {
            System.err.println("Hata Kodu: " + e.getHataKodu() + " - " + e.getMessage());
        }
    }
}
// Çıktı:
// Hata Kodu: 1001 - Dosya adı boş olamaz!
// Dosya işleniyor: gecerliDosya.txt
```


**Kod Açıklaması:**
* `class GecersizDosyaAdiException extends Exception`: Özel istisna sınıfımızı `Exception` sınıfından türetiyoruz. Bu, onu bir **checked** istisna yapar.
* `super(mesaj)`: Üst sınıfın (`Exception`) yapıcı metoduna hata mesajını iletiyoruz.
* `hataKodu`: İsteğe bağlı olarak, hata ile ilgili ek bilgiler (örneğin bir hata kodu) tutabiliriz.
* `throw new GecersizDosyaAdiException(…)`: Özel istisnamızı `throw` ile fırlatıyoruz.

#### 4. NE ZAMAN TERCİH EDİLİR?
* **Özel istisna sınıfları tercih edilir:** Uygulamanızın iş mantığına özgü, birden fazla farklı hata durumu olduğunda ve bu hataları birbirinden ayırt etmeniz gerektiğinde.
* **Standart istisnalar tercih edilir:** Hata durumu Java'nın standart sınıflarından biriyle tam olarak ifade edilebiliyorsa (örneğin, geçersiz bir argüman için `IllegalArgumentException`).

#### 5. ALTERNATİFLERİ

| Özellik | Özel İstisna Sınıfı | Standart İstisna Sınıfı |
|:--- |:--- |:--- |
| **Spesifiklik** | Yüksek (uygulamaya özgü) | Düşük (genel amaçlı) |
| **Okunabilirlik** | Hata türü hemen anlaşılır | Hata türü yorum gerektirebilir |
| **Ek Bilgi** | Hata kodu, zaman damgası gibi ek alanlar eklenebilir | Genellikle sadece mesaj içerir |
| **Karmaşıklık** | Yeni bir sınıf oluşturmayı gerektirir | Hazır olarak gelir, ek kod yazılmaz |

#### 6. YAYGIN HATALAR
* **Hata:** Çok fazla sayıda özel istisna sınıfı oluşturmak. Bu, kodun gereksiz yere karmaşıklaşmasına neden olur.
  * **Çözüm:** Yalnızca gerçekten gerekli olduğunda ve hata durumları arasında anlamlı bir fark olduğunda özel istisna sınıfları oluşturun.
* **Hata:** Özel istisna sınıfını `RuntimeException` yerine `Exception`'dan türetmek. Bu, onu checked bir istisna yapar ve her kullanıldığı yerde `try-catch` veya `throws` eklenmesini zorunlu kılar. Eğer hatanın yakalanması zorunlu değilse, `RuntimeException`'dan türetmek daha uygun olabilir.


## 3. DOSYA İŞLEMLERİ İÇİN TEMEL SINIFLAR

### `FileReader` ve `FileWriter`

#### 1. TANIM
`FileReader` ve `FileWriter`, sırasıyla karakter tabanlı dosyaları okumak ve yazmak için kullanılan temel sınıflardır. Karakter akışları (character streams) ile çalışırlar, bu nedenle metin dosyaları (.txt,.csv) için idealdirler.

#### 2. NEDEN VAR?
Dosyalarla çalışmanın en temel yoludur. Bayt tabanlı akışların (InputStream/OutputStream) aksine, karakter kodlamasını (encoding) otomatik olarak hallederler. Bu sayede Türkçe karakterler gibi özel karakterlerin doğru okunup yazılmasını sağlarlar.

**Günlük Hayat Analojisi:** Bir kitap okuyucusu (`FileReader`) ve bir yazar (`FileWriter`) gibidir. Okuyucu, kitabı sayfa sayfa okur; yazar ise kitaba sayfa sayfa yazar.

#### 3. NASIL KULLANILIR?


```java
import java.io.*;

public class FileReaderWriterOrnegi {
    public static void main(String[] args) {
        // Kaynak ve hedef dosya yolları
        String kaynakDosya = "kaynak.txt";
        String hedefDosya = "hedef.txt";

        // try-with-resources ile kaynakları otomatik yönet
        try (FileReader okuyucu = new FileReader(kaynakDosya);
             FileWriter yazici = new FileWriter(hedefDosya)) {

            int karakter; // read() metodu int döndürür
            // Dosyanın sonuna gelene kadar (read() -1 dönene kadar) oku
            while ((karakter = okuyucu.read()) != -1) {
                yazici.write(karakter); // Okunan karakteri hedef dosyaya yaz
            }
            System.out.println("Dosya başarıyla kopyalandı.");
        } catch (FileNotFoundException e) {
            System.err.println("Dosya bulunamadı: " + e.getMessage());
        } catch (IOException e) {
            System.err.println("Okuma/Yazma hatası: " + e.getMessage());
        }
    }
}
```


**Kod Açıklaması:**
* `FileReader okuyucu = new FileReader(kaynakDosya)`: Okunacak dosyayı belirtiyoruz.
* `FileWriter yazici = new FileWriter(hedefDosya)`: Yazılacak dosyayı belirtiyoruz. Eğer dosya yoksa oluşturulur, varsa üzerine yazılır.
* `okuyucu.read()`: Dosyadan bir sonraki karakteri okur. Karakterin int değerini döndürür. Dosya sonunda -1 döndürür.
* `yazici.write(karakter)`: Okunan karakteri hedef dosyaya yazar.

#### 4. NE ZAMAN TERCİH EDİLİR?
* **`FileReader`/`FileWriter` tercih edilir:** Küçük boyutlu metin dosyalarıyla çalışırken, karakter karakter okuma/yazma işlemi yeterli olduğunda.
* **`BufferedReader`/`BufferedWriter` tercih edilir:** Büyük dosyalarla çalışırken veya satır satır okuma/yazma yapmak istediğinizde (performans kritik olduğunda).

#### 5. ALTERNATİFLERİ

| Özellik | `FileReader`/`FileWriter` | `BufferedReader`/`BufferedWriter` |
|:--- |:--- |:--- |
| **Tamponlama** | Yok (her işlemde doğrudan diske erişir) | Var (verileri bellekte biriktirerek toplu işlem yapar) |
| **Performans** | Düşük (çok sayıda disk erişimi) | Yüksek (az sayıda disk erişimi) |
| **Kullanım Kolaylığı** | Basit (sadece okuma/yazma) | Orta (ek metotlar: `readLine()`, `newLine()`) |
| **Kullanım Alanı** | Küçük dosyalar, karakter karakter işleme | Büyük dosyalar, satır satır işleme |

#### 6. YAYGIN HATALAR
* **Hata:** `FileWriter`'ın var olan bir dosyanın üzerine yazacağını unutmak. Eğer dosyaya ekleme yapmak istiyorsanız, `FileWriter` yapıcısına ikinci parametre olarak `true` vermelisiniz: `new FileWriter("dosya.txt", true)`.
  * **Çözüm:** Ekleme modu için `true` parametresini kullanın.
* **Hata:** `read()` metodunun `int` döndürdüğünü unutup direkt `char`'a cast etmek. Dosya sonunda -1 döndüğü için cast işlemi hatalı karaktere yol açabilir.
  * **Çözüm:** `read()`'in dönüş değerini kontrol edin (-1 değilse) ve sonra `(char)` cast edin.


### `BufferedReader` ve `BufferedWriter`

#### 1. TANIM
`BufferedReader` ve `BufferedWriter`, karakter akışlarını sarmalayarak (wrap) tamponlama (buffering) yapan sınıflardır. Verileri bellekte biriktirerek toplu halde okuma/yazma yaparlar, bu sayede disk erişim sayısını azaltarak performansı artırırlar.

#### 2. NEDEN VAR?
`FileReader` ve `FileWriter` her okuma/yazma işleminde doğrudan diske erişir. Bu, özellikle büyük dosyalarla çalışırken çok yavaştır. `BufferedReader` ve `BufferedWriter`, verileri bir tampon (buffer) bellekte biriktirerek, tampon dolduğunda veya boşaldığında toplu disk erişimi yapar. Bu, performansı önemli ölçüde artırır.

**Günlük Hayat Analojisi:** Bir kamyon şoförü düşünün. Her bir kutuyu ayrı ayrı fabrikaya götürmek (`FileWriter`) yerine, kutuları bir depoda biriktirip kamyon dolunca fabrikaya götürmek (`BufferedWriter`) çok daha verimlidir.

#### 3. NASIL KULLANILIR?


```java
import java.io.*;

public class BufferedReaderWriterOrnegi {
    public static void main(String[] args) {
        String kaynakDosya = "ogrenciler.txt";
        String hedefDosya = "yeniOgrenciler.txt";

        // try-with-resources ile kaynakları yönet
        try (BufferedReader okuyucu = new BufferedReader(new FileReader(kaynakDosya));
             BufferedWriter yazici = new BufferedWriter(new FileWriter(hedefDosya))) {

            String satir;
            // readLine() dosya sonunda null döndürür
            while ((satir = okuyucu.readLine()) != null) {
                // Her satırı büyük harfe çevirerek yaz
                yazici.write(satir.toUpperCase());
                yazici.newLine(); // Satır sonu ekle
            }
            System.out.println("Dosya başarıyla işlendi.");
        } catch (FileNotFoundException e) {
            System.err.println("Dosya bulunamadı: " + e.getMessage());
        } catch (IOException e) {
            System.err.println("Okuma/Yazma hatası: " + e.getMessage());
        }
    }
}
```


**Kod Açıklaması:**
* `BufferedReader okuyucu = new BufferedReader(new FileReader(kaynakDosya))`: `FileReader`'ı `BufferedReader` ile sarmalıyoruz. `BufferedReader`'ın yapıcısı bir `Reader` nesnesi alır.
* `okuyucu.readLine()`: Bir satırı okuyup `String` olarak döndürür. Satır sonu karakterini (`\n`, `\r\n`) okumaz. Dosya sonunda `null` döndürür.
* `yazici.write(satir.toUpperCase())`: Okunan satırı büyük harfe çevirip yazıcıya gönderir.
* `yazici.newLine()`: Platformdan bağımsız satır sonu karakterini ekler (`\n` veya `\r\n`).

#### 4. NE ZAMAN TERCİH EDİLİR?
* **`BufferedReader`/`BufferedWriter` tercih edilir:** Büyük metin dosyalarıyla çalışırken, satır satır işleme yaparken (örneğin, bir CSV dosyasını ayrıştırmak) veya performans kritik olduğunda.
* **`FileReader`/`FileWriter` tercih edilir:** Küçük dosyalarla çalışırken veya karakter karakter işleme yapmak gerektiğinde (nadir bir durum).

#### 5. ALTERNATİFLERİ
Yukarıdaki tabloda `FileReader`/`FileWriter` ile karşılaştırılmıştır.

#### 6. YAYGIN HATALAR
* **Hata:** `readLine()` ile okunan satırın `null` kontrolünü yapmamak. Dosya sonunda `null` döner ve bu durumda işlem yapmaya çalışmak `NullPointerException`'a yol açar.
  * **Çözüm:** `while ((satir = okuyucu.readLine())!= null)` desenini kullanarak her zaman null kontrolü yapın.
* **Hata:** `BufferedWriter`'ı `close()` yapmayı unutmak. Bu, tamponda bekleyen verilerin diske yazılmamasına neden olur. `try-with-resources` bu sorunu otomatik çözer.
  * **Çözüm:** Her zaman `try-with-resources` kullanın veya `finally` bloğunda `close()` yapın.


### `PrintWriter`

#### 1. TANIM
`PrintWriter`, biçimlendirilmiş çıktı (formatted output) için kullanılan bir sınıftır. `System.out.println()` ve `System.out.printf()` metotlarına benzer şekilde `print()`, `println()` ve `printf()` metotlarını sunar. Bu sayede dosyaya kolayca metin yazabiliriz.

#### 2. NEDEN VAR?
`FileWriter` ve `BufferedWriter` ile dosyaya yazmak için `write()`, `newLine()` gibi metotları kullanırız. `PrintWriter`, `println()` gibi daha kullanışlı metotlar sunarak kod yazmayı kolaylaştırır ve daha okunabilir hale getirir.

**Günlük Hayat Analojisi:** Bir yazıcı (`PrintWriter`) düşünün. Normal bir yazıcı (`FileWriter`) gibi sadece metin yazmakla kalmaz, aynı zamanda otomatik olarak yeni satıra geçebilir (`println`), sayfa düzeni yapabilir (`printf`) ve hatta hataları sessizce yok sayabilir (hata durumunu kontrol etmek için `checkError()` metodu vardır).

#### 3. NASIL KULLANILIR?


```java
import java.io.*;

public class TamponluDosyaKopyalama {
    public static void main(String[] args) {
        String kaynakDosya = "kaynak.txt";
        String hedefDosya = "hedef.txt";

        // try-with-resources ile kaynaklar otomatik kapatılır
        try (BufferedReader okuyucu = new BufferedReader(new FileReader(kaynakDosya));
             BufferedWriter yazici = new BufferedWriter(new FileWriter(hedefDosya))) {

            String satir;
            int satirNumarasi = 1;
            // Dosya sonuna kadar satır satır oku
            while ((satir = okuyucu.readLine()) != null) {
                // Satır numarası ve iki nokta ekleyerek hedef dosyaya yaz
                yazici.write(satirNumarasi + ": " + satir);
                yazici.newLine(); // Platformdan bağımsız yeni satır ekle
                satirNumarasi++;
            }
            System.out.println("Dosya başarıyla kopyalandı.");
        } catch (IOException e) {
            System.err.println("Dosya işlemi sırasında hata: " + e.getMessage());
        }
    }
}
// Çıktı (hedef.txt dosyası):
// 1: kaynak.txt'nin ilk satırı
// 2: kaynak.txt'nin ikinci satırı
```

0


0


**Kod Açıklaması:**
* `PrintWriter yazici = new PrintWriter(new FileWriter(hedefDosya))`: `FileWriter`'ı `PrintWriter` ile sarmalıyoruz.
* `yazici.println(…)`: Metni yazdıktan sonra otomatik olarak yeni satıra geçer.
* `yazici.printf(…)`: `System.out.printf()` ile aynı şekilde çalışır. Biçimlendirilmiş metin yazmamızı sağlar.
* `%n`: Platformdan bağımsız satır sonu karakterini temsil eder.

#### 4. NE ZAMAN TERCİH EDİLİR?
* **`PrintWriter` tercih edilir:** Dosyaya kolayca metin yazmak, özellikle de biçimlendirilmiş çıktı (tablolar, raporlar) oluşturmak istediğinizde.
* **`BufferedWriter` tercih edilir:** Sadece yüksek performanslı, tamponlu yazma işlemi yapmanız gerekiyorsa ve biçimlendirmeye ihtiyacınız yoksa.

#### 5. ALTERNATİFLERİ

| Özellik | `PrintWriter` | `BufferedWriter` |
|:--- |:--- |:--- |
| **Temel Metotlar** | `print()`, `println()`, `printf()` | `write()`, `newLine()` |
| **Biçimlendirme** | Var (`printf` ile) | Yok |
| **Hata Yönetimi** | `checkError()` ile hata kontrolü | İstisna fırlatır |
| **Performans** | Orta (tamponlama yapabilir) | Yüksek (tamponlama yapar) |
| **Kullanım Kolaylığı** | Yüksek | Düşük |

#### 6. YAYGIN HATALAR
* **Hata:** `PrintWriter`'ın hata durumunu kontrol etmemek. `PrintWriter`, yazma sırasında oluşan hataları istisna fırlatarak değil, bir bayrak (flag) ile belirtir. Bu nedenle, yazma işleminin başarılı olup olmadığını kontrol etmek için `checkError()` metodunu çağırmak gerekir.
  * **Çözüm:** Yazma işleminden sonra `if (yazici.checkError()) {… }` ile hata kontrolü yapın.
* **Hata:** `PrintWriter`'ı `File` nesnesi ile doğrudan kullanmak (örneğin `new PrintWriter("dosya.txt")`). Bu kullanımda karakter kodlaması (encoding) belirtilmediği için platform varsayılanı kullanılır, bu da taşınabilirlik sorunlarına yol açabilir.
  * **Çözüm:** Karakter kodlamasını belirtmek için `new PrintWriter(new FileWriter("dosya.txt", StandardCharsets.UTF_8))` gibi bir kullanım tercih edin.


### `FileReader` ve `FileWriter` (Bayt Tabanlı)

#### 1. TANIM
`FileReader` ve `FileWriter` sınıflarını daha önce karakter tabanlı olarak ele almıştık. Ancak Java'da aynı isimde bayt tabanlı sınıflar da vardır: `FileInputStream` (okuma) ve `FileOutputStream` (yazma). Bunlar, ham baytları (byte) okumak ve yazmak için kullanılır. Resim, video, ses dosyaları gibi ikili (binary) dosyalarla çalışmak için idealdir.

#### 2. NEDEN VAR?
Metin dosyaları dışında kalan tüm dosya türleri (resim, video, exe, zip) bayt tabanlıdır. Bu dosyaları karakter tabanlı sınıflarla (`FileReader`, `BufferedReader`) okumaya çalışmak, karakter kodlaması sorunlarına ve veri bozulmasına yol açar. `FileInputStream` ve `FileOutputStream`, bu tür dosyalarla güvenli bir şekilde çalışmamızı sağlar.

**Günlük Hayat Analojisi:** Bir kargo şirketi düşünün. Mektuplar (metin dosyaları) için ayrı, koliler (ikili dosyalar) için ayrı taşıma süreçleri vardır. Mektupları koli bandıyla sarmak (`FileReader` ile ikili dosya okumak) anlamsız ve hataya açıktır.

#### 3. NASIL KULLANILIR?


```java
import java.io.*;

public class TamponluDosyaKopyalama {
    public static void main(String[] args) {
        String kaynakDosya = "kaynak.txt";
        String hedefDosya = "hedef.txt";

        // try-with-resources ile kaynaklar otomatik kapatılır
        try (BufferedReader okuyucu = new BufferedReader(new FileReader(kaynakDosya));
             BufferedWriter yazici = new BufferedWriter(new FileWriter(hedefDosya))) {

            String satir;
            int satirNumarasi = 1;
            // Dosya sonuna kadar satır satır oku
            while ((satir = okuyucu.readLine()) != null) {
                // Satır numarası ve iki nokta ekleyerek hedef dosyaya yaz
                yazici.write(satirNumarasi + ": " + satir);
                yazici.newLine(); // Platformdan bağımsız yeni satır ekle
                satirNumarasi++;
            }
            System.out.println("Dosya başarıyla kopyalandı.");
        } catch (IOException e) {
            System.err.println("Dosya işlemi sırasında hata: " + e.getMessage());
        }
    }
}
// Çıktı (hedef.txt dosyası):
// 1: kaynak.txt'nin ilk satırı
// 2: kaynak.txt'nin ikinci satırı
```

1


1

java
import java.io.*;

public class TamponluDosyaKopyalama {
  public static void main(String[] args) {
  String kaynakDosya = "buyuk_bir_resim.jpg";
  String hedefDosya = "buyuk_bir_resim_kopya.jpg";

  // try-with-resources ile tamponlu akışları yönet
  try (BufferedInputStream giris = new BufferedInputStream(new FileInputStream(kaynakDosya));
  BufferedOutputStream cikis = new BufferedOutputStream(new FileOutputStream(hedefDosya))) {

  byte[] tampon = new byte[4096]; // 4 KB'lık bir tampon
  int okunanBaytSayisi;

  // Tamponu doldur, yaz ve sıfırla
  while ((okunanBaytSayisi = giris.read(tampon))!= -1) {
  cikis.write(tampon, 0, okunanBaytSayisi); // Tampondaki veriyi yaz
  // NOT: write() metodu, tamponun tamamını değil, sadece okunan kısmını yazar
  }
  System.out.println("Dosya başarıyla kopyalandı.");
  // Çıktı: Dosya başarıyla kopyalandı.

  } catch (FileNotFoundException e) {
  System.err.println("Dosya bulunamadı: " + e.getMessage());
  } catch (IOException e) {
  System.err.println("Dosya kopyalanırken hata oluştu: " + e.getMessage());
  }
  }
}


```java
import java.io.*;

public class TamponluDosyaKopyalama {
    public static void main(String[] args) {
        String kaynakDosya = "kaynak.txt";
        String hedefDosya = "hedef.txt";

        // try-with-resources ile kaynaklar otomatik kapatılır
        try (BufferedReader okuyucu = new BufferedReader(new FileReader(kaynakDosya));
             BufferedWriter yazici = new BufferedWriter(new FileWriter(hedefDosya))) {

            String satir;
            int satirNumarasi = 1;
            // Dosya sonuna kadar satır satır oku
            while ((satir = okuyucu.readLine()) != null) {
                // Satır numarası ve iki nokta ekleyerek hedef dosyaya yaz
                yazici.write(satirNumarasi + ": " + satir);
                yazici.newLine(); // Platformdan bağımsız yeni satır ekle
                satirNumarasi++;
            }
            System.out.println("Dosya başarıyla kopyalandı.");
        } catch (IOException e) {
            System.err.println("Dosya işlemi sırasında hata: " + e.getMessage());
        }
    }
}
// Çıktı (hedef.txt dosyası):
// 1: kaynak.txt'nin ilk satırı
// 2: kaynak.txt'nin ikinci satırı
```

2


2

java
import java.io.*;

public class PrintWriterOrnegi {
  public static void main(String[] args) {
  String dosyaAdi = "notlar.txt";
  // try-with-resources ile PrintWriter'ı otomatik kapat
  try (PrintWriter yazici = new PrintWriter(new FileWriter(dosyaAdi, true))) { // true: ekleme modu

  // println() ile satır satır yaz
  yazici.println("Öğrenci Not Listesi");
  yazici.println("===================");

  // printf() ile biçimlendirilmiş yazı
  String ogrenciAdi = "Ali";
  int not = 95;
  yazici.printf("%-15s %d%n", ogrenciAdi, not); // Sola hizalı, 15 karakterlik alan

  ogrenciAdi = "Ayşe";
  not = 87;
  yazici.printf("%-15s %d%n", ogrenciAdi, not);

  System.out.println("Notlar dosyaya yazıldı.");
  // Çıktı: Notlar dosyaya yazıldı.

  } catch (IOException e) {
  System.err.println("Dosyaya yazılırken hata oluştu: " + e.getMessage());
  }
  }
}


```java
import java.io.*;

public class TamponluDosyaKopyalama {
    public static void main(String[] args) {
        String kaynakDosya = "kaynak.txt";
        String hedefDosya = "hedef.txt";

        // try-with-resources ile kaynaklar otomatik kapatılır
        try (BufferedReader okuyucu = new BufferedReader(new FileReader(kaynakDosya));
             BufferedWriter yazici = new BufferedWriter(new FileWriter(hedefDosya))) {

            String satir;
            int satirNumarasi = 1;
            // Dosya sonuna kadar satır satır oku
            while ((satir = okuyucu.readLine()) != null) {
                // Satır numarası ve iki nokta ekleyerek hedef dosyaya yaz
                yazici.write(satirNumarasi + ": " + satir);
                yazici.newLine(); // Platformdan bağımsız yeni satır ekle
                satirNumarasi++;
            }
            System.out.println("Dosya başarıyla kopyalandı.");
        } catch (IOException e) {
            System.err.println("Dosya işlemi sırasında hata: " + e.getMessage());
        }
    }
}
// Çıktı (hedef.txt dosyası):
// 1: kaynak.txt'nin ilk satırı
// 2: kaynak.txt'nin ikinci satırı
```

3


3

java
import java.io.File;
import java.util.Date;

public class FileBilgisi {
  public static void main(String[] args) {
  // File nesnesi oluştur (dosya henüz var olmayabilir)
  File dosya = new File("ornek.txt");

  // Dosya hakkında bilgileri yazdır
  System.out.println("Dosya adı: " + dosya.getName());
  System.out.println("Dosya yolu: " + dosya.getPath());
  System.out.println("Mutlak yol: " + dosya.getAbsolutePath());

  // Dosyanın var olup olmadığını kontrol et
  if (dosya.exists()) {
  System.out.println("Dosya mevcut.");
  System.out.println("Dosya boyutu: " + dosya.length() + " bayt");
  System.out.println("Son değiştirilme: " + new Date(dosya.lastModified()));

  if (dosya.isDirectory()) {
  System.out.println("Bu bir dizindir.");
  } else if (dosya.isFile()) {
  System.out.println("Bu bir dosyadır.");
  }
  } else {
  System.out.println("Dosya mevcut değil.");
  }
  // Çıktı (dosya yoksa):
  // Dosya adı: ornek.txt
  // Dosya yolu: ornek.txt
  // Mutlak yol: C:\Users\…\ornek.txt
  // Dosya mevcut değil.
  }
}


```java
import java.io.*;

public class TamponluDosyaKopyalama {
    public static void main(String[] args) {
        String kaynakDosya = "kaynak.txt";
        String hedefDosya = "hedef.txt";

        // try-with-resources ile kaynaklar otomatik kapatılır
        try (BufferedReader okuyucu = new BufferedReader(new FileReader(kaynakDosya));
             BufferedWriter yazici = new BufferedWriter(new FileWriter(hedefDosya))) {

            String satir;
            int satirNumarasi = 1;
            // Dosya sonuna kadar satır satır oku
            while ((satir = okuyucu.readLine()) != null) {
                // Satır numarası ve iki nokta ekleyerek hedef dosyaya yaz
                yazici.write(satirNumarasi + ": " + satir);
                yazici.newLine(); // Platformdan bağımsız yeni satır ekle
                satirNumarasi++;
            }
            System.out.println("Dosya başarıyla kopyalandı.");
        } catch (IOException e) {
            System.err.println("Dosya işlemi sırasında hata: " + e.getMessage());
        }
    }
}
// Çıktı (hedef.txt dosyası):
// 1: kaynak.txt'nin ilk satırı
// 2: kaynak.txt'nin ikinci satırı
```

4


4

java
import java.io.File;
import java.io.FilenameFilter;

public class DizinFiltreleme {
  public static void main(String[] args) {
  String dizinYolu = "."; // Geçerli çalışma dizini

  File dizin = new File(dizinYolu);

  if (dizin.isDirectory()) {
  // Lambda ifadesi ile FilenameFilter oluştur
  FilenameFilter javaFilter = (dir, name) -> name.endsWith(".java");

  // Filtrelenmiş dosya listesini al
  File[] javaDosyalari = dizin.listFiles(javaFilter);

  if (javaDosyalari!= null && javaDosyalari.length > 0) {
  System.out.println("Dizindeki.java dosyaları:");
  for (File f: javaDosyalari) {
  System.out.println(" - " + f.getName());
  }
  } else {
  System.out.println("Dizinde.java dosyası bulunamadı.");
  }
  } else {
  System.out.println("Geçerli bir dizin değil.");
  }
  // Çıktı (örnek):
  // Dizindeki.java dosyaları:
  // - Main.java
  // - Öğrenci.java
  }
}


```java
import java.io.*;

public class TamponluDosyaKopyalama {
    public static void main(String[] args) {
        String kaynakDosya = "kaynak.txt";
        String hedefDosya = "hedef.txt";

        // try-with-resources ile kaynaklar otomatik kapatılır
        try (BufferedReader okuyucu = new BufferedReader(new FileReader(kaynakDosya));
             BufferedWriter yazici = new BufferedWriter(new FileWriter(hedefDosya))) {

            String satir;
            int satirNumarasi = 1;
            // Dosya sonuna kadar satır satır oku
            while ((satir = okuyucu.readLine()) != null) {
                // Satır numarası ve iki nokta ekleyerek hedef dosyaya yaz
                yazici.write(satirNumarasi + ": " + satir);
                yazici.newLine(); // Platformdan bağımsız yeni satır ekle
                satirNumarasi++;
            }
            System.out.println("Dosya başarıyla kopyalandı.");
        } catch (IOException e) {
            System.err.println("Dosya işlemi sırasında hata: " + e.getMessage());
        }
    }
}
// Çıktı (hedef.txt dosyası):
// 1: kaynak.txt'nin ilk satırı
// 2: kaynak.txt'nin ikinci satırı
```

5


5

java
import java.nio.file.*;
import java.io.IOException;
import java.util.List;

public class NioBasitOrnek {
  public static void main(String[] args) {
  Path dosyaYolu = Paths.get("ornek_nio.txt"); // Paths.get() ile Path nesnesi oluştur

  // Dosyaya yazma (Files.write() ile)
  try {
  String icerik = "Merhaba, NIO.2 Dünyası!";
  Files.write(dosyaYolu, icerik.getBytes()); // String'i byte dizisine çevir
  System.out.println("Dosyaya yazıldı: " + dosyaYolu.toAbsolutePath());
  // Çıktı: Dosyaya yazıldı: C:\Users\…\ornek_nio.txt
  } catch (IOException e) {
  System.err.println("Yazma hatası: " + e.getMessage());
  }

  // Dosyadan okuma (Files.readAllLines() ile)
  try {
  List<String> satirlar = Files.readAllLines(dosyaYolu); // Tüm satırları bir List'e oku
  System.out.println("Dosya içeriği:");
  for (String satir: satirlar) {
  System.out.println(satir);
  }
  // Çıktı: Dosya içeriği:
  // Merhaba, NIO.2 Dünyası!
  } catch (IOException e) {
  System.err.println("Okuma hatası: " + e.getMessage());
  }
  }
}


```java
import java.io.*;

public class TamponluDosyaKopyalama {
    public static void main(String[] args) {
        String kaynakDosya = "kaynak.txt";
        String hedefDosya = "hedef.txt";

        // try-with-resources ile kaynaklar otomatik kapatılır
        try (BufferedReader okuyucu = new BufferedReader(new FileReader(kaynakDosya));
             BufferedWriter yazici = new BufferedWriter(new FileWriter(hedefDosya))) {

            String satir;
            int satirNumarasi = 1;
            // Dosya sonuna kadar satır satır oku
            while ((satir = okuyucu.readLine()) != null) {
                // Satır numarası ve iki nokta ekleyerek hedef dosyaya yaz
                yazici.write(satirNumarasi + ": " + satir);
                yazici.newLine(); // Platformdan bağımsız yeni satır ekle
                satirNumarasi++;
            }
            System.out.println("Dosya başarıyla kopyalandı.");
        } catch (IOException e) {
            System.err.println("Dosya işlemi sırasında hata: " + e.getMessage());
        }
    }
}
// Çıktı (hedef.txt dosyası):
// 1: kaynak.txt'nin ilk satırı
// 2: kaynak.txt'nin ikinci satırı
```

6


6

java
// Hatalı: Dosyanın üzerine yazar
Files.write(dosyaYolu, "Yeni içerik".getBytes());

// Doğru: Dosyaya ekleme yapar
Files.write(dosyaYolu, "Eklenecek içerik".getBytes(), StandardOpenOption.APPEND);


```java
import java.io.*;

public class TamponluDosyaKopyalama {
    public static void main(String[] args) {
        String kaynakDosya = "kaynak.txt";
        String hedefDosya = "hedef.txt";

        // try-with-resources ile kaynaklar otomatik kapatılır
        try (BufferedReader okuyucu = new BufferedReader(new FileReader(kaynakDosya));
             BufferedWriter yazici = new BufferedWriter(new FileWriter(hedefDosya))) {

            String satir;
            int satirNumarasi = 1;
            // Dosya sonuna kadar satır satır oku
            while ((satir = okuyucu.readLine()) != null) {
                // Satır numarası ve iki nokta ekleyerek hedef dosyaya yaz
                yazici.write(satirNumarasi + ": " + satir);
                yazici.newLine(); // Platformdan bağımsız yeni satır ekle
                satirNumarasi++;
            }
            System.out.println("Dosya başarıyla kopyalandı.");
        } catch (IOException e) {
            System.err.println("Dosya işlemi sırasında hata: " + e.getMessage());
        }
    }
}
// Çıktı (hedef.txt dosyası):
// 1: kaynak.txt'nin ilk satırı
// 2: kaynak.txt'nin ikinci satırı
```

7


7

java
// Taşınabilir (Portable) yol oluşturma
Path dogruYol = Paths.get("anaDizin", "altDizin", "dosya.txt");
// Windows: anaDizin\altDizin\dosya.txt
// Linux: anaDizin/altDizin/dosya.txt


```java
import java.io.*;

public class TamponluDosyaKopyalama {
    public static void main(String[] args) {
        String kaynakDosya = "kaynak.txt";
        String hedefDosya = "hedef.txt";

        // try-with-resources ile kaynaklar otomatik kapatılır
        try (BufferedReader okuyucu = new BufferedReader(new FileReader(kaynakDosya));
             BufferedWriter yazici = new BufferedWriter(new FileWriter(hedefDosya))) {

            String satir;
            int satirNumarasi = 1;
            // Dosya sonuna kadar satır satır oku
            while ((satir = okuyucu.readLine()) != null) {
                // Satır numarası ve iki nokta ekleyerek hedef dosyaya yaz
                yazici.write(satirNumarasi + ": " + satir);
                yazici.newLine(); // Platformdan bağımsız yeni satır ekle
                satirNumarasi++;
            }
            System.out.println("Dosya başarıyla kopyalandı.");
        } catch (IOException e) {
            System.err.println("Dosya işlemi sırasında hata: " + e.getMessage());
        }
    }
}
// Çıktı (hedef.txt dosyası):
// 1: kaynak.txt'nin ilk satırı
// 2: kaynak.txt'nin ikinci satırı
```

8


8

java
import java.nio.file.*;
import java.io.IOException;
import java.util.List;
import java.util.ArrayList;

public class NioDosyaIslemleri {
  public static void main(String[] args) {
  Path kaynak = Paths.get("kaynak_metin.txt"); // Okunacak dosya
  Path hedef = Paths.get("hedef_metin.txt"); // Yazılacak dosya

  // 1. Kaynak dosyayı oluştur (test için)
  try {
  Files.write(kaynak,
  "Java NIO.2 çok güçlüdür.\nDosya işlemleri artık çok kolay.\n".getBytes());
  System.out.println("Kaynak dosya oluşturuldu.");
  } catch (IOException e) {
  System.err.println("Kaynak oluşturma hatası: " + e.getMessage());
  }

  // 2. Dosyayı oku ve satırları büyük harfe çevir
  try {
  // Tüm satırları oku
  List<String> satirlar = Files.readAllLines(kaynak);
  List<String> buyukHarfliSatirlar = new ArrayList<>();

  // Her satırı büyük harfe çevir
  for (String satir: satirlar) {
  buyukHarfliSatirlar.add(satir.toUpperCase());
  }

  // Yeni dosyaya yaz
  Files.write(hedef, buyukHarfliSatirlar);
  System.out.println("Hedef dosya oluşturuldu: " + hedef.toAbsolutePath());

  // 3. Hedef dosyayı oku ve ekrana yazdır
  System.out.println("\nHedef dosya içeriği:");
  Files.readAllLines(hedef).forEach(System.out::println);
  // Çıktı: Hedef dosya içeriği:
  // JAVA NIO.2 ÇOK GÜÇLÜDÜR.
  // DOSYA İŞLEMLERİ ARTIK ÇOK KOLAY.

  } catch (IOException e) {
  System.err.println("Dosya işlemi hatası: " + e.getMessage());
  }

  // 4. Temizlik: test dosyalarını sil
  try {
  Files.deleteIfExists(kaynak);
  Files.deleteIfExists(hedef);
  System.out.println("\nTest dosyaları temizlendi.");
  } catch (IOException e) {
  System.err.println("Temizlik hatası: " + e.getMessage());
  }
  }
}


```java
import java.io.*;

public class TamponluDosyaKopyalama {
    public static void main(String[] args) {
        String kaynakDosya = "kaynak.txt";
        String hedefDosya = "hedef.txt";

        // try-with-resources ile kaynaklar otomatik kapatılır
        try (BufferedReader okuyucu = new BufferedReader(new FileReader(kaynakDosya));
             BufferedWriter yazici = new BufferedWriter(new FileWriter(hedefDosya))) {

            String satir;
            int satirNumarasi = 1;
            // Dosya sonuna kadar satır satır oku
            while ((satir = okuyucu.readLine()) != null) {
                // Satır numarası ve iki nokta ekleyerek hedef dosyaya yaz
                yazici.write(satirNumarasi + ": " + satir);
                yazici.newLine(); // Platformdan bağımsız yeni satır ekle
                satirNumarasi++;
            }
            System.out.println("Dosya başarıyla kopyalandı.");
        } catch (IOException e) {
            System.err.println("Dosya işlemi sırasında hata: " + e.getMessage());
        }
    }
}
// Çıktı (hedef.txt dosyası):
// 1: kaynak.txt'nin ilk satırı
// 2: kaynak.txt'nin ikinci satırı
```

9


9

java
try {
  int sonuc = 10 / 0;
} catch (ArithmeticException e) {
  System.out.println("Hata: " + e.getMessage());
} finally {
  System.out.println("Finally bloğu çalıştı.");
}
```


## Alıştırmalar

**Alıştırma 1: Öğrenci Not Defteri**

Bir metin dosyasından öğrenci notlarını okuyan, ortalamayı hesaplayan ve sonuçları yeni bir dosyaya yazan bir program yazın. try-with-resources kullanın.

**Alıştırma 2: Özel İstisna ile Dosya Doğrulama**

`GecersizDosyaFormatiException` adında özel bir istisna sınıfı oluşturun. Bir dosyanın `.txt` uzantılı olup olmadığını kontrol eden, değilse bu istisnayı fırlatan bir metot yazın.

**Alıştırma 3: Dizin Gezgini**

Bir dizindeki tüm `.java` dosyalarını listeleyen, her dosyanın boyutunu ve son değiştirilme tarihini gösteren bir program yazın. `File` sınıfını kullanın.

**Alıştırma 4: NIO.2 ile Dosya Kopyalama**

`Files.copy()` metodunu kullanarak bir dosyayı kopyalayan program yazın. Kopyalama sırasında hedef dosya zaten varsa, üzerine yazma seçeneği sunun.

**Alıştırma 5: Log Analizörü**

Bir log dosyasındaki hata mesajlarını (ERROR kelimesi içeren satırları) filtreleyen ve ayrı bir dosyaya yazan program yazın. `BufferedReader` ve `PrintWriter` kullanın.


## Sık Yapılan Hatalar (Hata Katalogu)

| Hata | Açıklama | Çözüm |
|---|---|---|
| **Dosya Bulunamadı** | Okunmaya çalışılan dosya mevcut değil. | Dosya yolunu kontrol edin, `File.exists()` ile ön kontrol yapın. |
| **Unchecked İstisnayı Yakalamamak** | `NullPointerException` gibi unchecked istisnaları yakalamamak. | Null kontrolleri yapın, gerekirse try-catch kullanın. |
| **finally'de Kaynak Kapatmayı Unutmak** | try-catch'den sonra akışları kapatmamak. | try-with-resources kullanın veya finally bloğunda kapatın. |
| **Çok Genel İstisna Yakalamak** | Sadece `Exception` yakalamak, özel hataları gizler. | Mümkün olduğunca spesifik istisna sınıfları yakalayın. |
| **throw'u throws ile Karıştırmak** | throw istisnayı fırlatır, throws ise bildirir. | throw'u metot içinde, throws'u metot imzasında kullanın. |
| **NIO.2'de StandardOpenOption Kullanmamak** | `Files.write()` varsayılan olarak üzerine yazar. | Ekleme yapmak için `StandardOpenOption.APPEND` kullanın. |
| **Path Ayracı Sorunu** | Windows'ta `\`, Linux'ta `/` kullanmak. | `Paths.get()`'e parçalar halinde yol verin veya `File.separator` kullanın. |


## İleri Okuma Kaynakları

1. **Oracle Java Tutorials - Essential Java Classes: Basic I/O** - Java'nın resmi dokümantasyonu, temel G/Ç işlemleri için başvuru kaynağı.
  - https://docs.oracle.com/javase/tutorial/essential/io/

2. **Oracle Java Tutorials - Essential Java Classes: Exceptions** - İstisna yönetimi için resmi eğitim.
  - https://docs.oracle.com/javase/tutorial/essential/exceptions/

3. **Java NIO.2 API Specification** - NIO.2 paketinin detaylı API dokümantasyonu.
  - https://docs.oracle.com/javase/8/docs/api/java/nio/file/package-summary.html

4. **"Java: The Complete Reference" - Herbert Schildt** - Dosya işlemleri ve istisna yönetimi konularında kapsamlı bir kaynak.

5. **"Effective Java" - Joshua Bloch** - İstisna yönetimi için en iyi uygulamalar (Best Practices) konusunda mükemmel bir rehber.


Bu bölümde, Java'da dosya işlemleri ve hata yönetiminin temellerini öğrendiniz. Artık dosyaları okuyabilir, yazabilir, hataları yönetebilir ve modern NIO.2 API'sini kullanabilirsiniz. Bir sonraki bölümde, bu bilgileri kullanarak daha karmaşık uygulamalar geliştireceğiz.

## Bolum ozeti

Bu bölümde, programların harici verilerle etkileşim kurmasını sağlayan **dosya işlemleri** ile program akışını kontrol altına alan **hata yönetimi** kavramlarını öğreneceksiniz. Java’da dosyaların nasıl okunup yazılacağını, `File`, `FileReader`, `BufferedReader` ve `FileWriter` gibi temel sınıfları uygulamalı olarak keşfedeceksiniz. Ayrıca, beklenmedik durumlarla başa çıkmak için `try-catch-finally` yapısını ve özel hata türlerini nasıl oluşturacağınızı kavrayacaksınız. Bölüm sonunda, hem dosya işlemleri sırasında oluşan hataları yönetebilecek hem de kendi hata sınıflarınızı tasarlayarak daha sağlam Java uygulamaları geliştirebileceksiniz.

## Terim sozlugu

**Dosya** — Kalıcı depolama birimlerinde (sabit disk, SSD) verilerin adlandırılmış bir bütün halinde saklandığı yapı.

**Dosya İşlemleri** — Programın çalışma zamanında dosyaları okuma, yazma, güncelleme ve silme gibi eylemlerin tümü.

**Akış (Stream)** — Verilerin kaynaktan hedefe doğru sıralı bir şekilde aktığı soyut veri yolu.

**Hata Yönetimi** — Program çalışırken beklenmedik durumların (hata) yakalanması ve uygun şekilde işlenmesi süreci.

**İstisna (Exception)** — Programın normal akışını bozan, çalışma zamanında meydana gelen beklenmedik olay.

**try-catch Bloğu** — Hata olasılığı bulunan kodun denendiği (try) ve hata oluştuğunda yakalandığı (catch) yapı.

**finally Bloğu** — Hata olsun ya da olmasın her durumda çalıştırılması garanti olan kod bloğu.

**try-with-resources** — Otomatik kaynak yönetimi sağlayan, dosya gibi kaynakların kullanımdan sonra kendiliğinden kapatıldığı Java 7 özelliği.

**File Sınıfı** — Dosya ve dizinlerin yol bilgilerini, özelliklerini ve temel işlemlerini temsil eden Java sınıfı.

**FileReader** — Karakter tabanlı dosya okuma işlemleri için kullanılan, metin dosyalarını karakter karakter okuyan sınıf.

**FileWriter** — Karakter tabanlı dosya yazma işlemleri için kullanılan, metin dosyalarına karakter karakter yazan sınıf.

**BufferedReader** — Verileri tamponlayarak (buffer) okuyan, böylece okuma performansını artıran sarmalayıcı sınıf.

**BufferedWriter** — Verileri tamponlayarak yazan, böylece yazma performansını artıran sarmalayıcı sınıf.

**IOException** — Giriş/çıkış işlemleri sırasında oluşan hataları temsil eden, dosya işlemlerinde en sık karşılaşılan istisna türü.

**Dosya Yolu (Path)** — İşletim sisteminde bir dosya veya dizinin konumunu belirten, mutlak veya göreceli olabilen adres bilgisi.

## Kendini degerlendirme sorulari

Elbette, işte "Dosya İşlemleri ve Hata Yönetimi" bölümü için hazırladığım kendini değerlendirme soruları.


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

## Bir sonraki bolume kopru

Bu bölümde dosyalarla nasıl iletişim kuracağımızı ve olası hataları nasıl yöneteceğimizi öğrendik. Bir sonraki bölümde, bu dosyalardan okuduğumuz verileri daha karmaşık yapılara dönüştürecek ve **Veri Yapıları (Collections Framework)** ile tanışacağız. Artık dosyadan gelen her satırı bir liste elemanına veya anahtar-değer çiftine dönüştürebilecek, büyük veri kümelerini hafızada etkin bir şekilde yönetebileceksiniz.
