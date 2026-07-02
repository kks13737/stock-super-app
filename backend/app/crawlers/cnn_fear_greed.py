from __future__ import annotations

import re
from datetime import datetime, timezone

import requests
from bs4 import BeautifulSoup


def parse_fear_greed(html: str) -> dict[str, str | int]:
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text(" ", strip=True)
    now = datetime.now(timezone.utc).isoformat()

    index_value = 0
    patterns = [
        r"Fear\s*&\s*Greed\s*Index[^0-9]{0,40}(\d{1,3})",
        r"(\d{1,3})\s*/\s*100",
        r'"score"\s*:\s*"?(\d{1,3})"?',
    ]
    for pattern in patterns:
        match = re.search(pattern, html, flags=re.IGNORECASE | re.DOTALL)
        if match:
            index_value = int(match.group(1))
            break

    state_label = "unknown"
    for label in ["Extreme Fear", "Fear", "Neutral", "Greed", "Extreme Greed"]:
        if label.lower() in text.lower():
            state_label = label
            break

    return {
        "source": "cnn",
        "index_value": index_value,
        "state_label": state_label,
        "fetched_at": now,
    }


def fetch_and_parse_fear_greed(source_url: str) -> dict[str, str | int]:
    response = requests.get(
        source_url,
        timeout=20,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        },
    )
    response.raise_for_status()
    return parse_fear_greed(response.text)
