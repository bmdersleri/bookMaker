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
project-alias: python-programlama-giris
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

Programlarımız sadece geçici verilerle çalışmaz. Bir oyunun en yüksek skorunu, bir kullanıcının ayarlarını veya bir öğrencinin not listesini kalıcı olarak saklamamız gerekir. İşte bu noktada **dosya işlemleri** devreye girer. Ancak dosyalarla çalışmak, her an bir şeylerin ters gidebileceği anlamına da gelir: dosya bulunamayabilir, izinler yetersiz olabilir veya disk dolabilir. Bu bölümde, hem dosyalarla nasıl güvenli ve etkili bir şekilde çalışacağımızı hem de bu tür beklenmedik durumları (hataları) profesyonelce nasıl yöneteceğimizi öğreneceğiz.


## 1. Dosya Açma Modları: Dosyaya Hangi Yetkiyle Yaklaşıyoruz?

### TANIM
Dosya açma modları, bir dosyayı programımızda kullanmak üzere açarken hangi işlemleri (okuma, yazma, ekleme) yapabileceğimizi belirleyen karakter dizileridir (`'r'`, `'w'`, `'a'` gibi).

### NEDEN VAR?
Bir dosyayı açarken niyetimizi belirtmezsek, istenmeyen sonuçlar doğabilir. Örneğin, sadece okumak istediğimiz bir dosyayı yanlışlıkla yazma modunda açarsak, dosyanın tüm içeriğini silebiliriz. Veya önemli bir log dosyasına bilgi eklemek isterken, yanlışlıkla eski kayıtların üzerine yazabiliriz. Açma modları, bu tür kazaları önlemek için bir "güvenlik önlemi" görevi görür. Bu kavram olmasaydı, her dosya işlemi potansiyel bir veri kaybı riski taşırdı.

### NASIL KULLANILIR?
`open()` fonksiyonuna ikinci parametre olarak modu belirtiriz. İşte en yaygın modlar:

| Mod | Açıklama | Dosya Yoksa | İmleç Başlangıcı |
|:--- |:--- |:--- |:--- |
| `'r'` | **Okuma (Read)** | Hata verir (`FileNotFoundError`) | Başlangıç |
| `'w'` | **Yazma (Write)** | Yeni dosya oluşturur | Başlangıç (içeriği siler) |
| `'a'` | **Ekleme (Append)** | Yeni dosya oluşturur | Dosyanın sonu |
| `'r+'` | **Okuma ve Yazma** | Hata verir | Başlangıç |
| `'w+'` | **Okuma ve Yazma (Üzerine yazar)** | Yeni dosya oluşturur | Başlangıç (içeriği siler) |
| `'a+'` | **Okuma ve Ekleme** | Yeni dosya oluşturur | Dosyanın sonu |

Şimdi bu modları bir örnekle görelim:


```python
# ornek_veri.txt dosyasını oluşturalım (ilk çalıştırmada)
with open('ornek_veri.txt', 'w', encoding='utf-8') as dosya:
    dosya.write("Bu ilk satirdir.\n")
    dosya.write("Bu ikinci satirdir.\n")

print("1. 'r' modu ile okuma denemesi:")
try:
    # 'r' modu: sadece okuma. Dosya yoksa hata verir.
    with open('ornek_veri.txt', 'r', encoding='utf-8') as dosya:
        icerik = dosya.read()
        print(f"Okunan icerik:\n{icerik}")
except FileNotFoundError:
    print("HATA: Dosya bulunamadi!")

print("\n2. 'w' modu ile yazma denemesi:")
# 'w' modu: dosyayi silip yeniden olusturur.
with open('ornek_veri.txt', 'w', encoding='utf-8') as dosya:
    dosya.write("Bu 'w' modu ile yazilan tek satirdir.\n")
print("Dosyaya yazildi.")

# 'r' ile tekrar okuyalim, eski verinin silindigini gorelim.
with open('ornek_veri.txt', 'r', encoding='utf-8') as dosya:
    print(f"Yeni icerik:\n{dosya.read()}")

print("\n3. 'a' modu ile ekleme denemesi:")
# 'a' modu: dosyanin sonuna ekleme yapar.
with open('ornek_veri.txt', 'a', encoding='utf-8') as dosya:
    dosya.write("Bu satir 'a' modu ile eklendi.\n")
print("Dosyaya eklendi.")

with open('ornek_veri.txt', 'r', encoding='utf-8') as dosya:
    print(f"Son icerik:\n{dosya.read()}")
# Çıktı:
# 1. 'r' modu ile okuma denemesi:
# Okunan icerik:
# Bu ilk satirdir.
# Bu ikinci satirdir.
#
# 2. 'w' modu ile yazma denemesi:
# Dosyaya yazildi.
# Yeni icerik:
# Bu 'w' modu ile yazilan tek satirdir.
#
# 3. 'a' modu ile ekleme denemesi:
# Dosyaya eklendi.
# Son icerik:
# Bu 'w' modu ile yazilan tek satirdir.
# Bu satir 'a' modu ile eklendi.
```


**Kod Açıklaması:**
1. İlk olarak `ornek_veri.txt` dosyasını `'w'` modunda açıp içine iki satır yazıyoruz.
2. `'r'` modunu deniyoruz. `try-except` ile olası `FileNotFoundError` hatasını yakalıyoruz. Dosya var olduğu için içeriği başarıyla okuyoruz.
3. `'w'` modunu kullanarak dosyaya yeni bir satır yazıyoruz. Bu işlem, dosyanın eski içeriğini tamamen siler. Ardından dosyayı tekrar okuyarak bunu doğruluyoruz.
4. `'a'` modu ile dosyaya bir satır daha ekliyoruz. Son okumada, dosyanın sonuna eklendiğini ve eski verinin korunduğunu görüyoruz.

### NE ZAMAN TERCİH EDİLİR?
- **`'r'`:** Bir dosyayı sadece okumak, analiz etmek veya ekrana yazdırmak istediğinizde. Örneğin, bir konfigürasyon dosyasını okumak.
- **`'w'`:** Bir dosyayı sıfırdan oluşturmak veya tamamen güncellemek istediğinizde. Örneğin, bir programın çıktısını yeni bir dosyaya kaydetmek.
- **`'a'`:** Bir dosyaya yeni kayıtlar eklemek, eski veriyi korumak istediğinizde. Örneğin, bir web sunucusunun log dosyasına her yeni isteği eklemek.

