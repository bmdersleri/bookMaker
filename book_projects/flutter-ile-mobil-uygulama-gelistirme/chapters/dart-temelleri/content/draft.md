---
chapter_id: dart-temelleri
chapter_no: 3
title: "Dart Temelleri"
artifact_type: chapter
artifact_version: project-based
language: tr
---

# Flutter İçin Dart Temelleri

## Bölümün Yol Haritası

Bu bölümde Flutter uygulamalarını anlayabilmek ve yazabilmek için gerekli Dart temelleri ele alınmaktadır. Flutter arayüzleri widget tabanlı olsa da bu widget'ların tamamı Dart diliyle ifade edilir. Bu nedenle Dart sözdizimini, değişken kullanımını, null-safety yaklaşımını, koleksiyonları, fonksiyonları, sınıfları ve temel async yapısını bilmek Flutter öğrenme sürecinin zorunlu bir parçasıdır.

Bu bölümün amacı okuyucuyu ileri düzey Dart programcısı yapmak değildir. Amaç, Flutter kodlarını okuyabilecek, küçük bileşenler yazabilecek, basit model sınıfları oluşturabilecek ve bir ekranda kullanılacak örnek veri listesini Dart ile hazırlayabilecek düzeye getirmektir.

Bu bölümde özellikle şu konulara odaklanılacaktır:

- Dart'ın Flutter içindeki rolü
- `main()` fonksiyonu
- Değişken tanımlama
- `var`, `final` ve `const` farkı
- Temel veri tipleri
- Null-safety mantığı
- List ve Map kullanımı
- Fonksiyon tanımlama
- Class ve constructor kullanımı
- Basit model sınıfı tasarımı
- `Future`, `async` ve `await` kavramlarına giriş
- Dart model sınıfından beslenen basit liste ekranı

Bu bölümde Dart isolate, metaprogramlama ve Dart package geliştirme gibi ileri konulara girilmeyecektir. Bu konular kitabın kapsamı dışındadır.

---

## Kavramsal Açıklama

### Dart Neden Flutter İçin Önemlidir?

Flutter uygulamalarında ekranda gördüğümüz her yapı Dart kodu ile oluşturulur. Bir metin göstermek, buton eklemek, bir liste üretmek, bir model sınıfından veri okumak veya kullanıcı etkileşimine cevap vermek Dart dilinin temel yapılarını kullanmayı gerektirir.

Örneğin Flutter'da aşağıdaki gibi bir `Text` widget'ı yazıldığında:

```dart
Text('Merhaba Flutter')
```

buradaki metin değeri, fonksiyon çağrısı, parametre verme biçimi ve nesne oluşturma mantığı Dart sözdiziminin parçasıdır. Bu nedenle Flutter öğrenirken Dart konularını tamamen atlamak mümkün değildir.

### `main()` Fonksiyonu

Dart programlarında çalışmanın başladığı nokta `main()` fonksiyonudur.

<!-- CODE_META
id: b02_kod_01_main_fonksiyonu
language: dart
validation_mode: dart_analyze
-->
```dart
void main() {
  print('Merhaba Dart');
}
```

Bu örnekte `void`, fonksiyonun geriye değer döndürmediğini belirtir. `print()` fonksiyonu ise konsola çıktı yazdırmak için kullanılır.

### Değişkenler

Dart'ta değişken tanımlamak için açık tür belirtilebilir veya `var` anahtar kelimesi kullanılabilir.

<!-- CODE_META
id: b02_kod_02_degiskenler
language: dart
validation_mode: dart_analyze
-->
```dart
void main() {
  String ad = 'Elif';
  int yas = 21;
  double ortalama = 3.42;
  bool aktifMi = true;

  print(ad);
  print(yas);
  print(ortalama);
  print(aktifMi);
}
```

Dart güçlü tip denetimine sahip bir dildir. Bu nedenle `int` olarak tanımlanan bir değişkene daha sonra metin değeri atanamaz.

### `var`, `final` ve `const`

Dart'ta değişken tanımlarken sık karşılaşılan üç kullanım vardır: `var`, `final` ve `const`.

