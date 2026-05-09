---
chapter_id: etkilesim-formlar
chapter_no: 4
title: "Etkileşim ve Formlar"
artifact_type: chapter
artifact_version: project-based
language: tr
---

# Bölüm 5 — Etkileşim ve Formlar

## Bölümün Amacı

Bu bölümde Flutter uygulamalarında kullanıcıdan veri alma, bu veriyi işleme ve temel doğrulama adımlarını uygulama konuları ele alınmaktadır. Önceki bölümlerde widget mantığı ve layout sistemi üzerinde durulmuştu. Bu bölümde ise kullanıcının arayüzle doğrudan etkileşime geçtiği alanlar incelenecektir.

Mobil uygulamalarda form yapıları oldukça yaygındır. Kullanıcı girişi, kayıt ekranı, profil güncelleme, arama kutusu, geri bildirim formu, ders başvuru ekranı ve anket ekranı gibi birçok senaryo form bileşenlerine dayanır. Flutter’da bu tür işlemler için `TextField`, `TextEditingController`, `Form`, `TextFormField`, `GlobalKey<FormState>` ve doğrulama fonksiyonları kullanılır.

Bu bölüm sonunda öğrenci:

- Flutter’da kullanıcı etkileşimini açıklayabilir.
- `TextField` ile metin girişi alabilir.
- `TextEditingController` ile giriş değerini okuyabilir.
- `Form` ve `TextFormField` yapısını kullanabilir.
- Form doğrulama mantığını uygulayabilir.
- Buton etkileşimleriyle form verisini işleyebilir.
- Basit bir geri bildirim formu geliştirebilir.
- Form bileşenlerini küçük ve okunabilir widget’lara ayırabilir.

## Kullanıcı Etkileşimi Nedir?

Mobil uygulamalarda kullanıcı etkileşimi, kullanıcının ekrandaki bileşenlerle iletişim kurmasıdır. Bu etkileşim bir butona basmak, metin yazmak, seçim yapmak, kaydırmak, liste öğesine dokunmak veya form göndermek şeklinde olabilir.

Flutter’da etkileşim çoğunlukla callback fonksiyonlarıyla yönetilir. Örneğin `ElevatedButton` widget’ının `onPressed` özelliği, butona basıldığında çalışacak fonksiyonu belirtir.

```yaml
CODE_META:
  id: b05_kod01_basit_buton_etkilesimi
  chapter: 5
  language: dart
  framework: flutter
  runnable: true
  file: lib/main.dart
  purpose: ElevatedButton ile temel kullanıcı etkileşimi oluşturma
```

```dart
import 'package:flutter/material.dart';

void main() {
  runApp(const ButonEtkilesimiUygulamasi());
}

class ButonEtkilesimiUygulamasi extends StatelessWidget {
  const ButonEtkilesimiUygulamasi({super.key});

  @override
  Widget build(BuildContext context) {
    return const MaterialApp(
      home: ButonEtkilesimiSayfasi(),
    );
  }
}

class ButonEtkilesimiSayfasi extends StatefulWidget {
  const ButonEtkilesimiSayfasi({super.key});

  @override
  State<ButonEtkilesimiSayfasi> createState() => _ButonEtkilesimiSayfasiState();
}

class _ButonEtkilesimiSayfasiState extends State<ButonEtkilesimiSayfasi> {
  String mesaj = 'Henüz butona basılmadı.';

  void mesajGuncelle() {
    setState(() {
      mesaj = 'Butona basıldı.';
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Buton Etkileşimi'),
      ),
      body: Center(
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Text(mesaj),
            const SizedBox(height: 16),
            ElevatedButton(
              onPressed: mesajGuncelle,
              child: const Text('Mesajı Güncelle'),
            ),
          ],
        ),
      ),
    );
  }
}
```

Bu örnekte kullanıcı butona bastığında `mesajGuncelle()` fonksiyonu çalışır. Fonksiyon içinde `setState()` çağrıldığı için ekrandaki mesaj güncellenir.

::: {custom-style="Ipucu Kutusu"}
**İpucu:** Flutter’da birçok etkileşim, ilgili widget’ın `onPressed`, `onChanged`, `onTap` veya benzeri callback özelliklerine fonksiyon atanarak yönetilir.
:::

## `TextField` ile Metin Girişi

