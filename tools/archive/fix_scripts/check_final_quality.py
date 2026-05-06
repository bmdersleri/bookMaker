import sys, re
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path

final = Path('D:/bookMaker_Deepseek/book_projects/java-temelleri/build/generation/step4_final.md').read_text(encoding='utf-8')

h1 = re.findall(r'^# (.+)$', final, re.MULTILINE)
h2 = re.findall(r'^## (.+)$', final, re.MULTILINE)
h3 = re.findall(r'^### (.+)$', final, re.MULTILINE)
code_blocks = len(re.findall(r'```', final)) // 2
mermaid = len(re.findall(r'```mermaid', final))

print('=== FINAL CHAPTER STRUCTURE ===')
print(f'H1: {h1[0] if h1 else "N/A"}')
print(f'H2 sections: {len(h2)}')
print(f'H3 sections: {len(h3)}')
print(f'Code blocks: {code_blocks}')
print(f'Mermaid diagrams: {mermaid}')
print(f'Total: {len(final.split())} words, {len(final)} chars')
print()

print('H2 Headers:')
for h in h2:
    print(f'  {h}')
print()

print('H3 Headers:')
for h in h3:
    print(f'  {h}')
print()

# Show the ENRICH separators
separators = final.count('---')
print(f'Separators (---): {separators}')
print(f'Sections (via ---): {separators + 1}')
