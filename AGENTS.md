# AGENTS.md — OpenCode Project Rules

Bu dosya, OpenCode'un bu projede daha güvenli, verimli ve tutarlı çalışması için hazırlanmıştır.  
Amaç: Gereksiz bağlam tüketimini azaltmak, yanlış dosya değişikliklerini önlemek, test edilebilir küçük adımlarla ilerlemek ve özellikle Windows/WSL/PowerShell ortamında kararlı bir geliştirme akışı sağlamaktır.

---

## 1. Proje Bağlamı

Bu proje; kitap üretimi, ders materyali hazırlama, kod bloğu çıkarımı, kalite kontrol, Markdown/DOCX üretimi, Mermaid diyagramları, GitHub senkronizasyonu ve otomatik test süreçlerini destekleyen akademik/teknik bir üretim altyapısıdır.

Muhtemel proje türleri:

- BookMaker / BookFactory
- Flutter, Java, React, Python veya veri bilimi kitap projeleri
- Manifest tabanlı bölüm üretimi
- Markdown tabanlı akademik içerik üretimi
- Kod doğrulama ve test otomasyonu
- Pandoc / Mermaid / DOCX üretim hattı

Bu projede yapılan değişiklikler, yalnızca kodu değil; kitap çıktısı, kalite raporu, bölüm yapısı, test çıktısı ve dokümantasyon bütünlüğünü de etkileyebilir.

---

## 2. Genel Çalışma İlkesi

OpenCode önce anlamalı, sonra önermeli, sonra uygulamalıdır.

Varsayılan yaklaşım:

1. İlgili dosyaları incele.
2. Problemi veya hedefi netleştir.
3. En küçük güvenli değişikliği öner.
4. Gerekli değilse geniş refaktör yapma.
5. Değişiklikten sonra uygun test veya doğrulama komutunu çalıştır.
6. Sonuçları kısa, açık ve dosya bazlı raporla.

Geniş kapsamlı görevlerde önce plan üret:

- Mimari analiz
- Riskli dosyalar
- Önerilen adımlar
- Test stratejisi
- Geri dönüş planı

---

## 3. Güvenlik ve Sınırlar

Aşağıdaki işlemler açık kullanıcı onayı olmadan yapılmamalıdır:

- `git reset --hard`
- `git clean -fdx`
- `git push --force`
- Büyük klasör silme
- `.env`, API key, token, sertifika veya özel anahtar dosyalarını okuma/değiştirme
- Oluşturulmuş kalite raporlarını, build çıktılarını veya logları topluca silme
- Kitap bölümlerini tamamen yeniden yazma
- Çok sayıda dosyada otomatik toplu değişiklik yapma

Aşağıdaki dosya türleri hassas kabul edilir:

- `.env`
- `.env.*`
- `*.key`
- `*.pem`
- `*.pfx`
- `credentials*`
- `secrets*`
- `token*`
- `id_rsa*`
- `id_ed25519*`

Bu dosyaları okuma, özetleme veya düzenleme önerme.

---

## 4. Windows / PowerShell / WSL Kuralları

Kullanıcı Windows ortamında çalışıyor olabilir. Komut önerirken ortamı dikkate al.

Varsayılan öncelik:

1. WSL içinde çalışılıyorsa Bash komutları kullanılabilir.
2. Windows PowerShell kullanılıyorsa PowerShell uyumlu komutlar ver.
3. PowerShell komutlarında satır devamı için backtick kullanılabilir; ancak mümkünse tek satırlık komutlar tercih edilmelidir.
4. Türkçe karakterlerin bozulmaması için UTF-8 kodlama korunmalıdır.

PowerShell'de dosya yazarken tercih:

```powershell
Set-Content -Path "dosya.md" -Value $content -Encoding UTF8
```

Büyük metinler için burada-belge kullanımında dikkatli ol:

```powershell
@'
metin
'@ | Set-Content -Path "dosya.md" -Encoding UTF8
```

Kodlama sorunlarını kontrol etmek için:

```powershell
Select-String -Path .\*.md -Pattern "Ã|Ä|Å|�" -Recurse
```

---

## 5. Git Kullanım Kuralları

Değişiklik yapmadan önce:

```bash
git status --short
git branch --show-current
git log --oneline -5
```

Değişiklikten sonra:

```bash
git diff
git status --short
```

Commit öncesi mutlaka:

```bash
git diff --check
```

Commit önerilecekse mesaj kısa ve açıklayıcı olmalıdır:

```bash
git add <dosyalar>
git commit -m "Fix chapter validation mode handling"
```

Kullanıcı açıkça istemedikçe commit atma veya push yapma.

---

## 6. Python / uv / Test Kuralları

