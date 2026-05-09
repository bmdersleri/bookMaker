---
chapter_id: widget-mantigi
chapter_no: 15
title: "Flutter’da Widget Mantığı"
artifact_type: chapter
artifact_version: project-based
language: tr
---

# Bölüm 3 — Flutter’da Widget Mantığı

## Bölümün Amacı

Bu bölümde Flutter uygulamalarının temel yapı taşı olan **widget** kavramı ele alınmaktadır. Flutter’da ekranda görülen hemen her unsur bir widget olarak modellenir. Metinler, butonlar, satırlar, sütunlar, kartlar, ikonlar, boşluklar, uygulama çubuğu ve hatta sayfanın tamamı widget yaklaşımıyla oluşturulur.

Bölümün temel amacı, öğrencinin Flutter arayüzlerini yalnızca hazır bileşenleri yan yana koyarak değil, arkasındaki düşünme biçimini anlayarak geliştirmesidir. Bu nedenle bölüm boyunca widget ağacı, `build()` metodu, `StatelessWidget`, `StatefulWidget` ve `setState()` kavramları adım adım açıklanacaktır.

Bu bölüm sonunda öğrenci:

- Flutter’da widget kavramını açıklayabilir.
- Widget ağacının nasıl oluştuğunu yorumlayabilir.
- `StatelessWidget` ve `StatefulWidget` arasındaki farkı ayırt edebilir.
- `build()` metodunun görevini açıklayabilir.
- Basit durum değişimlerini `setState()` ile yönetebilir.
- Küçük arayüzleri yeniden kullanılabilir alt widget’lara bölebilir.

## Flutter’da Widget Nedir?

Flutter’da widget, kullanıcı arayüzünün yapı taşıdır. Bir widget, ekranda neyin nasıl görüneceğini veya nasıl yerleşeceğini tanımlayan küçük bir yapı birimi olarak düşünülebilir.

Örneğin aşağıdaki unsurların tamamı widget’tır:

- Bir metin: `Text`
- Bir buton: `ElevatedButton`
- Bir ikon: `Icon`
- Bir satır düzeni: `Row`
- Bir sütun düzeni: `Column`
- Bir boşluk: `SizedBox`
- Bir kart: `Card`
- Bir uygulama iskeleti: `Scaffold`
- Bir uygulama: `MaterialApp`

Flutter’da arayüz geliştirme, widget’ları uygun biçimde iç içe yerleştirme ve gerektiğinde küçük parçalara ayırma sürecidir.

::: {custom-style="Dikkat Kutusu"}
**Dikkat:** Flutter’da widget kavramı yalnızca ekranda görünen nesneleri ifade etmez. Yerleşim, hizalama, tema, boşluk ve davranış gibi birçok unsur da widget yapısı içinde temsil edilir.
:::

## Widget Ağacı

Flutter arayüzleri iç içe geçmiş widget’lardan oluşur. Bu yapı genellikle **widget ağacı** olarak adlandırılır.

Basit bir Flutter uygulaması şu şekilde düşünülebilir:

```text
MaterialApp
└── Scaffold
    ├── AppBar
    │   └── Text
    └── Body
        └── Center
            └── Column
                ├── Text
                ├── SizedBox
                └── ElevatedButton
```

Bu ağaçta en üstte uygulamanın genel yapısını tanımlayan `MaterialApp` bulunur. Sayfa iskeleti `Scaffold` ile kurulur. Uygulama çubuğu `AppBar`, içerik alanı ise genellikle `body` özelliği üzerinden tanımlanır.

Widget ağacını doğru anlamak, Flutter’da hata ayıklama ve arayüz tasarımı açısından kritik öneme sahiptir. Çünkü çoğu arayüz problemi yanlış widget yerleşimi, hatalı parent-child ilişkisi veya gereksiz iç içe geçme nedeniyle ortaya çıkar.

## İlk Basit Widget Örneği

Aşağıdaki örnekte tek görevi ekranda bir metin göstermek olan sade bir Flutter uygulaması bulunmaktadır.

