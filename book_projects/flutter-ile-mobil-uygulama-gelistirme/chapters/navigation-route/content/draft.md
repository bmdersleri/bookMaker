---
chapter_id: navigation-route
chapter_no: 9
title: "Navigation ve Route Yönetimi"
artifact_type: chapter
artifact_version: project-based
language: tr
---

# Bölüm 7 — Navigation ve Route Yönetimi

## Bölümün Amacı

Bu bölümde Flutter uygulamalarında ekranlar arasında geçiş yapma, route kavramı ve temel navigation yönetimi ele alınmaktadır. Önceki bölümlerde widget mantığı, layout sistemi, formlar ve dinamik listeleme konuları incelenmişti. Gerçek bir mobil uygulama çoğu zaman tek ekrandan oluşmaz. Kullanıcı; ana sayfa, liste ekranı, detay ekranı, form ekranı, ayarlar ekranı ve profil ekranı gibi farklı sayfalar arasında geçiş yapar.

Flutter’da bu geçişler temel olarak `Navigator`, `Route`, `MaterialPageRoute`, adlandırılmış rotalar ve veri aktarımı yaklaşımlarıyla yönetilir. Bu bölümde önce klasik `Navigator.push` ve `Navigator.pop` yapısı ele alınacak, ardından named routes ve detay sayfasına veri gönderme örnekleri gösterilecektir.

Bu bölüm sonunda öğrenci:

- Navigation ve route kavramlarını açıklayabilir.
- `Navigator.push` ile yeni sayfaya geçebilir.
- `Navigator.pop` ile önceki sayfaya dönebilir.
- `MaterialPageRoute` kullanımını anlayabilir.
- Sayfalar arasında veri aktarabilir.
- Named routes mantığını temel düzeyde kurabilir.
- Liste ekranından detay ekranına geçiş yapabilir.
- Navigation akışını küçük bir örnek uygulamada kullanabilir.

## Navigation Nedir?

Navigation, kullanıcının uygulama içinde bir ekrandan başka bir ekrana geçmesini sağlayan yapıdır. Mobil uygulamalarda navigation akışı kullanıcı deneyimini doğrudan etkiler. Kullanıcı bir ders listesine bakabilir, listeden bir ders seçebilir, ders detayına gidebilir ve ardından geri dönebilir.

Flutter’da her ekran genellikle ayrı bir widget sınıfı olarak tasarlanır. Örneğin:

- `AnaSayfa`
- `DersListesiSayfasi`
- `DersDetaySayfasi`
- `AyarlarSayfasi`
- `ProfilSayfasi`

Bu sayfalar arasında geçiş yapmak için `Navigator` kullanılır.

::: {custom-style="Dikkat Kutusu"}
**Dikkat:** Flutter’da navigation yalnızca ekran değiştirmek değildir. Geri dönüş davranışı, veri aktarımı, kullanıcı akışı ve uygulama mimarisiyle doğrudan ilişkilidir.
:::

## Route Kavramı

Flutter’da bir ekran genellikle bir route olarak düşünülebilir. Route, kullanıcının görebileceği bir sayfayı temsil eder. Yeni bir sayfaya geçildiğinde route yığınına yeni bir route eklenir. Geri dönüldüğünde ise bu route yığından çıkarılır.

Bu mantık basitçe şu şekilde düşünülebilir:

```text
Başlangıç:
[AnaSayfa]

Detay sayfasına gidildiğinde:
[AnaSayfa, DetaySayfasi]

Geri dönüldüğünde:
[AnaSayfa]
```

Flutter bu yığın mantığını `Navigator` ile yönetir.

## İlk Sayfa Geçişi: `Navigator.push`

Yeni bir sayfaya geçmek için `Navigator.push` kullanılır. Aşağıdaki örnekte ana sayfadan bilgi sayfasına geçiş yapılmaktadır.

```yaml
CODE_META:
  id: b07_kod01_navigator_push
  chapter: 7
  language: dart
  framework: flutter
  runnable: true
  file: lib/main.dart
  purpose: Navigator.push ve MaterialPageRoute ile yeni sayfaya geçiş
```