| Anahtar Kelime | Anlamı | Kullanım Durumu |
|---|---|---|
| `var` | Türü ilk atanan değerden çıkarır. | Değeri sonradan değişebilen değişkenler |
| `final` | Değer yalnızca bir kez atanır. | Çalışma zamanında belirlenen sabit değerler |
| `const` | Derleme zamanında sabit olmalıdır. | Gerçek sabit değerler |

<!-- CODE_META
id: b02_kod_03_final_const
language: dart
validation_mode: dart_analyze
-->
```dart
void main() {
  var bolum = 'Bilgisayar Programcılığı';
  bolum = 'Yazılım Geliştirme';

  final kayitTarihi = DateTime.now();

  const kurum = 'MAKÜ';

  print(bolum);
  print(kayitTarihi);
  print(kurum);
}
```

Burada `kayitTarihi` çalışma zamanında oluştuğu için `final` ile tanımlanır. `kurum` değeri ise değişmeyen bir metin sabiti olduğu için `const` ile tanımlanabilir.

### Null-Safety

Dart'ta null-safety, bir değişkenin `null` değer alıp alamayacağını açık biçimde belirtmeyi sağlar. Varsayılan olarak değişkenler `null` olamaz.

<!-- CODE_META
id: b02_kod_04_null_safety
language: dart
validation_mode: dart_analyze
-->
```dart
void main() {
  String ad = 'Yasemin';
  String? ikinciAd;

  print(ad);
  print(ikinciAd);
}
```

`String?` ifadesi, bu değişkenin metin değeri alabileceği gibi `null` da olabileceğini gösterir.

Null değeri kullanılmadan önce kontrol edilmelidir:

```dart
void main() {
  String? kullaniciAdi;

  if (kullaniciAdi == null) {
    print('Kullanıcı adı henüz girilmedi.');
  } else {
    print('Kullanıcı adı: $kullaniciAdi');
  }
}
```

Flutter uygulamalarında null-safety özellikle form alanları, opsiyonel kullanıcı bilgileri, API'den gelebilecek eksik veriler ve model sınıflarında önemlidir.

### List ve Map

Dart'ta birden fazla veriyi tutmak için koleksiyon yapıları kullanılır. En yaygın iki yapı `List` ve `Map` türleridir.

`List`, sıralı veri tutar:

<!-- CODE_META
id: b02_kod_05_list
language: dart
validation_mode: dart_analyze
-->
```dart
void main() {
  final dersler = <String>[
    'Flutter',
    'Dart',
    'Mobil Programlama',
  ];

  for (final ders in dersler) {
    print(ders);
  }
}
```

`Map`, anahtar-değer ilişkisiyle veri tutar:

<!-- CODE_META
id: b02_kod_06_map
language: dart
validation_mode: dart_analyze
-->
```dart
void main() {
  final ogrenci = <String, dynamic>{
    'ad': 'İsmail',
    'yas': 22,
    'aktif': true,
  };

  print(ogrenci['ad']);
  print(ogrenci['yas']);
}
```

Flutter uygulamalarında List yapısı genellikle liste ekranları için, Map yapısı ise JSON benzeri veri yapılarıyla çalışırken karşımıza çıkar.

### Fonksiyonlar

Fonksiyonlar, belirli bir görevi yerine getiren tekrar kullanılabilir kod bloklarıdır.

<!-- CODE_META
id: b02_kod_07_fonksiyonlar
language: dart
validation_mode: dart_analyze
-->
```dart
String selamla(String ad) {
  return 'Merhaba $ad';
}

int ikiSayiyiTopla(int a, int b) {
  return a + b;
}

void main() {
  print(selamla('Bahar'));
  print(ikiSayiyiTopla(12, 8));
}
```

Flutter'da fonksiyonlar; buton tıklamalarında, veri dönüştürme işlemlerinde, validasyonlarda ve küçük yardımcı işlemlerde sık kullanılır.

### Class ve Constructor

Dart nesne yönelimli bir dildir. Flutter uygulamalarında verileri düzenli temsil etmek için model sınıfları kullanılır.