```yaml
CODE_META:
  id: b03_kod01_basit_widget
  chapter: 3
  language: dart
  framework: flutter
  runnable: true
  file: lib/main.dart
  purpose: Basit bir StatelessWidget ile metin gösterimi
```

```dart
import 'package:flutter/material.dart';

void main() {
  runApp(const TemelWidgetUygulamasi());
}

class TemelWidgetUygulamasi extends StatelessWidget {
  const TemelWidgetUygulamasi({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Widget Mantığı',
      home: Scaffold(
        appBar: AppBar(
          title: const Text('Widget Mantığı'),
        ),
        body: const Center(
          child: Text(
            'Flutter arayüzleri widgetlardan oluşur.',
            textAlign: TextAlign.center,
          ),
        ),
      ),
    );
  }
}
```

Bu örnekte dikkat edilmesi gereken ilk nokta, uygulamanın `runApp()` fonksiyonu ile başlatılmasıdır. `runApp()` fonksiyonuna verilen nesne bir widget’tır. Bu örnekte uygulamanın kök widget’ı `TemelWidgetUygulamasi` sınıfıdır.

## `build()` Metodunun Görevi

Flutter’da bir widget’ın ekranda nasıl görüneceğini belirleyen temel metot `build()` metodudur. Bu metot bir `Widget` döndürür.

```dart
@override
Widget build(BuildContext context) {
  return const Text('Merhaba Flutter');
}
```

`build()` metodu, ilgili widget’ın arayüz tanımını üretir. Flutter ihtiyaç duyduğunda bu metodu tekrar çalıştırabilir. Bu nedenle `build()` metodu içinde doğrudan ağır hesaplamalar yapmak veya ağ isteği başlatmak doğru değildir.

::: {custom-style="Ipucu Kutusu"}
**İpucu:** `build()` metodunu, “Bu widget şu anda ekranda nasıl görünmeli?” sorusunun cevabını üreten fonksiyon gibi düşünebilirsiniz.
:::

## `StatelessWidget`

`StatelessWidget`, kendi içinde değişen bir duruma ihtiyaç duymayan widget türüdür. Bu tür widget’lar genellikle dışarıdan aldıkları değerleri ekranda gösterir veya sabit bir arayüz parçası üretir.

Aşağıdaki örnekte öğrenci adını ve bölüm bilgisini gösteren basit bir kart widget’ı hazırlanmıştır.

```yaml
CODE_META:
  id: b03_kod02_stateless_ogrenci_karti
  chapter: 3
  language: dart
  framework: flutter
  runnable: true
  file: lib/main.dart
  purpose: StatelessWidget ile yeniden kullanılabilir kart bileşeni oluşturma
```

```dart
import 'package:flutter/material.dart';

void main() {
  runApp(const OgrenciKartUygulamasi());
}

class OgrenciKartUygulamasi extends StatelessWidget {
  const OgrenciKartUygulamasi({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Öğrenci Kartı',
      home: Scaffold(
        appBar: AppBar(
          title: const Text('StatelessWidget Örneği'),
        ),
        body: const Center(
          child: OgrenciKarti(
            adSoyad: 'Elif Yılmaz',
            bolum: 'Bilgisayar Programcılığı',
            seviye: '1. Sınıf',
          ),
        ),
      ),
    );
  }
}

class OgrenciKarti extends StatelessWidget {
  final String adSoyad;
  final String bolum;
  final String seviye;

  const OgrenciKarti({
    super.key,
    required this.adSoyad,
    required this.bolum,
    required this.seviye,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      margin: const EdgeInsets.all(16),
      child: Padding(
        padding: const EdgeInsets.all(20),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            const Icon(Icons.person, size: 48),
            const SizedBox(height: 12),
            Text(
              adSoyad,
              style: const TextStyle(
                fontSize: 20,
                fontWeight: FontWeight.bold,
              ),
            ),
            const SizedBox(height: 8),
            Text(bolum),
            Text(seviye),
          ],
        ),
      ),
    );
  }
}
```

Bu örnekte `OgrenciKarti` sınıfı dışarıdan üç bilgi almaktadır:

- `adSoyad`
- `bolum`
- `seviye`

