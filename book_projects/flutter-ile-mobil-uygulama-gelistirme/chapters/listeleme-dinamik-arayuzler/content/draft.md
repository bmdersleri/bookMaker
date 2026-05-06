---
chapter_id: listeleme-dinamik-arayuzler
chapter_no: 8
title: "Listeleme ve Dinamik Arayüzler"
artifact_type: chapter
artifact_version: project-based
language: tr
---

# Bölüm 6 — Listeleme ve Dinamik Arayüzler

## Bölümün Amacı

Bu bölümde Flutter uygulamalarında verileri listeleme, dinamik arayüz üretme ve liste öğeleriyle kullanıcı etkileşimi kurma konuları ele alınmaktadır. Önceki bölümlerde widget mantığı, layout sistemi, etkileşim ve formlar incelenmişti. Bu bölümde ise uygulama içinde birden fazla verinin düzenli biçimde gösterilmesi üzerinde durulacaktır.

Mobil uygulamalarda liste yapıları çok yaygındır. Ders listesi, öğrenci listesi, görev listesi, ürün listesi, bildirim listesi, mesajlar, etkinlikler ve rapor kayıtları gibi birçok ekran listeleme mantığına dayanır. Flutter’da bu tür arayüzler için `ListView`, `ListView.builder`, `ListTile`, `Card`, `GridView`, model sınıfları ve koleksiyon işlemleri kullanılır.

Bu bölüm sonunda öğrenci:

- Flutter’da statik ve dinamik listeleme arasındaki farkı açıklayabilir.
- `ListView` ve `ListView.builder` kullanabilir.
- `ListTile` ile okunabilir liste öğeleri oluşturabilir.
- Basit model sınıfı ile veri temsil edebilir.
- Liste verisinden dinamik widget üretebilir.
- Liste öğesi ekleme, silme ve filtreleme işlemlerini uygulayabilir.
- `GridView` ile basit ızgara görünümü oluşturabilir.
- Liste ekranlarını daha okunabilir widget bileşenlerine ayırabilir.

## Listeleme Neden Önemlidir?

Mobil uygulamaların büyük bölümü bir veri kümesini kullanıcıya göstermeye dayanır. Kullanıcı bu verileri inceler, filtreler, seçer, düzenler veya detayına gider. Bu nedenle listeleme ekranları uygulama geliştirmede merkezi bir role sahiptir.

Örneğin bir eğitim uygulamasında şu ekranlar liste yapısı kullanabilir:

- Dersler
- Haftalık konular
- Öğrenci görevleri
- Duyurular
- Sınav sonuçları
- Kaynak dokümanlar
- Geri bildirim kayıtları

Flutter’da listeleme yalnızca ekrana metin basmak değildir. Verinin model hâline getirilmesi, uygun widget ile temsil edilmesi, performanslı biçimde üretilmesi ve kullanıcı etkileşimlerine cevap vermesi gerekir.

::: {custom-style="Dikkat Kutusu"}
**Dikkat:** Küçük ve sabit listeler için `ListView` yeterli olabilir. Ancak veri sayısı arttığında `ListView.builder` daha doğru bir tercihtir.
:::

## Statik Liste: `ListView`

`ListView`, child widget’ları kaydırılabilir bir liste içinde gösterir. Sabit sayıda öğe için `children` özelliği kullanılabilir.

```yaml
CODE_META:
  id: b06_kod01_listview_statik
  chapter: 6
  language: dart
  framework: flutter
  runnable: true
  file: lib/main.dart
  purpose: ListView ile sabit sayıda liste öğesi gösterme
```

```dart
import 'package:flutter/material.dart';

void main() {
  runApp(const StatikListeUygulamasi());
}

class StatikListeUygulamasi extends StatelessWidget {
  const StatikListeUygulamasi({super.key});

  @override
  Widget build(BuildContext context) {
    return const MaterialApp(
      home: StatikListeSayfasi(),
    );
  }
}

class StatikListeSayfasi extends StatelessWidget {
  const StatikListeSayfasi({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Statik Liste'),
      ),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: const [
          ListTile(
            leading: Icon(Icons.book),
            title: Text('Flutter’a Giriş'),
            subtitle: Text('Hafta 1'),
          ),
          ListTile(
            leading: Icon(Icons.code),
            title: Text('Dart Temelleri'),
            subtitle: Text('Hafta 2'),
          ),
          ListTile(
            leading: Icon(Icons.widgets),
            title: Text('Widget Mantığı'),
            subtitle: Text('Hafta 3'),
          ),
        ],
      ),
    );
  }
}
```

