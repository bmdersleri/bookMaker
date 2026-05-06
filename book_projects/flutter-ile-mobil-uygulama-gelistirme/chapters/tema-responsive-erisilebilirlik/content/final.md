# Bölüm 11 — Tema, Responsive Tasarım ve Erişilebilirlik

## Bölümün Amacı

Bu bölümde Flutter uygulamalarında tema yönetimi, responsive tasarım ve erişilebilirlik konuları ele alınmaktadır. Kullanıcı arayüzü yalnızca çalışır durumda olmakla yetinmemeli; farklı ekran boyutlarında düzenli görünmeli, görsel bütünlük taşımalı ve mümkün olduğunca geniş kullanıcı grupları tarafından erişilebilir olmalıdır.

## 11.1. Tema Nedir?

Tema, uygulamanın renk, tipografi, buton görünümü, kart yapısı ve genel görsel dilini belirleyen kurallar bütünüdür. Flutter’da tema çoğunlukla `ThemeData` ile tanımlanır.

```yaml
CODE_META:
  id: b11_kod01_themadata
  chapter: 11
  language: dart
  framework: flutter
  runnable: true
  file: lib/main.dart
  purpose: ThemeData ve ColorScheme ile uygulama teması oluşturma
```

```dart
import 'package:flutter/material.dart';

void main() {
  runApp(const TemaUygulamasi());
}

class TemaUygulamasi extends StatelessWidget {
  const TemaUygulamasi({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Tema Kullanımı',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.indigo),
        useMaterial3: true,
      ),
      home: const TemaSayfasi(),
    );
  }
}

class TemaSayfasi extends StatelessWidget {
  const TemaSayfasi({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Tema Kullanımı')),
      body: Center(
        child: Card(
          child: Padding(
            padding: const EdgeInsets.all(20),
            child: Text(
              'Bu kart uygulama temasından etkilenir.',
              style: Theme.of(context).textTheme.titleMedium,
            ),
          ),
        ),
      ),
    );
  }
}
```

::: {custom-style="Ipucu Kutusu"}
**İpucu:** Renkleri her widget içinde elle vermek yerine tema üzerinden yönetmek, büyük projelerde bakım kolaylığı sağlar.
:::

## 11.2. Açık ve Koyu Tema

```yaml
CODE_META:
  id: b11_kod02_light_dark_theme
  chapter: 11
  language: dart
  framework: flutter
  runnable: true
  file: lib/main.dart
  purpose: Açık ve koyu tema tanımlama
```

```dart
import 'package:flutter/material.dart';

void main() {
  runApp(const CiftTemaUygulamasi());
}

class CiftTemaUygulamasi extends StatelessWidget {
  const CiftTemaUygulamasi({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Açık ve Koyu Tema',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.teal),
        useMaterial3: true,
      ),
      darkTheme: ThemeData(
        colorScheme: ColorScheme.fromSeed(
          seedColor: Colors.teal,
          brightness: Brightness.dark,
        ),
        useMaterial3: true,
      ),
      themeMode: ThemeMode.system,
      home: const CiftTemaSayfasi(),
    );
  }
}

class CiftTemaSayfasi extends StatelessWidget {
  const CiftTemaSayfasi({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Tema Modu')),
      body: const Center(
        child: Text('Tema cihaz ayarına göre değişebilir.'),
      ),
    );
  }
}
```

## 11.3. Responsive Tasarım, MediaQuery ve LayoutBuilder

Responsive tasarım, arayüzün farklı ekran boyutlarına uyum sağlamasıdır. Flutter’da responsive kararlar için `MediaQuery`, `LayoutBuilder`, `Flexible`, `Expanded`, `Wrap` ve `GridView` kullanılabilir.

```yaml
CODE_META:
  id: b11_kod03_mediaquery_layoutbuilder
  chapter: 11
  language: dart
  framework: flutter
  runnable: true
  file: lib/main.dart
  purpose: MediaQuery ve LayoutBuilder ile responsive düzen oluşturma
```

