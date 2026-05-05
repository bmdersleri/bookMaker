# Changelog

## [0.1.0] — Unreleased (deepseek branch)

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