Bu örnekte liste öğeleri elle yazılmıştır. Öğelerin sayısı az ve sabitse bu yaklaşım kabul edilebilir. Ancak gerçek uygulamalarda veriler çoğunlukla bir liste, API cevabı veya yerel veritabanından gelir. Bu durumda dinamik listeleme gerekir.

## `ListTile` ile Liste Öğesi Tasarlama

`ListTile`, liste içinde sık kullanılan hazır bir öğe tasarım widget’ıdır. Başlık, alt başlık, sol ikon ve sağ aksiyon alanı gibi yapıları destekler.

`ListTile` içinde sık kullanılan alanlar şunlardır:

| Özellik | Açıklama |
|---|---|
| `leading` | Öğenin sol tarafındaki ikon veya görsel |
| `title` | Ana başlık |
| `subtitle` | Alt açıklama |
| `trailing` | Sağ taraftaki ikon veya aksiyon |
| `onTap` | Öğeye dokunulduğunda çalışacak fonksiyon |

Aşağıdaki örnek, seçilen liste öğesine göre ekranda mesaj göstermektedir.

```yaml
CODE_META:
  id: b06_kod02_listtile_ontap
  chapter: 6
  language: dart
  framework: flutter
  runnable: true
  file: lib/main.dart
  purpose: ListTile onTap ile liste öğesi etkileşimi kurma
```

```dart
import 'package:flutter/material.dart';

void main() {
  runApp(const ListTileEtkilesimUygulamasi());
}

class ListTileEtkilesimUygulamasi extends StatelessWidget {
  const ListTileEtkilesimUygulamasi({super.key});

  @override
  Widget build(BuildContext context) {
    return const MaterialApp(
      home: ListTileEtkilesimSayfasi(),
    );
  }
}

class ListTileEtkilesimSayfasi extends StatelessWidget {
  const ListTileEtkilesimSayfasi({super.key});

  void konuSecildi(BuildContext context, String konu) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text('$konu seçildi.'),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final konular = [
      'Widget Mantığı',
      'Layout Sistemi',
      'Formlar',
      'Dinamik Listeler',
    ];

    return Scaffold(
      appBar: AppBar(
        title: const Text('Konu Listesi'),
      ),
      body: ListView(
        children: [
          for (final konu in konular)
            ListTile(
              leading: const Icon(Icons.check_circle_outline),
              title: Text(konu),
              trailing: const Icon(Icons.chevron_right),
              onTap: () => konuSecildi(context, konu),
            ),
        ],
      ),
    );
  }
}
```

Bu örnekte `for` ifadesiyle liste verisinden widget üretilmiştir. Öğeye dokunulduğunda `SnackBar` ile seçilen konu gösterilir.

## Model Sınıfı ile Veri Temsili

Uygulama verilerini yalnızca `String` listeleriyle temsil etmek her zaman yeterli değildir. Bir ders kaydında başlık, hafta, açıklama, tamamlanma durumu ve ikon gibi birden fazla bilgi olabilir. Bu durumda model sınıfı kullanmak daha düzenli bir yaklaşımdır.

```yaml
CODE_META:
  id: b06_kod03_model_sinifi
  chapter: 6
  language: dart
  framework: flutter
  runnable: true
  file: lib/main.dart
  purpose: Basit model sınıfı ile liste verisi temsil etme
```

```dart
import 'package:flutter/material.dart';

void main() {
  runApp(const ModelListeUygulamasi());
}

class DersKonusu {
  final String baslik;
  final String hafta;
  final String aciklama;
  final bool tamamlandi;

  const DersKonusu({
    required this.baslik,
    required this.hafta,
    required this.aciklama,
    required this.tamamlandi,
  });
}

class ModelListeUygulamasi extends StatelessWidget {
  const ModelListeUygulamasi({super.key});

  @override
  Widget build(BuildContext context) {
    return const MaterialApp(
      home: ModelListeSayfasi(),
    );
  }
}

class ModelListeSayfasi extends StatelessWidget {
  const ModelListeSayfasi({super.key});

  @override
  Widget build(BuildContext context) {
    final konular = [
      const DersKonusu(
        baslik: 'Flutter’a Giriş',
        hafta: 'Hafta 1',
        aciklama: 'Flutter ekosistemi ve proje yapısı',
        tamamlandi: true,
      ),
      const DersKonusu(
        baslik: 'Dart Temelleri',
        hafta: 'Hafta 2',
        aciklama: 'Değişkenler, fonksiyonlar ve sınıflar',
        tamamlandi: true,
      ),
      const DersKonusu(
        baslik: 'Dinamik Listeler',
        hafta: 'Hafta 6',
        aciklama: 'ListView.builder ve model tabanlı arayüz',
        tamamlandi: false,
      ),
    ];

    return Scaffold(
      appBar: AppBar(
        title: const Text('Model Tabanlı Liste'),
      ),
      body: ListView(
        children: [
          for (final konu in konular)
            ListTile(
              leading: Icon(
                konu.tamamlandi
                    ? Icons.check_circle
                    : Icons.radio_button_unchecked,
              ),
              title: Text(konu.baslik),
              subtitle: Text('${konu.hafta} • ${konu.aciklama}'),
            ),
        ],
      ),
    );
  }
}
```

