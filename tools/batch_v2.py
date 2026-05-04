"""
batch_v2.py — Optimize Edilmis Kitap Bolum Uretim Scripti

Iyilestirmeler (P1-P12):
  P1:  Tek script, sirali islem
  P2:  requests streaming
  P3:  Retry mekanizmasi (3 deneme, backoff)
  P4:  Gecici dosya + atomik tasima
  P5:  Progress gostergesi (5sn)
  P6:  Tek prompt modu (varsayilan)
  P7:  Detayli hata raporlama
  P8:  Resume destegi (batch_progress.json)
  P9:  Outline token optimizasyonu (2048)
  P10: Buyuk bolum uyarisi
  P11: On API testi (preflight)
  P12: Combined prompt + BOLUM_METNI ayristirma

Kullanim:
  python tools/batch_v2.py              # varsayilan: combined prompt
  python tools/batch_v2.py --two-step   # iki asamali (outline+chapter ayri)
  python tools/batch_v2.py --batch 3    # sadece 3. batch
"""

from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path

# --- Yapilandirma ---
API_KEY = "sk-98a85ecced414d499d34caf73a09b80d"
BASE_URL = "https://api.deepseek.com/v1"
MODEL = "deepseek-chat"
TIMEOUT = 600
MAX_RETRIES = 3
RETRY_DELAYS = [5, 15, 45]  # saniye (ustel backoff)
PROGRESS_INTERVAL = 5  # saniye

# Proje kokunu bul
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

# Stdout/stderr encoding (Windows icin)
sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

import requests
from bookmaker.generation.postprocess import process as postprocess
from bookmaker.authoring.pipeline import AuthoringPipeline

# --- Sabit Promptlar ---
SYSTEM_OUTLINE = (
    "Sen deneyimli bir teknik kitap editorusun. "
    "Verilen konu ve amac dogrultusunda ayrintili bir bolum outline'i hazirlayacaksin. "
    "Tek H1 baslik, en az 5 H2 alt bolum, kod orneklerinin yer alacagi bolumleri isaretle. "
    "Pedagojik akis: kavram -> ornek -> uygulama -> degerlendirme."
)

SYSTEM_CHAPTER = (
    "Sen deneyimli bir teknik kitap yazari ve pedagojik icerik uzmanisin. "
    "Verilen outline gore eksiksiz bir bolum Markdown metni ureteceksin.\n\n"
    "Kurallar:\n"
    "1. YAML front matter ILE BASLA (title, subtitle, author, date, lang vb. tum alanlar).\n"
    "2. Basliklar elle numaralandirilmasin (sadece #, ##, ### kullan).\n"
    "3. Her kod blogundan once <!-- CODE_META ... --> blogu olsun.\n"
    "4. Kod ornekleri Java olsun, dosya adi public class adiyla uyumlu olsun.\n"
    "5. Pedagojik kutular icin blockquote kullan.\n"
    "6. Bolum sonunda ozet, terim sozlugu, sorular ve alistirmalar olsun.\n"
    "7. Her ana bolum icin 1-2 Mermaid diyagrami ekle (```mermaid ... ```).\n"
    "8. Bolum en az 12000 karakter olmali."
)

SYSTEM_COMBINED = (
    "Sen deneyimli bir teknik kitap yazari ve pedagojik icerik uzmanisin. "
    "Verilen konu icin once ayrintili bir outline, sonra bu outline'a gore "
    "eksiksiz bir bolum metni ureteceksin.\n\n"
    "Once OZET_BOLUM_BASLIGI ve altinda outline'i YAML listesi olarak yaz.\n"
    "Sonra — BOLUM_METNI basligi altinda tam Markdown bolumunu yaz.\n\n"
    + SYSTEM_CHAPTER
)

