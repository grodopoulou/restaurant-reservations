from datetime import datetime, time
import pytest

from reservations.domain.availability import Availability
from reservations.domain.arrival_slot import ArrivalSlot
from reservations.infrastructure.in_memory import InMemoryAvailabilityRepository,InMemoryReservationRepository, InMemoryWaitlistRepository
from reservations.domain.contact_details import ContactDetails
from reservations.domain.guest_count import GuestCount
from reservations.domain.booking_policy import BookingPolicy
from reservations.domain.reservation import ReservationStatus
from reservations.domain.waitlist_entry import WaitlistEntry, WaitlistStatus
from reservations.application.promote_from_waitlist import PromoteFromWaitlist
from reservations.application.errors import SlotNotAvailableError,WaitlistEntryNotFoundError
from reservations.domain.errors import NotEnoughSeatsError


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


def test_promote_from_waitlist_successfully():
    """
    Test that a valid promote request creates a reservation with status Confirmed, change the waitlist status to Promoted, reduce the number of free seats and the waitlist_entry arrival slot and guest count is the same with the reservation. 
    """
    availability_repo = InMemoryAvailabilityRepository()
    reservation_repo = InMemoryReservationRepository()
    waitlist_repo = InMemoryWaitlistRepository()
    contact, guest_count, slot, policy = request_data()
    availability_repo.save(Availability(slot, 40))
    waitlist_entry = WaitlistEntry(contact, guest_count, slot)
    waitlist_repo.add(waitlist_entry)
    use_case = PromoteFromWaitlist(waitlist_repo, reservation_repo, availability_repo)
    reservation = use_case.execute(waitlist_entry.id)
    assert reservation is reservation_repo.get(reservation.id)
    assert reservation_repo.get(reservation.id).status == ReservationStatus.CONFIRMED
    assert waitlist_repo.get(waitlist_entry.id).status == WaitlistStatus.PROMOTED
    assert availability_repo.get(slot).free_seats == 15
    assert waitlist_entry.guest_count == reservation.guest_count
    assert waitlist_entry.arrival_slot == reservation.arrival_slot


def test_waitlist_entry_not_found():
    """
    Test that if there is not a waitlist entry then raises a WaitlistEntryNotFoundError, the waitlist repo will be empty and the available seats does not change.
    """   
    availability_repo = InMemoryAvailabilityRepository()
    reservation_repo = InMemoryReservationRepository()
    waitlist_repo = InMemoryWaitlistRepository()
    contact, guest_count, slot, policy = request_data()
    availability_repo.save(Availability(slot, 40))
    waitlist_entry = WaitlistEntry(contact, guest_count, slot)
    use_case = PromoteFromWaitlist(waitlist_repo, reservation_repo, availability_repo)
    with pytest.raises(WaitlistEntryNotFoundError, match="αναμονή"):
        use_case.execute(waitlist_entry.id)
    assert waitlist_repo.get_all() == []
    assert availability_repo.get(slot).free_seats == 40


def test_slot_not_available():
    """
    Test that if there is not availability then a SlotNotAvailableError will be raised and the waitlist_entry status is still Waiting.
    """
    availability_repo = InMemoryAvailabilityRepository()
    reservation_repo = InMemoryReservationRepository()
    waitlist_repo = InMemoryWaitlistRepository()
    contact, guest_count, slot, policy = request_data()
    waitlist_entry = WaitlistEntry(contact, guest_count, slot)
    waitlist_repo.add(waitlist_entry)
    use_case = PromoteFromWaitlist(waitlist_repo, reservation_repo, availability_repo)
    with pytest.raises(SlotNotAvailableError, match="διαθεσιμότητα"):
        use_case.execute(waitlist_entry.id)
    assert waitlist_repo.get(waitlist_entry.id).status == WaitlistStatus.WAITING