`TextField`, kullanıcıdan metin girişi almak için kullanılan temel widget’tır. Arama kutusu, kullanıcı adı alanı veya kısa not alanı gibi basit girişlerde kullanılabilir.

```yaml
CODE_META:
  id: b05_kod02_textfield_temel
  chapter: 5
  language: dart
  framework: flutter
  runnable: true
  file: lib/main.dart
  purpose: TextField ile kullanıcıdan metin girişi alma
```

```dart
import 'package:flutter/material.dart';

void main() {
  runApp(const TextFieldTemelUygulamasi());
}

class TextFieldTemelUygulamasi extends StatelessWidget {
  const TextFieldTemelUygulamasi({super.key});

  @override
  Widget build(BuildContext context) {
    return const MaterialApp(
      home: TextFieldTemelSayfasi(),
    );
  }
}

class TextFieldTemelSayfasi extends StatefulWidget {
  const TextFieldTemelSayfasi({super.key});

  @override
  State<TextFieldTemelSayfasi> createState() => _TextFieldTemelSayfasiState();
}

class _TextFieldTemelSayfasiState extends State<TextFieldTemelSayfasi> {
  String ad = '';

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('TextField Kullanımı'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            TextField(
              decoration: const InputDecoration(
                labelText: 'Adınızı giriniz',
                border: OutlineInputBorder(),
              ),
              onChanged: (deger) {
                setState(() {
                  ad = deger;
                });
              },
            ),
            const SizedBox(height: 20),
            Text('Merhaba $ad'),
          ],
        ),
      ),
    );
  }
}
```

Bu örnekte `onChanged` fonksiyonu, kullanıcı metin alanına her karakter yazdığında çalışır. Girilen değer `ad` değişkenine aktarılır ve ekranda gösterilir.

`TextField` için sık kullanılan özellikler şunlardır:

| Özellik | Açıklama |
|---|---|
| `decoration` | Alanın görsel açıklamasını ve kenarlık yapısını belirler |
| `labelText` | Metin alanının açıklayıcı etiketidir |
| `hintText` | Kullanıcıya örnek veya ipucu gösterir |
| `keyboardType` | Klavye türünü belirler |
| `obscureText` | Şifre alanlarında metni gizler |
| `onChanged` | Metin değiştikçe çalışan callback fonksiyonudur |

## `TextEditingController`

`TextEditingController`, metin alanındaki değeri okumak, değiştirmek veya temizlemek için kullanılır. Basit uygulamalarda `onChanged` yeterli olabilir; ancak form gönderme anında değeri okumak gerektiğinde controller daha kullanışlıdır.

```yaml
CODE_META:
  id: b05_kod03_texteditingcontroller
  chapter: 5
  language: dart
  framework: flutter
  runnable: true
  file: lib/main.dart
  purpose: TextEditingController ile metin değerini okuma ve temizleme
```

```dart
import 'package:flutter/material.dart';

void main() {
  runApp(const ControllerUygulamasi());
}

class ControllerUygulamasi extends StatelessWidget {
  const ControllerUygulamasi({super.key});

  @override
  Widget build(BuildContext context) {
    return const MaterialApp(
      home: ControllerSayfasi(),
    );
  }
}

class ControllerSayfasi extends StatefulWidget {
  const ControllerSayfasi({super.key});

  @override
  State<ControllerSayfasi> createState() => _ControllerSayfasiState();
}

class _ControllerSayfasiState extends State<ControllerSayfasi> {
  final TextEditingController notController = TextEditingController();
  String kaydedilenNot = '';

  @override
  void dispose() {
    notController.dispose();
    super.dispose();
  }

  void notuKaydet() {
    setState(() {
      kaydedilenNot = notController.text.trim();
    });
  }

  void notuTemizle() {
    setState(() {
      notController.clear();
      kaydedilenNot = '';
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Controller Kullanımı'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            TextField(
              controller: notController,
              decoration: const InputDecoration(
                labelText: 'Kısa not',
                hintText: 'Bugünkü çalışma notunuzu yazınız',
                border: OutlineInputBorder(),
              ),
              maxLines: 3,
            ),
            const SizedBox(height: 16),
            Wrap(
              spacing: 12,
              children: [
                ElevatedButton(
                  onPressed: notuKaydet,
                  child: const Text('Kaydet'),
                ),
                OutlinedButton(
                  onPressed: notuTemizle,
                  child: const Text('Temizle'),
                ),
              ],
            ),
            const SizedBox(height: 20),
            Text('Kaydedilen not: $kaydedilenNot'),
          ],
        ),
      ),
    );
  }
}
```

