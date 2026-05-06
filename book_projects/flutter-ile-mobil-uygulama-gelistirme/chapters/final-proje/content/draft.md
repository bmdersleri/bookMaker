---
chapter_id: final-proje
chapter_no: 5
title: "Final Proje"
artifact_type: chapter
artifact_version: project-based
language: tr
---

# Bölüm 16 — Final Proje

## Bölümün Amacı

Bu bölümde kitap boyunca öğrenilen Flutter becerileri bütünleşik bir final proje üzerinden bir araya getirilmektedir. Final proje, öğrencinin yalnızca tekil widget örneklerini değil; model, state, form, listeleme, navigation, tema ve kalite kontrol yaklaşımını birlikte kullanmasını hedefler.

Bu bölüm sonunda öğrenci:

- Küçük ölçekli bir Flutter proje yapısı planlayabilir.
- Model sınıfı oluşturabilir.
- Form ile veri girişi alabilir.
- Liste ekranı tasarlayabilir.
- Detay ekranına navigation yapabilir.
- Basit state yönetimi uygulayabilir.
- Tema, layout ve erişilebilirlik ilkelerini dikkate alabilir.
- Projesini rubrik ölçütlerine göre değerlendirebilir.

## Final Proje Tanımı

Final proje önerisi: **Ders Takip ve Görev Yönetimi Uygulaması**

Bu uygulamada kullanıcı ders veya görev kaydı ekleyebilecek, kayıtları listeleyebilecek, detay ekranına geçebilecek ve tamamlanma durumunu değiştirebilecektir.

Temel özellikler:

- Ders/görev modeli
- Kayıt ekleme formu
- Liste ekranı
- Detay ekranı
- State yönetimi
- Navigation
- Tema kullanımı
- Boş liste durumu
- Basit değerlendirme rubriği

::: {custom-style="Dikkat Kutusu"}
**Dikkat:** Final proje, karmaşık paket kullanımından çok temel Flutter becerilerinin temiz, anlaşılır ve sürdürülebilir biçimde uygulanmasına odaklanmalıdır.
:::

## Proje Modeli

```yaml
CODE_META:
  id: b16_kod01_final_proje_model
  chapter: 16
  language: dart
  framework: flutter
  runnable: false
  file: lib/models/gorev.dart
  purpose: Final proje için görev model sınıfı
```

```dart
class Gorev {
  final String baslik;
  final String aciklama;
  final bool tamamlandi;

  const Gorev({
    required this.baslik,
    required this.aciklama,
    required this.tamamlandi,
  });

  Gorev kopyala({
    String? baslik,
    String? aciklama,
    bool? tamamlandi,
  }) {
    return Gorev(
      baslik: baslik ?? this.baslik,
      aciklama: aciklama ?? this.aciklama,
      tamamlandi: tamamlandi ?? this.tamamlandi,
    );
  }
}
```

## Bütünleşik Mini Final Proje

[SCREENSHOT:b16_01_final_proje_ders_gorev_yonetimi]

<!-- SCREENSHOT_META
id: b16_01_final_proje_ders_gorev_yonetimi
chapter_id: chapter_05
title: "Final Proje Ders Gorev Yonetimi"
kind: browser_page
url: "http://127.0.0.1:5173/__book__/final-proje/b16_01_final_proje_ders_gorev_yonetimi"
viewport: 1440x900
wait_for: "networkidle"
output_file: assets/auto/screenshots/b16_01_final_proje_ders_gorev_yonetimi.png
caption: "Final Proje Ders Gorev Yonetimi ekran görüntüsü."
validation_mode: capture
-->

```yaml
CODE_META:
  id: b16_kod02_final_proje_ders_gorev_yonetimi
  chapter: 16
  language: dart
  framework: flutter
  runnable: true
  file: lib/main.dart
  purpose: Model, form, listview, state, navigation ve tema kullanımıyla final proje
  screenshot: b16_01_final_proje_ders_gorev_yonetimi
```