### ALTERNATİFLERİ
Dosya işlemleri için `open()` dışında, özel amaçlı kütüphaneler de vardır. Ancak temel dosya işlemleri için `open()` ve modları en yaygın ve doğrudan yöntemdir.

### YAYGIN HATALAR
- **`'w'` ile `'a'` modunu karıştırmak:** En sık yapılan hata, bir dosyaya veri eklemek isterken `'w'` modunu kullanarak tüm eski veriyi silmektir. **Çözüm:** Ekleme yapacaksanız her zaman `'a'` modunu kullanın.
- **Dosyanın var olup olmadığını kontrol etmemek:** `'r'` modunda var olmayan bir dosyayı açmak `FileNotFoundError` hatasına yol açar. **Çözüm:** `try-except` kullanın veya `os.path.exists()` ile dosyanın varlığını kontrol edin.


## 2. `with` Context Manager: Kaynakları Güvenle Yönetmek

### TANIM
`with` deyimi, bir kaynağın (dosya, ağ bağlantısı, veritabanı bağlantısı gibi) işimiz bittiğinde otomatik olarak temizlenmesini (kapatılmasını) garanti eden bir Python yapısıdır.

### NEDEN VAR?
Dosyayı `open()` ile açtıktan sonra, işimiz bittiğinde `close()` ile kapatmazsak, kaynak sızıntısı (resource leak) oluşur. Bu, dosyanın başka programlar tarafından kullanılmasını engelleyebilir veya programın bellek kullanımının artmasına neden olabilir. Ayrıca, dosya işlemi sırasında bir hata oluşursa `close()` çağrısı hiç çalışmayabilir. `with` deyimi, bu sorunu ortadan kaldırır: bloktan nasıl çıkılırsa çıkılsın (normal sonlanma veya hata), kaynak otomatik olarak kapatılır. Bu kavram olmasaydı, her dosya işleminden sonra `close()` çağırmayı unutmamak ve hata durumlarını ayrıca ele almak zorunda kalırdık.

**Günlük Hayat Analojisi:** Bir otel odası kiraladığınızı düşünün (`open`). Odada kaldığınız süre boyunca (`with` bloğu) odanın tadını çıkarırsınız. Otelden ayrılırken (`blok sonu`), resepsiyona anahtarı teslim etmeniz gerekir (`close`). `with` deyimi, odadan ayrıldığınız anda otel görevlisinin sizin yerinize anahtarı teslim etmesi gibidir. Siz çıkış yapmayı unutsanız bile, görevli odanın boşaldığını fark eder ve anahtarı teslim alır. Bu sayede oda başka bir müşteri için hemen hazır hale gelir.

### NASIL KULLANILIR?
`with open(…) as degisken_adi:` şeklinde kullanılır.


```python
# notlar.txt dosyasina ogrenci notlarini yazalim
ogrenci_notlari = ["Ali: 85", "Ayse: 92", "Mehmet: 78", "Fatma: 88"]

# 'with' kullanarak dosyayi guvenle acip yaziyoruz
with open('notlar.txt', 'w', encoding='utf-8') as dosya:
    print("Dosyaya notlar yaziliyor...")
    for not_satiri in ogrenci_notlari:
        # Her not satirini dosyaya yaz
        dosya.write(not_satiri + '\n')
    # Burada dosya.close() cagirmamiza gerek yok!
    print("Yazma islemi tamamlandi.")

# 'with' blogu bittigi anda dosya otomatik olarak kapatildi.
# Simdi dosyayi tekrar acip okuyalim.
with open('notlar.txt', 'r', encoding='utf-8') as dosya:
    print("\nDosyadan okunan notlar:")
    for satir in dosya:
        print(satir.strip())  # strip() ile satir sonundaki '\n' karakterini temizliyoruz
# Çıktı:
# Dosyaya notlar yaziliyor...
# Yazma islemi tamamlandi.
#
# Dosyadan okunan notlar:
# Ali: 85
# Ayse: 92
# Mehmet: 78
# Fatma: 88
```


**Kod Açıklaması:**
1. `with open('notlar.txt', 'w') as dosya:` satırı, `notlar.txt` dosyasını yazma modunda açar ve `dosya` değişkenine atar.
2. `with` bloğunun içinde `dosya.write()` ile verilerimizi yazıyoruz. Bu işlem sırasında bir hata olsa bile, bloktan çıkıldığında `dosya` otomatik olarak kapatılır.
3. Blok bittiğinde, dosyayı kapatmak için `dosya.close()` çağırmamıza gerek yoktur. Bu, `with` deyiminin en büyük avantajıdır.
4. İkinci `with` bloğunda ise aynı dosyayı okuyoruz.

### NE ZAMAN TERCİH EDİLİR?
Her zaman! Dosya, ağ bağlantısı, veritabanı bağlantısı gibi açılıp kapatılması gereken her türlü kaynak için `with` deyimini kullanmak en iyi uygulamadır (best practice). `close()`'u manuel olarak çağırmak, unutkanlık veya hata durumları nedeniyle risklidir.

### ALTERNATİFLERİ
`with` deyimi olmadan da dosya işlemi yapılabilir:


```python
dosya = open('notlar.txt', 'r')
icerik = dosya.read()
dosya.close()  # Kapatmayı unutmamalıyız!
```


Ancak bu yöntem, yukarıda belirtilen riskleri taşır. `with` deyimi, Python 2.5 ile tanıtılmıştır ve o zamandan beri kaynak yönetimi için standart haline gelmiştir.

### YAYGIN HATALAR
- **`with` bloğu dışında dosyayı kullanmaya çalışmak:** `with` bloğu bittiğinde dosya kapanır. Blok dışında `dosya` değişkenine erişmeye çalışmak `ValueError: I/O operation on closed file.` hatasına yol açar. **Çözüm:** Dosyayla ilgili tüm işlemleri `with` bloğu içinde yapın.


## 3. Dosyadan Veri Okuma: `read()`, `readline()`, `readlines()`

### TANIM
Bu üç yöntem, bir dosyanın içeriğini farklı şekillerde okumamızı sağlar: `read()` tüm dosyayı tek bir string olarak, `readline()` bir sonraki satırı string olarak, `readlines()` ise tüm satırları bir liste olarak döndürür.

### NEDEN VAR?
Her durumda dosyanın tamamını okumak verimli olmayabilir. Çok büyük dosyalarda (örneğin bir milyon satırlık bir log dosyası) `read()` veya `readlines()` kullanmak, tüm dosyanın belleğe yüklenmesine ve programın çökmesine neden olabilir. `readline()` ise satır satır okuyarak belleği verimli kullanmamızı sağlar. Bu yöntemler, farklı okuma senaryoları için esneklik sunar.

