def schedule_news_job() -> None:
    from app.services.crawl_service import run_news_sync

    run_news_sync()


def schedule_fear_greed_job() -> None:
    from app.services.crawl_service import run_fear_greed_sync

    run_fear_greed_sync()
