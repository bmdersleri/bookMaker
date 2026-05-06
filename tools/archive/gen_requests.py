"""Bolum uretimi - requests kutuphanesi ile."""
import sys, time, json
from pathlib import Path

root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root))
sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

import requests
from bookmaker.generation.postprocess import process as postprocess
from bookmaker.authoring.pipeline import AuthoringPipeline

ch_id = sys.argv[1]
title = sys.argv[2]
purpose = sys.argv[3] if len(sys.argv) > 3 else ""

outline_p = root / "chapters" / ch_id / "outline_versions" / "v001.md"
outline = outline_p.read_text(encoding="utf-8") if outline_p.exists() else ""

SYSTEM = "Sen deneyimli bir teknik kitap yazari ve pedagojik icerik uzmanisin. Verilen outline gore eksiksiz bir bolum Markdown metni uret. 1) YAML front matter ILE BASLA. 2) Basliklar elle numaralandirilmasin. 3) Her Java kod blogundan once <!-- CODE_META ... --> blogu olsun. 4) Kod ornekleri Java olsun. 5) pedagojik kutu icin blockquote. 6) Sonunda ozet, terim, soru, alistirma."
USER = f"Bolum: {title}\nAmac: {purpose}\nOutline:\n{outline}\n\nEksiksiz bolum metnini uret."

payload = {
    "model": "deepseek-chat",
    "messages": [
        {"role": "system", "content": SYSTEM},
        {"role": "user", "content": USER},
    ],
    "max_tokens": 8192,
    "temperature": 0.7,
    "stream": True,
}

headers = {
    "Authorization": "Bearer sk-98a85ecced414d499d34caf73a09b80d",
    "Content-Type": "application/json",
}

sys.stderr.write(f"Basliyor: {ch_id} | outline:{len(outline)}c\n")
sys.stderr.flush()

t0 = time.time()
try:
    resp = requests.post(
        "https://api.deepseek.com/v1/chat/completions",
        headers=headers,
        json=payload,
        stream=True,
        timeout=600,
    )
    sys.stderr.write(f"Baglandi: {resp.status_code}\n")
    sys.stderr.flush()
    
    if resp.status_code != 200:
        sys.stderr.write(f"HTTP {resp.status_code}: {resp.text[:200]}\n")
        sys.exit(1)
    
    full_text = ""
    chunk_count = 0
    for line in resp.iter_lines(decode_unicode=True):
        if line and line.startswith("data: ") and line != "data: [DONE]":
            try:
                data = json.loads(line[6:])
                delta = data.get("choices", [{}])[0].get("delta", {}).get("content", "")
                if delta:
                    full_text += delta
                    chunk_count += 1
            except json.JSONDecodeError:
                pass
    
    elapsed = time.time() - t0
    sys.stderr.write(f"API:{elapsed:.1f}s|{len(full_text)}c|{chunk_count}chunks\n")
    
    full_text = postprocess(full_text, ch_id, title)
    pipe = AuthoringPipeline(root)
    pipe.paste_draft(ch_id, full_text)
    pipe.advance(ch_id, "full_text_pasted")
    
    sys.stdout.write(f"OK|{len(full_text)}c|{elapsed:.1f}s|{chunk_count}chunks\n")
except Exception as e:
    elapsed = time.time() - t0
    sys.stdout.write(f"ERR|{elapsed:.1f}s|{e}\n")
