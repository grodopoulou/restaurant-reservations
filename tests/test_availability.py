import pytest
from datetime import datetime
from reservations.domain.arrival_slot import ArrivalSlot
from reservations.domain.guest_count import GuestCount
from reservations.domain.availability import Availability


def test_valid_availability_with_zero_reserve():
    slot = ArrivalSlot(datetime(2026, 11, 14, 21, 0))
    availability = Availability(slot, capacity=20)
    assert availability.free_seats == 20


def test_valid_availability_with_reserve():
    slot = ArrivalSlot(datetime(2026, 11, 14, 21, 0))
    availability = Availability(slot, capacity=20)
    availability.reserve(GuestCount(10))
    assert availability.free_seats == 10


def test_rejects_outnumber_reserved_seats():
    slot = ArrivalSlot(datetime(2026, 11, 14, 21, 0))
    availability = Availability(slot, capacity=10)
    with pytest.raises(ValueError):
        availability.reserve(GuestCount(15))
    assert availability.free_seats == 10


def test_accepts_seats_availability_equals_reserved():
    slot = ArrivalSlot(datetime(2026, 11, 14, 21, 0))
    availability = Availability(slot, capacity=10)
    availability.reserve(GuestCount(10))
    assert availability.free_seats == 0