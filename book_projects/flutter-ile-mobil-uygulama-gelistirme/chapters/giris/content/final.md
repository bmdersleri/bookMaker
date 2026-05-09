---
chapter_id: giris
chapter_no: 6
title: "Flutter ile Mobil Uygulama Geliştirmeye Giriş"
artifact_type: chapter
artifact_version: project-based
language: tr
---

# Flutter Ekosistemine Giriş ve İlk Uygulama

## Bölüm Özeti

Bu bölümde Flutter ekosisteminin temel bileşenleri tanıtılmakta, geliştirme ortamının nasıl doğrulanacağı açıklanmakta ve ilk Flutter uygulamasının nasıl oluşturulacağı adım adım gösterilmektedir. Bölümün amacı, okuyucunun Flutter'ı yalnızca bir arayüz kütüphanesi olarak değil; Dart dili, widget yaklaşımı, geliştirme araçları, test edilebilir proje yapısı ve çoklu platform hedefleriyle birlikte bir uygulama geliştirme ekosistemi olarak kavramasını sağlamaktır.

Bu bölüm, kitabın sonraki bölümlerinde kullanılacak ortak kavramlara hazırlık niteliğindedir. Bu nedenle state management, API kullanımı, veri kalıcılığı ve uygulama yayınlama süreçleri ayrıntılandırılmamıştır. Bu konular ilerleyen bölümlerde ayrı başlıklar hâlinde ele alınacaktır.

## Öğrenme Kazanımları

Bu bölümü tamamlayan okuyucu:

1. Flutter'ın ne amaçla kullanıldığını ve hangi platformları hedefleyebildiğini açıklar.
2. Flutter, Dart, widget, SDK, emulator/simulator ve hot reload kavramlarını temel düzeyde tanımlar.
3. Yerel geliştirme ortamının hazır olup olmadığını `flutter doctor` komutu ile kontrol eder.
4. Komut satırı üzerinden yeni bir Flutter projesi oluşturur.
5. Oluşturulan projenin temel klasör ve dosya yapısını yorumlar.
6. `main.dart` dosyasındaki ilk uygulama kodunu okuyup temel parçalarına ayırır.
7. Basit bir Flutter arayüzünde `MaterialApp`, `Scaffold`, `AppBar`, `Center` ve `Text` widget'larının görevini açıklar.
8. Bölüm sonunda verilen laboratuvar görevini tamamlayarak ilk uygulamasını kişiselleştirir.

---

## Flutter Nedir?

Flutter, tek bir kod tabanı ile birden fazla platform için uygulama geliştirmeyi hedefleyen açık kaynaklı bir kullanıcı arayüzü geliştirme teknolojisidir. Mobil uygulamalar Flutter'ın en bilinen kullanım alanı olsa da Flutter ekosistemi yalnızca Android ve iOS ile sınırlı değildir. Web, masaüstü ve gömülü sistemlere yönelik kullanım senaryoları da ekosistemin parçasıdır.

Flutter geliştirme sürecinde arayüzler, küçük ve birleştirilebilir yapı taşları olan widget'lar ile oluşturulur. Bir Flutter uygulamasında ekranda görülen metin, buton, satır, sütun, boşluk, hizalama, tema ve sayfa yapısı gibi unsurların tamamı widget yaklaşımıyla temsil edilir.

Flutter'ın temel ayırt edici özellikleri şunlardır:

- Tek kod tabanı ile çoklu platform hedefleme
- Dart programlama dili ile uygulama geliştirme
- Widget tabanlı arayüz mimarisi
- Hızlı geliştirme için hot reload desteği
- Zengin hazır arayüz bileşenleri
- Komut satırı, VS Code ve Android Studio gibi araçlarla çalışma imkânı
- Test, analiz ve hata ayıklama araçlarıyla bütünleşik geliştirme deneyimi

Flutter öğrenirken asıl amaç yalnızca ekrana bir buton koymayı öğrenmek değildir. Daha önemli amaç, uygulama arayüzünün nasıl parçalara ayrıldığını, bu parçaların nasıl bir ağaç yapısı oluşturduğunu ve kod değişikliklerinin ekrana nasıl yansıdığını anlamaktır.

---

