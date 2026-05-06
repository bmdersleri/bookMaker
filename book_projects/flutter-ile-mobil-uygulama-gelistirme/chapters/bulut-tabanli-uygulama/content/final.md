# Bölüm 13 — Bulut Tabanlı Uygulama Mantığı

## Bölümün Amacı

Bu bölümde Flutter uygulamalarında bulut tabanlı çalışma mantığı ele alınmaktadır. Gerçek mobil uygulamalar çoğu zaman yalnızca cihaz içindeki verilerle çalışmaz; kullanıcı kimliği, merkezi veritabanı, dosya depolama, bildirimler ve analiz gibi servislerle bütünleşir. Bu servisler çoğunlukla bulut tabanlı backend yapıları üzerinden sağlanır.

Bu bölüm sonunda öğrenci:

- Bulut tabanlı uygulama kavramını açıklayabilir.
- Backend, API, authentication ve database kavramlarını ayırt edebilir.
- Flutter uygulamasında servis katmanının neden gerekli olduğunu yorumlayabilir.
- Firebase benzeri BaaS yaklaşımlarının temel mantığını açıklayabilir.
- Bulut servislerini doğrudan widget içine yazmak yerine servis sınıfıyla temsil edebilir.
- Asenkron veri alma ve modelleme mantığını bulut senaryosunda kullanabilir.

## 13.1. Bulut Tabanlı Uygulama Nedir?

Bulut tabanlı uygulama, verisini ve bazı işlevlerini internet üzerindeki servislerle paylaşan uygulamadır. Kullanıcı bir hesaba giriş yapabilir, veriler farklı cihazlarda eşitlenebilir ve uygulama merkezi bir veritabanıyla çalışabilir.

Örnek bulut servisleri:

- Authentication
- Realtime database
- Cloud database
- File storage
- Push notification
- Analytics
- Remote config

::: {custom-style="Dikkat Kutusu"}
**Dikkat:** Bulut servisleri uygulamayı güçlendirir; ancak gizlilik, güvenlik, internet bağımlılığı ve maliyet gibi başlıklar mutlaka düşünülmelidir.
:::

## 13.2. Backend ve BaaS Yaklaşımı

Backend, uygulamanın sunucu tarafında çalışan veri ve iş mantığı katmanıdır. BaaS yani Backend as a Service yaklaşımı ise hazır bulut servisleriyle backend ihtiyacının önemli bir kısmını yönetmeyi sağlar. Firebase bu yaklaşımın en bilinen örneklerinden biridir.

Bu kitapta doğrudan dış servis bağlantısı yerine, bulut servis mantığını öğretmek için simülasyon tabanlı örnekler kullanılacaktır. Böylece örnekler kopyala-çalıştır niteliğini korur.

## 13.3. Kullanıcı Modeli ve Auth Mantığı

```yaml
CODE_META:
  id: b13_kod01_auth_servis_simulasyonu
  chapter: 13
  language: dart
  framework: flutter
  runnable: true
  file: lib/main.dart
  purpose: Bulut authentication mantığını servis sınıfıyla simüle etme
```

