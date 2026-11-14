class SlotNotAvailableError(Exception):
    """Custom Error that indicates that there is no availability for the selected time."""


class ReservationNotFoundError(Exception):
    """Custom Error when a reservation cannot be found."""


class SeatsAvailableError(Exception):
    """Custom Error when there are enough seats for reservation and do not need join to a waitlist entry."""


class WaitlistEntryNotFoundError(Exception):
    """Custom Error when a waitlist entry cannot be found."""