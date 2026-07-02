from pydantic import BaseModel


class NewsArticleItem(BaseModel):
    id: int
    source: str
    title: str
    url: str
    publisher: str | None = None
    published_at: str | None = None
    summary: str | None = None
    fetched_at: str
    created_at: str


class NewsSyncResult(BaseModel):
    source: str
    fetched_count: int
    saved_count: int
    status: str
    message: str

