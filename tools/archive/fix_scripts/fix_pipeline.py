"""Pipeline.py bozuk metodu düzelt."""
p = "src/bookmaker/generation/pipeline.py"
c = open(p, "r", encoding="utf-8", errors="replace").read()

# Bozuk bolumu bul ve sil
broken = "generate_chapter_with_spec"
bad_start = c.find(broken)
if bad_start > 0:
    # Metoddan onceki kismi bul
    before_method = c.rfind("    def ", 0, bad_start)
    if before_method > 0:
        before_line = c.rfind("\n", 0, before_method)
        clean = c[:before_line].rstrip()
        # _fallback_content'i ekle
        fb_start = c.find("def _fallback_content")
        if fb_start > 0:
            clean += "\n\n\n" + c[fb_start:]
        open(p, "w", encoding="utf-8").write(clean)
        print("Pipeline duzeltildi, uzunluk:", len(clean))
    else:
        print("Metod baslangici bulunamadi")
else:
    print("generate_chapter_with_spec bulunamadi")
