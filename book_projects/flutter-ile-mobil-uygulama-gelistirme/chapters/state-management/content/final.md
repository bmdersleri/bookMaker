---
chapter_id: state-management
chapter_no: 12
title: "State Management Temelleri"
artifact_type: chapter
artifact_version: project-based
language: tr
---

# Bölüm 8 — State Management Temelleri

## Bölümün Amacı

Bu bölümde Flutter uygulamalarında state management kavramı ele alınmaktadır. Önceki bölümlerde `StatefulWidget`, `setState()`, formlar, dinamik listeler ve navigation yapısı üzerinde durulmuştu. Bu bölümde ise uygulama verisinin nerede tutulacağı, ne zaman güncelleneceği ve güncellenen verinin arayüze nasıl yansıtılacağı daha sistematik biçimde incelenecektir.

State management, Flutter öğrenen öğrenciler için kritik bir eşiktir. Küçük örneklerde `setState()` yeterli olabilir; ancak uygulama büyüdükçe state’in birden fazla widget arasında paylaşılması, güncelleme mantığının ayrıştırılması ve kodun sürdürülebilir hâle getirilmesi gerekir.

Bu bölüm sonunda öğrenci:

- State kavramını açıklayabilir.
- Local state ve shared state arasındaki farkı ayırt edebilir.
- `setState()` kullanım sınırlarını yorumlayabilir.
- State’i üst widget’a taşıma yaklaşımını uygulayabilir.
- `ValueNotifier` ve `ValueListenableBuilder` ile basit reaktif yapı kurabilir.
- `ChangeNotifier` ile daha düzenli state modeli oluşturabilir.
- `AnimatedBuilder` veya `ListenableBuilder` yaklaşımının mantığını kavrayabilir.
- Küçük bir sepet uygulaması üzerinden state yönetimini uygulayabilir.

## State Nedir?

State, bir uygulamanın belirli bir andaki verisel durumudur. Kullanıcının ekranda gördüğü birçok şey state’e bağlı olarak değişir. Örneğin:

- Sayaç değeri
- Form alanındaki metin
- Seçili sekme
- Tamamlanan görev sayısı
- Kullanıcının giriş yapıp yapmadığı
- Sepetteki ürünler
- Filtrelenmiş liste
- Tema seçimi

Flutter’da arayüz, state’e göre yeniden üretilir. State değiştiğinde Flutter ilgili widget ağacını tekrar değerlendirir ve ekranda gerekli güncellemeleri yapar.

::: {custom-style="Dikkat Kutusu"}
**Dikkat:** State management, yalnızca değişken tanımlamak değildir. Verinin yaşam süresini, kim tarafından değiştirileceğini ve hangi widget’ların bu değişiklikten etkileneceğini tasarlama sürecidir.
:::

## Local State ve Shared State

Flutter uygulamalarında state iki temel düzeyde düşünülebilir:

| State Türü | Açıklama | Örnek |
|---|---|---|
| Local state | Yalnızca tek widget veya küçük bir alanı ilgilendirir | Sayaç değeri, açık/kapalı panel |
| Shared state | Birden fazla widget veya ekran tarafından kullanılır | Kullanıcı bilgisi, sepet verisi, tema seçimi |

Local state için çoğu zaman `StatefulWidget` ve `setState()` yeterlidir. Ancak veri birden fazla widget tarafından kullanılacaksa state’i daha merkezi ve kontrollü yönetmek gerekir.

## `setState()` ile Local State

`setState()`, Flutter’da state yönetiminin en temel yoludur. Küçük ve yerel değişiklikler için oldukça uygundur.

```yaml
CODE_META:
  id: b08_kod01_setstate_local_state
  chapter: 8
  language: dart
  framework: flutter
  runnable: true
  file: lib/main.dart
  purpose: setState ile local state yönetimi
```

