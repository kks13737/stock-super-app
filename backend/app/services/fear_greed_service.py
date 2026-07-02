from __future__ import annotations

from app.repositories.fear_greed_repository import list_fear_greed_items, save_fear_greed_snapshot


def list_fear_greed_items_service(limit: int = 50) -> list[dict[str, object]]:
    return list_fear_greed_items(limit=limit)


def persist_fear_greed_snapshot(item: dict[str, object]) -> dict[str, object]:
    return save_fear_greed_snapshot(item)

