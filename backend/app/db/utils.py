from __future__ import annotations


def row_to_dict(row) -> dict[str, object] | None:
    if row is None:
        return None
    return dict(row)


def rows_to_dicts(rows) -> list[dict[str, object]]:
    return [dict(row) for row in rows]