# --- Bolum Listesi (batch'lere ayrilmis) ---
BATCHES = {
    2: [
        ("bolum-12", "Tarih ve Zaman Islemleri",
         "LocalDate, LocalTime, LocalDateTime, DateTimeFormatter ve tarih/zaman hesaplamalarini ogretmek"),
        ("bolum-13", "Paketler, import Kullanimi ve Proje Duzeni",
         "Java paket sistemi, import mekanizmasi ve moduler proje yapilandirmasini ogretmek"),
        ("bolum-14", "Koleksiyonlar ve Dinamik Veri Yonetimi",
         "ArrayList, LinkedList, HashMap, HashSet ve koleksiyon algoritmalarini ogretmek"),
        ("bolum-15", "Hata Yonetimi ve Dayanikli Programlama",
         "try-catch-finally, checked/unchecked exception, custom exception ve hata yonetim stratejilerini ogretmek"),
        ("bolum-16", "Dosya Islemleri ve Kalici Veri Saklama",
         "File, FileReader/Writer, BufferedReader/BufferedWriter, NIO.2 ve serilestirmeyi ogretmek"),
    ],
    3: [
        ("bolum-17", "Sinif, Nesne, Constructor ve Kapsulleme",
         "Sinif tanimlama, nesne olusturma, constructor cesitleri, this anahtar kelimesi, erisim belirtecleri, getter/setter ve encapsulation prensibini ogretmek"),
        ("bolum-18", "Kalitim ve Interface'e Kisa On Bakis",
         "extends, super, override, abstract class, interface ve polymorphism temellerini ogretmek"),
        ("bolum-19", "GUI Programlamaya Giris ve Swing Arayuz Tasarimi",
         "Swing bilesenleri, JFrame, JPanel, layout yoneticileri ve basit GUI uygulamasi yapimini ogretmek"),
        ("bolum-20", "Temel Swing Bilesenleri, Olay Yonetimi ve Form Dogrulama",
         "JButton, JTextField, JLabel, ActionListener, KeyListener, form dogrulama ve kullanici girdisi islemeyi ogretmek"),
        ("bolum-21", "Liste, Tablo, Menu ve Diyaloglarla GUI Veri Sunumu",
         "JList, JTable, JMenuBar, JDialog, JOptionPane ve veri goruntuleme bilesenlerini ogretmek"),
    ],
    4: [
        ("bolum-22", "JDBC ile Veritabani Programlamaya Giris",
         "JDBC mimarisi, Connection/Statement/ResultSet, SQL sorgulama, CRUD islemleri ve prepared statement'i ogretmek"),
        ("bolum-23", "Butunlesik Uygulama ve Final Proje Rehberi",
         "Ogrenilen tum konulari birlestiren kapsamli bir uygulama ve final proje kilavuzu sunmak"),
        ("ek-a", "Sik Yapilan Java Hatalari ve Cozum Rehberi",
         "Yaygin derleme ve calisma zamani hatalarini, cozum yontemlerini ve debugging yaklasimlarini ogretmek"),
        ("ek-b", "JavaFX'e Kisa Bakis",
         "JavaFX mimarisi, Scene Builder, FXML, kontroller ve Swing'den JavaFX'e gecis konularina giris yapmak"),
        ("ek-c", "Mini Proje Fikirleri ve Rubrikler",
         "Farkli seviyelerde mini projeler, degerlendirme rubrikleri ve proje teslim kurallarini sunmak"),
        ("ek-d", "Java Programlama Kontrol Rehberi, Sik Hatalar ve Kod Kalitesi",
         "Kod kalite standartlari, yaygin hata desenleri, kod review checklist ve en iyi uygulamalari ogretmek"),
    ],
}


