<!-- v1.3 notu: Bu dosya v1.2 içeriği temel alınarak otomasyon uyumlu pakete dahil edilmiştir. Görünen numaralar üretim hattında atanır; kalıcı kimlikler manifestte tutulur. -->

# Java'nın Temelleri — Pilot Çıktı Değerlendirme Notu v1.3

Bu not, Bölüm 8 pilot DOCX/PDF çıktısından sonra prompt ve dönüşüm zincirine eklenen kuralları özetler.

## Başarılı görülen noktalar

- Üst bilgi `Java'nın Temelleri — Prof. Dr. İsmail KIRBAŞ` biçimine taşınmıştır.
- Pedagojik kutular, kod blokları ve tablolar ders kitabı düzenine uygun görünmüştür.
- Mermaid diyagramı PNG olarak belgeye yerleşmiş ve ham `flowchart TD` kodu final PDF'de görünmemiştir.
- Bölüm yol haritası, öğrenme çıktıları, mini uygulama, hata ayıklama, alıştırma ve rubrik yapısı korunmuştur.

## Kalıcı hâle getirilen düzeltmeler

1. Mermaid diyagramları final çıktıda ham kod olarak bırakılmayacaktır.
2. Mermaid görsel genişliği varsayılan 12-13 cm aralığında tutulacaktır.
3. Kod satırı uzunluğu mümkünse 90 karakteri aşmayacaktır.
4. Çok uzun kod örnekleri küçük alt örneklere bölünecektir.
5. Numaralı listelerde görünür çıktı tutarlılığı için açık numaralandırma kullanılacaktır.
6. `BÖLÜM SONU` tekilleştirilecektir.
7. DOCX dönüşümünde `referenceV14_java_temelleri.docx` ve `styles_revised_v14.lua` kullanılacaktır.

## Önerilen dönüşüm sırası

```bash
python prepare_mermaid_images_v14.py Bolum_08_GPT_pilot.md --force
python render_all_mermaid_png_v14.py mermaid_images --force
pandoc -f markdown+tex_math_single_backslash Bolum_08_GPT_pilot.md \
  -o bolum_08.docx \
  --reference-doc=referenceV14_java_temelleri.docx \
  --lua-filter=styles_revised_v14.lua
```

DOCX üretiminden sonra PDF/PNG görsel kontrolü yapılmalıdır.
