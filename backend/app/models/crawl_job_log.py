from dataclasses import dataclass


@dataclass
class CrawlJobLog:
    job_type: str
    status: str
    started_at: str
    finished_at: str | None = None
    error_message: str | None = None
    payload: str | None = None

