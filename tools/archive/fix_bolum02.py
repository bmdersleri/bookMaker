#!/usr/bin/env python3
"""Fix double prefix in bolum-02"""
import re

path = 'chapters/bolum-02/draft_versions/v001.md'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix double prefix in H1 - use exact Turkish characters
content = content.replace('# Bölüm 2: Bölüm 2: Java', '# Bölüm 2: Java')
# Fix title in front matter
content = content.replace('title: "Bölüm 2: Java', 'title: "Java')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

# Verify
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    stripped = line.strip()
    if stripped.startswith('# ') and not stripped.startswith('## '):
        print(f'H1 L{i+1}: {stripped[:80]}')
    elif stripped.startswith('## ') and not stripped.startswith('### '):
        print(f'  H2 L{i+1}: {stripped[:60]}')