Bu örnekte `notController.text` ile metin alanındaki değer okunmaktadır. `clear()` metodu ise alanı temizler. `TextEditingController` kullanıldığında `dispose()` içinde controller’ın serbest bırakılması iyi bir uygulama pratiğidir.

::: {custom-style="Dikkat Kutusu"}
**Dikkat:** `TextEditingController` bir kaynak yönetimi nesnesidir. Stateful widget içinde kullanılıyorsa çoğu durumda `dispose()` metodunda temizlenmelidir.
:::

## `Form` ve `TextFormField`

Basit metin alanları için `TextField` yeterli olabilir. Ancak birden fazla alanın birlikte doğrulanması ve gönderilmesi gerekiyorsa `Form` yapısı kullanılmalıdır.

`Form`, form alanlarını kapsayan üst yapıdır. `TextFormField` ise doğrulama desteği olan metin giriş alanıdır.

```yaml
CODE_META:
  id: b05_kod04_form_textformfield
  chapter: 5
  language: dart
  framework: flutter
  runnable: true
  file: lib/main.dart
  purpose: Form ve TextFormField ile temel doğrulama yapısı kurma
```

```dart
import 'package:flutter/material.dart';

void main() {
  runApp(const FormTemelUygulamasi());
}

class FormTemelUygulamasi extends StatelessWidget {
  const FormTemelUygulamasi({super.key});

  @override
  Widget build(BuildContext context) {
    return const MaterialApp(
      home: FormTemelSayfasi(),
    );
  }
}

class FormTemelSayfasi extends StatefulWidget {
  const FormTemelSayfasi({super.key});

  @override
  State<FormTemelSayfasi> createState() => _FormTemelSayfasiState();
}

class _FormTemelSayfasiState extends State<FormTemelSayfasi> {
  final GlobalKey<FormState> formKey = GlobalKey<FormState>();
  final TextEditingController adController = TextEditingController();
  final TextEditingController epostaController = TextEditingController();

  @override
  void dispose() {
    adController.dispose();
    epostaController.dispose();
    super.dispose();
  }

  void formuGonder() {
    final formGecerli = formKey.currentState!.validate();

    if (!formGecerli) {
      return;
    }

    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text(
          'Form gönderildi: ${adController.text} - ${epostaController.text}',
        ),
      ),
    );
  }

  String? bosOlamaz(String? deger) {
    if (deger == null || deger.trim().isEmpty) {
      return 'Bu alan boş bırakılamaz.';
    }

    return null;
  }

  String? epostaKontrol(String? deger) {
    if (deger == null || deger.trim().isEmpty) {
      return 'E-posta alanı boş bırakılamaz.';
    }

    if (!deger.contains('@')) {
      return 'Geçerli bir e-posta adresi giriniz.';
    }

    return null;
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Form Kullanımı'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Form(
          key: formKey,
          child: Column(
            children: [
              TextFormField(
                controller: adController,
                decoration: const InputDecoration(
                  labelText: 'Ad Soyad',
                  border: OutlineInputBorder(),
                ),
                validator: bosOlamaz,
              ),
              const SizedBox(height: 16),
              TextFormField(
                controller: epostaController,
                decoration: const InputDecoration(
                  labelText: 'E-posta',
                  border: OutlineInputBorder(),
                ),
                keyboardType: TextInputType.emailAddress,
                validator: epostaKontrol,
              ),
              const SizedBox(height: 20),
              ElevatedButton(
                onPressed: formuGonder,
                child: const Text('Formu Gönder'),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
```

Bu örnekte `formKey.currentState!.validate()` çağrısı, form içindeki tüm `TextFormField` alanlarının `validator` fonksiyonlarını çalıştırır. Eğer herhangi bir alan geçersizse form gönderilmez.

## Doğrulama Mantığı

Form doğrulama, kullanıcının girdiği verinin beklenen kurallara uygun olup olmadığını kontrol etme işlemidir. Örneğin:

- Ad alanı boş olmamalıdır.
- E-posta adresi `@` içermelidir.
- Şifre belirli uzunlukta olmalıdır.
- Sayısal alanlarda negatif değer girilmemelidir.
- Telefon numarası belirli karakterlerden oluşmalıdır.

