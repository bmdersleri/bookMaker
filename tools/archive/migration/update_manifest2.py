"""GUI_MANIFEST.md - Kitap sihirbazi, versiyon takibi bolumleri ekle."""
import sys
sys.stdout.reconfigure(encoding='utf-8')

path = r'D:\bookMaker_Deepseek\GUI_MANIFEST.md'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

new_sections = """
---

## 9. Kitap Olusturma Sihirbazi (Genisletilmis)

### 9.1 Sihirbaz Adimlari

```
+------------------------------------------------------------------+
|  Kitap Olusturma Sihirbazi                              1/5      |
+------------------------------------------------------------------+
|  o ADIM 1 -> ● ADIM 2 -> o ADIM 3 -> o ADIM 4 -> o ADIM 5       |
+------------------------------------------------------------------+
```

#### ADIM 1: Proje Temelleri

- **Proje Adi** (teknik): [a-z0-9_-]+, benzersiz olmali
- **Kitap Adi (TR)**: Min 5, max 100 karakter
- **Kitap Adi (EN)**: Ingilizce alternatif baslik
- **Yazar**: Zorunlu alan
- **Dil**: Turkce / Ingilizce / ...

Onizleme: Olusturulacak dizin yapisi gosterilir:
```
book_projects/java-temelleri/
+-- chapters/    (27 bolum)
+-- build/       (ciktilar)
+-- kodlar/      (kod ornekleri)
+-- assets/      (resimler, diyagramlar)
```

Validasyon: Proje adi benzersiz olmali, dizin mevcut degilse olusturulur.

#### ADIM 2: LLM Destekli Bolum Planlama

Iki secenek:
1. **Bos baslangic**: Bolumler manuel eklenir
2. **LLM ile plan olustur**: Konu girilir, yapay zeka bolum plani onerir

LLM Plani Parametreleri:
- Ana Bolum Sayisi: [23]
- Ek Bolum Sayisi: [4]
- Proje tabanli ogrenme: ☑
- Kod ornekleri: ☑
- Bolum sonu alistirmalari: ☑
- Ileri duzey konular ayri: ☐

LLM Plani Onizlemesi (tablo):
| # | Baslik | Tur | Sure |
|---|--------|-----|------|
| 1 | Java'ya Giris ve Kurulum | core | 2s |
| 2 | Degiskenler ve Veri Tipleri | core | 3s |
| ... | ... | ... | ... |
| 23 | Bitirme Projesi | core | 4s |
| EK-A | Kurulum Kilavuzu | ek | 1s |

Duzenleme: Baslik, tur, sure ve siralama degistirilebilir.
Bolum ekle/sil butonlari.

#### ADIM 3: LLM Yapilandirmasi

- Saglayici secimi: DeepSeek / OpenAI / Anthropic / Ozel URL
- API Anahtari (maskeli giris)
- Model secimi
- Varsayilan ayarlar: Sicaklik (0.7), Max Token (4096), Timeout (120s), Max Retry (3)
- Baglanti Testi butonu: Yesil OK / Kirmizi hata mesaji

#### ADIM 4: Cikti Ayarlari

- Hedef Formatlar: DOCX ☑, PDF ☐, EPUB ☐, HTML ☐
- DOCX Ayarlari: Referans sablon, Pandoc filtresi, Icindekiler ☑, Kod renklendirme ☑
- Mermaid Ayarlari: Render motoru (mmdc), Cikti formati (PNG), Arkaplan (Beyaz)

#### ADIM 5: Onay ve Olusturma

Ozet:
- Kitap: Java'nin Temelleri (23 + 4 bolum)
- Yazar: Ismail Kirbas
- LLM: DeepSeek deepseek-v4-flash
- Cikti: DOCX

Olusturulacak dosyalar:
- book_profile.yaml
- book_manifest.yaml
- book_architecture.yaml
- pipeline_state.yaml
- llm_config.json
- chapters/ dizini ve alt dizinler
- build/ dizini

---

## 10. Mevcut Proje Uzerinde Degisiklikler

### 10.1 Degisiklik Turleri

| Degisiklik | Aciklama | Arayuz |
|-----------|----------|--------|
| **Bolum Ekleme** | Yeni bolum olusturma | + buton -> form -> manifest guncelle |
| **Bolum Silme** | Bolum kaldirma | cop buton -> onay modali |
| **Bolum Yeniden Adlandirma** | Baslik degistirme | kalem buton -> inline edit |
| **Bolum Siralama** | Surukle-birak ile yeniden sirala | drag handle |
| **Icerik Duzenleme** | Markdown editor | Goz -> Duzenle modu |
| **Kavram Guncelleme** | Bolum konseptleri | Pipeline -> Kavramlar alani |
| **Manuel Onay** | Editor onayi | Onayla butonu |
| **Versiyon Gecisi** | Eski versiyona donme | Versiyon paneli -> Geri al |

### 10.2 Degisiklik Akisi

```
Kullanici Degisiklik Yapar
        |
        v
+---------------------+
| Anlik Validasyon    | <- Hataliysa kirmizi outline + hata mesaji
+---------------------+
        |
        v
+---------------------+
| Onizleme (opsiyonel)| <- Sag panelde canli render
+---------------------+
        |
        v
+---------------------+
| Kaydet              | <- Manifest guncellenir
+---------------------+
        |
        v
+---------------------+
| Versiyon Olustur    | <- Otomatik yedek alinir
+---------------------+
        |
        v
+---------------------+
| Pipeline State      | <- Durum guncellenir
| Guncelle            |
+---------------------+
```

### 10.3 Toplu Islemler

| Islem | Aciklama | Arayuz |
|-------|----------|--------|
| **Toplu Pipeline** | Secili bolumleri sirayla isle | Checkbox + "Toplu Uret" |
| **Toplu Build** | Secili bolumleri DOCX yap | Checkbox + "Toplu Build" |
| **Toplu Onay** | Secili bolumleri onayla | Checkbox + "Toplu Onayla" |
| **Toplu Sifirla** | Secili bolumleri planned'a cek | Checkbox + "Sifirla" |

---

## 11. Versiyon Takip Sistemi

### 11.1 Versiyon Kapsami

| Duzey | Ne Versiyonlanir? | Versiyon Formati | Depolama |
|-------|-------------------|------------------|----------|
| **Kitap** | Manifest, mimari, profil | v1.0.0 (semver) | version_history/book_v{version}/ |
| **Bolum** | Tam metin, front matter | v{major}.{minor} | chapters/{id}/versions/v{m}.{n}.md |
| **Pipeline** | State degisiklikleri | Zaman damgasi | pipeline_state.yaml commit'leri |
| **Konfigurasyon** | LLM ayarlari | Zaman damgasi | llm_config.json yedekleri |

### 11.2 Versiyon Paneli Tasarimi

```
+------------------------------------------------------------------+
|  Versiyon Gecmisi: bolum-03                                      |
+------------------------------------------------------------------+
|  +------+---------------+---------------+-------------+----------+
|  | Ver  | Tarih         | Kelime        | Islem       | Aksiyon  |
|  +------+---------------+---------------+-------------+----------+
|  | v2.0 | 04.05.2026    | 2,594 OK      | Pipeline    | [G][D][I]|
|  |      | 18:54         | (guncel)      | (LLM uretim)|          |
|  +------+---------------+---------------+-------------+----------+
|  | v1.0 | 03.05.2026    | 1,743         | Manuel      | [G][D][I]|
|  |      | 12:30         |               | yazim       |          |
|  +------+---------------+---------------+-------------+----------+
|
|  G = Goruntule   D = Bu versiyona don   I = Indir
|
|  !! Dikkat: v1.0'a donmek mevcut degisiklikleri kaybettirir.
|              Mevcut surum otomatik yedeklenir.
+------------------------------------------------------------------+
```

### 11.3 Versiyon Karsilastirma (Diff)

Iki versiyon arasinda:
- Metrik tablosu: Kelime, Kod Blogu, Mermaid, Tablo, Bold, Zenginlik
- Degisim yuzdeleri ve yonleri (+/-)
- Metin farki (diff): Satir bazinda ekleme/cikarma gosterimi

### 11.4 Versiyon Islemleri

| Islem | Tetikleyici | Aciklama |
|-------|------------|----------|
| **Otomatik Kaydet** | Pipeline tamamlaninca | Yeni versiyon olusturulur |
| **Manuel Kaydet** | Kullanici "Kaydet" butonu | Yeni versiyon olusturulur |
| **Geri Alma** | Kullanici "Bu versiyona don" | Eski versiyon aktif olur, yeni yedeklenir |
| **Karsilastirma** | Kullanici 2 versiyon secer | Diff ve istatistik tablosu |
| **Disari Aktarma** | Kullanici "Indir" butonu | .md dosyasi indirilir |
| **Temizleme** | Otomatik (30 gun) | 30 gunden eski versiyonlar silinir (opsiyonel) |

### 11.5 Versiyon Depolama Yapisi

```
book_projects/java-temelleri/
+-- version_history/
|   +-- book_v1.0.0/
|   |   +-- book_profile.yaml
|   |   +-- book_manifest.yaml
|   |   +-- book_architecture.yaml
|   +-- book_v1.1.0/
|       +-- ...
|
+-- chapters/bolum-03/
    +-- versions/
    |   +-- v1.0.md          (manuel yazim)
    |   +-- v2.0.md          (LLM pipeline)
    |   +-- v2.1.md          (manuel duzeltme)
    |   +-- version_log.json (metadata)
    +-- approved/
        +-- bolum-03_v002.md (aktif versiyon)
```

### 11.6 version_log.json Formati

```json
{
  "chapter_id": "bolum-03",
  "current_version": "v2.1",
  "versions": [
    {
      "version": "v1.0",
      "created_at": "2026-05-03T12:30:00",
      "source": "manual",
      "words": 1743,
      "score": 28,
      "author": "Ismail KIRBAS",
      "notes": "Ilk manuel yazim"
    },
    {
      "version": "v2.0",
      "created_at": "2026-05-04T18:54:00",
      "source": "llm_pipeline",
      "words": 2594,
      "score": 100,
      "model": "deepseek-chat",
      "temperature": 0.7,
      "pipeline_elapsed_s": 152.3,
      "spec_words": 1518,
      "seed_words": 1562,
      "enrich_count": 6,
      "notes": "LLM pipeline ile tam otomatik uretim"
    },
    {
      "version": "v2.1",
      "created_at": "2026-05-04T20:15:00",
      "source": "manual_edit",
      "words": 2610,
      "score": 95,
      "author": "Ismail KIRBAS",
      "notes": "Giris paragrafi duzeltildi, 2 kod ornegi eklendi"
    }
  ]
}
```
"""

# Teknoloji Yigini oncesine ekle
old_marker = '\n---\n\n## 7. Teknoloji Yığını'
if old_marker in content:
    content = content.replace(old_marker, new_sections + old_marker)
    print("Kitap sihirbazi, proje degisiklikleri, versiyon takibi eklendi.")
else:
    print(f"HATA isaret bulunamadi!")

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"Toplam: {len(content)} karakter")

# Icerik haritasi
import re
sections = re.findall(r'^## (\d+\..*)$', content, re.MULTILINE)
print(f"\nGuncel Icerik Haritasi ({len(sections)} bolum):")
for s in sections:
    print(f"  {s}")
