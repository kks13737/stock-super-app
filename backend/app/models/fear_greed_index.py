from dataclasses import dataclass


@dataclass
class FearGreedIndex:
    source: str
    index_value: int
    state_label: str
    fetched_at: str

