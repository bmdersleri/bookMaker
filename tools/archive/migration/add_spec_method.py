"""Pipeline.py'ye generate_chapter_with_spec metodunu ekle."""
method = '''
    # ----------------------------------------------------------
    # GENERATE WITH SPEC (kapsamli, ara dosya kayitli)
    # ----------------------------------------------------------

    def generate_chapter_with_spec(
        self, chapter_id: str, title: str, concepts: list[str],
        chapter_no=None, enrich_types=None, next_chapter=None, save=True,
    ):
        """Spec -> Validate -> Seed -> Normalize -> Enrich -> Assemble.
        Her asamanin ciktisi build/generation/ altina kaydedilir."""
        gen_dir = self.root / "build" / "generation"
        gen_dir.mkdir(parents=True, exist_ok=True)
        t0 = time.time()
        result = {"chapter_id": chapter_id, "title": title, "steps": {}}

        # --- STEP 0: SPEC ---
        print(f"\\n--- ADIM 0: SPEC ---")
        spec = generate_spec(self.seed_client, title, concepts,
                             f"Hedef: {self.config.audience}", chapter_no)
        self._save_gen(gen_dir / "step0_spec.md", spec)
        self._save_gen(gen_dir / "prompt0_spec.txt",
            build_spec_prompt(title, concepts,
                f"Hedef: {self.config.audience}", chapter_no))
        result["spec"] = spec

        # --- STEP 0.5: VALIDATE ---
        print(f"\\n--- ADIM 0.5: DOGRULAMA ---")
        validation = validate_spec(self.enrich_client, spec, title)
        self._save_gen(gen_dir / "step0_validation.md", validation["notes"])
        self._save_gen(gen_dir / "prompt0_validation.txt",
            build_spec_validation_prompt(spec, title))
        result["validation"] = validation

        # --- STEP 1: SEED ---
        print(f"\\n--- ADIM 1: SEED ---")
        seed_prompt = build_seed_from_spec_prompt(spec, title)
        self._save_gen(gen_dir / "prompt1_seed.txt", seed_prompt)
        seed_start = time.time()
        raw = self.seed_client.generate_text(SYSTEM_AUTHOR, seed_prompt)
        result["seed_time"] = round(time.time() - seed_start, 1)
        self._save_gen(gen_dir / "step1_seed.md", raw)
        print(f"  [SEED] {len(raw.split())} kelime, {result['seed_time']}s")

        # --- STEP 2: NORMALIZE ---
        norm = self.normalize_chapter(raw, chapter_id, title)
        self._save_gen(gen_dir / "step2_normalized.md", norm)

        # --- STEP 3: ENRICH ---
        missing = self.detect_missing(norm)
        enriched = self.enrich(norm, title, enrich_types, next_chapter) if missing else {}
        for k, v in enriched.items():
            self._save_gen(gen_dir / f"prompt3_enrich_{k}.txt",
                f"Enrichment: {k}, Chapter: {title}")
        result["enriched"] = enriched
        result["missing"] = [m for m in missing if not m["existing"]]

        # --- STEP 4: ASSEMBLE + FINAL NORMALIZE ---
        final = self.assemble(norm, enriched, chapter_id, title)
        final = self.normalize_chapter(final, chapter_id, title)
        self._save_gen(gen_dir / "step4_final.md", final)

        if save:
            path = self._save_chapter(chapter_id, final)
            result["path"] = str(path)

        wc = len(final.split())
        tt = round(time.time() - t0, 1)
        print(f"\\n  DONE {chapter_id}: {wc} kelime, {tt}s")
        print(f"  Dosyalar: {gen_dir}")
        return result

    def _save_gen(self, path, content):
        """Icerigi generation dizinine kaydet."""
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(str(content), encoding="utf-8")
        except Exception:
            pass

'''

p = "src/bookmaker/generation/pipeline.py"
c = open(p, "r", encoding="utf-8").read()

# _fallback_content fonksiyonundan ONCE ekle
fb_pos = c.find("def _fallback_content")
if fb_pos > 0:
    new = c[:fb_pos] + method + "\n\n" + c[fb_pos:]
    open(p, "w", encoding="utf-8").write(new)
    print(f"Metot eklendi, yeni uzunluk: {len(new)}")
else:
    print("_fallback_content bulunamadi")
