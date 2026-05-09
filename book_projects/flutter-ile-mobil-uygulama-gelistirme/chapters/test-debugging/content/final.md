---
chapter_id: test-debugging
chapter_no: 14
title: "Test ve Debugging"
artifact_type: chapter
artifact_version: project-based
language: tr
---

# Bölüm 14 — Test ve Debugging

## Bölümün Amacı

Bu bölümde Flutter uygulamalarında hata ayıklama, debug etme ve test yazma temelleri ele alınmaktadır. Bir uygulamanın yalnızca çalışması yeterli değildir; beklenen davranışı güvenilir biçimde sürdürmesi gerekir. Test ve debugging, yazılım kalitesinin temel parçalarıdır.

Bu bölüm sonunda öğrenci:

- Debugging kavramını açıklayabilir.
- `debugPrint`, breakpoint ve Flutter DevTools mantığını yorumlayabilir.
- Unit test ve widget test farkını açıklayabilir.
- Basit bir fonksiyon için unit test yazabilir.
- Basit bir widget için widget test mantığını kavrayabilir.
- Test edilebilir kod yazmanın önemini açıklayabilir.

## Debugging Nedir?

Debugging, uygulamadaki hataları bulma, nedenlerini anlama ve düzeltme sürecidir. Flutter’da debugging için konsol çıktıları, breakpoint, inspector, hot reload, hot restart ve DevTools gibi araçlar kullanılabilir.

::: {custom-style="Dikkat Kutusu"}
**Dikkat:** Debugging yalnızca hata çıktısını okumak değildir. Hatanın hangi veri, hangi state ve hangi kullanıcı akışıyla oluştuğunu sistematik olarak incelemek gerekir.
:::

## `debugPrint` Kullanımı

```yaml
CODE_META:
  id: b14_kod01_debugprint
  chapter: 14
  language: dart
  framework: flutter
  runnable: true
  file: lib/main.dart
  purpose: debugPrint ile basit hata ayıklama çıktısı üretme
```

```dart
import 'package:flutter/material.dart';

void main() {
  runApp(const DebugPrintUygulamasi());
}

class DebugPrintUygulamasi extends StatelessWidget {
  const DebugPrintUygulamasi({super.key});

  @override
  Widget build(BuildContext context) {
    return const MaterialApp(home: DebugPrintSayfasi());
  }
}

class DebugPrintSayfasi extends StatefulWidget {
  const DebugPrintSayfasi({super.key});

  @override
  State<DebugPrintSayfasi> createState() => _DebugPrintSayfasiState();
}

class _DebugPrintSayfasiState extends State<DebugPrintSayfasi> {
  int sayac = 0;

  void artir() {
    setState(() {
      sayac++;
    });

    debugPrint('Sayaç değeri güncellendi: $sayac');
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('debugPrint'),
      ),
      body: Center(
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Text('Sayaç: $sayac'),
            const SizedBox(height: 12),
            ElevatedButton(
              onPressed: artir,
              child: const Text('Artır'),
            ),
          ],
        ),
      ),
    );
  }
}
```

## Test Edilebilir Kod Yazmak

Test yazmayı kolaylaştırmak için iş mantığı mümkün olduğunca widget kodundan ayrılmalıdır.

```yaml
CODE_META:
  id: b14_kod02_test_edilebilir_sinif
  chapter: 14
  language: dart
  framework: flutter
  runnable: true
  file: lib/main.dart
  purpose: Test edilebilir basit iş mantığı sınıfı oluşturma
```

```dart
import 'package:flutter/material.dart';

void main() {
  final hesaplayici = PuanHesaplayici();
  runApp(PuanUygulamasi(sonuc: hesaplayici.harfNotu(85)));
}

class PuanHesaplayici {
  String harfNotu(int puan) {
    if (puan >= 90) {
      return 'AA';
    }

    if (puan >= 80) {
      return 'BA';
    }

    if (puan >= 70) {
      return 'BB';
    }

    return 'Geliştirilmeli';
  }
}

class PuanUygulamasi extends StatelessWidget {
  final String sonuc;

  const PuanUygulamasi({
    super.key,
    required this.sonuc,
  });

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: Scaffold(
        body: Center(
          child: Text('Sonuç: $sonuc'),
        ),
      ),
    );
  }
}
```

## Unit Test Mantığı

Unit test, küçük bir fonksiyonun veya sınıfın beklenen sonucu üretip üretmediğini sınar.

```yaml
CODE_META:
  id: b14_kod03_unit_test_ornegi
  chapter: 14
  language: dart
  framework: flutter
  runnable: false
  file: test/puan_hesaplayici_test.dart
  purpose: flutter_test ile basit unit test örneği
```

```dart
import 'package:flutter_test/flutter_test.dart';

class PuanHesaplayici {
  String harfNotu(int puan) {
    if (puan >= 90) {
      return 'AA';
    }

    if (puan >= 80) {
      return 'BA';
    }

    return 'Geliştirilmeli';
  }
}

void main() {
  test('85 puan BA döndürmelidir', () {
    final hesaplayici = PuanHesaplayici();

    expect(hesaplayici.harfNotu(85), 'BA');
  });
}
```

## Widget Test Mantığı