## Flutter Ekosisteminin Temel Bileşenleri

Flutter ekosistemi birkaç ana bileşenden oluşur:

| Bileşen | Görevi |
|---|---|
| Flutter SDK | Uygulama geliştirme, derleme, çalıştırma ve test araçlarını sağlar. |
| Dart | Flutter uygulamalarının yazıldığı programlama dilidir. |
| Widget sistemi | Kullanıcı arayüzünün yapı taşlarını oluşturur. |
| Flutter CLI | `flutter create`, `flutter run`, `flutter doctor` gibi komutları sunar. |
| Paket ekosistemi | Uygulamalara ek özellik kazandırmak için paket kullanımını sağlar. |
| DevTools | Hata ayıklama, performans inceleme ve widget ağacı analizi için kullanılır. |
| IDE/Editor eklentileri | VS Code veya Android Studio içinde Flutter geliştirme desteği sağlar. |

Bu kitapta temel geliştirme ortamı olarak VS Code ve PowerShell odaklı bir yaklaşım izlenecektir. Ancak Flutter projeleri Android Studio, IntelliJ tabanlı editörler veya farklı terminal ortamlarıyla da geliştirilebilir.

---

## Geliştirme Ortamını Kontrol Etme

İlk uygulamayı oluşturmadan önce Flutter SDK'nın sistem tarafından görülebildiği doğrulanmalıdır. Bunun için terminalde şu komut çalıştırılır:

```powershell
flutter --version
```

Bu komut Flutter SDK sürümünü, Dart sürümünü ve bazı temel ortam bilgilerini gösterir.

Daha ayrıntılı kontrol için:

```powershell
flutter doctor
```

`flutter doctor`, Flutter geliştirme ortamındaki eksik veya hatalı bileşenleri raporlar. Örneğin Android toolchain, lisans onayları, bağlı cihazlar, VS Code eklentileri veya tarayıcı desteği gibi konularda uyarılar gösterebilir.

Bu bölüm için `flutter doctor` çıktısının tamamen kusursuz olması zorunlu değildir; ancak en azından Flutter SDK'nın çalışır durumda olması ve bir hedef cihazın ya da tarayıcının görülebilmesi beklenir.

Örnek kontrol akışı:

```powershell
flutter --version
flutter doctor
flutter devices
```

Bu komutlar çalıştırıldığında sistemde görülen cihazlar listelenir. Eğer Android emulator, fiziksel Android cihaz, iOS simulator veya Chrome gibi bir hedef görünüyorsa ilk uygulama çalıştırılabilir.

---

## İlk Flutter Projesini Oluşturma

Yeni bir Flutter projesi oluşturmak için uygun bir çalışma klasörüne geçilir. Örneğin:

```powershell
cd D:\flutter_projects
```

Ardından yeni proje oluşturulur:

```powershell
flutter create ilk_flutter_uygulamam
```

Proje klasörüne geçilir:

```powershell
cd ilk_flutter_uygulamam
```

VS Code ile açmak için:

```powershell
code .
```

Projenin çalıştırılması için:

```powershell
flutter run
```

Birden fazla cihaz varsa Flutter hangi hedefte çalıştırmak istediğinizi sorabilir. Web hedefi için örnek kullanım:

```powershell
flutter run -d chrome
```

Bu aşamada Flutter, varsayılan sayaç uygulamasını oluşturur ve seçilen hedefte çalıştırır. Bu varsayılan uygulama, Flutter'ın proje şablonunu ve temel çalışma biçimini görmek için yararlıdır; ancak bu bölümde daha sade bir ilk uygulama hazırlanacaktır.

---

## Flutter Proje Yapısını Tanıma

Yeni oluşturulan Flutter projesinde birçok klasör ve dosya bulunur. Başlangıç düzeyinde en önemli olanlar şunlardır:

| Dosya/Klasör | Açıklama |
|---|---|
| `lib/` | Uygulama kaynak kodlarının ana klasörüdür. |
| `lib/main.dart` | Uygulamanın başlangıç dosyasıdır. |
| `pubspec.yaml` | Paket, varlık, sürüm ve proje yapılandırmalarını içerir. |
| `test/` | Test dosyalarının bulunduğu klasördür. |
| `android/` | Android platformuna özgü dosyaları içerir. |
| `ios/` | iOS platformuna özgü dosyaları içerir. |
| `web/` | Web hedefi için gerekli dosyaları içerir. |
| `windows/`, `macos/`, `linux/` | Masaüstü platformlarına özgü dosyaları içerir. |

