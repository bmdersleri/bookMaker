---
chapter_id: async-api-json
chapter_no: 1
title: "Asenkron Programlama, API ve JSON"
artifact_type: chapter
artifact_version: project-based
language: tr
---

# Bölüm 9 — Asenkron Programlama, API ve JSON

## Bölümün Amacı

Bu bölümde Flutter uygulamalarında asenkron işlemler, API istekleri ve JSON verisiyle çalışma konusu ele alınmaktadır. Gerçek uygulamalarda veriler çoğu zaman sabit listelerden değil; uzak servislerden, REST API uç noktalarından veya yerel veri kaynaklarından gelir. Bu nedenle `Future`, `async`, `await`, HTTP isteği, JSON çözümleme ve model sınıfına dönüştürme becerileri Flutter geliştiricisi için temel düzeyde gereklidir.

Bu bölüm sonunda öğrenci `Future`, `async`, `await`, `jsonDecode`, model sınıfı, servis sınıfı ve `FutureBuilder` ile temel API veri akışını kurabilir.

## Asenkron Programlama Nedir?

Asenkron programlama, uzun sürebilecek işlemlerin kullanıcı arayüzünü kilitlemeden yürütülmesini sağlar. API isteği göndermek, dosya okumak, veritabanından kayıt almak veya zamanlayıcı beklemek asenkron işlem örnekleridir.

::: {custom-style="Dikkat Kutusu"}
**Dikkat:** Ağ isteği, dosya okuma veya uzun süren hesaplama gibi işlemler doğrudan `build()` metodu içinde başlatılmamalıdır.
:::

## `Future`, `async` ve `await`

```yaml
CODE_META:
  id: b09_kod01_future_async_await
  chapter: 9
  language: dart
  framework: flutter
  runnable: true
  file: lib/main.dart
  purpose: Future, async ve await kullanımını gösterme
```

```dart
import 'package:flutter/material.dart';

void main() {
  runApp(const AsyncGirisUygulamasi());
}

Future<String> dersBilgisiGetir() async {
  await Future.delayed(const Duration(seconds: 2));
  return 'Flutter asenkron programlama konusu yüklendi.';
}

class AsyncGirisUygulamasi extends StatelessWidget {
  const AsyncGirisUygulamasi({super.key});

  @override
  Widget build(BuildContext context) {
    return const MaterialApp(home: AsyncGirisSayfasi());
  }
}

class AsyncGirisSayfasi extends StatefulWidget {
  const AsyncGirisSayfasi({super.key});

  @override
  State<AsyncGirisSayfasi> createState() => _AsyncGirisSayfasiState();
}

class _AsyncGirisSayfasiState extends State<AsyncGirisSayfasi> {
  String mesaj = 'Henüz veri yüklenmedi.';

  Future<void> yukle() async {
    final sonuc = await dersBilgisiGetir();
    setState(() {
      mesaj = sonuc;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Future, async, await')),
      body: Center(
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Text(mesaj, textAlign: TextAlign.center),
            const SizedBox(height: 16),
            ElevatedButton(
              onPressed: yukle,
              child: const Text('Veriyi Yükle'),
            ),
          ],
        ),
      ),
    );
  }
}
```

## JSON Verisini Model Sınıfına Dönüştürme

JSON, web servislerinde veri taşımak için yaygın kullanılan metinsel veri biçimidir. Dart’ta JSON çözümlemek için `dart:convert` paketinden `jsonDecode` kullanılır.

```yaml
CODE_META:
  id: b09_kod02_jsondecode_model
  chapter: 9
  language: dart
  framework: flutter
  runnable: true
  file: lib/main.dart
  purpose: JSON verisini model sınıfına dönüştürme
```

