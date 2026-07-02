from app.db.connection import ping_database


def get_backend_health() -> dict[str, object]:
    return {"status": "ok", "service": "backend"}


def get_database_health() -> dict[str, object]:
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

