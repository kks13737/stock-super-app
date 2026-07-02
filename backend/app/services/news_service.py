from __future__ import annotations

from app.repositories.news_repository import list_news_articles, save_news_articles


def list_news_articles_service(limit: int = 50) -> list[dict[str, object]]:
    return list_news_articles(limit=limit)


def persist_news_articles(items: list[dict[str, object]]) -> int:
    if not items:
        return 0
    return save_news_articles(items)

