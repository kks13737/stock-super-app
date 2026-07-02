from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str
    service: str
    connected: bool | None = None
    error: str | None = None

