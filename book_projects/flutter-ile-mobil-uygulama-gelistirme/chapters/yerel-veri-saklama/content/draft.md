# Bölüm 10 — Yerel Veri Saklama

## Bölümün Amacı

Bu bölümde Flutter uygulamalarında yerel veri saklama mantığı ele alınmaktadır. Birçok mobil uygulama, kullanıcı tercihlerini, basit ayarları, son kullanılan değerleri veya küçük veri kümelerini cihaz üzerinde saklamak zorundadır. İnternet bağlantısı olmasa bile bazı bilgilerin korunması kullanıcı deneyimi açısından önemlidir.

Bu bölüm sonunda öğrenci geçici state ile kalıcı veri arasındaki farkı ayırt edebilir, JSON tabanlı küçük veri saklama yaklaşımını açıklayabilir ve yerel veri saklama için servis sınıfı tasarlayabilir.

## 10.1. Neden Yerel Veri Saklarız?

Yerel veri saklama; tema tercihi, son girilen kullanıcı adı, dil seçimi, taslak notlar, offline küçük kayıtlar ve API cache verileri için kullanılabilir.

::: {custom-style="Dikkat Kutusu"}
**Dikkat:** Şifre, token veya kişisel hassas veriler için güvenli saklama yaklaşımları ayrıca ele alınmalıdır.
:::

## 10.2. SharedPreferences Mantığı

Küçük anahtar-değer verileri için Flutter ekosisteminde sık kullanılan paketlerden biri `shared_preferences` paketidir.

```yaml
dependencies:
  shared_preferences: ^2.2.0
```

Bu bölümde harici bağımlılığı azaltmak için bazı örneklerde local storage servis mantığı simüle edilmiştir.

## 10.3. Basit Saklama Servisi

```yaml
CODE_META:
  id: b10_kod01_bellek_tabanli_ayar_servisi
  chapter: 10
  language: dart
  framework: flutter
  runnable: true
  file: lib/main.dart
  purpose: Yerel veri saklama servis mantığını simülasyonla gösterme
```

```dart
import 'package:flutter/material.dart';

void main() {
  runApp(const AyarSaklamaUygulamasi());
}

class AyarServisi {
  String _kullaniciAdi = '';

  Future<void> kullaniciAdiKaydet(String ad) async {
    await Future.delayed(const Duration(milliseconds: 300));
    _kullaniciAdi = ad;
  }

  Future<String> kullaniciAdiOku() async {
    await Future.delayed(const Duration(milliseconds: 300));
    return _kullaniciAdi;
  }
}

class AyarSaklamaUygulamasi extends StatelessWidget {
  const AyarSaklamaUygulamasi({super.key});

  @override
  Widget build(BuildContext context) {
    return const MaterialApp(home: AyarSaklamaSayfasi());
  }
}

class AyarSaklamaSayfasi extends StatefulWidget {
  const AyarSaklamaSayfasi({super.key});

  @override
  State<AyarSaklamaSayfasi> createState() => _AyarSaklamaSayfasiState();
}

class _AyarSaklamaSayfasiState extends State<AyarSaklamaSayfasi> {
  final AyarServisi servis = AyarServisi();
  final TextEditingController adController = TextEditingController();
  String kayitliAd = 'Henüz kayıt yok.';

  @override
  void dispose() {
    adController.dispose();
    super.dispose();
  }

  Future<void> kaydet() async {
    await servis.kullaniciAdiKaydet(adController.text.trim());
    final okunan = await servis.kullaniciAdiOku();

    setState(() {
      kayitliAd = okunan.isEmpty ? 'Boş kayıt.' : okunan;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Yerel Veri Saklama')),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            TextField(
              controller: adController,
              decoration: const InputDecoration(
                labelText: 'Kullanıcı adı',
                border: OutlineInputBorder(),
              ),
            ),
            const SizedBox(height: 16),
            ElevatedButton(
              onPressed: kaydet,
              child: const Text('Kaydet ve Oku'),
            ),
            const SizedBox(height: 20),
            Text('Kayıtlı değer: $kayitliAd'),
          ],
        ),
      ),
    );
  }
}
```

## 10.4. JSON Olarak Saklama Mantığı

```yaml
CODE_META:
  id: b10_kod02_model_json_saklama
  chapter: 10
  language: dart
  framework: flutter
  runnable: true
  file: lib/main.dart
  purpose: Model nesnesini JSON'a dönüştürme ve geri okuma
```

```dart
import 'dart:convert';
import 'package:flutter/material.dart';

void main() {
  runApp(const JsonSaklamaUygulamasi());
}

class KullaniciAyari {
  final String ad;
  final bool koyuTema;

  const KullaniciAyari({required this.ad, required this.koyuTema});

  Map<String, dynamic> toJson() {
    return {'ad': ad, 'koyuTema': koyuTema};
  }

  factory KullaniciAyari.fromJson(Map<String, dynamic> json) {
    return KullaniciAyari(
      ad: json['ad'] as String,
      koyuTema: json['koyuTema'] as bool,
    );
  }
}

class JsonSaklamaUygulamasi extends StatelessWidget {
  const JsonSaklamaUygulamasi({super.key});

  @override
  Widget build(BuildContext context) {
    const ayar = KullaniciAyari(ad: 'Bahar', koyuTema: true);
    final jsonMetni = jsonEncode(ayar.toJson());
    final okunan = KullaniciAyari.fromJson(jsonDecode(jsonMetni));

    return MaterialApp(
      home: Scaffold(
        appBar: AppBar(title: const Text('JSON Saklama')),
        body: Center(
          child: Text('Okunan ayar: ${okunan.ad}, koyu tema: ${okunan.koyuTema}'),
        ),
      ),
    );
  }
}
```

