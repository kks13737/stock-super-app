from __future__ import annotations

from app.repositories._base import execute_update, execute_write


def create_crawl_job_log(job_type: str, status: str, started_at: str, payload: str | None = None) -> int:
    return execute_write(
        """
        INSERT INTO crawl_job_log (job_type, status, started_at, payload)
        VALUES (?, ?, ?, ?)
        """,
        (job_type, status, started_at, payload),
    )


def finish_crawl_job_log(job_id: int, status: str, finished_at: str, error_message: str | None = None) -> int:
    return execute_update(
        """
        UPDATE crawl_job_log
        SET status = ?,
            finished_at = ?,
            error_message = ?
        WHERE id = ?
        """,
        (status, finished_at, error_message, job_id),
    )

