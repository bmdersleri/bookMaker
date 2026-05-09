# Bölüm 3: Koşullar ve Döngüler - Kendini Değerlendirme Soruları

## Doğru/Yanlış Soruları

**Soru 1:** Java'da `if` bloğu her zaman bir `else` bloğu ile birlikte kullanılmalıdır.
- Cevap: Yanlış
- Açıklama: `if` bloğu tek başına kullanılabilir; `else` isteğe bağlıdır ve yalnızca koşul yanlış olduğunda çalışacak kod varsa eklenir.

**Soru 2:** `switch` ifadesi, `break` anahtar kelimesi olmadan da çalışabilir ancak bu durumda "fall-through" (düşme) davranışı sergiler.
- Cevap: Doğru
- Açıklama: `break` kullanılmazsa, eşleşen `case`'den sonraki tüm `case`'ler de sırayla çalıştırılır.

**Soru 3:** `for` döngüsü, yalnızca belirli bir sayıda tekrar edilecek işlemler için kullanılabilir.
- Cevap: Yanlış
- Açıklama: `for` döngüsü, bir koleksiyon üzerinde gezinmek (for-each) veya bir koşul sağlandığı sürece çalışmak gibi farklı amaçlarla da kullanılabilir.

**Soru 4:** `while` döngüsü, koşul kontrolünü döngü bloğunun sonunda yapar.
- Cevap: Yanlış
- Açıklama: `while` döngüsü, koşul kontrolünü döngü bloğunun **başında** yapar. Koşul yanlışsa döngü bloğu hiç çalışmaz.

**Soru 5:** `do-while` döngüsü, koşul yanlış olsa bile döngü bloğunu en az bir kez çalıştırır.
- Cevap: Doğru
- Açıklama: `do-while` döngüsünde koşul kontrolü bloğun sonunda yapıldığı için, blok en az bir kez çalıştırılır.

**Soru 6:** Java'da `break` ifadesi yalnızca döngülerden çıkmak için kullanılabilir.
- Cevap: Yanlış
- Açıklama: `break` ifadesi hem döngülerden hem de `switch` bloklarından çıkmak için kullanılabilir.

**Soru 7:** `continue` ifadesi, döngünün o anki iterasyonunu sonlandırır ve bir sonraki iterasyona geçer.
- Cevap: Doğru
- Açıklama: `continue` ifadesi, döngü bloğunun kalan kısmını atlayarak bir sonraki adıma geçilmesini sağlar.

**Soru 8:** İç içe döngülerde, içteki döngüdeki `break` ifadesi dıştaki döngüyü de sonlandırır.
- Cevap: Yanlış
- Açıklama: `break` ifadesi yalnızca içinde bulunduğu en içteki döngüyü sonlandırır. Dıştaki döngüyü sonlandırmak için etiketli (labeled) `break` kullanılmalıdır.

**Soru 9:** `if-else if-else` yapısı, üç veya daha fazla koşulun sırayla kontrol edilmesini sağlar.
- Cevap: Doğru
- Açıklama: Bu yapı, birden fazla koşulu sırayla değerlendirir ve ilk doğru koşulun bloğunu çalıştırır.

**Soru 10:** `switch` ifadesi, Java 7'den itibaren `String` türündeki değişkenlerle de kullanılabilir.
- Cevap: Doğru
- Açıklama: Java 7 ile birlikte `switch` ifadesine `String` desteği eklenmiştir.

---

## Boşluk Doldurma Soruları

**Soru 1:** Bir koşulun doğru olup olmadığını kontrol etmek için kullanılan yapıya ________ denir.
- Cevap: `if` ifadesi (veya karar yapısı)
- Açıklama: `if` ifadesi, belirtilen koşul doğruysa bir kod bloğunu çalıştırır.

**Soru 2:** `switch` ifadesinde, eşleşen `case`'den sonraki `case`'lerin de çalışmasını engellemek için ________ anahtar kelimesi kullanılır.
- Cevap: `break`
- Açıklama: `break` ifadesi, `switch` bloğundan çıkarak fall-through davranışını önler.

**Soru 3:** Bir döngünün kaç kez döneceği önceden bilindiğinde en uygun döngü türü ________ döngüsüdür.
- Cevap: `for`
- Açıklama: `for` döngüsü, başlangıç değeri, koşul ve artış/değişim adımlarını tek bir satırda tanımlamayı sağlar.

**Soru 4:** Koşul kontrolünü döngü bloğunun sonunda yapan döngü türü ________ döngüsüdür.
- Cevap: `do-while`
- Açıklama: `do-while` döngüsü, önce bloğu çalıştırır, sonra koşulu kontrol eder.

**Soru 5:** Bir döngünün o anki iterasyonunu sonlandırıp bir sonraki iterasyona geçmek için ________ ifadesi kullanılır.
- Cevap: `continue`
- Açıklama: `continue` ifadesi, döngü bloğunun kalanını atlayarak bir sonraki adıma geçilmesini sağlar.

**Soru 6:** Bir döngüden veya `switch` bloğundan çıkmak için ________ ifadesi kullanılır.
- Cevap: `break`
- Açıklama: `break` ifadesi, içinde bulunduğu döngüyü veya `switch` bloğunu sonlandırır.

**Soru 7:** Java'da bir dizi veya koleksiyonun tüm elemanlarını sırayla işlemek için kullanılan `for` döngüsü varyasyonuna ________ döngüsü denir.
- Cevap: for-each (veya gelişmiş for)
- Açıklama: for-each döngüsü, `for (veriTürü eleman : dizi)` sözdizimiyle kullanılır.

**Soru 8:** Koşul ifadelerinde, mantıksal VE işlemi ________ operatörüyle, mantıksal VEYA işlemi ________ operatörüyle yapılır.
- Cevap: `&&`, `||`
- Açıklama: `&&` (AND) tüm koşullar doğruysa, `||` (OR) en az bir koşul doğruysa true döndürür.

**Soru 9:** Bir değişkenin değerine göre birden fazla seçenek arasından seçim yapmak için ________ ifadesi kullanılır.
- Cevap: `switch`
- Açıklama: `switch` ifadesi, tek bir değişkenin değerine göre farklı `case` bloklarına yönlendirme yapar.

**Soru 10:** İç içe döngülerde, dıştaki döngüyü sonlandırmak için ________ kullanılır.
- Cevap: etiketli break (labeled break)
- Açıklama: `break etiketAdi;` şeklinde kullanılan etiketli break, belirtilen etikete sahip döngüyü sonlandırır.