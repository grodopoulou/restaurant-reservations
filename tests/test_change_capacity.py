import pytest
from datetime import datetime

from reservations.domain.availability import Availability
from reservations.domain.arrival_slot import ArrivalSlot
from reservations.domain.guest_count import GuestCount
from reservations.infrastructure.in_memory import InMemoryAvailabilityRepository
from reservations.application.change_capacity import ChangeCapacity
from reservations.application.errors import SlotNotAvailableError


def test_change_capacity_successfully():
    """ Test a valid change of capacity is saved. """
    availability_repo = InMemoryAvailabilityRepository()
    slot = ArrivalSlot(datetime(2026, 11, 14, 21, 0))
    availability_repo.save(Availability(slot, 20))
    use_case = ChangeCapacity(availability_repo)
    use_case.execute(slot, 40)
    assert availability_repo.get(slot).capacity == 40


def test_rejects_change_capacity_for_closed_time():
    """
    Test that if the time of the arrival slot is closed then a change of capacity raises a SlotNotAvailableError.
    """
    availability_repo = InMemoryAvailabilityRepository()
    slot = ArrivalSlot(datetime(2026, 11, 14, 21, 0))
    use_case = ChangeCapacity(availability_repo)
    with pytest.raises(SlotNotAvailableError, match="ώρα"):
        use_case.execute(slot, 40)
    assert availability_repo.get(slot) is None


def test_rejects_change_capacity_less_reserved_seats():
    """
    Tests that changing the capacity with fewer than the reserved seats will raise ValueError.
    """
    availability_repo = InMemoryAvailabilityRepository()
    slot = ArrivalSlot(datetime(2026, 11, 14, 21, 0))
    availability_repo.save(Availability(slot, 20))
    availability_repo.get(slot).reserve(GuestCount(20))
    use_case = ChangeCapacity(availability_repo)
    with pytest.raises(ValueError, match="δεσμευμένες"):
        use_case.execute(slot, 15)
    assert availability_repo.get(slot).capacity == 20
    assert availability_repo.get(slot).reserved_seats == 20