## 10.5. Dosya ve Cache Mantığı

Dosya tabanlı saklama için gerçek projelerde `path_provider` gibi paketler gerekebilir. Cache verileri ise kalıcı veri kadar güvenilir kabul edilmemelidir. Cache, performansı artırmak için geçici olarak saklanan veridir.

## 10.6. Mini Uygulama: Yerel Not Defteri Simülasyonu

[SCREENSHOT:b10_01_yerel_not_defteri]

```yaml
CODE_META:
  id: b10_kod03_yerel_not_defteri
  chapter: 10
  language: dart
  framework: flutter
  runnable: true
  file: lib/main.dart
  purpose: Yerel veri saklama mantığını not listesi üzerinden simüle etme
  screenshot: b10_01_yerel_not_defteri
```

```dart
import 'package:flutter/material.dart';

void main() {
  runApp(const YerelNotUygulamasi());
}

class NotKaydi {
  final String baslik;
  final String icerik;

  const NotKaydi({required this.baslik, required this.icerik});
}

class NotServisi {
  final List<NotKaydi> _notlar = [];

  Future<List<NotKaydi>> notlariOku() async {
    await Future.delayed(const Duration(milliseconds: 300));
    return List.unmodifiable(_notlar);
  }

  Future<void> notEkle(NotKaydi not) async {
    await Future.delayed(const Duration(milliseconds: 300));
    _notlar.add(not);
  }
}

class YerelNotUygulamasi extends StatefulWidget {
  const YerelNotUygulamasi({super.key});

  @override
  State<YerelNotUygulamasi> createState() => _YerelNotUygulamasiState();
}

class _YerelNotUygulamasiState extends State<YerelNotUygulamasi> {
  final NotServisi servis = NotServisi();
  final TextEditingController baslikController = TextEditingController();
  final TextEditingController icerikController = TextEditingController();
  List<NotKaydi> notlar = [];

  @override
  void dispose() {
    baslikController.dispose();
    icerikController.dispose();
    super.dispose();
  }

  Future<void> notEkle() async {
    final baslik = baslikController.text.trim();
    final icerik = icerikController.text.trim();

    if (baslik.isEmpty || icerik.isEmpty) {
      return;
    }

    await servis.notEkle(NotKaydi(baslik: baslik, icerik: icerik));
    final okunanNotlar = await servis.notlariOku();

    setState(() {
      notlar = okunanNotlar;
      baslikController.clear();
      icerikController.clear();
    });
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Yerel Not Defteri',
      home: Scaffold(
        appBar: AppBar(title: const Text('Yerel Not Defteri')),
        body: Column(
          children: [
            Padding(
              padding: const EdgeInsets.all(12),
              child: Column(
                children: [
                  TextField(
                    controller: baslikController,
                    decoration: const InputDecoration(
                      labelText: 'Başlık',
                      border: OutlineInputBorder(),
                    ),
                  ),
                  const SizedBox(height: 8),
                  TextField(
                    controller: icerikController,
                    decoration: const InputDecoration(
                      labelText: 'İçerik',
                      border: OutlineInputBorder(),
                    ),
                  ),
                  const SizedBox(height: 8),
                  ElevatedButton(
                    onPressed: notEkle,
                    child: const Text('Not Ekle'),
                  ),
                ],
              ),
            ),
            Expanded(
              child: notlar.isEmpty
                  ? const Center(child: Text('Henüz not yok.'))
                  : ListView.builder(
                      itemCount: notlar.length,
                      itemBuilder: (context, index) {
                        final not = notlar[index];

                        return Card(
                          margin: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                          child: ListTile(
                            title: Text(not.baslik),
                            subtitle: Text(not.icerik),
                          ),
                        );
                      },
                    ),
            ),
          ],
        ),
      ),
    );
  }
}
```

## 10.7. Laboratuvar Görevi

“Ders Çalışma Notları” adlı uygulama geliştiriniz. Kullanıcı başlık ve içerik girebilmeli, notlar listelenmeli, boş alan girilirse kayıt yapılmamalı, notlar model sınıfı ile temsil edilmeli ve servis sınıfı üzerinden yönetilmelidir.

## 10.8. Değerlendirme Rubriği

| Ölçüt | Puan | Açıklama |
|---|---:|---|
| Model sınıfı | 15 | Veri anlamlı modelle temsil edilmiştir |
| Servis yapısı | 20 | Saklama işlemi ayrı sınıfta yönetilmiştir |
| JSON mantığı | 15 | `toJson`/`fromJson` yaklaşımı anlaşılmıştır |
| Listeleme | 15 | Kayıtlar listelenmiştir |
| Form etkileşimi | 15 | Kullanıcıdan veri alınmıştır |
| Kod okunabilirliği | 20 | Sınıflar ve metotlar düzenlidir |

## 10.9. Bölüm Özeti

Bu bölümde yerel veri saklama ihtiyacı, geçici state ile kalıcı veri farkı, SharedPreferences mantığı, JSON dönüşümü, dosya tabanlı saklama, local storage ve cache kavramları ele alındı.

## Bölüm Sonu Kontrol Listesi

- [ ] Kalıcı veri ile geçici state farkını açıklayabiliyorum.
- [ ] Yerel veri saklama ihtiyacını yorumlayabiliyorum.
- [ ] JSON dönüşümü yapabiliyorum.
- [ ] Saklama servis sınıfı tasarlayabiliyorum.
- [ ] Cache ve kalıcı veri farkını yorumlayabiliyorum.
