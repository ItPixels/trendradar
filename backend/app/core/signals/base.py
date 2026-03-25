from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class RawSignal:
    source: str
    source_id: str
    title: str
    url: Optional[str] = None
    content: Optional[str] = None
    metrics: dict = field(default_factory=dict)
    detected_at: datetime = field(default_factory=datetime.utcnow)
    signal_strength: float = 0.0


class BaseSignalAdapter(ABC):
    source_name: str
    weight: float
    tier: int  # 1, 2, or 3

    @abstractmethod
    async def fetch_signals(self) -> list[RawSignal]:
        """Fetch raw signals from the source."""
        pass

    @abstractmethod
    async def health_check(self) -> bool:
        """Check if the source is available."""
        pass

    def get_source_info(self) -> dict:
        return {
            "name": self.source_name,
            "weight": self.weight,
            "tier": self.tier,
        }