Bu bilgiler `final` olarak tanımlanmıştır. Çünkü `StatelessWidget` içinde bu değerlerin widget yaşam süresi boyunca değişmesi beklenmez.

## `StatefulWidget`

Bazı arayüzlerde kullanıcı etkileşimi sonucunda ekranda görünen değerlerin değişmesi gerekir. Örneğin bir sayaç uygulamasında butona basıldıkça ekrandaki sayı artar. Bu tür durumlarda `StatefulWidget` kullanılır.

`StatefulWidget` iki parçadan oluşur:

1. Widget sınıfı
2. State sınıfı

Widget sınıfı genel yapıyı temsil eder. State sınıfı ise değişebilen verileri ve arayüzün güncellenme mantığını içerir.

```yaml
CODE_META:
  id: b03_kod03_stateful_sayac
  chapter: 3
  language: dart
  framework: flutter
  runnable: true
  file: lib/main.dart
  purpose: StatefulWidget ve setState ile sayaç uygulaması
```

```dart
import 'package:flutter/material.dart';

void main() {
  runApp(const SayacUygulamasi());
}

class SayacUygulamasi extends StatelessWidget {
  const SayacUygulamasi({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Sayaç Uygulaması',
      home: const SayacSayfasi(),
    );
  }
}

class SayacSayfasi extends StatefulWidget {
  const SayacSayfasi({super.key});

  @override
  State<SayacSayfasi> createState() => _SayacSayfasiState();
}

class _SayacSayfasiState extends State<SayacSayfasi> {
  int sayac = 0;

  void artir() {
    setState(() {
      sayac++;
    });
  }

  void azalt() {
    setState(() {
      if (sayac > 0) {
        sayac--;
      }
    });
  }

  void sifirla() {
    setState(() {
      sayac = 0;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('StatefulWidget Sayaç'),
      ),
      body: Center(
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            const Text('Güncel sayaç değeri'),
            const SizedBox(height: 8),
            Text(
              '$sayac',
              style: const TextStyle(
                fontSize: 48,
                fontWeight: FontWeight.bold,
              ),
            ),
            const SizedBox(height: 24),
            Wrap(
              spacing: 12,
              children: [
                ElevatedButton(
                  onPressed: azalt,
                  child: const Text('Azalt'),
                ),
                ElevatedButton(
                  onPressed: artir,
                  child: const Text('Artır'),
                ),
                OutlinedButton(
                  onPressed: sifirla,
                  child: const Text('Sıfırla'),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}
```

Bu örnekte `sayac` değişkeni state sınıfı içinde tutulmaktadır. Kullanıcı butona bastığında ilgili fonksiyon çalışır ve `setState()` çağrısı ile Flutter’a arayüzün güncellenmesi gerektiği bildirilir.

## `setState()` Nasıl Çalışır?

`setState()` metodu, Flutter’a ilgili state nesnesindeki bir değerin değiştiğini bildirir. Bu çağrıdan sonra Flutter ilgili widget’ın `build()` metodunu tekrar çalıştırır ve yeni arayüz durumunu üretir.

Aşağıdaki kullanım doğrudur:

```dart
setState(() {
  sayac++;
});
```

Aşağıdaki kullanım ise hatalı bir alışkanlığa dönüşebilir:

```dart
sayac++;
setState(() {});
```

İkinci kullanım teknik olarak bazı durumlarda çalışsa da değişikliğin `setState()` bloğu içinde yapılması daha okunabilir ve daha doğru bir pratiktir.

::: {custom-style="Sinav Notu Kutusu"}
**Sınav Notu:** `setState()` tüm uygulamayı yeniden başlatmaz. İlgili state nesnesinin arayüzünü tekrar üretir. Bu nedenle `setState()` kavramı “ekranı yenile” komutu gibi değil, “bu state değişti, arayüzü yeniden hesapla” bildirimi gibi anlaşılmalıdır.
:::

## Widget Kompozisyonu

Flutter’da iyi arayüz tasarımı, her şeyi tek bir büyük `build()` metodu içine yazmak yerine arayüzü küçük ve anlamlı widget’lara bölmeyi gerektirir. Bu yaklaşıma **widget kompozisyonu** denir.

