"""Migrate pipeline.py from dual model to single model."""
from pathlib import Path

p = Path("src/bookmaker/generation/pipeline.py")
content = p.read_text(encoding="utf-8")

changes = 0

# 1. Class docstring
old = 'seed_model   -> Pro (DeepSeek V4 Pro)    -> ana icerik\n#     enrich_model -> Flash (DeepSeek V4 Flash) -> tamamlama'
new = 'model -> DeepSeek v4 Flash (deepseek-chat) -> tum API cagrilari'
if old in content:
    content = content.replace(old, new)
    changes += 1
    print("1. Class docstring: OK")

# 2. __init__ - replace dual client with single
old = '        self.seed_client: Optional[OpenAICompatibleClient] = None\n        self.enrich_client: Optional[OpenAICompatibleClient] = None'
new = '        self.client: Optional[OpenAICompatibleClient] = None'
if old in content:
    content = content.replace(old, new)
    changes += 1
    print("2. __init__: OK")

# 3. _init_clients - single client
old = """        base = {"api_key": self.llm_config.api_key,
                "base_url": self.llm_config.base_url}
        sm = self.llm_config.seed_model or "deepseek-chat"
        self.seed_client = OpenAICompatibleClient(**base, model=sm, timeout=300)
        em = self.llm_config.enrich_model or sm
        self.enrich_client = OpenAICompatibleClient(**base, model=em, timeout=60)"""

new = """        base = {"api_key": self.llm_config.api_key,
                "base_url": self.llm_config.base_url,
                "model": self.llm_config.model}
        self.client = OpenAICompatibleClient(**base, timeout=120)"""

if old in content:
    content = content.replace(old, new)
    changes += 1
    print("3. _init_clients: OK")
else:
    print(f"3. _init_clients: NOT FOUND!")
    # Debug: show what's around that area
    idx = content.find('_init_clients')
    print(repr(content[idx:idx+400]))

# 4. is_ready
old = '        return bool(self.llm_config.is_configured() and self.seed_client)'
new = '        return bool(self.llm_config.is_configured() and self.client)'
if old in content:
    content = content.replace(old, new)
    changes += 1
    print("4. is_ready: OK")

# 5. seed() - replace self.seed_client
old = '        if not self.seed_client:'
new = '        if not self.client:'
if old in content:
    content = content.replace(old, new)
    changes += 1
    print("5. seed() check: OK")

old = '        model_name = self.llm_config.seed_model or "varsayilan"'
if old in content:
    content = content.replace(old, '        model = self.llm_config.model')
    changes += 1
    print("5b. seed() model: OK")

old = '        self.seed_client.generate_text(SYSTEM_AUTHOR, user_prompt)'
new = '        self.client.generate_text(SYSTEM_AUTHOR, user_prompt)'
if old in content:
    content = content.replace(old, new)
    changes += 1
    print("5c. seed() API call: OK")

# 6. enrich() - replace enrich_client
old = '        if not self.enrich_client:'
new = '        if not self.client:'
if old in content:
    content = content.replace(old, new)
    changes += 1
    print("6a. enrich() check: OK")

old = '        model_name = self.llm_config.enrich_model or "varsayilan"'
if old in content:
    content = content.replace(old, '        model = self.llm_config.model')
    changes += 1
    print("6b. enrich() model: OK")

old = '        c = self.enrich_client.generate_text(SYSTEM_AUTHOR, user_prompt)'
new = '        c = self.client.generate_text(SYSTEM_AUTHOR, user_prompt)'
if old in content:
    content = content.replace(old, new)
    changes += 1
    print("6c. _call_enrich: OK")

# 7. generate_chapter() - model info
old = '            "model_seed": self.llm_config.seed_model or "varsayilan",\n            "model_enrich": self.llm_config.enrich_model or "varsayilan",'
new = '            "model": self.llm_config.model,'
if old in content:
    content = content.replace(old, new)
    changes += 1
    print("7a. generate_chapter() model info: OK")

old = 'f"\\n  Seed: {result[\'model_seed\']} | Enrich: {result[\'model_enrich\']}"'
new = 'f"\\n  Model: {result[\'model\']}"'
if old in content:
    content = content.replace(old, new)
    changes += 1
    print("7b. generate_chapter() display: OK")

# 8. generate_chapter_with_spec - model info
old = 'f\'"model":"{self.llm_config.seed_model}"\''
new = 'f\'"model":"{self.llm_config.model}"\''
if old in content:
    content = content.replace(old, new)
    changes += 1
    print("8a. spec method model info: OK")

# 9. generate_chapter_with_spec - client refs
old = 'spec = generate_spec(self.seed_client, title, concepts,'
new = 'spec = generate_spec(self.client, title, concepts,'
if old in content:
    content = content.replace(old, new)
    changes += 1
    print("9a. spec call: OK")

old = 'validation = validate_spec(self.enrich_client, spec, title)'
new = 'validation = validate_spec(self.client, spec, title)'
if old in content:
    content = content.replace(old, new)
    changes += 1
    print("9b. validation call: OK")

p.write_text(content, encoding="utf-8")
print(f"\nTotal changes: {changes}")

# Verify
import py_compile
py_compile.compile(str(p), doraise=True)
print("Syntax: OK")
