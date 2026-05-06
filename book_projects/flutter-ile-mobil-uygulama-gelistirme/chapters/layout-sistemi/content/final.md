---
chapter_id: layout-sistemi
chapter_no: 7
title: "Layout Sistemi"
artifact_type: chapter
artifact_version: project-based
language: tr
---

# Bölüm 4 — Flutter Layout Sistemi

## Bölümün Amacı

Bu bölümde Flutter arayüzlerinin ekranda nasıl yerleştirildiği ele alınmaktadır. Önceki bölümde widget mantığı, `StatelessWidget`, `StatefulWidget`, `build()` metodu ve `setState()` kavramları incelenmişti. Bu bölümde ise bu widget’ların ekranda nasıl hizalandığı, nasıl boyutlandırıldığı ve farklı ekran genişliklerine nasıl uyum sağlayabileceği açıklanacaktır.

Flutter’da layout sistemi, yalnızca görsel bir düzenleme meselesi değildir. Doğru layout tasarımı; okunabilirlik, erişilebilirlik, performans, responsive davranış ve bakım kolaylığı açısından kritik öneme sahiptir.

Bu bölüm sonunda öğrenci:

- Flutter layout sisteminin temel çalışma mantığını açıklayabilir.
- `Row` ve `Column` ile yatay/dikey yerleşim kurabilir.
- `mainAxisAlignment` ve `crossAxisAlignment` özelliklerini kullanabilir.
- `Container`, `Padding`, `SizedBox` ve `Center` gibi temel layout widget’larını ayırt edebilir.
- `Expanded` ve `Flexible` ile esnek alan yönetimi yapabilir.
- `Wrap` ile taşma problemlerine daha güvenli çözümler üretebilir.
- Basit responsive layout kararlarını `LayoutBuilder` ile uygulayabilir.
- Küçük bir profil/özet kartı arayüzünü layout ilkelerine uygun biçimde geliştirebilir.

## Layout Sistemi Neden Önemlidir?

Mobil uygulamalarda ekran alanı sınırlıdır. Aynı uygulama farklı telefonlarda, tabletlerde ve masaüstü boyutlarında farklı genişliklerde çalışabilir. Bu nedenle arayüz elemanlarının yalnızca ekrana konulması yeterli değildir; aynı zamanda okunabilir, düzenli ve uyumlu biçimde yerleştirilmesi gerekir.

Flutter’da layout sistemi şu sorulara cevap verir:

- Bir widget ekranda nerede duracak?
- Ne kadar genişlik ve yükseklik kullanacak?
- Yanındaki veya altındaki widget’larla ilişkisi nasıl olacak?
- Ekran daraldığında veya genişlediğinde nasıl davranacak?
- İçerik taşarsa ne olacak?

Bu sorulara verilen cevaplar, uygulamanın kullanıcı deneyimini doğrudan etkiler.

::: {custom-style="Dikkat Kutusu"}
**Dikkat:** Flutter’da layout problemlerinin önemli bir kısmı, widget ağacındaki parent-child ilişkisini ve kısıt mantığını yeterince anlamamaktan kaynaklanır.
:::

## Flutter’da Kısıt Mantığı

Flutter layout sisteminin temelinde **constraints go down, sizes go up, parent sets position** yaklaşımı bulunur. Bu ifade şu şekilde açıklanabilir:

1. Üst widget, alt widget’a hangi genişlik ve yükseklik aralığında yerleşebileceğini bildirir.
2. Alt widget, bu sınırlar içinde kendi boyutunu belirler.
3. Üst widget, alt widget’ın ekrandaki konumunu belirler.

Bu yaklaşım, Flutter layout sistemini anlamak için temel ilkedir. Örneğin bir `Center` widget’ı, child widget’ını ortalamaya çalışır. Ancak child widget’ın ne kadar yer kaplayacağı, kendisine gelen kısıtlara göre belirlenir.

```yaml
CODE_META:
  id: b04_kod01_center_text
  chapter: 4
  language: dart
  framework: flutter
  runnable: true
  file: lib/main.dart
  purpose: Center ve Text ile basit layout mantığını gösterme
```

