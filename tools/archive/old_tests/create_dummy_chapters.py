import os
from pathlib import Path

project_root = Path("book_projects/dummy-kitap")

chapters = [
    ("bolum-01", "Giriş ve Temel Kavramlar", "Java programlama diline giriş, temel sözdizimi, değişkenler ve veri tipleri hakkında temel bilgiler."),
    ("bolum-02", "Kontrol Yapıları", "if-else, switch-case gibi karar yapıları ve program akış kontrolü."),
    ("bolum-03", "Döngüler", "for, while, do-while döngüleri ve döngü kontrol ifadeleri."),
    ("bolum-04", "Metotlar ve Fonksiyonlar", "Metot tanımlama, parametre geçişi, geri dönüş değerleri ve overloading."),
    ("bolum-05", "Diziler ve Koleksiyonlar", "Tek boyutlu ve çok boyutlu diziler, ArrayList, HashMap gibi koleksiyonlar."),
    ("bolum-06", "Nesne Yönelimli Programlama", "Sınıflar, nesneler, constructor'lar, encapsulation ve access modifiers."),
    ("bolum-07", "Kalıtım ve Polimorfizm", "Inheritance, super anahtarı, method overriding ve polymorphism."),
    ("bolum-08", "Arayüzler ve Soyut Sınıflar", "Interface ve abstract class farkları, default ve static metotlar."),
    ("bolum-09", "Hata Yönetimi", "try-catch-finally, throw, throws, özel exception sınıfları."),
    ("bolum-10", "Dosya İşlemleri ve I/O", "FileReader, FileWriter, BufferedReader, BufferedWriter ve NIO paketi."),
]

for chapter_id, title, description in chapters:
    ch_dir = project_root / "chapters" / chapter_id
    seed_dir = ch_dir / "seed"
    outline_dir = ch_dir / "outline_versions"
    draft_dir = ch_dir / "draft_versions"
    approved_dir = ch_dir / "approved"

    # Create directories
    seed_dir.mkdir(parents=True, exist_ok=True)
    outline_dir.mkdir(parents=True, exist_ok=True)
    draft_dir.mkdir(parents=True, exist_ok=True)
    approved_dir.mkdir(parents=True, exist_ok=True)

    # Seed file
    seed_content = f"""chapter_id: {chapter_id}
purpose: '{description}'
target_reader_state: 'Temel programlama kavramlarını öğrenmeye yeni başlayan öğrenci'
learning_outcomes:
- Bu bölümün temel kavramlarını anlama
- Pratik örneklerle pekiştirme
prerequisites: []
mandatory_concepts:
- Temel programlama mantığı
required_examples: []
required_code_items: []
intentional_mismatch_examples: []
required_diagrams: []
required_assets: []
mini_application: ''
common_mistakes: []
exercises:
- Bölüm sonu alıştırma sorusu
lab_task: ''
out_of_scope: []
author_notes: '{title} - Dummy kitap test bölümü'
"""
    (seed_dir / "seed_v001.yaml").write_text(seed_content, encoding="utf-8")

    # Draft/approved content
    ch_num = chapter_id.split("-")[1]
    dummy_md = f"""# Bölüm {int(ch_num)}: {title}

## Giriş

Bu bölümde **{title.lower()}** konusunu detaylı olarak inceleyeceğiz. {description}

## Öğrenme Hedefleri

Bu bölümü tamamladığınızda:
- {title} ile ilgili temel kavramları anlayacaksınız
- Pratik örnekler üzerinde çalışabileceksiniz
- Gerçek dünya problemlerine uygulayabileceksiniz

## Temel Kavramlar

### Kavram 1: Tanımlar

{title} konusu, Java programlamanın önemli yapı taşlarından biridir. Bu kavramı anlamak için:

1. Önce temel sözdizimini öğrenmelisiniz
2. Ardından pratik örneklerle pekiştirmelisiniz
3. Son olarak karmaşık senaryolarda kullanmalısınız

```java
public class Ornek {{
    public static void main(String[] args) {{
        // {title} örneği
        System.out.println("{title} konusuna hoş geldiniz!");
        
        int sayi = 10;
        if (sayi > 5) {{
            System.out.println("Sayı 5'ten büyüktür: " + sayi);
        }}
    }}
}}
```

## Detaylı İnceleme

{description} Bu bölüm boyunca teorik bilgileri örneklerle destekleyerek ilerleyeceğiz.

```mermaid
flowchart TD
    A[Başlangıç] --> B{{Veri Girişi}}
    B --> C{{İşlem}}
    C --> D{{Sonuç}}
    D --> E[Bitir]
```

### Önemli Noktalar

- **Sözdizimi Kuralları**: Doğru yazım kurallarına dikkat edin
- **Yaygın Hatalar**: Sık yapılan hataları öğrenin
- **Best Practices**: En iyi uygulama örneklerini takip edin

## Örnek Uygulama

```java
public class Uygulama {{
    private String mesaj;
    
    public Uygulama(String mesaj) {{
        this.mesaj = mesaj;
    }}
    
    public void goster() {{
        System.out.println("Mesaj: " + mesaj);
    }}
    
    public static void main(String[] args) {{
        Uygulama u = new Uygulama("Test mesajı");
        u.goster();
    }}
}}
```

## Bölüm Özeti

Bu bölümde **{title}** konusunu ele aldık. Aşağıdaki kazanımları elde ettiniz:

| Kazanım | Açıklama |
|---------|----------|
| Temel Bilgi | {title} temel kavramları |
| Kodlama | Java ile uygulama örnekleri |
| Problem Çözme | Gerçek dünya senaryoları |

## Alıştırmalar

1. Yukarıdaki kod örneğini çalıştırarak sonucu gözlemleyin
2. Kendi örneğinizi yazarak pekiştirme yapın
3. Hata durumlarını test edin

---

**Sonraki Bölüm**: Bir sonraki bölümde yeni bir konuya geçiş yapacağız.
"""
    (draft_dir / "v001.md").write_text(dummy_md, encoding="utf-8")
    (approved_dir / f"{chapter_id}_v001.md").write_text(dummy_md, encoding="utf-8")

    # Outline file
    outline_md = f"""# {title} - Taslak

## Amaç
{description}

## Öğrenme Çıktıları
- Temel kavramları anlama
- Kod yazabilme
- Problem çözebilme

## Bölüm Yapısı
1. Giriş
2. Temel Kavramlar
3. Detaylı İnceleme
4. Örnek Uygulama
5. Bölüm Özeti
6. Alıştırmalar
"""
    (outline_dir / "v001.md").write_text(outline_md, encoding="utf-8")

print("10 bölüm başarıyla oluşturuldu!")
for i, (cid, title, _) in enumerate(chapters):
    print(f"  {i+1}. {cid}: {title}")
