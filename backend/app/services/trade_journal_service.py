from __future__ import annotations

from app.repositories.trade_journal_repository import (
    create_trade_journal as repo_create_trade_journal,
    delete_trade_journal as repo_delete_trade_journal,
    get_trade_journal as repo_get_trade_journal,
    list_trade_journals as repo_list_trade_journals,
    update_trade_journal as repo_update_trade_journal,
)


def list_trade_journals(trade_date: str | None = None) -> list[dict[str, object]]:
    return repo_list_trade_journals(trade_date=trade_date)


def get_trade_journal(journal_id: int) -> dict[str, object] | None:
    return repo_get_trade_journal(journal_id)


def create_trade_journal(payload: dict[str, object]) -> dict[str, object]:
    return repo_create_trade_journal(payload)


def update_trade_journal(journal_id: int, payload: dict[str, object]) -> dict[str, object] | None:
    return repo_update_trade_journal(journal_id, payload)


def delete_trade_journal(journal_id: int) -> bool:
    return repo_delete_trade_journal(journal_id)