def test_not_enough_seats_to_promote():
    """
    Test that if there are not enough seats available to promote the waitlist entry then raise a NotEnoughSeatsError, the waitlist status will be Waiting and the available seats does not change.
    """
    availability_repo = InMemoryAvailabilityRepository()
    reservation_repo = InMemoryReservationRepository()
    waitlist_repo = InMemoryWaitlistRepository()
    contact, guest_count, slot, policy = request_data()
    availability_repo.save(Availability(slot, 24))
    waitlist_entry = WaitlistEntry(contact, guest_count, slot)
    waitlist_repo.add(waitlist_entry)
    use_case = PromoteFromWaitlist(waitlist_repo, reservation_repo, availability_repo)
    with pytest.raises(NotEnoughSeatsError, match="θέσεις"):
        use_case.execute(waitlist_entry.id)
    assert waitlist_repo.get(waitlist_entry.id).status == WaitlistStatus.WAITING
    assert availability_repo.get(slot).free_seats == 24


def test_rejects_promote_cancelled_waitlist_entry():
    """
    Test that if a cancelled waitlist_entry try to be promoted then raises a ValueError, the waitlist status remains Cancelled and the available free seats does not change.
    """
    availability_repo = InMemoryAvailabilityRepository()
    reservation_repo = InMemoryReservationRepository()
    waitlist_repo = InMemoryWaitlistRepository()
    contact, guest_count, slot, policy = request_data()
    availability_repo.save(Availability(slot, 40))
    waitlist_entry = WaitlistEntry(contact, guest_count, slot)
    waitlist_repo.add(waitlist_entry)
    waitlist_entry.cancel()
    use_case = PromoteFromWaitlist(waitlist_repo, reservation_repo, availability_repo)
    with pytest.raises(ValueError, match="κατάσταση"):
        use_case.execute(waitlist_entry.id)
    assert waitlist_repo.get(waitlist_entry.id).status == WaitlistStatus.CANCELLED
    assert availability_repo.get(slot).free_seats == 40


def test_double_promote_waitlist_entry():
    """
    Test that if a promoted waitlist_entry try to be promoted again then raises a ValueError, the waitlist status remains Promoted and the available free seats does not change again. 
    """
    availability_repo = InMemoryAvailabilityRepository()
    reservation_repo = InMemoryReservationRepository()
    waitlist_repo = InMemoryWaitlistRepository()
    contact, guest_count, slot, policy = request_data()
    availability_repo.save(Availability(slot, 60))
    waitlist_entry = WaitlistEntry(contact, guest_count, slot)
    waitlist_repo.add(waitlist_entry)
    use_case = PromoteFromWaitlist(waitlist_repo, reservation_repo, availability_repo)
    use_case.execute(waitlist_entry.id)
    with pytest.raises(ValueError, match="κατάσταση"):
        use_case.execute(waitlist_entry.id)
    assert waitlist_repo.get(waitlist_entry.id).status == WaitlistStatus.PROMOTED
    assert availability_repo.get(slot).free_seats == 35


def test_promote_with_exactly_enough_seats():
    """
    Test that if the available free seats are equal to guests from the waitlist entry then the waitlist entry will be promoted and there would not be other seats available. 
    """
    availability_repo = InMemoryAvailabilityRepository()
    reservation_repo = InMemoryReservationRepository()
    waitlist_repo = InMemoryWaitlistRepository()
    contact, guest_count, slot, policy = request_data()
    availability_repo.save(Availability(slot, 25))
    waitlist_entry = WaitlistEntry(contact, guest_count, slot)
    waitlist_repo.add(waitlist_entry)
    use_case = PromoteFromWaitlist(waitlist_repo, reservation_repo, availability_repo)
    reservation = use_case.execute(waitlist_entry.id)
    assert reservation is reservation_repo.get(reservation.id)
    assert reservation_repo.get(reservation.id).status == ReservationStatus.CONFIRMED
    assert waitlist_repo.get(waitlist_entry.id).status == WaitlistStatus.PROMOTED
    assert availability_repo.get(slot).free_seats == 0