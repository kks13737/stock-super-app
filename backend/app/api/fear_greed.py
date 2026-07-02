from fastapi import APIRouter

from app.services.crawl_service import run_fear_greed_sync
from app.services.fear_greed_service import list_fear_greed_items_service

router = APIRouter(prefix="/fear-greed", tags=["fear-greed"])


@router.get("")
def list_fear_greed(limit: int = 50) -> dict[str, list[dict[str, object]]]:
    return {"items": list_fear_greed_items_service(limit=limit)}


@router.post("/sync")
def sync_fear_greed() -> dict[str, object]:
    return run_fear_greed_sync()
