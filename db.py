import datetime

from settings import dbase, spare_parts_db, root_logger
import sys
import traceback
from sqlalchemy import create_engine, Column, Integer, Text, Boolean, ForeignKey, asc
from sqlalchemy.orm import sessionmaker, relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import exists

sys.stderr.write = root_logger.error
sys.stdout.write = root_logger.info

service_engine = create_engine(f"sqlite:///{dbase}")
service_session = sessionmaker(bind=service_engine)()
service_base = declarative_base()
service_conn = service_session.bind

store_engine = create_engine(f"sqlite:///{spare_parts_db}")
store_session = sessionmaker(bind=store_engine)()
store_base = declarative_base()
store_conn = store_session.bind


# ----------------------------------------------------Tables --------------------------------
class Calendar(service_base):
    __tablename__ = 'Calendar'

    ID = Column(Integer, primary_key=True, autoincrement=True)

    Ημερομηνία = Column("Ημερομηνία", Text)
    Πελάτης = Column(Text)
    Μηχάνημα = Column(Text)
    Σκοπός = Column(Text)
    Ενέργειες = Column(Text)
    Τεχνικός = Column(Text)
    Ημ_Ολοκλ = Column(Text)
    Επείγων = Column(Text)
    Τηλέφωνο = Column(Text)
    Σημειώσεις = Column(Text)
    Copier_ID = Column(Integer, ForeignKey('Φωτοτυπικά.ID'))
    machine = relationship("Machine", backref=backref("calendar"))
    # consumable = relationship("Consumables", backref=backref("calendar"))
    ΔΤΕ = Column(Text)
    Service_ID = Column(Text)
    Μετρητής = Column(Text)
    Επ_Service = Column(Text)
    Customer_ID = Column(Text)
    Price = Column(Text)
    Κατάσταση = Column(Boolean, default=True)

    def __repr__(self):
        return "<Calendar(ID='%i', Ημερομηνία='%s', Πελάτης='%s', Μηχάνημα='%s', Σκοπός='%s', Ενέργειες='%s'" \
               "Τεχνικός='%s', Ημ_Ολοκλ='%s', Επείγων='%s', Τηλέφωνο='%s', Σημειώσεις='%s', Copier_ID='%i'" \
               "machine='%s', ΔΤΕ='%s', Service_ID='%s', Μετρητής='%s', Επ_Service='%s', Customer_ID='%i'" \
               "Price='%s', Κατάσταση='%i')>" \
               % (self.ID, self.Ημερομηνία, self.Πελάτης, self.Μηχάνημα, self.Σκοπός, self.Ενέργειες,
                  self.Τεχνικός, self.Ημ_Ολοκλ, self.Επείγων, self.Τηλέφωνο, self.Σημειώσεις, self.Copier_ID,
                  self.machine, self.ΔΤΕ, self.Service_ID, self.Μετρητής, self.Επ_Service, self.Customer_ID,
                  self.Price, self.Κατάσταση)

    def __str__(self):
        return f"{self.Ημερομηνία} {self.Πελάτης} {self.Μηχάνημα}" \
               f"{self.Σκοπός} {self.Ενέργειες} {self.Τεχνικός} {self.Ημ_Ολοκλ} {self.Επείγων} {self.Τηλέφωνο}" \
               f"{self.Σημειώσεις} {self.Copier_ID} {self.machine} {self.ΔΤΕ} {self.Service_ID} {self.Μετρητής} " \
               f"{self.Επ_Service} {self.Customer_ID} {self.Price} {self.Κατάσταση}"


class Machine(service_base):
    __tablename__ = 'Φωτοτυπικά'

    ID = Column(Integer, primary_key=True, autoincrement=True)

    Εταιρεία = Column(Text)
    Serial = Column(Text)
    Εναρξη = Column(Text)
    Μετρητής_έναρξης = Column(Text)
    Πελάτη_ID = Column(Integer, ForeignKey('Πελάτες.ID'))  # __tablename__ = 'Πελάτες'
    # customer = relationship("Customer", backref=backref("machine"))
    service = relationship("Service", backref=backref("machine"), order_by="Service.Ημερομηνία")
    Σημειώσεις = Column(Text)
    Κατάσταση = Column(Boolean, default=True)

    def __repr__(self):
        return "<Machine(ID='%i', Εταιρεία='%s', Serial='%s', Εναρξη='%s', Μετρητής_έναρξης='%s', Πελάτη_ID='%i', " \
               "Σημειώσεις='%s', Κατάσταση='%i')>" % (self.ID, self.Εταιρεία, self.Serial, self.Εναρξη,
                                                      self.Μετρητής_έναρξης, self.Πελάτη_ID,
                                                      self.Σημειώσεις, self.Κατάσταση)

    def __str__(self):
        return f"{self.Εταιρεία} {self.Serial} {self.Εναρξη}" \
               f"{self.Μετρητής_έναρξης} {self.Πελάτη_ID} {self.Σημειώσεις} {self.Κατάσταση} {self.service}"


class Customer(service_base):
    __tablename__ = 'Πελάτες'

    ID = Column(Integer, primary_key=True, autoincrement=True)

    Επωνυμία_Επιχείρησης = Column(Text, unique=True)
    Ονοματεπώνυμο = Column(Text)
    Διεύθυνση = Column(Text)
    Πόλη = Column(Text)
    Ταχ_Κώδικας = Column(Text)
    Περιοχή = Column(Text)
    Τηλέφωνο = Column(Text)
    Κινητό = Column(Text)
    Φαξ = Column(Text)
    E_mail = Column(Text)
    Σελίδες_πακέτου = Column(Text)
    Κόστος_πακέτου = Column(Text)
    Σημειώσεις = Column(Text)
    machines = relationship("Machine", backref=backref("Customer"))
    Κατάσταση = Column(Boolean, default=True)

    def __repr__(self):
        return "<Customer(ID='%i', Επωνυμία_Επιχείρησης='%s', Ονοματεπώνυμο='%s', Διεύθυνση='%s', Πόλη='%s', " \
               "Ταχ_Κώδικας='%s', Περιοχή='%s', Τηλέφωνο='%s', Κινητό='%s', Φαξ='%s', E_mail='%s', Σελίδες_πακέτου='%s'" \
               "Κόστος_πακέτου='%s', Σημειώσεις='%s', Κατάσταση='%i')>" \
               % (self.ID, self.Επωνυμία_Επιχείρησης, self.Ονοματεπώνυμο, self.Διεύθυνση, self.Πόλη, self.Ταχ_Κώδικας,
                  self.Περιοχή, self.Τηλέφωνο, self.Κινητό, self.Φαξ, self.E_mail, self.Σελίδες_πακέτου,
                  self.Κόστος_πακέτου, self.Σημειώσεις, self.Κατάσταση)

    def __str__(self):
        return f"{self.Επωνυμία_Επιχείρησης} {self.Ονοματεπώνυμο} {self.Διεύθυνση}" \
               f"{self.Πόλη} {self.Ταχ_Κώδικας} {self.Περιοχή} {self.Τηλέφωνο} {self.Κινητό} {self.Φαξ}" \
               f"{self.E_mail} {self.Σελίδες_πακέτου} {self.Κόστος_πακέτου} {self.Σημειώσεις} {self.Κατάσταση}"


class Companies(service_base):
    __tablename__ = 'Companies'

    ID = Column(Integer, primary_key=True, autoincrement=True)

    Εταιρεία = Column(Text)
    Κατηγορία_μηχανήματος = Column(Text)

    def __repr__(self):
        return "<Companies(id='%i', Εταιρεία='%s', Κατηγορία_μηχανήματος='%s')>" \
               % (self.ID, self.Εταιρεία, self.Κατηγορία_μηχανήματος)

    def __str__(self):
        return f"{self.Εταιρεία} {self.Κατηγορία_μηχανήματος}"