**Günlük Hayat Analojisi:** Kalın bir kitabınız olduğunu düşünün.
- `read()`: Kitabın tamamını fotokopi çekmek gibidir. Hızlıca tüm içeriğe sahip olursunuz ama çok fazla kağıt (bellek) harcarsınız.
- `readline()`: Kitabı sayfa sayfa okumak gibidir. Her seferinde sadece bir sayfayı (satırı) okur, bir sonraki sayfaya geçersiniz. Bu, belleği çok az kullanır.
- `readlines()`: Kitabın içindekiler tablosunu çıkarmak gibidir. Her sayfanın (satırın) başlığını bir listeye yazarsınız. Tüm kitabın bir özetini elde edersiniz.

### NASIL KULLANILIR?
Önce 10 satırlık bir `ogrenciler.txt` dosyası oluşturalım.


```python
# ogrenciler.txt dosyasini olustur
with open('ogrenciler.txt', 'w', encoding='utf-8') as dosya:
    for i in range(1, 11):
        dosya.write(f"{i}. ogrenci\n")

print("1. read() ile dosyanin tamamini okuma:")
with open('ogrenciler.txt', 'r', encoding='utf-8') as dosya:
    # read() tum icerigi tek bir string olarak dondurur
    tum_icerik = dosya.read()
    print(f"Veri tipi: {type(tum_icerik)}")
    print(f"Icerik:\n{tum_icerik}")
# Çıktı:
# 1. read() ile dosyanin tamamini okuma:
# Veri tipi: <class 'str'>
# Icerik:
# 1. ogrenci
# 2. ogrenci
# ...
# 10. ogrenci

print("\n2. readline() ile satir satir okuma:")
with open('ogrenciler.txt', 'r', encoding='utf-8') as dosya:
    # readline() her cagrildiginda bir sonraki satiri okur
    satir1 = dosya.readline()
    satir2 = dosya.readline()
    print(f"1. satir: {satir1.strip()}")
    print(f"2. satir: {satir2.strip()}")
# Çıktı:
# 2. readline() ile satir satir okuma:
# 1. satir: 1. ogrenci
# 2. satir: 2. ogrenci

print("\n3. readlines() ile tum satirlari listeye alma:")
with open('ogrenciler.txt', 'r', encoding='utf-8') as dosya:
    # readlines() tum satirlari bir liste olarak dondurur
    satir_listesi = dosya.readlines()
    print(f"Veri tipi: {type(satir_listesi)}")
    print(f"Liste uzunlugu: {len(satir_listesi)}")
    print(f"Ilk 3 satir: {satir_listesi[:3]}")
# Çıktı:
# 3. readlines() ile tum satirlari listeye alma:
# Veri tipi: <class 'list'>
# Liste uzunlugu: 10
# Ilk 3 satir: ['1. ogrenci\n', '2. ogrenci\n', '3. ogrenci\n']
```


**Kod Açıklaması:**
1. `read()` metodu, dosyanın tüm içeriğini okur ve tek bir `str` (string) nesnesi olarak döndürür. Küçük dosyalar için idealdir.
2. `readline()` metodu, her çağrıldığında dosyadaki bir sonraki satırı okur ve bir `str` olarak döndürür. Büyük dosyaları satır satır işlemek için kullanılır.
3. `readlines()` metodu, dosyadaki tüm satırları okur ve her satırı bir liste elemanı olarak içeren bir `list` döndürür. Her satırın sonunda `\n` (yeni satır) karakteri bulunur.

### NE ZAMAN TERCİH EDİLİR?
- **`read()`:** Dosyanın tamamına aynı anda ihtiyacınız olduğunda ve dosya boyutu küçük olduğunda (örneğin, bir konfigürasyon dosyası).
- **`readline()`:** Dosyayı bellek baskısı olmadan satır satır işlemeniz gerektiğinde (örneğin, büyük bir log dosyasını analiz etmek).
- **`readlines()`:** Dosyanın tüm satırlarına hızlıca erişmeniz ve liste işlemleri yapmanız gerektiğinde (örneğin, bir dosyadaki tüm satırları ters çevirmek). Ancak dosya çok büyükse dikkatli olunmalıdır.

### ALTERNATİFLERİ
Dosyayı bir `for` döngüsü ile doğrudan satır satır okumak da mümkündür. Bu yöntem, `readline()`'a benzer şekilde belleği verimli kullanır ve genellikle en Pythonic yöntem olarak kabul edilir:


```python
with open('ogrenciler.txt', 'r') as dosya:
    for satir in dosya:
        print(satir.strip())
```


### YAYGIN HATALAR
- **`readlines()` ile büyük dosyaları okumak:** Çok büyük dosyalarda `readlines()` tüm dosyayı belleğe yükleyeceği için `MemoryError` (bellek yetersiz) hatası alınabilir. **Çözüm:** Büyük dosyalar için `for satir in dosya:` döngüsünü veya `readline()`'ı tercih edin.


## 4. Dosyaya Veri Yazma: `write()` ve `writelines()`

### TANIM
`write()` metodu, bir dosyaya tek bir string yazmak için kullanılırken, `writelines()` metodu bir liste (veya herhangi bir iterable) içindeki stringleri dosyaya yazmak için kullanılır.

### NEDEN VAR?
Eğer bir dosyaya birden fazla satır yazmak istiyorsak, her satır için ayrı ayrı `write()` çağırmak yerine, tüm satırları bir listede toplayıp tek seferde `writelines()` ile yazmak daha verimli ve kod okunabilirliği açısından daha iyidir.

### NASIL KULLANILIR?


