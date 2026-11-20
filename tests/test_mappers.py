from datetime import datetime
from uuid import uuid4
from reservations.domain.arrival_slot import ArrivalSlot
from reservations.domain.guest_count import GuestCount
from reservations.domain.contact_details import ContactDetails
from reservations.domain.reservation import Reservation, ReservationStatus
from reservations.infrastructure.mappers import reservation_to_record, record_to_reservation
from reservations.infrastructure.orm import ReservationRecord


def test_reservation_is_mapped_to_record():
    """
    Test that a reservation is converted successfully into ReservationRecord.
    """
    contact = ContactDetails("Παπαδοπούλου", "Μαρία", "papadopoulou@example.com", "6979999999")
    guest_count = GuestCount(4)
    slot = ArrivalSlot(datetime(2026, 11, 14, 21, 0))
    reservation = Reservation(contact, guest_count, slot)
    record = reservation_to_record(reservation)
    assert isinstance(record, ReservationRecord)
    assert record.id == reservation.id
    assert record.surname == "Παπαδοπούλου"
    assert record.firstname == "Μαρία"
    assert record.email == "papadopoulou@example.com"
    assert record.phone == "6979999999"
    assert record.guest_count == 4
    assert record.arrival_slot == datetime(2026, 11, 14, 21, 0)
    assert record.status == "CONFIRMED"


def test_record_is_mapped_to_reservation():
    """
    Test that a ReservationRecord is converted successfully into Reservation.
    """
    record_id = uuid4()
    record = ReservationRecord(
        id=record_id,
        surname="Παπαδοπούλου",
        firstname="Μαρία",
        email="papadopoulou@gmail.com",
        phone="6979999999",
        guest_count= 4,
        arrival_slot= datetime(2026, 11, 14, 21, 0),
        status="CANCELLED"
        )
    reservation = record_to_reservation(record)
    assert isinstance(reservation, Reservation)
    assert reservation.id == record_id
    assert reservation.status == ReservationStatus.CANCELLED
    assert reservation.contact.surname == "Παπαδοπούλου"
    assert reservation.contact.firstname == "Μαρία"
    assert reservation.contact.email == "papadopoulou@gmail.com"
    assert reservation.contact.phone == "6979999999"
    assert reservation.guest_count.value == 4
    assert reservation.arrival_slot.starts_at == datetime(2026, 11, 14, 21, 0)
    