Bu örnekte `DersKonusu` sınıfı, liste öğesinin veri modelini temsil eder. Bu yaklaşım kodun okunabilirliğini artırır ve ilerleyen bölümlerde API veya yerel veri saklama yapılarıyla çalışmayı kolaylaştırır.

## `ListView.builder`

`ListView.builder`, liste öğelerini ihtiyaç oldukça üretir. Özellikle veri sayısının fazla olduğu durumlarda daha verimli bir yaklaşımdır. Çünkü tüm liste öğelerini aynı anda oluşturmak yerine ekranda ihtiyaç duyulan öğeler oluşturulur.

```yaml
CODE_META:
  id: b06_kod04_listview_builder
  chapter: 6
  language: dart
  framework: flutter
  runnable: true
  file: lib/main.dart
  purpose: ListView.builder ile dinamik ve performanslı liste oluşturma
```

```dart
import 'package:flutter/material.dart';

void main() {
  runApp(const BuilderListeUygulamasi());
}

class BuilderListeUygulamasi extends StatelessWidget {
  const BuilderListeUygulamasi({super.key});

  @override
  Widget build(BuildContext context) {
    return const MaterialApp(
      home: BuilderListeSayfasi(),
    );
  }
}

class BuilderListeSayfasi extends StatelessWidget {
  const BuilderListeSayfasi({super.key});

  @override
  Widget build(BuildContext context) {
    final dersler = List.generate(
      30,
      (index) => 'Ders konusu ${index + 1}',
    );

    return Scaffold(
      appBar: AppBar(
        title: const Text('ListView.builder'),
      ),
      body: ListView.builder(
        itemCount: dersler.length,
        itemBuilder: (context, index) {
          final ders = dersler[index];

          return ListTile(
            leading: CircleAvatar(
              child: Text('${index + 1}'),
            ),
            title: Text(ders),
            subtitle: const Text('Dinamik olarak üretildi'),
          );
        },
      ),
    );
  }
}
```

Bu örnekte `itemCount`, listenin kaç öğeden oluştuğunu belirtir. `itemBuilder` ise her bir indeks için ilgili widget’ı üretir.

::: {custom-style="Sinav Notu Kutusu"}
**Sınav Notu:** `ListView.builder`, uzun veya dinamik listelerde tercih edilmelidir. Çünkü öğeleri ihtiyaç oldukça üretir.
:::

## Liste Öğelerini Card ile Görselleştirme

Liste öğeleri yalnızca `ListTile` ile değil, `Card` içinde daha zengin görsel yapılara sahip olacak şekilde de tasarlanabilir.

```yaml
CODE_META:
  id: b06_kod05_card_liste
  chapter: 6
  language: dart
  framework: flutter
  runnable: true
  file: lib/main.dart
  purpose: Card ve ListTile ile daha okunabilir liste öğeleri tasarlama
```

```dart
import 'package:flutter/material.dart';

void main() {
  runApp(const CardListeUygulamasi());
}

class Gorev {
  final String baslik;
  final String aciklama;
  final int oncelik;

  const Gorev({
    required this.baslik,
    required this.aciklama,
    required this.oncelik,
  });
}

class CardListeUygulamasi extends StatelessWidget {
  const CardListeUygulamasi({super.key});

  @override
  Widget build(BuildContext context) {
    return const MaterialApp(
      home: CardListeSayfasi(),
    );
  }
}

class CardListeSayfasi extends StatelessWidget {
  const CardListeSayfasi({super.key});

  @override
  Widget build(BuildContext context) {
    final gorevler = [
      const Gorev(
        baslik: 'Dart tekrarını yap',
        aciklama: 'Fonksiyon ve sınıf örneklerini incele',
        oncelik: 1,
      ),
      const Gorev(
        baslik: 'Layout alıştırması hazırla',
        aciklama: 'Row, Column ve Expanded kullan',
        oncelik: 2,
      ),
      const Gorev(
        baslik: 'Form uygulamasını tamamla',
        aciklama: 'Validator ve SnackBar ekle',
        oncelik: 3,
      ),
    ];

    return Scaffold(
      appBar: AppBar(
        title: const Text('Card Liste'),
      ),
      body: ListView.builder(
        padding: const EdgeInsets.all(12),
        itemCount: gorevler.length,
        itemBuilder: (context, index) {
          final gorev = gorevler[index];

          return Card(
            child: ListTile(
              leading: CircleAvatar(
                child: Text('${gorev.oncelik}'),
              ),
              title: Text(gorev.baslik),
              subtitle: Text(gorev.aciklama),
              trailing: const Icon(Icons.chevron_right),
            ),
          );
        },
      ),
    );
  }
}
```

