"""Bolum uretimi - urllib ile."""
import sys, time, json, urllib.request
from pathlib import Path

root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root))

from bookmaker.generation.postprocess import process as postprocess
from bookmaker.authoring.pipeline import AuthoringPipeline

chapter_id = sys.argv[1]
title = sys.argv[2]
purpose = sys.argv[3] if len(sys.argv) > 3 else ""

sys.stderr.write(f"START:{chapter_id}\n"); sys.stderr.flush()

pipe = AuthoringPipeline(root)
outline_p = pipe.root / "chapters" / chapter_id / "outline_versions" / "v001.md"
if outline_p.exists():
    outline = outline_p.read_text(encoding="utf-8")
else:
    sys.stderr.write("NO OUTLINE\n"); sys.exit(1)

sys.stderr.write(f"Outline: {len(outline)} chars\n"); sys.stderr.flush()

system_prompt = """Sen deneyimli bir teknik kitap yazari ve pedagojik icerik uzmanisin.
Verilen outline gore eksiksiz bir bolum Markdown metni ureteceksin.

YAML FRONT MATTER ile basla.

Kurallar:
1. YAML front matter ILE BASLA.
2. Basliklar elle numaralandirilmasin.
3. Her Java kod blogundan once CODE_META blogu olsun.
4. Kod ornekleri Java olsun.
5. Pedagojik kutular icin blockquote kullan.
6. Bolum sonunda ozet, terim sozlugu, sorular ve alistirmalar olsun."""

user = f"Bolum: {title}\n\nAmac: {purpose}\n\nOutline:\n{outline}\n\nEksiksiz bolum metnini uret."

payload = json.dumps({
    "model": "deepseek-chat",
    "messages": [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user},
    ],
    "max_tokens": 8192,
    "temperature": 0.7,
}).encode("utf-8")

req = urllib.request.Request(
    "https://api.deepseek.com/v1/chat/completions",
    data=payload,
    headers={
        "Authorization": "Bearer sk-98a85ecced414d499d34caf73a09b80d",
        "Content-Type": "application/json",
    },
    method="POST",
)

sys.stderr.write("Generating...\n"); sys.stderr.flush()
t0 = time.time()
try:
    with urllib.request.urlopen(req, timeout=300) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        elapsed = time.time() - t0
        full_text = data["choices"][0]["message"]["content"]
        usage = data.get("usage", {})
        sys.stderr.write(f"API: {elapsed:.1f}s, {len(full_text)} chars, tokens: {usage}\n")

        # Post-process
        full_text = postprocess(full_text, chapter_id, title)

        # Kaydet
        pipe.paste_draft(chapter_id, full_text)
        pipe.advance(chapter_id, "full_text_pasted")

        sys.stdout.write(f"OK:{chapter_id}|chars:{len(full_text)}|time:{elapsed:.1f}s\n")
except Exception as e:
    elapsed = time.time() - t0
    sys.stdout.write(f"ERROR|{elapsed:.1f}s|{e}\n")