```dart
import 'package:flutter/material.dart';

void main() {
  runApp(const NavigationGirisUygulamasi());
}

class NavigationGirisUygulamasi extends StatelessWidget {
  const NavigationGirisUygulamasi({super.key});

  @override
  Widget build(BuildContext context) {
    return const MaterialApp(
      home: AnaSayfa(),
    );
  }
}

class AnaSayfa extends StatelessWidget {
  const AnaSayfa({super.key});

  void bilgiSayfasinaGit(BuildContext context) {
    Navigator.push(
      context,
      MaterialPageRoute(
        builder: (context) => const BilgiSayfasi(),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Ana Sayfa'),
      ),
      body: Center(
        child: ElevatedButton(
          onPressed: () => bilgiSayfasinaGit(context),
          child: const Text('Bilgi Sayfasına Git'),
        ),
      ),
    );
  }
}

class BilgiSayfasi extends StatelessWidget {
  const BilgiSayfasi({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Bilgi Sayfası'),
      ),
      body: const Center(
        child: Text('Bu ekran Navigator.push ile açıldı.'),
      ),
    );
  }
}
```

Bu örnekte `MaterialPageRoute`, yeni açılacak sayfayı üretir. `builder` fonksiyonu, geçilecek sayfanın widget’ını döndürür.

## Önceki Sayfaya Dönmek: `Navigator.pop`

Bir sayfadan önceki sayfaya dönmek için `Navigator.pop(context)` kullanılır. AppBar içinde varsayılan geri butonu çoğu durumda otomatik olarak görünür. Ancak özel bir butonla da geri dönüş yapılabilir.

```yaml
CODE_META:
  id: b07_kod02_navigator_pop
  chapter: 7
  language: dart
  framework: flutter
  runnable: true
  file: lib/main.dart
  purpose: Navigator.pop ile önceki sayfaya dönme
```

```dart
import 'package:flutter/material.dart';

void main() {
  runApp(const GeriDonusUygulamasi());
}

class GeriDonusUygulamasi extends StatelessWidget {
  const GeriDonusUygulamasi({super.key});

  @override
  Widget build(BuildContext context) {
    return const MaterialApp(
      home: IlkSayfa(),
    );
  }
}

class IlkSayfa extends StatelessWidget {
  const IlkSayfa({super.key});

  void ikinciSayfayaGit(BuildContext context) {
    Navigator.push(
      context,
      MaterialPageRoute(
        builder: (context) => const IkinciSayfa(),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('İlk Sayfa'),
      ),
      body: Center(
        child: ElevatedButton(
          onPressed: () => ikinciSayfayaGit(context),
          child: const Text('İkinci Sayfaya Git'),
        ),
      ),
    );
  }
}

class IkinciSayfa extends StatelessWidget {
  const IkinciSayfa({super.key});

  void geriDon(BuildContext context) {
    Navigator.pop(context);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('İkinci Sayfa'),
      ),
      body: Center(
        child: ElevatedButton(
          onPressed: () => geriDon(context),
          child: const Text('Geri Dön'),
        ),
      ),
    );
  }
}
```

`Navigator.pop` mevcut route’u yığından çıkarır. Böylece kullanıcı bir önceki ekrana döner.

::: {custom-style="Ipucu Kutusu"}
**İpucu:** `push` yeni sayfa ekler, `pop` mevcut sayfayı kapatır. Bu iki kavram navigation sisteminin temelidir.
:::

## Sayfaya Veri Göndermek

Gerçek uygulamalarda yalnızca sayfaya geçmek yeterli değildir. Çoğu zaman seçilen öğeye ait bilgiler detay sayfasına gönderilmelidir. Örneğin ders listesinden bir ders seçildiğinde, ders başlığı ve açıklaması detay sayfasında gösterilebilir.

```yaml
CODE_META:
  id: b07_kod03_sayfaya_veri_gonderme
  chapter: 7
  language: dart
  framework: flutter
  runnable: true
  file: lib/main.dart
  purpose: Navigator.push ile detay sayfasına veri gönderme
```