Bu proje Python tabanlıysa öncelik `uv` kullanımındadır.

Önerilen temel komutlar:

```bash
uv run pytest tests/ -q
uv run ruff check .
uv run python -m pytest tests/ -q
```

Dar kapsamlı değişikliklerde önce ilgili testi çalıştır:

```bash
uv run pytest tests/test_relevant_file.py -q
```

Ardından gerekiyorsa geniş test:

```bash
uv run pytest tests/ -q
```

Test başarısız olursa:

1. İlk hata kaynağını bul.
2. Stack trace'i özetle.
3. Rastgele refaktör yapma.
4. En küçük düzeltmeyi öner.
5. Aynı testi tekrar çalıştır.

---

## 7. BookMaker / BookFactory Özel Kuralları

Bu projede aşağıdaki kavramlar önemli olabilir:

- `book_manifest.yaml`
- `chapter_manifest.yaml`
- `CODE_META`
- `SCREENSHOT_META`
- `book_projects/`
- `chapters/`
- `content/draft.md`
- `content/final.md`
- `logs/reviews/`
- `book_quality_report.json`
- `chapter validator`
- `validation modes`
- `profile-aware validation`
- Markdown kalite kontrolü
- Kod bloğu çıkarımı ve testleri
- Mermaid diyagram üretimi
- Pandoc DOCX üretimi

Kalite kontrol komutları proje yapısına göre değişebilir. Önce mevcut README, pyproject veya docs dosyalarını incele.

Muhtemel komutlar:

```bash
uv run bookmaker check book book_projects/flutter-ile-mobil-uygulama-gelistirme --json --verbose
```

Kod bloğu çıkarımı için muhtemel komut örneği:

```bash
uv run python -m tools.code.extract_code_blocks --package-root . --out-dir build/code --manifest build/code_manifest.json --yaml-manifest build/code_manifest.yaml --chapters-dir chapters
```

Kod meta doğrulama için muhtemel komut örneği:

```bash
uv run python -m tools.code.validate_code_meta build/code_manifest.json --package-root .
```

Kod testleri için muhtemel komut örneği:

```bash
uv run python -m tools.code.run_code_tests --manifest build/code_manifest.json --package-root . --report-json build/test_reports/code_test_report.json --report-md build/test_reports/code_test_report.md
```

Bu komutları çalıştırmadan önce gerçek proje yollarını kontrol et.

---

## 8. Markdown ve Akademik İçerik Kuralları

Markdown kitap bölümlerinde:

- Tek bir ana H1 başlığı kullanılmalı.
- Bölüm başlık hiyerarşisi tutarlı olmalı.
- Türkçe karakterler korunmalı.
- Gereksiz İngilizce-Türkçe karışımı yapılmamalı.
- Kod bloklarında dil etiketi belirtilmeli.
- Mermaid diyagramları geçerli sözdizimiyle yazılmalı.
- Görsel/screenshot yer tutucuları sistematik olmalı.
- Callout kutuları varsa mevcut stil standardı korunmalı.

Kitap içeriğini düzenlerken:

1. Bölümün pedagojik bütünlüğünü koru.
2. Kod örneklerini çalışabilir tut.
3. Gereksiz uzun teorik ekleme yapma.
4. Terimleri tutarlı kullan.
5. Öğrenme çıktıları, özetler ve alıştırmalar varsa formatı bozma.

---

## 9. Flutter Kitabı Özel Kuralları

Flutter içeriklerinde:

- Flutter 3.24+ ve Dart 3.5+ varsay.
- Null-safety zorunludur.
- Deprecated API kullanma.
- `flutter_lints` uyumuna dikkat et.
- Widget, BuildContext, State, Route, Future, Stream gibi teknik terimleri tutarlı kullan.
- Kod örnekleri eğitim amaçlı, çalışabilir ve sade olmalıdır.
- Proje tabanlı ilerleyen yapılarda önceki bölüm kazanımlarını bozma.

---

## 10. Java Kitabı Özel Kuralları

Java içeriklerinde:

- Temel Java kitabında gereksiz ileri OOP detayı verme.
- OOP ayrı kitap konusu olarak ele alınabilir.
- Kod örnekleri `javac` ile derlenebilir olmalıdır.
- Swing, event handling ve JDBC örneklerinde açıklayıcı yorumlar kullanılmalıdır.
- Dosya adları ile public class adları uyumlu olmalıdır.

---

## 11. React / Web Kitabı Özel Kuralları

React içeriklerinde:

- Modern React yaklaşımı kullan.
- Functional components ve hooks varsayılan olsun.
- Eski class component yapısını yalnızca tarihsel/karşılaştırmalı anlat.
- Kod örnekleri Vite tabanlı projelere uyumlu olmalıdır.
- Gereksiz bağımlılık ekleme.
- Erişilebilirlik ve responsive tasarım notlarını koru.