class Copiers_Log(service_base):
    __tablename__ = 'Copiers_Log'

    ID = Column(Integer, primary_key=True, autoincrement=True)

    ID_μηχανήματος = Column(Text, ForeignKey('Φωτοτυπικά.ID'))
    machine = relationship("Machine", backref=backref("transfers_Log"))
    Μηχάνημα = Column(Text)
    Ημερομηνία = Column(Text)
    Προηγούμενος_Πελάτης = Column(Text)
    Νέος_Πελάτης = Column(Text)
    Σημειώσεις = Column(Text)

    def __repr__(self):
        return "<Copiers_Log(ID='%i', ID_μηχανήματος='%i', machine='%s', Μηχάνημα='%s', Ημερομηνία='%s', " \
               "Προηγούμενος_Πελάτης='%s', Νέος_Πελάτης='%s', Σημειώσεις='%s')>" \
               % (self.ID, self.ID_μηχανήματος, self.machine, self.Μηχάνημα, self.Ημερομηνία, self.Προηγούμενος_Πελάτης,
                  self.Νέος_Πελάτης, self.Σημειώσεις)

    def __str__(self):
        return f"{self.ID_μηχανήματος} {self.machine} {self.Μηχάνημα} {self.Ημερομηνία} {self.Προηγούμενος_Πελάτης}" \
               f"{self.Νέος_Πελάτης} {self.Σημειώσεις}"


class Service(service_base):
    __tablename__ = 'Service'

    ID = Column(Integer, primary_key=True, autoincrement=True)

    Ημερομηνία = Column(Text)
    Σκοπός_Επίσκεψης = Column(Text)
    Ενέργειες = Column(Text)
    Τεχνικός = Column(Text)
    Σημειώσεις = Column(Text)
    Μετρητής = Column(Text)
    Επ_Service = Column(Text)
    Copier_ID = Column(Integer, ForeignKey('Φωτοτυπικά.ID'))
    consumable = relationship("Consumables", backref=backref("service"))
    # consumable = relationship("Consumables", backref=backref("service"), order_by="Service.Ημερομηνία")
    ΔΤΕ = Column(Text)
    Price = Column(Text)

    def __repr__(self):
        return "<Service(ID='%i', Ημερομηνία='%s', Σκοπός_Επίσκεψης='%s', Ενέργειες='%s', Τεχνικός='%s', Σημειώσεις='%s'" \
               "Μετρητής='%s', Επ_Service='%s', Copier_ID='%i', ΔΤΕ='%s', Price='%s', consumable='%s')>" \
               % (self.ID, self.Ημερομηνία, self.Σκοπός_Επίσκεψης, self.Ενέργειες, self.Τεχνικός, self.Σημειώσεις,
                  self.Μετρητής, self.Επ_Service, self.Copier_ID, self.ΔΤΕ, self.Price, self.consumable)

    def __str__(self):
        return f"{self.Ημερομηνία} {self.Σκοπός_Επίσκεψης} {self.Ενέργειες} {self.Τεχνικός} {self.Σημειώσεις}" \
               f"{self.Μετρητής} {self.Επ_Service} {self.Copier_ID} {self.ΔΤΕ} {self.Price} {self.consumable}"


class Consumables(service_base):
    __tablename__ = 'Ανταλλακτικά'

    ID = Column(Integer, primary_key=True, autoincrement=True)

    PARTS_NR = Column(Text)
    ΠΕΡΙΓΡΑΦΗ = Column(Text)
    ΚΩΔΙΚΟΣ = Column(Text)
    ΤΕΜΑΧΙΑ = Column(Text)
    ΠΑΡΑΤΗΡΗΣΗΣ = Column(Text)
    ΜΗΧΑΝΗΜΑ = Column(Text)
    Service_ID = Column(Integer, ForeignKey('Service.ID'))
    Customer_ID = Column(Integer, ForeignKey('Πελάτες.ID'))
    customer = relationship("Customer", backref=backref("consumables"))
    Calendar_ID = Column(Text)

    def __repr__(self):
        return "<Consumables(ID='%i', PARTS_NR='%s', ΠΕΡΙΓΡΑΦΗ='%s', ΚΩΔΙΚΟΣ='%s', ΤΕΜΑΧΙΑ='%s', ΠΑΡΑΤΗΡΗΣΗΣ='%s'," \
               "ΜΗΧΑΝΗΜΑ='%s', Service_ID='%i', Customer_ID='%i', Calendar_ID='%s')>" \
               % (self.ID, self.PARTS_NR, self.ΠΕΡΙΓΡΑΦΗ, self.ΚΩΔΙΚΟΣ, self.ΤΕΜΑΧΙΑ, self.ΠΑΡΑΤΗΡΗΣΗΣ, self.ΜΗΧΑΝΗΜΑ,
                  self.Service_ID, self.Customer_ID, self.Calendar_ID)

    def __str__(self):
        return f"{self.PARTS_NR} {self.ΠΕΡΙΓΡΑΦΗ} {self.ΚΩΔΙΚΟΣ} {self.ΤΕΜΑΧΙΑ} {self.ΠΑΡΑΤΗΡΗΣΗΣ}" \
               f"{self.ΜΗΧΑΝΗΜΑ} {self.Service_ID} {self.Customer_ID}  {self.Calendar_ID}"


class Receiver_emails(service_base):
    __tablename__ = 'Receiver_emails'

    ID = Column(Integer, primary_key=True, autoincrement=True)

    Receiver_email = Column(Text)

    def __repr__(self):
        return "<Receiver_emails(ID='%i', Receiver_email='%s')>" \
               % (self.ID, self.Receiver_email)

    def __str__(self):
        return f"{self.Receiver_email}"


class Sender_emails(service_base):
    __tablename__ = 'Sender_emails'

    ID = Column(Integer, primary_key=True, autoincrement=True)

    sender_email = Column(Text)
    password = Column(Text)
    smtp_server = Column(Text)
    port = Column(Text)

    def __repr__(self):
        return "<Sender_emails(ID='%i', sender_email='%s', password='%s', smtp_server='%s', port='%s')>" \
               % (self.ID, self.sender_email, self.password, self.smtp_server, self.port)

    def __str__(self):
        return f"{self.sender_email} {self.password} {self.smtp_server} {self.port}"


class Service_data(service_base):
    __tablename__ = 'Service_data'

    ID = Column(Integer, primary_key=True, autoincrement=True)

    Ενέργειες = Column(Text)
    Σκοπός = Column(Text)
    Τεχνικός = Column(Text)


    def __repr__(self):
        return "<Service_data(ID='%i', Ενέργειες='%s', Σκοπός='%s', Τεχνικός='%s')>" \
               % (self.ID, self.Ενέργειες, self.Σκοπός, self.Τεχνικός)

    def __str__(self):
        return f"{self.Ενέργειες} {self.Σκοπός} {self.Τεχνικός}"


class Support(service_base):
    __tablename__ = 'Support'

    ID = Column(Integer, primary_key=True, autoincrement=True)

    IsActive = Column(Boolean)
    Activation_date = Column(Text)

    def __repr__(self):
        return "<Support(ID='%i', IsActive='%i', Activation_date='%s')>" \
               % (self.ID, self.IsActive, self.Activation_date)

    def __str__(self):
        return f"{self.IsActive} {self.Activation_date}"


# ---------------------------------------- Συναρτήσεις Service Book ---------------------------
def fetch_active_calendar():
    try:
        data = service_session.query(Calendar).filter(Calendar.Κατάσταση == 1)
        return data
    except Exception:
        traceback.print_exc()
        return


def fetch_completed_calendar(completed_date):
    """
    Αναζήτηση κλησεων που έχουν κλείση στην επιλεγμένη ημερομηνία
    :param completed_date:
    :return items:
    """
    try:

        data = service_session.query(Calendar).filter(Calendar.Κατάσταση == 0).filter(
            Calendar.Ημ_Ολοκλ == completed_date)
        return data
    except Exception:
        traceback.print_exc()
        return


