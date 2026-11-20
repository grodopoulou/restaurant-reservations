from datetime import datetime
from uuid import uuid4
from reservations.domain.reservation import Reservation, ReservationStatus
from reservations.domain.contact_details import ContactDetails
from reservations.domain.arrival_slot import ArrivalSlot
from reservations.domain.guest_count import GuestCount
from reservations.infrastructure.orm import ReservationRecord


def reservation_to_record(reservation: Reservation):
    """A function that converts a Reservation into a ReservationRecord and returns the ReservationRecord."""
    return ReservationRecord(
        id=reservation.id,
        surname=reservation.contact.surname,
        firstname=reservation.contact.firstname,
        email=reservation.contact.email,
        phone=reservation.contact.phone,
        guest_count=reservation.guest_count.value,
        arrival_slot=reservation.arrival_slot.starts_at,
        status=reservation.status.name
    )


def record_to_reservation(record: ReservationRecord):
    """A function that converts a ReservationRecord into a Reservation and returns the Reservation."""
    
    contact = ContactDetails(
        record.surname,
        record.firstname,
        record.email,
        record.phone
    )
    return Reservation(
        contact,
        guest_count=GuestCount(record.guest_count),
        arrival_slot=ArrivalSlot(record.arrival_slot),
        id=record.id,
        status=ReservationStatus[record.status]
    )
