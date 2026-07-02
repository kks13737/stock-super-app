from datetime import datetime, timezone

from fastapi import APIRouter

from app.db.connection import ping_database

router = APIRouter(tags=["health"])


@router.get("/health")
def health_check() -> dict[str, object]:
    return {
        "status": "ok",
        "service": "backend",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@router.get("/health/db")
def database_health_check() -> dict[str, object]:
    try:
        ping_database()
        return {"status": "ok", "service": "database", "connected": True}
    except Exception as exc:
        return {
            "status": "error",
            "service": "database",
            "connected": False,
            "error": str(exc),
        }


@router.get("/health/full")
def full_health_check() -> dict[str, object]:
    api_health = health_check()
    db_health = database_health_check()
    return {
        "api": api_health,
        "database": db_health,
        "overall": "ok" if db_health["connected"] else "degraded",
    }

