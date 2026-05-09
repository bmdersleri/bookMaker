"""
token_analysis.py — bookMaker token optimizasyon analizi
"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHAPTERS_DIR = ROOT / "chapters"

CHAPTER_ORDER = [
    "bolum-01","bolum-02","bolum-03","bolum-04","bolum-05","bolum-06",
    "bolum-07","bolum-08","bolum-09","bolum-10","bolum-11",
    "bolum-12","bolum-13","bolum-14","bolum-15","bolum-16",
    "bolum-17","bolum-18","bolum-19","bolum-20","bolum-21",
    "bolum-22","bolum-23","ek-a","ek-b","ek-c","ek-d",
]

# Yaklasik token donusum: Turkce icin ~3.8 chars/token
CHARS_PER_TOKEN = 3.8

# DeepSeek fiyatlandirma (yaklasik)
COST_INPUT_PER_1K = 0.00014   # $/1K input tokens
COST_OUTPUT_PER_1K = 0.00028  # $/1K output tokens

# Mevcut system prompt
SYSTEM_PROMPT = (
    "Sen deneyimli bir teknik kitap yazari ve pedagojik icerik uzmanisin. "
    "Verilen konu icin once ayrintili bir outline, sonra bu outline'a gore "
    "eksiksiz bir bolum metni ureteceksin.\n\n"
    "Once OZET_BOLUM_BASLIGI ve altinda outline'i YAML listesi olarak yaz.\n"
    "Sonra -- BOLUM_METNI basligi altinda tam Markdown bolumunu yaz.\n\n"
    "Sen deneyimli bir teknik kitap yazari ve pedagojik icerik uzmanisin. "
    "Verilen outline gore eksiksiz bir bolum Markdown metni ureteceksin.\n\n"
    "Kurallar:\n"
    "1. YAML front matter ILE BASLA (title, subtitle, author, date, lang vb. tum alanlar).\n"
    "2. Basliklar elle numaralandirilmasin (sadece #, ##, ### kullan).\n"
    "3. Her kod blogundan once <!-- CODE_META ... --> blogu olsun.\n"
    "4. Kod ornekleri Java olsun, dosya adi public class adiyla uyumlu olsun.\n"
    "5. Pedagogik kutular icin blockquote kullan.\n"
    "6. Bolum sonunda ozet, terim sozlugu, sorular ve alistirmalar olsun.\n"
    "7. Her ana bolum icin 1-2 Mermaid diyagrami ekle.\n"
    "8. Bolum en az 12000 karakter olmali."
)


def analyze_chapters():
    """Her bolumu analiz et."""
    data = []
    for ch in CHAPTER_ORDER:
        path = CHAPTERS_DIR / ch / "draft_versions" / "v001.md"
        if not path.exists():
            print(f"  [UYARI] {ch} bulunamadi")
            continue
        
        text = path.read_text(encoding="utf-8")
        total_chars = len(text)
        total_tokens = round(total_chars / CHARS_PER_TOKEN)
        
        # Front matter
        fm_match = re.match(r'^---\n(.*?)\n---', text, re.DOTALL)
        fm_chars = len(fm_match.group(0)) if fm_match else 0
        fm_tokens = round(fm_chars / CHARS_PER_TOKEN)
        
        # Kod bloklari
        code_blocks = re.findall(r'```java\n(.*?)```', text, re.DOTALL)
        code_block_count = len(code_blocks)
        code_chars = sum(len(b) for b in code_blocks)
        code_tokens = round(code_chars / CHARS_PER_TOKEN)
        
        # CODE_META
        code_meta_count = len(re.findall(r'<!-- CODE_META.*?-->', text, re.DOTALL))
        code_meta_chars = sum(len(m) for m in re.findall(r'<!-- CODE_META.*?-->', text, re.DOTALL))
        code_meta_tokens = round(code_meta_chars / CHARS_PER_TOKEN)
        
        # Mermaid
        mermaid_count = len(re.findall(r'```mermaid', text))
        
        data.append({
            'name': ch,
            'total_chars': total_chars,
            'total_tokens': total_tokens,
            'fm_chars': fm_chars,
            'fm_tokens': fm_tokens,
            'code_blocks': code_block_count,
            'code_chars': code_chars,
            'code_tokens': code_tokens,
            'code_meta': code_meta_count,
            'code_meta_tokens': code_meta_tokens,
            'mermaid': mermaid_count,
        })
    
    return data


def print_analysis(data):
    """Analiz sonuclarini yazdir."""
    if not data:
        return
    
    # Ozet istatistikler
    totals = {
        'chars': sum(d['total_chars'] for d in data),
        'tokens': sum(d['total_tokens'] for d in data),
        'fm_chars': sum(d['fm_chars'] for d in data),
        'code_chars': sum(d['code_chars'] for d in data),
        'code_meta_tokens': sum(d['code_meta_tokens'] for d in data),
        'code_blocks': sum(d['code_blocks'] for d in data),
        'code_meta': sum(d['code_meta'] for d in data),
        'mermaid': sum(d['mermaid'] for d in data),
    }
    avg_chars = totals['chars'] // len(data)
    
    print("=" * 65)
    print("  bookMaker — TOKEN OPTIMIZASYONU ANALIZI")
    print("=" * 65)
    print()
    
    print(f"  Analiz edilen bolum: {len(data)}")
    print(f"  Toplam karakter:     {totals['chars']:>8,}")
    print(f"  Toplam token (tah.): {totals['tokens']:>8,}")
    print(f"  Ortalama/bolum:      {avg_chars:>8,} chars (~{round(avg_chars/CHARS_PER_TOKEN):,} tokens)")
    print()
    
    # 1. Bilesen dagilimi
    print("-" * 65)
    print("  1. TOKEN DAGILIMI (ortalama bolum)")
    print("-" * 65)
    
    avg_fm = totals['fm_chars'] // len(data)
    avg_code = totals['code_chars'] // len(data)
    avg_cmeta = totals['code_meta_tokens'] * CHARS_PER_TOKEN // len(data)
    avg_text_chars = avg_chars - avg_fm - avg_code - avg_cmeta
    
    print(f"     Metin/icerik:     {avg_text_chars:>7,} chars ({round(avg_text_chars/CHARS_PER_TOKEN):>4,} tok)  %{avg_text_chars*100//avg_chars}")
    print(f"     Front matter:     {avg_fm:>7,} chars ({round(avg_fm/CHARS_PER_TOKEN):>4,} tok)  %{avg_fm*100//avg_chars}")
    print(f"     Kod bloklari:     {avg_code:>7,} chars ({round(avg_code/CHARS_PER_TOKEN):>4,} tok)  %{avg_code*100//avg_chars}")
    print(f"     CODE_META:        {avg_cmeta:>7,} chars ({round(avg_cmeta/CHARS_PER_TOKEN):>4,} tok)  %{avg_cmeta*100//avg_chars}")
    print()
    
    # 2. Maliyet analizi
    print("-" * 65)
    print("  2. MALIYET ANALIZI (DeepSeek deepseek-chat)")
    print("-" * 65)
    
    system_tokens = round(len(SYSTEM_PROMPT) / CHARS_PER_TOKEN)
    user_tokens = 50  # title + purpose
    
    avg_output_tokens = round(avg_chars / CHARS_PER_TOKEN)
    max_chars = max(d['total_chars'] for d in data)
    max_tokens = round(max_chars / CHARS_PER_TOKEN)
    
    # Combined (mevcut)
    cost_input = (system_tokens + user_tokens) * COST_INPUT_PER_1K / 1000
    cost_output_avg = avg_output_tokens * COST_OUTPUT_PER_1K / 1000
    cost_per_chapter_avg = cost_input + cost_output_avg
    
    cost_output_max = max_tokens * COST_OUTPUT_PER_1K / 1000
    cost_per_chapter_max = cost_input + cost_output_max
    
    print(f"     System prompt:    ~{system_tokens} tokens")
    print(f"     User prompt:      ~{user_tokens} tokens")
    print(f"     Toplam input:     ~{system_tokens + user_tokens} tokens/cagri")
    print(f"     Output avg:       ~{avg_output_tokens:,} tokens")
    print(f"     Output max:       ~{max_tokens:,} tokens (B21)")
    print()
    print(f"     Maliyet/bolum:    ~${cost_per_chapter_avg:.5f} (avg)")
    print(f"     Maliyet/bolum:    ~${cost_per_chapter_max:.5f} (max)")
    print(f"     Maliyet/27 bolum: ~${cost_per_chapter_avg * 27:.4f} (avg)")
    print()
    
    # Iki asamali karsilastirma
    outline_tokens = 1400  # tahmini
    cost_two_step_input = (system_tokens + user_tokens) * 2 * COST_INPUT_PER_1K / 1000
    cost_two_step_output = (outline_tokens + avg_output_tokens) * COST_OUTPUT_PER_1K / 1000
    cost_two_step = cost_two_step_input + cost_two_step_output
    
    print(f"     Iki asamali:      ~${cost_two_step:.5f}/bolum (%{((cost_two_step/cost_per_chapter_avg)-1)*100:.0f} pahali)")
    print(f"     Combined:         ~${cost_per_chapter_avg:.5f}/bolum")
    print()
    
    # 3. Iyilestirme senaryolari
    print("-" * 65)
    print("  3. IYILESTIRME SENARYOLARI")
    print("-" * 65)
    print()
    
    # 3a. System prompt kisaltma
    print("  A) System Prompt Optimizasyonu")
    print("     ----------------------------------------")
    opt_prompt_tokens = 100  # hedef
    saved_input = system_tokens - opt_prompt_tokens
    saved_input_total = saved_input * 27
    print(f"     Mevcut:    {system_tokens} tokens/cagri")
    print(f"     Hedef:     {opt_prompt_tokens} tokens/cagri")
    print(f"     Kazanc:    {saved_input} tok/cagri x 27 = {saved_input_total:,} tok")
    print(f"     Tasarruf:  ${saved_input_total * COST_INPUT_PER_1K / 1000:.5f}")
    print()
    
    # 3b. max_tokens optimizasyonu
    print("  B) max_tokens Optimizasyonu")
    print("     ----------------------------------------")
    print(f"     Mevcut:    max_tokens=12288 (~49K chars) — tum bolumler icin")
    print(f"     Gereken:   max(ortalama*1.5, maks) = ~{max(round(avg_chars/CHARS_PER_TOKEN*1.5), max_tokens):,} tokens")
    print(f"     En buyuk:  B21 = {max_tokens:,} tokens (47K chars)")
    print(f"     Oneri:     max_tokens=8192 kucuk bolumler, 12288 devam")
    print()
    
    # 3c. Front matter kucultme
    avg_fm_tokens = round(avg_fm / CHARS_PER_TOKEN)
    opt_fm_tokens = 60  # ~250 chars
    saved_fm = avg_fm_tokens - opt_fm_tokens
    saved_fm_total = saved_fm * len(data)
    print(f"  C) Front Matter Optimizasyonu")
    print("     ----------------------------------------")
    print(f"     Mevcut:    ~{avg_fm_tokens} tokens/bolum")
    print(f"     Hedef:     ~{opt_fm_tokens} tokens/bolum (10 temel alan)")
    print(f"     Kazanc:    {saved_fm} tok/bolum x {len(data)} = {saved_fm_total:,} tok")
    print(f"     Tasarruf:  ${saved_fm_total * COST_OUTPUT_PER_1K / 1000:.5f}")
    print()
    
    # 3d. CODE_META verimliligi
    avg_cmeta_tokens_actual = totals['code_meta_tokens'] // len(data)
    opt_cmeta_tokens = round(12 * 50 / CHARS_PER_TOKEN)  # 12 blok x 50 chars
    saved_cmeta = avg_cmeta_tokens_actual - opt_cmeta_tokens
    saved_cmeta_total = saved_cmeta * len(data)
    print(f"  D) CODE_META Optimizasyonu")
    print("     ----------------------------------------")
    print(f"     Mevcut:    ~{avg_cmeta_tokens_actual} tokens/bolum ({totals['code_meta']} blok)")
    print(f"     Hedef:     ~{opt_cmeta_tokens} tokens/bolum (kisa format)")
    print(f"     Kazanc:    {saved_cmeta} tok/bolum x {len(data)} = {saved_cmeta_total:,} tok")
    print(f"     Tasarruf:  ${saved_cmeta_total * COST_OUTPUT_PER_1K / 1000:.5f}")
    print()
    
    # TOPLAM
    print("  E) TOPLAM IYILESTIRME")
    print("     ----------------------------------------")
    total_saved_input = saved_input * 27
    total_saved_output = saved_fm_total + saved_cmeta_total
    total_saved_all = total_saved_input + total_saved_output
    total_cost = (total_saved_input * COST_INPUT_PER_1K + total_saved_output * COST_OUTPUT_PER_1K) / 1000
    total_hiz = round(total_saved_all / (system_tokens + user_tokens + avg_output_tokens) * 100)
    print(f"     Input kazanci:     {total_saved_input:>6,} tokens")
    print(f"     Output kazanci:    {total_saved_output:>6,} tokens")
    print(f"     Toplam token:      {total_saved_all:>6,} tokens")
    print(f"     Maliyet kazanci:   ~${total_cost:.5f}")
    print(f"     Hiz kazanci:       ~%{total_hiz} daha hizli")
    print(f"     (Ana kazanc: gereksiz output token\'larini azaltmak)")
    print()
    
    # 4. Bolum olceklendirme
    print("-" * 65)
    print("  4. BOLUM OLCEKLENDIRME ONERILERI")
    print("-" * 65)
    print()
    
    data.sort(key=lambda d: d['total_chars'], reverse=True)
    print("     En buyuk 5 bolum:")
    for d in data[:5]:
        print(f"       {d['name']}: {d['total_chars']:>6,} chars ({d['total_tokens']:>5,} tok)")
    print()
    print("     En kucuk 5 bolum:")
    for d in data[-5:]:
        print(f"       {d['name']}: {d['total_chars']:>6,} chars ({d['total_tokens']:>5,} tok)")
    print()
    
    # 5. Kod ve Mermaid
    print("-" * 65)
    print("  5. KOD VE MERMAID ISTATISTIKLERI")
    print("-" * 65)
    print()
    print(f"     Kod bloklari:      {totals['code_blocks']} blok ({totals['code_chars']:,} chars)")
    print(f"     CODE_META:         {totals['code_meta']} blok")
    print(f"     Mermaid:           {totals['mermaid']} diyagram")
    print()
    
    # Mermaid sorunu
    if totals['mermaid'] == 0:
        print("  [!] UYARI: Hic Mermaid diyagrami bulunamadi!")
        print("      Sistem prompt'ta talimat olmasina ragmen LLM Mermaid")
        print("      olusturmuyor. Bunun token optimizasyonu acisindan")
        print("      iki yuzu var:")
        print("      - EKSI: Gorsel icerik yok, kitap kalitesi dusuk")
        print("      - ARTI: ~200-400 tok/bolum daha az output")
        print()


if __name__ == "__main__":
    data = analyze_chapters()
    print_analysis(data)