Flutter’da `TextFormField` için `validator` fonksiyonu kullanılır. Bu fonksiyon geçerli değer için `null`, hatalı değer için hata mesajı döndürür.

```dart
String? bosOlamaz(String? deger) {
  if (deger == null || deger.trim().isEmpty) {
    return 'Bu alan boş bırakılamaz.';
  }

  return null;
}
```

Bu fonksiyonun dönüş tipi `String?` şeklindedir. Çünkü hata yoksa `null`, hata varsa hata mesajı döndürülür.

::: {custom-style="Sinav Notu Kutusu"}
**Sınav Notu:** `validator` fonksiyonunda `null` dönmek “alan geçerli” anlamına gelir. Hata mesajı dönmek ise alanın geçersiz olduğunu bildirir.
:::

## Klavye Türü ve Giriş Davranışı

Flutter’da metin alanlarının klavye türü `keyboardType` ile belirlenebilir. Bu özellik, kullanıcının veri girişini kolaylaştırır.

| Kullanım | Örnek |
|---|---|
| Metin girişi | `TextInputType.text` |
| E-posta girişi | `TextInputType.emailAddress` |
| Sayı girişi | `TextInputType.number` |
| Telefon girişi | `TextInputType.phone` |
| Çok satırlı metin | `TextInputType.multiline` |

Örneğin e-posta alanı için:

```dart
TextFormField(
  keyboardType: TextInputType.emailAddress,
)
```

Şifre alanı için ise `obscureText` kullanılabilir:

```dart
TextFormField(
  obscureText: true,
)
```

Bu özellikler yalnızca görsel kolaylık sağlamaz; aynı zamanda kullanıcı deneyimini de iyileştirir.

## `SnackBar` ile Kullanıcıya Geri Bildirim Verme

Form gönderme, kayıt alma veya hata bildirme gibi işlemlerde kullanıcıya kısa geri bildirim göstermek gerekir. Flutter’da bunun için `SnackBar` kullanılabilir.

```yaml
CODE_META:
  id: b05_kod05_snackbar_geri_bildirim
  chapter: 5
  language: dart
  framework: flutter
  runnable: true
  file: lib/main.dart
  purpose: SnackBar ile kullanıcıya kısa geri bildirim verme
```

```dart
import 'package:flutter/material.dart';

void main() {
  runApp(const SnackBarUygulamasi());
}

class SnackBarUygulamasi extends StatelessWidget {
  const SnackBarUygulamasi({super.key});

  @override
  Widget build(BuildContext context) {
    return const MaterialApp(
      home: SnackBarSayfasi(),
    );
  }
}

class SnackBarSayfasi extends StatelessWidget {
  const SnackBarSayfasi({super.key});

  void mesajGoster(BuildContext context) {
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(
        content: Text('İşlem başarıyla tamamlandı.'),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('SnackBar'),
      ),
      body: Center(
        child: ElevatedButton(
          onPressed: () => mesajGoster(context),
          child: const Text('Mesaj Göster'),
        ),
      ),
    );
  }
}
```

`ScaffoldMessenger.of(context).showSnackBar()` çağrısı, mevcut sayfa üzerinde kısa bir mesaj gösterir. Bu yapı form gönderme işlemlerinde sık kullanılır.

## Formu Widget’lara Bölmek

Formlar büyüdükçe tüm kodu tek bir `build()` metodu içinde tutmak okunabilirliği azaltır. Bu nedenle form alanlarını küçük widget’lara bölmek iyi bir yaklaşımdır.

Aşağıdaki örnekte form alanı ayrı bir widget olarak tasarlanmıştır.

```yaml
CODE_META:
  id: b05_kod06_form_alani_widget
  chapter: 5
  language: dart
  framework: flutter
  runnable: true
  file: lib/main.dart
  purpose: Form alanını yeniden kullanılabilir widget olarak tasarlama
```

