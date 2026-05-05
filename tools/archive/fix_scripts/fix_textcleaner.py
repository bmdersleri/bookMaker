"""Fix TextCleaner: implement _extract_protected_blocks with placeholder
and properly restore them in _restore_blocks."""
from pathlib import Path

p = Path('D:/bookMaker_Deepseek/src/bookmaker/generation/clean_text.py')
content = p.read_text(encoding='utf-8')

# Replace _extract_protected_blocks
old_extract_start = '    @classmethod\n    def _extract_protected_blocks(cls, text: str) -> dict:\n        """Kod bloklarını geçici olarak çıkar (koru)."""\n        blocks = []\n        clean_parts = []\n        last_end = 0\n\n        pattern = re.compile(r\'```(\\w*)\\n.*?```\', re.DOTALL)\n        for match in pattern.finditer(text):\n            clean_parts.append(text[last_end:match.start()])\n            blocks.append(match.group(0))\n            last_end = match.end()\n        clean_parts.append(text[last_end:])\n\n        return {\n            "clean": "".join(clean_parts),\n            "blocks": blocks,\n        }'

new_extract = '''    PLACEHOLDER_PREFIX = "CODEBLOCK_PLACEHOLDER_"

    @classmethod
    def _extract_protected_blocks(cls, text: str) -> dict:
        """Kod bloklarını geçici olarak çıkar, yerine placeholder koy.

        Hem ```lang\\n...``` hem de ```...``` (dil belirtilmemiş) formatını destekler.
        """
        blocks = []
        result_parts = []
        last_end = 0

        # Daha esnek pattern: ``` ardından isteğe bağlı dil, isteğe bağlı newline
        pattern = re.compile(r'```(\\w*)\\s*\\n(.*?)```', re.DOTALL)
        for match in pattern.finditer(text):
            result_parts.append(text[last_end:match.start()])
            placeholder = f"\\n\\n{cls.PLACEHOLDER_PREFIX}{len(blocks)}\\n\\n"
            result_parts.append(placeholder)
            blocks.append(match.group(0))
            last_end = match.end()
        result_parts.append(text[last_end:])

        return {
            "clean": "".join(result_parts),
            "blocks": blocks,
        }'''

# Replace _restore_blocks
old_restore = '''    @classmethod
    def _restore_blocks(cls, text: str, blocks: list[str]) -> str:
        """Kod bloklarını geri yerleştir."""
        if not blocks:
            return text
        result = []
        remaining = text
       
        # Her blok için bir PLACEHOLDER kullan
        for i, block in enumerate(blocks):
            placeholder = f"``BLOCK_{i}``"
            # İlk plaseholder'ı blokla değiştir
            idx = remaining.find(placeholder)
            # Placeholder yoksa — bloklar korunmamış, normal string işle
            pass

        # Basit yaklaşım: blokları sırayla geri koy
        # Not: Bu basitleştirilmiş versiyon. Bloklar korunarak
        # temizlik yapıldığı için, metnin başına geri eklenebilir.
        # Gerçek uygulamada blok pozisyonları korunmalı.
        return text'''

new_restore = '''    @classmethod
    def _restore_blocks(cls, text: str, blocks: list[str]) -> str:
        """Placeholder'ları asıl kod bloklarıyla değiştir."""
        if not blocks:
            return text
        for i, block in enumerate(blocks):
            placeholder = f"{cls.PLACEHOLDER_PREFIX}{i}"
            if placeholder in text:
                text = text.replace(placeholder, f"\\n\\n{block}\\n\\n")
        return text'''

if old_extract_start in content:
    content = content.replace(old_extract_start, new_extract)
    print('_extract_protected_blocks: REPLACED')
else:
    print('_extract_protected_blocks: NOT FOUND')
    # Try to find what's actually there
    idx = content.find('def _extract_protected_blocks')
    print(f'Found at: {idx}')
    print(repr(content[idx:idx+200]))

if old_restore in content:
    content = content.replace(old_restore, new_restore)
    print('_restore_blocks: REPLACED')
else:
    print('_restore_blocks: NOT FOUND')
    idx = content.find('def _restore_blocks')
    print(f'Found at: {idx}')
    print(repr(content[idx:idx+200]))

p.write_text(content, encoding='utf-8')
print(f'Written: {len(content)} chars')

# Verify syntax
import py_compile
py_compile.compile(str(p), doraise=True)
print('Syntax: OK')