Yeni başlayanlar çoğunlukla `lib/main.dart` üzerinde çalışır. Ancak iyi bir Flutter geliştiricisi, projenin yalnızca `main.dart` dosyasından ibaret olmadığını erken aşamada fark etmelidir. Uygulama büyüdükçe kodlar farklı klasörlere ayrılır, bileşenler modüler hâle getirilir ve test edilebilir bir yapı kurulur.

Bu bölümde yalnızca `lib/main.dart` dosyası üzerinde çalışılacaktır.

---

## İlk Uygulama Kodunu Yazma

Varsayılan `lib/main.dart` dosyasının içeriğini aşağıdaki kod ile değiştirin:

```dart
import 'package:flutter/material.dart';

void main() {
  runApp(const IlkFlutterUygulamasi());
}

class IlkFlutterUygulamasi extends StatelessWidget {
  const IlkFlutterUygulamasi({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'İlk Flutter Uygulamam',
      debugShowCheckedModeBanner: false,
      home: Scaffold(
        appBar: AppBar(
          title: const Text('Flutter ile İlk Adım'),
        ),
        body: const Center(
          child: Text(
            'Merhaba Flutter!',
            style: TextStyle(fontSize: 28),
          ),
        ),
      ),
    );
  }
}
```

Bu kod, ekranda üst kısmında başlık çubuğu bulunan ve ortasında "Merhaba Flutter!" yazan basit bir uygulama oluşturur.

Kodun temel parçaları şöyledir:

| Kod Parçası | Görevi |
|---|---|
| `import 'package:flutter/material.dart';` | Material Design bileşenlerini projeye dahil eder. |
| `void main()` | Dart uygulamasının başlangıç noktasıdır. |
| `runApp(örnek çıktı ilgili uygulama çalıştırıldığında gözlemlenir)` | Flutter uygulamasını başlatır. |
| `StatelessWidget` | Durum tutmayan bir arayüz bileşeni tanımlar. |
| `build(örnek çıktı ilgili uygulama çalıştırıldığında gözlemlenir)` | Widget'ın ekranda nasıl görüneceğini belirler. |
| `MaterialApp` | Material Design tabanlı uygulama kabuğunu oluşturur. |
| `Scaffold` | Sayfa iskeletini sağlar. |
| `AppBar` | Üst uygulama çubuğunu oluşturur. |
| `Center` | İçeriği ortalar. |
| `Text` | Ekrana metin yazar. |

Bu örnekte herhangi bir kullanıcı etkileşimi, state management veya veri kaynağı kullanılmamıştır. Amaç, Flutter uygulamasının en temel iskeletini anlamaktır.

[SCREENSHOT:b01_01_ilk_flutter_uygulamasi]

<!-- SCREENSHOT_META
id: b01_01_ilk_flutter_uygulamasi
chapter_id: chapter_06
title: "Ilk Flutter Uygulamasi"
kind: browser_page
url: "http://127.0.0.1:5173/__book__/giris/b01_01_ilk_flutter_uygulamasi"
viewport: 1440x900
wait_for: "networkidle"
output_file: assets/auto/screenshots/b01_01_ilk_flutter_uygulamasi.png
caption: "Ilk Flutter Uygulamasi ekran görüntüsü."
validation_mode: capture
-->

**Şekil 1.1.** İlk Flutter uygulamasında AppBar ve ortalanmış metin görünümü.

---

## Widget Ağacı Mantığı

Flutter arayüzleri hiyerarşik bir ağaç yapısı gibi düşünülebilir. Yukarıdaki örneğin sadeleştirilmiş widget ağacı şu şekildedir:

```text
IlkFlutterUygulamasi
└── MaterialApp
    └── Scaffold
        ├── AppBar
        │   └── Text
        └── Center
            └── Text
```

