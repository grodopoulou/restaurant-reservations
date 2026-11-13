from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class ArrivalSlot:
    """
    A class to represent the date and the time of the reservation.
    """
    starts_at: datetime

    def __post_init__(self):
        """
        Initializes the ArrivalSlot.
        
        Checks that the ArivalSlot does not have microseconds and seconds.
        """

        if self.starts_at.microsecond != 0 or self.starts_at.second != 0:
            raise ValueError("Μη έγκυρη ώρα.")