from datetime import datetime
from uuid import uuid4

from reservations.domain.availability import Availability
from reservations.domain.arrival_slot import ArrivalSlot
from reservations.infrastructure.in_memory import InMemoryAvailabilityRepository, InMemoryReservationRepository
from reservations.domain.contact_details import ContactDetails
from reservations.domain.guest_count import GuestCount
from reservations.domain.reservation import Reservation


def my_reservation():
    """Makes a reservation for tests"""
    return Reservation(ContactDetails("Παπαδοπούλου", "Μαρία", "papadopoulou@example.com", "6979999999"), GuestCount(4), ArrivalSlot(datetime(2026, 11, 14, 21, 0)))


def test_get_returns_none_for_unknown_arrival_slot():
    """
    Test that get returns None for an arrival slot that has not been saved.
    """
    repo = InMemoryAvailabilityRepository()
    assert repo.get(ArrivalSlot(datetime(2026, 11, 14, 21, 0))) is None


def test_get_returns_saved_availability_for_same_arrival_slot():
    """
    Test that a new ArrivalSlot with the same time, gets the stored Availability.
    """
    repo = InMemoryAvailabilityRepository()
    slot1 = ArrivalSlot(datetime(2026, 11, 14, 21, 0))
    slot2 = ArrivalSlot(datetime(2026, 11, 14, 21, 0))
    availability = Availability(slot1, capacity=20)
    repo.save(availability)
    found = repo.get(slot2)
    assert found is availability


def test_get_returns_none_for_unknown_reservation_id():
    """
    Test that get returns None for a reservation_id that does not exist.
    """
    repo = InMemoryReservationRepository()
    assert repo.get(reservation_id = uuid4()) is None


def test_get_returns_added_reservation_for_its_id():
    """
    Test that a new Reservation with a unique id, gets the stored Reservation.
    """
    repo = InMemoryReservationRepository()
    reserv = my_reservation()
    repo.add(reserv)
    found = repo.get(reserv.id)
    assert found is reserv