```dart
import 'package:flutter/material.dart';

void main() {
  runApp(const LocalStateUygulamasi());
}

class LocalStateUygulamasi extends StatelessWidget {
  const LocalStateUygulamasi({super.key});

  @override
  Widget build(BuildContext context) {
    return const MaterialApp(
      home: LocalStateSayfasi(),
    );
  }
}

class LocalStateSayfasi extends StatefulWidget {
  const LocalStateSayfasi({super.key});

  @override
  State<LocalStateSayfasi> createState() => _LocalStateSayfasiState();
}

class _LocalStateSayfasiState extends State<LocalStateSayfasi> {
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

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Local State'),
      ),
      body: Center(
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Text(
              '$sayac',
              style: Theme.of(context).textTheme.displayMedium,
            ),
            const SizedBox(height: 16),
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
              ],
            ),
          ],
        ),
      ),
    );
  }
}
```

Bu örnekte sayaç değeri yalnızca `LocalStateSayfasi` widget’ını ilgilendirir. Bu nedenle `setState()` yeterli ve anlaşılır bir çözümdür.

## `setState()` Ne Zaman Yetersiz Kalır?

`setState()` basit durumlar için uygundur; ancak şu durumlarda kod karmaşıklaşabilir:

- Aynı state birden fazla widget tarafından kullanılıyorsa
- State birkaç alt widget’a parametre olarak taşınıyorsa
- Liste, filtre, seçim ve hesaplama mantığı aynı sınıfta büyüyorsa
- Birden fazla ekranda aynı veriye ihtiyaç varsa
- İş mantığı ile arayüz kodu birbirine karışıyorsa

Bu durumlarda state’i ayrı sınıflara taşımak veya Flutter’ın `Listenable` tabanlı yapılarını kullanmak daha okunabilir olabilir.

::: {custom-style="Sinav Notu Kutusu"}
**Sınav Notu:** `setState()` kötü bir yöntem değildir. Ancak her problemi `setState()` ile çözmeye çalışmak, büyüyen uygulamalarda bakım maliyetini artırabilir.
:::

## State’i Üst Widget’a Taşımak

Birden fazla alt widget aynı veriye ihtiyaç duyduğunda state üst widget’a taşınabilir. Alt widget’lar veriyi ve fonksiyonları parametre olarak alır.

```yaml
CODE_META:
  id: b08_kod02_state_lifting
  chapter: 8
  language: dart
  framework: flutter
  runnable: true
  file: lib/main.dart
  purpose: State'i üst widget'a taşıma ve alt widget'lara parametre ile aktarma
```

```dart
import 'package:flutter/material.dart';

void main() {
  runApp(const StateLiftingUygulamasi());
}

class StateLiftingUygulamasi extends StatelessWidget {
  const StateLiftingUygulamasi({super.key});

  @override
  Widget build(BuildContext context) {
    return const MaterialApp(
      home: PuanSayfasi(),
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
        puan += 10;
      }
    });
  }

  void puanAzalt() {
    setState(() {
      if (puan > 0) {
        puan -= 10;
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('State Lifting'),
      ),
      body: Center(
        child: PuanPaneli(
          puan: puan,
          artir: puanArtir,
          azalt: puanAzalt,
        ),
      ),
    );
  }
}

class PuanPaneli extends StatelessWidget {
  final int puan;
  final VoidCallback artir;
  final VoidCallback azalt;

  const PuanPaneli({
    super.key,
    required this.puan,
    required this.artir,
    required this.azalt,
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
            Text(
              'Güncel Puan',
              style: Theme.of(context).textTheme.titleMedium,
            ),
            const SizedBox(height: 12),
            Text(
              '$puan',
              style: Theme.of(context).textTheme.displaySmall,
            ),
            const SizedBox(height: 16),
            LinearProgressIndicator(value: puan / 100),
            const SizedBox(height: 20),
            Wrap(
              spacing: 12,
              children: [
                ElevatedButton(
                  onPressed: azalt,
                  child: const Text('-10'),
                ),
                ElevatedButton(
                  onPressed: artir,
                  child: const Text('+10'),
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

Bu örnekte state `PuanSayfasi` içinde tutulur. `PuanPaneli` yalnızca kendisine verilen veriyi gösterir ve butonlara basıldığında üst widget’taki fonksiyonları çağırır. Bu yaklaşım, state yönetiminin daha anlaşılır olmasını sağlar.

## `ValueNotifier` ve `ValueListenableBuilder`

Flutter SDK içinde gelen basit ama güçlü yapılardan biri `ValueNotifier` sınıfıdır. Tek bir değeri izlemek ve değiştiğinde arayüzü güncellemek için kullanılabilir.

`ValueListenableBuilder`, `ValueNotifier` değer değiştiğinde yalnızca ilgili arayüz parçasını yeniden üretir.

```yaml
CODE_META:
  id: b08_kod03_valuenotifier
  chapter: 8
  language: dart
  framework: flutter
  runnable: true
  file: lib/main.dart
  purpose: ValueNotifier ve ValueListenableBuilder ile basit state yönetimi
