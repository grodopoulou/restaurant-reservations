import pytest
from datetime import datetime, time
from reservations.domain.arrival_slot import ArrivalSlot
from reservations.domain.guest_count import GuestCount
from reservations.domain.booking_policy import BookingPolicy
from reservations.domain.errors import OnlineBookingNotAllowedError


def my_policy():
    """ 
    Make a policy.
    """
    return BookingPolicy(time(22, 0), time(20, 0), 20, "210 0099988")


def test_accepts_valid_request():
    """
    Test accepts a valid request.
    """
    policy = my_policy()
    assert policy.check(ArrivalSlot(datetime(2026, 11, 14, 21, 0)), GuestCount(10), now=datetime(2026, 11, 14, 12, 0)) is None


def test_rejects_arrival_time_after_last_online_arrival_time():
    """
    Test rejects arrival time after the arrival cutoff.
    """
    policy = my_policy()
    with pytest.raises(OnlineBookingNotAllowedError, match="22:00"):
        policy.check(ArrivalSlot(datetime(2026, 11, 14, 22, 30)), GuestCount(10), now=datetime(2026, 11, 14, 12, 0))


def test_accepts_arrival_time_same_with_last_online_arrival_time():
    """
    Test accepts the arrival time to be the same as the latest arrival time online booking is accepted.
    """
    policy = my_policy()
    assert policy.check(ArrivalSlot(datetime(2026, 11, 14, 22, 0)), GuestCount(10), now=datetime(2026, 11, 14, 12, 0)) is None


def test_accepts_guest_count_equal_to_max():
    """
    Test accepts the number of guests to be the same as the maximum guest size per online booking.
    """
    policy = my_policy()
    assert policy.check(ArrivalSlot(datetime(2026, 11, 14, 21, 0)), GuestCount(20), now=datetime(2026, 11, 14, 12, 0)) is None


def test_rejects_more_guests_than_guest_count():
    """
    Test rejects the number of guests be more than the maximum guest size per online booking.
    """
    policy = my_policy()
    with pytest.raises(OnlineBookingNotAllowedError, match="περισσότερων"):
        policy.check(ArrivalSlot(datetime(2026, 11, 14, 21, 0)), GuestCount(25), now=datetime(2026, 11, 14, 12, 0))


def test_rejects_online_booking_after_same_day_cutoff_time():
    """
    Test rejects the online booking time be after the same day's cutoff time.
    """
    policy = my_policy()
    with pytest.raises(OnlineBookingNotAllowedError, match="20:00"):
        policy.check(ArrivalSlot(datetime(2026, 11, 14, 21, 0)), GuestCount(15), now=datetime(2026, 11, 14, 20, 30))


def test_rejects_arrival_in_the_past():
    """
    Test rejects an online booking day that is for a previous day.
    """
    policy = my_policy()
    with pytest.raises(OnlineBookingNotAllowedError, match="τωρινή"):
        policy.check(ArrivalSlot(datetime(2026, 11, 12, 21, 0)), GuestCount(10), now=datetime(2026, 11, 14, 12, 0))


def test_accepts_arrival_time_be_after_same_day_cutoff_time_for_another_day():
    """
    Test accepts an online booking time that is after the same day's cutoff time if the request is for another day.
    """
    policy = my_policy()
    assert policy.check(ArrivalSlot(datetime(2026, 11, 16, 21, 0)), GuestCount(10), now=datetime(2026, 11, 14, 21, 0)) is None