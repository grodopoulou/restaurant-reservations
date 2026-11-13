import pytest
from datetime import datetime
from reservations.domain.arrival_slot import ArrivalSlot
from reservations.domain.guest_count import GuestCount
from reservations.domain.contact_details import ContactDetails
from reservations.domain.reservation import Reservation, ReservationStatus


def my_reservation():
    return Reservation(ContactDetails("Παπαδοπούλου", "Μαρία", "papadopoulou@example.com", "6979999999"), GuestCount(4), ArrivalSlot(datetime(2026, 11, 14, 21, 0)))


def test_new_reservation_is_confirmed():
    """
        Test a new reservation if the status is Confirmed.
    """
    reservation = my_reservation()
    assert reservation.status == ReservationStatus.CONFIRMED


def test_a_reservation_to_be_cancelled():
    """
    Test if we cancel a reservation the Reservation Status should be Cancelled.
    """
    reservation = my_reservation()
    reservation.cancel()
    assert reservation.status == ReservationStatus.CANCELLED


def test_rejects_cancel_an_already_cancelled_reservation():
    """
    Test a cancelled reservation should not be cancelled.
    Raises ValueError.
    """
    reservation = my_reservation()
    reservation.cancel()
    with pytest.raises(ValueError):
        reservation.cancel()
    assert reservation.status == ReservationStatus.CANCELLED


def test_id_must_be_unique():
    """
    Test if two reservations with same details have two different ids.
    """
    reservation1 = my_reservation()
    reservation2 = my_reservation()
    assert reservation1.id != reservation2.id