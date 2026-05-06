import re
import uuid


def slugify(text: str) -> str:
    """Metni URL/dosya uyumlu slug'a çevirir."""
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_-]+", "_", text)
    return text


def new_event_id() -> str:
    return f"evt_{uuid.uuid4().hex[:12]}"


def new_issue_id() -> str:
    return f"iss_{uuid.uuid4().hex[:8]}"