```dart
import 'dart:convert';
import 'package:flutter/material.dart';

void main() {
  runApp(const JsonModelUygulamasi());
}

class Ders {
  final int id;
  final String baslik;
  final String aciklama;

  const Ders({
    required this.id,
    required this.baslik,
    required this.aciklama,
  });

  factory Ders.fromJson(Map<String, dynamic> json) {
    return Ders(
      id: json['id'] as int,
      baslik: json['baslik'] as String,
      aciklama: json['aciklama'] as String,
    );
  }
}

class JsonModelUygulamasi extends StatelessWidget {
  const JsonModelUygulamasi({super.key});

  @override
  Widget build(BuildContext context) {
    const jsonMetni = '{"id":1,"baslik":"API ve JSON","aciklama":"Flutter içinde JSON çözümleme"}';
    final Map<String, dynamic> veri = jsonDecode(jsonMetni);
    final ders = Ders.fromJson(veri);

    return MaterialApp(
      home: Scaffold(
        appBar: AppBar(title: const Text('JSON Model')),
        body: Center(
          child: ListTile(
            leading: CircleAvatar(child: Text('${ders.id}')),
            title: Text(ders.baslik),
            subtitle: Text(ders.aciklama),
          ),
        ),
      ),
    );
  }
}
```

## `FutureBuilder` ile Veri Akışı

```yaml
CODE_META:
  id: b09_kod03_futurebuilder_servis
  chapter: 9
  language: dart
  framework: flutter
  runnable: true
  file: lib/main.dart
  purpose: FutureBuilder ile yükleniyor, hata ve başarı durumlarını yönetme
```

```dart
import 'package:flutter/material.dart';

void main() {
  runApp(const ApiServisUygulamasi());
}

class Ders {
  final String baslik;
  final String hafta;

  const Ders({required this.baslik, required this.hafta});
}

class DersApiServisi {
  Future<List<Ders>> dersleriGetir() async {
    await Future.delayed(const Duration(seconds: 1));

    try {
      return const [
        Ders(baslik: 'Asenkron Programlama', hafta: 'Hafta 9'),
        Ders(baslik: 'API ve JSON', hafta: 'Hafta 9'),
        Ders(baslik: 'FutureBuilder', hafta: 'Hafta 9'),
      ];
    } catch (hata) {
      throw Exception('API verisi alınamadı: $hata');
    }
  }
}

class ApiServisUygulamasi extends StatelessWidget {
  const ApiServisUygulamasi({super.key});

  @override
  Widget build(BuildContext context) {
    return const MaterialApp(home: ApiServisSayfasi());
  }
}

class ApiServisSayfasi extends StatefulWidget {
  const ApiServisSayfasi({super.key});

  @override
  State<ApiServisSayfasi> createState() => _ApiServisSayfasiState();
}

class _ApiServisSayfasiState extends State<ApiServisSayfasi> {
  final DersApiServisi servis = DersApiServisi();
  late Future<List<Ders>> dersFuture;

  @override
  void initState() {
    super.initState();
    dersFuture = servis.dersleriGetir();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('API Servis Yapısı')),
      body: FutureBuilder<List<Ders>>(
        future: dersFuture,
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator());
          }

          if (snapshot.hasError) {
            return Center(child: Text('Hata: ${snapshot.error}'));
          }

          final dersler = snapshot.data ?? [];

          return ListView.builder(
            itemCount: dersler.length,
            itemBuilder: (context, index) {
              final ders = dersler[index];

              return ListTile(
                leading: const Icon(Icons.cloud_download_outlined),
                title: Text(ders.baslik),
                subtitle: Text(ders.hafta),
              );
            },
          );
        },
      ),
    );
  }
}
```

## Mini Uygulama: API Benzeri Ders Listesi

[SCREENSHOT:b09_01_api_ders_listesi]

<!-- SCREENSHOT_META
id: b09_01_api_ders_listesi
chapter_id: chapter_01
title: "Api Ders Listesi"
kind: browser_page
url: "http://127.0.0.1:5173/__book__/async-api-json/b09_01_api_ders_listesi"
viewport: 1440x900
wait_for: "networkidle"
output_file: assets/auto/screenshots/b09_01_api_ders_listesi.png
caption: "Api Ders Listesi ekran görüntüsü."
validation_mode: capture
-->

```yaml
CODE_META:
  id: b09_kod04_api_ders_listesi
  chapter: 9
  language: dart
  framework: flutter
  runnable: true
  file: lib/main.dart
  purpose: FutureBuilder, model sınıfı ve API benzeri servisle ders listesi gösterme
  screenshot: b09_01_api_ders_listesi
```