```dart
import 'package:flutter/material.dart';

void main() {
  runApp(const LayoutGirisUygulamasi());
}

class LayoutGirisUygulamasi extends StatelessWidget {
  const LayoutGirisUygulamasi({super.key});

  @override
  Widget build(BuildContext context) {
    return const MaterialApp(
      home: LayoutGirisSayfasi(),
    );
  }
}

class LayoutGirisSayfasi extends StatelessWidget {
  const LayoutGirisSayfasi({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Layout Mantığı'),
      ),
      body: const Center(
        child: Text(
          'Bu metin Center widget ile ortalanmıştır.',
          textAlign: TextAlign.center,
        ),
      ),
    );
  }
}
```

Bu örnekte `Scaffold` sayfa iskeletini kurar. `Center`, kendisine verilen `Text` widget’ını içerik alanının ortasına yerleştirir.

## `Column` ile Dikey Yerleşim

`Column`, child widget’ları dikey yönde alt alta yerleştirir. Mobil uygulamalarda en sık kullanılan layout widget’larından biridir.

```yaml
CODE_META:
  id: b04_kod02_column_temel
  chapter: 4
  language: dart
  framework: flutter
  runnable: true
  file: lib/main.dart
  purpose: Column ile dikey yerleşim oluşturma
```

```dart
import 'package:flutter/material.dart';

void main() {
  runApp(const ColumnOrnegiUygulamasi());
}

class ColumnOrnegiUygulamasi extends StatelessWidget {
  const ColumnOrnegiUygulamasi({super.key});

  @override
  Widget build(BuildContext context) {
    return const MaterialApp(
      home: ColumnOrnegiSayfasi(),
    );
  }
}

class ColumnOrnegiSayfasi extends StatelessWidget {
  const ColumnOrnegiSayfasi({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Column Örneği'),
      ),
      body: const Center(
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Icon(Icons.phone_android, size: 48),
            SizedBox(height: 12),
            Text(
              'Flutter Layout',
              style: TextStyle(
                fontSize: 24,
                fontWeight: FontWeight.bold,
              ),
            ),
            SizedBox(height: 8),
            Text('Column ile dikey yerleşim'),
          ],
        ),
      ),
    );
  }
}
```

Bu örnekte `Column` içindeki widget’lar yukarıdan aşağıya sıralanır. `SizedBox` widget’ları ise elemanlar arasında boşluk oluşturmak için kullanılır.

`mainAxisSize: MainAxisSize.min` kullanımı, `Column` widget’ının dikey eksende yalnızca ihtiyacı kadar yer kaplamasını sağlar. Bu ifade kaldırılırsa `Column`, bulunduğu alanın yüksekliğini daha geniş kullanabilir.

## `Row` ile Yatay Yerleşim

`Row`, child widget’ları yatay yönde yan yana yerleştirir. Buton grupları, küçük bilgi satırları ve ikon-metin birliktelikleri için sık kullanılır.

```yaml
CODE_META:
  id: b04_kod03_row_temel
  chapter: 4
  language: dart
  framework: flutter
  runnable: true
  file: lib/main.dart
  purpose: Row ile yatay yerleşim oluşturma
```

```dart
import 'package:flutter/material.dart';

void main() {
  runApp(const RowOrnegiUygulamasi());
}

class RowOrnegiUygulamasi extends StatelessWidget {
  const RowOrnegiUygulamasi({super.key});

  @override
  Widget build(BuildContext context) {
    return const MaterialApp(
      home: RowOrnegiSayfasi(),
    );
  }
}

class RowOrnegiSayfasi extends StatelessWidget {
  const RowOrnegiSayfasi({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Row Örneği'),
      ),
      body: Center(
        child: Row(
          mainAxisSize: MainAxisSize.min,
          children: const [
            Icon(Icons.check_circle, color: Colors.green),
            SizedBox(width: 8),
            Text('Görev tamamlandı'),
          ],
        ),
      ),
    );
  }
}
```

Bu örnekte ikon ve metin yan yana gösterilmiştir. `SizedBox(width: 8)` yatay boşluk üretir.

::: {custom-style="Ipucu Kutusu"}
**İpucu:** `Column` dikey eksende, `Row` yatay eksende çalışır. Bu iki widget Flutter layout sisteminin en temel düzenleme araçlarıdır.
:::

## Ana Eksen ve Çapraz Eksen

`Row` ve `Column` kullanırken iki temel eksen vardır:

- **Ana eksen:** Widget’ın yerleşim yönüdür.
- **Çapraz eksen:** Ana eksene dik olan yöndür.

`Column` için ana eksen dikey, çapraz eksen yataydır. `Row` için ana eksen yatay, çapraz eksen dikeydir.

Bu ayrım özellikle şu özellikleri kullanırken önemlidir:

- `mainAxisAlignment`
- `crossAxisAlignment`

Aşağıdaki örnek, butonların dikey eksende nasıl dağıtılabileceğini gösterir.

```yaml
CODE_META:
  id: b04_kod04_alignment_column
  chapter: 4
  language: dart
  framework: flutter
  runnable: true
  file: lib/main.dart
  purpose: mainAxisAlignment ve crossAxisAlignment kullanımını gösterme
```

```dart
import 'package:flutter/material.dart';

void main() {
  runApp(const HizalamaUygulamasi());
}

class HizalamaUygulamasi extends StatelessWidget {
  const HizalamaUygulamasi({super.key});

  @override
  Widget build(BuildContext context) {
    return const MaterialApp(
      home: HizalamaSayfasi(),
    );
  }
}

class HizalamaSayfasi extends StatelessWidget {
  const HizalamaSayfasi({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Hizalama'),
      ),
      body: const Column(
        mainAxisAlignment: MainAxisAlignment.center,
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          Padding(
            padding: EdgeInsets.all(8),
            child: ElevatedButton(
              onPressed: null,
              child: Text('Birinci Buton'),
            ),
          ),
          Padding(
            padding: EdgeInsets.all(8),
            child: ElevatedButton(
              onPressed: null,
              child: Text('İkinci Buton'),
            ),
          ),
        ],
      ),
    );
  }
}
```

Bu örnekte `mainAxisAlignment: MainAxisAlignment.center`, elemanların dikey eksende ortalanmasını sağlar. `crossAxisAlignment: CrossAxisAlignment.stretch` ise child widget’ların yatay eksende genişlemesine izin verir.

## `Container`

`Container`, Flutter’da en çok kullanılan yardımcı layout widget’larından biridir. Kenar boşluğu, iç boşluk, arka plan rengi, genişlik, yükseklik ve dekorasyon gibi işlemler için kullanılabilir.

Ancak `Container` gereksiz yere her yerde kullanılmamalıdır. Sadece ihtiyaç olduğunda tercih edilmelidir.

```yaml
CODE_META:
  id: b04_kod05_container_card
  chapter: 4
  language: dart
  framework: flutter
  runnable: true
  file: lib/main.dart
  purpose: Container ile boyut, renk ve iç boşluk yönetimi
```

```dart
import 'package:flutter/material.dart';

void main() {
  runApp(const ContainerOrnegiUygulamasi());
}

class ContainerOrnegiUygulamasi extends StatelessWidget {
  const ContainerOrnegiUygulamasi({super.key});

  @override
  Widget build(BuildContext context) {
    return const MaterialApp(
      home: ContainerOrnegiSayfasi(),
    );
  }
}

class ContainerOrnegiSayfasi extends StatelessWidget {
  const ContainerOrnegiSayfasi({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Container Örneği'),
      ),
      body: Center(
        child: Container(
          width: 280,
          padding: const EdgeInsets.all(20),
          decoration: BoxDecoration(
            color: Colors.indigo.shade50,
            borderRadius: BorderRadius.circular(16),
            border: Border.all(color: Colors.indigo),
          ),
          child: const Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              Icon(Icons.dashboard, size: 48),
              SizedBox(height: 12),
              Text(
                'Layout Kartı',
                style: TextStyle(
                  fontSize: 22,
                  fontWeight: FontWeight.bold,
                ),
              ),
              SizedBox(height: 8),
              Text(
                'Container, padding ve decoration ile görsel yapı kurar.',
                textAlign: TextAlign.center,
              ),
            ],
          ),
        ),
      ),
    );
  }
}
```

Bu örnekte `Container`, kart benzeri bir yapı oluşturmak için kullanılmıştır. `padding`, içerik ile kenarlar arasında boşluk bırakır. `decoration`, arka plan ve kenarlık gibi görsel özellikleri tanımlar.

## `Padding` ve `SizedBox`