<!-- CODE_META
id: b02_kod_08_model_sinifi
language: dart
validation_mode: dart_analyze
-->
```dart
class Ders {
  final String ad;
  final int kredi;
  final bool zorunluMu;

  const Ders({
    required this.ad,
    required this.kredi,
    required this.zorunluMu,
  });
}

void main() {
  const ders = Ders(
    ad: 'Flutter ile Mobil Programlama',
    kredi: 4,
    zorunluMu: true,
  );

  print(ders.ad);
  print(ders.kredi);
  print(ders.zorunluMu);
}
```

Bu örnekte `Ders` adlı bir model sınıfı tanımlanmıştır. `final` alanlar, nesne oluşturulduktan sonra değiştirilemeyen değerleri ifade eder. `required` ifadesi ise ilgili parametrenin nesne oluşturulurken verilmesini zorunlu kılar.

### Future, Async ve Await

Flutter uygulamalarında bazı işlemler hemen sonuçlanmaz. Örneğin dosya okuma, ağ isteği yapma veya veritabanından veri çekme gibi işlemler zaman alabilir. Dart'ta bu tür işlemleri temsil etmek için `Future` kullanılır.

<!-- CODE_META
id: b02_kod_09_future_async_await
language: dart
validation_mode: dart_analyze
-->
```dart
Future<String> kullaniciAdiniGetir() async {
  await Future.delayed(const Duration(seconds: 1));
  return 'Elif';
}

Future<void> main() async {
  final ad = await kullaniciAdiniGetir();
  print('Kullanıcı: $ad');
}
```

Bu bölümde `async` yapısı yalnızca temel düzeyde tanıtılmıştır. API kullanımı ve JSON veri işleme ilerleyen bölümlerde ayrıntılı olarak ele alınacaktır.

---

## Temel Örnek

Bu bölümün temel örneğinde bir ders model sınıfı oluşturulacak ve bu modelden üretilen liste konsola yazdırılacaktır.

<!-- CODE_META
id: b02_kod_10_ders_listesi
language: dart
validation_mode: dart_analyze
-->
```dart
class Ders {
  final String ad;
  final String ogretimElemani;
  final int haftaSayisi;

  const Ders({
    required this.ad,
    required this.ogretimElemani,
    required this.haftaSayisi,
  });

  String ozet() {
    return '$ad - $ogretimElemani - $haftaSayisi hafta';
  }
}

void main() {
  const dersler = <Ders>[
    Ders(
      ad: 'Flutter ile Mobil Programlama',
      ogretimElemani: 'Prof. Dr. İsmail Kırbaş',
      haftaSayisi: 14,
    ),
    Ders(
      ad: 'Dart Temelleri',
      ogretimElemani: 'Prof. Dr. İsmail Kırbaş',
      haftaSayisi: 2,
    ),
  ];

  for (final ders in dersler) {
    print(ders.ozet());
  }
}
```

Bu örnekte birkaç önemli Dart özelliği birlikte kullanılmıştır:

- `class` ile model tanımlama
- `final` alanlarla değişmez veri yapısı oluşturma
- `const` constructor kullanma
- Liste içinde nesne saklama
- `for-in` döngüsü ile liste üzerinde dolaşma
- Sınıf içinde metot tanımlama

Bu yapı, ilerleyen Flutter uygulamalarında ekranlara veri sağlamak için kullanılacak yaklaşımın temelidir.

---

## Çalışan Mini Uygulama

Bu mini uygulamada Dart model sınıfından beslenen basit bir Flutter liste ekranı hazırlanacaktır. Amaç, Dart'ta tanımlanan model sınıfının Flutter arayüzünde nasıl kullanılabileceğini göstermektir.

Aşağıdaki kod `lib/main.dart` dosyasına yazılabilir.

