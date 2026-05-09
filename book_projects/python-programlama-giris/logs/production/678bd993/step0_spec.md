Harika bir görev! İşte **Bölüm 3: Koşullar ve Döngüler** için hazırladığım kapsamlı plan. Tüm kurallara harfiyen uyuyorum.

---

## 1. KAVRAMLAR

| Kavram | Ne Olduğu (1 cümle) | Zorluk | Kod Örneği? | Gösterilecek Konu (1 cümle) |
| :--- | :--- | :--- | :--- | :--- |
| **Karşılaştırma Operatörleri** | İki değeri birbiriyle karşılaştırarak `true` veya `false` sonucu üreten sembollerdir (`==`, `!=`, `<`, `>`, `<=`, `>=`). | ★☆☆☆☆ | Evet | Bir not sisteminde geçme/kalma durumunu belirlemek. |
| **Mantıksal Operatörler** | Birden fazla koşulu birleştirerek tek bir `true`/`false` sonucu üreten operatörlerdir (`&&`, `||`, `!`). | ★★☆☆☆ | Evet | Bir kullanıcının giriş yapabilmesi için hem kullanıcı adının hem de şifrenin doğru olması gerektiğini kontrol etmek. |
| **if-else if-else** | Belirli bir koşulun doğruluğuna göre farklı kod bloklarının çalıştırılmasını sağlayan temel kontrol yapısıdır. | ★★☆☆☆ | Evet | Bir öğrencinin notuna göre harf notunu (A, B, C, F) belirlemek. |
| **while Döngüsü** | Belirtilen bir koşul `true` olduğu sürece bir kod bloğunu tekrar tekrar çalıştıran döngü türüdür. | ★★☆☆☆ | Evet | Kullanıcı geçerli bir sayı girene kadar giriş istemek (doğrulama döngüsü). |
| **for Döngüsü** | Bir aralıktaki her bir eleman için veya belirli bir sayaç değişkeni ile belirli sayıda tekrar için kullanılan döngü türüdür. | ★★☆☆☆ | Evet | 1'den 10'a kadar olan sayıların toplamını hesaplamak. |
| **break/continue** | Döngülerin akışını kontrol etmek için kullanılan özel anahtar kelimelerdir; `break` döngüyü tamamen sonlandırır, `continue` ise mevcut iterasyonu atlar. | ★★★☆☆ | Evet | Bir listede belirli bir sayıyı bulduğumuzda döngüden çıkmak (`break`) veya çift sayıları atlayarak sadece tek sayıları yazdırmak (`continue`). |
| **List Comprehension** | (Bu kavram Java'da doğrudan yoktur; en yakın alternatifi Stream API ve `filter`/`map` işlemleridir.) Mevcut bir listeden yeni bir liste oluşturmak için kullanılan kısa ve öz bir sözdizimidir. | ★★★☆☆ | Evet | Bir tamsayı listesindeki sadece çift sayıları filtreleyerek yeni bir liste oluşturmak (Java Stream API ile). |
| **match-case (Java 21+)** | Bir değişkenin değerine göre birden fazla desenle eşleşme yaparak ilgili kod bloğunu çalıştıran, modern ve güçlü bir kontrol yapısıdır. | ★★★★☆ | Evet | Bir gün numarasına (1-7) göre haftanın hangi günü olduğunu yazdırmak (switch-case ile karşılaştırmalı). |

---

## 2. KOD ÖRNEKLERİ

1.  **Kavram:** Karşılaştırma ve Mantıksal Operatörler
    *   **Dosya Adı:** `NotDegerlendirme.java`
    *   **Tahmini Satır Sayısı:** 20
    *   **Kullanılacak Özellikler:** `Scanner`, `int`, `boolean`, `if`, `&&`, `||`, `>=`, `<`, `==`.

2.  **Kavram:** `if-else if-else` ve `while` Döngüsü
    *   **Dosya Adı:** `HarfNotuHesaplama.java`
    *   **Tahmini Satır Sayısı:** 35
    *   **Kullanılacak Özellikler:** `Scanner`, `while` (doğrulama için), `if-else if-else`, `break`.

3.  **Kavram:** `for` Döngüsü, `break` ve `continue`
    *   **Dosya Adı:** `SayiBulmaca.java`
    *   **Tahmini Satır Sayısı:** 25
    *   **Kullanılacak Özellikler:** `int[]` dizi, `for` döngüsü, `if`, `break` (sayıyı bulunca), `continue` (belirli koşulları atla).

4.  **Kavram:** List Comprehension (Stream API alternatifi)
    *   **Dosya Adı:** `FiltrelemeOrnegi.java`
    *   **Tahmini Satır Sayısı:** 20
    *   **Kullanılacak Özellikler:** `List<Integer>`, `ArrayList`, `for` döngüsü (geleneksel), `Stream` API (`filter`, `collect`, `toList()`).

5.  **Kavram:** `match-case` (Java 21+ Pattern Matching for Switch)
    *   **Dosya Adı:** `GunBulma.java`
    *   **Tahmini Satır Sayısı:** 25
    *   **Kullanılacak Özellikler:** `int`, `switch` expression, `case` ile desen eşleme, `yield` veya ok operatörü (`->`).

---

## 3. DİYAGRAMLAR

1.  **Neyi Görselleştirecek?** `if-else if-else` yapısının karar akışını.
    *   **Tür:** Flowchart
    *   **Düğümler:**
        *   Başla (Notu al)
        *   Karar: `not >= 90` mı? (Elmas)
        *   İşlem: "AA" yazdır (Dikdörtgen)
        *   Karar: `not >= 80` mi? (Elmas)
        *   İşlem: "BA" yazdır (Dikdörtgen)
        *   Karar: `not >= 70` mi? (Elmas)
        *   İşlem: "BB" yazdır (Dikdörtgen)
        *   İşlem: "FF" yazdır (Dikdörtgen)
        *   Bitir

2.  **Neyi Görselleştirecek?** `break` ve `continue` komutlarının döngü akışına etkisini.
    *   **Tür:** Flowchart
    *   **Düğümler:**
        *   Başla (Döngüye gir)
        *   Karar: Döngü koşulu sağlanıyor mu? (Elmas)
        *   Karar: `break` koşulu sağlandı mı? (Elmas)
        *   İşlem: Döngüden Çık (Dikdörtgen)
        *   Karar: `continue` koşulu sağlandı mı? (Elmas)
        *   İşlem: Altındaki kodu atla, bir sonraki iterasyona geç (Dikdörtgen)
        *   İşlem: Döngü gövdesinin geri kalanını çalıştır (Dikdörtgen)
        *   Bitir (Döngü bitti)

---

## 4. SÖZLÜK (Terim Listesi)

1.  Karşılaştırma Operatörü
2.  Mantıksal Operatör
3.  Koşul İfadesi (Conditional Statement)
4.  Kod Bloğu (Code Block)
5.  Döngü (Loop)
6.  İterasyon (Iteration)
7.  Sonsuz Döngü (Infinite Loop)
8.  Sayaç Değişkeni (Counter Variable)
9.  Kontrol Akışı (Control Flow)
10. Desen Eşleme (Pattern Matching)
11. Stream API
12. Lambda İfadesi
13. Doğrulama Döngüsü (Validation Loop)
14. Kısa Devre Değerlendirmesi (Short-circuit Evaluation)
15. `switch` İfadesi / İfade Biçimi (Expression)

---

## 5. DEĞERLENDİRME

**Doğru/Yanlış Soruları Konuları:**
1.  `==` operatörü iki String'in içeriğini karşılaştırır.
2.  `&&` operatörü, birinci koşul `false` ise ikinci koşulu değerlendirmez (kısa devre).
3.  `while` döngüsü koşul her zaman `true` ise hiç çalışmaz.
4.  `for` döngüsü içinde `break` kullanmak, sadece içinde bulunduğu en içteki döngüyü sonlandırır.
5.  `match-case` yapısı Java 17'de tanıtılmıştır.

**Boşluk Doldurma Soruları Konuları:**
1.  Bir koşulun tersini almak için kullanılan mantıksal operatör: `___`.
2.  Bir döngünün belirli bir iterasyonunu atlamak için kullanılan anahtar kelime: `___`.
3.  Bir koşul `true` olduğu sürece kod bloğunu çalıştıran döngü türü: `___`.
4.  Bir aralıkta (başlangıç, bitiş, artış miktarı) belirli sayıda tekrar için kullanılan döngü türü: `___`.
5.  Java'da bir tam sayıyı, bir dizi sabit değerle karşılaştırmak için kullanılan modern yapı: `___`.

---

## 6. ALIŞTIRMALAR

1.  **Konu:** Kullanıcıdan alınan bir sayının pozitif, negatif veya sıfır olduğunu belirleyen program.
    *   **Zorluk:** ★☆☆☆☆
2.  **Konu:** Kullanıcıdan alınan bir sayının faktöriyelini hesaplayan program (`for` döngüsü kullanarak).
    *   **Zorluk:** ★★☆☆☆
3.  **Konu:** Bir tamsayı dizisindeki en büyük elemanı bulan program (`for` döngüsü ve `if` koşulu kullanarak).
    *   **Zorluk:** ★★☆☆☆

---

## 7. SIK YAPILAN HATALAR

1.  **Atama ve Karşılaştırma Karışıklığı:** `if (x = 5)` yazarak `=` (atama) operatörünü `==` (karşılaştırma) yerine kullanmak.
2.  **Noktalı Virgül Tuzağı:** `while (x < 10);` yazarak döngü parantezinin hemen sonuna noktalı virgül koyup döngü gövdesini boş bırakmak (sonsuz döngü veya hiç çalışmama).
3.  **Geçersiz Koşullar:** `if (10 < x < 20)` gibi matematiksel gösterimi Java'ya olduğu gibi uygulamak (doğrusu: `if (10 < x && x < 20)`).
4.  **break/continue Kapsamı:** `break` veya `continue`'u, iç içe döngülerde sadece en içteki döngüyü etkileyeceğini unutarak yanlış yerde kullanmak.

---

## 8. TABLOLAR

**Karşılaştırma Tablosu: `while` vs `for` Döngüsü**

| Özellik | `while` Döngüsü | `for` Döngüsü |
| :--- | :--- | :--- |
| **Kullanım Amacı** | Koşul odaklı, tekrar sayısı bilinmiyorsa | Sayaç odaklı, tekrar sayısı biliniyorsa |
| **Sözdizimi** | `while (koşul) { ... }` | `for (başlangıç; koşul; güncelleme) { ... }` |
| **Sayaç Yönetimi** | Genellikle döngü gövdesi içinde elle yapılır | Döngü başlığında otomatik olarak yapılır |
| **Sonsuz Döngü Riski** | Yüksek (koşul güncellenmezse) | Daha düşük (sayaç genellikle artar) |
| **Örnek Senaryo** | Kullanıcı "çıkış" yazana kadar menü göstermek | 1'den 100'e kadar sayıların toplamını bulmak |

**Karşılaştırma Tablosu: `break` vs `continue`**

| Özellik | `break` | `continue` |
| :--- | :--- | :--- |
| **Etkisi** | İçinde bulunduğu en içteki döngüyü tamamen sonlandırır. | İçinde bulunduğu en içteki döngünün mevcut iterasyonunu sonlandırır, bir sonraki iterasyona geçer. |
| **Kullanım Amacı** | Bir koşul sağlandığında döngüden erken çıkmak için. | Bir koşul sağlandığında, döngünün geri kalan kodunu atlayıp yeni bir tekrara başlamak için. |
| **Sonuç** | Döngü sona erer, döngüden sonraki kod çalışır. | Döngü devam eder, sadece o adım atlanır. |