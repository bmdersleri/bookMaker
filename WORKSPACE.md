# WORKSPACE

Bu dosya mevcut Windows/PowerShell calisma ortaminda kullanilabilecek araclari, sistem imkanlarini ve dikkat edilmesi gereken kisitlari listeler.

## Sistem

```text
Calisma dizini: D:\bookMaker
Isletim sistemi: Windows
Shell: PowerShell 7.x
PowerShell surumu: 7.6.1
Timezone: Europe/Istanbul
```

## Repo

```text
GitHub: https://github.com/bmdersleri/bookMaker
Remote: origin https://github.com/bmdersleri/bookMaker.git
Branch: main
```

Git komutlarinda su uyari gorulebilir:

```text
warning: unable to access 'C:\Users\ismai/.config/git/ignore': Permission denied
```

Bu uyari temel Git komutlarini su ana kadar engellemedi.

## Dosya Kodlamasi

Tum yeni ve degistirilen dosyalarda UTF-8 kullanilmalidir.

PowerShell ile dosya yazimi gerekirse UTF-8 acikca korunmalidir. Manuel kod duzenlemelerinde `apply_patch` tercih edilmelidir.

## Sandbox ve Izin Notlari

- `D:\bookMaker` icinde okuma/yazma yapilabilir.
- Bazi sistem, Winget, Scoop ve AppData yollarina sandbox icinden dogrudan erisim engellenebilir.
- Kurulum, ag erisimi veya sistem klasoru erisimi gerektiren komutlarda yukseltme izni gerekebilir.
- PATH kurulumdan sonra guncellense bile mevcut Codex oturumu yeni PATH'i otomatik miras almayabilir.
- Bu durumda araclar tam executable yolu ile calistirilabilir.

## Ana Runtime ve Gelistirme Araclari

```text
Python: 3.14.0
Node.js: v24.11.1
npm: 11.13.0
Java: 17.0.10
javac: 17.0.10
Git: 2.44.0.1
GitHub CLI: mevcut
PowerShell: 7.6.1
SQLite CLI: 3.51.3
```

## Arama ve Inceleme

```text
rg: mevcut
rga: ripgrep-all 0.10.9
fd: 10.4.2
fzf: mevcut
```

Notlar:

- `rg` normalde calisiyor.
- `rga` DOCX/PDF/EPUB/arsiv gibi dosyalarda arama icin kullanilabilir.
- `fd` sistemde kurulu, ancak sandbox icinde dogrudan calismayabilir.
- `rga` varsayilan kullanici config/cache konumlarina erismeye calisirken sandbox icinde `Could not parse config / Erisim engellendi` hatasi verebilir.
- Bu repo icin `.rga-config.json` eklendi ve cache kapatildi. Sandbox icinde `rga` su sekilde calistirilmalidir:

```powershell
rga --rga-config-file=.\.rga-config.json "CODE_META" promptlar
```

`fd` tam yolu:

```text
C:\Users\ismai\AppData\Local\Microsoft\WinGet\Packages\sharkdp.fd_Microsoft.Winget.Source_8wekyb3d8bbwe\fd-v10.4.2-x86_64-pc-windows-msvc\fd.exe
```

## Veri ve Metin Isleme

```text
jq: kurulu
yq: kurulu
bat: kurulu olabilir; ayrica tekrar dogrulanmadi
7z: 26.00
tar: Windows sistem araci
curl: Windows sistem araci
```

Not:

- `jq` ve `yq` Winget yollarinda kurulu gorundu; sandbox icinden dogrudan calistirirken erisim engeli verebilir.

## Belge, Kitap ve Yayin Hatti

```text
pandoc: 3.9
calibre / ebook-convert: 9.8.0
qpdf: 12.3.2
pdftotext: 24.04.0
pdfinfo: mevcut
ExifTool: 13.57
```

Kullanim alanlari:

- `pandoc`: Markdown -> DOCX/HTML/PDF/EPUB donusumu.
- `ebook-convert`: EPUB ve e-kitap formatlari.
- `qpdf`: PDF dogrulama, birlestirme, bolme, yapisal kontrol.
- `pdftotext` / `pdfinfo`: PDF metin ve metadata inceleme.
- `ExifTool`: DOCX/PDF/gorsel metadata inceleme ve temizleme.

Tam yollar:

```text
C:\Program Files\Pandoc\pandoc.exe
C:\Program Files\Calibre2\ebook-convert.exe
C:\Program Files\qpdf 12.3.2\bin\qpdf.exe
C:\Users\ismai\AppData\Local\Programs\ExifTool\ExifTool.exe
```

## Diyagram ve Gorsel Isleme

```text
mmdc: 11.12.0
ImageMagick / magick: 7.1.2-21
```

Kullanim alanlari:

- `mmdc`: Mermaid diyagramlarini PNG/SVG/PDF olarak render etmek.
- `magick`: QR, gorsel boyutlandirma, format donusumu, gorsel kalite kontrol.

Tam yollar:

```text
C:\Users\ismai\AppData\Roaming\npm\mmdc.ps1
C:\Program Files\ImageMagick-7.1.2-Q16-HDRI\magick.exe
```

## Kalite, Lint ve Kontrol Araclari