<!-- CODE_META
id: b02_kod_11_flutter_model_liste_ekrani
language: dart
validation_mode: flutter_analyze
-->
```dart
import 'package:flutter/material.dart';

void main() {
  runApp(const DersListesiUygulamasi());
}

class Ders {
  final String ad;
  final String aciklama;
  final int hafta;

  const Ders({
    required this.ad,
    required this.aciklama,
    required this.hafta,
  });
}

class DersListesiUygulamasi extends StatelessWidget {
  const DersListesiUygulamasi({super.key});

  static const List<Ders> dersler = [
    Ders(
      ad: 'Dart Temelleri',
      aciklama: 'Flutter kodlarını anlamak için gerekli dil temelleri.',
      hafta: 2,
    ),
    Ders(
      ad: 'Widget Mantığı',
      aciklama: 'Flutter arayüzlerinin yapı taşlarını tanıma.',
      hafta: 3,
    ),
    Ders(
      ad: 'Layout Sistemi',
      aciklama: 'Row, Column, Container ve hizalama yaklaşımları.',
      hafta: 4,
    ),
  ];

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Dart Model Listesi',
      debugShowCheckedModeBanner: false,
      home: Scaffold(
        appBar: AppBar(
          title: const Text('Dart Modelinden Liste'),
        ),
        body: ListView.builder(
          itemCount: dersler.length,
          itemBuilder: (context, index) {
            final ders = dersler[index];

            return ListTile(
              leading: CircleAvatar(
                child: Text('${ders.hafta}'),
              ),
              title: Text(ders.ad),
              subtitle: Text(ders.aciklama),
            );
          },
        ),
      ),
    );
  }
}
```

Bu örnek, Flutter arayüzüne geçmeden önce Dart model sınıfının neden önemli olduğunu gösterir. `Ders` sınıfı, ekranda gösterilecek verinin düzenli biçimde temsil edilmesini sağlar. `dersler` listesi ise bu modelden oluşturulmuş sabit bir veri kümesidir.

`ListView.builder`, listedeki her öğe için bir `ListTile` üretir. Bu bölümde `ListView.builder` ayrıntılı olarak incelenmemektedir; yalnızca Dart listesinin Flutter ekranında nasıl kullanılabileceğini göstermek için kullanılmıştır.

[SCREENSHOT:b02_01_dart_model_liste_ekrani]

<!-- SCREENSHOT_META
id: b02_01_dart_model_liste_ekrani
chapter_id: chapter_03
title: "Dart Model Liste Ekrani"
kind: browser_page
url: "http://127.0.0.1:5173/__book__/dart-temelleri/b02_01_dart_model_liste_ekrani"
viewport: 1440x900
wait_for: "networkidle"
output_file: assets/auto/screenshots/b02_01_dart_model_liste_ekrani.png
caption: "Dart Model Liste Ekrani ekran görüntüsü."
validation_mode: capture
-->

**Şekil 2.1.** Dart model sınıfından beslenen basit Flutter liste ekranı.

---

## Sık Yapılan Hatalar

### `final` ve `const` Kavramlarını Karıştırmak

Yeni başlayanlar `final` ve `const` kavramlarını sıkça karıştırır. `final`, değerin yalnızca bir kez atanacağını belirtir. `const` ise değerin derleme zamanında sabit olması gerektiğini ifade eder.

Hatalı kullanım:

```dart
final tarih = DateTime.now();
```

Bu kullanım doğrudur. Ancak aynı ifade `const` ile yazılamaz:

```dart
const tarih = DateTime.now();
```

Çünkü `DateTime.now()` çalışma zamanında hesaplanır.

### Null Olabilecek Değeri Doğrudan Kullanmak

Null-safety yapısında `String?` gibi nullable bir değeri kontrol etmeden kullanmak hataya yol açabilir.

Doğru yaklaşım:

```dart
void main() {
  String? ad;

  if (ad != null) {
    print(ad.length);
  } else {
    print('Ad bilgisi yok.');
  }
}
```

### Liste Elemanına Yanlış İndeksle Erişmek

Listelerde indeksler sıfırdan başlar. Üç elemanlı bir listenin son elemanı `liste[2]` ile alınır. `liste[3]` hatalıdır.

```dart
void main() {
  final sehirler = ['Burdur', 'Isparta', 'Antalya'];

  print(sehirler[0]);
  print(sehirler[2]);
}
```

### Model Sınıfı Yerine Dağınık Map Kullanmak

Küçük örneklerde Map kullanımı kolay görünse de uygulama büyüdükçe model sınıfı daha okunabilir ve güvenli bir yapı sağlar.

Dağınık kullanım:

```dart
final ders = {
  'ad': 'Flutter',
  'hafta': 4,
};
```

