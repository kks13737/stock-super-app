from pydantic import BaseModel, Field


class TradeJournalCreate(BaseModel):
    trade_date: str = Field(..., examples=["2026-07-02"])
    ticker: str = Field(..., examples=["AAPL"])
    stock_name: str = Field(..., examples=["Apple"])
    side: str = Field(..., examples=["buy"])
    quantity: float = Field(..., ge=0)
    price: float = Field(..., ge=0)
    memo: str | None = None


class TradeJournalUpdate(BaseModel):
    trade_date: str | None = None
    ticker: str | None = None
    stock_name: str | None = None
    side: str | None = None
    quantity: float | None = Field(default=None, ge=0)
    price: float | None = Field(default=None, ge=0)
    memo: str | None = None


class TradeJournalItem(TradeJournalCreate):
    id: int
    created_at: str
    updated_at: str