```dart
import 'package:flutter/material.dart';

void main() {
  runApp(const VeriGondermeUygulamasi());
}

class VeriGondermeUygulamasi extends StatelessWidget {
  const VeriGondermeUygulamasi({super.key});

  @override
  Widget build(BuildContext context) {
    return const MaterialApp(
      home: DersListesiSayfasi(),
    );
  }
}

class Ders {
  final String baslik;
  final String aciklama;

  const Ders({
    required this.baslik,
    required this.aciklama,
  });
}

class DersListesiSayfasi extends StatelessWidget {
  const DersListesiSayfasi({super.key});

  @override
  Widget build(BuildContext context) {
    final dersler = [
      const Ders(
        baslik: 'Flutter’a Giriş',
        aciklama: 'Flutter SDK, proje yapısı ve ilk uygulama.',
      ),
      const Ders(
        baslik: 'Widget Mantığı',
        aciklama: 'StatelessWidget, StatefulWidget ve setState.',
      ),
      const Ders(
        baslik: 'Navigation',
        aciklama: 'Sayfalar arası geçiş ve veri aktarımı.',
      ),
    ];

    return Scaffold(
      appBar: AppBar(
        title: const Text('Ders Listesi'),
      ),
      body: ListView.builder(
        itemCount: dersler.length,
        itemBuilder: (context, index) {
          final ders = dersler[index];

          return ListTile(
            leading: const Icon(Icons.menu_book_outlined),
            title: Text(ders.baslik),
            subtitle: Text(ders.aciklama),
            trailing: const Icon(Icons.chevron_right),
            onTap: () {
              Navigator.push(
                context,
                MaterialPageRoute(
                  builder: (context) => DersDetaySayfasi(ders: ders),
                ),
              );
            },
          );
        },
      ),
    );
  }
}

class DersDetaySayfasi extends StatelessWidget {
  final Ders ders;

  const DersDetaySayfasi({
    super.key,
    required this.ders,
  });

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(ders.baslik),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Text(
          ders.aciklama,
          style: Theme.of(context).textTheme.titleMedium,
        ),
      ),
    );
  }
}
```

Bu örnekte `DersDetaySayfasi`, constructor üzerinden `Ders` nesnesi almaktadır. Liste öğesine dokunulduğunda ilgili ders detay sayfasına gönderilir.

## Sayfadan Geriye Veri Döndürmek

Bazen açılan sayfa kapandığında önceki sayfaya bir değer döndürmek gerekir. Örneğin seçim ekranında kullanıcı bir seçenek seçer ve önceki sayfa bu seçimi kullanır.

```yaml
CODE_META:
  id: b07_kod04_geriye_veri_dondurme
  chapter: 7
  language: dart
  framework: flutter
  runnable: true
  file: lib/main.dart
  purpose: Navigator.pop ile önceki sayfaya veri döndürme
```

```dart
import 'package:flutter/material.dart';

void main() {
  runApp(const GeriyeVeriUygulamasi());
}

class GeriyeVeriUygulamasi extends StatelessWidget {
  const GeriyeVeriUygulamasi({super.key});

  @override
  Widget build(BuildContext context) {
    return const MaterialApp(
      home: SecimAnaSayfasi(),
    );
  }
}

class SecimAnaSayfasi extends StatefulWidget {
  const SecimAnaSayfasi({super.key});

  @override
  State<SecimAnaSayfasi> createState() => _SecimAnaSayfasiState();
}

class _SecimAnaSayfasiState extends State<SecimAnaSayfasi> {
  String secilenKonu = 'Henüz seçim yapılmadı.';

  Future<void> konuSec(BuildContext context) async {
    final sonuc = await Navigator.push<String>(
      context,
      MaterialPageRoute(
        builder: (context) => const KonuSecimSayfasi(),
      ),
    );

    if (sonuc == null) {
      return;
    }

    setState(() {
      secilenKonu = sonuc;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Seçim Ana Sayfası'),
      ),
      body: Center(
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Text(secilenKonu),
            const SizedBox(height: 16),
            ElevatedButton(
              onPressed: () => konuSec(context),
              child: const Text('Konu Seç'),
            ),
          ],
        ),
      ),
    );
  }
}

class KonuSecimSayfasi extends StatelessWidget {
  const KonuSecimSayfasi({super.key});

  @override
  Widget build(BuildContext context) {
    final konular = [
      'Widget Mantığı',
      'Layout Sistemi',
      'Formlar',
      'Navigation',
    ];

    return Scaffold(
      appBar: AppBar(
        title: const Text('Konu Seç'),
      ),
      body: ListView(
        children: [
          for (final konu in konular)
            ListTile(
              title: Text(konu),
              onTap: () {
                Navigator.pop(context, konu);
              },
            ),
        ],
      ),
    );
  }
}
```

