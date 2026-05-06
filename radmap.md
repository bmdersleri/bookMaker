# FAZ 5 Studio GUI Roadmap

Bu dosya, Studio GUI geliştirmesine başlamadan önce uygulanacak planı tanımlar.
Test projesi olarak aşağıdaki Flutter kitabı kullanılacaktır:

```text
book_projects/flutter-ile-mobil-uygulama-gelistirme
```

## Başlangıç Durumu

Mevcut FAZ 5 altyapısı:

- Studio FastAPI uygulaması: `src/bookmaker/studio/app.py`
- Frontend template: `src/bookmaker/studio/templates/index.html`
- Frontend davranışları: `src/bookmaker/studio/static/app.js`
- Stil dosyası: `src/bookmaker/studio/static/styles.css`
- Servisler:
  - `book_service.py`
  - `chapter_service.py`
  - `prompt_service.py`
  - `pipeline_service.py`
  - `generation_service.py`
  - `observer_service.py`
  - `quality_service.py`
  - `build_service.py`
  - `export_service.py`
  - `manifest_service.py` facade olarak

Son tamamlanan FAZ 5 adımı:

- Studio proje seçici `book_manifest.yaml` tabanlı hale getirildi.
- Studio wizard yeni kitap oluştururken project-based workspace üretiyor.
- Legacy `book_profile.yaml`, `book_architecture.yaml`, `approved/`, `draft_versions/`, `seed/`, `outline_versions/` üretimi yeni wizard akışından kaldırıldı.

## Ana Hedef

Studio GUI, Flutter kitabını gerçek test projesi olarak kullanarak aşağıdaki işleri ergonomik şekilde yapabilmeli:

1. Kitap ve bölüm durumunu güvenilir göstermek.
2. Bölüm içeriklerini görüntülemek, kalite kontrolünü çalıştırmak ve raporları göstermek.
3. Prompt dosyalarını GUI üzerinden düzenlemek.
4. Project-based dosya yollarıyla uyumlu build/export/quality akışlarını yönetmek.
5. Pipeline/job durumunu okunabilir, iptal edilebilir ve izlenebilir hale getirmek.
6. Flutter kitap validasyonunu `100/pass` seviyesinde korumak.

## Temel İlkeler

- Flutter kitabı gerçek veri seti olarak kullanılacak; fixture-only ilerlenmeyecek.
- GUI değişiklikleri servis sözleşmeleriyle birlikte test edilecek.
- Legacy path varsayımları azaltılacak; yeni kod `book_manifest.yaml`, `chapter_manifest.yaml`, `content/draft.md`, `content/final.md`, `logs/`, `exports/` yapısını temel alacak.
- Büyük tek seferlik UI yenilemesi yapılmayacak; küçük, doğrulanabilir adımlar tercih edilecek.
- Her adım sonunda en az odak testleri ve mümkünse tam kabul seti çalıştırılacak.

## Tespit Edilen Mevcut GUI Sorunları

### Navigasyon ve Sekmeler

- `index.html` içinde `build` ve `quality` tab içerikleri var, ancak üst sekme navigasyonunda yalnız `chapters`, `pipeline`, `config` görünüyor.
- `app.js` içinde `loadQualityTab()` ve build panel fonksiyonları var, fakat sekme geçiş akışı bunları tam görünür kılmıyor.
- Bazı UI metinleri Java odaklı kalmış:
  - Pipeline placeholder değerleri Java kavramları içeriyor.
  - Kod çıkarma açıklaması Java kod bloklarını vurguluyor.

### Wizard Uyumsuzlukları

- `index.html` wizard input id'leri ile `app.js` içinde beklenen id'ler tam uyumlu değil.
  - HTML: `wiz-language`, `wiz-audience`, `wiz-chapters`
  - JS bazı yerlerde: `wiz-lang`, `wiz-author`, `wiz-type`, `wiz-chapter-count`, `wiz-appendix-count`, `wiz-title-en`
- Wizard adım sayısı ve JS kontrolü uyumsuz:
  - HTML üç adımlı yapı gösteriyor.
  - JS bazı fonksiyonlarda beş adım varsayıyor.
- `openWizard()` varsayılan proje adını `java-...` olarak veriyor; Flutter test projesi bağlamında nötr veya profile-aware olmalı.

### Project-based Yol Uyumu

