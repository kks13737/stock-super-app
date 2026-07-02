from dataclasses import dataclass


@dataclass
class TradeJournal:
    trade_date: str
    ticker: str
    stock_name: str
    side: str
    quantity: float
    price: float
    memo: str | None = None