Bu örnekte `Navigator.push<String>` çağrısı sonucunda bir `String` değer beklenmektedir. Seçim sayfasında `Navigator.pop(context, konu)` ile seçilen konu önceki sayfaya döndürülür.

## Named Routes

Küçük uygulamalarda `MaterialPageRoute` doğrudan kullanılabilir. Ancak ekran sayısı arttıkça route adlarıyla çalışmak daha düzenli bir yapı sağlayabilir. Buna named routes denir.

```yaml
CODE_META:
  id: b07_kod05_named_routes
  chapter: 7
  language: dart
  framework: flutter
  runnable: true
  file: lib/main.dart
  purpose: MaterialApp routes ve Navigator.pushNamed kullanımı
```

```dart
import 'package:flutter/material.dart';

void main() {
  runApp(const NamedRouteUygulamasi());
}

class NamedRouteUygulamasi extends StatelessWidget {
  const NamedRouteUygulamasi({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      initialRoute: '/',
      routes: {
        '/': (context) => const AnaSayfa(),
        '/dersler': (context) => const DerslerSayfasi(),
        '/ayarlar': (context) => const AyarlarSayfasi(),
      },
    );
  }
}

class AnaSayfa extends StatelessWidget {
  const AnaSayfa({super.key});

  void rotayaGit(BuildContext context, String routeName) {
    Navigator.pushNamed(context, routeName);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Ana Sayfa'),
      ),
      body: Center(
        child: Wrap(
          spacing: 12,
          children: [
            ElevatedButton(
              onPressed: () => rotayaGit(context, '/dersler'),
              child: const Text('Dersler'),
            ),
            OutlinedButton(
              onPressed: () => rotayaGit(context, '/ayarlar'),
              child: const Text('Ayarlar'),
            ),
          ],
        ),
      ),
    );
  }
}

class DerslerSayfasi extends StatelessWidget {
  const DerslerSayfasi({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Dersler'),
      ),
      body: const Center(
        child: Text('Dersler sayfası'),
      ),
    );
  }
}

class AyarlarSayfasi extends StatelessWidget {
  const AyarlarSayfasi({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Ayarlar'),
      ),
      body: const Center(
        child: Text('Ayarlar sayfası'),
      ),
    );
  }
}
```

Bu örnekte route adları `MaterialApp` içindeki `routes` haritasında tanımlanmıştır. Sayfa geçişleri ise `Navigator.pushNamed` ile yapılmaktadır.

::: {custom-style="Dikkat Kutusu"}
**Dikkat:** Named routes düzen sağlar; ancak karmaşık parametre aktarımı gereken senaryolarda constructor tabanlı navigation veya daha gelişmiş route yönetimi tercih edilebilir.
:::

## `pushReplacement` ve Akış Yönetimi

Bazı durumlarda yeni sayfaya geçerken önceki sayfanın geri dönülebilir olmasını istemeyiz. Örneğin giriş başarılı olduktan sonra kullanıcı login ekranına geri dönmemelidir. Bu durumda `Navigator.pushReplacement` kullanılabilir.

```yaml
CODE_META:
  id: b07_kod06_push_replacement
  chapter: 7
  language: dart
  framework: flutter
  runnable: true
  file: lib/main.dart
  purpose: Navigator.pushReplacement ile ekran değiştirme
```

