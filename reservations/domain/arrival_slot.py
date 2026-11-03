from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class ArrivalSlot:
    starts_at: datetime

    def __post_init__(self):
        if self.starts_at.microsecond != 0 or self.starts_at.second != 0:
            raise ValueError("Μη έγκυρη ώρα.")