```dart
import 'package:flutter/material.dart';

void main() {
  runApp(const ResponsivePanelUygulamasi());
}

class ResponsivePanelUygulamasi extends StatelessWidget {
  const ResponsivePanelUygulamasi({super.key});

  @override
  Widget build(BuildContext context) {
    return const MaterialApp(home: ResponsivePanelSayfasi());
  }
}

class ResponsivePanelSayfasi extends StatelessWidget {
  const ResponsivePanelSayfasi({super.key});

  @override
  Widget build(BuildContext context) {
    final ekranGenisligi = MediaQuery.sizeOf(context).width;
    final kartlar = const [
      BilgiKarti(baslik: 'Ders', deger: 'Flutter'),
      BilgiKarti(baslik: 'Hafta', deger: '11'),
      BilgiKarti(baslik: 'Konu', deger: 'Responsive'),
      BilgiKarti(baslik: 'Genişlik', deger: 'Dinamik'),
    ];

    return Scaffold(
      appBar: AppBar(title: const Text('Responsive Panel')),
      body: LayoutBuilder(
        builder: (context, constraints) {
          final sutunSayisi = constraints.maxWidth >= 700 ? 2 : 1;

          return Column(
            children: [
              Padding(
                padding: const EdgeInsets.all(12),
                child: Text('Ekran genişliği: ${ekranGenisligi.toStringAsFixed(0)}'),
              ),
              Expanded(
                child: GridView.count(
                  padding: const EdgeInsets.all(16),
                  crossAxisCount: sutunSayisi,
                  crossAxisSpacing: 12,
                  mainAxisSpacing: 12,
                  children: kartlar,
                ),
              ),
            ],
          );
        },
      ),
    );
  }
}

class BilgiKarti extends StatelessWidget {
  final String baslik;
  final String deger;

  const BilgiKarti({super.key, required this.baslik, required this.deger});

  @override
  Widget build(BuildContext context) {
    return Card(
      child: Center(
        child: ListTile(
          leading: const Icon(Icons.info_outline),
          title: Text(baslik),
          subtitle: Text(deger),
        ),
      ),
    );
  }
}
```

## 11.4. Accessibility ve Semantics

Erişilebilirlik; uygulamanın farklı kullanıcı ihtiyaçlarına uygun biçimde kullanılabilmesini ifade eder. Kontrast, okunabilir metin, yeterli dokunma alanı ve ekran okuyucu dostu açıklamalar önemlidir.

```yaml
CODE_META:
  id: b11_kod04_semantics
  chapter: 11
  language: dart
  framework: flutter
  runnable: true
  file: lib/main.dart
  purpose: Semantics ile erişilebilir açıklama ekleme
```

```dart
import 'package:flutter/material.dart';

void main() {
  runApp(const SemanticsUygulamasi());
}

class SemanticsUygulamasi extends StatelessWidget {
  const SemanticsUygulamasi({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: Scaffold(
        appBar: AppBar(title: const Text('Semantics')),
        body: Center(
          child: Semantics(
            label: 'Ders ilerleme durumu yüzde yetmiş',
            child: const CircularProgressIndicator(value: 0.7),
          ),
        ),
      ),
    );
  }
}
```

## 11.5. Mini Uygulama: Erişilebilir Responsive Ders Paneli

[SCREENSHOT:b11_01_responsive_erisilebilir_ders_paneli]

```yaml
CODE_META:
  id: b11_kod05_responsive_erisilebilir_panel
  chapter: 11
  language: dart
  framework: flutter
  runnable: true
  file: lib/main.dart
  purpose: ThemeData, LayoutBuilder, responsive düzen ve Semantics kullanımı
  screenshot: b11_01_responsive_erisilebilir_ders_paneli
```