```dart
import 'package:flutter/material.dart';

void main() {
  runApp(const FormWidgetUygulamasi());
}

class FormWidgetUygulamasi extends StatelessWidget {
  const FormWidgetUygulamasi({super.key});

  @override
  Widget build(BuildContext context) {
    return const MaterialApp(
      home: FormWidgetSayfasi(),
    );
  }
}

class FormWidgetSayfasi extends StatefulWidget {
  const FormWidgetSayfasi({super.key});

  @override
  State<FormWidgetSayfasi> createState() => _FormWidgetSayfasiState();
}

class _FormWidgetSayfasiState extends State<FormWidgetSayfasi> {
  final GlobalKey<FormState> formKey = GlobalKey<FormState>();
  final TextEditingController adController = TextEditingController();
  final TextEditingController mesajController = TextEditingController();

  @override
  void dispose() {
    adController.dispose();
    mesajController.dispose();
    super.dispose();
  }

  String? bosOlamaz(String? deger) {
    if (deger == null || deger.trim().isEmpty) {
      return 'Bu alan boş bırakılamaz.';
    }

    return null;
  }

  void gonder() {
    if (!formKey.currentState!.validate()) {
      return;
    }

    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(
        content: Text('Form başarıyla gönderildi.'),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Parçalı Form'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Form(
          key: formKey,
          child: Column(
            children: [
              OzelMetinAlani(
                controller: adController,
                label: 'Ad Soyad',
                validator: bosOlamaz,
              ),
              const SizedBox(height: 16),
              OzelMetinAlani(
                controller: mesajController,
                label: 'Mesaj',
                validator: bosOlamaz,
                maxLines: 4,
              ),
              const SizedBox(height: 20),
              ElevatedButton(
                onPressed: gonder,
                child: const Text('Gönder'),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

class OzelMetinAlani extends StatelessWidget {
  final TextEditingController controller;
  final String label;
  final String? Function(String?) validator;
  final int maxLines;

  const OzelMetinAlani({
    super.key,
    required this.controller,
    required this.label,
    required this.validator,
    this.maxLines = 1,
  });

  @override
  Widget build(BuildContext context) {
    return TextFormField(
      controller: controller,
      maxLines: maxLines,
      decoration: InputDecoration(
        labelText: label,
        border: const OutlineInputBorder(),
      ),
      validator: validator,
    );
  }
}
```

Bu örnekte `OzelMetinAlani`, form alanı üretmek için kullanılan yeniden kullanılabilir bir widget’tır. Böylece ana form kodu daha okunabilir hâle gelir.

## Mini Uygulama: Ders Geri Bildirim Formu

Bu mini uygulamada öğrencinin bir ders için geri bildirim gönderebildiği basit bir form geliştirilecektir. Formda ad soyad, e-posta, ders adı ve geri bildirim mesajı alanları bulunacaktır.

[SCREENSHOT:b05_01_ders_geri_bildirim_formu]

<!-- SCREENSHOT_META
id: b05_01_ders_geri_bildirim_formu
chapter_id: chapter_04
title: "Ders Geri Bildirim Formu"
kind: browser_page
url: "http://127.0.0.1:5173/__book__/etkilesim-formlar/b05_01_ders_geri_bildirim_formu"
viewport: 1440x900
wait_for: "networkidle"
output_file: assets/auto/screenshots/b05_01_ders_geri_bildirim_formu.png
caption: "Ders Geri Bildirim Formu ekran görüntüsü."
validation_mode: capture
-->

```yaml
CODE_META:
  id: b05_kod07_ders_geri_bildirim_formu
  chapter: 5
  language: dart
  framework: flutter
  runnable: true
  file: lib/main.dart
  purpose: Form, TextFormField, TextEditingController, validator ve SnackBar kullanımı
  screenshot: b05_01_ders_geri_bildirim_formu
```

