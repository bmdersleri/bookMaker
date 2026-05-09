"""Fix remaining dual model references in pipeline.py"""
import re
from pathlib import Path

p = Path("src/bookmaker/generation/pipeline.py")
content = p.read_text(encoding="utf-8")

# Fix 1: docstring comments
old = "        seed_model   -> Pro (DeepSeek V4 Pro)    -> ana icerik\n        enrich_model -> Flash (DeepSeek V4 Flash) -> tamamlama"
new = "        model -> DeepSeek v4 Flash (deepseek-chat) -> tum API cagrilari"
if old in content:
    content = content.replace(old, new)
    print("1. Docstring: FIXED")
else:
    print("1. Docstring: NOT FOUND")

# Fix 2: all self.seed_client -> self.client
count = 0
for m in re.finditer(r"self\.seed_client", content):
    count += 1
    print(f"  seed_client at offset {m.start()}: ...{content[m.start():m.end()+40]}...")
content = content.replace("self.seed_client.generate_text", "self.client.generate_text")
print(f"2. self.seed_client.generate_text: {count} -> 0")

# Fix 3: seed_model in spec method metrics
old = 'f\'"model":"{self.llm_config.seed_model}"}\''
new = 'f\'"model":"{self.llm_config.model}"}\''
if old in content:
    content = content.replace(old, new)
    print("3. seed_model in spec: FIXED")
else:
    print("3. seed_model in spec: NOT FOUND")

p.write_text(content, encoding="utf-8")

import py_compile
py_compile.compile(str(p), doraise=True)
print("Syntax: OK")

# Final verification
for name in ["seed_client", "enrich_client", "seed_model", "enrich_model"]:
    print(f"  {name}: {content.count(name)} remaining")
if content.count("seed_client") + content.count("enrich_client") + content.count("seed_model") + content.count("enrich_model") == 0:
    print("\nALL CLEAN!")
