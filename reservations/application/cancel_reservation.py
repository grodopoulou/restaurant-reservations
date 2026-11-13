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
        """
        Executes the cancellation process:
        1. Find the reservation using its ID.
        2. Checks if there is reservation.
        3. Find the availability for its time slot.
        4. Checks if there is availability.
        5. Cancel the booking.
        6. Release its reserved spots.
        7. Save the availability.
        """
        reservation = self._reservation_repo.get(reservation_id)
        if reservation is None:
            raise ReservationNotFoundError("Η κράτηση δεν βρέθηκε.")
        available = self._availability_repo.get(reservation.arrival_slot)
        if available is None:
            raise SlotNotAvailableError("Δεν υπάρχει διαθεσιμότητα για την κράτηση")
        reservation.cancel()
        available.release(reservation.guest_count)
        self._availability_repo.save(available)