from datetime import datetime, time
import pytest
from uuid import uuid4

from reservations.domain.availability import Availability
from reservations.domain.arrival_slot import ArrivalSlot
from reservations.domain.reservation import ReservationStatus, Reservation
from reservations.infrastructure.in_memory import InMemoryAvailabilityRepository, InMemoryReservationRepository
from reservations.domain.contact_details import ContactDetails
from reservations.domain.guest_count import GuestCount
from reservations.domain.booking_policy import BookingPolicy
from reservations.application.create_reservation import CreateReservation
from reservations.application.cancel_reservation import CancelReservation
from reservations.application.errors import SlotNotAvailableError, ReservationNotFoundError


def request_data():
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


def test_cancel_reservation_successfully():
    """
    Test that cancelling a reservation releases its seats and this reservation status is cancelled. 
    """
    availability_repo = InMemoryAvailabilityRepository()
    reservation_repo = InMemoryReservationRepository()
    contact, guest_count, slot, policy, now = request_data()
    availability_repo.save(Availability(slot, 20))
    new_reservation = CreateReservation(availability_repo, reservation_repo, policy)
    created_reservation = new_reservation.execute(contact, guest_count, slot, now)
    cancel_reservation = CancelReservation(reservation_repo, availability_repo)
    cancel_reservation.execute(created_reservation.id)
    assert reservation_repo.get(created_reservation.id).status == ReservationStatus.CANCELLED
    assert availability_repo.get(slot).free_seats == 20


def test_cancel_reservation_not_found():
    """
    Test that cancelling a non-existing reservation raises an error.
    """
    availability_repo = InMemoryAvailabilityRepository()
    reservation_repo = InMemoryReservationRepository()
    cancel_reservation = CancelReservation(reservation_repo, availability_repo)
    with pytest.raises(ReservationNotFoundError, match="κράτηση"):
        cancel_reservation.execute(uuid4())


def test_cancel_reservation_availability_not_found():
    """
    Test that cancelling a reservation without availability raises error.
    """
    availability_repo = InMemoryAvailabilityRepository()
    reservation_repo = InMemoryReservationRepository()
    contact, guest_count, slot, policy, now = request_data()
    reservation = Reservation(contact, guest_count, slot)
    reservation_repo.add(reservation)
    cancel_reservation = CancelReservation(reservation_repo, availability_repo)
    with pytest.raises(SlotNotAvailableError, match="διαθεσιμότητα"):
        cancel_reservation.execute(reservation.id)
    assert reservation.status == ReservationStatus.CONFIRMED


def test_rejects_double_cancellation():
    """
    Test that cancelling an already cancelled reservation
    raises an error without releasing seats again.
    """
    availability_repo = InMemoryAvailabilityRepository()
    reservation_repo = InMemoryReservationRepository()
    contact, guest_count, slot, policy, now = request_data()
    availability_repo.save(Availability(slot, 20))
    new_reservation = CreateReservation(availability_repo, reservation_repo, policy)
    created_reservation = new_reservation.execute(contact, guest_count, slot, now)
    cancel_reservation = CancelReservation(reservation_repo, availability_repo)
    cancel_reservation.execute(created_reservation.id)
    assert availability_repo.get(slot).free_seats == 20
    with pytest.raises(ValueError, match="ακυρωμένη"):
        cancel_reservation.execute(created_reservation.id)
    assert availability_repo.get(slot).free_seats == 20


def test_rejects_cancel_reservation_twice():
    """
    Test that cancelling an already cancelled reservation
    raises ValueError and does not restore seats more than once.
    """
    availability_repo = InMemoryAvailabilityRepository()
    reservation_repo = InMemoryReservationRepository()
    contact, guest_count, slot, policy, now = request_data()
    availability_repo.save(Availability(slot, 20))
    new_reservation = CreateReservation(availability_repo, reservation_repo, policy)
    created_reservation1 = new_reservation.execute(contact, guest_count, slot, now)
    created_reservation2 = new_reservation.execute(contact, guest_count, slot, now)
    cancel_reservation = CancelReservation(reservation_repo, availability_repo)
    cancel_reservation.execute(created_reservation1.id)
    with pytest.raises(ValueError, match="ακυρωμένη"):
            cancel_reservation.execute(created_reservation1.id)
    assert availability_repo.get(slot).free_seats == 16