"""Bolum uretimi - streaming ile."""
import sys, time, json, httpx
from pathlib import Path

root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(root))

from bookmaker.generation.postprocess import process as postprocess
from bookmaker.authoring.pipeline import AuthoringPipeline

chapter_id = sys.argv[1]
title = sys.argv[2]
purpose = sys.argv[3] if len(sys.argv) > 3 else ""

sys.stderr.write(f"START:{chapter_id}\n")
sys.stderr.flush()

# Outline oku
pipe = AuthoringPipeline(root)
outline_p = pipe.root / "chapters" / chapter_id / "outline_versions" / "v001.md"
if outline_p.exists():
    outline = outline_p.read_text(encoding="utf-8")
else:
    sys.stderr.write("NO OUTLINE\n")
    sys.exit(1)

sys.stderr.write(f"Outline: {len(outline)} chars\n")

# Streaming ile chapter uret
api_key = "sk-98a85ecced414d499d34caf73a09b80d"
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json",
}

system_prompt = """Sen deneyimli bir teknik kitap yazari ve pedagojik icerik uzmanisin.
Verilen outline ve seed bilgisine gore CHAPTER_SPEC.md uyumlu
eksiksiz bir bolum Markdown metni ureteceksin.

YAML FRONT MATTER ile basla.

Kurallar:
1. YAML front matter ILE BASLA.
2. Basliklar elle numaralandirilmasin.
3. Her kod blogundan once CODE_META blogu olsun.
4. Kod ornekleri Java olsun, dosya adi public class adiyla uyumlu olsun.
5. Pedagojik kutular icin blockquote kullan.
6. Bolum sonunda ozet, terim sozlugu, sorular ve alistirmalar olsun."""

user_prompt = f"Bolum: {title}\n\nAmac: {purpose or 'Temel kavramlari ogretmek'}\n\nOutline:\n{outline}\n\nYukaridaki outline'a gore eksiksiz bolum metnini uret."

payload = {
    "model": "deepseek-chat",
    "messages": [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ],
    "max_tokens": 8192,
    "temperature": 0.7,
    "stream": True,
}

sys.stderr.write("Generating (streaming)...\n")
sys.stderr.flush()

t0 = time.time()
full_text = ""
chunk_count = 0
try:
    with httpx.Client(timeout=300) as client:
        with client.stream("POST", "https://api.deepseek.com/v1/chat/completions", headers=headers, json=payload) as resp:
            if resp.status_code != 200:
                sys.stderr.write(f"HTTP {resp.status_code}: {resp.text[:200]}\n")
                sys.exit(1)
            for line in resp.iter_lines():
                if line.startswith("data: ") and line != "data: [DONE]":
                    try:
                        data = json.loads(line[6:])
                        delta = data.get("choices", [{}])[0].get("delta", {}).get("content", "")
                        if delta:
                            full_text += delta
                            chunk_count += 1
                    except json.JSONDecodeError:
                        pass
    elapsed = time.time() - t0
    sys.stderr.write(f"API: {elapsed:.1f}s, {chunk_count} chunks, {len(full_text)} chars\n")

    # Post-process
    full_text = postprocess(full_text, chapter_id, title)

    # Kaydet
    pipe.paste_draft(chapter_id, full_text)
    pipe.advance(chapter_id, "full_text_pasted")

    sys.stdout.write(f"OK:{chapter_id}|chars:{len(full_text)}|time:{elapsed:.1f}s|chunks:{chunk_count}\n")
except Exception as e:
    elapsed = time.time() - t0
    sys.stdout.write(f"ERROR|{elapsed:.1f}s|{e}\n")