```dart
import 'package:flutter/material.dart';

void main() {
  runApp(const GeriBildirimUygulamasi());
}

class GeriBildirimUygulamasi extends StatelessWidget {
  const GeriBildirimUygulamasi({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Ders Geri Bildirim Formu',
      theme: ThemeData(
        colorSchemeSeed: Colors.deepPurple,
        useMaterial3: true,
      ),
      home: const GeriBildirimSayfasi(),
    );
  }
}

class GeriBildirimSayfasi extends StatefulWidget {
  const GeriBildirimSayfasi({super.key});

  @override
  State<GeriBildirimSayfasi> createState() => _GeriBildirimSayfasiState();
}

class _GeriBildirimSayfasiState extends State<GeriBildirimSayfasi> {
  final GlobalKey<FormState> formKey = GlobalKey<FormState>();

  final TextEditingController adSoyadController = TextEditingController();
  final TextEditingController epostaController = TextEditingController();
  final TextEditingController dersController = TextEditingController();
  final TextEditingController mesajController = TextEditingController();

  @override
  void dispose() {
    adSoyadController.dispose();
    epostaController.dispose();
    dersController.dispose();
    mesajController.dispose();
    super.dispose();
  }

  String? bosOlamaz(String? deger) {
    if (deger == null || deger.trim().isEmpty) {
      return 'Bu alan boş bırakılamaz.';
    }

    return null;
  }

  String? epostaDogrula(String? deger) {
    if (deger == null || deger.trim().isEmpty) {
      return 'E-posta alanı boş bırakılamaz.';
    }

    if (!deger.contains('@') || !deger.contains('.')) {
      return 'Geçerli bir e-posta adresi giriniz.';
    }

    return null;
  }

  void formuGonder() {
    if (!formKey.currentState!.validate()) {
      return;
    }

    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text(
          '${adSoyadController.text} için geri bildirim kaydedildi.',
        ),
      ),
    );

    adSoyadController.clear();
    epostaController.clear();
    dersController.clear();
    mesajController.clear();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Ders Geri Bildirim Formu'),
      ),
      body: Center(
        child: ConstrainedBox(
          constraints: const BoxConstraints(maxWidth: 640),
          child: SingleChildScrollView(
            padding: const EdgeInsets.all(16),
            child: Card(
              child: Padding(
                padding: const EdgeInsets.all(20),
                child: Form(
                  key: formKey,
                  child: Column(
                    children: [
                      const Icon(Icons.rate_review_outlined, size: 56),
                      const SizedBox(height: 12),
                      Text(
                        'Ders Geri Bildirimi',
                        style: Theme.of(context).textTheme.headlineSmall,
                      ),
                      const SizedBox(height: 20),
                      TextFormField(
                        controller: adSoyadController,
                        decoration: const InputDecoration(
                          labelText: 'Ad Soyad',
                          border: OutlineInputBorder(),
                          prefixIcon: Icon(Icons.person_outline),
                        ),
                        validator: bosOlamaz,
                      ),
                      const SizedBox(height: 16),
                      TextFormField(
                        controller: epostaController,
                        decoration: const InputDecoration(
                          labelText: 'E-posta',
                          border: OutlineInputBorder(),
                          prefixIcon: Icon(Icons.mail_outline),
                        ),
                        keyboardType: TextInputType.emailAddress,
                        validator: epostaDogrula,
                      ),
                      const SizedBox(height: 16),
                      TextFormField(
                        controller: dersController,
                        decoration: const InputDecoration(
                          labelText: 'Ders Adı',
                          border: OutlineInputBorder(),
                          prefixIcon: Icon(Icons.menu_book_outlined),
                        ),
                        validator: bosOlamaz,
                      ),
                      const SizedBox(height: 16),
                      TextFormField(
                        controller: mesajController,
                        decoration: const InputDecoration(
                          labelText: 'Geri Bildirim Mesajı',
                          alignLabelWithHint: true,
                          border: OutlineInputBorder(),
                          prefixIcon: Icon(Icons.edit_note),
                        ),
                        maxLines: 5,
                        validator: bosOlamaz,
                      ),
                      const SizedBox(height: 20),
                      SizedBox(
                        width: double.infinity,
                        child: ElevatedButton.icon(
                          onPressed: formuGonder,
                          icon: const Icon(Icons.send),
                          label: const Text('Geri Bildirimi Gönder'),
                        ),
                      ),
                    ],
                  ),
                ),
              ),
            ),
          ),
        ),
      ),
    );
  }
}
```

Bu uygulamada form doğrulama, controller kullanımı, temizleme işlemi ve kullanıcıya `SnackBar` ile geri bildirim verme bir arada kullanılmıştır. `SingleChildScrollView`, küçük ekranlarda formun taşmasını azaltmak için eklenmiştir.

## Sık Yapılan Hatalar