`Padding`, bir widget’ın çevresinde iç boşluk oluşturmak için kullanılır. `SizedBox` ise sabit boşluk veya sabit boyut oluşturmak için tercih edilir.

Aşağıdaki iki kullanım farklı amaçlara hizmet eder:

```dart
const Padding(
  padding: EdgeInsets.all(16),
  child: Text('İç boşluklu metin'),
);
```

```dart
const SizedBox(height: 16);
```

İlk örnekte metnin çevresine boşluk eklenir. İkinci örnekte ise iki widget arasında dikey boşluk oluşturulur.

::: {custom-style="Dikkat Kutusu"}
**Dikkat:** Boşluk vermek için gereksiz `Container` kullanmak yerine çoğu durumda `SizedBox` veya `Padding` daha açık ve okunabilir bir tercihtir.
:::

## `Expanded` ve `Flexible`

`Row` ve `Column` içinde yer paylaşımı yapmak için `Expanded` ve `Flexible` kullanılır.

`Expanded`, child widget’ın kullanılabilir alanı doldurmasını sağlar. `Flexible` ise child widget’a esnek davranma imkânı verir ancak onu mutlaka tüm alanı kaplamaya zorlamaz.

```yaml
CODE_META:
  id: b04_kod06_expanded_flexible
  chapter: 4
  language: dart
  framework: flutter
  runnable: true
  file: lib/main.dart
  purpose: Expanded ve Flexible ile esnek alan yönetimi
```

```dart
import 'package:flutter/material.dart';

void main() {
  runApp(const EsnekLayoutUygulamasi());
}

class EsnekLayoutUygulamasi extends StatelessWidget {
  const EsnekLayoutUygulamasi({super.key});

  @override
  Widget build(BuildContext context) {
    return const MaterialApp(
      home: EsnekLayoutSayfasi(),
    );
  }
}

class EsnekLayoutSayfasi extends StatelessWidget {
  const EsnekLayoutSayfasi({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Expanded ve Flexible'),
      ),
      body: Column(
        children: [
          Expanded(
            flex: 2,
            child: Container(
              alignment: Alignment.center,
              color: Colors.blue.shade100,
              child: const Text('Alan 1 - flex: 2'),
            ),
          ),
          Expanded(
            flex: 1,
            child: Container(
              alignment: Alignment.center,
              color: Colors.orange.shade100,
              child: const Text('Alan 2 - flex: 1'),
            ),
          ),
        ],
      ),
    );
  }
}
```

Bu örnekte ekran dikey olarak iki alana ayrılmıştır. Birinci alan `flex: 2`, ikinci alan `flex: 1` değerine sahiptir. Bu nedenle birinci alan ikinci alana göre daha fazla yer kaplar.

## Taşma Problemleri ve `Wrap`

Flutter’da `Row` içine çok fazla widget yerleştirildiğinde yatay taşma hatası oluşabilir. Bu durumda ekranda sarı-siyah uyarı çizgileri görülebilir. Böyle durumlarda `Wrap`, uygun bir çözüm olabilir.

`Wrap`, child widget’ları mevcut satıra sığmadığında yeni satıra geçirir.

```yaml
CODE_META:
  id: b04_kod07_wrap_chip
  chapter: 4
  language: dart
  framework: flutter
  runnable: true
  file: lib/main.dart
  purpose: Wrap ile taşma sorunlarını azaltma
```

```dart
import 'package:flutter/material.dart';

void main() {
  runApp(const WrapOrnegiUygulamasi());
}

class WrapOrnegiUygulamasi extends StatelessWidget {
  const WrapOrnegiUygulamasi({super.key});

  @override
  Widget build(BuildContext context) {
    return const MaterialApp(
      home: WrapOrnegiSayfasi(),
    );
  }
}

class WrapOrnegiSayfasi extends StatelessWidget {
  const WrapOrnegiSayfasi({super.key});

  @override
  Widget build(BuildContext context) {
    final konular = [
      'Widget',
      'Layout',
      'State',
      'Navigation',
      'Form',
      'API',
      'Test',
      'Yayınlama',
    ];

    return Scaffold(
      appBar: AppBar(
        title: const Text('Wrap Örneği'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Wrap(
          spacing: 8,
          runSpacing: 8,
          children: [
            for (final konu in konular)
              Chip(
                label: Text(konu),
              ),
          ],
        ),
      ),
    );
  }
}
```