```text
tokei: 12.1.2
ruff: 0.15.12
markdownlint-cli2: 0.22.1
Vale: 3.14.1
lychee: 0.23.0
pre-commit: 4.6.0
actionlint: 1.7.12
hyperfine: 1.20.0
```

Kullanim alanlari:

- `tokei`: kod/metin istatistikleri.
- `ruff`: Python lint/format kalite kontrolu.
- `markdownlint-cli2`: Markdown bicim ve baslik kontrolu.
- `Vale`: akademik dil, terminoloji ve stil kontrolu.
- `lychee`: link ve URL dogrulama.
- `pre-commit`: commit oncesi otomatik kalite kapilari.
- `actionlint`: GitHub Actions workflow dosyalarini denetleme.
- `hyperfine`: komut performans benchmarklari.

Tam yollar:

```text
C:\Users\ismai\AppData\Local\Microsoft\WinGet\Packages\XAMPPRocky.Tokei_Microsoft.Winget.Source_8wekyb3d8bbwe\tokei.exe
C:\Users\ismai\AppData\Roaming\Python\Python314\Scripts\ruff.exe
C:\Users\ismai\AppData\Roaming\npm\markdownlint-cli2.ps1
C:\Users\ismai\AppData\Local\Microsoft\WinGet\Packages\errata-ai.Vale_Microsoft.Winget.Source_8wekyb3d8bbwe\vale.exe
C:\Users\ismai\AppData\Local\Microsoft\WinGet\Packages\lycheeverse.lychee_Microsoft.Winget.Source_8wekyb3d8bbwe\lychee.exe
C:\Users\ismai\.local\bin\pre-commit.exe
```

## Python Proje ve Paket Araclari

```text
uv: 0.11.8
ruff: 0.15.12
pre-commit: 4.6.0
playwright: 1.59.0
```

`uv` tam yolu:

```text
C:\Users\ismai\AppData\Local\Microsoft\WinGet\Packages\astral-sh.uv_Microsoft.Winget.Source_8wekyb3d8bbwe\uv.exe
C:\Users\ismai\AppData\Roaming\uv\tools\playwright\Scripts\playwright.exe
C:\Users\ismai\AppData\Roaming\uv\tools\playwright\Scripts\python.exe
```

Playwright Chromium browser bileseni kuruldu ve headless render smoke testi basarili oldu.

## SQLite

```text
sqlite3: 3.51.3
```

Kullanim alani:

- Manifest, indeks, cache, kitap varlik katalogu veya analiz sonuclari icin lokal veritabani.

Kurulum:

- Scoop ile `sqlite` paketi kuruldu.
- `sqlite3` shim'i olusturuldu.

## Otomasyon ve Site Araclari

```text
just: 1.50.0
mkdocs: 1.6.1
mkdocs-material: 9.7.6
```

Kullanim alanlari:

- `just`: ortak proje komutlari icin `justfile`.
- `mkdocs` + `mkdocs-material`: kitap/dokumantasyon icin HTML site uretimi.

Tam yollar:

```text
C:\Users\ismai\scoop\shims\just.exe
C:\Users\ismai\.local\bin\mkdocs.exe
C:\Users\ismai\AppData\Roaming\uv\tools\mkdocs\Scripts\python.exe
```

`mkdocs-material` import dogrulamasi:

```text
9.7.6
```

## Git ve Buyuk Dosya Yonetimi

```text
git-lfs: 3.4.1
```

Kullanim alani:

- DOCX, PDF, gorsel, QR, kapak, veri seti gibi buyuk veya binary dosyalari GitHub deposunda daha saglikli yonetmek.

## Paket Yoneticileri

```text
scoop: kurulu
winget: kurulu
npm: 11.13.0
uv: 0.11.8
```

Kullanilan kurulumlar:

- Winget ile: `tokei`, `ImageMagick`, `QPDF`, `Vale`, `lychee`, `uv`, `calibre`, `ExifTool`
- npm global ile: `markdownlint-cli2`
- Scoop ile: `just`
- uv tool ile: `pre-commit`, `mkdocs --with mkdocs-material`

## Sample Inceleme Icin Faydalı Komutlar

Basliklari listeleme:

```powershell
rg -n "^# (Bolum|Ek)" sample\Java_Temelleri_Kompakt_Birlesik_cift_qr_gomulu.md
```

Kod kimliklerini sayma:

```powershell
([regex]::Matches((Get-Content sample\Java_Temelleri_Kompakt_Birlesik_cift_qr_gomulu.md -Raw), '\*\*Kod kimligi:\*\*')).Count
```

Markdown/DOCX icinde genel arama:

```powershell
rga "Kod kimligi|QR|Mermaid|Kaynaklar" sample
```

Tokei ile istatistik:

```powershell
& 'C:\Users\ismai\AppData\Local\Microsoft\WinGet\Packages\XAMPPRocky.Tokei_Microsoft.Winget.Source_8wekyb3d8bbwe\tokei.exe' sample
```

DOCX medya sayisi:

```powershell
Add-Type -AssemblyName System.IO.Compression.FileSystem
([System.IO.Compression.ZipFile]::OpenRead((Resolve-Path 'sample\Java_Temelleri_Kompakt_Birlesik_cift_qr_gomulu.docx')).Entries | Where-Object FullName -like 'word/media/*').Count
```
