from uuid import UUID

from reservations.domain.repositories import AvailabilityRepository, ReservationRepository
from reservations.domain.availability import Availability
from reservations.domain.arrival_slot import ArrivalSlot
from reservations.domain.reservation import Reservation


class InMemoryAvailabilityRepository(AvailabilityRepository):
    """
    Keeps the Availability in memory and is used for tests.

    Functions:
        Save
        Get
    """
    def __init__(self):
        """
        It creates an empty dictionary. The field is internal and cannot be accessed from outside.
        """
        self._items = {}

    def save(self, availability: Availability):
        """
        Saves the Availability (new or updated).

        Args:
            availability (Availability): the availability, capacity and reserved seats, of one arrival slot. Updates if availability exists

        Returns: 
        Nothing
        """
        self._items[availability.arrival_slot] = availability

    def get(self, arrival_slot: ArrivalSlot) -> Availability | None:
        """
        Gets the availability for a specific time.
        
        Args:
            arrival_slot (ArrivalSlot): the time for the arrival.

        Returns:
        The availability for the time, or None if it does not exist.
        """
        return self._items.get(arrival_slot)



class InMemoryReservationRepository(ReservationRepository):
    """
    Keeps the Reservation in memory and is used for tests.

    Functions:
        Add
        Get
    """
    def __init__(self):
        """
        It creates an empty dictionary. The field is internal and cannot be accessed from outside.
        """
        self._items = {}

    def add(self, reservation: Reservation):
        """
        Stores the Reservation.
        
        Args:
            reservation (Reservation): the contact details, number of guests and arrival_slot information of the reservation.
        
        Returns: 
        Nothing
        """
        self._items[reservation.id] = reservation

    def get(self, reservation_id: UUID) -> Reservation | None:
        """
        Gets the reservation of a unique id.

        Args:
            reservation_id (UUID): unique id for a specific reservation.
        
        Returns:
        The reservation for this unique id, or None if it does not exist.
        """
        return self._items.get(reservation_id)