Bu örnekte her görev bir `Card` içinde gösterilmiştir. Böylece öğeler görsel olarak birbirinden daha net ayrılır.

## Listeye Öğe Ekleme ve Silme

Dinamik arayüzlerde kullanıcı listeye yeni öğe ekleyebilir veya mevcut öğeyi silebilir. Bu durumda liste verisi state içinde tutulur ve değişikliklerden sonra `setState()` çağrılır.

```yaml
CODE_META:
  id: b06_kod06_liste_ekle_sil
  chapter: 6
  language: dart
  framework: flutter
  runnable: true
  file: lib/main.dart
  purpose: State içinde liste tutma, öğe ekleme ve silme
```

```dart
import 'package:flutter/material.dart';

void main() {
  runApp(const DinamikGorevUygulamasi());
}

class DinamikGorevUygulamasi extends StatelessWidget {
  const DinamikGorevUygulamasi({super.key});

  @override
  Widget build(BuildContext context) {
    return const MaterialApp(
      home: DinamikGorevSayfasi(),
    );
  }
}

class DinamikGorevSayfasi extends StatefulWidget {
  const DinamikGorevSayfasi({super.key});

  @override
  State<DinamikGorevSayfasi> createState() => _DinamikGorevSayfasiState();
}

class _DinamikGorevSayfasiState extends State<DinamikGorevSayfasi> {
  final TextEditingController gorevController = TextEditingController();

  final List<String> gorevler = [
    'Bölüm 6 taslağını oku',
    'ListView.builder örneğini çalıştır',
    'Mini uygulamayı geliştir',
  ];

  @override
  void dispose() {
    gorevController.dispose();
    super.dispose();
  }

  void gorevEkle() {
    final yeniGorev = gorevController.text.trim();

    if (yeniGorev.isEmpty) {
      return;
    }

    setState(() {
      gorevler.add(yeniGorev);
      gorevController.clear();
    });
  }

  void gorevSil(int index) {
    setState(() {
      gorevler.removeAt(index);
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Dinamik Görev Listesi'),
      ),
      body: Column(
        children: [
          Padding(
            padding: const EdgeInsets.all(12),
            child: Row(
              children: [
                Expanded(
                  child: TextField(
                    controller: gorevController,
                    decoration: const InputDecoration(
                      labelText: 'Yeni görev',
                      border: OutlineInputBorder(),
                    ),
                  ),
                ),
                const SizedBox(width: 8),
                ElevatedButton(
                  onPressed: gorevEkle,
                  child: const Text('Ekle'),
                ),
              ],
            ),
          ),
          Expanded(
            child: ListView.builder(
              itemCount: gorevler.length,
              itemBuilder: (context, index) {
                final gorev = gorevler[index];

                return ListTile(
                  leading: CircleAvatar(
                    child: Text('${index + 1}'),
                  ),
                  title: Text(gorev),
                  trailing: IconButton(
                    icon: const Icon(Icons.delete_outline),
                    onPressed: () => gorevSil(index),
                  ),
                );
              },
            ),
          ),
        ],
      ),
    );
  }
}
```

Bu örnekte görev listesi state içinde tutulur. Yeni görev eklendiğinde `gorevler.add()` çağrılır. Silme işleminde ise `removeAt(index)` kullanılır. Her iki işlem de `setState()` içinde yapıldığı için arayüz güncellenir.

## Liste Filtreleme

Listeleme ekranlarında arama ve filtreleme önemli bir kullanıcı deneyimi unsurudur. Aşağıdaki örnekte kullanıcı metin alanına yazdıkça ders listesi filtrelenmektedir.

```yaml
CODE_META:
  id: b06_kod07_liste_filtreleme
  chapter: 6
  language: dart
  framework: flutter
  runnable: true
  file: lib/main.dart
  purpose: TextField ve where ile liste filtreleme
```