```dart
import 'package:flutter/material.dart';

void main() {
  runApp(const FinalProjeUygulamasi());
}

class Gorev {
  final String baslik;
  final String aciklama;
  final bool tamamlandi;

  const Gorev({
    required this.baslik,
    required this.aciklama,
    required this.tamamlandi,
  });

  Gorev kopyala({
    String? baslik,
    String? aciklama,
    bool? tamamlandi,
  }) {
    return Gorev(
      baslik: baslik ?? this.baslik,
      aciklama: aciklama ?? this.aciklama,
      tamamlandi: tamamlandi ?? this.tamamlandi,
    );
  }
}

class FinalProjeUygulamasi extends StatelessWidget {
  const FinalProjeUygulamasi({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Final Proje',
      theme: ThemeData(
        colorSchemeSeed: Colors.indigo,
        useMaterial3: true,
      ),
      home: const GorevListesiSayfasi(),
    );
  }
}

class GorevListesiSayfasi extends StatefulWidget {
  const GorevListesiSayfasi({super.key});

  @override
  State<GorevListesiSayfasi> createState() => _GorevListesiSayfasiState();
}

class _GorevListesiSayfasiState extends State<GorevListesiSayfasi> {
  final TextEditingController baslikController = TextEditingController();
  final TextEditingController aciklamaController = TextEditingController();

  List<Gorev> gorevler = const [
    Gorev(
      baslik: 'Flutter final projesini planla',
      aciklama: 'Model, form, liste ve navigation akışını belirle.',
      tamamlandi: false,
    ),
  ];

  @override
  void dispose() {
    baslikController.dispose();
    aciklamaController.dispose();
    super.dispose();
  }

  void gorevEkle() {
    final baslik = baslikController.text.trim();
    final aciklama = aciklamaController.text.trim();

    if (baslik.isEmpty || aciklama.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Başlık ve açıklama boş olamaz.')),
      );
      return;
    }

    setState(() {
      gorevler = [
        ...gorevler,
        Gorev(
          baslik: baslik,
          aciklama: aciklama,
          tamamlandi: false,
        ),
      ];
      baslikController.clear();
      aciklamaController.clear();
    });
  }

  void durumDegistir(int index) {
    final gorev = gorevler[index];

    setState(() {
      gorevler[index] = gorev.kopyala(
        tamamlandi: !gorev.tamamlandi,
      );
    });
  }

  void detayaGit(Gorev gorev) {
    Navigator.push(
      context,
      MaterialPageRoute(
        builder: (context) => GorevDetaySayfasi(gorev: gorev),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final tamamlanan = gorevler.where((gorev) => gorev.tamamlandi).length;

    return Scaffold(
      appBar: AppBar(
        title: const Text('Ders Görev Yönetimi'),
      ),
      body: Column(
        children: [
          Card(
            margin: const EdgeInsets.all(12),
            child: ListTile(
              leading: const Icon(Icons.analytics_outlined),
              title: Text('Toplam görev: ${gorevler.length}'),
              subtitle: Text('Tamamlanan görev: $tamamlanan'),
            ),
          ),
          Padding(
            padding: const EdgeInsets.all(12),
            child: Column(
              children: [
                TextField(
                  controller: baslikController,
                  decoration: const InputDecoration(
                    labelText: 'Görev başlığı',
                    border: OutlineInputBorder(),
                  ),
                ),
                const SizedBox(height: 8),
                TextField(
                  controller: aciklamaController,
                  decoration: const InputDecoration(
                    labelText: 'Görev açıklaması',
                    border: OutlineInputBorder(),
                  ),
                ),
                const SizedBox(height: 8),
                SizedBox(
                  width: double.infinity,
                  child: ElevatedButton.icon(
                    onPressed: gorevEkle,
                    icon: const Icon(Icons.add),
                    label: const Text('Görev Ekle'),
                  ),
                ),
              ],
            ),
          ),
          Expanded(
            child: gorevler.isEmpty
                ? const Center(child: Text('Henüz görev yok.'))
                : ListView.builder(
                    itemCount: gorevler.length,
                    itemBuilder: (context, index) {
                      final gorev = gorevler[index];

                      return Card(
                        margin: const EdgeInsets.symmetric(
                          horizontal: 12,
                          vertical: 6,
                        ),
                        child: ListTile(
                          leading: Icon(
                            gorev.tamamlandi
                                ? Icons.check_circle
                                : Icons.radio_button_unchecked,
                          ),
                          title: Text(gorev.baslik),
                          subtitle: Text(gorev.aciklama),
                          trailing: Switch(
                            value: gorev.tamamlandi,
                            onChanged: (_) => durumDegistir(index),
                          ),
                          onTap: () => detayaGit(gorev),
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

class GorevDetaySayfasi extends StatelessWidget {
  final Gorev gorev;

  const GorevDetaySayfasi({
    super.key,
    required this.gorev,
  });

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Görev Detayı'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Card(
          child: ListTile(
            leading: Icon(
              gorev.tamamlandi
                  ? Icons.check_circle
                  : Icons.pending_actions,
            ),
            title: Text(gorev.baslik),
            subtitle: Text(gorev.aciklama),
          ),
        ),
      ),
    );
  }
}
```

## Proje Klasör Önerisi

```text
lib/
├── main.dart
├── models/
│   └── gorev.dart
├── screens/
│   ├── gorev_listesi_sayfasi.dart
│   └── gorev_detay_sayfasi.dart
├── widgets/
│   ├── gorev_karti.dart
│   └── ozet_karti.dart
└── services/
    └── gorev_servisi.dart
```

## Teslim Beklentileri

Öğrenci final proje tesliminde şu çıktıları sunmalıdır:

- Çalışan Flutter projesi
- Kısa proje açıklaması
- Ekran görüntüleri
- Kullanılan temel widget listesi
- Test edilen senaryolar
- Bilinen eksikler
- Geliştirme önerileri

## Laboratuvar Görevi

Final proje uygulamasını kendi senaryonuza göre genişletiniz. En az bir form, bir liste, bir detay ekranı, navigation, state yönetimi, tema ve boş durum mesajı bulunmalıdır.

## Değerlendirme Rubriği

| Ölçüt | Puan | Açıklama |
|---|---:|---|
| Proje bütünlüğü | 20 | Uygulama anlamlı bir senaryo etrafında tamamlanmıştır |
| Model kullanımı | 15 | Veri model sınıfıyla temsil edilmiştir |
| Form yapısı | 15 | Kullanıcıdan veri alınabilmektedir |
| Listeleme | 15 | Veriler `ListView.builder` ile gösterilmiştir |
| Navigation | 15 | Liste-detay geçişi çalışmaktadır |
| State yönetimi | 10 | Veri değişimleri doğru yönetilmiştir |
| Kod okunabilirliği | 10 | Kod düzenli ve anlaşılırdır |

## Bölüm Özeti

Bu bölümde kitap boyunca öğrenilen model, form, listview, navigation, state, tema ve proje teslim becerileri final proje çatısı altında birleştirildi.

## Bölüm Sonu Kontrol Listesi

- [ ] Final proje senaryosu belirleyebiliyorum.
- [ ] Model sınıfı oluşturabiliyorum.
- [ ] Form ile veri girişi alabiliyorum.
- [ ] Liste ve detay ekranı kurabiliyorum.
- [ ] Navigation kullanabiliyorum.
- [ ] Projemi rubrik ölçütlerine göre değerlendirebiliyorum.