```dart
import 'package:flutter/material.dart';

void main() {
  runApp(const ApiDersListesiUygulamasi());
}

class Ders {
  final int id;
  final String baslik;
  final String seviye;

  const Ders({required this.id, required this.baslik, required this.seviye});
}

class DersServisi {
  Future<List<Ders>> dersleriGetir() async {
    await Future.delayed(const Duration(seconds: 2));
    return const [
      Ders(id: 1, baslik: 'Flutter Temelleri', seviye: 'Başlangıç'),
      Ders(id: 2, baslik: 'Layout Sistemi', seviye: 'Orta'),
      Ders(id: 3, baslik: 'API ve JSON', seviye: 'Orta'),
    ];
  }
}

class ApiDersListesiUygulamasi extends StatelessWidget {
  const ApiDersListesiUygulamasi({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'API Ders Listesi',
      theme: ThemeData(colorSchemeSeed: Colors.blue, useMaterial3: true),
      home: const ApiDersListesiSayfasi(),
    );
  }
}

class ApiDersListesiSayfasi extends StatefulWidget {
  const ApiDersListesiSayfasi({super.key});

  @override
  State<ApiDersListesiSayfasi> createState() => _ApiDersListesiSayfasiState();
}

class _ApiDersListesiSayfasiState extends State<ApiDersListesiSayfasi> {
  final DersServisi servis = DersServisi();
  late Future<List<Ders>> dersFuture;

  @override
  void initState() {
    super.initState();
    dersFuture = servis.dersleriGetir();
  }

  Future<void> yenile() async {
    setState(() {
      dersFuture = servis.dersleriGetir();
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('API Ders Listesi')),
      body: RefreshIndicator(
        onRefresh: yenile,
        child: FutureBuilder<List<Ders>>(
          future: dersFuture,
          builder: (context, snapshot) {
            if (snapshot.connectionState == ConnectionState.waiting) {
              return const Center(child: CircularProgressIndicator());
            }

            if (snapshot.hasError) {
              return ListView(
                children: [
                  Padding(
                    padding: const EdgeInsets.all(24),
                    child: Text('Veri alınamadı: ${snapshot.error}'),
                  ),
                ],
              );
            }

            final dersler = snapshot.data ?? [];

            if (dersler.isEmpty) {
              return const Center(child: Text('Ders bulunamadı.'));
            }

            return ListView.builder(
              itemCount: dersler.length,
              itemBuilder: (context, index) {
                final ders = dersler[index];

                return Card(
                  margin: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                  child: ListTile(
                    leading: CircleAvatar(child: Text('${ders.id}')),
                    title: Text(ders.baslik),
                    subtitle: Text(ders.seviye),
                  ),
                );
              },
            );
          },
        ),
      ),
    );
  }
}
```

## Laboratuvar Görevi

“API Destekli Ders Listesi” adlı uygulama geliştiriniz. Uygulamada servis sınıfı, model sınıfı, `FutureBuilder`, yükleniyor göstergesi, hata mesajı, boş liste mesajı ve yenileme davranışı bulunmalıdır.

## Değerlendirme Rubriği

| Ölçüt | Puan | Açıklama |
|---|---:|---|
| Asenkron yapı | 20 | `Future`, `async`, `await` doğru kullanılmıştır |
| Modelleme | 15 | JSON/API verisi model sınıfıyla temsil edilmiştir |
| FutureBuilder | 20 | Yükleniyor, hata ve başarı durumları yönetilmiştir |
| Listeleme | 15 | API verisi listelenmiştir |
| Hata yönetimi | 15 | Kullanıcıya anlaşılır hata mesajı sunulmuştur |
| Kod okunabilirliği | 15 | Servis, model ve arayüz ayrımı yapılmıştır |

## Bölüm Özeti

Bu bölümde asenkron programlama, `Future`, `async`, `await`, JSON çözümleme, model sınıfı, servis sınıfı ve `FutureBuilder` kullanımı ele alındı.

## Bölüm Sonu Kontrol Listesi

- [ ] `Future` kavramını açıklayabiliyorum.
- [ ] `async` ve `await` kullanabiliyorum.
- [ ] JSON verisini `jsonDecode` ile çözümleyebiliyorum.
- [ ] Model sınıfı oluşturabiliyorum.
- [ ] `FutureBuilder` ile asenkron veri gösterebiliyorum.
- [ ] Hata ve boş liste durumlarını yönetebiliyorum.
