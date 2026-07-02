from __future__ import annotations

from app.repositories._base import execute_write, fetch_all


def list_fear_greed_items(limit: int = 50) -> list[dict[str, object]]:
    return fetch_all(
        """
        SELECT * FROM fear_greed_index
        ORDER BY datetime(fetched_at) DESC, id DESC
        LIMIT ?
        """,
        (limit,),
    )


def save_fear_greed_snapshot(item: dict[str, object]) -> dict[str, object]:
    last_id = execute_write(
        """
        INSERT INTO fear_greed_index (source, index_value, state_label, fetched_at)
        VALUES (?, ?, ?, ?)
        """,
        (
            item["source"],
            item["index_value"],
            item["state_label"],
            item["fetched_at"],
        ),
    )
    rows = fetch_all("SELECT * FROM fear_greed_index WHERE id = ?", (last_id,))
    return rows[0] if rows else {}