```dart
import 'package:flutter/material.dart';

void main() {
  runApp(const ReplacementUygulamasi());
}

class ReplacementUygulamasi extends StatelessWidget {
  const ReplacementUygulamasi({super.key});

  @override
  Widget build(BuildContext context) {
    return const MaterialApp(
      home: GirisSayfasi(),
    );
  }
}

class GirisSayfasi extends StatelessWidget {
  const GirisSayfasi({super.key});

  void girisYap(BuildContext context) {
    Navigator.pushReplacement(
      context,
      MaterialPageRoute(
        builder: (context) => const PanelSayfasi(),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Giriş'),
      ),
      body: Center(
        child: ElevatedButton(
          onPressed: () => girisYap(context),
          child: const Text('Giriş Yap'),
        ),
      ),
    );
  }
}

class PanelSayfasi extends StatelessWidget {
  const PanelSayfasi({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Panel'),
      ),
      body: const Center(
        child: Text('Ana panele hoş geldiniz.'),
      ),
    );
  }
}
```

Bu örnekte giriş sayfası, panel sayfası ile değiştirilir. Kullanıcı geri butonuna bastığında giriş sayfasına dönmez.

## Mini Uygulama: Ders Listesi ve Detay Ekranı

Bu mini uygulamada ders konularını listeleyen ve seçilen konunun detayını ayrı sayfada gösteren bir navigation akışı geliştirilecektir.

[SCREENSHOT:b07_01_ders_listesi_detay_navigation]

<!-- SCREENSHOT_META
id: b07_01_ders_listesi_detay_navigation
chapter_id: chapter_09
title: "Ders Listesi Detay Navigation"
kind: browser_page
url: "http://127.0.0.1:5173/__book__/navigation-route/b07_01_ders_listesi_detay_navigation"
viewport: 1440x900
wait_for: "networkidle"
output_file: assets/auto/screenshots/b07_01_ders_listesi_detay_navigation.png
caption: "Ders Listesi Detay Navigation ekran görüntüsü."
validation_mode: capture
-->

```yaml
CODE_META:
  id: b07_kod07_ders_listesi_detay_navigation
  chapter: 7
  language: dart
  framework: flutter
  runnable: true
  file: lib/main.dart
  purpose: Liste ekranından detay ekranına veri aktarımı ve navigation akışı
  screenshot: b07_01_ders_listesi_detay_navigation
```

