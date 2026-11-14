from datetime import datetime, time
import pytest
from uuid import uuid4

from reservations.infrastructure.in_memory import InMemoryWaitlistRepository, InMemoryAvailabilityRepository
from reservations.domain.arrival_slot import ArrivalSlot
from reservations.domain.contact_details import ContactDetails
from reservations.domain.guest_count import GuestCount
from reservations.domain.availability import Availability
from reservations.domain.booking_policy import BookingPolicy
from reservations.domain.waitlist_entry import WaitlistEntry, WaitlistStatus
from reservations.application.join_waitlist import JoinWaitlist
from reservations.application.cancel_waitlist_entry import CancelWaitlistEntry
from reservations.application.errors import  WaitlistEntryNotFoundError



def request_data():
    """ A function with request and policy data. """
    slot = ArrivalSlot(datetime(2026, 11, 14, 21, 0))
    contact = ContactDetails(
        "Παπαδοπούλου",
        "Μαρία",
        "papadopoulou@example.com",
        "6979999999",
    )
    guest_count = GuestCount(4)
    policy = BookingPolicy(time(22, 0), time(20, 0), 20, "210 0099988")
    now = datetime(2026, 11, 10, 10, 0)
    return contact, guest_count, slot, policy, now


def test_cancel_waitlist_entry_successfully():
    """ 
    Test that cancelling a waitlist entry sets its status to CANCELLED.
    """
    waitlist_repo = InMemoryWaitlistRepository()  
    contact, guest_count, slot, policy, now = request_data()
    entry = WaitlistEntry(contact, guest_count, slot)
    waitlist_repo.add(entry)
    use_case = CancelWaitlistEntry(waitlist_repo)
    use_case.execute(entry.id)
    assert entry.status == WaitlistStatus.CANCELLED
    assert waitlist_repo.get(entry.id) is entry


def test_cancel_waitlist_not_found():
    """ 
    Test that cancelling a waitlist entry that does not exist raises a WaitlistEntryNotFoundError.
    """
    waitlist_repo = InMemoryWaitlistRepository()  
    contact, guest_count, slot, policy, now = request_data()
    entry = WaitlistEntry(contact, guest_count, slot)
    use_case = CancelWaitlistEntry(waitlist_repo)
    with pytest.raises(WaitlistEntryNotFoundError, match="αναμονή"):
        use_case.execute(entry.id)
    assert waitlist_repo.get_all() == []


def test_double_cancel_waitlist_entry():
    """ 
    Test that cancelling a waitlist entry that has been cancelled raises a ValueError.
    """
    waitlist_repo = InMemoryWaitlistRepository()  
    contact, guest_count, slot, policy, now = request_data()
    entry = WaitlistEntry(contact, guest_count, slot)
    waitlist_repo.add(entry)
    use_case = CancelWaitlistEntry(waitlist_repo)
    use_case.execute(entry.id)
    with pytest.raises(ValueError, match="ακυρωθεί"):
        use_case.execute(entry.id)
    assert waitlist_repo.get(entry.id).status == WaitlistStatus.CANCELLED