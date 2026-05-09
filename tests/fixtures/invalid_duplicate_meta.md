---
title: "Hatalı Bölüm — Yinelenen Meta"
subtitle: "Java'nın Temelleri"
author: "Test"
date: "2026"
lang: tr-TR
documentclass: report
toc: true
toc-depth: 3
numbersections: true
repo: testrepo
project-alias: test
chapter-alias: test-dup
chapter_id: test-dup
chapter_type: core
automation_profile: academic_technical_book_v1
chapter_spec: chapter_spec_v0_1
numbering: auto
github_slug: test-dup
qr_policy: dual_for_code_examples
asset_policy: manual_override
---

# Yinelenen Meta Bölümü

<!-- SECTION_META
order: 001
title: "Giriş"
-->

## Giriş

Giriş metni.

<!-- SECTION_META
order: 001
title: "Yinelenen Sıra"
-->

## Yinelenen Sıra

Aynı order değeri kullanıldı.

<!-- CODE_META
order: 001
code_id: test_dup_kod01
extension: java
title: "İlk kod"
file: "IlkKod.java"
link: "https://example.com"
intentional_mismatch: false
validation_mode: runnable
kind: example
main_class: "IlkKod"
extract: true
test: compile
github: true
qr_policy: dual
-->

```java
// Dosya: IlkKod.java
public class IlkKod {
    public static void main(String[] args) {
        System.out.println("İlk");
    }
}
```

<!-- CODE_META
order: 002
code_id: test_dup_kod01
extension: java
title: "Aynı ID'li kod"
file: "AyniId.java"
link: "https://example.com"
intentional_mismatch: false
validation_mode: runnable
kind: example
main_class: "AyniId"
extract: true
test: compile
github: true
qr_policy: dual
-->

```java
// Dosya: AyniId.java
public class AyniId {
    public static void main(String[] args) {
        System.out.println("Aynı ID");
    }
}
```