Daha düzenli kullanım:

```dart
class Ders {
  final String ad;
  final int hafta;

  const Ders({
    required this.ad,
    required this.hafta,
  });
}
```

### Async Fonksiyonu Beklemeden Kullanmak

`Future` döndüren bir fonksiyonun sonucu gerekiyorsa `await` kullanılmalıdır.

```dart
Future<String> veriGetir() async {
  return 'Veri hazır';
}

Future<void> main() async {
  final sonuc = await veriGetir();
  print(sonuc);
}
```

---

## Bölüm Sonu Laboratuvarı

### Laboratuvar Görevi: Ders Modelinden Liste Ekranı Oluşturma

Bu laboratuvar görevinde öğrenciden Dart model sınıfı oluşturarak bu sınıftan beslenen basit bir Flutter liste ekranı geliştirmesi beklenmektedir.

### Amaç

Öğrencinin Dart değişkenleri, `final/const`, List, class, constructor ve basit Flutter liste ekranı ilişkisini uygulamalı olarak kavraması.

### Görev Adımları

1. `dart_model_liste_lab` adlı yeni bir Flutter projesi oluşturun.
2. `lib/main.dart` dosyasını sadeleştirin.
3. `Ders` veya `HayvanKaydi` adlı bir model sınıfı oluşturun.
4. Model sınıfında en az üç alan bulunsun.
5. Bu modelden en az dört örnek içeren bir `List` oluşturun.
6. Listeyi `ListView.builder` ile ekranda gösterin.
7. Her liste elemanında başlık ve açıklama metni bulunsun.
8. Uygulamayı Chrome, emulator veya fiziksel cihaz üzerinde çalıştırın.
9. Ekran görüntüsünü `bolum02_dart_model_liste.png` adıyla kaydedin.
10. 5-8 cümlelik kısa bir açıklama yazın: “Bu uygulamada Dart model sınıfı neden kullanıldı?”

### Beklenen Çıktı

Öğrencinin uygulamasında model sınıfından üretilmiş bir veri listesi ekranda okunabilir biçimde gösterilmelidir.

### Teslim Edilecekler

- `lib/main.dart`
- Uygulama ekran görüntüsü
- Kısa açıklama notu

### Değerlendirme Rubriği

| Ölçüt | Açıklama | Puan |
|---|---|---:|
| Model sınıfı | En az üç alana sahip doğru bir Dart model sınıfı oluşturulmuştur. | 20 |
| Constructor kullanımı | `required`, `final` ve constructor yapısı doğru kullanılmıştır. | 15 |
| Liste oluşturma | Model sınıfından en az dört örnek içeren bir liste hazırlanmıştır. | 15 |
| Flutter ekranı | Liste verileri Flutter arayüzünde doğru gösterilmiştir. | 20 |
| Kod okunabilirliği | Kod düzenli, anlaşılır ve gereksiz karmaşıklıktan uzaktır. | 10 |
| Ekran çıktısı | Uygulama çalıştırılmış ve ekran görüntüsü alınmıştır. | 10 |
| Açıklama notu | Öğrenci model sınıfı kullanım amacını doğru açıklamıştır. | 10 |
| **Toplam** |  | **100** |

---

## Özet

Bu bölümde Flutter geliştirme sürecinde gerekli Dart temelleri ele alındı. `main()` fonksiyonu, değişkenler, temel veri tipleri, `var`, `final`, `const`, null-safety, List, Map, fonksiyonlar, class ve constructor kavramları örneklerle açıklandı. Ayrıca `Future`, `async` ve `await` yapıları giriş düzeyinde tanıtıldı.

Bölümün uygulama tarafında Dart model sınıfından beslenen basit bir Flutter liste ekranı oluşturuldu. Böylece Dart dilinde tanımlanan veri yapılarının Flutter arayüzünde nasıl kullanılabileceği gösterildi.

Bu bölümden sonra okuyucunun Flutter örneklerinde karşılaşacağı temel Dart ifadelerini daha rahat okuyabilmesi ve küçük model sınıfları oluşturabilmesi beklenmektedir. Sonraki bölümde Flutter'ın widget mantığı daha ayrıntılı biçimde ele alınacaktır.
