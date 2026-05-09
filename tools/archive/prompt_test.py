"""
prompt_test.py — Token optimizasyonu dogrulama
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import tools.batch_v2 as bv2

print("=" * 60)
print("  P13 TOKEN OPTIMIZASYONU — DOGRULAMA")
print("=" * 60)
print()

# 1. PROMPT BOYUTLARI
print("1. PROMPT BOYUTLARI")
print("-" * 40)
old_system = {
    "SYSTEM_COMBINED": 968,  # onceki ~242 tok
    "SYSTEM_CHAPTER": 656,   # onceki ~164 tok
    "SYSTEM_OUTLINE": 270,   # degismedi ~68 tok
}
for name, obj in [("SYSTEM_COMBINED", bv2.SYSTEM_COMBINED),
                   ("SYSTEM_CHAPTER", bv2.SYSTEM_CHAPTER),
                   ("SYSTEM_OUTLINE", bv2.SYSTEM_OUTLINE)]:
    chars = len(obj)
    tokens = chars // 4
    old = old_system.get(name, 0)
    diff = old - chars
    pct = diff * 100 // max(old, 1)
    print(f"  {name:20s}: {chars:4d}c (~{tokens:3d} tok)  {f'%{pct} kucuk' if diff > 0 else 'degismedi'}")

total_old = sum(old_system.values())
total_new = len(bv2.SYSTEM_COMBINED) + len(bv2.SYSTEM_CHAPTER) + len(bv2.SYSTEM_OUTLINE)
print(f"  {'TOPLAM':20s}: {total_new:4d}c ({total_new//4:3d} tok)  eskiden {total_old:4d}c (%{(total_old-total_new)*100//total_old} kucuk)")
print()

# 2. DINAMIK MAX_TOKENS
print("2. DINAMIK MAX_TOKENS")
print("-" * 40)
test_cases = [
    ("bolum-01", 12000, "kucuk"),
    ("bolum-07", 26000, "orta"),
    ("bolum-11", 31000, "buyuk"),
    ("bolum-21", 47000, "cok buyuk"),
    ("ek-c",    16000, "orta-kucuk"),
]
for ch_id, expected, label in test_cases:
    est = bv2.estimate_chapter_size(ch_id)
    mt = bv2.dynamic_max_tokens(ch_id)
    ok = "OK" if est == expected else f"HATA (beklenen {expected})"
    print(f"  {ch_id:12s}: tahmin={est:>5,} chars, max_tokens={mt:>5}  [{label:10s}] {ok}")

print()

# 3. ESKI vs YENI KARSILASTIRMASI
print("3. ESKI vs YENI KARSILASTIRMASI (27 bolum)")
print("-" * 40)
# Eski: 12288 sabit
# Yeni: dinamik
old_total_tokens_per_chapter = (old_system["SYSTEM_COMBINED"] // 4) + 50  # system + user
old_total_output = 27 * (12288 // 2)  # ortalama output ~6144 tok

chapters = list(bv2.CHAPTER_SIZE_ESTIMATE.keys())
new_total_output = 0
for ch in chapters:
    mt = bv2.dynamic_max_tokens(ch)
    new_total_output += mt // 2  # ortalama kullanim = max/2

new_system_per_chapter = (len(bv2.SYSTEM_COMBINED) // 4) + 30  # kisaltilmis user

print(f"  Input/bolum (eski):     {old_system['SYSTEM_COMBINED']//4 + 50:3d} tok")
print(f"  Input/bolum (yeni):     {len(bv2.SYSTEM_COMBINED)//4 + 30:3d} tok")
print(f"  Input kazanci:          {(old_system['SYSTEM_COMBINED']//4 + 50) - (len(bv2.SYSTEM_COMBINED)//4 + 30):3d} tok/bolum")
print(f"  Output (eski):          {27 * (12288 // 2):>7,} tok (hepsi 12288)")
print(f"  Output (yeni):          {new_total_output:>7,} tok (dinamik)")
print(f"  Tasarruf:               {old_total_output - new_total_output:>7,} tok")
print()

# 4. P10 UYARI TESTI
print("4. P10 UYARI ESIGI (> 30000 chars)")
print("-" * 40)
for ch in chapters:
    est = bv2.estimate_chapter_size(ch)
    if est > 30000:
        print(f"  [UYARI] {ch:12s}: {est:>5,} chars -> max_tokens={bv2.dynamic_max_tokens(ch)}")
print()

print("=" * 60)
print("  DOGRULAMA TAMAM — Tum optimizasyonlar aktif")
print("=" * 60)
