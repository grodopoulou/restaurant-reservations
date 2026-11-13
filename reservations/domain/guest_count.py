from dataclasses import dataclass


@dataclass(frozen=True)
class GuestCount:
    """
    A class to represent the number of the guest.
    """
    value: int

    def __post_init__(self):
        """
        Initializes the GuestCount.

        Raises ValueError:
        if the number of guest is less than 1.
        """
        if self.value < 1:
           raise ValueError("Οι κρατήσεις θα πρέπει να είναι από ένα (1) άτομο και πάνω.")
        