---

## 12. Kod Değiştirme Stratejisi

Kod düzenlerken:

- İlgili dosya dışında değişiklik yapma.
- Büyük dosyaları komple yeniden yazma.
- Önce mevcut fonksiyonları ve testleri incele.
- Geriye uyumluluğu koru.
- Yeni davranış ekleniyorsa test ekle.
- Test eklenemiyorsa nedenini belirt.
- Hata mesajlarını kullanıcı dostu yap.
- CLI davranışını değiştirirken README veya dokümantasyonu güncelle.

---

## 13. Hata Ayıklama Yaklaşımı

Bir hata logu verildiğinde:

1. En üstteki belirtiyi değil, kök nedeni ara.
2. Hangi dosya/satır etkileniyor belirt.
3. Tekrarlanabilir minimal senaryo çıkar.
4. En küçük düzeltmeyi öner.
5. Düzeltme sonrası çalıştırılacak komutu ver.

Cevap formatı:

```text
Bulgu:
- ...

Muhtemel neden:
- ...

Önerilen düzeltme:
- ...

Etkilenecek dosyalar:
- ...

Doğrulama komutu:
- ...
```

---

## 14. OpenCode Kullanım Akışı

Küçük görevlerde:

```text
Inspect the relevant file, propose the smallest fix, then apply it.
```

Büyük görevlerde:

```text
Analyze first. Do not edit files yet. Produce a step-by-step plan with risks and test strategy.
```

Refaktörlerde:

```text
Refactor only the relevant function or module. Preserve public behavior. Add focused tests.
```

Test hatalarında:

```text
Read the failing test and implementation. Find the root cause. Do not rewrite unrelated code.
```

Dokümantasyonda:

```text
Update only the requested section. Preserve existing terminology and structure.
```

---

## 15. Model Kullanımı

Yerel veya uzak Ollama modeli kullanılıyorsa:

- Küçük düzeltmelerde yerel model yeterli olabilir.
- Büyük mimari değişikliklerde güçlü model tercih edilmelidir.
- Uzun dosyalarda bağlamı daralt.
- Modelden tüm projeyi birden analiz etmesini isteme.
- Görevi dosya, modül veya test bazında sınırla.

Tailscale üzerinden uzak Ollama kullanılıyorsa endpoint örneği:

```text
http://100.74.65.9:11434/v1
```

API anahtarlarını veya gizli yapılandırmaları dosyalara yazma.

---

## 16. Önerilen Özel OpenCode Komutları

Projede şu dizin oluşturulabilir:

```text
.opencode/commands/
```

Önerilen komutlar:

```text
/status
/review
/test
/quality
/commit-check
```

Bu komutlar için ayrı Markdown dosyaları oluşturulabilir.

---

## 17. Kalite Raporlama Formatı

Değişiklik sonrası özet şu formatta verilmelidir:

```text
Yapılanlar:
- ...

Değişen dosyalar:
- ...

Çalıştırılan kontroller:
- ...

Sonuç:
- ...

Kalan riskler:
- ...
```

Test çalıştırılamadıysa açıkça belirt:

```text
Test çalıştırılmadı.
Neden: ...
Önerilen komut: ...
```

---

## 18. Kaçınılması Gereken Promptlar

Aşağıdaki türden geniş ve belirsiz görevler risklidir:

```text
Fix everything.
Refactor the whole project.
Make this production-ready.
Improve all files.
Clean the repository.
```

Bunların yerine dar kapsamlı görevler tercih edilmelidir:

```text
Inspect the chapter validator and identify why profile-specific validation modes fail.
```

```text
Update only the README section about the code validation pipeline.
```

```text
Fix the failing test in tests/test_chapter_validator_profile_modes.py.
```

---

## 19. Varsayılan Davranış Özeti

OpenCode bu projede şu şekilde davranmalıdır:

- Önce incele.
- Sonra planla.
- Küçük değişiklik yap.
- Test et.
- Diff'i kontrol et.
- Riskleri raporla.
- Kullanıcı istemedikçe commit/push yapma.
- Gizli dosyalara dokunma.
- UTF-8 ve Türkçe karakterleri koru.
- Kitap üretim hattının bütünlüğünü bozma.

---

## 20. Kısa Komut Hatırlatıcı

```bash
git status --short
git diff
git diff --check
uv run pytest tests/ -q
uv run ruff check .
```

Kalite kontrol örneği:

```bash
uv run bookmaker check book book_projects/flutter-ile-mobil-uygulama-gelistirme --json --verbose
```

---

Bu dosya proje kök dizininde tutulmalı ve mümkünse Git deposuna eklenmelidir.