def fetch_active_calendar_on_selected_date(active_date):
    """
    Αναζήτηση κλησεων που δεν έχουν κλείση στην επιλεγμένη ημερομηνία
    :param active_date:
    :return items:
    """
    try:

        data = service_session.query(Calendar).filter(Calendar.Κατάσταση == 1).filter(
            Calendar.Ημερομηνία == active_date)
        return data
    except Exception:
        traceback.print_exc()
        return


def fetch_active_calendar_on_selected_machine(selected_machine_id):
    """
    Αναζήτηση κλησεων που δεν έχουν κλείση στo επιλεγμένο μηχάνημα
    :param selected_machine_id:
    :return obj:
    """
    try:

        data = service_session.query(Calendar).filter(Calendar.Κατάσταση == 1).filter(
            Calendar.Copier_ID == selected_machine_id)
        return data
    except Exception:
        traceback.print_exc()
        return


def fetch_active_customers():
    try:
        data = service_session.query(Customer).filter(Customer.Κατάσταση == 1).order_by \
            (asc(Customer.Επωνυμία_Επιχείρησης))
        return data
    except Exception:
        traceback.print_exc()
        return


def fetch_inactive_customers():
    try:
        data = service_session.query(Customer).filter(Customer.Κατάσταση == 0).order_by(
            asc(Customer.Επωνυμία_Επιχείρησης))
        return data
    except Exception:
        traceback.print_exc()
        return


def fetch_active_machines():
    try:
        data = service_session.query(Machine).filter(Machine.Κατάσταση == 1)
        return data
    except Exception:
        traceback.print_exc()
        return


def fetch_inactive_machines():
    try:
        data = service_session.query(Machine).filter(Machine.Κατάσταση == 0)
        return data
    except Exception:
        traceback.print_exc()
        return


def fetch_transfers_logs():
    try:
        data = service_session.query(Copiers_Log).all()
        return data
    except Exception:
        traceback.print_exc()
        return


def fetch_service_data():
    try:
        data = service_session.query(Service_data).all()
        return data
    except Exception:
        traceback.print_exc()
        return


def fetch_service_reasons():
    try:
        data = service_session.query(Service_data.Σκοπός, Service_data.ID).filter(Service_data.Σκοπός != " ").\
            filter(Service_data.Σκοπός != "").filter(Service_data.Σκοπός is not None).\
            order_by(asc(Service_data.Σκοπός))
        return data
    except Exception:
        traceback.print_exc()
        return


def fetch_service_actions():
    try:
        data = service_session.query(Service_data.Ενέργειες, Service_data.ID).filter(Service_data.Ενέργειες != " ").\
            filter(Service_data.Ενέργειες != "").filter(Service_data.Ενέργειες is not None).\
            order_by(asc(Service_data.Ενέργειες))
        return data
    except Exception:
        traceback.print_exc()
        return


def fetch_service_technicians():
    try:
        data = service_session.query(Service_data.Τεχνικός, Service_data.ID).filter(Service_data.Τεχνικός != " ").\
            filter(Service_data.Τεχνικός != "").filter(Service_data.Τεχνικός is not None).\
            order_by(asc(Service_data.Τεχνικός))
        return data
    except Exception:
        traceback.print_exc()
        return


def fetch_sender_emails_data():
    try:
        data = service_session.query(Sender_emails).all()
        return data
    except Exception:
        traceback.print_exc()
        return


def fetch_receiver_emails_data():
    try:
        data = service_session.query(Receiver_emails).all()
        return data
    except Exception:
        traceback.print_exc()
        return


def fetch_companies_data():
    try:
        data = service_session.query(Companies.Εταιρεία, Companies.ID).filter(Companies.Εταιρεία != "").\
            filter(Companies.Εταιρεία != "").filter(Companies.Εταιρεία is not None).\
            order_by(asc(Companies.Εταιρεία))
        return data
    except Exception:
        traceback.print_exc()
        return


def fetch_companies_katigories_data():
    try:
        data = service_session.query(Companies.Κατηγορία_μηχανήματος, Companies.ID).filter(Companies.Κατηγορία_μηχανήματος != "").\
            filter(Companies.Κατηγορία_μηχανήματος != "").filter(Companies.Κατηγορία_μηχανήματος is not None).\
            order_by(asc(Companies.Κατηγορία_μηχανήματος))
        return data
    except Exception:
        traceback.print_exc()
        return


def get_customer_from_id(customer_id):
    try:
        customer = service_session.query(Customer).get(customer_id)
        return customer
    except Exception:
        traceback.print_exc()
        return


def get_customer_from_name(customer_name):
    try:
        customer = service_session.query(Customer).filter(Customer.Κατάσταση == 1). \
            filter(Customer.Επωνυμία_Επιχείρησης == customer_name)
        return customer
    except Exception:
        traceback.print_exc()
        return


def get_inactive_customer_from_name(customer_name):
    try:
        customer = service_session.query(Customer).filter(Customer.Κατάσταση == 0). \
            filter(Customer.Επωνυμία_Επιχείρησης == customer_name)
        return customer
    except Exception:
        traceback.print_exc()
        return


def get_machines_from_id(machine_id):
    try:
        machine = service_session.query(Machine).get(machine_id)
        return machine
    except Exception:
        traceback.print_exc()
        return


def search_on_customers(text_to_search):
    last_like = f"%{text_to_search}%"  # για να τα κάνει κεφαλαία αν γράψουμε με μικρά
    # στήν βάση είναι ολλα κεφαλαία αρα θελει κεφαλαία για να βρει
    try:
        customers = service_session.query(Customer).filter((Customer.Επωνυμία_Επιχείρησης.ilike(last_like)) |
                                                           (Customer.Τηλέφωνο.ilike(last_like)) |
                                                           (Customer.Φαξ.ilike(last_like)) |
                                                           (Customer.Διεύθυνση.ilike(last_like)) |
                                                           (Customer.Κινητό.ilike(last_like)) |
                                                           (Customer.Ονοματεπώνυμο.ilike(last_like)) |
                                                           (Customer.E_mail.ilike(last_like)) |
                                                           (Customer.Περιοχή.ilike(last_like)) |
                                                           (Customer.Σημειώσεις.ilike(last_like)) |
                                                           (Customer.Ταχ_Κώδικας.ilike(last_like)) |
                                                           (Customer.Πόλη.ilike(last_like))). \
            order_by(asc(Customer.Επωνυμία_Επιχείρησης))
        return customers
    except Exception:
        traceback.print_exc()
        return


def search_on_machines(text_to_search):
    last_like = f"%{text_to_search.upper()}%"  # για να τα κάνει κεφαλαία αν γράψουμε με μικρά
    # στήν βάση είναι ολλα κεφαλαία αρα θελει κεφαλαία για να βρει
    try:
        machines = service_session.query(Machine).filter(Machine.Κατάσταση == 1).filter(
            (Machine.Εταιρεία.ilike(last_like)) |
            (Machine.Serial.ilike(last_like)) |
            (Machine.Σημειώσεις.ilike(last_like))). \
            order_by(asc(Machine.Εταιρεία))

        return machines
    except Exception:
        traceback.print_exc()
        return


def search_on_selected_customer_machines(text_to_search, customer):
    last_like = f"%{text_to_search.upper()}%"  # για να τα κάνει κεφαλαία αν γράψουμε με μικρά
    # στήν βάση είναι ολλα κεφαλαία αρα θελει κεφαλαία για να βρει
    try:
        machines = service_session.query(Machine).filter(Machine.Customer == customer).filter(Machine.Κατάσταση == 1). \
            filter((Machine.Εταιρεία.ilike(last_like)) |
                   (Machine.Serial.ilike(last_like)) |
                   (Machine.Σημειώσεις.ilike(last_like))). \
            order_by(asc(Machine.Εταιρεία))

        return machines
    except Exception:
        traceback.print_exc()
        return