Bu örnekte konu etiketleri ekrana sığmadığında alt satıra geçebilir. Bu yapı, özellikle filtre etiketleri, kategori listeleri ve beceri kartları için kullanışlıdır.

## `LayoutBuilder` ile Responsive Karar Verme

`LayoutBuilder`, parent widget’tan gelen kısıtları okuyarak ekran genişliğine göre farklı layout kararları vermeye imkân tanır.

Aşağıdaki örnekte ekran genişliğine göre kartlar tek sütun veya iki sütun olarak gösterilmektedir.

```yaml
CODE_META:
  id: b04_kod08_layoutbuilder_responsive
  chapter: 4
  language: dart
  framework: flutter
  runnable: true
  file: lib/main.dart
  purpose: LayoutBuilder ile basit responsive layout oluşturma
```

```dart
import 'package:flutter/material.dart';

void main() {
  runApp(const ResponsiveLayoutUygulamasi());
}

class ResponsiveLayoutUygulamasi extends StatelessWidget {
  const ResponsiveLayoutUygulamasi({super.key});

  @override
  Widget build(BuildContext context) {
    return const MaterialApp(
      home: ResponsiveLayoutSayfasi(),
    );
  }
}

class ResponsiveLayoutSayfasi extends StatelessWidget {
  const ResponsiveLayoutSayfasi({super.key});

  @override
  Widget build(BuildContext context) {
    final kartlar = [
      const BilgiKarti(baslik: 'Ders', deger: 'Mobil Programlama'),
      const BilgiKarti(baslik: 'Hafta', deger: '4'),
      const BilgiKarti(baslik: 'Konu', deger: 'Layout Sistemi'),
      const BilgiKarti(baslik: 'Durum', deger: 'Uygulama'),
    ];

    return Scaffold(
      appBar: AppBar(
        title: const Text('Responsive Layout'),
      ),
      body: LayoutBuilder(
        builder: (context, constraints) {
          final genisEkran = constraints.maxWidth >= 600;

          return Padding(
            padding: const EdgeInsets.all(16),
            child: GridView.count(
              crossAxisCount: genisEkran ? 2 : 1,
              crossAxisSpacing: 12,
              mainAxisSpacing: 12,
              childAspectRatio: genisEkran ? 3 : 4,
              children: kartlar,
            ),
          );
        },
      ),
    );
  }
}

class BilgiKarti extends StatelessWidget {
  final String baslik;
  final String deger;

  const BilgiKarti({
    super.key,
    required this.baslik,
    required this.deger,
  });

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

Bu örnekte `constraints.maxWidth` değeri okunur. Genişlik 600 piksel veya üzerindeyse iki sütunlu yapı, daha dar ekranlarda tek sütunlu yapı kullanılır.

## Mini Uygulama: Responsive Profil Kartı

Bu mini uygulamada layout sisteminin temel parçaları bir araya getirilerek responsive davranış gösteren bir profil kartı geliştirilecektir.

[SCREENSHOT:b04_01_responsive_profil_karti]

<!-- SCREENSHOT_META
id: b04_01_responsive_profil_karti
chapter_id: chapter_07
title: "Responsive Profil Karti"
kind: browser_page
url: "http://127.0.0.1:5173/__book__/layout-sistemi/b04_01_responsive_profil_karti"
viewport: 1440x900
wait_for: "networkidle"
output_file: assets/auto/screenshots/b04_01_responsive_profil_karti.png
caption: "Responsive Profil Karti ekran görüntüsü."
validation_mode: capture
-->

```yaml
CODE_META:
  id: b04_kod09_responsive_profil_karti
  chapter: 4
  language: dart
  framework: flutter
  runnable: true
  file: lib/main.dart
  purpose: Row, Column, Container, Padding, Expanded, Wrap ve LayoutBuilder kullanımı
  screenshot: b04_01_responsive_profil_karti
```

```dart
import 'package:flutter/material.dart';

void main() {
  runApp(const ProfilKartiUygulamasi());
}

class ProfilKartiUygulamasi extends StatelessWidget {
  const ProfilKartiUygulamasi({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Responsive Profil Kartı',
      theme: ThemeData(
        colorSchemeSeed: Colors.teal,
        useMaterial3: true,
      ),
      home: const ProfilKartiSayfasi(),
    );
  }
}