```

```dart
import 'package:flutter/material.dart';

void main() {
  runApp(const ValueNotifierUygulamasi());
}

class ValueNotifierUygulamasi extends StatelessWidget {
  const ValueNotifierUygulamasi({super.key});

  @override
  Widget build(BuildContext context) {
    return const MaterialApp(
      home: ValueNotifierSayfasi(),
    );
  }
}

class ValueNotifierSayfasi extends StatefulWidget {
  const ValueNotifierSayfasi({super.key});

  @override
  State<ValueNotifierSayfasi> createState() => _ValueNotifierSayfasiState();
}

class _ValueNotifierSayfasiState extends State<ValueNotifierSayfasi> {
  final ValueNotifier<int> sayac = ValueNotifier<int>(0);

  @override
  void dispose() {
    sayac.dispose();
    super.dispose();
  }

  void artir() {
    sayac.value++;
  }

  void sifirla() {
    sayac.value = 0;
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('ValueNotifier'),
      ),
      body: Center(
        child: ValueListenableBuilder<int>(
          valueListenable: sayac,
          builder: (context, deger, child) {
            return Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                Text(
                  '$deger',
                  style: Theme.of(context).textTheme.displayMedium,
                ),
                const SizedBox(height: 20),
                Wrap(
                  spacing: 12,
                  children: [
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
            );
          },
        ),
      ),
    );
  }
}
```

Bu örnekte `setState()` kullanılmamıştır. `sayac.value` değiştiğinde `ValueListenableBuilder` yeniden çalışır ve ekrandaki değer güncellenir.

::: {custom-style="Ipucu Kutusu"}
**İpucu:** `ValueNotifier`, tek değerlik basit state senaryoları için pratik bir çözümdür. Daha karmaşık yapılarda `ChangeNotifier` gibi modeller tercih edilebilir.
:::

## `ChangeNotifier` ile State Modeli

`ChangeNotifier`, birden fazla değeri ve iş mantığını tek bir model sınıfında toplamak için kullanılabilir. State değiştiğinde `notifyListeners()` çağrılır. Bu çağrı, ilgili dinleyicilere state’in değiştiğini bildirir.

```yaml
CODE_META:
  id: b08_kod04_changenotifier
  chapter: 8
  language: dart
  framework: flutter
  runnable: true
  file: lib/main.dart
  purpose: ChangeNotifier ile basit state modeli oluşturma
```

```dart
import 'package:flutter/material.dart';

void main() {
  runApp(const ChangeNotifierUygulamasi());
}

class SayacModeli extends ChangeNotifier {
  int _deger = 0;

  int get deger => _deger;

  void artir() {
    _deger++;
    notifyListeners();
  }

  void azalt() {
    if (_deger > 0) {
      _deger--;
      notifyListeners();
    }
  }

  void sifirla() {
    _deger = 0;
    notifyListeners();
  }
}

class ChangeNotifierUygulamasi extends StatefulWidget {
  const ChangeNotifierUygulamasi({super.key});

  @override
  State<ChangeNotifierUygulamasi> createState() => _ChangeNotifierUygulamasiState();
}

