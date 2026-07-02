from dataclasses import dataclass


@dataclass
class NewsArticle:
    source: str
    title: str
    url: str
    publisher: str | None
    published_at: str | None
    summary: str | None
    fetched_at: str

