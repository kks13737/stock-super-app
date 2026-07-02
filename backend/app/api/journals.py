from fastapi import APIRouter, HTTPException

from app.schemas.trade_journal import TradeJournalCreate, TradeJournalUpdate
from app.services.trade_journal_service import (
    create_trade_journal,
    delete_trade_journal,
    get_trade_journal,
    list_trade_journals,
    update_trade_journal,
)

router = APIRouter(prefix="/trade-journals", tags=["trade-journals"])


@router.get("")
def list_trade_journals_api(trade_date: str | None = None) -> dict[str, list[dict[str, object]]]:
    return {"items": list_trade_journals(trade_date=trade_date)}


@router.post("")
def create_trade_journal_api(payload: TradeJournalCreate) -> dict[str, object]:
    item = create_trade_journal(payload.model_dump())
    return {"item": item, "message": "trade journal saved"}


@router.get("/{journal_id}")
def get_trade_journal_api(journal_id: int) -> dict[str, object]:
    item = get_trade_journal(journal_id)
    if item is None:
        raise HTTPException(status_code=404, detail="trade journal not found")
    return {"item": item}


@router.put("/{journal_id}")
def update_trade_journal_api(journal_id: int, payload: TradeJournalUpdate) -> dict[str, object]:
    item = update_trade_journal(journal_id, payload.model_dump(exclude_none=True))
    if item is None:
        raise HTTPException(status_code=404, detail="trade journal not found")
    return {"item": item, "message": "trade journal updated"}


@router.delete("/{journal_id}")
def delete_trade_journal_api(journal_id: int) -> dict[str, object]:
    deleted = delete_trade_journal(journal_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="trade journal not found")
    return {"message": "trade journal deleted"}
