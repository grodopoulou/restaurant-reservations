class OnlineBookingNotAllowedError(Exception):
    """This request is not permitted for online booking."""


class NotEnoughSeatsError(ValueError):
    """Raised when there are not enough available seats."""