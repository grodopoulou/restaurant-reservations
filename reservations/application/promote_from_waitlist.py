from uuid import UUID

from reservations.domain.reservation import Reservation
from reservations.domain.repositories import AvailabilityRepository, ReservationRepository, WaitlistRepository
from reservations.domain.errors import NotEnoughSeatsError
from reservations.domain.waitlist_entry import WaitlistStatus
from reservations.application.errors import WaitlistEntryNotFoundError, SlotNotAvailableError


class PromoteFromWaitlist:
    """
    Use case that promotes a waitlist entry to a confirmed reservation.
    Used by the admin, who picks the entry from the waitlist.
    """
    def __init__(self, waitlist_repo: WaitlistRepository, reservation_repo: ReservationRepository, availability_repo: AvailabilityRepository,
    ):
        self._waitlist_repo = waitlist_repo
        self._reservation_repo = reservation_repo
        self._availability_repo = availability_repo

    def execute(self, waitlist_entry_id: UUID) -> Reservation:
        """
        Executes the promotion process:
        1. Find the waitlist entry using its ID.
        2. If there is no such entry, raise WaitlistEntryNotFoundError.
        3. Find the availability for the entry's arrival slot.
        4. If there is no availability, raise SlotNotAvailableError.
        5. If the seats are not enough raise NotEnoughSeatsError.
        6. If the waitlist status is not Waiting, raise ValueError.
        7. Create the Reservation from the entry's contact, guest count
        and arrival slot.
        8. Reserve the seats.
        9. Promote the waitlist entry.
        10. Add the reservation, save the availability and save the
        waitlist entry.
        11. Return the reservation.
        """
        waitlist = self._waitlist_repo.get(waitlist_entry_id)
        if waitlist is None:
            raise WaitlistEntryNotFoundError("Δεν υπάρχει η αναμονή που ζητήσατε.")
        availability = self._availability_repo.get(waitlist.arrival_slot)
        if availability is None:
            raise SlotNotAvailableError("Δεν υπάρχει διαθεσιμότητα.")
        
        if waitlist.guest_count.value > availability.free_seats:
            raise NotEnoughSeatsError("Δεν υπάρχουν αρκετές θέσεις για τη κράτηση.")
        if waitlist.status != WaitlistStatus.WAITING:
            raise ValueError("Ελέγξτε την κατάσταση της αναμονής.")
        reservation = Reservation(waitlist.contact, waitlist.guest_count, waitlist.arrival_slot)
        availability.reserve(waitlist.guest_count)
        waitlist.promote()
        self._reservation_repo.add(reservation)
        self._availability_repo.save(availability)
        self._waitlist_repo.save(waitlist)
        return reservation