```python
# cikti.txt dosyasina veri yazalim
yazilacak_satirlar = ["Python ogreniyorum.\n", "Bu cok eglenceli!\n", "Dosya islemleri kolay.\n"]

print("1. write() ile tek tek yazma:")
with open('cikti.txt', 'w', encoding='utf-8') as dosya:
    # write() ile her satiri ayri ayri yaziyoruz
    dosya.write("Bu ilk satirdir.\n")
    dosya.write("Bu ikinci satirdir.\n")
print("Dosyaya iki satir yazildi.")

print("\n2. writelines() ile liste olarak yazma:")
with open('cikti.txt', 'a', encoding='utf-8') as dosya:
    # writelines() ile bir listedeki tum elemanlari yaziyoruz
    dosya.writelines(yazilacak_satirlar)
print("Listedeki satirlar dosyaya eklendi.")

print("\nDosyanin son hali:")
with open('cikti.txt', 'r', encoding='utf-8') as dosya:
    print(dosya.read())
# Çıktı:
# 1. write() ile tek tek yazma:
# Dosyaya iki satir yazildi.
#
# 2. writelines() ile liste olarak yazma:
# Listedeki satirlar dosyaya eklendi.
#
# Dosyanin son hali:
# Bu ilk satirdir.
# Bu ikinci satirdir.
# Python ogreniyorum.
# Bu cok eglenceli!
# Dosya islemleri kolay.
```


**Kod Açıklaması:**
1. `write()` ile dosyaya iki ayrı satır yazıyoruz. Her `write()` çağrısı bir string alır.
2. `writelines()` ile `yazilacak_satirlar` listesindeki tüm stringleri dosyaya yazıyoruz. `'a'` (ekleme) modunu kullandığımız için önceki veriler silinmez.
3. **Önemli Not:** `writelines()`, listenin elemanlarına otomatik olarak yeni satır karakteri (`\n`) eklemez. Bu nedenle, listedeki her stringin sonunda `\n` olduğundan emin olmalıyız.

### NE ZAMAN TERCİH EDİLİR?
- **`write()`:** Dosyaya bir veya birkaç string yazarken, özellikle de yazılacak veri dinamik olarak oluşturuluyorsa.
- **`writelines()`:** Yazılacak tüm satırlar önceden bir liste (veya tuple, set gibi bir iterable) halinde hazırsa. Örneğin, bir dosyadaki tüm satırları okuyup üzerinde değişiklik yaptıktan sonra tekrar yazmak için idealdir.

### ALTERNATİFLERİ
`print()` fonksiyonunu `file` parametresi ile kullanarak da dosyaya yazabiliriz:


```python
with open('cikti.txt', 'a') as dosya:
    print("Bu satir print ile yazildi.", file=dosya)
```


### YAYGIN HATALAR
- **`writelines()`'e `\n` eklemeyi unutmak:** `writelines()` otomatik olarak satır sonu eklemez. Eğer listedeki stringlerin sonunda `\n` yoksa, tüm veri tek bir satırda birleşir. **Çözüm:** Listeyi oluştururken her elemanın sonuna `\n` ekleyin veya `yazilacak_satirlar = [f"{satir}\n" for satir in yazilacak_satirlar]` gibi bir liste kavrama (list comprehension) kullanın.


## 5. CSV Modülü: Tablo Verilerini İşlemek

### TANIM
CSV (Comma-Separated Values), tablo halindeki verileri metin dosyasında saklamak için kullanılan basit bir dosya formatıdır. Python'un `csv` modülü, bu formatı okumak ve yazmak için kullanışlı araçlar sunar.

### NEDEN VAR?
Verileri virgülle ayırarak manuel olarak okumak/yazmak, özellikle veri içinde virgül, tırnak işareti veya yeni satır gibi özel karakterler varsa, çok karmaşık ve hataya açık bir hale gelir. `csv` modülü, tüm bu özel durumları otomatik olarak halleder. Bu kavram olmasaydı, her geliştirici kendi CSV ayrıştırıcısını (parser) yazmak zorunda kalırdı.

**Günlük Hayat Analojisi:** Bir Excel tablosunu düşünün. CSV dosyası, bu tablonun sütunlarının virgülle, satırlarının ise yeni satırla ayrılmış metin halidir. `csv` modülü de Excel'in bu metni anlaması ve düzenlemesi gibidir.

### NASIL KULLANILIR?
Öncelikle `notlar.csv` adında bir dosya oluşturalım:


```python
# notlar.csv dosyasini olustur
with open('notlar.csv', 'w', encoding='utf-8', newline='') as dosya:
    # csv.writer() ile bir yazici nesnesi olustur
    csv_yazici = csv.writer(dosya)
    # writerow() ile tek bir satir yaz
    csv_yazici.writerow(['Isim', 'Vize', 'Final'])
    csv_yazici.writerow(['Ali', 85, 90])
    csv_yazici.writerow(['Ayse', 92, 95])
    csv_yazici.writerow(['Mehmet', 78, 80])
    csv_yazici.writerow(['Fatma', 88, 85])

print("CSV dosyasi olusturuldu.\n")

print("1. csv.reader ile okuma:")
with open('notlar.csv', 'r', encoding='utf-8') as dosya:
    # csv.reader() ile bir okuyucu nesnesi olustur
    csv_okuyucu = csv.reader(dosya)
    # Her satir bir liste olarak gelir
    for satir in csv_okuyucu:
        print(satir)
# Çıktı:
# 1. csv.reader ile okuma:
# ['Isim', 'Vize', 'Final']
# ['Ali', '85', '90']
# ['Ayse', '92', '95']
# ['Mehmet', '78', '80']
# ['Fatma', '88', '85']

print("\n2. csv.DictReader ile okuma (satirlari sozluk olarak):")
with open('notlar.csv', 'r', encoding='utf-8') as dosya:
    # DictReader, ilk satiri baslik (key) olarak kullanir
    csv_dict_okuyucu = csv.DictReader(dosya)
    for satir in csv_dict_okuyucu:
        # Her satir bir sozluk olarak gelir
        print(f"{satir['Isim']} - Vize: {satir['Vize']}, Final: {satir['Final']}")
# Çıktı:
# 2. csv.DictReader ile okuma (satirlari sozluk olarak):
# Ali - Vize: 85, Final: 90
# Ayse - Vize: 92, Final: 95
# Mehmet - Vize: 78, Final: 80
# Fatma - Vize: 88, Final: 85
```


**Kod Açıklaması:**
1. `csv.writer(dosya)` ile bir yazıcı nesnesi oluşturuyoruz. `writerow()` metodu, bir liste alır ve onu virgüllerle ayırarak dosyaya yazar.
2. `csv.reader(dosya)` ile bir okuyucu nesnesi oluşturuyoruz. Bu nesne üzerinde döngü yapmak, her satırı bir liste olarak döndürür.
3. `csv.DictReader(dosya)` ise daha kullanışlıdır. CSV dosyasının ilk satırını sütun başlıkları olarak kabul eder ve sonraki her satırı, bu başlıkları anahtar (key) olarak kullanan bir sözlük (dictionary) olarak döndürür. Bu, verilere `satir['Isim']` gibi anlamlı isimlerle erişmemizi sağlar.