```dart
import 'package:flutter/material.dart';

void main() {
  runApp(const FiltrelemeUygulamasi());
}

class FiltrelemeUygulamasi extends StatelessWidget {
  const FiltrelemeUygulamasi({super.key});

  @override
  Widget build(BuildContext context) {
    return const MaterialApp(
      home: FiltrelemeSayfasi(),
    );
  }
}

class FiltrelemeSayfasi extends StatefulWidget {
  const FiltrelemeSayfasi({super.key});

  @override
  State<FiltrelemeSayfasi> createState() => _FiltrelemeSayfasiState();
}

class _FiltrelemeSayfasiState extends State<FiltrelemeSayfasi> {
  String aramaMetni = '';

  final List<String> dersler = [
    'Flutter’a Giriş',
    'Dart Temelleri',
    'Widget Mantığı',
    'Layout Sistemi',
    'Etkileşim ve Formlar',
    'Listeleme ve Dinamik Arayüzler',
    'Navigation ve Route',
  ];

  @override
  Widget build(BuildContext context) {
    final filtreliDersler = dersler
        .where(
          (ders) => ders.toLowerCase().contains(aramaMetni.toLowerCase()),
        )
        .toList();

    return Scaffold(
      appBar: AppBar(
        title: const Text('Liste Filtreleme'),
      ),
      body: Column(
        children: [
          Padding(
            padding: const EdgeInsets.all(12),
            child: TextField(
              decoration: const InputDecoration(
                labelText: 'Ders ara',
                prefixIcon: Icon(Icons.search),
                border: OutlineInputBorder(),
              ),
              onChanged: (deger) {
                setState(() {
                  aramaMetni = deger;
                });
              },
            ),
          ),
          Expanded(
            child: ListView.builder(
              itemCount: filtreliDersler.length,
              itemBuilder: (context, index) {
                final ders = filtreliDersler[index];

                return ListTile(
                  leading: const Icon(Icons.menu_book_outlined),
                  title: Text(ders),
                );
              },
            ),
          ),
        ],
      ),
    );
  }
}
```

Bu örnekte `where()` metodu ile arama metnini içeren dersler seçilmiştir. Ardından `.toList()` ile sonuçlar listeye dönüştürülmüştür.

::: {custom-style="Ipucu Kutusu"}
**İpucu:** Filtreleme işlemi basit listelerde doğrudan state içinde yapılabilir. Daha büyük uygulamalarda bu mantık ayrı servis veya state management katmanına taşınabilir.
:::

## Boş Liste Durumu

Listeleme ekranlarında yalnızca veri varken nasıl görüneceği değil, veri yokken ne gösterileceği de düşünülmelidir. Boş liste durumları kullanıcıya anlamlı bir açıklama sunmalıdır.

```dart
if (gorevler.isEmpty) {
  return const Center(
    child: Text('Henüz görev bulunmuyor.'),
  );
}
```

Boş durum mesajı, kullanıcının ekranın neden boş olduğunu anlamasını sağlar. İyi bir uygulamada gerekirse kullanıcıya yeni öğe ekleme veya filtreyi temizleme seçeneği de sunulabilir.

## `GridView` ile Izgara Görünümü

Bazı veriler dikey liste yerine ızgara yapısıyla gösterilebilir. Örneğin kategori kartları, ürünler, galeri öğeleri veya küçük bilgi kutuları için `GridView` kullanılabilir.

```yaml
CODE_META:
  id: b06_kod08_gridview_kartlar
  chapter: 6
  language: dart
  framework: flutter
  runnable: true
  file: lib/main.dart
  purpose: GridView.count ile basit ızgara görünümü oluşturma
```

```dart
import 'package:flutter/material.dart';

void main() {
  runApp(const GridViewUygulamasi());
}

class GridViewUygulamasi extends StatelessWidget {
  const GridViewUygulamasi({super.key});

  @override
  Widget build(BuildContext context) {
    return const MaterialApp(
      home: GridViewSayfasi(),
    );
  }
}

class GridViewSayfasi extends StatelessWidget {
  const GridViewSayfasi({super.key});

  @override
  Widget build(BuildContext context) {
    final kategoriler = [
      ('Dersler', Icons.menu_book),
      ('Görevler', Icons.checklist),
      ('Formlar', Icons.assignment),
      ('Raporlar', Icons.bar_chart),
      ('Ayarlar', Icons.settings),
      ('Yardım', Icons.help_outline),
    ];

    return Scaffold(
      appBar: AppBar(
        title: const Text('GridView Örneği'),
      ),
      body: GridView.count(
        padding: const EdgeInsets.all(16),
        crossAxisCount: 2,
        crossAxisSpacing: 12,
        mainAxisSpacing: 12,
        children: [
          for (final kategori in kategoriler)
            Card(
              child: InkWell(
                onTap: () {},
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    Icon(kategori.$2, size: 42),
                    const SizedBox(height: 12),
                    Text(kategori.$1),
                  ],
                ),
              ),
            ),
        ],
      ),
    );
  }
}
```

