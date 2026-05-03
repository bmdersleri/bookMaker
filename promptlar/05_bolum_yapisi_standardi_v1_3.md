# Java'nın Temelleri — Bölüm Yapısı Standardı v1.3

**Amaç:** Kitaptaki tüm bölümlerin benzer pedagojik akışla, numarasız kaynak başlıklarıyla ve otomasyon uyumlu meta işaretleriyle üretilmesini sağlamak.

---

## 1. Standart bölüm akışı

```markdown
# [Bölüm başlığı]

## Bölümün yol haritası
## Bölümün konumu ve pedagojik rolü
## Öğrenme çıktıları
## Ön bilgi ve başlangıç varsayımları
## Ana kavramlar
## Adım adım kod örnekleri
## Kodun çalışma mantığı ve beklenen çıktı
## Uçtan uca mini uygulama
## Sık yapılan hatalar ve yanlış sezgiler
## Hata ayıklama egzersizi
## Bölümün sonraki bölümlerle ilişkisi
## Bölüm özeti
## Terim sözlüğü
## Kendini değerlendirme soruları
## Programlama alıştırmaları
## Haftalık laboratuvar / proje görevi
## Değerlendirme rubriği
## İleri okuma ve kaynaklar
## Bir sonraki bölüme köprü
```

---

## 2. Bölümün konumu ve pedagojik rolü

“Bölüm 7’de...” gibi sabit numaralı ifadelerden mümkün olduğunca kaçınılmalıdır. Bunun yerine kavramsal ifade tercih edilmelidir.

Doğru:

```text
Önceki bölümde kullanıcıdan veri alma mantığı ele alınmıştı.
```

Riskli:

```text
Bölüm 7’de Scanner konusu anlatılmıştı.
```

---

## 3. Kod örneği standardı

Kod örneği başlığı kaynak Markdown içinde numarasız yazılmalıdır:

```markdown
### Kod: Temel if kullanımı
```

`Kod 8.1` gibi görünür numara verilmemelidir. Her kod örneği `CODE_META` bloğu içermelidir.

---

## 4. Hatalı ve düzeltilmiş örnekler

Hatalı örnek:

```yaml
kind: broken_example
extract: false
test: skip
github: false
qr: none
```

Düzeltilmiş örnek:

```yaml
kind: fixed_example
extract: true
test: compile
github: true
qr: dual
```

---

## 5. Mermaid ve görsel standardı

Her Mermaid diyagramı `MERMAID_META` ile işaretlenmelidir. Kullanıcı tarafından elle düzenlenen görseller için aynı ID ile `assets/manual/` klasörüne dosya konabilir.

---

## 6. Bölüm sonu bileşenleri

Aşağıdaki kapanış bileşenleri eksik bırakılmamalıdır: özet, terim sözlüğü, değerlendirme soruları, programlama alıştırmaları, laboratuvar görevi, rubrik, ileri okuma ve köprü.

Kaynak Markdown sonunda elle `BÖLÜM SONU` yazılmaz.

---

## 7. Bölüm kalite kontrolü

- Başlıklar numarasız mı?
- `chapter_id` var mı?
- `CODE_META` ve `MERMAID_META` ID'leri benzersiz mi?
- Hatalı kodlar `test: skip` olarak işaretli mi?
- Derlenecek kodlarda dosya adı ve `mainClass` uyumlu mu?
- Görseller `assets/final/...` yoluna bağlanıyor mu?
