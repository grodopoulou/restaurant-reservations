from reservations.domain.arrival_slot import ArrivalSlot
from reservations.domain.repositories import AvailabilityRepository
from reservations.application.errors import SlotNotAvailableError


class ChangeCapacity:
    """
    Use case that changes the capacity.
    """
    def __init__(self, availability_repo: AvailabilityRepository):
        self._availability_repo = availability_repo

    def execute(self, arrival_slot: ArrivalSlot, new_capacity: int):
        """
        Executes the change capacity process:
        1. Find the availability for the time being.
        2. If there is no availability raise SlotNotAvailableError
        3. Change the capacity.
        4. Save the changes.
        """
        availability = self._availability_repo.get(arrival_slot)
        if availability is None:
            raise SlotNotAvailableError("Δεν υπάρχει διαθεσιμότητα για την ώρα που επιλέξατε.")
        availability.change_capacity(new_capacity)
        self._availability_repo.save(availability)