#!/usr/bin/env python3
"""B13'deki Mermaid bloklarını dök"""
import re

path = r"D:\bookMaker_Deepseek\chapters\bolum-13\draft_versions\v001.md"
with open(path, "r", encoding="utf-8", errors="replace") as f:
    content = f.read()

pattern = re.compile(r'```mermaid\s*(.*?)\s*```', re.DOTALL)
blocks = pattern.findall(content)

print(f"B13: {len(blocks)} Mermaid blok\n")

for i, block in enumerate(blocks):
    lines = block.strip().split('\n')
    # Find the line positions in the original file
    idx = content.find(f'```mermaid\n{block.strip()}\n```')
    line_num = content[:idx].count('\n') + 1
    print(f"--- Blok #{i+1} (satir {line_num}) ---")
    print(block.strip())
    print()
