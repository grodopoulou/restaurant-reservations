from reservations.domain.arrival_slot import ArrivalSlot
from reservations.domain.contact_details import ContactDetails
from reservations.domain.guest_count import GuestCount

from enum import Enum
from uuid import uuid4


class WaitlistStatus(Enum):
    """
        A class to represent the status of the waiting list.
        ENUM because we have three values for the status of the waiting list.
        WAITING,
        PROMOTED,
        CANCELLED
    """
    WAITING = "Waiting"
    PROMOTED = "Promoted"
    CANCELLED = "Cancelled"


class WaitlistEntry():
    """
        Entity with a unique id.
    """
    def __init__(self, contact: ContactDetails, guest_count: GuestCount, arrival_slot: ArrivalSlot):
        """
            Initializes the details of the waiting list.
        
            Parameters are the same with the reservation:
            contact (ContactDetails): contact details of the reservation
            guest_count (GuestCount): the number of guest for the reservation
            arrival_slot (ArrivalSlot): the arrival datetime
        
        """
        self.id = uuid4()
        self.contact = contact
        self.guest_count = guest_count
        self.arrival_slot = arrival_slot
        self.status = WaitlistStatus.WAITING

    def cancel(self):
        """
            Cancel a reservation of the waiting list if the status is waiting.
    
            Raises:
                ValueError: If the waiting status is not waiting.
        """
        if self.status != WaitlistStatus.WAITING:
            raise ValueError("Η αίτηση αναμονής που ζητήσατε δεν μπορεί να ακυρωθεί.")
        self.status = WaitlistStatus.CANCELLED

    def promote(self):
        """
            Promote a reservation of the waiting list if the status is waiting.
        
            Raises:
                ValueError: If the waiting status is not waiting.
        """
        if self.status != WaitlistStatus.WAITING:
            raise ValueError("Η αίτηση αναμονή που ζητήσατε δεν μπορεί να γίνει κράτηση.")
        self.status = WaitlistStatus.PROMOTED