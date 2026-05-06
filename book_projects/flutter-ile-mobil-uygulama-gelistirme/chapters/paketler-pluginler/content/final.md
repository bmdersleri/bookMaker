# Bölüm 12 — Paketler ve Plugin Kullanımı

## Bölümün Amacı

Bu bölümde Flutter ekosisteminde paket ve plugin kullanımı ele alınmaktadır. Gerçek uygulamalarda her işlevi sıfırdan yazmak yerine güvenilir paketlerden yararlanmak gerekir. HTTP isteği göndermek, yerel veri saklamak, kamera kullanmak, konum almak, ikon paketi eklemek veya grafik çizmek gibi birçok işlev paketler aracılığıyla sağlanır.

## 12.1. Package ve Plugin

Paket, Flutter veya Dart projelerine eklenebilen yeniden kullanılabilir kod birimidir. Plugin ise genellikle platforma özgü işlevlere erişim sağlayan pakettir. Kamera, konum, dosya sistemi, bildirimler ve sensörler gibi cihaz özelliklerine erişmek için plugin kullanılabilir.

| Yapı | Açıklama | Örnek |
|---|---|---|
| Package | Dart/Flutter kodu sağlar | Yardımcı UI bileşeni |
| Plugin | Platform API’lerine erişebilir | Kamera, konum, dosya |

::: {custom-style="Dikkat Kutusu"}
**Dikkat:** Her plugin platform permission veya ek yapılandırma gerektirebilir. Sadece dependency eklemek çoğu zaman yeterli olmayabilir.
:::

## 12.2. `pub.dev` Üzerinden Paket Seçimi

Paket seçerken güncellik, Flutter sürümüyle uyumluluk, lisans, dokümantasyon, örnek kod, bakım durumu, platform desteği ve güvenilirlik incelenmelidir.

## 12.3. `pubspec.yaml` Dosyasına Dependency Ekleme

```yaml
dependencies:
  flutter:
    sdk: flutter
  http: ^1.2.0
```

Paket eklendikten sonra şu komut çalıştırılır:

```bash
flutter pub get
```

## 12.4. Paket Import Etme

```dart
import 'package:http/http.dart' as http;
```

Bu kullanımda `as http`, isim çakışmalarını azaltmak ve kodun okunabilirliğini artırmak için tercih edilir.

## 12.5. Harici Paket Olmadan Paket Mantığını Simüle Etme

```yaml
CODE_META:
  id: b12_kod01_paket_mantigi_servis
  chapter: 12
  language: dart
  framework: flutter
  runnable: true
  file: lib/main.dart
  purpose: Paket kullanım mantığını servis sınıfıyla simüle etme
```

```dart
import 'package:flutter/material.dart';

void main() {
  runApp(const PaketMantigiUygulamasi());
}

class MetinAraci {
  String baslikBicimlendir(String metin) {
    final temiz = metin.trim();

    if (temiz.isEmpty) {
      return 'Başlıksız';
    }

    return temiz.toUpperCase();
  }
}

class PaketMantigiUygulamasi extends StatelessWidget {
  const PaketMantigiUygulamasi({super.key});

  @override
  Widget build(BuildContext context) {
    final arac = MetinAraci();
    final sonuc = arac.baslikBicimlendir(' flutter paketleri ');

    return MaterialApp(
      home: Scaffold(
        appBar: AppBar(title: const Text('Paket Mantığı')),
        body: Center(
          child: Text(sonuc),
        ),
      ),
    );
  }
}
```

## 12.6. HTTP Paketi Kullanım Şeması

```yaml
CODE_META:
  id: b12_kod02_http_paket_kullanim_semasi
  chapter: 12
  language: dart
  framework: flutter
  runnable: false
  file: lib/api_service.dart
  purpose: http paketiyle GET isteği mantığını gösterme
```

```dart
import 'dart:convert';
import 'package:http/http.dart' as http;

class ApiServisi {
  Future<List<dynamic>> verileriGetir() async {
    final response = await http.get(
      Uri.parse('https://example.com/api/items'),
    );

    if (response.statusCode != 200) {
      throw Exception('API isteği başarısız oldu.');
    }

    return jsonDecode(response.body) as List<dynamic>;
  }
}
```

## 12.7. Platform İzinleri ve Version Yönetimi