- `serve_output()` hâlâ `build/` altını temel alıyor.
- `jobs.py` generation çıktıları `build/generation` altında tutuluyor.
- Bazı build/export servisleri legacy path varsayımları taşıyor olabilir; adım adım doğrulanmalı.

### Görsel ve Kullanılabilirlik

- Arayüz işlevsel ama bazı paneller dağınık ve gizli.
- Aksiyon butonları metin ağırlıklı; ikon kullanımı tutarsız.
- Mobil ve dar ekran davranışı temel düzeyde.
- Flutter kitabı için önemli sinyaller görünür değil:
  - framework/profile
  - screenshot gereksinimi
  - CODE_META/test mode profili
  - bölüm bazlı kalite kararları

## Uygulama Fazları

### Aşama 1 - GUI Navigasyonunu Stabilize Et

Amaç: Mevcut gizli/yarım bağlı GUI panellerini güvenilir sekmelere dönüştürmek.

Yapılacaklar:

- Üst sekmelere `Kalite`, `Build/Export`, `Promptlar` ekle.
- `switchTab()` akışını her sekme için gerekli loader fonksiyonunu çağıracak şekilde düzenle.
- `build` ve `quality` panellerinin görünür/çalışır olmasını sağla.
- Bölüm seçici dropdownlarını Flutter kitabın 16 bölümünden doldur.
- Tab ve panel id'lerini tek sözleşmeye indir.

Test:

```powershell
$env:UV_CACHE_DIR='.\\.uv-cache'
uv run pytest tests/unit/test_studio_app.py -q --tb=short
uv run pytest tests/unit/test_studio_services.py -q --tb=short
```

Manuel doğrulama:

- Studio açıldığında Flutter kitabı seçili veya seçilebilir olmalı.
- Sekmeler arasında geçişte JS hatası olmamalı.
- Quality ve Build/Export panelleri görülebilmeli.

### Aşama 2 - Wizard UI Sözleşmesini Düzelt

Amaç: Wizard HTML, JS ve `wizard_service.create_book()` aynı veri sözleşmesini kullansın.

Yapılacaklar:

- Wizard input id'lerini tek sözleşmeye çek:
  - `wiz-project`
  - `wiz-title`
  - `wiz-author`
  - `wiz-language`
  - `wiz-book-type`
  - `wiz-chapter-count`
  - `wiz-appendix-count`
  - `wiz-chapters`
- JS tarafında üç adımlı wizard mantığını HTML ile uyumlu hale getir.
- Manuel bölüm listesi parser'ı ekle:
  - `alias`
  - opsiyonel `alias: Başlık`
- Varsayılan proje prefix'ini Java yerine nötr yap:
  - `book-...`
  - veya seçilen profile göre `flutter-...`
- Wizard özetinde oluşturulacak project-based dosyaları kısa ve doğru göster.

Test:

- `wizard_service.create_book()` testleri korunacak.
- Yeni GUI endpoint testi eklenecek:
  - `/api/book/create` ile geçerli payload project-based yapı üretir.

Manuel doğrulama:

- Wizard ile geçici bir test kitap oluşturulabilmeli.
- Yeni kitap `book_projects/<alias>` altında oluşmalı.
- Legacy dosyalar oluşmamalı.

### Aşama 3 - Flutter Kitap Dashboard Görünümü

Amaç: Flutter kitabının gerçek kalite/profil durumunu ilk ekranda okunur hale getirmek.

Yapılacaklar:

- Proje kartlarına şu alanları ekle:
  - kitap adı
  - alias
  - author
  - framework/profile
  - bölüm sayısı
- Ana dashboard istatistiklerine ekle:
  - profil/framework: `flutter`
  - screenshot policy
  - QR policy
  - code language: `dart`
- Bölüm tablosuna eklenebilecek alanlar:
  - alias/title ayrımı
  - final/draft var mı
  - kalite kararı
  - warning/error count
- `book_service.get_project_info()` gerekiyorsa bu alanları dönecek şekilde genişlet.

Test:

- `book_service.get_project_info()` Flutter manifestinden profile/framework bilgisi döndürür.
- `/api/project` response sözleşmesi test edilir.

Manuel doğrulama:

- Flutter kitabı seçildiğinde dashboard Dart/Flutter sinyallerini göstermeli.

### Aşama 4 - Prompt Editörü

Amaç: Mevcut `prompt_service` endpointleri GUI üzerinden kullanılabilir olsun.

