"""Batch bolum uretimi - seed + outline + streaming chapter."""
import sys, time, json, httpx
from pathlib import Path

root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root))
sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

from bookmaker.generation.postprocess import process as postprocess
from bookmaker.authoring.pipeline import AuthoringPipeline

API_KEY = "sk-98a85ecced414d499d34caf73a09b80d"
BASE_URL = "https://api.deepseek.com/v1"
MODEL = "deepseek-chat"
TIMEOUT = 300

CHAPTERS = [
    # (id, title, purpose)
    ("bolum-08", "Metotlar, Overloading ve Ozyineleme",
     "Metot tanimlama, parametre gecisi, overload ve recursive metot yapisini ogretmek"),
    ("bolum-09", "Diziler ve Cok Boyutlu Veri Yapilari",
     "Tek ve cok boyutlu dizi kullanimini, dizi islemlerini ve dizi tabanli algoritmalari ogretmek"),
    ("bolum-10", "String Islemleri ve Metin Problemleri",
     "String sinifi metodlari, metin manipulasyonu ve karakter islemlerini ogretmek"),
    ("bolum-11", "Matematiksel Yardimcilar ve Rastgelelik",
     "Math sinifi, random sayi uretimi ve matematiksel problem cozme yaklasimlarini ogretmek"),
]

SYSTEM_OUTLINE = """Sen deneyimli bir teknik kitap editorusun.
Verilen konu ve amac dogrultusunda ayrintili bir bolum outline'i hazirlayacaksin.

Outline:
- Tek H1 baslik
- En az 5 H2 alt bolum
- Her H2 altinda gerekirse H3 detaylari
- Kod orneklerinin yer alacagi bolumleri isaretle
- Pedagojik akis: kavram -> ornek -> uygulama -> degerlendirme"""

SYSTEM_CHAPTER = """Sen deneyimli bir teknik kitap yazari ve pedagojik icerik uzmanisin.
Verilen outline gore eksiksiz bir bolum Markdown metni ureteceksin.

Kurallar:
1. YAML front matter ILE BASLA (title, subtitle, author, date, lang, documentclass vb).
2. Basliklar elle numaralandirilmasin (sadece # ve ## ve ### kullan).
3. Her kod blogundan once "<!-- CODE_META ... -->" blogu olsun.
4. Kod ornekleri Java olsun, dosya adi public class adiyla uyumlu olsun.
5. Pedagojik kutular icin blockquote kullan.
6. Bolum sonunda ozet, terim sozlugu, sorular ve alistirmalar olsun.
7. Her bolum en az 12000 karakter olmali.
8. Her ana bolum icin 1-2 Mermaid diyagrami ekle."""

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
}

def stream_chat(messages, max_tokens=8192):
    """Streaming API call."""
    payload = {
        "model": MODEL,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": 0.7,
        "stream": True,
    }
    full_text = ""
    chunk_count = 0
    try:
        with httpx.Client(timeout=TIMEOUT) as client:
            with client.stream("POST", f"{BASE_URL}/chat/completions", headers=HEADERS, json=payload) as resp:
                if resp.status_code != 200:
                    return f"ERROR HTTP {resp.status_code}: {resp.text[:200]}"
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
        return full_text
    except Exception as e:
        return f"ERROR EXCEPTION: {e}"

def generate_outline(chapter_id, title, purpose):
    """Generate outline via streaming."""
    user = f"Konu: {title}\nAmac: {purpose or 'Temel kavramlari ogretmek'}\nAyrintili bir outline hazirla."
    result = stream_chat([
        {"role": "system", "content": SYSTEM_OUTLINE},
        {"role": "user", "content": user},
    ], max_tokens=4096)
    return result

def generate_chapter_text(chapter_id, title, purpose, outline):
    """Generate chapter text via streaming."""
    user = (
        f"Bolum: {title}\n\n"
        f"Amac: {purpose or 'Temel kavramlari ogretmek'}\n\n"
        f"Outline:\n{outline}\n\n"
        "Yukaridaki outline'a gore eksiksiz bolum metnini uret."
    )
    result = stream_chat([
        {"role": "system", "content": SYSTEM_CHAPTER},
        {"role": "user", "content": user},
    ], max_tokens=8192)
    return result

pipe = AuthoringPipeline(root)
total_ok = 0
total_err = 0

for ch_id, title, purpose in CHAPTERS:
    sys.stderr.write(f"\n{'='*60}\n")
    sys.stderr.write(f"BASLIYOR: {ch_id} - {title}\n")
    sys.stderr.flush()
    t_start = time.time()

    # 1. Seed olustur (yoksa)
    seed_dir = root / "chapters" / ch_id / "seed"
    seed_p = seed_dir / "seed_v001.yaml"
    if not seed_p.exists():
        pipe.seed(ch_id, purpose=purpose)
        sys.stderr.write(f"  Seed olusturuldu\n")
    else:
        sys.stderr.write(f"  Seed mevcut\n")

    # 2. Outline olustur (yoksa)
    outline_p = root / "chapters" / ch_id / "outline_versions" / "v001.md"
    if not outline_p.exists():
        sys.stderr.write(f"  Outline uretiliyor... ")
        sys.stderr.flush()
        t1 = time.time()
        outline = generate_outline(ch_id, title, purpose)
        t2 = time.time()
        if outline.startswith("ERROR"):
            sys.stderr.write(f"HATA: {outline[:100]}\n")
            total_err += 1
            continue
        pipe.paste_outline(ch_id, outline)
        sys.stderr.write(f"{len(outline)} chars, {t2-t1:.1f}s\n")
    else:
        outline = outline_p.read_text(encoding="utf-8")
        sys.stderr.write(f"  Outline mevcut ({len(outline)} chars)\n")

    # 3. Chapter uret
    sys.stderr.write(f"  Chapter uretiliyor... ")
    sys.stderr.flush()
    t3 = time.time()
    chapter_text = generate_chapter_text(ch_id, title, purpose, outline)
    t4 = time.time()
    if chapter_text.startswith("ERROR"):
        sys.stderr.write(f"HATA: {chapter_text[:100]}\n")
        total_err += 1
        continue

    # 4. Post-process
    chapter_text = postprocess(chapter_text, ch_id, title)

    # 5. Kaydet
    pipe.paste_draft(ch_id, chapter_text)
    pipe.advance(ch_id, "full_text_pasted")

    total_elapsed = time.time() - t_start
    sys.stderr.write(f"  OK: {len(chapter_text)} chars, {total_elapsed:.1f}s\n")
    sys.stdout.write(f"OK:{ch_id}|chars:{len(chapter_text)}|time:{total_elapsed:.1f}s\n")
    sys.stdout.flush()
    total_ok += 1

sys.stderr.write(f"\n{'='*60}\n")
sys.stderr.write(f"BATCH SONU: {total_ok} OK, {total_err} HATA\n")
