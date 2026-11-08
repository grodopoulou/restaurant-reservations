from abc import ABC, abstractmethod
from uuid import UUID

from reservations.domain.arrival_slot import ArrivalSlot
from reservations.domain.availability import Availability
from reservations.domain.reservation import Reservation


class AvailabilityRepository(ABC):
    """
    Interface that defines how Availability is stored and located
    """
    @abstractmethod
    def get(self, arrival_slot: ArrivalSlot) -> Availability | None:
        """
        Returns the availability for the time, or None if it does not exist.
        """

    @abstractmethod
    def save(self, availability: Availability) -> None:
        """
        Saves the Availability (new or updated).
        """


class ReservationRepository(ABC):
    """
    Interface that defines how Reservation is stored and located
    """
    @abstractmethod
    def add(self, reservation: Reservation) -> None:
        """
        Stores a new reservation. It does not return anything.
        """

    @abstractmethod
    def get(self, reservation_id: UUID) -> Reservation | None:
        """
        Returns the reservation, or None if it does not exist.
        """