def search_on_calendar(text_to_search):
    last_like = f"%{text_to_search.upper()}%"  # για να τα κάνει κεφαλαία αν γράψουμε με μικρά
    # στήν βάση είναι ολλα κεφαλαία αρα θελει κεφαλαία για να βρει
    try:
        calendar = service_session.query(Calendar).filter(Calendar.Κατάσταση == 1).filter(
            (Calendar.Πελάτης.ilike(last_like)) |
            (Calendar.Σκοπός.ilike(last_like)) |
            (Calendar.Ενέργειες.ilike(last_like)) |
            (Calendar.Τεχνικός.ilike(last_like)) |
            (Calendar.Τηλέφωνο.ilike(last_like)) |
            (Calendar.Σημειώσεις.ilike(last_like)) |
            (Calendar.Μηχάνημα.ilike(last_like)) |
            (Calendar.Price.ilike(last_like)))

        return calendar
    except Exception:
        traceback.print_exc()
        return


def search_on_service(machine_id, text_to_search):
    last_like = f"%{text_to_search.upper()}%"  # για να τα κάνει κεφαλαία αν γράψουμε με μικρά
    # στήν βάση είναι ολλα κεφαλαία αρα θελει κεφαλαία για να βρει
    try:
        service = service_session.query(Service).filter(Service.Copier_ID == machine_id). \
            filter((Service.Σκοπός_Επίσκεψης.ilike(last_like)) |
                   (Service.Ενέργειες.ilike(last_like)) |
                   (Service.Τεχνικός.ilike(last_like)) |
                   (Service.Σημειώσεις.ilike(last_like)) |
                   (Service.Price.ilike(last_like)))

        return service
    except Exception:
        traceback.print_exc()
        return


def search_for_errors_on_service(text_to_search):
    last_like = f"%{text_to_search.upper()}%"  # για να τα κάνει κεφαλαία αν γράψουμε με μικρά
    # στήν βάση είναι ολλα κεφαλαία αρα θελει κεφαλαία για να βρει
    try:
        service = service_session.query(Service).filter((Service.Σκοπός_Επίσκεψης.ilike(last_like)) |
                                                        (Service.Ενέργειες.ilike(last_like)) |
                                                        (Service.Σημειώσεις.ilike(last_like)))

        return service
    except Exception:
        traceback.print_exc()
        return


def search_for_dte_on_tasks(text_to_search):
    last_like = f"%{text_to_search.upper()}%"  # για να τα κάνει κεφαλαία αν γράψουμε με μικρά
    # στήν βάση είναι ολλα κεφαλαία αρα θελει κεφαλαία για να βρει
    try:
        dte = service_session.query(Calendar).filter((Calendar.ΔΤΕ.ilike(last_like)))

        return dte
    except Exception:
        traceback.print_exc()
        return


def search_for_dte_on_service(text_to_search):
    last_like = f"%{text_to_search.upper()}%"  # για να τα κάνει κεφαλαία αν γράψουμε με μικρά
    # στήν βάση είναι ολλα κεφαλαία αρα θελει κεφαλαία για να βρει
    try:
        dte = service_session.query(Service).filter((Service.ΔΤΕ.ilike(last_like)))

        return dte
    except Exception:
        traceback.print_exc()
        return


def search_on_customer_consumables(customer, text_to_search):
    last_like = f"%{text_to_search.upper()}%"  # για να τα κάνει κεφαλαία αν γράψουμε με μικρά
    # στήν βάση είναι ολλα κεφαλαία αρα θελει κεφαλαία για να βρει
    try:
        customer_consumables = service_session.query(Consumables).filter(Consumables.customer == customer). \
            filter((Consumables.ΠΕΡΙΓΡΑΦΗ.ilike(last_like)) | (Consumables.ΚΩΔΙΚΟΣ.ilike(last_like))). \
            order_by(asc(Consumables.ΠΕΡΙΓΡΑΦΗ))

        return customer_consumables
    except Exception:
        traceback.print_exc()
        return


def search_on_copiers_log(text_to_search):
    last_like = f"%{text_to_search}%"  # για να τα κάνει κεφαλαία αν γράψουμε με μικρά
    # στήν βάση είναι ολλα κεφαλαία αρα θελει κεφαλαία για να βρει
    try:
        log = service_session.query(Copiers_Log).filter((Copiers_Log.Μηχάνημα.ilike(last_like)) |
                                                        (Copiers_Log.Ημερομηνία.ilike(last_like)) |
                                                        (Copiers_Log.Προηγούμενος_Πελάτης.ilike(last_like)) |
                                                        (Copiers_Log.Νέος_Πελάτης.ilike(last_like)) |
                                                        (Copiers_Log.Σημειώσεις.ilike(last_like)))
        return log
    except Exception:
        traceback.print_exc()
        return


def check_if_customer_has_active_machines(given_customer):
    # session.query(exists().where(User.email == '...')).scalar()
    exist = service_session.query(exists().where(Machine.Κατάσταση == 1).
                                  where(Machine.Customer == given_customer)).scalar()
    if exist:
        return True
    else:
        return False


def get_machine_from_history(history_id):
    # last_like = f"%{text_to_search.upper()}%"  # για να τα κάνει κεφαλαία αν γράψουμε με μικρά
    # στήν βάση είναι ολλα κεφαλαία αρα θελει κεφαλαία για να βρ
    try:
        service_obj = service_session.query(Service).get(history_id)
        machine = service_session.query(Machine).get(service_obj.Copier_ID)
        return machine
    except Exception:
        traceback.print_exc()
        return


def check_if_customer_name_exist(customer_name):
    # session.query(exists().where(User.email == '...')).scalar()
    exist = service_session.query(exists().where(Customer.Κατάσταση == 1).
                                  where(Customer.Επωνυμία_Επιχείρησης == customer_name)).scalar()
    if exist:
        return True
    else:
        return False


def check_if_customer_name_is_inactive(given_name):
    exist = service_session.query(exists().where(Customer.Κατάσταση == 0).
                                  where(Customer.Επωνυμία_Επιχείρησης == given_name)).scalar()
    if exist:
        return True
    else:
        return False


def check_if_serial_exist(given_serial):
    # session.query(exists().where(User.email == '...')).scalar()
    exist = service_session.query(exists().where(Machine.Serial == given_serial)).scalar()
    if exist:
        return True
    else:
        return False


def get_DTE_from_calendar_id(given_calendar_id):
    try:
        calendar_obj = service_session.query(Calendar).get(int(given_calendar_id))
        calendar_dte = calendar_obj.ΔΤΕ
        return calendar_dte
    except Exception:
        traceback.print_exc()
        return


def get_customers_with_inactive_machines():
    # Μόνο απο ενεργούς πελάτες
    # Δεν μπορούμε να ενεργοποιήσουμε μηχάνημα σε ανενεργο πελάτη
    try:
        customers = fetch_active_customers()
        customers_with_inactive_machines = {}

        for customer in customers:
            for machine in customer.machines:
                if machine.Κατάσταση == 0:
                    try:  # προσθέση το μηχάνημα
                        customers_with_inactive_machines[customer].append(machine)
                    except KeyError:  # αν δεν υπάρχει τότε να κάνει λίστα
                        customers_with_inactive_machines[customer] = []
                        customers_with_inactive_machines[customer].append(machine)
        return customers_with_inactive_machines
    except Exception:
        traceback.print_exc()
        return


def check_if_reason_service_data_exist(given_data):
    exist = service_session.query(exists().where(Service_data.Σκοπός == given_data)).scalar()
    if exist:
        return True
    else:
        return False


