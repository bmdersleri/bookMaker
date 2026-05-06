"""
bolum-03 kalite analizi
"""
import sys, re
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
sys.stdout.reconfigure(encoding='utf-8')

gen_dir = Path("book_projects/java-temelleri/build/generation")

def analyze(text, label):
    h1 = re.findall(r'^# (.+)$', text, re.MULTILINE)
    h2 = re.findall(r'^## (.+)$', text, re.MULTILINE)
    h3 = re.findall(r'^### (.+)$', text, re.MULTILINE)
    code = len(re.findall(r'```', text)) // 2
    mermaid = len(re.findall(r'```mermaid', text))
    inline = len(re.findall(r'`[^`]+`', text))
    bold = len(re.findall(r'\*\*[^*]+\*\*', text))
    lists = len(re.findall(r'^[\s]*[-*+] ', text, re.MULTILINE))
    numbered = len(re.findall(r'^[\s]*\d+\. ', text, re.MULTILINE))
    tables = len(re.findall(r'^\|.*\|$', text, re.MULTILINE))
    richness = code * 5 + mermaid * 3 + bold // 2 + lists + numbered
    print(f'=== {label} ===')
    print(f'  Kelime: {len(text.split())}')
    print(f'  H1: {len(h1)}, H2: {len(h2)}, H3: {len(h3)}')
    print(f'  Kod bloklari: {code}')
    print(f'  Inline kod: {inline}')
    print(f'  Mermaid: {mermaid}')
    print(f'  Bold: {bold}')
    print(f'  Liste: {lists}, Numarali: {numbered}, Tablo: {tables}')
    print(f'  >>> ZENGINLIK: {richness}')
    print()

analyze((gen_dir / 'step1_seed.md').read_text(encoding='utf-8'), 'SEED')
analyze((gen_dir / 'step2_normalized.md').read_text(encoding='utf-8'), 'NORMALIZE')
analyze((gen_dir / 'step4_final.md').read_text(encoding='utf-8'), 'FINAL')

enrich_files = {'ozet': 'summary', 'sozluk': 'glossary', 'soru': 'questions',
                'alistirma': 'exercises', 'hata': 'errors', 'kopru': 'bridge'}
print('=== ENRICH ===')
total = 0
for etype, fname in enrich_files.items():
    path = gen_dir / f'step3_enrich_{fname}.md'
    if path.exists():
        t = path.read_text(encoding='utf-8')
        w = len(t.split())
        total += w
        print(f'  [{etype:12s}] {w:>5d} words')
print(f'  TOTAL: {total} words\n')

print('=== HATA TESPITI ===')
final = (gen_dir / 'step4_final.md').read_text(encoding='utf-8')
empty_cb = len(re.findall(r'```\s*```', final))
print(f'  Bos kod blogu: {empty_cb}')
all_bt = re.findall(r'```', final)
print(f'  Eslesmeyen ```: {len(all_bt) % 2 != 0}')
print(f'  Front matter: {"VAR" if final.strip().startswith("---") else "YOK"}')
for artifact in ['Harika', 'Iste', 'Elbette', 'Tabii ki']:
    if artifact in final[:500]:
        print(f'  LLM artifakti: "{artifact}"')
        break
else:
    print(f'  LLM artifakti: YOK')
for kw in ['public static void main', 'System.out.println', 'public class']:
    if kw in final:
        print(f'  Java kodu: {kw}')
        break
else:
    print(f'  Java kodu: YOK')
