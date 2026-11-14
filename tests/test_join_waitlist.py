from datetime import datetime, time
import pytest

from reservations.domain.availability import Availability
from reservations.domain.arrival_slot import ArrivalSlot
from reservations.infrastructure.in_memory import InMemoryAvailabilityRepository, InMemoryWaitlistRepository
from reservations.domain.contact_details import ContactDetails
from reservations.domain.guest_count import GuestCount
from reservations.domain.booking_policy import BookingPolicy
from reservations.application.join_waitlist import JoinWaitlist
from reservations.application.errors import SlotNotAvailableError, SeatsAvailableError
from reservations.domain.errors import OnlineBookingNotAllowedError


def request_data():
    """ A function with request and policy data. """
    slot = ArrivalSlot(datetime(2026, 11, 14, 21, 0))
    contact = ContactDetails(
        "Παπαδοπούλου",
        "Μαρία",
        "papadopoulou@example.com",
        "6979999999",
    )
    guest_count = GuestCount(25)
    policy = BookingPolicy(time(22, 0), time(20, 0), 50, "210 0099988")
    return contact, guest_count, slot, policy

def test_join_waitlist_successfully():
    """
    Test that a valid request creates the waitlist entry and the number of free seats does not change.
    """
    availability_repo = InMemoryAvailabilityRepository()
    waitlist_repo = InMemoryWaitlistRepository()
    contact, guest_count, slot, policy = request_data()
    availability_repo.save(Availability(slot, 20))
    use_case = JoinWaitlist(waitlist_repo, availability_repo, policy)
    now = datetime(2026, 11, 10, 10, 0)
    assert availability_repo.get(slot).free_seats < guest_count.value
    join_waitlist = use_case.execute(contact, guest_count, slot, now)
    assert waitlist_repo.get(join_waitlist.id) is join_waitlist
    assert availability_repo.get(slot).free_seats == 20


def test_join_waitlist_slot_not_available():
    """
    Test that if there is not availability a SlotNotAvailableError will be raised and ensure that waitlist will be still empty.
    """
    availability_repo = InMemoryAvailabilityRepository()
    waitlist_repo = InMemoryWaitlistRepository()
    contact, guest_count, slot, policy = request_data()
    use_case = JoinWaitlist(waitlist_repo, availability_repo, policy)
    now = datetime(2026, 11, 10, 10, 0)
    with pytest.raises(SlotNotAvailableError, match="ώρα"):
        use_case.execute(contact, guest_count, slot, now)
    assert waitlist_repo.get_all() == []


def test_seats_available_more_than_guests():
    """
    Test that if the free seats are more than the guest count then a SeatsAvailableError will be raised and the waitlist will be empty.
    """
    availability_repo = InMemoryAvailabilityRepository()
    waitlist_repo = InMemoryWaitlistRepository()
    contact, guest_count, slot, policy = request_data()
    availability_repo.save(Availability(slot, 30))
    use_case = JoinWaitlist(waitlist_repo, availability_repo, policy)
    now = datetime(2026, 11, 10, 10, 0)
    assert availability_repo.get(slot).free_seats >= guest_count.value
    with pytest.raises(SeatsAvailableError, match="θέσεις"):
        use_case.execute(contact, guest_count, slot, now)
    assert waitlist_repo.get_all() == []


def test_seats_available_same_as_guests():
    """
    Test that if the free seats are the same number with the guest count then a SeatsAvailableError will be raised and the waitlist will be empty.
    """
    availability_repo = InMemoryAvailabilityRepository()
    waitlist_repo = InMemoryWaitlistRepository()
    contact, guest_count, slot, policy = request_data()
    availability_repo.save(Availability(slot, 25))
    use_case = JoinWaitlist(waitlist_repo, availability_repo, policy)
    now = datetime(2026, 11, 10, 10, 0)
    assert availability_repo.get(slot).free_seats >= guest_count.value
    with pytest.raises(SeatsAvailableError, match="θέσεις"):
        use_case.execute(contact, guest_count, slot, now)
    assert waitlist_repo.get_all() == []


def test_guest_count_more_than_max_guest_count():
    """
    Test that if the number of guests are more than the maximum guest size per online booking then an OnlineBookingNotAllowedError will be raised.
    """
    availability_repo = InMemoryAvailabilityRepository()
    waitlist_repo = InMemoryWaitlistRepository()
    contact, guest_count, slot, policy = request_data()
    availability_repo.save(Availability(slot, 25))
    use_case = JoinWaitlist(waitlist_repo, availability_repo, policy)
    now = datetime(2026, 11, 10, 10, 0)
    guest_count = GuestCount(60)
    assert availability_repo.get(slot).free_seats < guest_count.value
    with pytest.raises(OnlineBookingNotAllowedError, match="ατόμων"):
        use_case.execute(contact, guest_count, slot, now)
    assert waitlist_repo.get_all() == []