def check_if_actions_service_data_exist(given_data):
    exist = service_session.query(exists().where(Service_data.Ενέργειες == given_data)).scalar()
    if exist:
        return True
    else:
        return False


def check_if_technician_service_data_exist(given_data):
    exist = service_session.query(exists().where(Service_data.Τεχνικός == given_data)).scalar()
    if exist:
        return True
    else:
        return False


def check_if_category_exist(given_data):
    exist = service_session.query(exists().where(Companies.Κατηγορία_μηχανήματος == given_data)).scalar()
    if exist:
        return True
    else:
        return False


def check_if_company_exist(given_data):
    exist = service_session.query(exists().where(Companies.Εταιρεία == given_data)).scalar()
    if exist:
        return True
    else:
        return False


def get_calendar_data_from_id(calendar_id):
    try:
        calendar_obj = service_session.query(Calendar).get(int(calendar_id))
        return calendar_obj
    except Exception:
        traceback.print_exc()
        return


def get_calendar_from_service_id(given_service_id):
    try:
        calendar_obj = service_session.query(Calendar).filter(Calendar.Service_ID == given_service_id).scalar()
        return calendar_obj
    except Exception:
        traceback.print_exc()
        return


def get_service_from_id(service_id):
    try:
        service_obj = service_session.query(Service).get(service_id)
        return service_obj
    except Exception:
        traceback.print_exc()
        return


def get_consumables_from_service_id(given_service_id):
    try:
        consumables_obj = service_session.query(Consumables).filter(Consumables.Service_ID == given_service_id).all()
        return consumables_obj
    except Exception:
        traceback.print_exc()
        return


def get_consumable_from_id(given_consumable_id):
    try:
        consumables_obj = service_session.query(Consumables).get(given_consumable_id)
        return consumables_obj
    except Exception:
        traceback.print_exc()
        return


def check_if_consumable_exist_on_service(given_code, given_service_id):
    exist = service_session.query(exists().where(Consumables.ΚΩΔΙΚΟΣ == given_code).where(Consumables.Service_ID == given_service_id)).scalar()
    if exist:
        return True
    else:
        return False


def check_if_support_exist():  # Αν ο πελάτης έχει υποστήριξη
    support_obj = service_session.query(Support).get(1)
    try:
        if support_obj.IsActive:
            last_activation = support_obj.Activation_date
            last_activation_date = datetime.datetime.strptime(last_activation, '%d %m %Y').date()
            today = datetime.datetime.today().date()
            last_day = last_activation_date + datetime.timedelta(days=366)
            remaining_days = last_day - today
            if remaining_days.days > 0:
                return remaining_days.days
            else:
                support_obj.IsActive = 0
                service_session.commit()
        else:
            return False
    except AttributeError:  # Αν δέν έχει IsActive
        return False


# ------------------------------------------ Αποθήκη ------------------------------------------
# Tables
class Brother(store_base):
    __tablename__ = 'BROTHER'

    ID = Column(Integer, primary_key=True, autoincrement=True)

    PARTS_NR = Column(Text)
    ΠΕΡΙΓΡΑΦΗ = Column(Text)
    ΚΩΔΙΚΟΣ = Column(Text)
    ΤΕΜΑΧΙΑ = Column(Text)
    ΠΑΡΑΤΗΡΗΣΗΣ = Column(Text)

    def __repr__(self):
        return "<Brother(id='%i', PARTS_NR='%s', ΠΕΡΙΓΡΑΦΗ='%s', ΚΩΔΙΚΟΣ='%s', ΤΕΜΑΧΙΑ='%s', ΠΑΡΑΤΗΡΗΣΗΣ='%s')>" \
               % (self.ID, self.PARTS_NR, self.ΠΕΡΙΓΡΑΦΗ, self.ΚΩΔΙΚΟΣ, self.ΤΕΜΑΧΙΑ, self.ΠΑΡΑΤΗΡΗΣΗΣ)

    def __str__(self):
        return f"{self.PARTS_NR} {self.ΠΕΡΙΓΡΑΦΗ} {self.ΚΩΔΙΚΟΣ} {self.ΤΕΜΑΧΙΑ} {self.ΠΑΡΑΤΗΡΗΣΗΣ}"


class Canon(store_base):
    __tablename__ = 'CANON'

    ID = Column(Integer, primary_key=True, autoincrement=True)

    PARTS_NR = Column(Text)
    ΠΕΡΙΓΡΑΦΗ = Column(Text)
    ΚΩΔΙΚΟΣ = Column(Text)
    ΤΕΜΑΧΙΑ = Column(Text)
    ΠΑΡΑΤΗΡΗΣΗΣ = Column(Text)

    def __repr__(self):
        return "<Canon(id='%i', PARTS_NR='%s', ΠΕΡΙΓΡΑΦΗ='%s', ΚΩΔΙΚΟΣ='%s', ΤΕΜΑΧΙΑ='%s', ΠΑΡΑΤΗΡΗΣΗΣ='%s')>" \
               % (self.ID, self.PARTS_NR, self.ΠΕΡΙΓΡΑΦΗ, self.ΚΩΔΙΚΟΣ, self.ΤΕΜΑΧΙΑ, self.ΠΑΡΑΤΗΡΗΣΗΣ)

    def __str__(self):
        return f"{self.PARTS_NR} {self.ΠΕΡΙΓΡΑΦΗ} {self.ΚΩΔΙΚΟΣ} {self.ΤΕΜΑΧΙΑ} {self.ΠΑΡΑΤΗΡΗΣΗΣ}"


class Epson(store_base):
    __tablename__ = 'EPSON'

    ID = Column(Integer, primary_key=True, autoincrement=True)

    PARTS_NR = Column(Text)
    ΠΕΡΙΓΡΑΦΗ = Column(Text)
    ΚΩΔΙΚΟΣ = Column(Text)
    ΤΕΜΑΧΙΑ = Column(Text)
    ΠΑΡΑΤΗΡΗΣΗΣ = Column(Text)

    def __repr__(self):
        return "<Epson(id='%i', PARTS_NR='%s', ΠΕΡΙΓΡΑΦΗ='%s', ΚΩΔΙΚΟΣ='%s', ΤΕΜΑΧΙΑ='%s', ΠΑΡΑΤΗΡΗΣΗΣ='%s')>" \
               % (self.ID, self.PARTS_NR, self.ΠΕΡΙΓΡΑΦΗ, self.ΚΩΔΙΚΟΣ, self.ΤΕΜΑΧΙΑ, self.ΠΑΡΑΤΗΡΗΣΗΣ)

    def __str__(self):
        return f"{self.PARTS_NR} {self.ΠΕΡΙΓΡΑΦΗ} {self.ΚΩΔΙΚΟΣ} {self.ΤΕΜΑΧΙΑ} {self.ΠΑΡΑΤΗΡΗΣΗΣ}"


class Konica(store_base):
    __tablename__ = 'KONICA'

    ID = Column(Integer, primary_key=True, autoincrement=True)

    PARTS_NR = Column(Text)
    ΠΕΡΙΓΡΑΦΗ = Column(Text)
    ΚΩΔΙΚΟΣ = Column(Text)
    ΤΕΜΑΧΙΑ = Column(Text)
    ΠΑΡΑΤΗΡΗΣΗΣ = Column(Text)

    def __repr__(self):
        return "<Konica(id='%i', PARTS_NR='%s', ΠΕΡΙΓΡΑΦΗ='%s', ΚΩΔΙΚΟΣ='%s', ΤΕΜΑΧΙΑ='%s', ΠΑΡΑΤΗΡΗΣΗΣ='%s')>" \
               % (self.ID, self.PARTS_NR, self.ΠΕΡΙΓΡΑΦΗ, self.ΚΩΔΙΚΟΣ, self.ΤΕΜΑΧΙΑ, self.ΠΑΡΑΤΗΡΗΣΗΣ)

    def __str__(self):
        return f"{self.PARTS_NR} {self.ΠΕΡΙΓΡΑΦΗ} {self.ΚΩΔΙΚΟΣ} {self.ΤΕΜΑΧΙΑ} {self.ΠΑΡΑΤΗΡΗΣΗΣ}"


