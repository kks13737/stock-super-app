from dataclasses import dataclass, field
from pathlib import Path
import os


def _split_csv(value: str) -> list[str]:
    return [item.strip() for item in value.split(",") if item.strip()]


@dataclass(frozen=True)
class Settings:
    project_root: Path = field(init=False)
    backend_root: Path = field(init=False)
    frontend_dir: Path = field(init=False)
    data_dir: Path = field(init=False)
    app_name: str = os.getenv("APP_NAME", "stock-super-app")
    app_env: str = os.getenv("APP_ENV", "development")
    api_host: str = os.getenv("API_HOST", "0.0.0.0")
    api_port: int = int(os.getenv("API_PORT", "8000"))
    database_path: Path = field(init=False)
    cors_origins: list[str] = field(init=False)
    cors_origin_regex: str = os.getenv("CORS_ORIGIN_REGEX", r"https://.*\.github\.io")
    naver_news_url: str = os.getenv(
        "NAVER_NEWS_URL",
        "https://finance.naver.com/news/news_list.naver?mode=LSS2D&section_id=101&section_id2=258",
    )
    cnn_fear_greed_url: str = os.getenv(
        "CNN_FEAR_GREED_URL",
        "https://edition.cnn.com/markets/fear-and-greed",
    )

    def __post_init__(self) -> None:
        project_root = Path(__file__).resolve().parents[3]
        backend_root = project_root / "backend"
        frontend_dir = project_root / "frontend"
        data_dir = backend_root / "data"
        default_db_path = data_dir / "stock_app.db"
        object.__setattr__(self, "project_root", project_root)
        object.__setattr__(self, "backend_root", backend_root)
        object.__setattr__(self, "frontend_dir", frontend_dir)
        object.__setattr__(self, "data_dir", data_dir)
        object.__setattr__(
            self,
            "database_path",
            Path(os.getenv("DATABASE_PATH", str(default_db_path))),
        )
        object.__setattr__(
            self,
            "cors_origins",
            _split_csv(os.getenv("CORS_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173")),
        )


settings = Settings()
