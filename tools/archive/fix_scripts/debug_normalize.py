"""Debug: Find what strips code/mermaid in normalize."""
import sys, re
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
from bookmaker.generation.postprocess import normalize, normalize_headings, build_front_matter, TextCleaner

BT = '```'
seed = Path('D:/bookMaker_Deepseek/book_projects/java-temelleri/build/generation/step1_seed_raw.md').read_text(encoding='utf-8')

print(f'Original: {len(seed)} chars, Mermaid: {seed.count(BT + "mermaid")}, Code blocks: {seed.count(BT)//2}')
print()

# Test each step
for step_name, step_fn, args in [
    ('normalize_headings', normalize_headings, [seed]),
    ('build_front_matter', build_front_matter, [seed, 'bolum-02', 'test']),
    ('TextCleaner.clean', TextCleaner().clean, [seed]),
    ('full normalize', normalize, [seed, 'bolum-02', 'test title']),
]:
    try:
        result = step_fn(*args)
        mermaid_count = result.count(BT + 'mermaid')
        code_count = result.count(BT) // 2
        lost = seed.count(BT)//2 - code_count
        print(f'{step_name:25s}: {len(result):>6d} chars  Mermaid:{mermaid_count}  Code:{code_count}  Lost:{lost}')
    except Exception as e:
        print(f'{step_name:25s}: ERROR: {e}')

# Check if TextCleaner strips backticks
print()
tc = TextCleaner()
test = 'Some text with `inline code` and ```code block```'
result = tc.clean(test)
print(f'TextCleaner test:')
print(f'  Input:  {test}')
print(f'  Output: {result}')
print(f'  BT preserved: {BT in result}')