# ============================================================
# P3: Retry Mekanizmasi
# ============================================================
def stream_with_retry(messages, max_tokens=8192, label=""):
    """Streaming API cagrisi — P3: 3 deneme, ustel backoff."""
    last_error = ""
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            result = _do_stream(messages, max_tokens, label)
            if result is not None and not result.startswith("ERROR"):
                return result
            last_error = result or "Bilinmeyen hata"
            if attempt < MAX_RETRIES:
                delay = RETRY_DELAYS[attempt - 1]
                log(f"  [Retry {attempt}/{MAX_RETRIES}] {delay}s sonra yeniden deneniyor... (hata: {last_error[:80]})")
                time.sleep(delay)
        except Exception as e:
            last_error = str(e)
            if attempt < MAX_RETRIES:
                delay = RETRY_DELAYS[attempt - 1]
                log(f"  [Retry {attempt}/{MAX_RETRIES}] {delay}s sonra yeniden deneniyor... (hata: {e})")
                time.sleep(delay)
    return f"ERROR ALL RETRIES FAILED: {last_error}"


def _do_stream(messages, max_tokens, label=""):
    """Tek bir streaming API cagrisi — P2: requests."""
    payload = {
        "model": MODEL,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": 0.7,
        "stream": True,
    }
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    resp = requests.post(
        f"{BASE_URL}/chat/completions",
        headers=headers,
        json=payload,
        stream=True,
        timeout=TIMEOUT,
    )

    if resp.status_code != 200:
        return f"ERROR HTTP {resp.status_code}: {resp.text[:300]}"

    full_text = ""
    chunk_count = 0
    t0 = time.time()
    last_progress = t0

    for line in resp.iter_lines(decode_unicode=True):
        if line and line.startswith("data: ") and line != "data: [DONE]":
            try:
                data = json.loads(line[6:])
                delta = data.get("choices", [{}])[0].get("delta", {}).get("content", "")
                if delta:
                    full_text += delta
                    chunk_count += 1
                    # P5: Periyodik progress
                    now = time.time()
                    if now - last_progress >= PROGRESS_INTERVAL:
                        elapsed = now - t0
                        sys.stderr.write(
                            f"\r    [progress] {chunk_count} chunks, "
                            f"{len(full_text):,} chars, {elapsed:.0f}s    "
                        )
                        sys.stderr.flush()
                        last_progress = now
            except json.JSONDecodeError:
                pass

    elapsed = time.time() - t0
    return full_text


# ============================================================
# P4: Gecici Dosya + Atomik Tasima
# ============================================================
def atomic_write(filepath, content):
    """P4: Once .tmp, sonra rename (atomik)."""
    tmp_path = filepath.with_suffix(filepath.suffix + ".tmp")
    tmp_path.write_text(content, encoding="utf-8")
    tmp_path.replace(filepath)  # atomik rename


# ============================================================
# P7: Detayli Hata Raporlama
# ============================================================
ERROR_LOG = ROOT / "build" / "reports" / "batch_errors.json"
PROGRESS_FILE = ROOT / "build" / "reports" / "batch_progress.json"
os.makedirs(ROOT / "build" / "reports", exist_ok=True)


def log(msg, end="\n"):
    """Stderr'e log yaz."""
    sys.stderr.write(msg + end)
    sys.stderr.flush()


