import pytest
from datetime import datetime
from reservations.domain.arrival_slot import ArrivalSlot
from reservations.domain.guest_count import GuestCount
from reservations.domain.availability import Availability
from reservations.domain.errors import NotEnoughSeatsError


def test_valid_availability_with_zero_reserve():
    """
    Test that the available seats are the seats given in the capacity if there is not a reservation.
    """
    slot = ArrivalSlot(datetime(2026, 11, 14, 21, 0))
    availability = Availability(slot, capacity=20)
    assert availability.free_seats == 20


def test_valid_availability_with_reserve():
    """
    Test the available seats after the reservation.
    """
    slot = ArrivalSlot(datetime(2026, 11, 14, 21, 0))
    availability = Availability(slot, capacity=20)
    availability.reserve(GuestCount(10))
    assert availability.free_seats == 10


def test_rejects_outnumber_reserved_seats():
    """
    Test that will raise a NotEnoughSeatsError if the reservation's guests are more than the capacity.
    """
    slot = ArrivalSlot(datetime(2026, 11, 14, 21, 0))
    availability = Availability(slot, capacity=10)
    with pytest.raises(NotEnoughSeatsError):
        availability.reserve(GuestCount(15))
    assert availability.free_seats == 10


def test_accepts_seats_availability_equals_reserved():
    """
    Test that there would not be available seats if the reservation's guests are the same with capacity.
    """
    slot = ArrivalSlot(datetime(2026, 11, 14, 21, 0))
    availability = Availability(slot, capacity=10)
    availability.reserve(GuestCount(10))
    assert availability.free_seats == 0


def test_valid_release():
    """
    Test that if a reservation is cancelled, its seats will be released.
    """
    slot = ArrivalSlot(datetime(2026, 11, 14, 21, 0))
    availability = Availability(slot, capacity=20)
    availability.reserve(GuestCount(10))
    availability.release(GuestCount(10))
    assert availability.free_seats == 20


def test_valid_availability_with_release_smaller_than_reserve():
    """
    Test the free seats after one reservation and one release. 
    """
    slot = ArrivalSlot(datetime(2026, 11, 14, 21, 0))
    availability = Availability(slot, capacity=20)
    availability.reserve(GuestCount(10))
    availability.release(GuestCount(4))
    assert availability.free_seats == 14


def test_rejects_availability_with_release_larger_than_reserve():
    """
    Test that will raise a ValueError if the release seats are more than the capacity.
    """
    slot = ArrivalSlot(datetime(2026, 11, 14, 21, 0))
    availability = Availability(slot, capacity=20)
    availability.reserve(GuestCount(10))
    with pytest.raises(ValueError):
        availability.release(GuestCount(15))
    assert availability.free_seats == 10


def test_valid_increasing_capacity():
    """
    Test that if the capacity is increased there would be more free seats. 
    """
    slot = ArrivalSlot(datetime(2026, 11, 14, 21, 0))
    availability = Availability(slot, capacity=20)
    availability.reserve(GuestCount(20))
    availability.change_capacity(40)
    assert availability.free_seats == 20


def test_valid_decreasing_capacity():
    """
    Test that a decrease of the capacity is possible, provided that the resulting capacity remains above the number of reserved seats.
    """
    slot = ArrivalSlot(datetime(2026, 11, 14, 21, 0))
    availability = Availability(slot, capacity=20)
    availability.reserve(GuestCount(5))
    availability.change_capacity(10)
    assert availability.free_seats == 5


def test_rejects_new_capacity_smaller_than_reserve():
    """
    Test that a decrease of the capacity raises ValueError, if it is less than the number of reserved seats.
    """
    slot = ArrivalSlot(datetime(2026, 11, 14, 21, 0))
    availability = Availability(slot, capacity=20)
    availability.reserve(GuestCount(10))
    with pytest.raises(ValueError):
        availability.change_capacity(5)
    assert availability.free_seats == 10


def test_valid_new_capacity_equal_to_reserved_rejects_new_reserve():
    """
    Test that will raise a ValueError if there are no available free seats to be reserved and the availability free seats will remain 0.
    """
    slot = ArrivalSlot(datetime(2026, 11, 14, 21, 0))
    availability = Availability(slot, capacity=20)
    availability.reserve(GuestCount(10))
    availability.change_capacity(10)
    with pytest.raises(ValueError):
        availability.reserve(GuestCount(5))
    assert availability.free_seats == 0