Bu yapı, Flutter'ın arayüzü küçük parçalara ayırma yaklaşımını gösterir. Her widget belirli bir görevi yerine getirir. Örneğin `Center` yalnızca çocuğunu ortalamakla ilgilenir; `Text` yalnızca metin gösterir; `Scaffold` ise sayfanın genel iskeletini düzenler.

Bu yaklaşım, uygulama büyüdüğünde arayüzü yönetilebilir parçalara ayırmayı kolaylaştırır.

---

## Hot Reload ile Hızlı Deneme

Flutter'ın öğrenme sürecini hızlandıran en önemli özelliklerinden biri hot reload'dur. Uygulama çalışırken kodda yapılan birçok değişiklik, uygulamayı tamamen kapatıp yeniden başlatmadan ekrana yansıtılabilir.

Örneğin `Text` widget'ındaki metni şu şekilde değiştirin:

```dart
'Merhaba Flutter!'
```

yerine:

```dart
'Flutter öğrenmeye başladım!'
```

VS Code'da debug oturumu açıkken hot reload düğmesine basabilir veya terminalde uygun kısayolu kullanabilirsiniz. Değişiklik kısa sürede ekrana yansır.

Hot reload özellikle arayüz tasarımı, metin düzenleme, renk, boyut ve hizalama denemelerinde oldukça kullanışlıdır. Ancak her değişiklik hot reload ile uygulanamayabilir. Bazı durumlarda hot restart veya uygulamayı yeniden başlatma gerekebilir.

---

## Sık Karşılaşılan Başlangıç Sorunları

Flutter'a yeni başlayanların karşılaşabileceği bazı tipik sorunlar şunlardır:

| Sorun | Olası Neden | Çözüm Yaklaşımı |
|---|---|---|
| `flutter` komutu tanınmıyor | Flutter SDK PATH'e eklenmemiştir. | Flutter SDK yolunu PATH'e ekleyin. |
| `flutter doctor` uyarı veriyor | Android toolchain, lisans veya editor eklentisi eksik olabilir. | `flutter doctor` çıktısındaki önerileri sırayla uygulayın. |
| Cihaz görünmüyor | Emulator kapalı veya fiziksel cihaz tanınmıyor olabilir. | `flutter devices` ile cihaz listesini kontrol edin. |
| Uygulama çok geç açılıyor | İlk derleme zaman alabilir. | İlk derlemenin normalden uzun sürebileceğini unutmayın. |
| Hot reload çalışmıyor | Debug oturumu doğru başlamamış olabilir. | Uygulamayı yeniden debug modunda başlatın. |

Başlangıç aşamasında hata mesajlarını dikkatle okumak önemlidir. Flutter araçları çoğu zaman hatanın nedeni hakkında yönlendirici bilgi verir.

---

## Mini Uygulama: Kişisel Karşılama Ekranı

Şimdi ilk uygulamayı küçük bir kişisel karşılama ekranına dönüştürelim. `body` bölümünü aşağıdaki gibi güncelleyin:

```dart
body: const Center(
  child: Column(
    mainAxisSize: MainAxisSize.min,
    children: [
      Text(
        'Merhaba Flutter!',
        style: TextStyle(fontSize: 28),
      ),
      SizedBox(height: 12),
      Text(
        'Bu benim ilk mobil uygulama ekranım.',
        style: TextStyle(fontSize: 18),
      ),
    ],
  ),
),
```

Bu güncellemede üç yeni kavram görülür:

| Widget | Görevi |
|---|---|
| `Column` | Çocuk widget'ları dikey olarak sıralar. |
| `SizedBox` | İki widget arasında boşluk oluşturur. |
| `mainAxisSize: MainAxisSize.min` | Column'un yalnızca ihtiyaç duyduğu kadar yer kaplamasını sağlar. |

Bu örnek hâlâ state management içermemektedir. Yalnızca statik bir arayüz düzenlemesi yapılmıştır.

---

## Bölüm Sonu Mini Özet

Bu bölümde Flutter ekosistemine giriş yapıldı ve ilk uygulama oluşturuldu. Flutter'ın Dart diliyle çalışan, widget tabanlı ve çoklu platform hedefleyen bir geliştirme teknolojisi olduğu görüldü. `flutter doctor`, `flutter create`, `flutter run` gibi temel komutlar tanıtıldı. `main.dart` dosyasının uygulama başlangıç noktası olduğu açıklandı. İlk uygulama üzerinden `MaterialApp`, `Scaffold`, `AppBar`, `Center`, `Column` ve `Text` gibi temel widget'lar incelendi.