def log_error(chapter_id, title, phase, error_msg, elapsed):
    """P7: Hatayi error log'a kaydet."""
    errors = []
    if ERROR_LOG.exists():
        try:
            errors = json.loads(ERROR_LOG.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            errors = []
    errors.append({
        "chapter_id": chapter_id,
        "title": title,
        "phase": phase,
        "error": str(error_msg)[:500],
        "elapsed_s": round(elapsed, 1),
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
    })
    ERROR_LOG.write_text(
        json.dumps(errors, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


# ============================================================
# P11: On API Testi (Pre-flight Check)
# ============================================================
def preflight_check():
    """P11: Batch basinda API baglantisini dogrula."""
    log(f"[Preflight] API baglantisi test ediliyor...", end="")
    try:
        payload = {
            "model": MODEL,
            "messages": [{"role": "user", "content": "Reply OK"}],
            "max_tokens": 5,
        }
        headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
        resp = requests.post(
            f"{BASE_URL}/chat/completions",
            headers=headers, json=payload, timeout=30,
        )
        elapsed = resp.elapsed.total_seconds()
        if resp.status_code == 200:
            log(f" OK ({elapsed:.1f}s)")
            return True
        else:
            log(f" FAIL (HTTP {resp.status_code}: {resp.text[:100]})")
            return False
    except Exception as e:
        log(f" FAIL ({e})")
        return False


# ============================================================
# P8: Resume Destegi (batch_progress.json)
# ============================================================
def save_progress(batch_num, ch_id, title, status, chars=0, elapsed=0):
    """P8: Ilerleme durumunu kaydet."""
    progress = {}
    if PROGRESS_FILE.exists():
        try:
            progress = json.loads(PROGRESS_FILE.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            progress = {}
    if str(batch_num) not in progress:
        progress[str(batch_num)] = {"chapters": {}}
    progress[str(batch_num)]["chapters"][ch_id] = {
        "title": title,
        "status": status,
        "chars": chars,
        "elapsed_s": round(elapsed, 1),
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
    }
    PROGRESS_FILE.write_text(
        json.dumps(progress, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


def load_progress(batch_num):
    """P8: Kayitli ilerlemeyi yukle. Tamamlanan chapter_id seti doner."""
    done = set()
    if PROGRESS_FILE.exists():
        try:
            progress = json.loads(PROGRESS_FILE.read_text(encoding="utf-8"))
            batch_data = progress.get(str(batch_num), {}).get("chapters", {})
            for ch_id, info in batch_data.items():
                if info.get("status") == "OK":
                    done.add(ch_id)
        except (json.JSONDecodeError, OSError):
            pass
    return done


# ============================================================
# P12: Combined Prompt — BOLUM_METNI Ayristirma
# ============================================================
def extract_chapter_from_combined(combined_text):
    """P12: Combined ciktidan sadece bolum metnini cikar.
    
    Combined cikti su formatta beklenir:
      OZET_BOLUM_BASLIGI
      ... outline ...
      BOLUM_METNI
      ... chapter ...
    
    Eger ayrac bulunamazsa, tum metni dondur.
    """
    marker = "BOLUM_METNI"
    idx = combined_text.find(marker)
    if idx != -1:
        return combined_text[idx + len(marker):].strip()
    # Alternatif: BOLUM_METNI veya benzeri bir baslik ara
    import re
    m = re.search(r"#+\s*BOLUM[_\s]?METNI", combined_text)
    if m:
        return combined_text[m.end():].strip()
    # Ayrac yoksa tum metni dondur
    return combined_text


# ============================================================
# P6: Tek Prompt Modu
# ============================================================
def generate_combined(chapter_id, title, purpose):
    """P6: Tek API cagrisinda outline + chapter."""
    user = (
        f"Konu: {title}\n"
        f"Amac: {purpose}\n\n"
        "Once ayrintili bir outline hazirla (OZET_BOLUM_BASLIGI altinda), "
        "sonra bu outline'a gore eksiksiz bolum metnini yaz (BOLUM_METNI altinda)."
    )
    return stream_with_retry(
        [
            {"role": "system", "content": SYSTEM_COMBINED},
            {"role": "user", "content": user},
        ],
        max_tokens=12288,
        label=f"{chapter_id} combined",
    )


def generate_outline(chapter_id, title, purpose):
    """Outline uret. P9: max_tokens=2048 (daha hizli)."""
    return stream_with_retry(
        [
            {"role": "system", "content": SYSTEM_OUTLINE},
            {"role": "user", "content": f"Konu: {title}\nAmac: {purpose}\nAyrintili outline hazirla."},
        ],
        max_tokens=2048,
        label=f"{chapter_id} outline",
    )


def generate_chapter_text(chapter_id, title, purpose, outline):
    """Chapter text uret."""
    user = (
        f"Bolum: {title}\n\n"
        f"Amac: {purpose}\n\n"
        f"Outline:\n{outline}\n\n"
        "Yukaridaki outline'a gore eksiksiz bolum metnini uret."
    )
    return stream_with_retry(
        [
            {"role": "system", "content": SYSTEM_CHAPTER},
            {"role": "user", "content": user},
        ],
        max_tokens=8192,
        label=f"{chapter_id} chapter",
    )


# ============================================================
# Ana Batch Fonksiyonu
# ============================================================
def process_chapter(ch_id, title, purpose, use_combined=True):
    """Tek bolumu isle: seed -> (combined/outline+chapter) -> postprocess -> kaydet.
    
    P1:  Bu fonksiyon bitmeden bir sonraki chapter'a gecmez.
    P10: Outline > 5000 chars ise uyari ver.
    P12: Varsayilan olarak combined prompt kullan.
    """
    pipe = AuthoringPipeline(ROOT)
    chapter_root = ROOT / "chapters" / ch_id

    log(f"\n{'='*60}")
    log(f"BASLIYOR: {ch_id} - {title}")

    t_start = time.time()

    try:
        # --- Seed ---
        seed_p = chapter_root / "seed" / "seed_v001.yaml"
        if not seed_p.exists():
            pipe.seed(ch_id, purpose=purpose)
            log(f"  [Seed] olusturuldu")
        else:
            log(f"  [Seed] mevcut")

        # --- P12: Combined prompt (varsayilan) ---
        if use_combined:
            log(f"  [Combined] outline+chapter tek cagrida...")
            t1 = time.time()
            combined = generate_combined(ch_id, title, purpose)
            if combined.startswith("ERROR"):
                raise RuntimeError(combined)
            elapsed = time.time() - t1
            log(f"  [Combined] {len(combined):,} chars, {elapsed:.1f}s")

            # P12: BOLUM_METNI ayristir
            chapter_text = extract_chapter_from_combined(combined)
            log(f"  [Extract] chapter: {len(chapter_text):,} chars (from {len(combined):,} combined)")

        # --- Iki asamali (outline + chapter) ---
        else:
            outline_p = chapter_root / "outline_versions" / "v001.md"

            if not outline_p.exists():
                log(f"  [Outline] uretiliyor...", end="")
                t1 = time.time()
                outline = generate_outline(ch_id, title, purpose)
                if outline.startswith("ERROR"):
                    raise RuntimeError(outline)
                elapsed = time.time() - t1
                atomic_write(outline_p, outline)
                pipe.advance(ch_id, "outline_pasted")
                log(f" {len(outline):,} chars, {elapsed:.1f}s")
            else:
                outline = outline_p.read_text(encoding="utf-8")
                log(f"  [Outline] mevcut ({len(outline):,} chars)")

            # P10: Buyuk bolum uyarisi
            if len(outline) > 5000:
                log(f"  [Uyari] Genis outline ({len(outline):,} chars) — bolum uzun olabilir")

            log(f"  [Chapter] uretiliyor...", end="")
            t2 = time.time()
            chapter_text = generate_chapter_text(ch_id, title, purpose, outline)
            if chapter_text.startswith("ERROR"):
                raise RuntimeError(chapter_text)
            elapsed = time.time() - t2

        # --- Post-process (F-001/F-002/F-003/F-006) ---
        chapter_text = postprocess(chapter_text, ch_id, title)
        log(f"  [PostProcess] {len(chapter_text):,} chars")

        # --- P4: Gecici dosya + atomik kaydet ---
        draft_p = chapter_root / "draft_versions" / "v001.md"
        atomic_write(draft_p, chapter_text)

        # Pipeline state guncelle
        pipe.advance(ch_id, "full_text_pasted")

        total_elapsed = time.time() - t_start
        log(f"  [OK] {len(chapter_text):,} chars, {total_elapsed:.1f}s")
        return True, len(chapter_text), total_elapsed

    except Exception as e:
        total_elapsed = time.time() - t_start
        log(f"  [HATA] {e}")
        log_error(ch_id, title, "chapter", str(e), total_elapsed)
        return False, 0, total_elapsed


def run_batch(batch_num, use_combined=True):
    """Bir batch'i calistir.
    
    P8:  Resume destegi — once tamamlanan chapter'lari kontrol et.
    P11: Batch basinda API baglantisi test et.
    """
    chapters = BATCHES.get(batch_num)
    if not chapters:
        log(f"Batch {batch_num} bulunamadi. Secenekler: {list(BATCHES.keys())}")
        return

    log(f"\n{'#'*60}")
    log(f"# BATCH {batch_num} BASLIYOR ({len(chapters)} bolum)")
    log(f"{'#'*60}")

    # P11: Pre-flight check
    if not preflight_check():
        log(f"[HATA] API baglantisi basarisiz. Batch iptal.")
        return

    # P8: Resume — daha once tamamlanan chapter'lari bul
    done = load_progress(batch_num)
    if done:
        log(f"[Resume] {len(done)} bolum daha once tamamlanmis, atlaniyor.")
        remaining = [(c, t, p) for c, t, p in chapters if c not in done]
        if len(remaining) == 0:
            log(f"[Resume] Tum bolumler zaten tamamlanmis.")
            return
        log(f"[Resume] {len(remaining)}/{len(chapters)} bolum kaldi.")
        chapters = remaining

    results = []
    ok = 0
    err = 0

    for ch_id, title, purpose in chapters:
        # P1: Sadece bir bolum — bitene kadar bekle
        success, size, duration = process_chapter(ch_id, title, purpose, use_combined)
        results.append((ch_id, title, success, size, duration))
        if success:
            ok += 1
            # P8: Ilerlemeyi kaydet
            save_progress(batch_num, ch_id, title, "OK", size, duration)
        else:
            err += 1
            save_progress(batch_num, ch_id, title, "HATA", 0, duration)

    # Batch sonu raporu
    log(f"\n{'#'*60}")
    log(f"# BATCH {batch_num} RAPORU")
    log(f"{'#'*60}")
    for ch_id, title, success, size, duration in results:
        status = "OK" if success else "HATA"
        log(f"  {ch_id}: {status} — {size:,} chars, {duration:.1f}s")
    log(f"  Toplam: {ok} OK, {err} HATA")
    log(f"{'#'*60}")


# ============================================================
# CLI Girisi
# ============================================================
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Optimize edilmis batch bolum uretimi")
    parser.add_argument("--batch", type=int, default=0, help="Batch numarasi (2, 3, 4). 0 = tumu")
    parser.add_argument("--two-step", action="store_true", help="Iki asamali mod (outline+chapter ayri)")
    args = parser.parse_args()

    use_combined = not args.two_step

    log(f"batch_v2.py — Optimize Edilmis Batch Uretim")
    log(f"  Mod: {'Iki asamali (outline+chapter)' if args.two_step else 'P12: Combined (varsayilan)'}")
    log(f"  P8:  Resume aktif")
    log(f"  P9:  Outline max_tokens=2048")
    log(f"  P10: Buyuk bolum uyarisi aktif")
    log(f"  P11: Preflight kontrol aktif")
    log(f"  Retry: {MAX_RETRIES} deneme, backoff: {RETRY_DELAYS}")
    log(f"  Progress interval: {PROGRESS_INTERVAL}s")
    log(f"  Timeout: {TIMEOUT}s")
    log(f"")

    if args.batch > 0:
        run_batch(args.batch, use_combined)
    else:
        for b in sorted(BATCHES.keys()):
            run_batch(b, use_combined)
            log(f"\nBatch {b} tamam. 5sn ara veriliyor...")
            time.sleep(5)

    log(f"\nTum batch'ler tamamlandi. Error log: {ERROR_LOG}")
    log(f"Progress file: {PROGRESS_FILE}")