### NE ZAMAN TERCİH EDİLİR?
- Verileriniz tablo formatındaysa (satırlar ve sütunlar) ve bu verileri Excel, Google Sheets gibi programlarla paylaşacaksanız.
- Veri analizi veya makine öğrenmesi projelerinde sıkça kullanılan bir formattır.

### ALTERNATİFLERİ
CSV dışında, yapılandırılmış veri için JSON, XML, YAML gibi birçok format vardır. CSV, en basit ve en yaygın olanıdır.

### YAYGIN HATALAR
- **`newline=''` parametresini unutmak:** Windows işletim sisteminde, CSV dosyası yazarken `open()` fonksiyonuna `newline=''` parametresini eklemezseniz, dosyada fazladan boş satırlar oluşabilir. **Çözüm:** Her zaman `open('dosya.csv', 'w', newline='')` şek

linde kullanın.

### JSON Modülü

#### 1 TANIM
JSON (JavaScript Object Notation), verileri metin tabanlı bir formatta saklamak ve aktarmak için kullanılan hafif bir veri değişim formatıdır. Python'da `json` modülü, Python nesnelerini (sözlük, liste, string, sayı) JSON formatına dönüştürmeyi (serialization) ve JSON formatındaki verileri Python nesnelerine dönüştürmeyi (deserialization) sağlar.

#### 2 NEDEN VAR?
**Günlük Hayat Analojisi:** Bir restoranın menüsünü düşünün. Menüyü bir kağıda (JSON) yazıyorsunuz. Bu kağıdı başka bir restorana (başka bir program) gönderdiğinizde, onlar da aynı menüyü okuyup anlayabiliyor. JSON, farklı programlama dilleri arasında veri alışverişi yapmak için bir "ortak dil" görevi görür.

**Tarihsel Bağlam:** JSON, 2000'lerin başında Douglas Crockford tarafından tanımlandı ve hızla XML'in yerini alarak web servislerinde (API) standart veri formatı haline geldi. Python'un `json` modülü, Python 2.6 ile birlikte standart kütüphaneye eklendi.

#### 3 NASIL KULLANILIR?
Öncelikle `ayarlar.json` adında bir yapılandırma dosyası oluşturalım ve okuyalım:


```python
import json

# Python sozlugumuz
ayarlar = {
    "uygulama_adi": "Not Defteri",
    "surum": 1.0,
    "yazar": "Python Kursu",
    "tema": "koyu",
    "dil": "tr"
}

# 1. Sozlugu JSON dosyasina yazma (serialization)
with open('ayarlar.json', 'w', encoding='utf-8') as dosya:
    json.dump(ayarlar, dosya, indent=4, ensure_ascii=False)
    # indent=4: dosyayi okunabilir yapar
    # ensure_ascii=False: Turkce karakterleri korur
print("Ayarlar JSON dosyasina yazildi.\n")

# 2. JSON dosyasini Python sozlugune cevirme (deserialization)
with open('ayarlar.json', 'r', encoding='utf-8') as dosya:
    yuklenen_ayarlar = json.load(dosya)
    print("JSON'dan yuklenen ayarlar:")
    print(f"Uygulama: {yuklenen_ayarlar['uygulama_adi']}")
    print(f"Surum: {yuklenen_ayarlar['surum']}")
    print(f"Tema: {yuklenen_ayarlar['tema']}")
# Cikti:
# JSON'dan yuklenen ayarlar:
# Uygulama: Not Defteri
# Surum: 1.0
# Tema: koyu

print("\n3. String uzerinde islem yapma (json.dumps ve json.loads):")
# Bir JSON string'ini Python nesnesine cevirme
json_string = '{"isim": "Ali", "yas": 25}'
python_sozluk = json.loads(json_string)
print(f"Python sozlugu: {python_sozluk}")
print(f"Isim: {python_sozluk['isim']}, Yas: {python_sozluk['yas']}")

# Bir Python nesnesini JSON string'ine cevirme
yeni_json_string = json.dumps(python_sozluk, indent=2, ensure_ascii=False)
print(f"\nJSON stringi:\n{yeni_json_string}")
# Cikti:
# JSON stringi:
# {
#   "isim": "Ali",
#   "yas": 25
# }
```


**Kod Açıklaması:**
1. `json.dump(veri, dosya)`: Bir Python nesnesini (genellikle sözlük) alır, JSON formatına çevirir ve bir dosyaya yazar. `indent=4` parametresi, JSON dosyasını daha okunabilir yapar (güzel yazdırma). `ensure_ascii=False` parametresi, Türkçe karakterlerin (ş, ç, ğ, ö, ü, ı) bozulmadan kaydedilmesini sağlar.
2. `json.load(dosya)`: Bir JSON dosyasını okur ve onu bir Python sözlüğüne (veya uygun türe) dönüştürür.
3. `json.dumps(veri)` ve `json.loads(string)`: Dosya yerine string üzerinde işlem yapmak için kullanılır. `dumps` Python nesnesini JSON string'ine çevirir, `loads` ise JSON string'ini Python nesnesine çevirir.

#### 4 NE ZAMAN TERCİH EDİLİR?
- Program ayarlarını, kullanıcı profillerini veya yapılandırma bilgilerini saklamak için idealdir.
- Web API'leri ile veri alışverişi yaparken neredeyse standarttır.
- Verileriniz hiyerarşik bir yapıya sahipse (iç içe sözlükler ve listeler) CSV'den çok daha uygundur.

#### 5 ALTERNATİFLERİ
| Özellik | JSON | CSV | XML |
|---------|------|-----|-----|
| Veri yapısı | Hiyerarşik (iç içe) | Düz (tablo) | Hiyerarşik (ağaç) |
| Okunabilirlik | Yüksek | Yüksek | Düşük |
| Dosya boyutu | Orta | Küçük | Büyük |
| Karmaşık veri | Uygun | Uygun değil | Uygun |
| Python desteği | Mükemmel (`json` modülü) | İyi (`csv` modülü) | Orta (`xml.etree`) |

#### 6 YAYGIN HATALAR
- **`ensure_ascii=False` parametresini unutmak:** Türkçe karakterler (İ, ğ, ü, ş, ö, ç) JSON dosyasına `\u0130` gibi kaçış dizileri olarak yazılır. **Çözüm:** `json.dump()` veya `json.dumps()` çağrısına `ensure_ascii=False` ekleyin.
- **JSON dosyasının formatının bozuk olması:** JSON, sözlük anahtarlarının çift tırnak (`"`) ile yazılmasını zorunlu kılar. `{'isim': 'Ali'}` geçersizdir, `{"isim": "Ali"}` doğrudur. **Çözüm:** Dosyayı manuel düzenlerken bu kurala dikkat edin.

