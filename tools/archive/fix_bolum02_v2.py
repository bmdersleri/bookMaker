#!/usr/bin/env python3
"""Fix double prefix in bolum-02 H1 using exact UTF-8 bytes."""
import re

path = 'chapters/bolum-02/draft_versions/v001.md'

with open(path, 'rb') as f:
    data = f.read()

# Turkish 'Bölüm 2:  Bölüm 2:' (note: TWO spaces between)
# UTF-8: B\xc3\xb6l\xc3\xbcm 2:  B\xc3\xb6l\xc3\xbcm 2:
bolum_prefix = b'B\xc3\xb6l\xc3\xbcm 2:'
double_prefix = bolum_prefix + b'  ' + bolum_prefix
single_prefix = bolum_prefix + b' '

data = data.replace(double_prefix, single_prefix)

with open(path, 'wb') as f:
    f.write(data)

# Verify
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

h1 = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
print('H1:', h1.group(1) if h1 else 'YOK')

# Count Bolum occurrences
bolum_count = content.count('B' + chr(0xF6 if False else 246))  # just a check
# simpler:
count = len(re.findall(r'B.l.m', content))
print(f'Bolum occurrences: {count}')
