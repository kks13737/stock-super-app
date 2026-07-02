from fastapi import APIRouter

from app.services.crawl_service import run_news_sync
from app.services.news_service import list_news_articles_service

router = APIRouter(prefix="/news", tags=["news"])


@router.get("")
def list_news(limit: int = 50) -> dict[str, list[dict[str, object]]]:
    return {"items": list_news_articles_service(limit=limit)}


@router.post("/sync")
def sync_news() -> dict[str, object]:
    return run_news_sync()
