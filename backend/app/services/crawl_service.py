from __future__ import annotations

from datetime import datetime, timezone

from app.core.config import settings
from app.crawlers.cnn_fear_greed import fetch_and_parse_fear_greed
from app.crawlers.naver_news import fetch_and_parse_news
from app.repositories.crawl_job_log_repository import create_crawl_job_log, finish_crawl_job_log
from app.services.fear_greed_service import persist_fear_greed_snapshot
from app.services.news_service import persist_news_articles


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def run_news_sync() -> dict[str, object]:
    started_at = _now_iso()
    job_id = create_crawl_job_log("news", "running", started_at, settings.naver_news_url)
    try:
        items = fetch_and_parse_news(settings.naver_news_url)
        saved_count = persist_news_articles(items)
        finish_crawl_job_log(job_id, "success", _now_iso())
        return {
            "source": "naver",
            "fetched_count": len(items),
            "saved_count": saved_count,
            "status": "success",
            "message": "news sync completed",
        }
    except Exception as exc:
        finish_crawl_job_log(job_id, "failed", _now_iso(), str(exc))
        return {
            "source": "naver",
            "fetched_count": 0,
            "saved_count": 0,
            "status": "failed",
            "message": f"news sync failed: {exc}",
        }


def run_fear_greed_sync() -> dict[str, object]:
    started_at = _now_iso()
    job_id = create_crawl_job_log("fear_greed", "running", started_at, settings.cnn_fear_greed_url)
    try:
        snapshot = fetch_and_parse_fear_greed(settings.cnn_fear_greed_url)
        saved = persist_fear_greed_snapshot(snapshot)
        finish_crawl_job_log(job_id, "success", _now_iso())
        return {
            "source": "cnn",
            "index_value": saved.get("index_value"),
            "state_label": saved.get("state_label", "unknown"),
            "status": "success",
            "message": "fear-greed sync completed",
        }
    except Exception as exc:
        finish_crawl_job_log(job_id, "failed", _now_iso(), str(exc))
        return {
            "source": "cnn",
            "index_value": None,
            "state_label": "unknown",
            "status": "failed",
            "message": f"fear-greed sync failed: {exc}",
        }
