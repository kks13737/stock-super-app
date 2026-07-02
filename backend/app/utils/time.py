from datetime import datetime, timezone, timedelta


KST = timezone(timedelta(hours=9))


def now_kst() -> datetime:
    return datetime.now(KST)


def now_utc_iso() -> str:
    return datetime.now(timezone.utc).isoformat()