Bu örnekte `GridView.count` ile iki sütunlu bir ızgara oluşturulmuştur. `crossAxisCount`, satırdaki sütun sayısını belirler.

## Mini Uygulama: Dinamik Ders Takip Listesi

Bu mini uygulamada öğrencinin ders konularını takip edebileceği, arama yapabileceği ve tamamlanma durumunu değiştirebileceği bir liste ekranı geliştirilecektir.

[SCREENSHOT:b06_01_dinamik_ders_takip_listesi]

<!-- SCREENSHOT_META
id: b06_01_dinamik_ders_takip_listesi
chapter_id: chapter_08
title: "Dinamik Ders Takip Listesi"
kind: browser_page
url: "http://127.0.0.1:5173/__book__/listeleme-dinamik-arayuzler/b06_01_dinamik_ders_takip_listesi"
viewport: 1440x900
wait_for: "networkidle"
output_file: assets/auto/screenshots/b06_01_dinamik_ders_takip_listesi.png
caption: "Dinamik Ders Takip Listesi ekran görüntüsü."
validation_mode: capture
-->

```yaml
CODE_META:
  id: b06_kod09_dinamik_ders_takip_listesi
  chapter: 6
  language: dart
  framework: flutter
  runnable: true
  file: lib/main.dart
  purpose: Model, ListView.builder, filtreleme ve durum güncelleme kullanımı
  screenshot: b06_01_dinamik_ders_takip_listesi
```

```dart
import 'package:flutter/material.dart';

void main() {
  runApp(const DersTakipUygulamasi());
}

class DersKonusu {
  final String baslik;
  final String hafta;
  final String aciklama;
  final bool tamamlandi;

  const DersKonusu({
    required this.baslik,
    required this.hafta,
    required this.aciklama,
    required this.tamamlandi,
  });

  DersKonusu kopyala({
    String? baslik,
    String? hafta,
    String? aciklama,
    bool? tamamlandi,
  }) {
    return DersKonusu(
      baslik: baslik ?? this.baslik,
      hafta: hafta ?? this.hafta,
      aciklama: aciklama ?? this.aciklama,
      tamamlandi: tamamlandi ?? this.tamamlandi,
    );
  }
}

class DersTakipUygulamasi extends StatelessWidget {
  const DersTakipUygulamasi({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Ders Takip Listesi',
      theme: ThemeData(
        colorSchemeSeed: Colors.blue,
        useMaterial3: true,
      ),
      home: const DersTakipSayfasi(),
    );
  }
}

class DersTakipSayfasi extends StatefulWidget {
  const DersTakipSayfasi({super.key});

  @override
  State<DersTakipSayfasi> createState() => _DersTakipSayfasiState();
}

class _DersTakipSayfasiState extends State<DersTakipSayfasi> {
  String aramaMetni = '';

  List<DersKonusu> konular = const [
    DersKonusu(
      baslik: 'Flutter’a Giriş',
      hafta: 'Hafta 1',
      aciklama: 'Flutter SDK, proje yapısı ve çalışma mantığı',
      tamamlandi: true,
    ),
    DersKonusu(
      baslik: 'Dart Temelleri',
      hafta: 'Hafta 2',
      aciklama: 'Değişkenler, fonksiyonlar, sınıflar ve async giriş',
      tamamlandi: true,
    ),
    DersKonusu(
      baslik: 'Widget Mantığı',
      hafta: 'Hafta 3',
      aciklama: 'StatelessWidget, StatefulWidget ve setState',
      tamamlandi: true,
    ),
    DersKonusu(
      baslik: 'Layout Sistemi',
      hafta: 'Hafta 4',
      aciklama: 'Row, Column, Expanded, Wrap ve LayoutBuilder',
      tamamlandi: true,
    ),
    DersKonusu(
      baslik: 'Etkileşim ve Formlar',
      hafta: 'Hafta 5',
      aciklama: 'TextField, Form, validator ve SnackBar',
      tamamlandi: false,
    ),
    DersKonusu(
      baslik: 'Listeleme ve Dinamik Arayüzler',
      hafta: 'Hafta 6',
      aciklama: 'ListView.builder, model ve filtreleme',
      tamamlandi: false,
    ),
  ];

  void durumDegistir(DersKonusu konu) {
    final index = konular.indexOf(konu);

    if (index == -1) {
      return;
    }

    setState(() {
      konular[index] = konu.kopyala(
        tamamlandi: !konu.tamamlandi,
      );
    });
  }

  @override
  Widget build(BuildContext context) {
    final filtreliKonular = konular
        .where(
          (konu) =>
              konu.baslik.toLowerCase().contains(aramaMetni.toLowerCase()) ||
              konu.aciklama.toLowerCase().contains(aramaMetni.toLowerCase()),
        )
        .toList();

    final tamamlananSayisi =
        konular.where((konu) => konu.tamamlandi).length;

    return Scaffold(
      appBar: AppBar(
        title: const Text('Ders Takip Listesi'),
      ),
      body: Column(
        children: [
          OzetPaneli(
            toplam: konular.length,
            tamamlanan: tamamlananSayisi,
          ),
          Padding(
            padding: const EdgeInsets.all(12),
            child: TextField(
              decoration: const InputDecoration(
                labelText: 'Konu ara',
                prefixIcon: Icon(Icons.search),
                border: OutlineInputBorder(),
              ),
              onChanged: (deger) {
                setState(() {
                  aramaMetni = deger;
                });
              },
            ),
          ),
          Expanded(
            child: filtreliKonular.isEmpty
                ? const BosListeMesaji()
                : ListView.builder(
                    itemCount: filtreliKonular.length,
                    itemBuilder: (context, index) {
                      final konu = filtreliKonular[index];

                      return DersKonusuKarti(
                        konu: konu,
                        durumDegistir: () => durumDegistir(konu),
                      );
                    },
                  ),
          ),
        ],
      ),
    );
  }
}

class OzetPaneli extends StatelessWidget {
  final int toplam;
  final int tamamlanan;

  const OzetPaneli({
    super.key,
    required this.toplam,
    required this.tamamlanan,
  });

  @override
  Widget build(BuildContext context) {
    final oran = toplam == 0 ? 0.0 : tamamlanan / toplam;

    return Card(
      margin: const EdgeInsets.all(12),
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            Text(
              'Tamamlanan Konular',
              style: Theme.of(context).textTheme.titleMedium,
            ),
            const SizedBox(height: 8),
            LinearProgressIndicator(value: oran),
            const SizedBox(height: 8),
            Text('$tamamlanan / $toplam konu tamamlandı'),
          ],
        ),
      ),
    );
  }
}

class DersKonusuKarti extends StatelessWidget {
  final DersKonusu konu;
  final VoidCallback durumDegistir;

  const DersKonusuKarti({
    super.key,
    required this.konu,
    required this.durumDegistir,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      margin: const EdgeInsets.symmetric(
        horizontal: 12,
        vertical: 6,
      ),
      child: ListTile(
        leading: Icon(
          konu.tamamlandi
              ? Icons.check_circle
              : Icons.radio_button_unchecked,
        ),
        title: Text(konu.baslik),
        subtitle: Text('${konu.hafta} • ${konu.aciklama}'),
        trailing: Switch(
          value: konu.tamamlandi,
          onChanged: (_) => durumDegistir(),
        ),
      ),
    );
  }
}

class BosListeMesaji extends StatelessWidget {
  const BosListeMesaji({super.key});

  @override
  Widget build(BuildContext context) {
    return const Center(
      child: Text('Arama ölçütüne uygun konu bulunamadı.'),
    );
  }
}
```