Widget test, bir widget’ın ekranda beklenen metni, butonu veya davranışı üretip üretmediğini sınar.

```yaml
CODE_META:
  id: b14_kod04_widget_test_ornegi
  chapter: 14
  language: dart
  framework: flutter
  runnable: false
  file: test/sayac_widget_test.dart
  purpose: flutter_test ile basit widget test örneği
```

```dart
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  testWidgets('Buton ekranda görünmelidir', (tester) async {
    await tester.pumpWidget(
      const MaterialApp(
        home: Scaffold(
          body: ElevatedButton(
            onPressed: null,
            child: Text('Kaydet'),
          ),
        ),
      ),
    );

    expect(find.text('Kaydet'), findsOneWidget);
  });
}
```

## Flutter DevTools

Flutter DevTools; performans, widget ağacı, memory, network ve logging gibi alanlarda inceleme yapmaya yardımcı olur. Özellikle karmaşık arayüzlerde widget inspector ve performance sekmeleri önemlidir.

## Mini Uygulama: Test Edilebilir Görev Sayacı

[SCREENSHOT:b14_01_test_edilebilir_gorev_sayaci]

<!-- SCREENSHOT_META
id: b14_01_test_edilebilir_gorev_sayaci
chapter_id: chapter_14
title: "Test Edilebilir Gorev Sayaci"
kind: browser_page
url: "http://127.0.0.1:5173/__book__/test-debugging/b14_01_test_edilebilir_gorev_sayaci"
viewport: 1440x900
wait_for: "networkidle"
output_file: assets/auto/screenshots/b14_01_test_edilebilir_gorev_sayaci.png
caption: "Test Edilebilir Gorev Sayaci ekran görüntüsü."
validation_mode: capture
-->

```yaml
CODE_META:
  id: b14_kod05_test_edilebilir_gorev_sayaci
  chapter: 14
  language: dart
  framework: flutter
  runnable: true
  file: lib/main.dart
  purpose: Test edilebilir model ve Flutter arayüzünü birlikte gösterme
  screenshot: b14_01_test_edilebilir_gorev_sayaci
```

```dart
import 'package:flutter/material.dart';

void main() {
  runApp(const GorevSayaciUygulamasi());
}

class GorevModeli {
  int tamamlanan = 0;

  void artir() {
    tamamlanan++;
  }

  void sifirla() {
    tamamlanan = 0;
  }

  String durumMetni() {
    if (tamamlanan == 0) {
      return 'Henüz görev tamamlanmadı.';
    }

    return '$tamamlanan görev tamamlandı.';
  }
}

class GorevSayaciUygulamasi extends StatefulWidget {
  const GorevSayaciUygulamasi({super.key});

  @override
  State<GorevSayaciUygulamasi> createState() => _GorevSayaciUygulamasiState();
}

class _GorevSayaciUygulamasiState extends State<GorevSayaciUygulamasi> {
  final GorevModeli model = GorevModeli();

  void artir() {
    setState(() {
      model.artir();
    });
    debugPrint(model.durumMetni());
  }

  void sifirla() {
    setState(() {
      model.sifirla();
    });
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Görev Sayacı',
      home: Scaffold(
        appBar: AppBar(title: const Text('Test Edilebilir Görev Sayacı')),
        body: Center(
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              Text(model.durumMetni()),
              const SizedBox(height: 16),
              Wrap(
                spacing: 12,
                children: [
                  ElevatedButton(
                    onPressed: artir,
                    child: const Text('Görev Tamamla'),
                  ),
                  OutlinedButton(
                    onPressed: sifirla,
                    child: const Text('Sıfırla'),
                  ),
                ],
              ),
            ],
          ),
        ),
      ),
    );
  }
}
```

## Laboratuvar Görevi

“Test Edilebilir Puan Hesaplayıcı” uygulaması geliştiriniz. Puan hesaplama iş mantığı ayrı sınıfta olmalı, en az üç unit test senaryosu yazılmalı ve arayüzde test edilebilir bir sonuç gösterilmelidir.

## Değerlendirme Rubriği

| Ölçüt | Puan | Açıklama |
|---|---:|---|
| Debugging kullanımı | 15 | `debugPrint` ve hata izleme mantığı uygulanmıştır |
| Test edilebilir tasarım | 20 | İş mantığı widget dışına alınmıştır |
| Unit test | 20 | `test`, `expect` ve senaryolar doğru kullanılmıştır |
| Widget test | 15 | Temel widget test mantığı gösterilmiştir |
| DevTools farkındalığı | 10 | Araçların kullanım amacı açıklanmıştır |
| Kod okunabilirliği | 20 | Sınıflar ve testler düzenlidir |

## Bölüm Özeti

Bu bölümde debugging, `debugPrint`, test edilebilir kod, unit test, widget test, `flutter_test`, `expect` ve Flutter DevTools kavramları ele alındı.

## Bölüm Sonu Kontrol Listesi

- [ ] Debugging sürecini açıklayabiliyorum.
- [ ] `debugPrint` kullanabiliyorum.
- [ ] Unit test ve widget test farkını biliyorum.
- [ ] `flutter_test` ile temel test yapısını okuyabiliyorum.
- [ ] Test edilebilir kod yazmanın önemini açıklayabiliyorum.