Aşağıdaki örnekte sayaç ekranı daha küçük widget’lara ayrılmıştır.

```yaml
CODE_META:
  id: b03_kod04_widget_kompozisyonu
  chapter: 3
  language: dart
  framework: flutter
  runnable: true
  file: lib/main.dart
  purpose: Büyük arayüzü küçük widget bileşenlerine ayırma
```

```dart
import 'package:flutter/material.dart';

void main() {
  runApp(const KompozisyonUygulamasi());
}

class KompozisyonUygulamasi extends StatelessWidget {
  const KompozisyonUygulamasi({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Widget Kompozisyonu',
      home: const PuanSayfasi(),
    );
  }
}

class PuanSayfasi extends StatefulWidget {
  const PuanSayfasi({super.key});

  @override
  State<PuanSayfasi> createState() => _PuanSayfasiState();
}

class _PuanSayfasiState extends State<PuanSayfasi> {
  int puan = 50;

  void puanArtir() {
    setState(() {
      if (puan < 100) {
        puan += 5;
      }
    });
  }

  void puanAzalt() {
    setState(() {
      if (puan > 0) {
        puan -= 5;
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Puan Kontrolü'),
      ),
      body: Center(
        child: PuanPaneli(
          puan: puan,
          azalt: puanAzalt,
          artir: puanArtir,
        ),
      ),
    );
  }
}

class PuanPaneli extends StatelessWidget {
  final int puan;
  final VoidCallback azalt;
  final VoidCallback artir;

  const PuanPaneli({
    super.key,
    required this.puan,
    required this.azalt,
    required this.artir,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      margin: const EdgeInsets.all(16),
      child: Padding(
        padding: const EdgeInsets.all(20),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            const Text('Öğrenci Uygulama Puanı'),
            const SizedBox(height: 12),
            Text(
              '$puan',
              style: const TextStyle(
                fontSize: 44,
                fontWeight: FontWeight.bold,
              ),
            ),
            const SizedBox(height: 16),
            LinearProgressIndicator(value: puan / 100),
            const SizedBox(height: 20),
            Row(
              mainAxisSize: MainAxisSize.min,
              children: [
                ElevatedButton(
                  onPressed: azalt,
                  child: const Text('-5'),
                ),
                const SizedBox(width: 12),
                ElevatedButton(
                  onPressed: artir,
                  child: const Text('+5'),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}
```

Bu örnekte `PuanSayfasi` state’i yönetmektedir. `PuanPaneli` ise kendisine verilen değerleri ekrana basan yeniden kullanılabilir bir arayüz bileşenidir.

Bu ayrım önemlidir. Çünkü büyük projelerde her widget’ın kendi görevine odaklanması beklenir. Böylece kod okunabilir, test edilebilir ve sürdürülebilir hâle gelir.

## `const` Kullanımı ve Performans

Flutter’da değişmeyen widget’lar için `const` kullanmak iyi bir pratiktir. `const`, Flutter’ın gereksiz nesne üretimini azaltmasına yardımcı olur.

Örneğin:

```dart
const Text('Merhaba');
```

Aşağıdaki kullanımda ise değer çalışma zamanında değiştiği için `const` kullanılamaz:

```dart
Text('$sayac');
```

Çünkü `sayac` değiştikçe ekrandaki metin de değişecektir.

::: {custom-style="Dikkat Kutusu"}
**Dikkat:** `const` yalnızca performans için değil, kodun niyetini göstermek için de önemlidir. Değişmeyecek widget’ların `const` ile işaretlenmesi kodun okunabilirliğini artırır.
:::

## Mini Uygulama: Etkileşimli Ders Katılım Kartı

Bu mini uygulamada öğrenci katılım durumunu gösteren küçük bir Flutter ekranı hazırlanacaktır. Kullanıcı butona bastığında katılım puanı artacak ve ekrandaki değer güncellenecektir.

[SCREENSHOT:b03_01_katilim_karti]