class Kyocera(store_base):
    __tablename__ = 'KYOCERA'

    ID = Column(Integer, primary_key=True, autoincrement=True)

    PARTS_NR = Column(Text)
    ΠΕΡΙΓΡΑΦΗ = Column(Text)
    ΚΩΔΙΚΟΣ = Column(Text)
    ΤΕΜΑΧΙΑ = Column(Text)
    ΠΑΡΑΤΗΡΗΣΗΣ = Column(Text)

    def __repr__(self):
        return "<Kyocera(id='%i', PARTS_NR='%s', ΠΕΡΙΓΡΑΦΗ='%s', ΚΩΔΙΚΟΣ='%s', ΤΕΜΑΧΙΑ='%s', ΠΑΡΑΤΗΡΗΣΗΣ='%s')>" \
               % (self.ID, self.PARTS_NR, self.ΠΕΡΙΓΡΑΦΗ, self.ΚΩΔΙΚΟΣ, self.ΤΕΜΑΧΙΑ, self.ΠΑΡΑΤΗΡΗΣΗΣ)

    def __str__(self):
        return f"{self.PARTS_NR} {self.ΠΕΡΙΓΡΑΦΗ} {self.ΚΩΔΙΚΟΣ} {self.ΤΕΜΑΧΙΑ} {self.ΠΑΡΑΤΗΡΗΣΗΣ}"


class Lexmark(store_base):
    __tablename__ = 'LEXMARK'

    ID = Column(Integer, primary_key=True, autoincrement=True)

    PARTS_NR = Column(Text)
    ΠΕΡΙΓΡΑΦΗ = Column(Text)
    ΚΩΔΙΚΟΣ = Column(Text)
    ΤΕΜΑΧΙΑ = Column(Text)
    ΠΑΡΑΤΗΡΗΣΗΣ = Column(Text)

    def __repr__(self):
        return "<Lexmark(id='%i', PARTS_NR='%s', ΠΕΡΙΓΡΑΦΗ='%s', ΚΩΔΙΚΟΣ='%s', ΤΕΜΑΧΙΑ='%s', ΠΑΡΑΤΗΡΗΣΗΣ='%s')>" \
               % (self.ID, self.PARTS_NR, self.ΠΕΡΙΓΡΑΦΗ, self.ΚΩΔΙΚΟΣ, self.ΤΕΜΑΧΙΑ, self.ΠΑΡΑΤΗΡΗΣΗΣ)

    def __str__(self):
        return f"{self.PARTS_NR} {self.ΠΕΡΙΓΡΑΦΗ} {self.ΚΩΔΙΚΟΣ} {self.ΤΕΜΑΧΙΑ} {self.ΠΑΡΑΤΗΡΗΣΗΣ}"


class Oki(store_base):
    __tablename__ = 'OKI'

    ID = Column(Integer, primary_key=True, autoincrement=True)

    PARTS_NR = Column(Text)
    ΠΕΡΙΓΡΑΦΗ = Column(Text)
    ΚΩΔΙΚΟΣ = Column(Text)
    ΤΕΜΑΧΙΑ = Column(Text)
    ΠΑΡΑΤΗΡΗΣΗΣ = Column(Text)

    def __repr__(self):
        return "<Oki(id='%i', PARTS_NR='%s', ΠΕΡΙΓΡΑΦΗ='%s', ΚΩΔΙΚΟΣ='%s', ΤΕΜΑΧΙΑ='%s', ΠΑΡΑΤΗΡΗΣΗΣ='%s')>" \
               % (self.ID, self.PARTS_NR, self.ΠΕΡΙΓΡΑΦΗ, self.ΚΩΔΙΚΟΣ, self.ΤΕΜΑΧΙΑ, self.ΠΑΡΑΤΗΡΗΣΗΣ)

    def __str__(self):
        return f"{self.PARTS_NR} {self.ΠΕΡΙΓΡΑΦΗ} {self.ΚΩΔΙΚΟΣ} {self.ΤΕΜΑΧΙΑ} {self.ΠΑΡΑΤΗΡΗΣΗΣ}"


class Ricoh(store_base):
    __tablename__ = 'RICOH'

    ID = Column(Integer, primary_key=True, autoincrement=True)

    PARTS_NR = Column(Text)
    ΠΕΡΙΓΡΑΦΗ = Column(Text)
    ΚΩΔΙΚΟΣ = Column(Text)
    ΤΕΜΑΧΙΑ = Column(Text)
    ΠΑΡΑΤΗΡΗΣΗΣ = Column(Text)

    def __repr__(self):
        return "<Ricoh(id='%i', PARTS_NR='%s', ΠΕΡΙΓΡΑΦΗ='%s', ΚΩΔΙΚΟΣ='%s', ΤΕΜΑΧΙΑ='%s', ΠΑΡΑΤΗΡΗΣΗΣ='%s')>" \
               % (self.ID, self.PARTS_NR, self.ΠΕΡΙΓΡΑΦΗ, self.ΚΩΔΙΚΟΣ, self.ΤΕΜΑΧΙΑ, self.ΠΑΡΑΤΗΡΗΣΗΣ)

    def __str__(self):
        return f"{self.PARTS_NR} {self.ΠΕΡΙΓΡΑΦΗ} {self.ΚΩΔΙΚΟΣ} {self.ΤΕΜΑΧΙΑ} {self.ΠΑΡΑΤΗΡΗΣΗΣ}"


class Samsung(store_base):
    __tablename__ = 'SAMSUNG'

    ID = Column(Integer, primary_key=True, autoincrement=True)

    PARTS_NR = Column(Text)
    ΠΕΡΙΓΡΑΦΗ = Column(Text)
    ΚΩΔΙΚΟΣ = Column(Text)
    ΤΕΜΑΧΙΑ = Column(Text)
    ΠΑΡΑΤΗΡΗΣΗΣ = Column(Text)

    def __repr__(self):
        return "<Samsung(id='%i', PARTS_NR='%s', ΠΕΡΙΓΡΑΦΗ='%s', ΚΩΔΙΚΟΣ='%s', ΤΕΜΑΧΙΑ='%s', ΠΑΡΑΤΗΡΗΣΗΣ='%s')>" \
               % (self.ID, self.PARTS_NR, self.ΠΕΡΙΓΡΑΦΗ, self.ΚΩΔΙΚΟΣ, self.ΤΕΜΑΧΙΑ, self.ΠΑΡΑΤΗΡΗΣΗΣ)

    def __str__(self):
        return f"{self.PARTS_NR} {self.ΠΕΡΙΓΡΑΦΗ} {self.ΚΩΔΙΚΟΣ} {self.ΤΕΜΑΧΙΑ} {self.ΠΑΡΑΤΗΡΗΣΗΣ}"


class Sharp(store_base):
    __tablename__ = 'SHARP'

    ID = Column(Integer, primary_key=True, autoincrement=True)

    PARTS_NR = Column(Text)
    ΠΕΡΙΓΡΑΦΗ = Column(Text)
    ΚΩΔΙΚΟΣ = Column(Text)
    ΤΕΜΑΧΙΑ = Column(Text)
    ΠΑΡΑΤΗΡΗΣΗΣ = Column(Text)

    def __repr__(self):
        return "<Sharp(id='%i', PARTS_NR='%s', ΠΕΡΙΓΡΑΦΗ='%s', ΚΩΔΙΚΟΣ='%s', ΤΕΜΑΧΙΑ='%s', ΠΑΡΑΤΗΡΗΣΗΣ='%s')>" \
               % (self.ID, self.PARTS_NR, self.ΠΕΡΙΓΡΑΦΗ, self.ΚΩΔΙΚΟΣ, self.ΤΕΜΑΧΙΑ, self.ΠΑΡΑΤΗΡΗΣΗΣ)

    def __str__(self):
        return f"{self.PARTS_NR} {self.ΠΕΡΙΓΡΑΦΗ} {self.ΚΩΔΙΚΟΣ} {self.ΤΕΜΑΧΙΑ} {self.ΠΑΡΑΤΗΡΗΣΗΣ}"


