class SlotNotAvailableError(Exception):
    """Custom Error that indicates that there is no availability for the selected time."""


class ReservationNotFoundError(Exception):
    """Custom Error when a reservation cannot be found."""