```dart
import 'package:flutter/material.dart';

void main() {
  runApp(const AuthSimulasyonUygulamasi());
}

class Kullanici {
  final String eposta;
  final String adSoyad;

  const Kullanici({
    required this.eposta,
    required this.adSoyad,
  });
}

class AuthServisi {
  Future<Kullanici> girisYap({
    required String eposta,
    required String sifre,
  }) async {
    await Future.delayed(const Duration(seconds: 1));

    if (!eposta.contains('@') || sifre.length < 4) {
      throw Exception('Giriş bilgileri geçersiz.');
    }

    return Kullanici(
      eposta: eposta,
      adSoyad: 'Flutter Öğrencisi',
    );
  }
}

class AuthSimulasyonUygulamasi extends StatelessWidget {
  const AuthSimulasyonUygulamasi({super.key});

  @override
  Widget build(BuildContext context) {
    return const MaterialApp(home: AuthSayfasi());
  }
}

class AuthSayfasi extends StatefulWidget {
  const AuthSayfasi({super.key});

  @override
  State<AuthSayfasi> createState() => _AuthSayfasiState();
}

class _AuthSayfasiState extends State<AuthSayfasi> {
  final AuthServisi servis = AuthServisi();
  final TextEditingController epostaController = TextEditingController();
  final TextEditingController sifreController = TextEditingController();

  String mesaj = 'Henüz giriş yapılmadı.';
  bool yukleniyor = false;

  @override
  void dispose() {
    epostaController.dispose();
    sifreController.dispose();
    super.dispose();
  }

  Future<void> girisYap() async {
    setState(() {
      yukleniyor = true;
      mesaj = 'Giriş deneniyor...';
    });

    try {
      final kullanici = await servis.girisYap(
        eposta: epostaController.text.trim(),
        sifre: sifreController.text,
      );

      setState(() {
        mesaj = 'Hoş geldiniz: ${kullanici.adSoyad}';
      });
    } catch (hata) {
      setState(() {
        mesaj = 'Hata: $hata';
      });
    } finally {
      setState(() {
        yukleniyor = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Bulut Auth Simülasyonu'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            TextField(
              controller: epostaController,
              decoration: const InputDecoration(
                labelText: 'E-posta',
                border: OutlineInputBorder(),
              ),
            ),
            const SizedBox(height: 12),
            TextField(
              controller: sifreController,
              decoration: const InputDecoration(
                labelText: 'Şifre',
                border: OutlineInputBorder(),
              ),
              obscureText: true,
            ),
            const SizedBox(height: 16),
            ElevatedButton(
              onPressed: yukleniyor ? null : girisYap,
              child: const Text('Giriş Yap'),
            ),
            const SizedBox(height: 20),
            if (yukleniyor) const CircularProgressIndicator(),
            Text(mesaj),
          ],
        ),
      ),
    );
  }
}
```

## 13.4. Bulut Veritabanı Servisi Mantığı

```yaml
CODE_META:
  id: b13_kod02_cloud_database_simulasyonu
  chapter: 13
  language: dart
  framework: flutter
  runnable: true
  file: lib/main.dart
  purpose: Bulut database mantığını model ve servis sınıfıyla simüle etme
```

```dart
import 'package:flutter/material.dart';

void main() {
  runApp(const BulutVeriUygulamasi());
}

class DersKaydi {
  final String id;
  final String baslik;
  final bool tamamlandi;

  const DersKaydi({
    required this.id,
    required this.baslik,
    required this.tamamlandi,
  });
}

class BulutVeriServisi {
  final List<DersKaydi> _kayitlar = [
    const DersKaydi(id: '1', baslik: 'Flutter Giriş', tamamlandi: true),
    const DersKaydi(id: '2', baslik: 'Bulut Tabanlı Uygulama', tamamlandi: false),
  ];

  Future<List<DersKaydi>> dersleriGetir() async {
    await Future.delayed(const Duration(seconds: 1));
    return List.unmodifiable(_kayitlar);
  }

  Future<void> dersEkle(String baslik) async {
    await Future.delayed(const Duration(milliseconds: 500));
    _kayitlar.add(
      DersKaydi(
        id: DateTime.now().millisecondsSinceEpoch.toString(),
        baslik: baslik,
        tamamlandi: false,
      ),
    );
  }
}

class BulutVeriUygulamasi extends StatefulWidget {
  const BulutVeriUygulamasi({super.key});

  @override
  State<BulutVeriUygulamasi> createState() => _BulutVeriUygulamasiState();
}

class _BulutVeriUygulamasiState extends State<BulutVeriUygulamasi> {
  final BulutVeriServisi servis = BulutVeriServisi();
  late Future<List<DersKaydi>> dersFuture;

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

  Future<void> dersEkle() async {
    await servis.dersEkle('Yeni bulut kaydı');
    await yenile();
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Bulut Veri',
      home: Scaffold(
        appBar: AppBar(
          title: const Text('Bulut Database Simülasyonu'),
          actions: [
            IconButton(
              onPressed: dersEkle,
              icon: const Icon(Icons.add),
            ),
          ],
        ),
        body: FutureBuilder<List<DersKaydi>>(
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
                  leading: Icon(
                    ders.tamamlandi
                        ? Icons.cloud_done
                        : Icons.cloud_queue,
                  ),
                  title: Text(ders.baslik),
                  subtitle: Text('Kayıt ID: ${ders.id}'),
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

## 13.5. Mini Uygulama: Bulut Ders Paneli

[SCREENSHOT:b13_01_bulut_ders_paneli]

```yaml
CODE_META:
  id: b13_kod03_bulut_ders_paneli
  chapter: 13
  language: dart
  framework: flutter
  runnable: true
  file: lib/main.dart
  purpose: Auth, cloud database, model, service ve async akışını bir arada gösterme
  screenshot: b13_01_bulut_ders_paneli
