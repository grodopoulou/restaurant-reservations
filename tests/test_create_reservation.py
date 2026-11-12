from datetime import datetime, time
import pytest

from reservations.domain.availability import Availability
from reservations.domain.arrival_slot import ArrivalSlot
from reservations.infrastructure.in_memory import InMemoryAvailabilityRepository, InMemoryReservationRepository
from reservations.domain.contact_details import ContactDetails
from reservations.domain.guest_count import GuestCount
from reservations.domain.booking_policy import BookingPolicy
from reservations.application.create_reservation import CreateReservation
from reservations.application.errors import SlotNotAvailableError
from reservations.domain.errors import OnlineBookingNotAllowedError


def create_reservation():
    slot = ArrivalSlot(datetime(2026, 11, 14, 21, 0))
    contact = ContactDetails(
        "Παπαδοπούλου",
        "Μαρία",
        "papadopoulou@example.com",
        "6979999999",
    )
    guest_count = GuestCount(4)
    policy = BookingPolicy(time(22, 0), time(20, 0), 20, "210 0099988")
    return contact, guest_count, slot, policy


def test_create_reservation_successfully():
    """
    Test that a valid request creates the reservation and reserves the seats.
    """
    availability_repo = InMemoryAvailabilityRepository()
    reservation_repo = InMemoryReservationRepository()
    contact, guest_count, slot, policy = create_reservation()
    availability_repo.save(Availability(slot, 20))
    use_case = CreateReservation(availability_repo, reservation_repo, policy)
    now = datetime(2026, 11, 10, 10, 0)
    created_reservation = use_case.execute(contact, guest_count, slot, now)
    assert reservation_repo.get(created_reservation.id) is created_reservation
    assert availability_repo.get(slot).free_seats == 16


def test_rejects_if_there_is_not_availability():
    """
    Test that a request for a time without Availability is rejected.
    """
    availability_repo = InMemoryAvailabilityRepository()
    reservation_repo = InMemoryReservationRepository()
    contact, guest_count, slot, policy = create_reservation()
    use_case = CreateReservation(availability_repo, reservation_repo, policy)
    now = datetime(2026, 11, 10, 10, 0)
    with pytest.raises(SlotNotAvailableError, match="διαθεσιμότητα"):
        use_case.execute(contact, guest_count, slot, now)


def test_rejects_more_guests_than_available_seats():
    """
    Test that a request for more guests than the number of guests are available is rejected.
    """
    availability_repo = InMemoryAvailabilityRepository()
    reservation_repo = InMemoryReservationRepository()
    contact, guest_count, slot, policy = create_reservation()
    availability_repo.save(Availability(slot, 10))
    use_case = CreateReservation(availability_repo, reservation_repo, policy)
    guest_count = GuestCount(15)
    now = datetime(2026, 11, 10, 10, 0)
    with pytest.raises(ValueError, match="θέσεις"):
        use_case.execute(contact, guest_count, slot, now)
    assert availability_repo.get(slot).free_seats == 10


def test_rejects_more_guests_than_max_guests_of_the_policy():
    """
    Test that a request for more guests than the number of guests in the booking policy is rejected.
    """
    availability_repo = InMemoryAvailabilityRepository()
    reservation_repo = InMemoryReservationRepository()
    contact, guest_count, slot, policy = create_reservation()
    availability_repo.save(Availability(slot, 30))
    new_policy = BookingPolicy(time(22, 0), time(20, 0), 10, "210 0099988")
    use_case = CreateReservation(availability_repo, reservation_repo, new_policy)
    guest_count = GuestCount(15)
    now = datetime(2026, 11, 10, 10, 0)
    with pytest.raises(OnlineBookingNotAllowedError):
        use_case.execute(contact, guest_count, slot, now)
    assert availability_repo.get(slot).free_seats == 30