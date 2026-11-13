from reservations.domain.arrival_slot import ArrivalSlot
from reservations.domain.guest_count import GuestCount
from reservations.domain.errors import NotEnoughSeatsError


class Availability:
    """
    A class to represent the availability.
    """
    def __init__(self, arrival_slot: ArrivalSlot, capacity: int):
        """
        Initializes the Availability with arrival_slot and capacity.
        
        Parameters:
        arrival_slot(ArrivalSlot): arrival slot of the reservation
        capacity(int): seating capacity
        """

        if capacity < 0:
            raise ValueError("Η χωρητικότητα δεν μπορεί να είναι αρνητικός αριθμός.")
        self.arrival_slot = arrival_slot
        self.capacity = capacity
        self.reserved_seats = 0

    @property
    def free_seats(self) -> int:
        return self.capacity - self.reserved_seats

    def reserve(self, guest_count: GuestCount) -> None:
        if guest_count.value > self.free_seats:
            raise NotEnoughSeatsError("Δεν υπάρχει διαθέσιμες θέσεις για τη κράτησή.")
        self.reserved_seats += guest_count.value

    def release(self, guest_count: GuestCount) -> None:
        if guest_count.value > self.reserved_seats:
            raise ValueError("Ο αριθμός των θέσεων που αποδεσμεύετε είναι μεγαλύτερος από αυτές που έχουν δεσμευτεί.")
        self.reserved_seats -= guest_count.value

    def change_capacity(self, new_capacity: int) -> None:
        if new_capacity < self.reserved_seats:
            raise ValueError("Δεν μπορείτε να μειώσετε τη χωρητικότητα κάτω από τις δεσμευμένες θέσεις.")
        self.capacity = new_capacity
        