```

```dart
import 'package:flutter/material.dart';

void main() {
  runApp(const BulutDersPaneliUygulamasi());
}

class BulutDersPaneliUygulamasi extends StatelessWidget {
  const BulutDersPaneliUygulamasi({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Bulut Ders Paneli',
      theme: ThemeData(colorSchemeSeed: Colors.blue, useMaterial3: true),
      home: const BulutDersPaneli(),
    );
  }
}

class BulutDersPaneli extends StatelessWidget {
  const BulutDersPaneli({super.key});

  @override
  Widget build(BuildContext context) {
    final kartlar = const [
      _PanelKarti(ikon: Icons.login, baslik: 'Auth', deger: 'Aktif'),
      _PanelKarti(ikon: Icons.cloud, baslik: 'Cloud', deger: 'Simülasyon'),
      _PanelKarti(ikon: Icons.storage, baslik: 'Database', deger: 'Ders kayıtları'),
      _PanelKarti(ikon: Icons.security, baslik: 'Güvenlik', deger: 'Kurallar gerekli'),
    ];

    return Scaffold(
      appBar: AppBar(title: const Text('Bulut Ders Paneli')),
      body: GridView.count(
        padding: const EdgeInsets.all(16),
        crossAxisCount: 2,
        crossAxisSpacing: 12,
        mainAxisSpacing: 12,
        children: kartlar,
      ),
    );
  }
}

class _PanelKarti extends StatelessWidget {
  final IconData ikon;
  final String baslik;
  final String deger;

  const _PanelKarti({
    required this.ikon,
    required this.baslik,
    required this.deger,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      child: Center(
        child: ListTile(
          leading: Icon(ikon),
          title: Text(baslik),
          subtitle: Text(deger),
        ),
      ),
    );
  }
}
```

## 13.6. Güvenlik ve Veri Kuralları

Bulut servislerinde authentication yeterli değildir. Kullanıcıların hangi verilere erişebileceği kurallarla sınırlandırılmalıdır. Database rules, API authorization ve güvenli veri modeli kritik başlıklardır.

## 13.7. Laboratuvar Görevi

“Bulut Ders Kayıt Paneli” adlı uygulama geliştiriniz. Auth simülasyonu, cloud database servis simülasyonu, model sınıfı, asenkron veri çekme ve listeleme ekranı bulunmalıdır.

## 13.8. Değerlendirme Rubriği

| Ölçüt | Puan | Açıklama |
|---|---:|---|
| Bulut kavramları | 20 | Cloud, backend, auth ve database doğru açıklanmıştır |
| Servis sınıfı | 20 | Bulut işlemleri widget dışına alınmıştır |
| Asenkron akış | 20 | `Future`, `async`, `await` doğru kullanılmıştır |
| Modelleme | 15 | Veri model sınıfıyla temsil edilmiştir |
| Arayüz | 15 | Bulut verisi listelenmiştir |
| Güvenlik farkındalığı | 10 | Yetki ve veri kuralları ele alınmıştır |

## 13.9. Bölüm Özeti

Bu bölümde bulut tabanlı uygulama, backend, BaaS, Firebase mantığı, auth, cloud database, servis sınıfı ve güvenlik farkındalığı ele alındı.

## Bölüm Sonu Kontrol Listesi

- [ ] Bulut tabanlı uygulama kavramını açıklayabiliyorum.
- [ ] Auth ve database farkını biliyorum.
- [ ] Servis sınıfı ile bulut işlemi temsil edebiliyorum.
- [ ] Asenkron veri çekme akışını kurabiliyorum.
- [ ] Bulut güvenliği için temel riskleri yorumlayabiliyorum.
