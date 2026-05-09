<!-- v1.3 notu: Bu dosya v1.2 içeriği temel alınarak otomasyon uyumlu pakete dahil edilmiştir. Görünen numaralar üretim hattında atanır; kalıcı kimlikler manifestte tutulur. -->


**Amaç:** Bu belge, *Java'nın Temelleri* kitabının teknik doğruluk ve kaynak kullanım politikasını tanımlar. Amaç yalnızca kaynak listesi vermek değil; hangi tür kaynağın hangi amaçla kullanılacağını ve teknik doğrulamada hangi kaynakların öncelikli olduğunu belirlemektir.

---

## 1. Kaynak kullanım ilkesi

Bölüm üretimlerinde bilgi önceliği şu sırayla ele alınmalıdır:

1. Resmî Java dokümantasyonu ve Java SE API belgeleri
2. Oracle / Dev.java öğrenme kaynakları
3. Java Language Specification
4. Saygın yayınevlerinden çıkan Java ders kitapları
5. Akademik programlama eğitimi ve bilgisayar bilimi eğitimi kaynakları
6. Yardımcı bloglar, topluluk cevapları ve örnek kodlar
7. Yapay zekâ modelinin önerileri

Yapay zekâ tarafından üretilen teknik açıklama, kod örneği veya sınıflandırma tek başına yeterli kaynak sayılmamalıdır. Özellikle Java sürüm farkları, API kullanımı, Swing bileşenleri ve JDBC örnekleri resmî veya güvenilir teknik kaynaklarla doğrulanmalıdır.

---

## 2. Birincil teknik kaynaklar

### 2.1 Java SE Documentation

- Java SE Documentation
- Java SE API Specification
- Java Language Specification

**Kullanım amacı:**

- Dil sözdizimi,
- sınıf ve metot adları,
- standart kütüphane davranışları,
- `java.lang`, `java.util`, `java.io`, `java.nio.file`, `javax.swing`, `java.sql` paketleri,
- sürüm farkları

için birincil otoritedir.

---

### 2.2 Dev.java

**Kullanım amacı:**

- Java'ya başlangıç,
- temel dil yapıları,
- sınıflar ve nesneler,
- koleksiyonlar,
- hata yönetimi,
- modern Java öğrenme yaklaşımı

için güncel öğrenme kaynağı olarak kullanılabilir.

---

### 2.3 Java Tutorials

**Kullanım amacı:**

- Başlangıç düzeyi anlatım,
- örnek odaklı öğrenme,
- Swing ve GUI örnekleri,
- temel JDBC örnekleri,
- dosya işlemleri

için yardımcı kaynak olarak kullanılabilir.

---

## 3. Konu bazlı kaynak öncelikleri

| Konu | Öncelikli kaynak türü |
|---|---|
| JVM, JRE, JDK | Java SE / Oracle belgeleri |
| Dil sözdizimi | Java Language Specification + öğrenme kaynakları |
| Veri tipleri ve operatörler | Java Language Specification |
| String | Java SE API, `java.lang.String` |
| Math, Random | Java SE API, `java.lang.Math`, `java.util.Random` |
| Date-Time | Java SE API, `java.time` |
| Koleksiyonlar | Java SE API, `java.util` |
| Dosya işlemleri | Java SE API, `java.io`, `java.nio.file` |
| Hata yönetimi | Java Language Specification + API |
| Swing | Java Tutorials + Java SE API |
| JDBC | Java SE API, JDBC dokümantasyonu, veritabanı sürücü belgeleri |
| Programlama pedagojisi | ACM/IEEE CS Curricula, öğretim tasarımı kaynakları |

---

## 4. Yardımcı ders kitapları

Aşağıdaki türde kaynaklar bölüm akışını ve örnek tasarımını desteklemek için kullanılabilir:

- giriş düzeyi Java kitapları,
- bilgisayar mühendisliği için programlama kitapları,
- algoritmik problem çözme kitapları,
- nesneye yönelik programlamaya giriş kitapları,
- GUI programlama kaynakları,
- yazılım geliştirme temelleri kitapları.

Bu kaynaklar üslup ve pedagojik örnek tasarımında yardımcıdır; teknik ayrıntılar yine resmî Java belgeleriyle doğrulanmalıdır.

---

## 5. Sürüm politikası

Kitapta Java SE temel alınmalıdır. Kod örnekleri mümkün olduğunca yaygın kullanılan JDK sürümlerinde çalışabilecek şekilde yazılmalıdır. Sürüm bağımlı özellikler kullanılıyorsa açıkça belirtilmelidir.

Başlangıç kitabı olması nedeniyle:

- gereksiz modern sözdizimi gösterilerinden kaçınılmalı,
- `var`, record, pattern matching, sealed class gibi yapılar ana akışa alınmamalı,
- kullanılacaksa yalnızca ileri okuma kutusu olarak verilmelidir.

---

## 6. GUI kaynak politikası

Bu kitapta ana GUI aracı Swing olarak belirlenmiştir. Swing tercihinin gerekçesi:

- Java SE ekosistemi içinde uzun süredir bulunması,
- temel GUI kavramlarını öğretmek için yeterli olması,
- olay dinleyici mantığını görünür kılması,
- başlangıç düzeyi masaüstü uygulama geliştirmeye uygun olmasıdır.

JavaFX yalnızca Ek B'de kısa bakış olarak ele alınmalıdır.

---

## 7. JDBC kaynak politikası

JDBC konusu başlangıç düzeyinde kalmalıdır. Amaç öğrencinin veritabanı bağlantısının mantığını görmesidir.

İşlenecekler:

- bağlantı kurma,
- `PreparedStatement`,
- `ResultSet`,
- temel CRUD,
- bağlantı kapatma,
- SQL injection farkındalığı.

Kapsam dışı bırakılacaklar:

- JPA,
- Hibernate,
- Spring Data,
- transaction yönetimi ayrıntıları,
- bağlantı havuzu,
- kurumsal katmanlı mimari.

---

## 8. Pedagojik kaynaklar

Bölüm sonu alıştırmaları, öğrenme çıktıları ve rubrikler hazırlanırken şu pedagojik çerçeveler dikkate alınabilir:

- Bloom'un revize edilmiş taksonomisi,
- ACM/IEEE bilgisayar bilimleri müfredat önerileri,
- etkinlik temelli programlama öğretimi,
- problem temelli öğrenme,
- laboratuvar uygulaması tasarımı.

---

## 9. Kaynakların bölüm sonlarında kullanımı

Her bölümün sonunda kısa bir "İleri okuma ve kaynaklar" listesi verilmelidir. Liste öğrenciyi boğmamalıdır. Her bölüm için genellikle 3–6 kaynak yeterlidir.

Kaynaklar şu şekilde gruplanabilir:

- Resmî dokümantasyon
- Yardımcı öğretici kaynak
- İleri okuma
- Uygulama/laboratuvar kaynağı

---

## 10. Uyarı

Teknik bilgi uydurulmamalıdır. Emin olunmayan Java API davranışı, sürüm özelliği veya kütüphane kullanımı kesin ifadeyle yazılmamalıdır. Kodun çalıştırıldığı kesin değilse çıktı iddiası dikkatli kurulmalıdır.
