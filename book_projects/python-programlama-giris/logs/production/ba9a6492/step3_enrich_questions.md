Harika bir bölüm taslağı. İşte talimatlarınıza uygun olarak hazırlanmış, bölümün ana kavramlarını kapsayan Doğru/Yanlış ve Boşluk Doldurma soruları.

---

### Doğru/Yanlış Soruları

**Soru 1:** Java'da bir `int` türündeki değişkene, doğrudan atama yapmadan önce kullanmaya çalışmak derleme hatasına neden olur.
- **Cevap:** Doğru
- **Açıklama:** Java yerel değişkenlerinin (local variables) kullanılmadan önce mutlaka bir değerle başlatılması (initialize) gerekir.

**Soru 2:** `double` türündeki bir sayıyı, hiçbir veri kaybı olmadan `int` türüne dönüştürmek her zaman mümkündür.
- **Cevap:** Yanlış
- **Açıklama:** `double` türünden `int` türüne dönüşüm (daraltma dönüşümü), ondalık kısmın kesilmesine (truncation) neden olur ve bu bir veri kaybıdır.

**Soru 3:** `final` anahtar kelimesi ile tanımlanan bir değişkene, programın ilerleyen satırlarında yeni bir değer atanabilir.
- **Cevap:** Yanlış
- **Açıklama:** `final` anahtar kelimesi, değişkeni bir sabit haline getirir ve değeri yalnızca bir kez atanabilir; daha sonra değiştirilemez.

**Soru 4:** Bir `if` bloğu içinde tanımlanan bir değişkene, o `if` bloğunun dışından erişilebilir.
- **Cevap:** Yanlış
- **Açıklama:** Bir blok içinde (süslü parantezler `{}` arasında) tanımlanan değişkenin kapsamı (scope) yalnızca o blokla sınırlıdır. Blok dışından erişilemez.

**Soru 5:** `String` veri tipi, Java'da ilkel (primitive) bir veri tipidir.
- **Cevap:** Yanlış
- **Açıklama:** `String` bir referans (reference) veri tipidir. `int`, `double`, `boolean` gibi tipler ise ilkel veri tipleridir.

**Soru 6:** `char` veri tipi, tek bir Unicode karakterini saklamak için kullanılır.
- **Cevap:** Doğru
- **Açıklama:** Java'da `char` veri tipi, 16-bit'lik Unicode karakter setini temsil eder ve tek bir karakter (harf, rakam, sembol) saklar.

**Soru 7:** `null` değeri, herhangi bir ilkel veri tipindeki değişkene atanabilir.
- **Cevap:** Yanlış
- **Açıklama:** `null`, bir referansın hiçbir nesneyi işaret etmediğini belirtir ve yalnızca referans (nesne) türündeki değişkenlere atanabilir. İlkel tiplere atanamaz.

**Soru 8:** `+` operatörü, sayısal bir değer ile bir `String` değeri birleştirirken, sayısal değeri otomatik olarak `String`'e dönüştürür.
- **Cevap:** Doğru
- **Açıklama:** Java'da `+` operatörü, işlenenlerden en az biri `String` ise, birleştirme (concatenation) işlemi yapar ve diğer işleneni otomatik olarak `String`'e çevirir.

---

### Boşluk Doldurma Soruları

**Soru 1:** Java'da bir değişkenin türünün, program çalışmaya başlamadan önce belirlenmesine ve değiştirilememesine __________ denir.
- **Cevap:** statik tipleme (static typing)
- **Açıklama:** Bu, Java'nın derleme zamanında tip kontrolü yapmasını sağlar ve hataların erken yakalanmasına yardımcı olur.

**Soru 2:** Büyük bir veri tipini (örneğin `double`), daha küçük bir veri tipine (örneğin `int`) dönüştürmek için yapılan ve veri kaybına yol açabilen işleme __________ dönüşüm denir.
- **Cevap:** daraltma (narrowing)
- **Açıklama:** Bu tür dönüşümlerde, veri kaybı riskini kabul ettiğimizi belirtmek için açıkça tip dönüşümü (explicit cast) yapmamız gerekir.

**Soru 3:** Kullanıcıdan klavye aracılığıyla veri almak için kullanılan Java sınıfı __________'dır.
- **Cevap:** Scanner
- **Açıklama:** `Scanner` sınıfı, `java.util` paketinin bir parçasıdır ve standart giriş akışından (`System.in`) veri okumak için yaygın olarak kullanılır.

**Soru 4:** Bir `String`'in belirtilen bir karakter veya alt dize ile başlayıp başlamadığını kontrol eden metot __________'dır.
- **Cevap:** `startsWith()`
- **Açıklama:** Bu metot, `boolean` bir değer döndürür ve metinsel kontrollerde sıkça kullanılır.

**Soru 5:** Değeri program boyunca değişmeyen ve `final` anahtar kelimesi ile tanımlanan değişkenlere __________ denir.
- **Cevap:** sabit (constant)
- **Açıklama:** Sabitler, sihirli sayılar (magic numbers) kullanımını engelleyerek kodun okunabilirliğini ve bakımını kolaylaştırır.

**Soru 6:** Bir değişkenin program içinde erişilebilir olduğu bölgeye __________ denir.
- **Cevap:** kapsam (scope)
- **Açıklama:** Kapsam, genellikle değişkenin tanımlandığı süslü parantezler `{}` tarafından belirlenir.