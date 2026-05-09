## Sık Yapılan Hatalar

### Hata 1: JDK ile JRE'yi Karıştırmak
**Hata:** Öğrenciler, Java programı yazmak için sadece JRE (Java Runtime Environment) kurmanın yeterli olduğunu düşünür.
**Neden:** İnternetteki birçok kaynak "Java'yı indirin" derken aslında JRE'yi kasteder. Oyun veya hazır uygulama çalıştırmak için JRE yeterlidir.
**Düzeltme:** Java kodu yazıp derlemek için JDK (Java Development Kit) kurulmalıdır. JDK, içinde JRE'yi de barındırır. Konsolda `javac -version` yazarak JDK'nın kurulu olduğunu doğrulayın. JRE yüklüyse bu komut hata verecektir.

### Hata 2: `javac` ile `java` Komutlarını Karıştırmak
**Hata:** Öğrenciler kaynak kodu derlemeden doğrudan `java Merhaba.java` yazarak çalıştırmaya çalışır.
**Neden:** Python gibi yorumlanan dillerde kaynak kod doğrudan çalıştırılır. Java'nın derleme+çalıştırma adımlarını atlamak yaygındır.
**Düzeltme:** Önce `javac Merhaba.java` ile derleyin, ardından `java Merhaba` (uzantısız) ile çalıştırın. Bu iki adımın farkını kavrayana kadar her seferinde sırayı takip edin.

### Hata 3: Sınıf Adı ile Dosya Adını Aynı Yazmamak
**Hata:** `public class Merhaba` tanımlarken dosyayı `merhaba.java` veya `merhaba.JAVA` olarak kaydederler.
**Neden:** Java büyük-küçük harf duyarlıdır. Öğrenciler dosya sisteminin (Windows) bazen harf duyarsız olması nedeniyle hatayı fark etmez.
**Düzeltme:** Sınıf adı neyse dosya adı aynı olmalıdır: `Merhaba.java`. Derleme hatası alırsanız dosya adını ve sınıf adını birebir eşleştirin. Linux/Mac'te bu hata hemen görülür.

### Hata 4: `main` Metodunu Yanlış Yazmak
**Hata:** `public static void main(String[] args)` yerine `public void main()` veya `static void main()` yazarlar.
**Neden:** Java'da program giriş noktası çok spesifiktir. Öğrenciler diğer dillerdeki gibi herhangi bir metodu başlangıç noktası yapabileceklerini sanar.
**Düzeltme:** Ana metodu ezberlemek yerine anlayın: `public` (her yerden erişim), `static` (nesne oluşturmadan çağrı), `void` (geri dönüş yok), `String[] args` (komut satırı argümanları). İlk 10 programda bunu kopyala-yapıştır yapmaktan çekinmeyin.

### Hata 5: Kodun Her Satırına Noktalı Virgül Koymayı Unutmak
**Hata:** `System.out.println("Merhaba")` yazıp noktalı virgülü unuturlar veya `if` bloklarından sonra gereksiz noktalı virgül koyarlar.
**Neden:** Python gibi dillerde satır sonu belirteci yoktur. Öğrenciler "bir satır = bir komut" mantığıyla hareket eder.
**Düzeltme:** Her ifade sonuna `;` koyma alışkanlığı edinin. Derleme hatası mesajında satır numarası verilir, hatayı o satırda arayın. `if` bloklarından sonra noktalı virgül koymayın, çünkü bu bloğu boş bir ifade olarak algılatır.