class _ChangeNotifierUygulamasiState extends State<ChangeNotifierUygulamasi> {
  final SayacModeli model = SayacModeli();

  @override
  void dispose() {
    model.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: SayacModelSayfasi(model: model),
    );
  }
}

class SayacModelSayfasi extends StatelessWidget {
  final SayacModeli model;

  const SayacModelSayfasi({
    super.key,
    required this.model,
  });

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('ChangeNotifier'),
      ),
      body: Center(
        child: ListenableBuilder(
          listenable: model,
          builder: (context, child) {
            return Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                Text(
                  '${model.deger}',
                  style: Theme.of(context).textTheme.displayMedium,
                ),
                const SizedBox(height: 20),
                Wrap(
                  spacing: 12,
                  children: [
                    ElevatedButton(
                      onPressed: model.azalt,
                      child: const Text('Azalt'),
                    ),
                    ElevatedButton(
                      onPressed: model.artir,
                      child: const Text('Artır'),
                    ),
                    OutlinedButton(
                      onPressed: model.sifirla,
                      child: const Text('Sıfırla'),
                    ),
                  ],
                ),
              ],
            );
          },
        ),
      ),
    );
  }
}
```

Bu örnekte sayaç verisi ve sayaçla ilgili işlemler `SayacModeli` sınıfında toplanmıştır. Arayüz ise modeli dinleyerek güncellenir. Bu yaklaşım, iş mantığını widget sınıfından ayırmaya yardımcı olur.

## State Modelini Alt Widget’lara Aktarmak

State modeli oluşturulduktan sonra bu model alt widget’lara parametre olarak aktarılabilir. Bu yöntem küçük ve orta ölçekli örneklerde anlaşılırdır.

```yaml
CODE_META:
  id: b08_kod05_modeli_alt_widgetlara_aktarma
  chapter: 8
  language: dart
  framework: flutter
  runnable: true
  file: lib/main.dart
  purpose: ChangeNotifier modelini alt widget'lara parametre olarak aktarma
```

```dart
import 'package:flutter/material.dart';

void main() {
  runApp(const ModelAktarmaUygulamasi());
}

class DersIlerlemeModeli extends ChangeNotifier {
  int _tamamlanan = 2;
  final int toplam = 10;

  int get tamamlanan => _tamamlanan;
  double get oran => _tamamlanan / toplam;

  void artir() {
    if (_tamamlanan < toplam) {
      _tamamlanan++;
      notifyListeners();
    }
  }

  void azalt() {
    if (_tamamlanan > 0) {
      _tamamlanan--;
      notifyListeners();
    }
  }
}

class ModelAktarmaUygulamasi extends StatefulWidget {
  const ModelAktarmaUygulamasi({super.key});

  @override
  State<ModelAktarmaUygulamasi> createState() => _ModelAktarmaUygulamasiState();
}

class _ModelAktarmaUygulamasiState extends State<ModelAktarmaUygulamasi> {
  final DersIlerlemeModeli model = DersIlerlemeModeli();

  @override
  void dispose() {
    model.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: DersIlerlemeSayfasi(model: model),
    );
  }
}

class DersIlerlemeSayfasi extends StatelessWidget {
  final DersIlerlemeModeli model;

  const DersIlerlemeSayfasi({
    super.key,
    required this.model,
  });

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Ders İlerleme'),
      ),
      body: Center(
        child: IlerlemeKarti(model: model),
      ),
    );
  }
}

class IlerlemeKarti extends StatelessWidget {
  final DersIlerlemeModeli model;

  const IlerlemeKarti({
    super.key,
    required this.model,
  });

