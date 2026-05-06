---
chapter_id: performans-yayinlama
chapter_no: 11
title: "Performans ve Yayınlama"
artifact_type: chapter
artifact_version: project-based
language: tr
---

# Bölüm 15 — Performans ve Yayınlama

## Bölümün Amacı

Bu bölümde Flutter uygulamalarında temel performans ilkeleri ve yayınlama süreci ele alınmaktadır. Uygulamanın doğru çalışması kadar akıcı, hızlı ve güvenilir olması da önemlidir. Ayrıca geliştirilen uygulamanın kullanıcıya ulaştırılabilmesi için sürümleme, release build ve mağaza hazırlıkları bilinmelidir.

Bu bölüm sonunda öğrenci:

- Performans sorunlarını temel düzeyde yorumlayabilir.
- `const` kullanımının önemini açıklayabilir.
- Uzun listelerde builder yaklaşımını kullanabilir.
- Gereksiz rebuild risklerini fark edebilir.
- Release build mantığını açıklayabilir.
- Sürüm numarası ve yayınlama hazırlıklarını yorumlayabilir.

## Performans Neden Önemlidir?

Mobil uygulamalarda yavaş açılış, takılan animasyonlar, geciken listeleme ve aşırı bellek kullanımı kullanıcı deneyimini olumsuz etkiler. Performans yalnızca teknik değil, doğrudan kullanıcı memnuniyetini etkileyen bir kalite ölçütüdür.

::: {custom-style="Dikkat Kutusu"}
**Dikkat:** Performans optimizasyonu, ölçmeden tahmin yürütmek değildir. Önce problem gözlenmeli, sonra uygun araçlarla analiz edilmelidir.
:::

## `const` Kullanımı

```yaml
CODE_META:
  id: b15_kod01_const_kullanimi
  chapter: 15
  language: dart
  framework: flutter
  runnable: true
  file: lib/main.dart
  purpose: const kullanımının okunabilirlik ve performans açısından önemini gösterme
```

```dart
import 'package:flutter/material.dart';

void main() {
  runApp(const ConstUygulamasi());
}

class ConstUygulamasi extends StatelessWidget {
  const ConstUygulamasi({super.key});

  @override
  Widget build(BuildContext context) {
    return const MaterialApp(
      home: ConstSayfasi(),
    );
  }
}

class ConstSayfasi extends StatelessWidget {
  const ConstSayfasi({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('const Kullanımı')),
      body: const Center(
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Icon(Icons.speed, size: 48),
            SizedBox(height: 12),
            Text('Sabit widgetlarda const kullanın.'),
          ],
        ),
      ),
    );
  }
}
```

## Uzun Listelerde Builder Kullanımı

```yaml
CODE_META:
  id: b15_kod02_builder_performans
  chapter: 15
  language: dart
  framework: flutter
  runnable: true
  file: lib/main.dart
  purpose: Uzun listelerde ListView.builder kullanımını gösterme
```

```dart
import 'package:flutter/material.dart';

void main() {
  runApp(const BuilderPerformansUygulamasi());
}

class BuilderPerformansUygulamasi extends StatelessWidget {
  const BuilderPerformansUygulamasi({super.key});

  @override
  Widget build(BuildContext context) {
    return const MaterialApp(home: BuilderPerformansSayfasi());
  }
}

class BuilderPerformansSayfasi extends StatelessWidget {
  const BuilderPerformansSayfasi({super.key});

  @override
  Widget build(BuildContext context) {
    final veriler = List.generate(1000, (index) => 'Kayıt ${index + 1}');

    return Scaffold(
      appBar: AppBar(title: const Text('Builder Performansı')),
      body: ListView.builder(
        itemCount: veriler.length,
        itemBuilder: (context, index) {
          return ListTile(
            leading: CircleAvatar(child: Text('${index + 1}')),
            title: Text(veriler[index]),
          );
        },
      ),
    );
  }
}
```

## Rebuild Mantığını Anlamak

Gereksiz rebuild, uygulama performansını olumsuz etkileyebilir. Widget ağacını küçük parçalara bölmek, sabit widget’larda `const` kullanmak ve state kapsamını dar tutmak önemlidir.

```yaml
CODE_META:
  id: b15_kod03_rebuild_izleme
  chapter: 15
  language: dart
  framework: flutter
  runnable: true
  file: lib/main.dart
  purpose: Rebuild davranışını debugPrint ile gözlemleme
```

```dart
import 'package:flutter/material.dart';

void main() {
  runApp(const RebuildUygulamasi());
}

class RebuildUygulamasi extends StatefulWidget {
  const RebuildUygulamasi({super.key});

  @override
  State<RebuildUygulamasi> createState() => _RebuildUygulamasiState();
}

class _RebuildUygulamasiState extends State<RebuildUygulamasi> {
  int sayac = 0;

  void artir() {
    setState(() {
      sayac++;
    });
  }

  @override
  Widget build(BuildContext context) {
    debugPrint('Ana build çalıştı.');

    return MaterialApp(
      home: Scaffold(
        appBar: AppBar(title: const Text('Rebuild İzleme')),
        body: Center(
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              const SabitBaslik(),
              Text('Sayaç: $sayac'),
              ElevatedButton(
                onPressed: artir,
                child: const Text('Artır'),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

class SabitBaslik extends StatelessWidget {
  const SabitBaslik({super.key});

  @override
  Widget build(BuildContext context) {
    debugPrint('Sabit başlık build çalıştı.');
    return const Text('Performans İzleme');
  }
}
```