class ProfilKartiSayfasi extends StatelessWidget {
  const ProfilKartiSayfasi({super.key});

  @override
  Widget build(BuildContext context) {
    final yetenekler = [
      'Flutter',
      'Dart',
      'UI',
      'Layout',
      'Mobil',
      'Test',
    ];

    return Scaffold(
      appBar: AppBar(
        title: const Text('Responsive Profil Kartı'),
      ),
      body: LayoutBuilder(
        builder: (context, constraints) {
          final genisEkran = constraints.maxWidth >= 650;

          return Center(
            child: ConstrainedBox(
              constraints: const BoxConstraints(maxWidth: 760),
              child: Card(
                margin: const EdgeInsets.all(16),
                child: Padding(
                  padding: const EdgeInsets.all(24),
                  child: genisEkran
                      ? Row(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            const ProfilAvatar(),
                            const SizedBox(width: 24),
                            Expanded(
                              child: ProfilBilgileri(yetenekler: yetenekler),
                            ),
                          ],
                        )
                      : Column(
                          mainAxisSize: MainAxisSize.min,
                          children: [
                            const ProfilAvatar(),
                            const SizedBox(height: 20),
                            ProfilBilgileri(yetenekler: yetenekler),
                          ],
                        ),
                ),
              ),
            ),
          );
        },
      ),
    );
  }
}

class ProfilAvatar extends StatelessWidget {
  const ProfilAvatar({super.key});

  @override
  Widget build(BuildContext context) {
    return CircleAvatar(
      radius: 48,
      child: Text(
        'BK',
        style: Theme.of(context).textTheme.headlineMedium,
      ),
    );
  }
}

class ProfilBilgileri extends StatelessWidget {
  final List<String> yetenekler;

