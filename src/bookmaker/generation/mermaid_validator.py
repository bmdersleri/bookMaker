"""MermaidValidator — Mermaid diyagram kodlarini validate eder ve auto-fix uygular.
Saf Python regex (0 token) + mmdc compile (~5s timeout) + fallback.

Kullanim:
    validator = MermaidValidator(config)
    result = validator.validate("graph TD; A-->B")
    # -> MermaidResult(valid=True, ...)

    results = validator.validate_from_file(markdown_path, output_dir)
    # -> [MermaidResult, ...]
"""

from __future__ import annotations

import re
import subprocess
import tempfile
from dataclasses import dataclass, field
from pathlib import Path

from bookmaker.core.config import BookConfig

# ============================================================
# VERI YAPILARI
# ============================================================

@dataclass
class MermaidIssue:
    """Mermaid kodunda tespit edilen bir sorun."""
    type: str
    line: int
    message: str


@dataclass
class MermaidResult:
    """Bir mermaid diyagrami icin validate sonucu."""
    valid: bool = False
    code: str = ""
    fixed: bool = False
    issues: list[MermaidIssue] = field(default_factory=list)
    status: str = "unknown"
    path: str | None = None
    error: str = ""


# ============================================================
# VALIDATOR SINIFI
# ============================================================

