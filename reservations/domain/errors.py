class OnlineBookingNotAllowedError(Exception):
    """Raised when the request is not permitted for online booking."""


class NotEnoughSeatsError(ValueError):
    """Raised when there are not enough available seats."""


class UnknownReservationError(ValueError):
    """Raised when saving a reservation that the repository does not know."""