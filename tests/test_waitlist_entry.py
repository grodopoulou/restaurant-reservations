import pytest
from datetime import datetime
from reservations.domain.arrival_slot import ArrivalSlot
from reservations.domain.guest_count import GuestCount
from reservations.domain.contact_details import ContactDetails
from reservations.domain.waitlist_entry import WaitlistStatus, WaitlistEntry


def my_waitlist_entry():
    """
        Make a wait list entry.
    """
    return WaitlistEntry(ContactDetails("Παπαδοπούλου", "Μαρία", "papadopoulou@example.com", "6979999999"), GuestCount(4), ArrivalSlot(datetime(2026, 11, 14, 21, 0)))


def test_new_waitlist_entry_is_waiting():
    """
        Test a new wait list entry if the status is Waiting.
    """
    waitlist_entry = my_waitlist_entry()
    assert waitlist_entry.status == WaitlistStatus.WAITING


def test_a_waitlist_entry_to_be_cancelled():
    """
        Test if we cancel a wait list entry the Waitlist Status should be Cancelled.
    """
    waitlist_entry = my_waitlist_entry()
    waitlist_entry.cancel()
    assert waitlist_entry.status == WaitlistStatus.CANCELLED


def test_a_waitlist_entry_to_be_promoted():
    """
        Test if we promote a wait list entry the Waitlist Status should be Promoted.
    """
    waitlist_entry = my_waitlist_entry()
    waitlist_entry.promote()
    assert waitlist_entry.status == WaitlistStatus.PROMOTED


def test_rejects_cancel_an_already_cancelled_waitlist_entry():
    """
        Test a cancelled wait list entry should not be cancelled.
        Raises ValueError.
    """
    waitlist_entry = my_waitlist_entry()
    waitlist_entry.cancel()
    with pytest.raises(ValueError):
        waitlist_entry.cancel()
    assert waitlist_entry.status == WaitlistStatus.CANCELLED


def test_rejects_cancel_a_promoted_waitlist_entity():
    """
        Test a promoted wait list entry should not be cancelled.
        Raises ValueError.
    """
    waitlist_entry = my_waitlist_entry()
    waitlist_entry.promote()
    with pytest.raises(ValueError):
        waitlist_entry.cancel()
    assert waitlist_entry.status == WaitlistStatus.PROMOTED


def test_rejects_promote_a_cancell_waitlist_entity():
    """
        Test a cancelled wait list entry should not be promoted.
        Raises ValueError.
    """
    waitlist_entry = my_waitlist_entry()
    waitlist_entry.cancel()
    with pytest.raises(ValueError):
        waitlist_entry.promote()
    assert waitlist_entry.status == WaitlistStatus.CANCELLED


def test_id_must_be_unique():
    """
        Test if two wait list entities with same details have two different ids.
    """
    waitlist_entry1 = my_waitlist_entry()
    waitlist_entry2 = my_waitlist_entry()
    assert waitlist_entry1.id != waitlist_entry2.id