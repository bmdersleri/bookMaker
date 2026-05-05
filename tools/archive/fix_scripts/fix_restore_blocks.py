"""Fix _restore_blocks method in TextCleaner."""
from pathlib import Path

p = Path('D:/bookMaker_Deepseek/src/bookmaker/generation/clean_text.py')
with open(p, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Line numbers (1-indexed): 269-287
# 0-indexed: 268-286
new_method = [
    '    @classmethod\n',
    '    def _restore_blocks(cls, text: str, blocks: list[str]) -> str:\n',
    '        """Placeholderlari asil kod bloklariyla degistir."""\n',
    '        if not blocks:\n',
    '            return text\n',
    '        for i, block in enumerate(blocks):\n',
    '            placeholder = f"{cls.PLACEHOLDER_PREFIX}{i}"\n',
    '            if placeholder in text:\n',
    '                text = text.replace(placeholder, f"\\n\\n{block}\\n\\n")\n',
    '        return text\n',
    '\n',
]

lines[268:287] = new_method

with open(p, 'w', encoding='utf-8') as f:
    f.writelines(lines)

import py_compile
py_compile.compile(str(p), doraise=True)
print('Syntax OK')

# Verify the method
idx = next(i for i, l in enumerate(lines) if '_restore_blocks' in l and 'def' in l)
print(f'\nNew _restore_blocks (line {idx+1}):')
for j in range(idx, min(idx+12, len(lines))):
    print(f'  {j+1}: {lines[j]}', end='')