Yapılacaklar:

- Yeni `Promptlar` sekmesi ekle.
- Varsayılan promptlar:
  - `prompts/default_chapter.md`
  - `prompts/default_review.md`
- Bölüm promptları:
  - `chapters/<alias>/prompt.md`
- Bölüm seçici ile prompt yükle/kaydet.
- Kaydetme sonrası toast + path bilgisi göster.
- Değişiklik yapılmış ama kaydedilmemiş prompt için basit dirty-state uyarısı ekle.

Test:

- `prompt_service` mevcut roundtrip testleri korunur.
- Studio API prompt endpointleri için test eklenir:
  - `GET /api/prompts/default/chapter`
  - `PUT /api/prompts/default/chapter`
  - `GET /api/prompts/chapter/{alias}`
  - `PUT /api/prompts/chapter/{alias}`

Manuel doğrulama:

- Flutter kitabının `giris` bölüm promptu GUI'de açılıp kaydedilebilmeli.

### Aşama 5 - Kalite Panelini Flutter Kitapla Güçlendir

Amaç: `bookmaker check book` sonuçlarına yakın bir Studio kalite görünümü sağlamak.

Yapılacaklar:

- Quality tab görünür ve otomatik yüklenir hale getir.
- Bölüm bazlı tablo:
  - alias
  - skor
  - karar
  - hata
  - uyarı
  - son rapor path
- Tek bölüm kontrol butonu `/api/check/{chapter_id}` ile modalda detay gösterir.
- Kitap düzeyi kontrol için yeni GUI aksiyonu değerlendir:
  - mevcut `quality_service` yeterliyse kullan
  - değilse `book_validator.validate_book()` servis adapter'ı ekle
- `logs/reviews/` altındaki raporların GUI'den okunması opsiyonel faz olarak ayrılabilir.

Test:

- Flutter kitap için kalite endpointleri hata vermemeli.
- `bookmaker check book ... --json --verbose` yine `100/pass` kalmalı.

Manuel doğrulama:

- Flutter kitabın 16 bölümü kalite tablosunda görülebilmeli.

### Aşama 6 - Build/Export Panelini Project-based Yapıya Taşı

Amaç: Export ve çıktı yolları yeni mimariyle uyumlu olsun.

Yapılacaklar:

- Build/Export tab görünür hale getir.
- `exports/md`, `exports/docx`, `exports/pdf` hedeflerini UI'da göster.
- `serve_output()` için yalnız `build/` değil, project-based `exports/` ve gerektiğinde `logs/` dosyalarını güvenli sunma stratejisi belirle.
- Kod çıkarma açıklamalarını Java yerine profile-aware hale getir:
  - Flutter/Dart için `dart`/`flutter`
  - Java için `java`
- `export_service` içinde legacy build path varsayımları ayrıca incelenecek.

Test:

- Export endpointleri en az hata durumlarında deterministik response dönmeli.
- Path traversal güvenliği korunmalı.

Manuel doğrulama:

- Flutter kitapta export paneli doğru hedef klasörleri göstermeli.

### Aşama 7 - Pipeline ve Job Worker Project-based Yol Uyumu

Amaç: Generation/job akışı `build/generation` yerine project-based runtime yapıya hizalansın.

Yapılacaklar:

- `src/bookmaker/studio/jobs.py` incelenecek.
- Üretilen taslak çıktı hedefi:
  - `chapters/<alias>/content/draft.md`
- Onaylı/final hedef:
  - `chapters/<alias>/content/final.md`
- Prompt/log çıktıları:
  - `logs/production/`
  - `logs/errors/`
  - `logs/reviews/`
- Job progress UI sadeleştirilecek:
  - queued
  - running
  - done
  - error
  - cancelled
- Polling interval ve cancel davranışı doğrulanacak.

Test:

- Job create/list/cancel endpointleri test edilir.
- LLM gerektirmeyen dry-run veya mocked job testi eklenir.

Manuel doğrulama:

- LLM yapılandırılmamış durumda kullanıcıya net hata gösterilmeli.
- Job listesi boşken ve doluyken GUI düzgün görünmeli.

### Aşama 8 - Görsel Tasarım ve Ergonomi

Amaç: GUI'yi operasyonel bir Studio aracı gibi yoğun ama okunur hale getirmek.

Yapılacaklar:

