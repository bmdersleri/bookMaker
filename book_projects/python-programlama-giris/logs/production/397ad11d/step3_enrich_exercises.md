**Alıştırma 1: Sayısal İstatistik Hesaplayıcı (Kolay)**

- Amaç: Bu alıştırmada, fonksiyon tanımlama, parametre kullanma ve geri dönüş değeri kavramlarını pekiştireceksin. Ayrıca, `*args` yapısını kullanarak esnek sayıda parametre alan bir fonksiyon yazmayı öğreneceksin.
- Görev: Kullanıcıdan virgülle ayrılmış bir dizi sayı alan ve bu sayıların toplamını, ortalamasını, en büyüğünü ve en küçüğünü hesaplayan bir Python programı yaz. Hesaplamaları `hesapla` adlı bir fonksiyon içinde yap. Fonksiyon, sayıları `*args` olarak alsın ve sonuçları bir sözlük (dict) olarak döndürsün. Ana programda bu sözlüğün içindeki değerleri ekrana yazdır.
- İpucu: Kullanıcıdan gelen girdiyi almak için `input()` fonksiyonunu kullan. Girdiyi virgülden ayırmak için `split(',')` metodunu, her bir parçayı sayıya çevirmek için `float()` fonksiyonunu kullanabilirsin. En büyük ve en küçük değerler için `max()` ve `min()` fonksiyonlarını kullan.
- Beklenen Çıktı:
```
Lütfen sayıları virgülle ayırarak girin: 10,20,30,40,50
Hesaplanan İstatistikler:
Toplam: 150.0
Ortalama: 30.0
En Büyük: 50.0
En Küçük: 10.0
```

**Alıştırma 2: Modüler Hesap Makinesi ve Lambda Kullanımı (Orta)**

- Amaç: Bu alıştırmada, birden fazla fonksiyonu bir modül (`.py` dosyası) içinde organize etmeyi, bu modülü başka bir dosyadan içe aktarmayı (`import`) ve basit işlemler için lambda fonksiyonlarını kullanmayı öğreneceksin. Ayrıca, kullanıcıdan alınan girdiye göre farklı işlemleri seçmeyi deneyimleyeceksin.
- Görev: İki ayrı Python dosyası oluştur.
    1.  `islemler.py` adlı bir modül dosyası oluştur. Bu dosyada aşağıdaki işlemleri yapan fonksiyonları tanımla:
        - `topla(a, b)`: İki sayıyı toplar.
        - `cikar(a, b)`: İki sayıyı çıkarır.
        - `carp(a, b)`: İki sayıyı çarpar.
        - `bol(a, b)`: İki sayıyı böler (bölümü float olarak döndürür).
        - `ust_al(a, b)`: a üzeri b işlemini yapar (lambda fonksiyonu kullanarak tek satırda tanımla).
    2.  `ana_program.py` adlı ana dosyayı oluştur. Bu dosyada:
        - `islemler` modülünü içe aktar.
        - Kullanıcıya bir menü göster (1: Topla, 2: Çıkar, 3: Çarp, 4: Böl, 5: Üs Al, 0: Çıkış).
        - Kullanıcıdan iki sayı ve bir işlem seçeneği al.
        - Seçime göre ilgili fonksiyonu çağır ve sonucu ekrana yazdır.
        - Program, kullanıcı 0 girene kadar çalışmaya devam etsin. (While döngüsü ve if-elif yapısı kullanılabilir.)
- İpucu: Lambda fonksiyonunu `ust_al` değişkenine atayarak kullanabilirsin: `ust_al = lambda a, b: a ** b`. Modülü içe aktarmak için `import islemler` yazman yeterli. Modüldeki fonksiyonlara `islemler.topla(10, 5)` şeklinde erişebilirsin.
- Beklenen Çıktı:
```
Hesap Makinesi
1. Topla
2. Çıkar
3. Çarp
4. Böl
5. Üs Al
0. Çıkış
Seçiminiz: 1
Birinci sayı: 10
İkinci sayı: 5
Sonuç: 15.0

Hesap Makinesi
1. Topla
2. Çıkar
3. Çarp
4. Böl
5. Üs Al
0. Çıkış
Seçiminiz: 5
Birinci sayı: 2
İkinci sayı: 3
Sonuç: 8.0

Hesap Makinesi
1. Topla
2. Çıkar
3. Çarp
4. Böl
5. Üs Al
0. Çıkış
Seçiminiz: 0
Program sonlandırıldı.
```