Bazı pluginler Android veya iOS tarafında izin gerektirir. Android tarafında izinler çoğunlukla `AndroidManifest.xml`, iOS tarafında ise `Info.plist` içinde tanımlanır.

Paket version yönetimi yapılırken changelog okunmalı, breaking changes kontrol edilmeli ve testler çalıştırılmalıdır.

## 12.8. Mini Uygulama: Paket Bilgi Kartları

[SCREENSHOT:b12_01_paket_bilgi_kartlari]

```yaml
CODE_META:
  id: b12_kod03_paket_bilgi_kartlari
  chapter: 12
  language: dart
  framework: flutter
  runnable: true
  file: lib/main.dart
  purpose: Paket seçimi ölçütlerini kartlar halinde gösterme
  screenshot: b12_01_paket_bilgi_kartlari
```

```dart
import 'package:flutter/material.dart';

void main() {
  runApp(const PaketBilgiUygulamasi());
}

class PaketKriteri {
  final String baslik;
  final String aciklama;
  final IconData ikon;

  const PaketKriteri({
    required this.baslik,
    required this.aciklama,
    required this.ikon,
  });
}

class PaketBilgiUygulamasi extends StatelessWidget {
  const PaketBilgiUygulamasi({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Paket Bilgi Kartları',
      theme: ThemeData(colorSchemeSeed: Colors.orange, useMaterial3: true),
      home: const PaketBilgiSayfasi(),
    );
  }
}

class PaketBilgiSayfasi extends StatelessWidget {
  const PaketBilgiSayfasi({super.key});

  @override
  Widget build(BuildContext context) {
    final kriterler = const [
      PaketKriteri(
        baslik: 'Güncellik',
        aciklama: 'Paket düzenli bakım alıyor mu?',
        ikon: Icons.update,
      ),
      PaketKriteri(
        baslik: 'Dokümantasyon',
        aciklama: 'Kullanım örnekleri yeterli mi?',
        ikon: Icons.description_outlined,
      ),
      PaketKriteri(
        baslik: 'Platform Desteği',
        aciklama: 'Android, iOS, web ihtiyaçlarını karşılıyor mu?',
        ikon: Icons.devices,
      ),
      PaketKriteri(
        baslik: 'Lisans',
        aciklama: 'Proje için lisans uygun mu?',
        ikon: Icons.verified_user_outlined,
      ),
    ];

    return Scaffold(
      appBar: AppBar(title: const Text('Paket Seçim Kriterleri')),
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

## 12.9. Laboratuvar Görevi

“Paket Değerlendirme Paneli” adlı uygulama geliştiriniz. Öğrenci en az beş package/plugin kriterini kartlar halinde göstermeli; her kartta başlık, açıklama ve ikon bulunmalıdır. Ayrıca `pubspec.yaml`, dependencies, import, version, permission ve `pub.dev` seçimi kavramları açıklanmalıdır.

## 12.10. Değerlendirme Rubriği

| Ölçüt | Puan | Açıklama |
|---|---:|---|
| Paket/plugin ayrımı | 20 | Kavramlar doğru açıklanmıştır |
| pubspec mantığı | 15 | Dependency ekleme süreci anlaşılmıştır |
| Paket seçim kriterleri | 20 | Güncellik, lisans, dokümantasyon gibi ölçütler ele alınmıştır |
| Mini uygulama | 20 | Paket kriterleri kartlarla gösterilmiştir |
| Platform farkındalığı | 10 | Permission ve platform yapılandırması düşünülmüştür |
| Kod okunabilirliği | 15 | Model ve listeleme yapısı düzenlidir |

## 12.11. Bölüm Özeti

Bu bölümde Flutter package ve plugin kavramları, `pub.dev`, `pubspec.yaml`, dependencies, import kullanımı, platform permission, version yönetimi ve paket seçimi kriterleri ele alındı.

## Bölüm Sonu Kontrol Listesi

- [ ] Package ve plugin farkını açıklayabiliyorum.
- [ ] `pubspec.yaml` dosyasına dependency ekleyebiliyorum.
- [ ] Paket seçim kriterlerini yorumlayabiliyorum.
- [ ] Platform izinleri konusunda temel farkındalığa sahibim.
- [ ] Sürüm yönetimi ve bakım risklerini değerlendirebiliyorum.
