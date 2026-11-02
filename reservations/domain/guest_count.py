from dataclasses import dataclass


@dataclass(frozen=True)
class GuestCount:
    value: int

    def __post_init__(self):
        if self.value < 1:
           raise ValueError("Οι κρατήσεις θα πρέπει να είναι από ένα (1) άτομο και πάνω.")
        