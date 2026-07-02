from __future__ import annotations

from datetime import datetime, timezone
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


def parse_naver_news(html: str, source_url: str) -> list[dict[str, str]]:
    soup = BeautifulSoup(html, "html.parser")
    items: list[dict[str, str]] = []
    seen_urls: set[str] = set()
    now = datetime.now(timezone.utc).isoformat()

    candidates = soup.select("a[href*='read.naver'], td.title a, a.news_tit")
    for anchor in candidates:
        title = anchor.get_text(" ", strip=True)
        href = anchor.get("href")
        if not title or not href:
            continue
        url = urljoin(source_url, href)
        if url in seen_urls:
            continue
        seen_urls.add(url)
        items.append(
            {
                "source": "naver",
                "title": title,
                "url": url,
                "publisher": None,
                "published_at": None,
                "summary": None,
                "fetched_at": now,
            }
        )

    return items[:50]


def fetch_and_parse_news(source_url: str) -> list[dict[str, str]]:
    response = requests.get(
        source_url,
        timeout=20,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        },
    )
    response.raise_for_status()
    return parse_naver_news(response.text, source_url)