```dart
import 'package:flutter/material.dart';

void main() {
  runApp(const DersNavigationUygulamasi());
}

class DersKonusu {
  final String baslik;
  final String hafta;
  final String aciklama;
  final List<String> kazanımlar;

  const DersKonusu({
    required this.baslik,
    required this.hafta,
    required this.aciklama,
    required this.kazanımlar,
  });
}

class DersNavigationUygulamasi extends StatelessWidget {
  const DersNavigationUygulamasi({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Ders Navigation',
      theme: ThemeData(
        colorSchemeSeed: Colors.indigo,
        useMaterial3: true,
      ),
      home: const DersListesiSayfasi(),
    );
  }
}

class DersListesiSayfasi extends StatelessWidget {
  const DersListesiSayfasi({super.key});

  List<DersKonusu> get konular => const [
        DersKonusu(
          baslik: 'Flutter’a Giriş',
          hafta: 'Hafta 1',
          aciklama: 'Flutter ekosistemi ve proje yapısı',
          kazanımlar: [
            'Flutter SDK kavramını açıklar',
            'Proje yapısını tanır',
            'İlk uygulamayı çalıştırır',
          ],
        ),
        DersKonusu(
          baslik: 'Widget Mantığı',
          hafta: 'Hafta 3',
          aciklama: 'StatelessWidget, StatefulWidget ve setState',
          kazanımlar: [
            'Widget ağacını açıklar',
            'StatefulWidget kullanır',
            'setState ile arayüz günceller',
          ],
        ),
        DersKonusu(
          baslik: 'Navigation ve Route',
          hafta: 'Hafta 7',
          aciklama: 'Sayfalar arası geçiş ve veri aktarımı',
          kazanımlar: [
            'Navigator.push kullanır',
            'Navigator.pop ile geri döner',
            'Detay sayfasına veri gönderir',
          ],
        ),
      ];

  void detayaGit(BuildContext context, DersKonusu konu) {
    Navigator.push(
      context,
      MaterialPageRoute(
        builder: (context) => DersDetaySayfasi(konu: konu),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Ders Konuları'),
      ),
      body: ListView.builder(
        padding: const EdgeInsets.all(12),
        itemCount: konular.length,
        itemBuilder: (context, index) {
          final konu = konular[index];

          return Card(
            child: ListTile(
              leading: CircleAvatar(
                child: Text('${index + 1}'),
              ),
              title: Text(konu.baslik),
              subtitle: Text('${konu.hafta} • ${konu.aciklama}'),
              trailing: const Icon(Icons.chevron_right),
              onTap: () => detayaGit(context, konu),
            ),
          );
        },
      ),
    );
  }
}

class DersDetaySayfasi extends StatelessWidget {
  final DersKonusu konu;

  const DersDetaySayfasi({
    super.key,
    required this.konu,
  });

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(konu.hafta),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Card(
          child: Padding(
            padding: const EdgeInsets.all(20),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  konu.baslik,
                  style: Theme.of(context).textTheme.headlineSmall,
                ),
                const SizedBox(height: 8),
                Text(konu.aciklama),
                const SizedBox(height: 20),
                const Text(
                  'Kazanımlar',
                  style: TextStyle(fontWeight: FontWeight.bold),
                ),
                const SizedBox(height: 8),
                for (final kazanim in konu.kazanımlar)
                  Padding(
                    padding: const EdgeInsets.only(bottom: 8),
                    child: Row(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        const Icon(Icons.check, size: 18),
                        const SizedBox(width: 8),
                        Expanded(child: Text(kazanim)),
                      ],
                    ),
                  ),
                const SizedBox(height: 20),
                SizedBox(
                  width: double.infinity,
                  child: OutlinedButton.icon(
                    onPressed: () => Navigator.pop(context),
                    icon: const Icon(Icons.arrow_back),
                    label: const Text('Listeye Dön'),
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
```

Bu mini uygulamada liste ekranı ve detay ekranı birlikte çalışır. Kullanıcı ders konusuna dokunduğunda ilgili model nesnesi detay sayfasına gönderilir. Detay sayfası bu nesneyi constructor üzerinden alır ve ekranda gösterir.

## Navigation Tasarımında Dikkat Edilecek Noktalar

Navigation akışı tasarlanırken şu sorular sorulmalıdır:

- Kullanıcı bu ekrandan nereye geçebilir?
- Kullanıcı geri döndüğünde hangi ekrana ulaşmalıdır?
- Detay sayfası hangi veriye ihtiyaç duyar?
- Geriye veri döndürmek gerekir mi?
- Login, onboarding veya tamamlanan işlem gibi ekranlarda geri dönüş engellenmeli mi?
- Route adları veya constructor tabanlı geçişlerden hangisi daha okunabilir olur?

Bu sorular navigation yapısının yalnızca teknik değil, kullanıcı deneyimi açısından da düşünülmesi gerektiğini gösterir.

## Sık Yapılan Hatalar

| Hata | Açıklama | Çözüm |
|---|---|---|
| `context` yanlış yerde kullanmak | Navigation beklenmeyen hata verebilir | Geçerli widget context’iyle çağrı yap |
| Her geçişi karmaşık hâle getirmek | Kod okunabilirliği azalır | Basit uygulamalarda `MaterialPageRoute` yeterlidir |
| Detay sayfasına eksik veri göndermek | Sayfa anlamlı içerik gösteremez | Constructor parametrelerini net tanımla |
| Geri dönüş davranışını düşünmemek | Kullanıcı akışı bozulabilir | `push`, `pop`, `pushReplacement` farkını bil |
| Route adlarını dağınık yazmak | Büyük projede bakım zorlaşır | Route adlarını sabitlerde veya merkezi yapıda tut |
| Gereksiz named route kullanmak | Küçük projede fazladan karmaşıklık oluşur | Basit örneklerde doğrudan route kullan |

