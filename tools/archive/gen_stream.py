"""Tek bolum streaming ile uret - dogrudan API cagrisi."""
import sys, time, json, httpx
from pathlib import Path

root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root))
sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

from bookmaker.generation.postprocess import process as postprocess
from bookmaker.authoring.pipeline import AuthoringPipeline

ch_id = sys.argv[1]
title = sys.argv[2]
purpose = sys.argv[3] if len(sys.argv) > 3 else ""

API_KEY = "sk-98a85ecced414d499d34caf73a09b80d"
BASE_URL = "https://api.deepseek.com/v1"
MODEL = "deepseek-chat"

HEADERS = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

SYSTEM_CHAPTER = """Sen deneyimli bir teknik kitap yazari ve pedagojik icerik uzmanisin.
Verilen outline gore eksiksiz bir bolum Markdown metni ureteceksin.

Kurallar:
1. YAML front matter ILE BASLA.
2. Basliklar elle numaralandirilmasin.
3. Her kod blogundan once "<!-- CODE_META ... -->" blogu olsun.
4. Kod ornekleri Java olsun, dosya adi public class adiyla uyumlu olsun.
5. Pedagojik kutular icin blockquote kullan.
6. Bolum sonunda ozet, terim sozlugu, sorular ve alistirmalar olsun.
7. Bolum en az 12000 karakter olmali."""

pipe = AuthoringPipeline(root)
outline_p = root / "chapters" / ch_id / "outline_versions" / "v001.md"
outline = outline_p.read_text(encoding="utf-8") if outline_p.exists() else ""

sys.stderr.write(f"Outline: {len(outline)} chars\n")
sys.stderr.flush()

user = (
    f"Bolum: {title}\nAmac: {purpose}\nOutline:\n{outline}\n\n"
    "Yukaridaki outline'a gore eksiksiz bolum metnini uret."
)
payload = {
    "model": MODEL,
    "messages": [
        {"role": "system", "content": SYSTEM_CHAPTER},
        {"role": "user", "content": user},
    ],
    "max_tokens": 8192,
    "temperature": 0.7,
    "stream": True,
}

t0 = time.time()
full_text = ""
chunk_count = 0
try:
    with httpx.Client(timeout=300) as client:
        with client.stream("POST", f"{BASE_URL}/chat/completions", headers=HEADERS, json=payload) as resp:
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

    full_text = postprocess(full_text, ch_id, title)
    pipe.paste_draft(ch_id, full_text)
    pipe.advance(ch_id, "full_text_pasted")
    sys.stdout.write(f"OK:{ch_id}|chars:{len(full_text)}|time:{elapsed:.1f}s|chunks:{chunk_count}\n")
except Exception as e:
    elapsed = time.time() - t0
    sys.stdout.write(f"ERROR|{elapsed:.1f}s|{e}\n")
