from datetime import datetime
from uuid import uuid4
import pytest
import copy

from reservations.domain.availability import Availability
from reservations.domain.arrival_slot import ArrivalSlot
from reservations.infrastructure.in_memory import InMemoryAvailabilityRepository, InMemoryReservationRepository, InMemoryWaitlistRepository
from reservations.domain.contact_details import ContactDetails
from reservations.domain.guest_count import GuestCount
from reservations.domain.reservation import Reservation
from reservations.domain.waitlist_entry import WaitlistEntry


def my_reservation():
    """Makes a reservation for tests"""
    return Reservation(ContactDetails("Παπαδοπούλου", "Μαρία", "papadopoulou@example.com", "6979999999"), GuestCount(4), ArrivalSlot(datetime(2026, 11, 14, 21, 0)))


def my_waitlist_entry():
    """Makes a waitlist entry for tests"""
    return WaitlistEntry(ContactDetails("Παπαδοπούλου", "Μαρία", "papadopoulou@example.com", "6979999999"), GuestCount(4), ArrivalSlot(datetime(2026, 11, 14, 21, 0)))


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


def test_add_waitlist_entry():
    """
    Test that a new waitlist entry is successfully added
    and can be retrieved using its ID.
    """
    repo = InMemoryWaitlistRepository()
    waitlist_entry = my_waitlist_entry()
    repo.add(waitlist_entry)
    assert repo.get(waitlist_entry.id) is waitlist_entry


def test_add_duplicate_waitlist_entry():
    """
    Test that adding a waitlist entry with an existing ID
    raises a ValueError.
    """
    repo = InMemoryWaitlistRepository()
    waitlist_entry = my_waitlist_entry()
    repo.add(waitlist_entry)
    with pytest.raises(ValueError):
        repo.add(waitlist_entry)


def test_get_non_existing_waitlist_entry():
    """
    Test that retrieving a waitlist entry with a non-existing ID
    returns None.
    """
    repo = InMemoryWaitlistRepository()
    assert repo.get(uuid4()) is None


def test_get_all_waitlist_entries():
    """
    Test that get_all returns all waitlist entries stored
    in the repository.
    """
    repo = InMemoryWaitlistRepository()
    waitlist_entry1 = my_waitlist_entry()
    waitlist_entry2 = WaitlistEntry(ContactDetails("Γεωργακοπούλου", "Ελένη", "georgakopoulou@example.com", "6979999999"), GuestCount(5), ArrivalSlot(datetime(2026, 11, 14, 21, 0)))
    waitlist_entry3 = WaitlistEntry(ContactDetails("Πετράκη", "Δήμητρα", "petraki@example.com", "6979999999"), GuestCount(7), ArrivalSlot(datetime(2026, 11, 14, 21, 0)))
    repo.add(waitlist_entry1)
    repo.add(waitlist_entry2)
    repo.add(waitlist_entry3)
    assert len(repo.get_all()) == 3
    assert repo.get_all() == [waitlist_entry1, waitlist_entry2, waitlist_entry3]



def test_get_all_returns_empty_list():
    """
    Test that get_all returns an empty list when there are no waitlist entries stored in the repository.
    """
    repo = InMemoryWaitlistRepository()
    assert repo.get_all() == []


def test_save_existing_waitlist_entry():
    """
    Test that save updates an existing waitlist entry
    while preserving its ID.
    """
    repo = InMemoryWaitlistRepository()
    waitlist_entry = my_waitlist_entry()
    repo.add(waitlist_entry)
    new_waitlist_entry = copy.deepcopy(waitlist_entry)
    new_waitlist_entry.guest_count = 10
    repo.save(new_waitlist_entry)
    assert repo.get(waitlist_entry.id).guest_count == 10
    assert repo.get(waitlist_entry.id).id == waitlist_entry.id


def test_save_non_existing_waitlist_entry():
    """
    Test that saving a non-existing waitlist entry raises a ValueError.
    """
    repo = InMemoryWaitlistRepository()
    waitlist_entry = my_waitlist_entry()
    with pytest.raises(ValueError):
        repo.save(waitlist_entry)