  const ProfilBilgileri({
    super.key,
    required this.yetenekler,
  });

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          'Bahar Kaya',
          style: Theme.of(context).textTheme.headlineSmall,
        ),
        const SizedBox(height: 4),
        Text(
          'Mobil uygulama geliştirme öğrencisi',
          style: Theme.of(context).textTheme.bodyLarge,
        ),
        const SizedBox(height: 16),
        const Text(
          'İlgi alanları',
          style: TextStyle(fontWeight: FontWeight.bold),
        ),
        const SizedBox(height: 8),
        Wrap(
          spacing: 8,
          runSpacing: 8,
          children: [
            for (final yetenek in yetenekler)
              Chip(
                label: Text(yetenek),
              ),
          ],
        ),
        const SizedBox(height: 20),
        Row(
          children: [
            Expanded(
              child: ElevatedButton.icon(
                onPressed: () {},
                icon: const Icon(Icons.mail_outline),
                label: const Text('İletişim'),
              ),
            ),
            const SizedBox(width: 12),
            Expanded(
              child: OutlinedButton.icon(
                onPressed: () {},
                icon: const Icon(Icons.bookmark_border),
                label: const Text('Kaydet'),
              ),
            ),
          ],
        ),
      ],
    );
  }
}
```

Bu uygulamada dar ekranlarda profil görseli ve bilgiler dikey olarak sıralanır. Geniş ekranlarda ise avatar solda, bilgiler sağda olacak şekilde yatay layout kullanılır. Böylece aynı arayüz farklı ekran boyutlarına daha uyumlu hâle gelir.

## Sık Yapılan Hatalar

| Hata | Açıklama | Çözüm |
|---|---|---|
| Her boşluk için `Container` kullanmak | Kod gereksiz karmaşıklaşır | `SizedBox` veya `Padding` kullan |
| `Row` içinde taşmayı göz ardı etmek | Ekranda overflow hatası oluşur | `Expanded`, `Flexible` veya `Wrap` kullan |
| `Column` içinde uzun içeriği doğrudan vermek | Küçük ekranlarda taşma olabilir | `SingleChildScrollView` veya liste yapısı kullan |
| `Expanded` widget’ını yanlış parent içinde kullanmak | Runtime layout hatası oluşabilir | `Expanded` yalnızca `Row`, `Column`, `Flex` içinde kullanılmalı |
| Tüm arayüzü tek widget içine yığmak | Bakım zorlaşır | Anlamlı alt widget’lara böl |
| Responsive davranışı hiç düşünmemek | Tablet/geniş ekran deneyimi zayıflar | `LayoutBuilder` veya uygun grid yapıları kullan |

## Laboratuvar Görevi

Bu laboratuvar çalışmasında öğrenciden “Ders Bilgi Paneli” adlı responsive bir arayüz geliştirmesi beklenmektedir.

### İstenenler

1. Uygulama başlığı “Ders Bilgi Paneli” olmalıdır.
2. Sayfada bir ders adı, hafta bilgisi ve kısa açıklama yer almalıdır.
3. En az üç bilgi kartı oluşturulmalıdır.
4. Kartlar dar ekranda tek sütun, geniş ekranda iki sütun olarak gösterilmelidir.
5. `LayoutBuilder` kullanılmalıdır.
6. Kartların içinde `Row` ve `Column` birlikte kullanılmalıdır.
7. Arayüzde `Padding`, `SizedBox`, `Expanded` ve `Wrap` örnekleri bulunmalıdır.
8. Kod en az üç anlamlı widget sınıfına bölünmelidir.

### Beklenen Kazanımlar

Bu laboratuvar sonunda öğrenci:

- Responsive layout kararını ekran genişliğine göre verebilir.
- `Row` ve `Column` widget’larını birlikte kullanabilir.
- `Expanded` ile alan paylaşımı yapabilir.
- `Wrap` ile taşma riskini azaltabilir.
- Büyük arayüzleri küçük widget bileşenlerine ayırabilir.

## Değerlendirme Rubriği

| Ölçüt | Puan | Açıklama |
|---|---:|---|
| Layout widget’larının doğru kullanımı | 25 | `Row`, `Column`, `Padding`, `SizedBox`, `Expanded` doğru kullanılmıştır |
| Responsive yapı | 20 | `LayoutBuilder` ile ekran genişliğine göre karar verilmiştir |
| Arayüz okunabilirliği | 15 | Kartlar, metinler ve boşluklar düzenlidir |
| Widget kompozisyonu | 15 | Kod anlamlı alt widget’lara bölünmüştür |
| Taşma riskinin azaltılması | 10 | `Wrap`, `Expanded` veya uygun sınırlamalar kullanılmıştır |
| Kod okunabilirliği | 10 | Sınıf ve değişken adları anlamlıdır |
| `const` kullanımı | 5 | Sabit widget’larda `const` tercih edilmiştir |

## Bölüm Özeti

Bu bölümde Flutter layout sisteminin temel mantığı incelendi. `Row` ve `Column` ile yatay ve dikey yerleşim kurma, `mainAxisAlignment` ve `crossAxisAlignment` ile hizalama yapma, `Container`, `Padding` ve `SizedBox` ile boşluk ve görsel yapı oluşturma konuları ele alındı.

Ayrıca `Expanded` ve `Flexible` ile esnek alan paylaşımı, `Wrap` ile taşma problemlerine çözüm üretme ve `LayoutBuilder` ile responsive layout kararları verme örneklerle gösterildi. Bölümün mini uygulamasında bu kavramlar responsive bir profil kartı üzerinde birleştirildi.

Bu bölümden çıkarılması gereken ana fikir şudur: Flutter’da başarılı bir arayüz, yalnızca doğru widget’ları seçmekle değil; bu widget’ları doğru boyut, hizalama, boşluk ve ekran uyumu ilkeleriyle yerleştirmekle oluşturulur.

## Bölüm Sonu Kontrol Listesi

- [ ] `Row` ve `Column` arasındaki farkı açıklayabiliyorum.
- [ ] Ana eksen ve çapraz eksen kavramlarını yorumlayabiliyorum.
- [ ] `mainAxisAlignment` ve `crossAxisAlignment` kullanabiliyorum.
- [ ] `Container`, `Padding` ve `SizedBox` rollerini ayırt edebiliyorum.
- [ ] `Expanded` ve `Flexible` ile alan yönetimi yapabiliyorum.
- [ ] `Wrap` ile taşma riskini azaltabiliyorum.
- [ ] `LayoutBuilder` ile basit responsive kararlar verebiliyorum.
- [ ] Büyük arayüzleri küçük ve anlamlı widget’lara bölebiliyorum.