<!-- SCREENSHOT_META
id: b03_01_katilim_karti
chapter_id: chapter_15
title: "Katilim Karti"
kind: browser_page
url: "http://127.0.0.1:5173/__book__/widget-mantigi/b03_01_katilim_karti"
viewport: 1440x900
wait_for: "networkidle"
output_file: assets/auto/screenshots/b03_01_katilim_karti.png
caption: "Katilim Karti ekran görüntüsü."
validation_mode: capture
-->

```yaml
CODE_META:
  id: b03_kod05_katilim_karti
  chapter: 3
  language: dart
  framework: flutter
  runnable: true
  file: lib/main.dart
  purpose: StatelessWidget, StatefulWidget ve setState kavramlarını bir arada kullanma
  screenshot: b03_01_katilim_karti
```

```dart
import 'package:flutter/material.dart';

void main() {
  runApp(const KatilimUygulamasi());
}

class KatilimUygulamasi extends StatelessWidget {
  const KatilimUygulamasi({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Katılım Kartı',
      theme: ThemeData(
        colorSchemeSeed: Colors.indigo,
        useMaterial3: true,
      ),
      home: const KatilimSayfasi(),
    );
  }
}

class KatilimSayfasi extends StatefulWidget {
  const KatilimSayfasi({super.key});

  @override
  State<KatilimSayfasi> createState() => _KatilimSayfasiState();
}

class _KatilimSayfasiState extends State<KatilimSayfasi> {
  int katilimPuani = 0;

  void katilimEkle() {
    setState(() {
      if (katilimPuani < 100) {
        katilimPuani += 10;
      }
    });
  }

  void sifirla() {
    setState(() {
      katilimPuani = 0;
    });
  }

  String durumMetni() {
    if (katilimPuani >= 80) {
      return 'Çok iyi katılım';
    }

    if (katilimPuani >= 50) {
      return 'Orta düzey katılım';
    }

    return 'Geliştirilmeli';
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Ders Katılım Kartı'),
      ),
      body: Center(
        child: KatilimKarti(
          adSoyad: 'Bahar Demir',
          dersAdi: 'Mobil Programlama',
          puan: katilimPuani,
          durum: durumMetni(),
          katilimEkle: katilimEkle,
          sifirla: sifirla,
        ),
      ),
    );
  }
}

class KatilimKarti extends StatelessWidget {
  final String adSoyad;
  final String dersAdi;
  final int puan;
  final String durum;
  final VoidCallback katilimEkle;
  final VoidCallback sifirla;

  const KatilimKarti({
    super.key,
    required this.adSoyad,
    required this.dersAdi,
    required this.puan,
    required this.durum,
    required this.katilimEkle,
    required this.sifirla,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      margin: const EdgeInsets.all(20),
      child: Padding(
        padding: const EdgeInsets.all(24),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            const Icon(Icons.school, size: 52),
            const SizedBox(height: 12),
            Text(
              adSoyad,
              style: Theme.of(context).textTheme.titleLarge,
            ),
            Text(dersAdi),
            const SizedBox(height: 20),
            Text(
              '$puan / 100',
              style: Theme.of(context).textTheme.displaySmall,
            ),
            const SizedBox(height: 8),
            LinearProgressIndicator(value: puan / 100),
            const SizedBox(height: 12),
            Text(durum),
            const SizedBox(height: 20),
            Wrap(
              spacing: 12,
              children: [
                ElevatedButton.icon(
                  onPressed: katilimEkle,
                  icon: const Icon(Icons.add),
                  label: const Text('Katılım Ekle'),
                ),
                OutlinedButton(
                  onPressed: sifirla,
                  child: const Text('Sıfırla'),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}
```

Bu uygulamada `KatilimSayfasi` değişen puanı yönetmektedir. `KatilimKarti` ise bu bilgileri ekranda gösteren ayrı bir widget olarak tasarlanmıştır. Bu yapı, state yönetimi ile arayüz sunumunun birbirinden ayrılmasını sağlar.

## Sık Yapılan Hatalar

Flutter’da widget mantığını öğrenirken aşağıdaki hatalar sık görülür:

| Hata | Açıklama | Çözüm |
|---|---|---|
| Tüm arayüzü tek `build()` içine yazmak | Kodun okunabilirliği azalır | Küçük widget’lara böl |
| Gereksiz yere `StatefulWidget` kullanmak | Kod karmaşıklaşır | Değişen veri yoksa `StatelessWidget` kullan |
| `setState()` dışında değişiklik yapmak | Arayüz beklenen şekilde güncellenmeyebilir | Değişikliği `setState()` içinde yap |
| `const` kullanmamak | Gereksiz nesne üretimi artabilir | Sabit widget’larda `const` kullan |
| Widget ağacını çok derinleştirmek | Bakım zorlaşır | Kompozisyon ve yardımcı widget kullan |

## Laboratuvar Görevi

Bu laboratuvar çalışmasında öğrenciden küçük bir “Görev Takip Kartı” uygulaması geliştirmesi beklenmektedir.

### İstenenler

1. Uygulama başlığı “Görev Takip Kartı” olmalıdır.
2. Ekranda bir görev adı gösterilmelidir.
3. Görevin tamamlanma yüzdesi gösterilmelidir.
4. `+10` ve `-10` butonları bulunmalıdır.
5. Değer 0 ile 100 arasında tutulmalıdır.
6. Görev kartı ayrı bir `StatelessWidget` olarak tasarlanmalıdır.
7. Değişen yüzde değeri bir `StatefulWidget` içinde yönetilmelidir.
8. Sabit widget’larda mümkün olduğunca `const` kullanılmalıdır.

### Beklenen Kazanımlar

Bu laboratuvar sonunda öğrenci:

- State ile sunum bileşenini ayırabilir.
- `VoidCallback` ile alt widget’a fonksiyon gönderebilir.
- `setState()` ile arayüz güncelleyebilir.
- Küçük ama anlamlı widget kompozisyonu kurabilir.

## Değerlendirme Rubriği

| Ölçüt | Puan | Açıklama |
|---|---:|---|
| Widget yapısının doğruluğu | 20 | `StatelessWidget` ve `StatefulWidget` doğru kullanılmıştır |
| State yönetimi | 20 | Değer değişimleri `setState()` ile yönetilmiştir |
| Arayüz düzeni | 20 | Kart, butonlar ve metinler okunabilir biçimde yerleştirilmiştir |
| Sınır kontrolleri | 15 | Değer 0–100 aralığında tutulmuştur |
| Kod okunabilirliği | 15 | Sınıf ve değişken adları anlamlıdır |
| `const` kullanımı | 10 | Sabit widget’larda `const` tercih edilmiştir |

## Bölüm Özeti

Bu bölümde Flutter’ın temel yapı taşı olan widget kavramı incelendi. Widget ağacının uygulama arayüzünü nasıl oluşturduğu açıklandı. `StatelessWidget` ve `StatefulWidget` arasındaki temel farklar örneklerle gösterildi. `build()` metodunun arayüz üretme görevi, `setState()` metodunun ise değişen state sonrasında arayüzü güncelleme rolü ele alındı.

Bölümün ana fikri şudur: Flutter’da başarılı arayüz geliştirme, widget’ları doğru seçme, doğru konumlandırma ve gerektiğinde küçük bileşenlere ayırma becerisine dayanır. Bu beceri, ilerleyen bölümlerde layout sistemini, formları, listeleri, navigation yapısını ve state management yaklaşımlarını anlamak için temel oluşturacaktır.

## Bölüm Sonu Kontrol Listesi

- [ ] Widget kavramını açıklayabiliyorum.
- [ ] Widget ağacını yorumlayabiliyorum.
- [ ] `StatelessWidget` kullanım amacını biliyorum.
- [ ] `StatefulWidget` kullanım amacını biliyorum.
- [ ] `build()` metodunun görevini açıklayabiliyorum.
- [ ] `setState()` ile basit arayüz güncellemesi yapabiliyorum.
- [ ] Büyük arayüzleri küçük widget’lara bölebiliyorum.
- [ ] Sabit widget’larda `const` kullanmaya dikkat ediyorum.