## Profiling ve DevTools

Flutter DevTools, performans analizi için frame rendering, CPU, memory ve widget rebuild gibi alanlarda yardımcı olur. Performans sorunu yaşandığında önce debug tahmini değil, ölçüm yapılmalıdır.

## Release Build Mantığı

Geliştirme sırasında kullanılan debug build, performans ve hata ayıklama bilgileri açısından yayın sürümünden farklıdır. Yayınlama öncesi release build hazırlanır.

Örnek komutlar:

```bash
flutter build apk --release
flutter build appbundle --release
```

Platforma göre iOS ve Android gereksinimleri farklıdır. İmzalama, sürüm numarası ve mağaza yönergeleri ayrıca dikkate alınmalıdır.

## Version ve Yayınlama Hazırlıkları

`pubspec.yaml` içinde version bilgisi uygulamanın sürümünü belirtir.

```yaml
version: 1.0.0+1
```

Burada `1.0.0` kullanıcıya görünen sürüm, `+1` ise build numarasıdır.

## Mini Uygulama: Performans Kontrol Paneli

[SCREENSHOT:b15_01_performans_kontrol_paneli]

<!-- SCREENSHOT_META
id: b15_01_performans_kontrol_paneli
chapter_id: chapter_11
title: "Performans Kontrol Paneli"
kind: browser_page
url: "http://127.0.0.1:5173/__book__/performans-yayinlama/b15_01_performans_kontrol_paneli"
viewport: 1440x900
wait_for: "networkidle"
output_file: assets/auto/screenshots/b15_01_performans_kontrol_paneli.png
caption: "Performans Kontrol Paneli ekran görüntüsü."
validation_mode: capture
-->

```yaml
CODE_META:
  id: b15_kod04_performans_kontrol_paneli
  chapter: 15
  language: dart
  framework: flutter
  runnable: true
  file: lib/main.dart
  purpose: Performans ilkelerini kartlarla gösteren kontrol paneli
  screenshot: b15_01_performans_kontrol_paneli
```

```dart
import 'package:flutter/material.dart';

void main() {
  runApp(const PerformansPaneliUygulamasi());
}

class PerformansKriteri {
  final String baslik;
  final String aciklama;
  final IconData ikon;

  const PerformansKriteri({
    required this.baslik,
    required this.aciklama,
    required this.ikon,
  });
}

class PerformansPaneliUygulamasi extends StatelessWidget {
  const PerformansPaneliUygulamasi({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Performans Paneli',
      theme: ThemeData(colorSchemeSeed: Colors.red, useMaterial3: true),
      home: const PerformansPaneli(),
    );
  }
}

class PerformansPaneli extends StatelessWidget {
  const PerformansPaneli({super.key});

  @override
  Widget build(BuildContext context) {
    final kriterler = const [
      PerformansKriteri(
        baslik: 'const',
        aciklama: 'Sabit widgetlarda const kullan',
        ikon: Icons.check_circle,
      ),
      PerformansKriteri(
        baslik: 'Builder',
        aciklama: 'Uzun listelerde builder kullan',
        ikon: Icons.list,
      ),
      PerformansKriteri(
        baslik: 'Profiling',
        aciklama: 'DevTools ile ölçüm yap',
        ikon: Icons.analytics,
      ),
      PerformansKriteri(
        baslik: 'Release',
        aciklama: 'Yayın öncesi release build al',
        ikon: Icons.rocket_launch,
      ),
    ];

    return Scaffold(
      appBar: AppBar(title: const Text('Performans Kontrol Paneli')),
      body: ListView.builder(
        padding: const EdgeInsets.all(12),
        itemCount: kriterler.length,
        itemBuilder: (context, index) {
          final kriter = kriterler[index];

          return Card(
            child: ListTile(
              leading: Icon(kriter.ikon),
              title: Text(kriter.baslik),
              subtitle: Text(kriter.aciklama),
            ),
          );
        },
      ),
    );
  }
}
```

## Laboratuvar Görevi

“Yayın Öncesi Kontrol Paneli” uygulaması geliştiriniz. Performans, version, release build, store hazırlığı, profiling ve test maddelerini kartlar hâlinde gösteriniz.

## Değerlendirme Rubriği

| Ölçüt | Puan | Açıklama |
|---|---:|---|
| Performans ilkeleri | 20 | `const`, builder ve rebuild mantığı açıklanmıştır |
| Profiling farkındalığı | 15 | DevTools kullanım amacı belirtilmiştir |
| Yayınlama bilgisi | 20 | Release build ve mağaza hazırlıkları açıklanmıştır |
| Version yönetimi | 15 | Sürüm ve build numarası yorumlanmıştır |
| Mini uygulama | 15 | Kontrol paneli düzgün tasarlanmıştır |
| Kod okunabilirliği | 15 | Model ve listeleme yapısı düzenlidir |

## Bölüm Özeti

Bu bölümde performans ilkeleri, `const`, builder kullanımı, rebuild mantığı, profiling, release build, version ve yayınlama hazırlıkları ele alındı.

## Bölüm Sonu Kontrol Listesi

- [ ] Performans sorunlarını temel düzeyde yorumlayabiliyorum.
- [ ] `const` kullanımının amacını açıklayabiliyorum.
- [ ] Uzun listelerde builder kullanabiliyorum.
- [ ] Release build kavramını biliyorum.
- [ ] Version ve build numarası farkını açıklayabiliyorum.
