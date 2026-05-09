#!/usr/bin/env python3
"""Convert H1 sub-headings to H2 in bolum-06 (for/while/do-while)"""
path = 'chapters/bolum-06/draft_versions/v001.md'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# These three H1 headings should be H2
content = content.replace('\n# for D', '\n## for D')
content = content.replace('\n# while D', '\n## while D')
content = content.replace('\n# do-while D', '\n## do-while D')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print('bolum-06: for/while/do-while converted to H2')

# Verify H1/H2 count
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()
h1_count = sum(1 for l in lines if l.strip().startswith('# ') and not l.strip().startswith('## '))
h2_count = sum(1 for l in lines if l.strip().startswith('## ') and not l.strip().startswith('### '))
print(f'H1: {h1_count}, H2: {h2_count}')
