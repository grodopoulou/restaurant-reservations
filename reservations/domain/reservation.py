from reservations.domain.arrival_slot import ArrivalSlot
from reservations.domain.guest_count import GuestCount
from reservations.domain.contact_details import ContactDetails

from uuid import uuid4
from enum import Enum


class ReservationStatus(Enum):
    """
        A class to represent the status of a reservation.
        ENUM because we have two values for the reservation status.
        CANCELLED,
        CONFIRMED
    """
    CANCELLED = "Cancelled"
    CONFIRMED = "Confirmed"


class Reservation:
    """
        Entity with a unique id.
    """
    def __init__(self, contact: ContactDetails, guest_count: GuestCount, arrival_slot: ArrivalSlot):
        """
        Initializes the reservation.

        Parameters:
            contact (ContactDetails): contact details of the reservation
            guest_count (GuestCount): the number of guest for the reservation
            arrival_slot (ArrivalSlot): the arrival datetime

        """
        self.id = uuid4()
        self.contact = contact
        self.guest_count = guest_count
        self.arrival_slot = arrival_slot
        self.status = ReservationStatus.CONFIRMED

    def cancel(self):
        """
        Cancel a reservation if that is confirmed.

        Raises:
            ValueError: If the reservation is cancelled because we can not cancel a cancelled reservation.
        """
        if self.status == ReservationStatus.CANCELLED:
            raise ValueError("Η κράτηση είναι ήδη ακυρωμένη.")
        self.status = ReservationStatus.CANCELLED