## Laboratuvar Görevi

Bu laboratuvar çalışmasında öğrenciden “Ders Kataloğu ve Detay Ekranı” adlı iki ekranlı bir Flutter uygulaması geliştirmesi beklenmektedir.

### İstenenler

1. Uygulamada bir ders kataloğu ekranı olmalıdır.
2. En az beş ders veya konu listelenmelidir.
3. Her ders için başlık, hafta ve kısa açıklama bilgisi tutulmalıdır.
4. Dersler `ListView.builder` ile gösterilmelidir.
5. Her ders `Card` ve `ListTile` ile temsil edilmelidir.
6. Liste öğesine dokunulduğunda detay sayfasına geçilmelidir.
7. Detay sayfasına seçilen ders nesnesi gönderilmelidir.
8. Detay sayfasında ders başlığı, açıklama ve en az üç kazanım gösterilmelidir.
9. Detay sayfasında özel bir “Listeye Dön” butonu bulunmalıdır.
10. Navigation için `Navigator.push` ve `Navigator.pop` kullanılmalıdır.

### Beklenen Kazanımlar

Bu laboratuvar sonunda öğrenci:

- Liste ekranından detay ekranına geçiş yapabilir.
- Model nesnesini sayfalar arasında taşıyabilir.
- `MaterialPageRoute` yapısını kullanabilir.
- Geri dönüş davranışını yönetebilir.
- Navigation akışını kullanıcı deneyimiyle birlikte düşünebilir.

## Değerlendirme Rubriği

| Ölçüt | Puan | Açıklama |
|---|---:|---|
| Navigation yapısı | 20 | `Navigator.push` ve `Navigator.pop` doğru kullanılmıştır |
| Veri aktarımı | 20 | Seçilen ders bilgisi detay sayfasına aktarılmıştır |
| Liste ekranı | 15 | Dersler `ListView.builder`, `Card` ve `ListTile` ile gösterilmiştir |
| Detay ekranı | 15 | Başlık, açıklama ve kazanımlar anlaşılır biçimde sunulmuştur |
| Model kullanımı | 10 | Ders verisi anlamlı bir model sınıfıyla temsil edilmiştir |
| Kullanıcı deneyimi | 10 | Geri dönüş ve ekran akışı anlaşılırdır |
| Kod okunabilirliği | 10 | Sayfalar ve widget’lar düzenli ayrılmıştır |

## Bölüm Özeti

Bu bölümde Flutter’da navigation ve route yönetimi ele alındı. `Navigator.push`, `Navigator.pop`, `MaterialPageRoute`, sayfaya veri gönderme, sayfadan geriye veri döndürme, named routes ve `pushReplacement` konuları örneklerle açıklandı.

Mini uygulamada ders listesinden detay sayfasına geçiş yapan bir yapı geliştirildi. Bu yapı, gerçek uygulamalardaki liste-detay akışlarının temelini oluşturur. Navigation bilgisi, ilerleyen bölümlerde state management, API verileri ve çok ekranlı proje geliştirme süreçlerinde daha da önemli hâle gelecektir.

Bölümün ana fikri şudur: Navigation yalnızca sayfa değiştirmek değildir; kullanıcının uygulama içinde anlamlı ve tutarlı bir yol izlemesini sağlayan temel deneyim katmanıdır.

## Bölüm Sonu Kontrol Listesi

- [ ] Navigation kavramını açıklayabiliyorum.
- [ ] Route yığını mantığını yorumlayabiliyorum.
- [ ] `Navigator.push` ile yeni sayfaya geçebiliyorum.
- [ ] `Navigator.pop` ile önceki sayfaya dönebiliyorum.
- [ ] `MaterialPageRoute` kullanabiliyorum.
- [ ] Sayfaya veri gönderebiliyorum.
- [ ] Sayfadan geriye veri döndürebiliyorum.
- [ ] Named routes yapısını temel düzeyde kurabiliyorum.