  @override
  Widget build(BuildContext context) {
    return ListenableBuilder(
      listenable: model,
      builder: (context, child) {
        return Card(
          margin: const EdgeInsets.all(16),
          child: Padding(
            padding: const EdgeInsets.all(20),
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                Text(
                  'Tamamlanan: ${model.tamamlanan} / ${model.toplam}',
                  style: Theme.of(context).textTheme.titleMedium,
                ),
                const SizedBox(height: 12),
                LinearProgressIndicator(value: model.oran),
                const SizedBox(height: 20),
                Wrap(
                  spacing: 12,
                  children: [
                    ElevatedButton(
                      onPressed: model.azalt,
                      child: const Text('Azalt'),
                    ),
                    ElevatedButton(
                      onPressed: model.artir,
                      child: const Text('Artır'),
                    ),
                  ],
                ),
              ],
            ),
          ),
        );
      },
    );
  }
}
```

Bu örnekte `DersIlerlemeModeli`, birden fazla widget tarafından kullanılabilir. Modeldeki değer değiştiğinde `ListenableBuilder` arayüzü yeniden üretir.

## Mini Uygulama: Basit Sepet Yönetimi

Bu mini uygulamada bir ürün listesi ve sepet özeti hazırlanacaktır. Kullanıcı ürünleri sepete ekleyebilecek, sepetten çıkarabilecek ve toplam tutarı görebilecektir.

[SCREENSHOT:b08_01_basit_sepet_state_management]

<!-- SCREENSHOT_META
id: b08_01_basit_sepet_state_management
chapter_id: chapter_12
title: "Basit Sepet State Management"
kind: browser_page
url: "http://127.0.0.1:5173/__book__/state-management/b08_01_basit_sepet_state_management"
viewport: 1440x900
wait_for: "networkidle"
output_file: assets/auto/screenshots/b08_01_basit_sepet_state_management.png
caption: "Basit Sepet State Management ekran görüntüsü."
validation_mode: capture
-->

```yaml
CODE_META:
  id: b08_kod06_basit_sepet_state_management
  chapter: 8
  language: dart
  framework: flutter
  runnable: true
  file: lib/main.dart
  purpose: ChangeNotifier ile ürün listesi ve sepet state yönetimi
  screenshot: b08_01_basit_sepet_state_management
```

```dart
import 'package:flutter/material.dart';

void main() {
  runApp(const SepetUygulamasi());
}

class Urun {
  final String ad;
  final double fiyat;

  const Urun({
    required this.ad,
    required this.fiyat,
  });
}

class SepetModeli extends ChangeNotifier {
  final List<Urun> urunler = const [
    Urun(ad: 'Flutter Kitabı', fiyat: 240),
    Urun(ad: 'Dart Alıştırma Defteri', fiyat: 120),
    Urun(ad: 'Mobil UI Notları', fiyat: 90),
  ];

  final List<Urun> _sepet = [];

  List<Urun> get sepet => List.unmodifiable(_sepet);

  double get toplamTutar {
    return _sepet.fold(
      0,
      (toplam, urun) => toplam + urun.fiyat,
    );
  }

  void sepeteEkle(Urun urun) {
    _sepet.add(urun);
    notifyListeners();
  }

  void sepettenCikar(Urun urun) {
    _sepet.remove(urun);
    notifyListeners();
  }

  int urunAdedi(Urun urun) {
    return _sepet.where((item) => item == urun).length;
  }
}

class SepetUygulamasi extends StatefulWidget {
  const SepetUygulamasi({super.key});

  @override
  State<SepetUygulamasi> createState() => _SepetUygulamasiState();
}

class _SepetUygulamasiState extends State<SepetUygulamasi> {
  final SepetModeli model = SepetModeli();

  @override
  void dispose() {
    model.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Basit Sepet',
      theme: ThemeData(
        colorSchemeSeed: Colors.green,
        useMaterial3: true,
      ),
      home: SepetSayfasi(model: model),
    );
  }
}

class SepetSayfasi extends StatelessWidget {
  final SepetModeli model;

  const SepetSayfasi({
    super.key,
    required this.model,
  });