class MermaidValidator:
    """4 asamali Mermaid validator: syntax -> auto-fix -> compile -> fallback."""

    # Auto-fix regex'leri
    AUTO_FIXES = [
        (r'([A-Za-z]\w*)\(([^)"\n]+)\)', r'\1("\2")'),
        (r'([A-Za-z]\w*)\[([^"\]]+)\]', r'\1["\2"]'),
        (r'([A-Za-z]\w*)\{([^"}]+)\}', r'\1{"\2"}'),
        (r'(\w+)\s*->(\s*\w)', r'\1 --> \2'),
    ]

    def __init__(self, config: BookConfig | None = None) -> None:
        self.config = config
        self.mmdc_cmd = config.mermaid_mmdc_cmd if config else [
            "C:\\Program Files\\PowerShell\\7\\pwsh.exe",
            "-NoProfile", "-Command", "mmdc",
        ]
        self.timeout = (config.mermaid_timeout if config else 10) or 10
        self.bg = (config.mermaid_background if config else "white") or "white"

    # ----------------------------------------------------------
    # ASAMA 1: SYNTAX CHECK
    # ----------------------------------------------------------

    def syntax_check(self, code: str) -> list[MermaidIssue]:
        """Regex ile syntax kontrolu. <1ms, 0 token."""
        issues = []
        lines = code.splitlines()

        for i, line in enumerate(lines):
            s = line.strip()
            if not s or s.startswith("%"):
                continue
            if s.startswith("graph") or s.startswith("flowchart"):
                continue

            # Parantez dengesi
            for oc, cc, name in [("[", "]", "kose"), ("(", ")", "normal"),
                                  ("{", "}", "suslu")]:
                o = s.count(oc)
                c = s.count(cc)
                if o != c:
                    issues.append(MermaidIssue(
                        "unbalanced", i,
                        f"{name} parantez: {o}/{c}",
                    ))

            # Tirnak dengesi
            if s.count('"') % 2 != 0:
                issues.append(MermaidIssue("quote", i, "Kapanmamis tirnak"))

        return issues

    # ----------------------------------------------------------
    # ASAMA 2: AUTO-FIX
    # ----------------------------------------------------------

    def auto_fix(self, code: str) -> tuple[str, list[MermaidIssue]]:
        """Yaygin hatalari otomatik duzeltir. <1ms, 0 token."""
        fixes = []
        for pattern, repl in self.AUTO_FIXES:
            new = re.sub(pattern, repl, code)
            if new != code:
                fixes.append(MermaidIssue("auto_fix", 0,
                               f"Uygulandi: {pattern[:30]}"))
                code = new
        return code, fixes

    # ----------------------------------------------------------
    # ASAMA 3: COMPILE (mmdc)
    # ----------------------------------------------------------

    def compile(self, code: str,
                output_path: Path | None = None) -> MermaidResult:
        """mmdc ile PNG'ye derlemeyi dener. ~5s timeout."""
        if output_path is None:
            with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
                output_path = Path(f.name)

        output_path.parent.mkdir(parents=True, exist_ok=True)
        mmd = output_path.with_suffix(".mmd")
        mmd.write_text(code, encoding="utf-8")

        cmd = self.mmdc_cmd + [
            "-i", str(mmd), "-o", str(output_path),
            "-f", "-b", self.bg,
        ]
        try:
            p = subprocess.run(cmd, capture_output=True, text=True,
                               timeout=self.timeout)
            ok = p.returncode == 0 and output_path.exists()
            r = MermaidResult(valid=ok, code=code,
                              status="passed" if ok else "failed",
                              path=str(output_path) if ok else None,
                              error=p.stderr if not ok else "")
            if not ok and p.stderr:
                for e in p.stderr.splitlines():
                    r.issues.append(MermaidIssue("compile", 0, e[:200]))
            return r
        except subprocess.TimeoutExpired:
            return MermaidResult(valid=False, code=code,
                                 status="timeout",
                                 error=f"mmdc timeout ({self.timeout}s)")
        except Exception as e:
            return MermaidResult(valid=False, code=code,
                                 status="error", error=str(e))
        finally:
            if mmd.exists():
                mmd.unlink()

    # ----------------------------------------------------------
    # ASAMA 4: FALLBACK
    # ----------------------------------------------------------

    def fallback(self, code: str) -> str:
        """Mermaid kodunu en basit haline indirger."""
        nodes, edges = [], []
        for line in code.splitlines():
            s = line.strip()
            if not s or s.startswith("%"):
                continue
            # Node'lari bul
            for pat in [r'(\w+)\[([^\]]+)\]', r'(\w+)\(([^)]+)\)']:
                for m in re.finditer(pat, s):
                    nodes.append((m.group(1), m.group(2)))
            # Oklari bul
            for m in re.finditer(r"(\w+)\s*(-->|==>|-\.->)\s*(\w+)", s):
                edges.append(m.groups())

        if not nodes:
            return "graph TD\n    A[\"Diyagram yuklenemedi\"]"

        result = ["graph TD"]
        for nid, label in nodes:
            result.append(f'    {nid}["{label}"]')
        for src, dst, arrow in edges:
            result.append(f"    {src} {arrow} {dst}")
        if not edges and len(nodes) > 1:
            for i in range(len(nodes) - 1):
                result.append(f"    {nodes[i][0]} --> {nodes[i+1][0]}")

        return "\n".join(result)

    # ----------------------------------------------------------
    # TUM VALIDATE AKISI
    # ----------------------------------------------------------

    def validate(self, code: str,
                 output_path: Path | None = None) -> MermaidResult:
        """Syntax -> auto-fix -> compile -> fallback."""
        issues = self.syntax_check(code)

        if not issues and output_path:
            r = self.compile(code, output_path)
            if r.status == "passed":
                return r

        fixed, fix_issues = self.auto_fix(code)
        all_issues = issues + fix_issues

        if output_path and fixed != code:
            r = self.compile(fixed, output_path)
            r.issues = all_issues + r.issues
            r.fixed = True
            if r.status == "passed":
                r.code = fixed
                return r

        fb = self.fallback(fixed if fixed != code else code)
        if output_path:
            r = self.compile(fb, output_path)
            r.issues = all_issues + [MermaidIssue("fallback", 0,
                "Orijinal kod basarisiz, fallback kullanildi")]
            r.code = fb
            r.fixed = (fb != code)
            if r.status != "passed":
                r.status = "fallback"
            return r

        return MermaidResult(valid=False, code=fb,
                             fixed=(fb != code),
                             issues=all_issues, status="fallback")

    # ----------------------------------------------------------
    # DOSYA UZERINDE CALISMA
    # ----------------------------------------------------------

    def validate_from_file(self, markdown_path: Path,
                           output_dir: Path) -> list[MermaidResult]:
        """Markdown dosyasindaki tum Mermaid bloklarini validate + render eder."""
        text = markdown_path.read_text(encoding="utf-8")
        output_dir.mkdir(parents=True, exist_ok=True)

        results = []
        for i, match in enumerate(
            re.finditer(r"```mermaid\s*\n(.*?)```", text, re.DOTALL)
        ):
            code = match.group(1).strip()
            png = output_dir / f"diagram_{i+1:03d}.png"
            r = self.validate(code, png)
            r.code = code
            results.append(r)

        return results
