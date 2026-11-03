import pytest
from reservations.domain.arrival_slot import ArrivalSlot
from datetime import datetime


def test_valid_arrival_slot():
    arrival = ArrivalSlot(datetime(2026, 11, 14, 21, 0))
    assert arrival.starts_at == datetime(2026, 11, 14, 21, 0)


def test_non_zero_second():
    with pytest.raises(ValueError):
        ArrivalSlot(datetime(2026, 11, 14, 21, 0, 45))


def test_non_zero_microsecond():
    with pytest.raises(ValueError):
        ArrivalSlot(datetime(2026, 11, 14, 21, 0, 0, 15))