### try-except-else-finally

#### 1 TANIM
`try-except-else-finally`, çalışma zamanı hatalarını (istisnaları) yakalamak ve programın çökmesini önlemek için kullanılan dört bloklu bir yapıdır. `try` bloğu hata oluşabilecek kodu, `except` bloğu hatayı yakalamayı, `else` bloğu hata oluşmazsa çalışacak kodu, `finally` bloğu ise her durumda çalışacak temizlik kodunu içerir.

#### 2 NEDEN VAR?
**Günlük Hayat Analojisi:** Bir yemek tarifi uyguluyorsunuz. Tarifin bir adımında "fırını 180 dereceye ayarla" yazıyor (`try`). Fırın bozuksa ("hata"), "fırın arızalı, başka bir fırın kullan" diyorsunuz (`except`). Fırın çalışıyorsa, yemeği pişiriyorsunuz (`else`). Her durumda, sonunda fırını temizliyorsunuz (`finally`).

#### 3 NASIL KULLANILIR?


```python
print("1. Temel try-except kullanimi:")
try:
    sayi = int(input("Bir sayi girin: "))  # Hata olusabilir
    sonuc = 10 / sayi                      # Bolme hatasi olusabilir
    print(f"Sonuc: {sonuc}")
except ValueError:
    print("Hata: Gecerli bir sayi girmediniz!")
except ZeroDivisionError:
    print("Hata: Sifira bolme yapamazsiniz!")
# Cikti (ornek):
# Bir sayi girin: 0
# Hata: Sifira bolme yapamazsiniz!

print("\n2. else ve finally bloklari ile:")
try:
    dosya = open('ornek_veri.txt', 'r')
    icerik = dosya.read()
except FileNotFoundError:
    print("Hata: Dosya bulunamadi!")
else:
    # Hata olusmazsa calisir
    print(f"Dosya icerigi:\n{icerik}")
finally:
    # Her durumda calisir (dosya acildiysa kapat)
    try:
        dosya.close()
        print("Dosya kapatildi.")
    except NameError:
        print("Dosya acilmadi, kapatmaya gerek yok.")
# Cikti (dosya varsa):
# Dosya icerigi:
# ...
# Dosya kapatildi.

print("\n3. Birden fazla hatayi tek except'te yakalama:")
try:
    deger = input("Bir sayi girin: ")
    sayi = int(deger)
    sonuc = 100 / sayi
except (ValueError, ZeroDivisionError) as hata:
    print(f"Hata olustu: {hata}")
# Cikti (ornek):
# Bir sayi girin: abc
# Hata olustu: invalid literal for int() with base 10: 'abc'
```


**Kod Açıklaması:**
1. `try` bloğu, hata oluşma ihtimali olan kodu içerir. Eğer bu blokta bir hata oluşursa, Python hemen uygun `except` bloğuna atlar.
2. `except` bloğu, belirli bir hata türünü yakalar. `except ValueError:` sadece değer hatasını, `except ZeroDivisionError:` sadece sıfıra bölme hatasını yakalar. Birden fazla `except` bloğu olabilir.
3. `else` bloğu, `try` bloğunda hiç hata oluşmazsa çalışır. Bu, hatasız durumdaki kodu `try` bloğundan ayırarak daha temiz bir yapı sağlar.
4. `finally` bloğu, hata olsun veya olmasın her durumda çalışır. Genellikle dosya kapatma, veritabanı bağlantısını sonlandırma gibi temizlik işlemleri için kullanılır.
5. `except (Hata1, Hata2) as hata:` ile birden fazla hata türünü tek bir blokta yakalayabilir ve hata mesajına `as` ile erişebilirsiniz.

#### 4 NE ZAMAN TERCİH EDİLİR?
- Her zaman! Özellikle kullanıcı girdisi alırken, dosya işlemleri yaparken, ağ bağlantıları kurarken veya harici kaynaklarla çalışırken mutlaka kullanılmalıdır.
- `else` bloğu, hata oluşmadığında çalışması gereken kodu `try` bloğundan ayırmak için kullanışlıdır.
- `finally` bloğu, kaynakların (dosya, ağ bağlantısı) her koşulda serbest bırakılmasını garanti etmek için idealdir.

#### 5 ALTERNATİFLERİ
| Özellik | try-except | if-else kontrolleri | assert |
|---------|------------|---------------------|--------|
| Kullanım | Hata oluştuğunda | Hata oluşmadan önce | Geliştirme aşamasında |
| Performans | Hata durumunda yavaş | Her zaman aynı hız | Debug modunda çalışır |
| Okunabilirlik | Yüksek | Orta | Düşük |
| Esneklik | Çok yüksek | Sınırlı | Sınırlı |

#### 6 YAYGIN HATALAR
- **Genel `except` kullanımı:** `except:` (hata türü belirtmeden) kullanmak, tüm hataları gizler ve hata ayıklamayı zorlaştırır. **Çözüm:** Mümkün olduğunca spesifik hata türlerini yakalayın.
- **`finally` bloğunda `return` veya `break` kullanmak:** `finally` bloğu her zaman çalıştığı için, bu blokta `return` veya `break` kullanmak, `try` veya `except` bloklarındaki aynı ifadeleri geçersiz kılar. **Çözüm:** `finally` bloğunda sadece temizlik işlemleri yapın, akışı değiştiren ifadeler kullanmayın.

### raise

#### 1 TANIM
`raise` anahtar kelimesi, belirli bir koşulda kendi hata sinyallerimizi oluşturmak (fırlatmak) için kullanılır. Bu sayede, programımızın belirli bir noktasında bir hata durumu olduğunu Python'a bildirebiliriz.

#### 2 NEDEN VAR?
**Günlük Hayat Analojisi:** Bir otomobilin gösterge panelindeki uyarı ışıklarını düşünün. Araç, benzin bitmek üzereyken veya motor sıcaklığı yükseldiğinde sizi uyarır (`raise`). Siz de bu uyarıya göre önlem alırsınız (`try-except`).

#### 3 NASIL KULLANILIR?