Bu bölümün en önemli kazanımı, Flutter'da arayüzün widget ağacı olarak düşünülmesidir. Bu düşünme biçimi, ilerleyen bölümlerde layout, navigasyon, form, veri yönetimi ve test konularını anlamayı kolaylaştıracaktır.

---

## Laboratuvar Görevi: İlk Flutter Ekranımı Oluşturuyorum

### Amaç

Bu laboratuvar görevinin amacı, öğrencinin yeni bir Flutter projesi oluşturması, `main.dart` dosyasını düzenlemesi ve basit bir kişisel karşılama ekranı hazırlamasıdır.

### Görev Adımları

1. `ilk_flutter_laboratuvar` adlı yeni bir Flutter projesi oluşturun.
2. Projeyi VS Code ile açın.
3. `lib/main.dart` dosyasındaki varsayılan kodu sadeleştirin.
4. Uygulama başlığını kendi belirlediğiniz bir başlıkla değiştirin.
5. Ekranın ortasında en az iki satırlık bir karşılama metni gösterin.
6. `Column`, `Text` ve `SizedBox` widget'larını kullanın.
7. Uygulamayı en az bir hedef cihazda veya Chrome üzerinde çalıştırın.
8. Ekran çıktısı alın ve dosya adını `bolum01_ilk_uygulama.png` olarak kaydedin.
9. Kısa bir gözlem notu yazın: "Bu uygulamada hangi widget ne işe yaradı?"

### Beklenen Çıktı

Öğrencinin ekranında üst başlık çubuğu bulunan ve orta bölümde kişisel karşılama metni gösteren basit bir Flutter uygulaması çalışmalıdır.

### Teslim Edilecekler

- `lib/main.dart` dosyası
- Uygulama ekran görüntüsü
- 5-8 cümlelik kısa gözlem notu

---

## Değerlendirme Rubriği

| Ölçüt | Açıklama | Puan |
|---|---|---:|
| Proje oluşturma | Flutter projesi doğru adla oluşturulmuş ve çalıştırılmıştır. | 15 |
| Kod düzeni | `main.dart` dosyası okunabilir, düzenli ve gereksiz şablon kodlardan arındırılmıştır. | 15 |
| Widget kullanımı | `MaterialApp`, `Scaffold`, `AppBar`, `Center` veya `Column`, `Text`, `SizedBox` gibi temel widget'lar doğru kullanılmıştır. | 25 |
| Görsel çıktı | Uygulama ekranı beklenen şekilde çalışmakta ve ekran görüntüsü alınmıştır. | 15 |
| Açıklama notu | Öğrenci kullandığı widget'ların görevini kısa ve doğru biçimde açıklamıştır. | 20 |
| Dosya teslim düzeni | Kod, ekran çıktısı ve gözlem notu düzenli biçimde teslim edilmiştir. | 10 |
| **Toplam** |  | **100** |

---

## Kontrol Soruları

1. Flutter'da `main()` fonksiyonunun görevi nedir?
2. `runApp()` fonksiyonu ne işe yarar?
3. `MaterialApp` ve `Scaffold` arasındaki fark nedir?
4. `Center` widget'ı hangi amaçla kullanılır?
5. `Column` ile `Row` arasında temel fark nedir?
6. Hot reload hangi tür geliştirme durumlarında yararlıdır?
7. `flutter doctor` komutu neden önemlidir?

---

## Sonraki Bölüme Hazırlık

Sonraki bölümde Dart programlama dilinin temel sözdizimi, değişkenler, veri tipleri, fonksiyonlar ve kontrol yapıları ele alınacaktır. Flutter geliştirme sürecinde Dart bilgisi yalnızca kod yazmak için değil, widget yapısını doğru anlamak için de gereklidir. Bu nedenle sonraki bölüme geçmeden önce bu bölümde oluşturulan ilk uygulamanın `main.dart` dosyasını birkaç kez değiştirerek hot reload davranışını gözlemlemek faydalı olacaktır.
