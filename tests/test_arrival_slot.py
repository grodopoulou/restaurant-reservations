import pytest
from reservations.domain.arrival_slot import ArrivalSlot
from datetime import datetime


def test_valid_arrival_slot():
    """
    Test that the arrival slot is valid. Valid is the arrival slot that has not microseconds and seconds.
    """
    arrival = ArrivalSlot(datetime(2026, 11, 14, 21, 0))
    assert arrival.starts_at == datetime(2026, 11, 14, 21, 0)


def test_non_zero_second():
    """
    Test that the arrival slot is raises ValueError if seconds are given.
    """
    with pytest.raises(ValueError):
        ArrivalSlot(datetime(2026, 11, 14, 21, 0, 45))


def test_non_zero_microsecond():
    """
    Test that the arrival slot is raises ValueError if seconds are given.
    """
    with pytest.raises(ValueError):
        ArrivalSlot(datetime(2026, 11, 14, 21, 0, 0, 15))