```python
# notlar.txt dosyasina ogrenci notlarini yazalim
ogrenci_notlari = ["Ali: 85", "Ayse: 92", "Mehmet: 78", "Fatma: 88"]

# 'with' kullanarak dosyayi guvenle acip yaziyoruz
with open('notlar.txt', 'w', encoding='utf-8') as dosya:
    print("Dosyaya notlar yaziliyor...")
    for not_satiri in ogrenci_notlari:
        # Her not satirini dosyaya yaz
        dosya.write(not_satiri + '\n')
    # Burada dosya.close() cagirmamiza gerek yok!
    print("Yazma islemi tamamlandi.")

# 'with' blogu bittigi anda dosya otomatik olarak kapatildi.
# Simdi dosyayi tekrar acip okuyalim.
with open('notlar.txt', 'r', encoding='utf-8') as dosya:
    print("\nDosyadan okunan notlar:")
    for satir in dosya:
        print(satir.strip())  # strip() ile satir sonundaki '\n' karakterini temizliyoruz
# Çıktı:
# Dosyaya notlar yaziliyor...
# Yazma islemi tamamlandi.
#
# Dosyadan okunan notlar:
# Ali: 85
# Ayse: 92
# Mehmet: 78
# Fatma: 88
```

0


0


**Kod Açıklaması:**
1. `raise ValueError("mesaj")` ile belirli bir hata türünde ve özel bir mesajla hata fırlatabiliriz.
2. Fırlattığımız hata, fonksiyonu çağıran yerdeki `try-except` bloğu tarafından yakalanabilir.
3. Hataları "yeniden fırlatmak" (re-raise) için `raise` (parametresiz) kullanabiliriz. Bu, mevcut hatayı daha üst bir seviyeye iletmek için kullanılır.

#### 4 NE ZAMAN TERCİH EDİLİR?
- Bir fonksiyona geçersiz parametreler gönderildiğinde.
- Dosya işlemlerinde, dosya formatı veya içeriği beklendiği gibi değilse.
- Kullanıcı girdisinin belirli kurallara uymadığı durumlarda.

#### 5 ALTERNATİFLERİ
| Özellik | raise | return ile hata kodu | assert |
|---------|-------|----------------------|--------|
| Kullanım | Hata durumunda | Hata durumunda | Debug amaçlı |
| Zorunluluk | Yakalanmalı | Kontrol edilebilir | Devre dışı bırakılabilir |
| Performans | Hata durumunda yavaş | Hızlı | Debug'da yavaş |

#### 6 YAYGIN HATALAR
- **Çok genel hata fırlatmak:** `raise Exception("Hata!")` yerine daha spesifik hata türleri (`ValueError`, `TypeError`, `FileNotFoundError`) kullanmak daha iyidir.
- **Hata mesajını yetersiz bırakmak:** Hata mesajı, sorunun ne olduğunu ve nasıl çözülebileceğini açıklamalıdır.

### Özel Hata Sınıfları

#### 1 TANIM
Özel hata sınıfları, Python'un yerleşik `Exception` sınıfını miras alarak oluşturduğumuz, kendi uygulamamıza özgü hata türleridir. Bu sayede, hataları daha anlamlı bir şekilde sınıflandırabilir ve yönetebiliriz.

#### 2 NEDEN VAR?
**Günlük Hayat Analojisi:** Bir hastanenin acil servisini düşünün. Her hasta farklı bir durumla gelir: kalp krizi, kemik kırığı, zehirlenme. Her durum için farklı bir doktor (farklı bir `except` bloğu) vardır. Özel hata sınıfları da tıpkı bu teşhisler gibi, sorunun kaynağını net bir şekilde belirtir.

#### 3 NASIL KULLANILIR?


```python
# notlar.txt dosyasina ogrenci notlarini yazalim
ogrenci_notlari = ["Ali: 85", "Ayse: 92", "Mehmet: 78", "Fatma: 88"]

# 'with' kullanarak dosyayi guvenle acip yaziyoruz
with open('notlar.txt', 'w', encoding='utf-8') as dosya:
    print("Dosyaya notlar yaziliyor...")
    for not_satiri in ogrenci_notlari:
        # Her not satirini dosyaya yaz
        dosya.write(not_satiri + '\n')
    # Burada dosya.close() cagirmamiza gerek yok!
    print("Yazma islemi tamamlandi.")

# 'with' blogu bittigi anda dosya otomatik olarak kapatildi.
# Simdi dosyayi tekrar acip okuyalim.
with open('notlar.txt', 'r', encoding='utf-8') as dosya:
    print("\nDosyadan okunan notlar:")
    for satir in dosya:
        print(satir.strip())  # strip() ile satir sonundaki '\n' karakterini temizliyoruz
# Çıktı:
# Dosyaya notlar yaziliyor...
# Yazma islemi tamamlandi.
#
# Dosyadan okunan notlar:
# Ali: 85
# Ayse: 92
# Mehmet: 78
# Fatma: 88
```

1


1


**Kod Açıklaması:**
1. `class DosyaHatasi(Exception):` ile `Exception` sınıfından miras alan yeni bir hata sınıfı tanımlıyoruz.
2. `__init__` metodunda, hata sınıfımıza özel parametreler (örneğin `dosya_adi`) ekleyebiliriz.
3. `super().__init__()` ile ana sınıfın yapıcı metodunu çağırarak hata mesajını belirliyoruz.
4. Özel hata sınıflarımızı, tıpkı yerleşik hata sınıfları gibi `raise` ile fırlatabiliyor ve `except` ile yakalayabiliyoruz.

#### 4 NE ZAMAN TERCİH EDİLİR?
- Uygulamanızda belirli bir işlevsellikle ilgili (dosya işlemleri, veritabanı, ağ) birden fazla hata durumu varsa.
- Hataları daha anlamlı bir şekilde kategorize etmek ve yönetmek istiyorsanız.
- Kullanıcıya veya diğer geliştiricilere daha açıklayıcı hata mesajları vermek istiyorsanız.

#### 5 ALTERNATİFLERİ
| Özellik | Özel Hata Sınıfı | Yerleşik Hata Sınıfı | Genel Exception |
|---------|------------------|----------------------|-----------------|
| Anlamlılık | Çok yüksek | Yüksek | Düşük |
| Esneklik | Çok yüksek | Sınırlı | Sınırlı |
| Karmaşıklık | Orta | Düşük | Çok düşük |
| Bakım | Kolay | Kolay | Zor |

