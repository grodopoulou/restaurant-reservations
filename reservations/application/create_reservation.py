from datetime import datetime

from reservations.domain.arrival_slot import ArrivalSlot
from reservations.domain.booking_policy import BookingPolicy
from reservations.domain.contact_details import ContactDetails
from reservations.domain.guest_count import GuestCount
from reservations.domain.repositories import AvailabilityRepository, ReservationRepository
from reservations.domain.reservation import Reservation
from reservations.application.errors import SlotNotAvailableError


class CreateReservation:
    """
    Use case that is responsible for managing the reservation flow,
    applying policy and availability checks and storing.
    """
    def __init__(self, availability_repo: AvailabilityRepository, reservation_repo: ReservationRepository, policy: BookingPolicy,
    ):
        self._availability_repo = availability_repo
        self._reservation_repo = reservation_repo
        self._policy = policy

    def execute(self, contact: ContactDetails, guest_count: GuestCount, arrival_slot: ArrivalSlot, now: datetime,
    ) -> Reservation:
        """
        Executes the reservation flow:
        1. Checks if the policy permits the request.
        2. Determines availability for the proposed time and verifies that it exists.
        3. Reserves the spots.
        4. Creates the reservation.
        5. Saves the changes and the reservation.
        6. Returns the created reservation.
        """
        self._policy.check(arrival_slot, guest_count, now)
        availability = self._availability_repo.get(arrival_slot)
        if availability is None:
            raise SlotNotAvailableError("Δεν υπάρχει διαθεσιμότητα για την ώρα που επιλέξατε.")
        availability.reserve(guest_count)
        self._availability_repo.save(availability)
        reservation = Reservation(contact, guest_count, arrival_slot)
        self._reservation_repo.add(reservation)
        return reservation
       