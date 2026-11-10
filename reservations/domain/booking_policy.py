from dataclasses import dataclass
from datetime import datetime, time

from reservations.domain.arrival_slot import ArrivalSlot
from reservations.domain.guest_count import GuestCount
from reservations.domain.errors import OnlineBookingNotAllowedError


@dataclass(frozen=True)
class BookingPolicy:
    """
        This class defines the booking policy.

        Parameters:
        last_online_arrival_time (time): latest arrival time for which online booking is accepted
        same_day_cutoff_time (time): the time until online reservations are accepted
        max_guest_count (int): maximum group size per online booking
        restaurant_phone (str): the phone number that will appear in the message
    """
    last_online_arrival_time: time
    same_day_cutoff_time: time
    max_guest_count: int
    restaurant_phone: str

    def check(self, arrival_slot: ArrivalSlot, guest_count: GuestCount, now: datetime):
        """
            This function checks whether the reservation violates the rules defined by the admin.

            Rules:
            1. The arrival time could not be after the last_online_arrival_time.
            2. The reservation group could not be larger than max_guest_count.
            3. For same-day reservations, the current time cannot be after same_day_cutoff_time.
            4. The arrival time could not be in the past.
        """
        if arrival_slot.starts_at.time() > self.last_online_arrival_time:
            raise OnlineBookingNotAllowedError(f"Για κρατήσεις μετά τις {self.last_online_arrival_time:%H:%M} παρακαλώ επικοινωνήστε απευθείας στο κατάστημα. Το τηλέφωνο: {self.restaurant_phone}")
        if guest_count.value > self.max_guest_count:
            raise OnlineBookingNotAllowedError(f"Οι Online κρατήσεις είναι μέχρι {self.max_guest_count}. Για κρατήσεις περισσότερων ατόμων, επικοινωνήστε με το κατάστημα. Το τηλέφωνο: {self.restaurant_phone}")
        if arrival_slot.starts_at.date() == now.date() and self.same_day_cutoff_time < now.time():
            raise OnlineBookingNotAllowedError(f"Οι Online κρατήσεις είναι μέχρι {self.same_day_cutoff_time:%H:%M}. Για κρατήσεις μετά από αυτή την ώρα, παρακαλώ επικοινωνήστε με το κατάστημα: {self.restaurant_phone}")
        if arrival_slot.starts_at < now:
            raise OnlineBookingNotAllowedError("Η ώρα κράτησης δεν μπορεί να είναι πριν από την τωρινή ώρα.")