import pytest

from reservations.domain.guest_count import GuestCount


def test_accepts_one_or_more_guests():
    assert GuestCount(4).value == 4


def test_rejects_zero_guests():
    with pytest.raises(ValueError):
        GuestCount(0)

def test_rejects_negative_guests():
    with pytest.raises(ValueError):
        GuestCount(-3)