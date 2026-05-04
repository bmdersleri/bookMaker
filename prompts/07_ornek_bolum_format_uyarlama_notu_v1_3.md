<!-- v1.3 notu: Bu dosya v1.2 içeriği temel alınarak otomasyon uyumlu pakete dahil edilmiştir. Görünen numaralar üretim hattında atanır; kalıcı kimlikler manifestte tutulur. -->

# Java'nın Temelleri — Örnek Bölüm Formatı Uyarlama Notu v1.3

Bu belge, veri madenciliği kitabı için hazırlanmış örnek Markdown bölüm dosyasındaki yapının *Java'nın Temelleri* kitabına nasıl uyarlandığını açıklar.

---

## 1. Uyarlanan temel yapı

Örnek bölüm dosyasında görülen aşağıdaki yapılar Java kitabı için standart kabul edilmiştir:

- YAML front matter ile başlama,
- tek `# Bölüm X: ...` ana başlığı kullanma,
- alt başlıkları `## X.1`, `## X.2`, `## X.3` biçiminde numaralandırma,
- bölüm yol haritası ile açılış yapma,
- bölümün konumu ve pedagojik rolünü açıklama,
- öğrenme çıktıları ve ön bilgi varsayımlarını erken vermek,
- tablo, Mermaid diyagramı ve kod bloklarını Pandoc uyumlu biçimde kullanma,
- blockquote biçiminde dikkat, ipucu, derinlemesine ve sınav notu kutuları oluşturma,
- bölüm sonunda özet, terim sözlüğü, sorular, alıştırmalar, laboratuvar görevi, rubrik ve köprü ile kapanma.

---

## 2. Java kitabına özel uyarlamalar

Veri madenciliği örneğinde Python, pandas, scikit-learn ve veri analizi bağlamı kullanılırken Java kitabında şu uyarlamalar yapılacaktır:

| Örnek bölümdeki yapı | Java kitabındaki karşılık |
|---|---|
| Python kod blokları | Java kod blokları |
| `# Dosya: ...py` | `// Dosya: BolumXXOrnekYYAd.java` |
| Veri kümesi bağlamı | Konsol, dosya, koleksiyon, GUI veya JDBC uygulama bağlamı |
| Veri kalitesi tabloları | Kavram karşılaştırma, hata türleri, bileşen özellikleri tabloları |
| Pipeline/ön işleme akışı | Program akışı, kullanıcı girdisi, GUI olay akışı veya CRUD akışı |
| Veri analizi laboratuvarı | Java uygulama geliştirme laboratuvarı |

---

## 3. Java kod bloğu standardı

Java kodlarında dosya adı ile `public class` adı uyumlu olmalıdır.

```java
// Dosya: Bolum10Ornek01ToplamHesaplama.java
public class Bolum10Ornek01ToplamHesaplama {
    public static void main(String[] args) {
        int toplam = 0;

        for (int i = 1; i <= 10; i++) {
            toplam += i;
        }

        System.out.println("Toplam: " + toplam);
    }
}
```

---

## 4. Pedagojik kutu standardı

Java bölümlerinde örnek bölümdeki görsel/renkli kutu mantığı Markdown blockquote olarak korunacaktır:

```markdown
> **⚠️ Dikkat:** Dizi indeksleri 0'dan başlar. Son elemanın indeksi `length - 1` değeridir.
```

Bu yapı Pandoc/DOCX dönüşümünde daha sonra özel stillerle renklendirilebilir.

---

## 5. Bölüm sonu yapısı

Örnek bölümdeki geniş bölüm sonu yapısı Java kitabında da korunacaktır. Özellikle şu bileşenler ihmal edilmemelidir:

1. Bölüm özeti
2. Terim sözlüğü
3. Kendini değerlendirme soruları
4. Çoktan seçmeli sorular
5. Açık uçlu kavramsal sorular
6. Yanlış gerekçeyi bulma soruları
7. Kolay-orta-zor programlama alıştırmaları
8. Hata ayıklama egzersizi
9. Haftalık laboratuvar/proje görevi
10. 100 puanlık değerlendirme rubriği
11. İleri okuma ve kaynaklar
12. Bir sonraki bölüme köprü

---

## 6. Kalite kontrol notu

Örnek bölümde görülebilecek olası numaralandırma tekrarları Java kitabında düzeltilmelidir. Her bölüm üretiminden sonra şu kontroller yapılmalıdır:

- `## X.1`, `## X.2`, `## X.3` başlıkları ardışık mı?
- Aynı başlık numarası iki kez geçiyor mu?
- Kod blokları kapatılmış mı?
- Tablolar Markdown uyumlu mu?
- Bölüm sonu bileşenleri eksiksiz mi?
- Sonraki bölüme geçiş cümlesi var mı?


---

## v1.3 DOCX/PDF dönüşüm güvenlik kuralları

Pilot Bölüm 8 çıktısından sonra aşağıdaki kurallar tüm bölümler için zorunlu hâle getirilmiştir.

### Mermaid diyagramları

- Markdown içinde `mermaid` kod bloğu kullanılabilir; ancak final DOCX/PDF üretiminde ham `flowchart TD` metni görünmemelidir.
- Her Mermaid bloğu dönüşümden önce `mermaid_images/diagram_001.png`, `diagram_002.png` biçiminde PNG dosyasına dönüştürülmelidir.
- Diyagram başlığı metinde ayrıca verilmelidir: `**Diyagram X.Y:** ...`.
- Mermaid düğüm metinleri kısa tutulmalıdır; uzun açıklama diyagram altında paragraf olarak verilmelidir.
- DOCX/PDF çıktıda diyagram genişliği varsayılan olarak 12-13 cm aralığında kalmalıdır. Çok büyük diyagramlar sayfanın metin alanının %85'ini aşmamalıdır.

### Kod blokları

- Java kodlarında tek satır mümkünse 90 karakteri aşmamalıdır.
- Uzun `System.out.println(...)` satırları daha kısa mesajlarla veya satır kırımıyla yazılmalıdır.
- 40-60 satırı aşan büyük kod örnekleri parçalara bölünmeli; önce veri alma, sonra karar, sonra çıktı üretme gibi alt adımlarla açıklanmalıdır.
- Kod blokları tablo, blockquote veya liste içine gömülmemelidir.

### Numaralı listeler

- Görünür çıktı tutarlılığı için öğrenme çıktıları, görev adımları ve kural listelerinde açık numaralandırma tercih edilmelidir: `1.`, `2.`, `3.`.
- Markdown otomatik liste kolaylığı için tüm satırların `1.` ile başlatılması önerilmez.

### Bölüm sonu

- Final çıktıda `BÖLÜM SONU` yalnızca bir kez görünmelidir.
- Dönüşüm filtresi bu etiketi otomatik üretiyorsa Markdown sonunda elle yazılan tekrarlar temizlenmelidir.

### Dönüşüm uyumluluğu

- DOCX dönüşümünde `referenceV14_java_temelleri.docx` ve `styles_revised_v14.lua` kullanılmalıdır.
- Markdown dosyası üretildikten sonra Mermaid görselleri hazırlanmalı, ardından Pandoc dönüşümü yapılmalıdır.
- Dönüşüm sonrası PDF/PNG görsel kontrolünde üst bilgi, tablo, kod bloğu, diyagram ve bölüm sonu yerleşimi incelenmelidir.