| Hata | Açıklama | Çözüm |
|---|---|---|
| Controller’ı dispose etmemek | Kaynak yönetimi açısından sorun oluşturabilir | `dispose()` içinde controller’ları temizle |
| Form doğrulamasını atlamak | Eksik veya hatalı veri gönderilebilir | `formKey.currentState!.validate()` kullan |
| Hata mesajı yerine sadece konsola yazmak | Kullanıcı hatayı göremez | `validator` ve `SnackBar` kullan |
| Çok uzun formu scroll olmadan tasarlamak | Küçük ekranlarda taşma olur | `SingleChildScrollView` kullan |
| Tüm formu tek büyük widget içinde yazmak | Okunabilirlik azalır | Alanları alt widget’lara böl |
| E-posta kontrolünü hiç yapmamak | Geçersiz veri alınabilir | Basit format kontrolü ekle |

## Laboratuvar Görevi

Bu laboratuvar çalışmasında öğrenciden “Öğrenci Etkinlik Başvuru Formu” geliştirmesi beklenmektedir.

### İstenenler

1. Uygulama başlığı “Etkinlik Başvuru Formu” olmalıdır.
2. Formda ad soyad, öğrenci numarası, e-posta ve etkinlik adı alanları bulunmalıdır.
3. Tüm alanlar boş geçilememelidir.
4. E-posta alanı için basit format kontrolü yapılmalıdır.
5. Öğrenci numarası alanında sayısal klavye kullanılmalıdır.
6. Form gönderildiğinde `SnackBar` ile başarı mesajı gösterilmelidir.
7. Form gönderildikten sonra alanlar temizlenmelidir.
8. Uzun ekranlar için `SingleChildScrollView` kullanılmalıdır.
9. En az bir özel form alanı widget’ı oluşturulmalıdır.
10. Controller’lar `dispose()` içinde temizlenmelidir.

### Beklenen Kazanımlar

Bu laboratuvar sonunda öğrenci:

- Form doğrulama akışını kurabilir.
- `TextEditingController` ile form verisi okuyabilir.
- `TextFormField` içinde `validator` kullanabilir.
- Kullanıcıya `SnackBar` ile geri bildirim verebilir.
- Form ekranını okunabilir widget parçalarına bölebilir.

## Değerlendirme Rubriği

| Ölçüt | Puan | Açıklama |
|---|---:|---|
| Form yapısı | 20 | `Form`, `GlobalKey<FormState>` ve `TextFormField` doğru kullanılmıştır |
| Doğrulama | 20 | Boş alan ve e-posta kontrolleri yapılmıştır |
| Controller yönetimi | 15 | Controller’lar doğru okunmuş ve `dispose()` içinde temizlenmiştir |
| Kullanıcı geri bildirimi | 15 | `SnackBar` ile anlamlı mesaj verilmiştir |
| Arayüz kullanılabilirliği | 10 | Form alanları düzenli ve okunabilirdir |
| Scroll ve taşma yönetimi | 10 | Küçük ekranlar için uygun yapı kurulmuştur |
| Kod okunabilirliği | 10 | Kod anlamlı widget parçalarına ayrılmıştır |

## Bölüm Özeti

Bu bölümde Flutter’da kullanıcı etkileşimi ve form yapıları incelendi. `TextField` ile basit metin girişi alma, `TextEditingController` ile giriş değerini okuma ve temizleme, `Form` ve `TextFormField` ile doğrulama yapısı kurma konuları örneklerle ele alındı.

Ayrıca `validator` fonksiyonlarının çalışma mantığı, `GlobalKey<FormState>` kullanımı, `SnackBar` ile kullanıcıya geri bildirim verme ve uzun formlarda `SingleChildScrollView` kullanımı açıklandı. Mini uygulamada bu kavramlar ders geri bildirim formu üzerinden bütünleştirildi.

Bölümün ana fikri şudur: Form tasarımı yalnızca veri almak değildir; doğru veri almak, kullanıcıya anlaşılır geri bildirim vermek ve arayüzü farklı ekran koşullarında kullanılabilir tutmaktır.

## Bölüm Sonu Kontrol Listesi

- [ ] `TextField` ile basit metin girişi alabiliyorum.
- [ ] `TextEditingController` ile alan değerini okuyabiliyorum.
- [ ] Controller’ları `dispose()` içinde temizlemem gerektiğini biliyorum.
- [ ] `Form` ve `TextFormField` yapısını kurabiliyorum.
- [ ] `validator` fonksiyonu yazabiliyorum.
- [ ] `GlobalKey<FormState>` ile form doğrulaması yapabiliyorum.
- [ ] `SnackBar` ile kullanıcıya geri bildirim verebiliyorum.
- [ ] Uzun formlar için scroll yapısı kurabiliyorum.
