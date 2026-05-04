#!/usr/bin/env python3
"""Kaynak bölümlerdeki hatalı Mermaid bloklarını bul ve düzelt"""
import re
import os

# Merged markdown'dan blok numaralarını ve kaynak bölümleri bul
merged_path = r"D:\bookMaker_Deepseek\build\output\java-programlamaya-giris.md"
with open(merged_path, "r", encoding="utf-8", errors="replace") as f:
    merged = f.read()

# Tüm mermaid bloklarını bul
pattern = re.compile(r'```mermaid\s*(.*?)\s*```', re.DOTALL)
blocks = pattern.findall(merged)

print(f"Toplam Mermaid bloğu (merged): {len(blocks)}")

# Problemli blokları bul (parantez, <br/>, çift tırnak içeren)
problem_indices = []
for i, block in enumerate(blocks):
    issues = []
    if '(' in block and ')' in block:
        # Check if parentheses are inside [] nodes
        lines = block.strip().split('\n')
        for line in lines:
            if '(' in line and '[' in line and ']' in line:
                # Extract content between [ and ]
                bracket_content = re.findall(r'\[([^\]]*)\]', line)
                for bc in bracket_content:
                    if '(' in bc:
                        issues.append(f"Parantez: {bc.strip()}")
            if '<br/>' in line:
                issues.append(f"HTML br: {line.strip()}")
            if '"' in line and not line.strip().startswith('"'):
                # Check for quotes inside [] but not the node syntax
                bracket_content = re.findall(r'\[([^\]]*)\]', line)
                for bc in bracket_content:
                    if '"' in bc:
                        issues.append(f"Tırnak: {bc.strip()}")
    if issues:
        print(f"\nBlok #{i+1}: {'; '.join(issues)}")

# Şimdi kaynak bölüm dosyalarını tara
chapters_dir = r"D:\bookMaker_Deepseek\chapters"
for root, dirs, files in os.walk(chapters_dir):
    for fname in files:
        if fname.endswith(".md") and "draft" in root:
            fpath = os.path.join(root, fname)
            with open(fpath, "r", encoding="utf-8", errors="replace") as f:
                content = f.read()
            
            # Mermaid bloklarını bul
            chapter_blocks = pattern.findall(content)
            for i, block in enumerate(chapter_blocks):
                issues = []
                lines = block.strip().split('\n')
                for line in lines:
                    if '(' in line and '[' in line and ']' in line:
                        bracket_content = re.findall(r'\[([^\]]*)\]', line)
                        for bc in bracket_content:
                            if '(' in bc:
                                issues.append(f"Parantez: {bc.strip()}")
                    if '<br/>' in line:
                        issues.append(f"HTML br: {line.strip()}")
                    if '"' in line:
                        bracket_content = re.findall(r'\[([^\]]*)\]', line)
                        for bc in bracket_content:
                            if '"' in bc:
                                issues.append(f"Tırnak: {bc.strip()}")
                if issues:
                    relpath = os.path.relpath(fpath, chapters_dir)
                    print(f"\n>> {relpath} - Blok #{i+1}: {'; '.join(issues)}")
                    print(f"  Icerik: {block.strip()[:200]}")
