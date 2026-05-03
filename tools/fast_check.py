"""build.py sadeleştirme — tek satırda test + lint."""

import subprocess
import sys
import time
from pathlib import Path


def run(cmd: str, cwd: Path | None = None) -> subprocess.CompletedProcess:
    """Komut çalıştır ve sonucu döndür."""
    return subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=cwd or Path.cwd())


def fast_check(project_root: Path = Path(".")) -> int:
    """Hızlı kalite kontrol: lint + fast test. Exit code döndürür."""
    t0 = time.time()

    # Lint
    lint = run("ruff check src/ tests/", project_root)
    if lint.returncode != 0:
        print(f"[FAIL] lint: {len(lint.stdout.splitlines())} hata")
        print(lint.stdout)
        return 1
    print(f"[OK] lint ({time.time()-t0:.1f}s)")

    # Fast test
    test = run("pytest tests/ -q --tb=short -m 'not slow'", project_root)
    print(test.stdout)
    if test.returncode != 0:
        print(f"[FAIL] test")
        return 1

    # Özet
    last_line = test.stdout.strip().splitlines()[-1] if test.stdout.strip() else "?"
    print(f"[OK] {last_line} ({time.time()-t0:.1f}s)")
    return 0


if __name__ == "__main__":
    sys.exit(fast_check())
