"""Fix TextCleaner final state - remove duplicate @classmethod and verify."""
from pathlib import Path

p = Path('D:/bookMaker_Deepseek/src/bookmaker/generation/clean_text.py')
with open(p, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Fix: line 269 (0-indexed: 268) duplicate @classmethod
# Current state:
# 268:     @classmethod
# 269:     @classmethod  
# 270:     def _restore_blocks...
# Should be:
# 268:     @classmethod
# 269:     def _restore_blocks...

for i, line in enumerate(lines):
    if '_restore_blocks' in line and 'def' in line:
        # Check if previous line is @classmethod
        if i > 0 and '@classmethod' in lines[i-1]:
            # Check if line before that is also @classmethod
            if i > 1 and '@classmethod' in lines[i-2]:
                print(f'Found duplicate @classmethod at lines {i-1},{i}')
                # Remove the duplicate (the one closest to def, or merge)
                # Keep line i-2 as @classmethod, remove line i-1
                lines[i-1] = ''  # Remove the duplicate
                print('Removed duplicate')
            else:
                print(f'OK: single @classmethod at line {i} before {lines[i].strip()[:60]}')
        else:
            print(f'WARNING: _restore_blocks at line {i+1} has no @classmethod!')
        break

# Remove empty lines caused by deletion
lines = [l for l in lines if l != '']

with open(p, 'w', encoding='utf-8') as f:
    f.writelines(lines)

# Verify
import py_compile
py_compile.compile(str(p), doraise=True)
print('Syntax OK')

# Quick test
import sys
sys.path.insert(0, str(Path('D:/bookMaker_Deepseek/src').parent))
from bookmaker.generation.clean_text import TextCleaner

BT = '```'
test = 'Some text\n\n```java\nSystem.out.println("hello");\n```\n\nMore text'
result = TextCleaner.clean(test)
print(f'\nTest:')
print(f'  Input:  {test[:60]}...')
print(f'  Output: {result[:100]}...')
print(f'  BT count input: {test.count(BT)//2}, output: {result.count(BT)//2}')
if BT in result:
    print('OK: Code blocks preserved!')
else:
    print('FAIL: Code blocks lost!')
