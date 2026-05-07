# Changelog

## Unreleased

### Added
- Export readiness checks and production export reports.
- Profile-aware code adapter pipeline (Java, Python, Flutter, React).
- Studio-friendly code validation summary payloads.
- Studio-friendly export report and output URLs.
- End-to-end smoke test coverage.
- GitHub Actions CI workflow with Python 3.12/3.13 matrix.
- Release checklist.

### Changed
- Export and assembly now use project-based `exports/` paths.
- Unknown code profiles now fall back to `ReviewOnlyAdapter`.
- React adapter safely skips TS/JSX/TSX blocks while checking plain JS.
- CI ruff check expanded to full `src/ tests/`.

### Fixed
- Code adapter timeout handling (Java, Python, Flutter).
- Export report generation for success and failure cases.

---

## [0.2.0] — 2026-05-07 (main branch)

### Added
- Inline editable chapter titles (double-click to edit, Enter/blur save, Escape cancel)
- Pipeline job detail panel (expandable per-step prompt→output mapping, timing, progress)
- Export UI controls: reference DOCX, lua filter, TOC depth in Build/Export tab
- Export sub-tab in Yapilandirma with full pandoc/output settings
- `PandocConfig`, `MermaidConfig`, `OutputsConfig` models in BookManifest
- Per-step tracking in pipeline jobs (prompt_file, output_file, elapsed_s)
- Split-panel markdown editor in chapter view (left: textarea, right: live preview)
- Chapter creation wizard (+ Bolum Ekle button, bulk delete)
- CHAPTER_PRODUCTION.md documenting the 6-stage pipeline

### Changed
- **book_profile.yaml eliminated** — BookConfig reads from book_manifest.yaml
- Single global llm_config.json (per-book LLM config removed from GUI)
- BookManifest extended with pandoc/mermaid/outputs optional sections
- Wizard creates book_manifest.yaml with full pandoc/defaults (no book_profile.yaml)
- ManifestManager simplified (profile_path, architecture_path, load_or_generate cleaned)
- All prompt builders parameterized with dynamic code_language (no hardcoded Java)
- Chapter view replaced with split-panel editor (save via POST /api/view/{id}/save)
- All book_manifest.yaml fields editable via Yapilandirma tab in GUI

### Removed
- Per-book LLM configuration tab and endpoints
- book_profile.yaml dependency (all config in book_manifest.yaml)
- _create_book_profile() and _create_llm_config() from wizard
- ManifestManager.profile_path() and architecture_path()

### Fixed
- Hardcoded Java references in all prompt builders (spec, seed, validation)
- Worker thread root-fixation bug (captured root at server startup)
- Markdown table rendering in preview panel (line-by-line state machine)
- Template ID conflicts in modal (document.importNode with <template> tags)

---

## [0.1.0] — 2026-05-04 (deepseek branch)

### Added
- 4-stage chapter generation pipeline: Spec → Seed → Normalize → Enrich → Assemble
- 6-step pedagogical depth chain: TANIM → NEDEN → NASIL → NE ZAMAN → ALTERNATİF → HATA
- DeepSeek Chat integration with auto-resume for truncated responses
- 6 parallel enrichment types: özet, sözlük, soru, alıştırma, hata, köprü
- Teorik derinleştirme (deepen theory): H2-based section expansion
- 5 generation strategies: basic, spec-guided, spec+deepen, sectioned, two-pass
- Studio GUI: FastAPI + vanilla JS, 5 tabs, wizard, SSE live build stream
- Chapter validator: parser, semantic checks, scoring, JSON/Markdown reports
- Production pipeline: Mermaid→PNG, Pandoc DOCX/PDF/EPUB/HTML export
- QR code generation with dual/source/page/none policies
- Book profile system (book_profile.yaml, book_architecture.yaml)
- CLI commands: check, build, production, generate, init, manifest, llm, github, studio
- 24 unit/integration/CLI tests
- CI workflow: ruff lint + pytest + prompt validation
- CLAUDE.md agent instructions for multi-session development

### Changed
- Migrated from dual-model (Pro+Flash) to single DeepSeek Chat model
- Tools cleaned: 94→30 scripts, archived fix/check/verify/migration scripts
- Enrichment prompts: context expanded from 500→2000 chars + concepts list
- Spec prompt: plan-only format (no code blocks in spec)
- Mermaid diagrams: optional (was mandatory)
- Question format: 5-10 D/Y + 5-10 Boşluk Doldurma, no multiple choice

### Fixed
- Enrichment key mismatch: Turkish→ASCII key mapping (özet→ozet)
- LLM meta-commentary cleanup in normalize_headings
- Front matter `---` handling in whitespace cleaner
- Code block indentation normalization (`_normalize_code_blocks`)
- Duplicate section insertion prevention (`turkish_terms` dedup)
- Multi-machine sync: machine-specific files removed from git tracking
- Broken venv: recreated with Python 3.14.4, missing `requests` added