  @override
  Widget build(BuildContext context) {
    return ListenableBuilder(
      listenable: model,
      builder: (context, child) {
        return Scaffold(
          appBar: AppBar(
            title: const Text('Basit Sepet'),
          ),
          body: Column(
            children: [
              SepetOzeti(model: model),
              Expanded(
                child: ListView.builder(
                  itemCount: model.urunler.length,
                  itemBuilder: (context, index) {
                    final urun = model.urunler[index];

                    return UrunKarti(
                      urun: urun,
                      adet: model.urunAdedi(urun),
                      ekle: () => model.sepeteEkle(urun),
                      cikar: () => model.sepettenCikar(urun),
                    );
                  },
                ),
              ),
            ],
          ),
        );
      },
    );
  }
}

class SepetOzeti extends StatelessWidget {
  final SepetModeli model;

  const SepetOzeti({
    super.key,
    required this.model,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      margin: const EdgeInsets.all(12),
      child: ListTile(
        leading: const Icon(Icons.shopping_cart_outlined),
        title: Text('Sepetteki ürün sayısı: ${model.sepet.length}'),
        subtitle: Text('Toplam tutar: ${model.toplamTutar.toStringAsFixed(2)} TL'),
      ),
    );
  }
}

class UrunKarti extends StatelessWidget {
  final Urun urun;
  final int adet;
  final VoidCallback ekle;
  final VoidCallback cikar;