Bu mini uygulamada model sınıfı, listeleme, filtreleme, boş liste durumu ve state güncelleme bir arada kullanılmıştır. `DersKonusuKarti`, liste öğesinin görsel temsilini ayrı bir widget olarak ele alır. `OzetPaneli` ise tamamlanma oranını üst bölümde gösterir.

## Performans ve Okunabilirlik Önerileri

Dinamik liste ekranlarında şu öneriler dikkate alınmalıdır:

- Uzun listelerde `ListView.builder` tercih edilmelidir.
- Liste öğesi tasarımı ayrı widget sınıfına taşınmalıdır.
- Sabit öğelerde mümkün olduğunca `const` kullanılmalıdır.
- Gereksiz iç içe widget yapılarından kaçınılmalıdır.
- Filtreleme ve sıralama mantığı büyüdüğünde ayrı fonksiyonlara ayrılmalıdır.
- Boş liste ve hata durumları kullanıcıya açıklanmalıdır.
- Uzun metinler için taşma davranışı düşünülmelidir.

Örneğin uzun başlıklar için `maxLines` ve `overflow` kullanılabilir:

```dart
Text(
  konu.baslik,
  maxLines: 1,
  overflow: TextOverflow.ellipsis,
)
```

Bu kullanım, çok uzun başlıkların arayüzü bozmasını önleyebilir.

## Sık Yapılan Hatalar

