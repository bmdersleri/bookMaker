"""Batch bolum uretimi - requests ile streaming."""
import sys, time, json, requests
from pathlib import Path

root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(root))
sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

from bookmaker.generation.postprocess import process as postprocess
from bookmaker.authoring.pipeline import AuthoringPipeline

API_KEY = "sk-98a85ecced414d499d34caf73a09b80d"
BASE_URL = "https://api.deepseek.com/v1"
MODEL = "deepseek-chat"
HEADERS = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

SYSTEM_OUTLINE = "Sen deneyimli bir teknik kitap editorusun. Verilen konu ve amac dogrultusunda ayrintili bir bolum outline'i hazirlayacaksin. Tek H1 baslik, en az 5 H2 alt bolum, kod orneklerinin yer alacagi bolumleri isaretle."
SYSTEM_CHAPTER = "Sen deneyimli bir teknik kitap yazari ve pedagojik icerik uzmanisin. Verilen outline gore eksiksiz bir bolum Markdown metni uret. 1) YAML front matter ILE BASLA. 2) Basliklar elle numaralandirilmasin. 3) Her kod blogundan once <!-- CODE_META ... --> blogu olsun. 4) Java kodu, dosya adi class adiyla uyumlu. 5) blockquote pedagojik kutu. 6) Sonunda ozet, terim, soru, alistirma."

def stream_chat(messages, max_tokens=8192):
    payload = {
        "model": MODEL, "messages": messages,
        "max_tokens": max_tokens, "temperature": 0.7, "stream": True,
    }
    full_text = ""
    chunk_count = 0
    try:
        resp = requests.post(f"{BASE_URL}/chat/completions", headers=HEADERS, json=payload, stream=True, timeout=600)
        if resp.status_code != 200:
            return f"ERROR HTTP {resp.status_code}: {resp.text[:200]}"
        for line in resp.iter_lines(decode_unicode=True):
            if line and line.startswith("data: ") and line != "data: [DONE]":
                try:
                    d = json.loads(line[6:])
                    delta = d.get("choices", [{}])[0].get("delta", {}).get("content", "")
                    if delta:
                        full_text += delta
                        chunk_count += 1
                except json.JSONDecodeError:
                    pass
        return full_text
    except Exception as e:
        return f"ERROR EXCEPTION: {e}"

CHAPTERS = [
    ("bolum-09", "Diziler ve Cok Boyutlu Veri Yapilari", "Tek ve cok boyutlu dizi kullanimini, dizi islemlerini ve dizi tabanli algoritmalari ogretmek"),
    ("bolum-10", "String Islemleri ve Metin Problemleri", "String sinifi metodlari, metin manipulasyonu ve karakter islemlerini ogretmek"),
    ("bolum-11", "Matematiksel Yardimcilar ve Rastgelelik", "Math sinifi, random sayi uretimi ve matematiksel problem cozme yaklasimlarini ogretmek"),
]

pipe = AuthoringPipeline(root)
total_ok, total_err = 0, 0

for ch_id, title, purpose in CHAPTERS:
    sys.stderr.write(f"\n{'='*60}\n=== {ch_id}: {title}\n")
    sys.stderr.flush()
    t_start = time.time()

    # Seed
    seed_p = root / "chapters" / ch_id / "seed" / "seed_v001.yaml"
    if not seed_p.exists():
        pipe.seed(ch_id, purpose=purpose)
        sys.stderr.write(f"  Seed OK\n")

    # Outline
    outline_p = root / "chapters" / ch_id / "outline_versions" / "v001.md"
    if not outline_p.exists():
        sys.stderr.write(f"  Outline... ")
        sys.stderr.flush()
        t1 = time.time()
        result = stream_chat([
            {"role": "system", "content": SYSTEM_OUTLINE},
            {"role": "user", "content": f"Konu: {title}\nAmac: {purpose}\nAyrintili outline hazirla."},
        ], max_tokens=4096)
        t2 = time.time()
        if result.startswith("ERROR"):
            sys.stderr.write(f"HATA: {result[:100]}\n"); total_err += 1; continue
        pipe.paste_outline(ch_id, result)
        sys.stderr.write(f"{len(result)}c {t2-t1:.1f}s\n")
    else:
        sys.stderr.write(f"  Outline mevcut\n")

    # Chapter
    outline = outline_p.read_text(encoding="utf-8")
    sys.stderr.write(f"  Chapter... ")
    sys.stderr.flush()
    t3 = time.time()
    result = stream_chat([
        {"role": "system", "content": SYSTEM_CHAPTER},
        {"role": "user", "content": f"Bolum: {title}\nAmac: {purpose}\nOutline:\n{outline}\n\nEksiksiz bolum metnini uret."},
    ], max_tokens=8192)
    t4 = time.time()
    if result.startswith("ERROR"):
        sys.stderr.write(f"HATA: {result[:100]}\n"); total_err += 1; continue

    result = postprocess(result, ch_id, title)
    pipe.paste_draft(ch_id, result)
    pipe.advance(ch_id, "full_text_pasted")

    total = time.time() - t_start
    sys.stderr.write(f"OK {len(result)}c {t4-t3:.1f}s (toplam:{total:.1f}s)\n")
    sys.stdout.write(f"OK:{ch_id}|{len(result)}c|{total:.1f}s\n")
    sys.stdout.flush()
    total_ok += 1

sys.stderr.write(f"\n=== BATCH: {total_ok} OK, {total_err} HATA ===\n")
