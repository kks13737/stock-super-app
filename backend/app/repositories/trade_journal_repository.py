from __future__ import annotations

from app.repositories._base import execute_update, execute_write, fetch_all, fetch_one


def list_trade_journals(trade_date: str | None = None) -> list[dict[str, object]]:
    if trade_date:
        return fetch_all(
            """
            SELECT * FROM trade_journal
            WHERE trade_date = ?
            ORDER BY trade_date DESC, id DESC
            """,
            (trade_date,),
        )
    return fetch_all(
        """
        SELECT * FROM trade_journal
        ORDER BY trade_date DESC, id DESC
        """
    )


def get_trade_journal(journal_id: int) -> dict[str, object] | None:
    return fetch_one("SELECT * FROM trade_journal WHERE id = ?", (journal_id,))


def create_trade_journal(payload: dict[str, object]) -> dict[str, object]:
    last_id = execute_write(
        """
        INSERT INTO trade_journal (trade_date, ticker, stock_name, side, quantity, price, memo)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            payload["trade_date"],
            payload["ticker"],
            payload["stock_name"],
            payload["side"],
            payload["quantity"],
            payload["price"],
            payload.get("memo"),
        ),
    )
    return get_trade_journal(last_id) or {}


def update_trade_journal(journal_id: int, payload: dict[str, object]) -> dict[str, object] | None:
    current = get_trade_journal(journal_id)
    if current is None:
        return None

    merged = {**current, **payload}
    execute_update(
        """
        UPDATE trade_journal
        SET trade_date = ?,
            ticker = ?,
            stock_name = ?,
            side = ?,
            quantity = ?,
            price = ?,
            memo = ?,
            updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
        """,
        (
            merged["trade_date"],
            merged["ticker"],
            merged["stock_name"],
            merged["side"],
            merged["quantity"],
            merged["price"],
            merged.get("memo"),
            journal_id,
        ),
    )
    return get_trade_journal(journal_id)


def delete_trade_journal(journal_id: int) -> bool:
    return execute_update("DELETE FROM trade_journal WHERE id = ?", (journal_id,)) > 0