  const UrunKarti({
    super.key,
    required this.urun,
    required this.adet,
    required this.ekle,
    required this.cikar,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      margin: const EdgeInsets.symmetric(
        horizontal: 12,
        vertical: 6,
      ),
      child: ListTile(
        title: Text(urun.ad),
        subtitle: Text('${urun.fiyat.toStringAsFixed(2)} TL'),
        leading: CircleAvatar(
          child: Text('$adet'),
        ),
        trailing: Wrap(
          spacing: 8,
          children: [
            IconButton(
              onPressed: adet == 0 ? null : cikar,
              icon: const Icon(Icons.remove),
            ),
            IconButton(
              onPressed: ekle,
              icon: const Icon(Icons.add),
            ),
          ],
        ),
      ),
    );
  }
}
```

Bu uygulamada ürün listesi ve sepet içeriği `SepetModeli` içinde tutulmaktadır. Model değiştiğinde `notifyListeners()` çağrılır ve `ListenableBuilder` arayüzü yeniden üretir.

## State Management Yaklaşımı Seçerken

State management için tek bir doğru yöntem yoktur. Seçim; uygulamanın büyüklüğüne, ekibin deneyimine, bağımlılık politikasına ve veri akışının karmaşıklığına göre değişir.

| Durum | Uygun Yaklaşım |
|---|---|
| Tek widget içinde basit değişken | `setState()` |
| Tek değerlik reaktif yapı | `ValueNotifier` |
| Birden fazla değeri olan basit model | `ChangeNotifier` |
| Birden fazla ekran ve modül | Daha gelişmiş state management paketleri |
| Büyük ekip ve sürdürülebilir mimari | Katmanlı mimari + test edilebilir state yapısı |

Bu kitapta temel kavramların anlaşılması için Flutter SDK içinde gelen yapılara ağırlık verilmiştir. Daha ileri düzeyde Provider, Riverpod, Bloc veya benzeri yaklaşımlar ayrıca ele alınabilir.

::: {custom-style="Dikkat Kutusu"}
**Dikkat:** State management paketi seçmek, temel state mantığını öğrenmenin yerine geçmez. Önce state’in nerede yaşadığını ve kim tarafından değiştirildiğini anlamak gerekir.
:::

## Sık Yapılan Hatalar

| Hata | Açıklama | Çözüm |
|---|---|---|
| Her şeyi tek `StatefulWidget` içinde tutmak | Kod büyüdükçe okunabilirlik azalır | State modelini ayrı sınıfa taşı |
| Gereksiz global değişken kullanmak | Veri akışı kontrolsüz hâle gelir | State sahibini net belirle |
| `notifyListeners()` çağırmayı unutmak | Arayüz güncellenmez | Model değişiminden sonra bildirim yap |
| Controller veya notifier dispose etmemek | Kaynak yönetimi sorunu oluşturabilir | `dispose()` içinde temizle |
| Basit durum için aşırı karmaşık yapı kurmak | Öğrenme ve bakım zorlaşır | Soruna uygun en basit yaklaşımı seç |
| State ile UI kodunu tamamen karıştırmak | Test ve bakım zorlaşır | İş mantığını modele taşı |

## Laboratuvar Görevi

Bu laboratuvar çalışmasında öğrenciden “Ders Materyali Sepeti” adlı bir state management uygulaması geliştirmesi beklenmektedir.

### İstenenler

1. Uygulama başlığı “Ders Materyali Sepeti” olmalıdır.
2. En az dört materyalden oluşan bir ürün listesi hazırlanmalıdır.
3. Her materyal için ad ve fiyat bilgisi tutulmalıdır.
4. Sepet verisi `ChangeNotifier` tabanlı bir modelde yönetilmelidir.
5. Kullanıcı ürünü sepete ekleyebilmelidir.
6. Kullanıcı ürünü sepetten çıkarabilmelidir.
7. Sepetteki toplam ürün sayısı gösterilmelidir.
8. Toplam tutar hesaplanmalıdır.
9. Ürün kartı ayrı bir widget olarak tasarlanmalıdır.
10. Model `dispose()` içinde temizlenmelidir.

### Beklenen Kazanımlar

Bu laboratuvar sonunda öğrenci:

- State modelini widget sınıfından ayırabilir.
- `ChangeNotifier` ile veri değişimini bildirebilir.
- `ListenableBuilder` ile arayüzü modele bağlayabilir.
- Sepet benzeri paylaşılan state senaryosunu uygulayabilir.
- Veriyi alt widget’lara parametre olarak aktarabilir.

## Değerlendirme Rubriği

| Ölçüt | Puan | Açıklama |
|---|---:|---|
| State modelinin doğruluğu | 25 | `ChangeNotifier` tabanlı model doğru oluşturulmuştur |
| Sepet işlemleri | 20 | Ekleme, çıkarma ve toplam tutar hesaplama çalışmaktadır |
| Arayüz güncelleme | 15 | `notifyListeners()` ve builder yapısı doğru kullanılmıştır |
| Widget kompozisyonu | 15 | Ürün kartı ve özet panel ayrı widget olarak tasarlanmıştır |
| Kaynak yönetimi | 10 | Model veya notifier `dispose()` içinde temizlenmiştir |
| Kod okunabilirliği | 10 | Sınıf ve değişken adları anlamlıdır |
| Kullanıcı deneyimi | 5 | Butonlar ve özet bilgiler anlaşılırdır |

## Bölüm Özeti

Bu bölümde Flutter’da state management temelleri incelendi. State kavramı, local state ve shared state ayrımı, `setState()` kullanım sınırları, state’i üst widget’a taşıma yaklaşımı, `ValueNotifier`, `ValueListenableBuilder`, `ChangeNotifier` ve `ListenableBuilder` örneklerle açıklandı.

Mini uygulamada ürün listesi ve sepet verisi `ChangeNotifier` tabanlı bir modelle yönetildi. Bu yapı, state yönetiminin yalnızca ekrandaki değeri değiştirmek değil; veri, iş mantığı ve arayüz güncelleme ilişkisini düzenlemek olduğunu göstermektedir.

Bölümün ana fikri şudur: State management, uygulamada değişen verinin nerede yaşayacağını, nasıl değişeceğini ve hangi widget’ları etkileyeceğini bilinçli olarak tasarlama sürecidir.

## Bölüm Sonu Kontrol Listesi

- [ ] State kavramını açıklayabiliyorum.
- [ ] Local state ve shared state farkını biliyorum.
- [ ] `setState()` kullanım sınırlarını yorumlayabiliyorum.
- [ ] State’i üst widget’a taşıyabiliyorum.
- [ ] `ValueNotifier` kullanabiliyorum.
- [ ] `ValueListenableBuilder` ile arayüz güncelleyebiliyorum.
- [ ] `ChangeNotifier` ile model oluşturabiliyorum.
- [ ] `notifyListeners()` çağrısının amacını açıklayabiliyorum.
