# BÖLÜM XX — ÜRETİM GİRDİSİ ŞABLONU v1.3

**Kitap:** Java'nın Temelleri  
**Sürüm:** 1.3  
**Çıktı biçimi:** Pandoc/DOCX uyumlu ve otomasyon tarafından ayrıştırılabilir Markdown

---

## 0. v1.3 üretim ilkesi

Tam bölüm metni YAML front matter ile başlamalıdır. Bölüm başlığı ve alt başlıklar **numarasız** yazılmalıdır. Görünen bölüm, alt başlık, kod, tablo, şekil ve diyagram numaraları build sırasında atanacaktır.

```markdown
---
title: "[Bölüm başlığı]"
subtitle: "Java'nın Temelleri"
author: "İsmail Kırbaş"
date: "2026"
lang: tr-TR
documentclass: report
toc: true
toc-depth: 3
numbersections: true

chapter_id: "[kalici-bolum-kimligi]"
chapter_type: "[core/gui/jdbc/project/appendix]"
automation_profile: "java_book_v1_3"
numbering: "auto"
github_slug: "[kalici-bolum-kimligi]"
qr_policy: "dual_for_code_examples"
asset_policy: "manual_override"
---

# [Bölüm başlığı]
```

---

## 1. Bölüm kimliği

**Bölüm başlığı:** [Bölüm başlığı]  
**Kalıcı bölüm kimliği (`chapter_id`):** [ornek: karar-yapilari]  
**Kısım:** [Kitap kısmı]  
**Bölüm türü:** [Temel konu / Uygulama / GUI / JDBC / Final proje / Ek]  
**Görünen bölüm numarası:** Build sırasında otomatik atanır.  
**GitHub slug:** [ornek: karar-yapilari]  
**Varsayılan QR politikası:** [dual/source/page/none]  
**Manuel görsel politikası:** `manual_override`

---

## 2. Bölümün amacı

[Bu bölümün temel amacı 1–2 paragrafla açıklanır.]

---

## 3. Öğrenme çıktıları

Bu bölüm tamamlandığında öğrenci:

1. [Çıktı 1]
2. [Çıktı 2]
3. [Çıktı 3]
4. [Çıktı 4]
5. [Çıktı 5]
6. [Çıktı 6]

---

## 4. Zorunlu kavramlar

- [Kavram 1]
- [Kavram 2]
- [Kavram 3]
- [Kavram 4]
- [Kavram 5]

---

## 5. Zorunlu kod varlıkları

| Kod ID | Tür | Başlık | Dosya adı | Test | GitHub | QR |
|---|---|---|---|---|---|---|
| `[chapter_id]_kod01` | `example` | [Örnek başlığı] | `[DosyaAdi.java]` | `compile` | `true` | `dual` |
| `[chapter_id]_kod02` | `application` | [Uygulama başlığı] | `[DosyaAdi.java]` | `compile` | `true` | `dual` |
| `[chapter_id]_hata01` | `broken_example` | [Hatalı örnek] | `[DosyaAdi.java]` | `skip` | `false` | `none` |
| `[chapter_id]_hata01_duzeltilmis` | `fixed_example` | [Düzeltilmiş örnek] | `[DosyaAdi.java]` | `compile` | `true` | `dual` |

---

## 6. Zorunlu Mermaid / görsel varlıkları

| Görsel ID | Tür | Başlık | Manuel öncelik | Genişlik |
|---|---|---|---|---:|
| `[chapter_id]_diyagram01` | `mermaid` | [Diyagram başlığı] | `true` | 12.5 cm |

---

## 7. Uçtan uca mini uygulama

**Uygulama adı:** [Mini uygulama adı]

**Amaç:** [Uygulamanın amacı]

Mini uygulamanın ana Java dosyası `kind: application`, `test: compile`, `github: true`, `qr: dual` olarak işaretlenmelidir.

---

## 8. Üretim sonrası kontrol

- Başlıklar numarasız mı?
- `chapter_id` var mı?
- `CODE_META` blokları eksiksiz mi?
- `MERMAID_META` blokları eksiksiz mi?
- Derlenecek kodlarda dosya adı ve `mainClass` uyumlu mu?
- Hatalı örnekler `test: skip` olarak işaretli mi?
- `BÖLÜM SONU` elle yazılmamış mı?
- Görsel yolları `assets/final/...` üzerinden mi verilmiş?
