"""Detayli kalite analizi - tum pipeline ciktilari."""
import sys, re
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

def analyze_markdown(path, label):
    text = Path(path).read_text(encoding='utf-8')
    
    h1 = re.findall(r'^# (.+)$', text, re.MULTILINE)
    h2 = re.findall(r'^## (.+)$', text, re.MULTILINE)
    h3 = re.findall(r'^### (.+)$', text, re.MULTILINE)
    code_blocks = len(re.findall(r'```', text)) // 2
    mermaid = len(re.findall(r'```mermaid', text))
    inline_code = len(re.findall(r'`[^`]+`', text))
    bold = len(re.findall(r'\*\*[^*]+\*\*', text))
    list_items = len(re.findall(r'^[\s]*[-*+] ', text, re.MULTILINE))
    numbered_items = len(re.findall(r'^[\s]*\d+\. ', text, re.MULTILINE))
    tables = len(re.findall(r'^\|.*\|$', text, re.MULTILINE))
    links = len(re.findall(r'\[.+\]\(.+\)', text))
    
    richness = code_blocks*5 + mermaid*3 + bold//2 + list_items + numbered_items
    
    print(f'=== {label} ===')
    print(f'  Dosya: {path.name} ({len(text):,} chars, ~{len(text.split()):,} words)')
    print(f'  H1: {h1[0][:80] if h1 else "None"}')
    print(f'  H2: {len(h2)} adet')
    for h in h2:
        print(f'    - {h[:80]}')
    print(f'  H3: {len(h3)} adet')
    for h in h3[:15]:
        print(f'    - {h[:80]}')
    if len(h3) > 15:
        print(f'    ... ve {len(h3)-15} tane daha')
    print(f'  Kod bloklari: {code_blocks}')
    print(f'  Inline kod: {inline_code}')
    print(f'  Mermaid: {mermaid}')
    print(f'  Bold metin: {bold}')
    print(f'  Liste ogeleri: {list_items}')
    print(f'  Numarali ogeler: {numbered_items}')
    print(f'  Tablo satirlari: {tables}')
    print(f'  Linkler: {links}')
    print(f'  >>> ZENGINLIK PUANI: {richness}')
    print()

print('=' * 70)
print('KALITE ANALIZI - bolum-02 Pipeline Ciktilari')
print('=' * 70)
print()

gen = Path('D:/bookMaker_Deepseek/book_projects/java-temelleri/build/generation')

analyze_markdown(gen / 'step1_seed_raw.md', '1. SEED (orijinal)')
analyze_markdown(gen / 'step2_normalized.md', '2. NORMALIZE')
analyze_markdown(gen / 'step4_final.md', '3. FINAL')

# ENRICH detay analizi
print('=' * 70)
print('ENRICH BOLUMLERI DETAY')
print('=' * 70)

enrich_files = {
    'ozet': 'step3_enrich_summary.md',
    'sozluk': 'step3_enrich_glossary.md',
    'soru': 'step3_enrich_questions.md',
    'alistirma': 'step3_enrich_exercises.md',
    'hata': 'step3_enrich_errors.md',
    'kopru': 'step3_enrich_bridge.md',
}

total_enrich_words = 0
for etype, fname in enrich_files.items():
    path = gen / fname
    if path.exists():
        text = path.read_text(encoding='utf-8')
        words = len(text.split())
        total_enrich_words += words
        # First 200 chars
        preview = text[:200].replace('\n', ' ')
        print(f'  [{etype:12s}] {words:>5d} words, {len(text):>6d} chars')
        print(f'            Baslangic: {preview}...')
        print()

print(f'Toplam ENRICH: {total_enrich_words} words')
print()

# Hata tespiti
print('=' * 70)
print('HATA TESPITI')
print('=' * 70)

for label, fname in [('FINAL', 'step4_final.md'), ('SEED', 'step1_seed_raw.md')]:
    path = gen / fname
    text = path.read_text(encoding='utf-8')
    
    issues = []
    
    # Empty code blocks
    empty_cb = len(re.findall(r'```\s*```', text))
    if empty_cb:
        issues.append(f'{empty_cb} bos kod blogu')
    
    # Unmatched backticks
    all_bt = re.findall(r'```', text)
    if len(all_bt) % 2 != 0:
        issues.append('Eslesmeyen ``` isaretleri!')
    
    # Front matter check
    has_fm = text.strip().startswith('---')
    issues.append(f'Front matter: {"VAR" if has_fm else "YOK"}')
    
    # Turkish character check
    has_tr = bool(re.search(r'[şğüöçİŞĞÜÖÇ]', text))
    issues.append(f'Turkce karakter: {"VAR" if has_tr else "YOK"}')
    
    # Check for LLM artifacts
    for artifact in ['Harika', 'Iste', 'Elbette', 'Tabii ki', 'Harika bir']:
        if artifact in text[:500]:
            issues.append(f'LLM artifakti bulundu: "{artifact}"')
            break
    
    # Java keyword in code
    java_kw = ['public class', 'System.out.println', 'public static void']
    found_kw = [kw for kw in java_kw if kw in text]
    if found_kw:
        issues.append(f'Java kod ornegi: {", ".join(found_kw)}')
    
    print(f'  {label}:')
    for issue in issues:
        print(f'    - {issue}')
    print()
