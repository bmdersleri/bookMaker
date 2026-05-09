from datetime import datetime, timedelta, timezone

ISTANBUL = timezone(timedelta(hours=3))


def now_iso() -> str:
    """Europe/Istanbul zaman damgası, ISO 8601."""
    return datetime.now(tz=ISTANBUL).isoformat(timespec="seconds")


def now_date() -> str:
    return datetime.now(tz=ISTANBUL).strftime("%Y-%m-%d")
