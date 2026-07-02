from dataclasses import dataclass


@dataclass
class HealthStatus:
    status: str
    service: str
    connected: bool | None = None
    error: str | None = None

