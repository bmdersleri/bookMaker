# Bölüm 2: Değişkenler ve Veri Tipleri - Yaygın Hatalar ve Yanlış Sezgiler

## Hata 1: `int` tipine ondalıklı sayı atama

**Hata:** `int sayi = 5.7;` yazmak ve derleyicinin bunu kabul edeceğini sanmak.

**Neden yapılır:** Günlük hayatta "5.7" bir sayıdır, programlama dillerinde de sayı olduğu düşünülür. Öğrenciler ondalıklı sayıların sadece `double` tipinde saklanabileceğini bilmezler.

**Düzeltme:** 
```java
int sayi = 5;      // Doğru
double sayi = 5.7; // Doğru
// int sayi = 5.7; // Hata: uyumsuz tipler
```

## Hata 2: `String` ile `char`'ı karıştırma

**Hata:** `String harf = 'A';` veya `char kelime = "Merhaba";` yazmak.

**Neden yapılır:** Öğrenciler metinsel ifadelerin hepsini "string" olarak düşünür, tek karakterin farklı bir tip olduğunu fark etmezler. Java'da tırnak işaretleri bile farklıdır: `"` çift tırnak String, `'` tek tırnak char içindir.

**Düzeltme:**
```java
String harf = "A";  // Doğru: çift tırnak
char harf = 'A';    // Doğru: tek tırnak
// String kelime = 'Merhaba'; // Hata: tek tırnak içinde çok karakter
```

## Hata 3: `Scanner` nesnesini kapatmamak

**Hata:** Kullanıcıdan veri aldıktan sonra `scanner.close();` çağırmamak.

**Neden yapılır:** Öğrenciler bellekteki kaynak yönetimini düşünmezler. Scanner bir kaynak (resource) olduğu için kapatılması gerektiği akıllarına gelmez. Küçük programlarda sorun çıkarmadığı için alışkanlık haline gelir.

**Düzeltme:**
```java
Scanner scanner = new Scanner(System.in);
int yas = scanner.nextInt();
scanner.close(); // Her zaman kapat
```

## Hata 4: `nextInt()`'den sonra `nextLine()` kullanırken satır sonu karakterini unutma

**Hata:** 
```java
int yas = scanner.nextInt();  // Kullanıcı: 25 (Enter)
String isim = scanner.nextLine(); // Boş string okur!
```

**Neden yapılır:** `nextInt()` sayıyı okur ama satır sonundaki `\n` (Enter) karakterini tamponda bırakır. `nextLine()` ise bu kalan `\n`'i hemen okur ve boş string döndürür. Öğrenciler bu davranışı sezgisel olarak tahmin edemezler.

**Düzeltme:**
```java
int yas = scanner.nextInt();
scanner.nextLine(); // Tampondaki \n'i temizle
String isim = scanner.nextLine(); // Artık doğru çalışır
```

## Hata 5: `final` değişkene sonradan değer atamaya çalışma

**Hata:** 
```java
final double PI = 3.14;
PI = 3.14159; // Hata: final değişken değiştirilemez
```

**Neden yapılır:** Öğrenciler "sabit" kavramını günlük hayattaki gibi "değişmeyen şey" olarak anlarlar ama programlama dilinin bu kuralı derleme aşamasında nasıl uyguladığını kavrayamazlar. Matematikte pi sayısı 3.14... diye bilinir, öğrenci "daha hassas versiyonunu kullanayım" diye düşünür.

**Düzeltme:** `final` değişkenler sadece bir kez atanabilir. Eğer değer değişecekse `final` kullanılmamalıdır:
```java
double pi = 3.14;  // final değil, değiştirilebilir
pi = 3.14159;      // Şimdi doğru
```