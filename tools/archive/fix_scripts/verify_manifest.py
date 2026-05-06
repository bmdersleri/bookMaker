import sys, re
sys.stdout.reconfigure(encoding='utf-8')

for fname in ['GUI_MANIFEST.md', 'GUI_ROADMAP.md']:
    path = f'D:/bookMaker_Deepseek/{fname}'
    with open(path, 'r', encoding='utf-8') as f:
        c = f.read()
    
    sections = re.findall(r'^## (.+)$', c, re.MULTILINE)
    checks = re.findall(r'- \[(.)\]', c)
    done = sum(1 for x in checks if x == 'x')
    todo = sum(1 for x in checks if x == ' ')
    endpoints = re.findall(r'`(GET|POST|PUT|DELETE|ws) .+`', c)
    
    print(f'=== {fname} ===')
    print(f'  Boyut:   {len(c):,} karakter')
    print(f'  Bolum:   {len(sections)}')
    print(f'  Tamam/Kaldi: {done}/{todo}')
    print(f'  Endpoint: {len(endpoints)}')
    print(f'  Icindekiler:')
    for s in sections:
        print(f'    {s}')
    print()
