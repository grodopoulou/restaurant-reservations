import datetime

from reservations.domain.repositories import AvailabilityRepository, WaitlistRepository
from reservations.domain.booking_policy import BookingPolicy
from reservations.domain.guest_count import GuestCount
from reservations.domain.contact_details import ContactDetails
from reservations.domain.arrival_slot import ArrivalSlot
from reservations.domain.waitlist_entry import WaitlistEntry
from reservations.application.errors import SlotNotAvailableError, SeatsAvailableError


class  JoinWaitlist:
    """
    Use case that add an entry to the waitlist.
    """
    def __init__(self, waitlist_repo: WaitlistRepository,availability_repo: AvailabilityRepository, policy: BookingPolicy,
    ):
        self._waitlist_repo = waitlist_repo
        self._availability_repo = availability_repo
        self._policy = policy

    def execute(self, contact: ContactDetails, guest_count: GuestCount, arrival_slot: ArrivalSlot, now: datetime, ) -> WaitlistEntry:
        """
        Executes the join in the waitlist flow:
        1. Checks if the policy permits the request.
        2. Checks the availability for the proposed time and raises a SlotNotAvailableError if there is not.
        3. Checks if there are enough seats and raise error.
        4. Creates the waitlist entry.
        5. Add waitlist entry.
        6. Returns the created waitlist entry.
        """
        self._policy.check(arrival_slot, guest_count, now)
        availability = self._availability_repo.get(arrival_slot)
        if availability is None:
            raise SlotNotAvailableError("Δεν υπάρχει διαθεσιμότητα για την ώρα που επιλέξατε.")
        if availability.free_seats >= guest_count.value:
            raise SeatsAvailableError("Υπάρχουν επαρκής θέσεις για κράτηση.") 
        waitlist = WaitlistEntry(contact, guest_count, arrival_slot)
        self._waitlist_repo.add(waitlist)
        return waitlist