#### 6 YAYGIN HATALAR
- **Gereksiz yere özel hata sınıfı oluşturmak:** Python'un yerleşik hata sınıfları (ValueError, TypeError, FileNotFoundError) çoğu durum için yeterlidir. Sadece gerçekten özel bir durum olduğunda yeni bir sınıf oluşturun.
- **Hata sınıfına yetersiz bilgi eklemek:** Hata sınıfınız, hatanın kaynağını ve çözüm yolunu bulmayı kolaylaştıracak kadar bilgi içermelidir.


## BÖLÜM ÖZETİ

Bu bölümde, Python'da dosya işlemleri ve hata yönetimi konularını detaylı bir şekilde inceledik:

1. **Dosya Açma Modları:** `r`, `w`, `a`, `r+`, `w+`, `a+` modlarının her birinin ne zaman ve nasıl kullanılacağını öğrendik.

2. **with Context Manager:** Dosyaları otomatik olarak açıp kapatan, kaynak yönetimini garanti altına alan bu yapının önemini kavradık.

3. **Okuma Yöntemleri:** `read()`, `readline()`, `readlines()` arasındaki farkları ve hangi durumda hangisinin tercih edileceğini gördük.

4. **Yazma Yöntemleri:** `write()` ve `writelines()` ile dosyaya veri yazma tekniklerini öğrendik.

5. **CSV Modülü:** Tablo verilerini okumak ve yazmak için `csv` modülünü, özellikle `csv.reader`, `csv.writer` ve `csv.DictReader` sınıflarını kullanmayı öğrendik.

6. **JSON Modülü:** Yapılandırma dosyaları ve web servisleri için vazgeçilmez olan JSON formatını, `json.dump()`, `json.load()`, `json.dumps()`, `json.loads()` fonksiyonlarıyla kullanmayı öğrendik.

7. **try-except-else-finally:** Hata yönetiminin dört bloklu yapısını, her bloğun hangi durumda çalıştığını ve nasıl kullanılacağını gördük.

8. **raise:** Belirli koşullarda kendi hata sinyallerimizi nasıl oluşturacağımızı öğrendik.

9. **Özel Hata Sınıfları:** Uygulamaya özgü hata türleri oluşturarak daha anlamlı ve yönetilebilir hata yönetimi yapmayı öğrendik.

## SÖZLÜK

| Terim | Anlamı |
|-------|--------|
| **Context Manager** | Kaynakları otomatik olarak yöneten, `with` anahtar kelimesiyle kullanılan yapı |
| **Serialization** | Python nesnelerini (sözlük, liste) metin formatına (JSON, CSV) dönüştürme |
| **Deserialization** | Metin formatındaki verileri Python nesnelerine dönüştürme |
| **İstisna (Exception)** | Çalışma zamanında oluşan hata durumu |
| **Yeniden Fırlatma (Re-raise)** | Yakalanan bir hatayı daha üst seviyeye iletme |
| **Encoding** | Karakterlerin sayısal değerlere dönüştürülme şekli (utf-8, latin-5) |
| **Buffer** | Verilerin geçici olarak depolandığı bellek alanı |
| **CSV** | Virgülle Ayrılmış Değerler (Comma-Separated Values) |
| **JSON** | JavaScript Object Notation |

## SORULAR

1. `r+` ve `w+` modları arasındaki temel fark nedir?
2. `with` anahtar kelimesi olmadan dosya işlemi yapmanın riskleri nelerdir?
3. `read()` ve `readlines()` arasındaki farkı açıklayın.
4. CSV dosyası yazarken `newline=''` parametresini kullanmanın önemi nedir?
5. JSON dosyasında Türkçe karakterlerin bozulmaması için hangi parametre kullanılır?
6. `try-except-else-finally` yapısında `else` bloğu hangi durumda çalışır?
7. Özel hata sınıfı oluşturmanın avantajları nelerdir?

## ALIŞTIRMALAR

1. **Öğrenci Not Defteri:** Kullanıcıdan öğrenci adı, vize ve final notlarını alarak `notlar.csv` dosyasına yazan bir program yazın.

2. **JSON Konfigürasyon Yöneticisi:** Bir programın ayarlarını (tema, dil, pencere boyutu) JSON dosyasında saklayan ve okuyan bir modül yazın.

3. **Güvenli Dosya Okuyucu:** Kullanıcıdan bir dosya adı alan, dosyayı okumaya çalışan ve olası tüm hataları (dosya bulunamadı, izin hatası, kodlama hatası) yakalayan bir program yazın.

4. **Özel Hata ile Veri Doğrulama:** Kullanıcıdan alınan e-posta adresini doğrulayan, geçersiz format için `GecersizEmailHatasi` adlı özel bir hata fırlatan bir fonksiyon yazın.

## YAYGIN HATALAR VE ÇÖZÜMLERİ

| Hata | Açıklama | Çözüm |
|------|----------|-------|
| `FileNotFoundError` | Dosya mevcut değil | Dosyanın varlığını kontrol edin veya `try-except` ile yakalayın |
| `PermissionError` | Dosyaya erişim izniniz yok | Dosya izinlerini kontrol edin veya yönetici olarak çalıştırın |
| `UnicodeDecodeError` | Yanlış kodlama | `open()` fonksiyonunda `encoding='utf-8'` parametresini kullanın |
| `ValueError` | Geçersiz değer | Girdi doğrulaması yapın |
| `TypeError` | Yanlış veri türü | Veri türlerini kontrol edin |
| `ZeroDivisionError` | Sıfıra bölme | Bölme işleminden önce paydayı kontrol edin |

## KAYNAKLAR

- Python Resmi Dokümantasyonu: Dosya İşlemleri
- Python Resmi Dokümantasyonu: csv Modülü
- Python Resmi Dokümantasyonu: json Modülü
- Python Resmi Dokümantasyonu: Hata Yönetimi
- Real Python: Python File Handling
- Real Python: Working With JSON Data in Python

## Bir sonraki bolume kopru

Bu bölümde dosyalarla güvenli ve etkili çalışmanın temellerini attınız. Artık `with` bloklarıyla kaynakları otomatik yönetebiliyor, CSV gibi yapılandırılmış verileri okuyup yazabiliyorsunuz. Bir sonraki bölümde, bu dosya işleme becerilerinizi kullanarak **büyük veri kümelerini işlemeyi** ve **veritabanı bağlantıları** kurmayı öğreneceksiniz; böylece programlarınız yalnızca metin dosyalarıyla değil, profesyonel veri kaynaklarıyla da çalışabilecek.
