from abc import ABC, abstractmethod
from uuid import UUID

from reservations.domain.arrival_slot import ArrivalSlot
from reservations.domain.availability import Availability
from reservations.domain.reservation import Reservation
from reservations.domain.waitlist_entry import WaitlistEntry


class AvailabilityRepository(ABC):
    """
    Interface that defines how Availability is stored and located.
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
    Interface that defines how Reservation is stored and located.
    """
    @abstractmethod
    def add(self, reservation: Reservation) -> None:
        """
        Adds a new reservation. It does not return anything.
        """

    @abstractmethod
    def get(self, reservation_id: UUID) -> Reservation | None:
        """
        Returns the reservation, or None if it does not exist.
        """


class WaitlistRepository(ABC):
    """
    Interface that defines how waitlist entries are stored and retrieved.
    """
    @abstractmethod
    def add(self, waitlist_entry: WaitlistEntry) -> None:
        """
        Adds a new WaitlistEntry. It does not return anything.
        """

    @abstractmethod
    def get(self, waitlist_entry_id: UUID) -> WaitlistEntry | None:
        """
        Returns the WaitlistEntry, or None if it does not exist.
        """

    @abstractmethod
    def get_all(self) -> list[WaitlistEntry]:
        """
        Returns a list of WaitlistEntries, or an empty list if none exists.
        """

    @abstractmethod
    def save(self, waitlist_entry: WaitlistEntry) -> None:
        """
        Saves the updated WaitlistEntry. It does not return anything.
        """