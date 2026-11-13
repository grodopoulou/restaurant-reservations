import pytest

from reservations.domain.guest_count import GuestCount


def test_accepts_one_or_more_guests():
    """Test the number of guests is the given."""
    assert GuestCount(4).value == 4


def test_rejects_zero_guests():
    """Test the number of guests can not be zero."""
    with pytest.raises(ValueError):
        GuestCount(0)

def test_rejects_negative_guests():
    """Test the number of guests can not be negative number."""
    with pytest.raises(ValueError):
        GuestCount(-3)