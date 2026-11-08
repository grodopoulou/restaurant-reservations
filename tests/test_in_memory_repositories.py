import pytest
from datetime import datetime

from reservations.domain.availability import Availability
from reservations.domain.arrival_slot import ArrivalSlot
from reservations.infrastructure.in_memory import InMemoryAvailabilityRepository


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