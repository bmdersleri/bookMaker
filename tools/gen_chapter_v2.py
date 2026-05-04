"""Tek bolum uretimi - v2, direk API cagrisi ile."""
import sys, time
from pathlib import Path

root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root))

from bookmaker.llm.openai import OpenAICompatibleClient
from bookmaker.generation.prompts import chapter_prompt
from bookmaker.generation.postprocess import process as postprocess
from bookmaker.authoring.pipeline import AuthoringPipeline

chapter_id = sys.argv[1]
title = sys.argv[2]
purpose = sys.argv[3] if len(sys.argv) > 3 else ""

sys.stderr.write(f"START:{chapter_id}\n")
sys.stderr.flush()

# API client - 300sn timeout
client = OpenAICompatibleClient(
    api_key="sk-98a85ecced414d499d34caf73a09b80d",
    model="deepseek-chat",
    base_url="https://api.deepseek.com/v1",
    timeout=300,
)

# Outline oku
pipe = AuthoringPipeline(root)
outline_p = pipe.root / "chapters" / chapter_id / "outline_versions" / "v001.md"
if outline_p.exists():
    outline = outline_p.read_text(encoding="utf-8")
    sys.stderr.write(f"Outline: {len(outline)} chars\n")
else:
    sys.stderr.write("NO OUTLINE FOUND\n")
    sys.exit(1)

sys.stderr.write("Generating chapter...\n")
sys.stderr.flush()

t0 = time.time()
sys_prompt, user_prompt = chapter_prompt(title, outline, purpose, None)
sys.stderr.write(f"Prompts generated: sys={len(sys_prompt)} user={len(user_prompt)}\n")
sys.stderr.flush()

chapter_text = client.generate_text(sys_prompt, user_prompt)
elapsed = time.time() - t0

sys.stderr.write(f"API done in {elapsed:.1f}s, got {len(chapter_text)} chars\n")

# Post-process
chapter_text = postprocess(chapter_text, chapter_id, title)

# Kaydet
pipe.paste_draft(chapter_id, chapter_text)
pipe.advance(chapter_id, "full_text_pasted")

sys.stdout.write(f"OK:{chapter_id}|chars:{len(chapter_text)}|time:{elapsed:.1f}s\n")