class Melanakia(store_base):
    __tablename__ = 'ΜΕΛΑΝΑΚΙΑ'

    ID = Column(Integer, primary_key=True, autoincrement=True)

    ΕΤΑΙΡΕΙΑ = Column(Text)
    ΠΟΙΟΤΗΤΑ = Column(Text)
    ΑΝΑΛΩΣΙΜΟ = Column(Text)
    ΠΕΡΙΓΡΑΦΗ = Column(Text)
    ΚΩΔΙΚΟΣ = Column(Text)
    ΤΕΜΑΧΙΑ = Column(Text)
    ΤΙΜΗ = Column(Text)
    ΣΥΝΟΛΟ = Column(Text)
    ΣΕΛΙΔΕΣ = Column(Text)
    ΠΕΛΑΤΕΣ = Column(Text)
    ΠΑΡΑΤΗΡΗΣΗΣ = Column(Text)

    def __repr__(self):
        return "<Melanakia(id='%i', ΕΤΑΙΡΕΙΑ='%s', ΠΟΙΟΤΗΤΑ='%s', ΑΝΑΛΩΣΙΜΟ='%s', ΠΕΡΙΓΡΑΦΗ='%s', ΚΩΔΙΚΟΣ='%s' " \
               "ΤΕΜΑΧΙΑ='%s', ΤΙΜΗ='%s', ΣΥΝΟΛΟ='%s', ΣΕΛΙΔΕΣ='%s', ΠΕΛΑΤΕΣ='%s', ΠΑΡΑΤΗΡΗΣΗΣ='%s')>" \
               % (self.ID, self.ΕΤΑΙΡΕΙΑ, self.ΠΟΙΟΤΗΤΑ, self.ΑΝΑΛΩΣΙΜΟ, self.ΠΕΡΙΓΡΑΦΗ, self.ΚΩΔΙΚΟΣ, self.ΤΕΜΑΧΙΑ,
                  self.ΤΙΜΗ, self.ΣΥΝΟΛΟ, self.ΣΕΛΙΔΕΣ, self.ΠΕΛΑΤΕΣ, self.ΠΑΡΑΤΗΡΗΣΗΣ)

    def __str__(self):
        return f"{self.ΕΤΑΙΡΕΙΑ} {self.ΠΟΙΟΤΗΤΑ} {self.ΑΝΑΛΩΣΙΜΟ} {self.ΠΕΡΙΓΡΑΦΗ} {self.ΚΩΔΙΚΟΣ} {self.ΤΕΜΑΧΙΑ} " \
               f"{self.ΤΙΜΗ} {self.ΣΥΝΟΛΟ} {self.ΣΕΛΙΔΕΣ} {self.ΠΕΛΑΤΕΣ} {self.ΠΑΡΑΤΗΡΗΣΗΣ}"


class Melanotainies(store_base):
    __tablename__ = 'ΜΕΛΑΝΟΤΑΙΝΙΕΣ'

    ID = Column(Integer, primary_key=True, autoincrement=True)

    ΕΤΑΙΡΕΙΑ = Column(Text)
    ΠΟΙΟΤΗΤΑ = Column(Text)
    ΑΝΑΛΩΣΙΜΟ = Column(Text)
    ΠΕΡΙΓΡΑΦΗ = Column(Text)
    ΚΩΔΙΚΟΣ = Column(Text)
    ΤΕΜΑΧΙΑ = Column(Text)
    ΤΙΜΗ = Column(Text)
    ΣΥΝΟΛΟ = Column(Text)
    ΠΕΛΑΤΕΣ = Column(Text)
    ΠΑΡΑΤΗΡΗΣΗΣ = Column(Text)

    def __repr__(self):
        return "<Melanotainies(id='%i', ΕΤΑΙΡΕΙΑ='%s', ΠΟΙΟΤΗΤΑ='%s', ΑΝΑΛΩΣΙΜΟ='%s', ΠΕΡΙΓΡΑΦΗ='%s', ΚΩΔΙΚΟΣ='%s' " \
               "ΤΕΜΑΧΙΑ='%s', ΤΙΜΗ='%s', ΣΥΝΟΛΟ='%s', ΠΕΛΑΤΕΣ='%s', ΠΑΡΑΤΗΡΗΣΗΣ='%s')>" \
               % (self.ID, self.ΕΤΑΙΡΕΙΑ, self.ΠΟΙΟΤΗΤΑ, self.ΑΝΑΛΩΣΙΜΟ, self.ΠΕΡΙΓΡΑΦΗ, self.ΚΩΔΙΚΟΣ, self.ΤΕΜΑΧΙΑ,
                  self.ΤΙΜΗ, self.ΣΥΝΟΛΟ, self.ΠΕΛΑΤΕΣ, self.ΠΑΡΑΤΗΡΗΣΗΣ)

    def __str__(self):
        return f"{self.ΕΤΑΙΡΕΙΑ} {self.ΠΟΙΟΤΗΤΑ} {self.ΑΝΑΛΩΣΙΜΟ} {self.ΠΕΡΙΓΡΑΦΗ} {self.ΚΩΔΙΚΟΣ} {self.ΤΕΜΑΧΙΑ} " \
               f"{self.ΤΙΜΗ} {self.ΣΥΝΟΛΟ}  {self.ΠΕΛΑΤΕΣ} {self.ΠΑΡΑΤΗΡΗΣΗΣ}"


class Toner(store_base):
    __tablename__ = 'ΤΟΝΕΡ'

    ID = Column(Integer, primary_key=True, autoincrement=True)

    ΕΤΑΙΡΕΙΑ = Column(Text)
    ΠΟΙΟΤΗΤΑ = Column(Text)
    ΑΝΑΛΩΣΙΜΟ = Column(Text)
    ΠΕΡΙΓΡΑΦΗ = Column(Text)
    ΚΩΔΙΚΟΣ = Column(Text)
    ΤΕΜΑΧΙΑ = Column(Text)
    ΤΙΜΗ = Column(Text)
    ΣΥΝΟΛΟ = Column(Text)
    ΣΕΛΙΔΕΣ = Column(Text)
    ΠΕΛΑΤΕΣ = Column(Text)
    ΠΑΡΑΤΗΡΗΣΗΣ = Column(Text)

    def __repr__(self):
        return "<Toner(id='%i', ΕΤΑΙΡΕΙΑ='%s', ΠΟΙΟΤΗΤΑ='%s', ΑΝΑΛΩΣΙΜΟ='%s', ΠΕΡΙΓΡΑΦΗ='%s', ΚΩΔΙΚΟΣ='%s' " \
               "ΤΕΜΑΧΙΑ='%s', ΤΙΜΗ='%s', ΣΥΝΟΛΟ='%s', ΣΕΛΙΔΕΣ='%s', ΠΕΛΑΤΕΣ='%s', ΠΑΡΑΤΗΡΗΣΗΣ='%s')>" \
               % (self.ID, self.ΕΤΑΙΡΕΙΑ, self.ΠΟΙΟΤΗΤΑ, self.ΑΝΑΛΩΣΙΜΟ, self.ΠΕΡΙΓΡΑΦΗ, self.ΚΩΔΙΚΟΣ, self.ΤΕΜΑΧΙΑ,
                  self.ΤΙΜΗ, self.ΣΥΝΟΛΟ, self.ΣΕΛΙΔΕΣ, self.ΠΕΛΑΤΕΣ, self.ΠΑΡΑΤΗΡΗΣΗΣ)

    def __str__(self):
        return f"{self.ΕΤΑΙΡΕΙΑ} {self.ΠΟΙΟΤΗΤΑ} {self.ΑΝΑΛΩΣΙΜΟ} {self.ΠΕΡΙΓΡΑΦΗ} {self.ΚΩΔΙΚΟΣ} {self.ΤΕΜΑΧΙΑ} " \
               f"{self.ΤΙΜΗ} {self.ΣΥΝΟΛΟ} {self.ΣΕΛΙΔΕΣ} {self.ΠΕΛΑΤΕΣ} {self.ΠΑΡΑΤΗΡΗΣΗΣ}"


