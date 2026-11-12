from uuid import UUID

from reservations.domain.repositories import AvailabilityRepository, ReservationRepository
from reservations.application.errors import SlotNotAvailableError, ReservationNotFoundError


class CancelReservation:
    """
    Use case that cancels the reservation.
    """
    def __init__(self, reservation_repo: ReservationRepository,availability_repo: AvailabilityRepository,
    ):
        self._reservation_repo = reservation_repo
        self._availability_repo = availability_repo

    def execute(self, reservation_id: UUID):
        reservation = self._reservation_repo.get(reservation_id)
        if reservation is None:
            raise ReservationNotFoundError("Η κράτηση δε βρέθηκε.")
        available = self._availability_repo.get(reservation.arrival_slot)
        if available is None:
            raise SlotNotAvailableError("Δεν υπάρχει διαθεσιμότητα για την κράτηση")
        reservation.cancel()
        available.release(reservation.guest_count)
        self._availability_repo.save(available)