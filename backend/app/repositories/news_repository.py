from __future__ import annotations

from datetime import datetime, timezone

from app.repositories._base import execute_write, fetch_all


def list_news_articles(limit: int = 50) -> list[dict[str, object]]:
    return fetch_all(
        """
        SELECT * FROM news_article
        ORDER BY datetime(COALESCE(published_at, fetched_at)) DESC, id DESC
        LIMIT ?
        """,
        (limit,),
    )


def save_news_articles(items: list[dict[str, object]]) -> int:
    saved_count = 0
    now = datetime.now(timezone.utc).isoformat()
    for item in items:
        execute_write(
            """
            INSERT INTO news_article (
                source, title, url, publisher, published_at, summary, fetched_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(url) DO UPDATE SET
                source = excluded.source,
                title = excluded.title,
                publisher = excluded.publisher,
                published_at = excluded.published_at,
                summary = excluded.summary,
                fetched_at = excluded.fetched_at
            """,
            (
                item["source"],
                item["title"],
                item["url"],
                item.get("publisher"),
                item.get("published_at"),
                item.get("summary"),
                item.get("fetched_at", now),
            ),
        )
        saved_count += 1
    return saved_count

