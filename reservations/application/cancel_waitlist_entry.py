from uuid import UUID

from reservations.domain.repositories import WaitlistRepository
from reservations.application.errors import WaitlistEntryNotFoundError


class CancelWaitlistEntry:
    """
    Use case that cancels the waitlist entry.
    """
    def __init__(self, waitlist_repo: WaitlistRepository,):
        self._waitlist_repo = waitlist_repo

    def execute(self, waitlist_entry_id: UUID):
        """
        Executes the cancellation process:
        1. Find the waitlist entry using its ID.
        2. Checks if there is waitlist entry else raise error.
        3. Cancel the waitlist entry.
        4. Save the changes.
        """
        waitlist = self._waitlist_repo.get(waitlist_entry_id)
        if waitlist is None:
            raise WaitlistEntryNotFoundError("Η αναμονή δεν βρέθηκε.")
        waitlist.cancel()
        self._waitlist_repo.save(waitlist)