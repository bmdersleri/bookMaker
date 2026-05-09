"""Tek bolum uretimi - 300sn timeout ile."""
import sys
from pathlib import Path

root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(root))

from bookmaker.generation.pipeline import GenerationPipeline
from bookmaker.llm.openai import OpenAICompatibleClient

chapter_id = sys.argv[1]
title = sys.argv[2]
purpose = sys.argv[3] if len(sys.argv) > 3 else ""

sys.stderr.write(f"Basliyor: {chapter_id} - {title}\n")
sys.stderr.flush()

pipe = GenerationPipeline(root)

# 300sn timeout
pipe.client = OpenAICompatibleClient(
    api_key=pipe.config.api_key,
    model=pipe.config.model,
    base_url=pipe.config.base_url,
    timeout=300,
)

text = pipe.generate_chapter(chapter_id, title, purpose=purpose)

draft_path = root / "chapters" / chapter_id / "draft_versions" / "v001.md"
chars = len(text)
lines = text.count("\n")

sys.stdout.write(f"OK:{draft_path}|chars:{chars}|lines:{lines}\n")
sys.stdout.flush()
