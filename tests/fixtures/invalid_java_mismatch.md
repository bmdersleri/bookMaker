---
title: "Hatalı Bölüm — Java Uyumsuzluğu"
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
chapter-alias: test-java
chapter_id: test-java
chapter_type: core
automation_profile: academic_technical_book_v1
chapter_spec: chapter_spec_v0_1
numbering: auto
github_slug: test-java
qr_policy: dual_for_code_examples
asset_policy: manual_override
---

# Java Uyumsuzluk Testi

<!-- SECTION_META
order: 001
title: "Giriş"
-->

## Giriş

Java dosya adı/sınıf adı uyumsuzluğu.

<!-- CODE_META
order: 001
code_id: test_java_kod01
extension: java
title: "Yanlış sınıf adı"
file: "DogruDosyaAdi.java"
link: "https://github.com/test/test"
intentional_mismatch: false
validation_mode: runnable
kind: example
main_class: "DogruDosyaAdi"
extract: true
test: compile
github: true
qr_policy: dual
-->

```java
// Dosya: DogruDosyaAdi.java
public class YanlisSinifAdi {
    public static void main(String[] args) {
        System.out.println("Hata");
    }
}
```
