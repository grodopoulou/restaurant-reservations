from dataclasses import dataclass


@dataclass(frozen=True)
class ContactDetails:
    """
    A class that represents the Contact Details of the reservation.

    Attributes:
        surname (str): The last name of the reservation.
        firstname (str): The first name of the reservation.
        email(str): email of the reservation.
        phone(str): phone number of the reservation.
    """
    surname: str
    firstname: str
    email: str
    phone: str

    def __post_init__(self):
        """
        Initialize Contact Details of the reservation. Verify that the data meets the requirements. 
        
        Requirements:
        The reservation must be made under a first and last name. The email address must be valid, and the phone number must consist of 10 digits.

        Args:
            surname (str): The last name of the reservation.
            firstname (str): The first name of the reservation.
            email(str): email of the reservation.
            phone(str): phone number of the reservation.
        """
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