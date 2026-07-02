from __future__ import annotations

from collections.abc import Sequence

from app.db.connection import get_connection
from app.db.utils import row_to_dict, rows_to_dicts


def fetch_one(query: str, params: Sequence[object] = ()) -> dict[str, object] | None:
    with get_connection() as connection:
        row = connection.execute(query, params).fetchone()
        return row_to_dict(row)


def fetch_all(query: str, params: Sequence[object] = ()) -> list[dict[str, object]]:
    with get_connection() as connection:
        rows = connection.execute(query, params).fetchall()
        return rows_to_dicts(rows)


def execute_write(query: str, params: Sequence[object] = ()) -> int:
    with get_connection() as connection:
        cursor = connection.execute(query, params)
        connection.commit()
        return cursor.lastrowid


def execute_update(query: str, params: Sequence[object] = ()) -> int:
    with get_connection() as connection:
        cursor = connection.execute(query, params)
        connection.commit()
        return cursor.rowcount

