from datetime import datetime, time

from reservations.domain.availability import Availability
from reservations.domain.arrival_slot import ArrivalSlot
from reservations.infrastructure.in_memory import InMemoryAvailabilityRepository, InMemoryReservationRepository
from reservations.domain.contact_details import ContactDetails
from reservations.domain.guest_count import GuestCount
from reservations.domain.booking_policy import BookingPolicy
from reservations.application.create_reservation import CreateReservation


def test_create_reservation_successfully():
    """
    Test that a valid request creates the reservation and reserves the seats.
    """
    availability_repo = InMemoryAvailabilityRepository()
    reservation_repo = InMemoryReservationRepository()
    slot = ArrivalSlot(datetime(2026, 11, 14, 21, 0))
    availability_repo.save(Availability(slot, 20))
    policy = BookingPolicy(time(22, 0), time(20, 0), 20, "210 0099988")
    use_case = CreateReservation(availability_repo, reservation_repo, policy)
    contact = ContactDetails("Παπαδοπούλου", "Μαρία", "papadopoulou@example.com", "6979999999")
    guest_count = GuestCount(4)
    now = datetime(2026, 11, 10, 10, 0)
    created_reservation = use_case.execute(contact, guest_count, slot, now)
    assert reservation_repo.get(created_reservation.id) is created_reservation
    assert availability_repo.get(slot).free_seats == 16


    