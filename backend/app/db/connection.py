from contextlib import contextmanager
import sqlite3

from app.core.config import settings


def _ensure_database_dir() -> None:
    settings.database_path.parent.mkdir(parents=True, exist_ok=True)


@contextmanager
def get_connection():
    _ensure_database_dir()
    connection = sqlite3.connect(str(settings.database_path))
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON;")
    try:
        yield connection
    finally:
        connection.close()


def ping_database() -> bool:
    with get_connection() as connection:
        connection.execute("SELECT 1")
    return True