- Kart içi kart kullanımını azalt.
- Sekme ve toolbar düzenini sıkılaştır.
- Butonlarda metin + uygun ikon kullan.
- Büyük metin alanlarında stabil yükseklik ve overflow davranışı sağla.
- Mobil/dar ekran için tablo yerine satır kartı veya yatay scroll stratejisi belirle.
- Renk paletini tek-hue görünümden uzaklaştır:
  - status renkleri anlamlı kalsın
  - primary/accent aşırı koyu tek tema hissi vermesin
- Türkçe karakter ve ASCII karışımı tutarlı hale getirilecek; mevcut dosya encoding'i korunacak.

Test:

- Playwright veya FastAPI TestClient ile index HTML smoke testi.
- Manuel ekran kontrolü:
  - desktop
  - dar viewport

### Aşama 9 - Flutter Kitap Kabul Senaryosu

Her GUI geliştirme turundan sonra Flutter kitap üzerinde şu senaryo çalıştırılacak:

1. Studio açılır.
2. Aktif proje olarak `flutter-ile-mobil-uygulama-gelistirme` seçilir.
3. Dashboard:
   - 16 bölüm görünür.
   - title doğru görünür.
   - profile/framework Flutter/Dart görünür.
4. Bölümler:
   - `giris`, `dart-temelleri`, `widget-mantigi` listede görünür.
   - Filtre/arama çalışır.
5. Promptlar:
   - `default_chapter.md` yüklenir.
   - `giris/prompt.md` yüklenir.
6. Kalite:
   - Bölüm kalite kontrolü hata vermeden döner.
   - Kitap check sonucu `100/pass` korunur.
7. Build/Export:
   - Panel açılır.
   - Hedef klasörler project-based `exports/` altında görünür.
8. Pipeline:
   - LLM yoksa net yapılandırma hatası gösterir.
   - LLM varsa job queue polling çalışır.

Komut kabul seti:

```powershell
$env:UV_CACHE_DIR='.\\.uv-cache'
uv run ruff check src/ tests/
uv run pytest tests/ -q --tb=short
uv run bookmaker check book book_projects/flutter-ile-mobil-uygulama-gelistirme --json --verbose
git diff --check
```

Beklenen:

```text
ruff PASS
pytest PASS
book check 100/pass
git diff --check PASS
```

## İlk Uygulama Paketi Önerisi

İlk implementation commit'i şu kapsamda tutulmalı:

```text
FAZ 5 GUI Step 1: Stabilize Studio tabs and Flutter project dashboard
```

Kapsam:

- Sekme navigasyonuna `Kalite`, `Build/Export`, `Promptlar` ekle.
- `switchTab()` loader akışını düzelt.
- Flutter kitap dashboard bilgilerini göster.
- Wizard id/adım uyuşmazlıklarını bozmadan not al; ayrı committe düzelt.
- Test:
  - `tests/unit/test_studio_app.py`
  - `tests/unit/test_studio_services.py`
  - tam kabul seti

Bu ilk paketten sonra ikinci commit:

```text
FAZ 5 GUI Step 2: Add prompt editor workflow
```

Üçüncü commit:

```text
FAZ 5 GUI Step 3: Align quality and build panels with project paths
```

## Riskler

- `app.js` içinde eski ve yeni wizard fonksiyonları karışmış görünüyor; doğrudan büyük düzenleme yapmak regresyon riski taşır.
- `index.html` içinde bazı paneller görünür değil ama JS fonksiyonları var; küçük bağlantı düzeltmeleri yeterli olabilir.
- `jobs.py` LLM ve dosya yazma akışı daha geniş risk taşır; GUI sekme/prompt/quality stabil olmadan job worker'a girilmemeli.
- Flutter kitabı gerçek proje olduğu için GUI testleri içerik dosyalarını yanlışlıkla değiştirmemeli; prompt edit testleri tmp_path ile yapılmalı.

## Commit ve Push Stratejisi

- Her aşama ayrı commit olmalı.
- `SESSION.md` güncellemesi ayrı commit olarak tutulmalı.
- Flutter kitap içerik dosyaları yalnız açıkça istenirse değiştirilmeli.
- Her commit öncesi:

```powershell
git status --short
git diff --check
```

- Her ana aşama sonrası:

```powershell
uv run ruff check src/ tests/
uv run pytest tests/ -q --tb=short
uv run bookmaker check book book_projects/flutter-ile-mobil-uygulama-gelistirme --json --verbose
```