```dart
import 'package:flutter/material.dart';

void main() {
  runApp(const DersPaneliUygulamasi());
}

class DersPaneliUygulamasi extends StatelessWidget {
  const DersPaneliUygulamasi({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Ders Paneli',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepPurple),
        useMaterial3: true,
      ),
      home: const DersPaneliSayfasi(),
    );
  }
}

class DersPaneliSayfasi extends StatelessWidget {
  const DersPaneliSayfasi({super.key});

  @override
  Widget build(BuildContext context) {
    final kartlar = const [
      PanelKarti(ikon: Icons.menu_book, baslik: 'Ders', deger: 'Mobil Programlama'),
      PanelKarti(ikon: Icons.schedule, baslik: 'Hafta', deger: '11'),
      PanelKarti(ikon: Icons.check_circle, baslik: 'İlerleme', deger: '%70'),
      PanelKarti(ikon: Icons.accessibility_new, baslik: 'Erişim', deger: 'Uygun'),
    ];

    return Scaffold(
      appBar: AppBar(title: const Text('Erişilebilir Ders Paneli')),
      body: LayoutBuilder(
        builder: (context, constraints) {
          final sutun = constraints.maxWidth >= 700 ? 2 : 1;

          return GridView.count(
            padding: const EdgeInsets.all(16),
            crossAxisCount: sutun,
            crossAxisSpacing: 12,
            mainAxisSpacing: 12,
            children: kartlar,
          );
        },
      ),
    );
  }
}

class PanelKarti extends StatelessWidget {
  final IconData ikon;
  final String baslik;
  final String deger;

  const PanelKarti({
    super.key,
    required this.ikon,
    required this.baslik,
    required this.deger,
  });

  @override
  Widget build(BuildContext context) {
    return Semantics(
      label: '$baslik bilgisi: $deger',
      child: Card(
        child: Center(
          child: ListTile(
            leading: Icon(ikon, size: 36),
            title: Text(baslik),
            subtitle: Text(deger, style: Theme.of(context).textTheme.titleLarge),
          ),
        ),
      ),
    );
  }
}
```

## 11.6. Kontrast ve Okunabilirlik

Kontrast, metnin arka plan üzerinde ne kadar rahat okunabildiğiyle ilgilidir. Sadece renk değişimiyle anlam vermek erişilebilir değildir. İkon, metin ve açıklama birlikte kullanılmalıdır.

## 11.7. Laboratuvar Görevi

“Responsive ve Erişilebilir Ders Paneli” uygulaması geliştiriniz. Uygulamada tema, kart tabanlı responsive yapı, `LayoutBuilder`, `MediaQuery`, `Semantics`, okunabilir metin stilleri, accessibility ve yeterli contrast kullanılmalıdır.

## 11.8. Değerlendirme Rubriği

| Ölçüt | Puan | Açıklama |
|---|---:|---|
| Tema kullanımı | 20 | `ThemeData` ve `ColorScheme` doğru kullanılmıştır |
| Responsive yapı | 20 | `LayoutBuilder` veya `MediaQuery` ile karar verilmiştir |
| Erişilebilirlik | 20 | Semantik etiket ve okunabilirlik düşünülmüştür |
| Arayüz düzeni | 15 | Kartlar ve boşluklar düzenlidir |
| Kod okunabilirliği | 15 | Widget’lar anlamlı ayrılmıştır |
| Kullanıcı deneyimi | 10 | Farklı ekranlarda anlaşılır yapı sunulmuştur |

## 11.9. Bölüm Özeti

Bu bölümde tema yönetimi, açık/koyu tema, responsive tasarım, `MediaQuery`, `LayoutBuilder`, accessibility, contrast ve `Semantics` kullanımı ele alındı.

## Bölüm Sonu Kontrol Listesi

- [ ] `ThemeData` kullanabiliyorum.
- [ ] `ColorScheme` mantığını açıklayabiliyorum.
- [ ] `MediaQuery` ile ekran ölçüsü okuyabiliyorum.
- [ ] `LayoutBuilder` ile responsive karar verebiliyorum.
- [ ] Erişilebilirlik için temel tasarım ilkelerini uygulayabiliyorum.
- [ ] `Semantics` widget’ını temel düzeyde kullanabiliyorum.
