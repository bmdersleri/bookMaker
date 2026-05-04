#!/usr/bin/env python3
"""B19 Mermaid bloklarini dok"""
import re

path = r"D:\bookMaker_Deepseek\chapters\bolum-19\draft_versions\v001.md"
with open(path, "r", encoding="utf-8", errors="replace") as f:
    content = f.read()

pattern = re.compile(r'```mermaid\s*(.*?)\s*```', re.DOTALL)
blocks = pattern.findall(content)

print(f"B19: {len(blocks)} Mermaid blok\n")

for i, block in enumerate(blocks):
    print(f"--- Blok #{i+1} ---")
    print(repr(block.strip()))
    print()
    print(block.strip())
    print()
