from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.api.health import router as health_router
from app.api.fear_greed import router as fear_greed_router
from app.api.journals import router as journals_router
from app.api.news import router as news_router
from app.core.config import settings
from app.db.init_db import init_db


def create_app() -> FastAPI:
    app = FastAPI(title=settings.app_name, version="0.1.0")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(health_router, prefix="/api")
    app.include_router(journals_router, prefix="/api")
    app.include_router(news_router, prefix="/api")
    app.include_router(fear_greed_router, prefix="/api")

    @app.on_event("startup")
    def on_startup() -> None:
        init_db()

    if settings.frontend_dir.exists():
        app.mount("/assets", StaticFiles(directory=settings.frontend_dir), name="assets")

        @app.get("/", include_in_schema=False)
        def index() -> FileResponse:
            return FileResponse(settings.frontend_dir / "index.html")

    return app


app = create_app()
