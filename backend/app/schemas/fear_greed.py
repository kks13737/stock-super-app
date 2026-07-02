from pydantic import BaseModel


class FearGreedItem(BaseModel):
    id: int
    source: str
    index_value: int
    state_label: str
    fetched_at: str
    created_at: str


class FearGreedSyncResult(BaseModel):
    source: str
    index_value: int | None
    state_label: str
    status: str
    message: str