| Hata | Açıklama | Çözüm |
|---|---|---|
| Uzun listede `children` kullanmak | Tüm öğeler baştan oluşturulur | `ListView.builder` kullan |
| Model sınıfı kullanmamak | Kod karmaşıklaşır | Veri yapısını modelle |
| Listeyi güncelleyip `setState()` çağırmamak | Arayüz yenilenmez | Değişiklikleri `setState()` içinde yap |
| Boş liste durumunu düşünmemek | Kullanıcı ekranın neden boş olduğunu anlayamaz | Açıklayıcı boş durum mesajı ekle |
| Filtreleme sonucunu yanlış listelemek | Arama sonuçları hatalı görünür | Filtrelenmiş liste üzerinden builder çalıştır |
| Silme işleminde yanlış index kullanmak | Beklenmeyen öğe silinebilir | İşlem yapılan veri listesini dikkatli takip et |
| Liste öğesini çok karmaşık yapmak | Bakım zorlaşır | Öğeyi ayrı widget sınıfına taşı |

## Laboratuvar Görevi

Bu laboratuvar çalışmasında öğrenciden “Öğrenci Görev Takip Listesi” adlı dinamik bir liste uygulaması geliştirmesi beklenmektedir.

### İstenenler

1. Uygulama başlığı “Öğrenci Görev Takip Listesi” olmalıdır.
2. Görevleri temsil eden bir model sınıfı oluşturulmalıdır.
3. Her görev için başlık, açıklama ve tamamlandı bilgisi tutulmalıdır.
4. Görevler `ListView.builder` ile listelenmelidir.
5. Her görev `Card` ve `ListTile` kullanılarak gösterilmelidir.
6. Kullanıcı yeni görev ekleyebilmelidir.
7. Kullanıcı görev silebilmelidir.
8. Kullanıcı görevleri metin alanı ile filtreleyebilmelidir.
9. Boş liste durumunda açıklayıcı mesaj gösterilmelidir.
10. Liste öğesi ayrı bir widget sınıfı olarak tasarlanmalıdır.

### Beklenen Kazanımlar

Bu laboratuvar sonunda öğrenci:

- Model tabanlı listeleme yapabilir.
- `ListView.builder` ile dinamik liste üretebilir.
- State içinde liste verisini güncelleyebilir.
- Kullanıcıdan gelen girişle listeye öğe ekleyebilir.
- Liste filtreleme ve boş durum yönetimi uygulayabilir.
- Liste öğelerini okunabilir alt widget’lara ayırabilir.

## Değerlendirme Rubriği

| Ölçüt | Puan | Açıklama |
|---|---:|---|
| Model sınıfı | 15 | Görev verisi anlamlı bir modelle temsil edilmiştir |
| Dinamik listeleme | 20 | `ListView.builder` doğru kullanılmıştır |
| Ekleme ve silme | 20 | Liste state içinde güncellenebilmiştir |
| Filtreleme | 15 | Arama metnine göre liste filtrelenmiştir |
| Boş durum yönetimi | 10 | Veri yokken anlamlı mesaj gösterilmiştir |
| Widget kompozisyonu | 10 | Liste öğesi ayrı widget olarak tasarlanmıştır |
| Kod okunabilirliği | 10 | Değişken ve sınıf adları anlamlıdır |

## Bölüm Özeti

Bu bölümde Flutter’da listeleme ve dinamik arayüz üretme konuları incelendi. `ListView`, `ListTile`, model sınıfları, `ListView.builder`, `Card`, `GridView`, listeye öğe ekleme, silme, filtreleme ve boş liste durumu örneklerle açıklandı.

Mini uygulamada ders konularını takip eden, arama yapabilen ve tamamlanma durumunu değiştirebilen bir liste ekranı geliştirildi. Bu örnek, sonraki bölümlerde ele alınacak navigation, state management, API verileri ve yerel veri saklama konularına temel oluşturur.

Bölümün ana fikri şudur: Liste ekranları yalnızca veriyi göstermekle kalmaz; veri modeli, kullanıcı etkileşimi, performans, filtreleme ve boş durum yönetimiyle birlikte düşünülmelidir.

## Bölüm Sonu Kontrol Listesi

- [ ] `ListView` ve `ListView.builder` farkını açıklayabiliyorum.
- [ ] `ListTile` ile okunabilir liste öğesi oluşturabiliyorum.
- [ ] Model sınıfı ile liste verisi temsil edebiliyorum.
- [ ] `ListView.builder` içinde `itemCount` ve `itemBuilder` kullanabiliyorum.
- [ ] State içinde listeye öğe ekleyip silebiliyorum.
- [ ] Liste filtreleme işlemi yapabiliyorum.
- [ ] Boş liste durumunu kullanıcıya açıklayabiliyorum.
- [ ] `GridView` ile basit ızgara görünümü oluşturabiliyorum.
