from dataclasses import dataclass


@dataclass(frozen=True)
class ContactDetails:
    surname: str
    firstname: str
    email: str
    phone: str

    def __post_init__(self):
        if not self.surname.strip() or not self.firstname.strip():
            raise ValueError ("Παρακαλώ συμπληρώστε το ονοματεπώνυμο της κράτησης.")
        if not self.email.strip():
            raise ValueError ("Μη έγκυρο email. Παρακαλώ συμπληρώστε email επικοινωνίας")
        if "@" not in self.email.strip():
            raise ValueError ("Μη έγκυρο email. Παρακαλώ δώστε έγκυρο email.")
        if not self.phone.strip():
            raise ValueError ("Μη έγκυρο τηλέφωνο.Παρακαλώ συμπληρώστε έγκυρο τηλέφωνο επικοινωνίας")
        if not self.phone.isdigit():
            raise ValueError ("Μη έγκυρο τηλέφωνο. Το τηλέφωνο θα πρέπει να αποτελείται μόνο από αριθμούς.")
        if len(self.phone) != 10:
            raise ValueError ("Μη έγκυρο τηλέφωνο. Το τηλέφωνο θα πρέπει να αποτελείται από 10 ψηφία.")