class Copiers(store_base):
    __tablename__ = 'ΦΩΤΟΤΥΠΙΚΑ'

    ID = Column(Integer, primary_key=True, autoincrement=True)

    ΕΤΑΙΡΕΙΑ = Column(Text)
    ΠΟΙΟΤΗΤΑ = Column(Text)
    ΑΝΑΛΩΣΙΜΟ = Column(Text)
    ΠΕΡΙΓΡΑΦΗ = Column(Text)
    ΚΩΔΙΚΟΣ = Column(Text)
    ΤΕΜΑΧΙΑ = Column(Text)
    ΤΙΜΗ = Column(Text)
    ΣΥΝΟΛΟ = Column(Text)
    ΣΕΛΙΔΕΣ = Column(Text)
    ΠΕΛΑΤΕΣ = Column(Text)
    ΠΑΡΑΤΗΡΗΣΗΣ = Column(Text)

    def __repr__(self):
        return "<Copiers(id='%i', ΕΤΑΙΡΕΙΑ='%s', ΠΟΙΟΤΗΤΑ='%s', ΑΝΑΛΩΣΙΜΟ='%s', ΠΕΡΙΓΡΑΦΗ='%s', ΚΩΔΙΚΟΣ='%s' " \
               "ΤΕΜΑΧΙΑ='%s', ΤΙΜΗ='%s', ΣΥΝΟΛΟ='%s', ΣΕΛΙΔΕΣ='%s', ΠΕΛΑΤΕΣ='%s', ΠΑΡΑΤΗΡΗΣΗΣ='%s')>" \
               % (self.ID, self.ΕΤΑΙΡΕΙΑ, self.ΠΟΙΟΤΗΤΑ, self.ΑΝΑΛΩΣΙΜΟ, self.ΠΕΡΙΓΡΑΦΗ, self.ΚΩΔΙΚΟΣ, self.ΤΕΜΑΧΙΑ,
                  self.ΤΙΜΗ, self.ΣΥΝΟΛΟ, self.ΣΕΛΙΔΕΣ, self.ΠΕΛΑΤΕΣ, self.ΠΑΡΑΤΗΡΗΣΗΣ)

    def __str__(self):
        return f"{self.ΕΤΑΙΡΕΙΑ} {self.ΠΟΙΟΤΗΤΑ} {self.ΑΝΑΛΩΣΙΜΟ} {self.ΠΕΡΙΓΡΑΦΗ} {self.ΚΩΔΙΚΟΣ} {self.ΤΕΜΑΧΙΑ} " \
               f"{self.ΤΙΜΗ} {self.ΣΥΝΟΛΟ} {self.ΣΕΛΙΔΕΣ} {self.ΠΕΛΑΤΕΣ} {self.ΠΑΡΑΤΗΡΗΣΗΣ}"


class Orders(store_base):
    __tablename__ = 'ΧΧΧ'

    ID = Column(Integer, primary_key=True, autoincrement=True)

    ΚΩΔΙΚΟΣ = Column(Text)
    ΗΜΕΡΟΜΗΝΙΑ = Column(Text)
    ΠΕΡΙΓΡΑΦΗ = Column(Text)
    ΑΠΟΤΕΛΕΣΜΑ = Column(Text)
    ΠΑΡΑΤΗΡΗΣΕΙΣ = Column(Text)
    images = Column(Text)

    # image = Column(Text)

    def __repr__(self):
        return "<Orders(id='%i', ΚΩΔΙΚΟΣ='%s', ΗΜΕΡΟΜΗΝΙΑ='%s', ΠΕΡΙΓΡΑΦΗ='%s', ΑΠΟΤΕΛΕΣΜΑ='%s', ΠΑΡΑΤΗΡΗΣΕΙΣ='%s'\
        images='%s')>" \
               % (
                   self.ID, self.ΚΩΔΙΚΟΣ, self.ΗΜΕΡΟΜΗΝΙΑ, self.ΠΕΡΙΓΡΑΦΗ, self.ΑΠΟΤΕΛΕΣΜΑ, self.ΠΑΡΑΤΗΡΗΣΕΙΣ,
                   self.images)

    def __str__(self):
        return f"{self.ΚΩΔΙΚΟΣ} {self.ΗΜΕΡΟΜΗΝΙΑ} {self.ΠΕΡΙΓΡΑΦΗ} {self.ΑΠΟΤΕΛΕΣΜΑ} {self.ΠΑΡΑΤΗΡΗΣΕΙΣ} {self.images}"


# ------------------------------------------ Συναρτήσεις αποθήκης -------------------------------------


def get_spare_parts(table):
    try:
        data = store_session.query(table).all()
        return data
    except Exception:
        traceback.print_exc()
        return


def search_on_spare_parts(table, text_to_search):
    last_like = f"%{text_to_search.upper()}%"  # για να τα κάνει κεφαλαία αν γράψουμε με μικρά
    # στήν βάση είναι ολλα κεφαλαία αρα θελει κεφαλαία για να βρει
    try:
        parts = store_session.query(table).filter((table.PARTS_NR.ilike(last_like)) |
                                                  (table.ΠΕΡΙΓΡΑΦΗ.ilike(last_like)) |
                                                  (table.ΚΩΔΙΚΟΣ.ilike(last_like))). \
            order_by(asc(table.ΠΕΡΙΓΡΑΦΗ))

        return parts
    except Exception:
        traceback.print_exc()
        return


def search_on_consumables(table, text_to_search):
    last_like = f"%{text_to_search.upper()}%"  # για να τα κάνει κεφαλαία αν γράψουμε με μικρά
    # στήν βάση είναι ολλα κεφαλαία αρα θελει κεφαλαία για να βρει
    try:
        parts = store_session.query(table).filter((table.ΠΕΡΙΓΡΑΦΗ.ilike(last_like)) |
                                                  (table.ΚΩΔΙΚΟΣ.ilike(last_like))). \
            order_by(asc(table.ΠΕΡΙΓΡΑΦΗ))

        return parts
    except Exception:
        traceback.print_exc()
        return


def get_selected_spare_part_from_code(table, given_code):
    try:
        spare_part_obj = store_session.query(table).filter(table.ΚΩΔΙΚΟΣ == given_code).scalar()
        return spare_part_obj
    except Exception:
        print("----------------- file  ------------", __name__)
        print("------------------ERROR ----------  get_selected_spare_part_from_code  line 1199  ------------")
        print("given_code", given_code)
        traceback.print_exc()
        return


def get_spare_part_from_code_from_all_db(given_code):
    all_tables = [Brother, Canon, Epson, Konica, Kyocera, Lexmark, Oki, Ricoh, Samsung, Sharp, Melanakia, Melanotainies,
                  Toner, Copiers]
    for table in all_tables:
        try:
            spare_part_obj = store_session.query(table).filter(table.ΚΩΔΙΚΟΣ == given_code).scalar()
            if spare_part_obj:
                return spare_part_obj
        except Exception:
            traceback.print_exc()
            return