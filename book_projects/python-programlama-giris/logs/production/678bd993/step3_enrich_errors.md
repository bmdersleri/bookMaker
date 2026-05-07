# Yaygın Hatalar ve Çözümleri

## Hata 1: **`else if` Yerine `else` Kullanmak**

**Hata:** Öğrenciler, birden fazla koşul kontrol etmek istediklerinde `else if` yerine `else` kullanarak tüm koşulları tek bir blokta sıralamaya çalışırlar.

```java
// YANLIŞ KULLANIM
int not = 75;
if (not >= 90) {
    System.out.println("AA");
} else (not >= 80) {  // HATA: else'den sonra koşul yazılmaz!
    System.out.println("BA");
} else (not >= 70) {
    System.out.println("BB");
}
```

**Neden yapılır?** Öğrenciler `else`'in sadece "değilse" anlamına geldiğini bilir, ancak `else`'in yanında koşul alamayacağını unuturlar. Günlük konuşmada "değilse, şu koşulda" ifadesi yaygındır.

**Düzeltme:** `else if` kullanılmalıdır:
```java
// DOĞRU KULLANIM
int not = 75;
if (not >= 90) {
    System.out.println("AA");
} else if (not >= 80) {  // Doğru: else if ile koşul eklenir
    System.out.println("BA");
} else if (not >= 70) {
    System.out.println("BB");
} else {
    System.out.println("Kaldı");
}
```

---

## Hata 2: **`=` ile `==` Karıştırmak**

**Hata:** Koşul ifadelerinde karşılaştırma yaparken `==` yerine `=` kullanmak.

```java
// YANLIŞ KULLANIM
int sayi = 5;
if (sayi = 10) {  // HATA: Atama operatörü kullanıldı, karşılaştırma değil
    System.out.println("Sayı 10");
}
```

**Neden yapılır?** Matematikte tek eşittir işareti "eşittir" anlamına gelir. Programlamada ise `=` atama, `==` karşılaştırma operatörüdür. Bu ayrım özellikle yeni başlayanlar için kafa karıştırıcıdır.

**Düzeltme:** Karşılaştırma için `==` kullanın:
```java
// DOĞRU KULLANIM
int sayi = 5;
if (sayi == 10) {  // Doğru: çift eşittir ile karşılaştırma
    System.out.println("Sayı 10");
}
```

**İpucu:** Sabit değeri sola yazmak hatayı yakalamayı kolaylaştırır:
```java
if (10 == sayi) {  // Eğer yanlışlıkla = yazarsanız derleme hatası alırsınız
    // ...
}
```

---

## Hata 3: **Sonsuz Döngü Oluşturmak**

**Hata:** Döngü koşulunun hiçbir zaman `false` olmaması nedeniyle programın sonsuza kadar çalışması.

```java
// YANLIŞ KULLANIM - Sonsuz döngü
int sayac = 1;
while (sayac <= 10) {
    System.out.println(sayac);
    // sayac++;  // Unutuldu! Döngü sonsuza kadar çalışır
}
```

**Neden yapılır?** Öğrenciler döngü değişkenini güncellemeyi unutur veya yanlış yönde günceller. Özellikle karmaşık koşullarda döngü değişkeninin değişmediği fark edilmez.

**Düzeltme:** Döngü değişkenini her adımda güncelleyin:
```java
// DOĞRU KULLANIM
int sayac = 1;
while (sayac <= 10) {
    System.out.println(sayac);
    sayac++;  // sayac = sayac + 1; ile aynı
}
```

**Başka bir yaygın hata:** Döngü değişkenini yanlış yönde güncellemek:
```java
// YANLIŞ - sayac küçülüyor, koşul hiç false olmaz
int sayac = 10;
while (sayac > 0) {
    System.out.println(sayac);
    sayac++;  // Hata: sayac artıyor, 10'dan büyük kalmaya devam eder
}
```

---

## Hata 4: **`break` ve `continue`'u Karıştırmak**

**Hata:** Öğrenciler `break`'in döngüyü tamamen sonlandırdığını, `continue`'un ise sadece mevcut iterasyonu atladığını karıştırır.

```java
// YANLIŞ KULLANIM - Beklenen: sadece 3'ü atla
for (int i = 1; i <= 5; i++) {
    if (i == 3) {
        break;  // Hata: break tüm döngüyü sonlandırır
    }
    System.out.println(i);
}
// Çıktı: 1 2 (3'ten sonraki tüm sayılar da atlandı)
```

**Neden yapılır?** "Kır" ve "devam et" kelimelerinin İngilizce anlamları yanıltıcı olabilir. "Break" (kır) döngüyü kırar, "continue" (devam et) ise bir sonraki adıma devam eder.

**Düzeltme:** Sadece 3'ü atlamak için `continue` kullanın:
```java
// DOĞRU KULLANIM
for (int i = 1; i <= 5; i++) {
    if (i == 3) {
        continue;  // Doğru: sadece 3'ü atla, döngü devam eder
    }
    System.out.println(i);
}
// Çıktı: 1 2 4 5
```

**Hızlı hatırlatma:** `break` = "çık", `continue` = "atla"

---

## Hata 5: **`switch`'te `break` Unutmak**

**Hata:** `switch` yapısında her `case`'den sonra `break` yazmayı unutmak, "fall-through" (düşme) davranışına neden olur.

```java
// YANLIŞ KULLANIM - Fall-through hatası
int gun = 2;
switch (gun) {
    case 1:
        System.out.println("Pazartesi");
    case 2:
        System.out.println("Salı");  // Bu da çalışır
    case 3:
        System.out.println("Çarşamba");  // Bu da çalışır!
}
// Çıktı: Salı Çarşamba (beklenen sadece "Salı")
```

**Neden yapılır?** Öğrenciler `switch`'in bir koşul yapısı olduğunu bilir, ancak `break`'in neden gerekli olduğunu anlamaz. `switch` aslında bir etiket atlama mekanizmasıdır.

**Düzeltme:** Her `case`'den sonra `break` ekleyin:
```java
// DOĞRU KULLANIM
int gun = 2;
switch (gun) {
    case 1:
        System.out.println("Pazartesi");
        break;  // Döngüden çık
    case 2:
        System.out.println("Salı");
        break;  // Döngüden çık
    case 3:
        System.out.println("Çarşamba");
        break;  // Döngüden çık
    default:
        System.out.println("Geçersiz gün");
}
// Çıktı: Salı
```

**Not:** Java 12+ ile `switch` ifadeleri (expression) bu sorunu çözmüştür, ancak temel `switch`'te hala geçerlidir.