"""Export report writer."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any


def write_export_report(project_root: str | Path, payload: dict[str, Any]) -> str:
    """Persist export report under logs/production/export_<timestamp>.json."""
    root = Path(project_root).resolve()
    out_dir = root / "logs" / "production"
    out_dir.mkdir(parents=True, exist_ok=True)

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    out_path = out_dir / f"export_{stamp}.json"
    data = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        **payload,
    }
    out_path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return str(out_path.relative_to(root))

