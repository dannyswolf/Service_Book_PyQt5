#  -*- coding: utf-8 -*-
import datetime
import getpass
import logging
import os
import sys

VERSION = "Demo V 1.0.3"
today = datetime.datetime.today().strftime("%d %m %Y")
user = getpass.getuser()

spare_parts_db = "ΑΠΟΘΗΚΗ.db"  # Local Dbase
dbase = "Service_book.db"  # Local Dbase

DB = os.path.dirname(os.path.realpath(dbase))  # Service_book.db
BASE_DIR = os.path.dirname(os.path.abspath(dbase))  # Service_book.db
STORE_DIR = os.path.dirname(os.path.abspath(spare_parts_db))  # 3. ΚΑΙΝΟΥΡΙΑ_ΑΠΟΘΗΚΗ.db

STORE_SPARE_PARTS_ROOT = os.path.join(STORE_DIR, "SpareParts_images/")
SPARE_PARTS_ROOT = os.path.join(BASE_DIR, f"Service_images/")


# -------------ΔΗΜΗΟΥΡΓΕΙΑ LOG FILE και Ημερομηνία ------------------

log_dir = "logs" + "/" + today + "/"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)
else:
    pass

log_file_name = "Service Book " + today + ".log"
log_file = os.path.join(log_dir, log_file_name)

# log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)  # or whatever
handler = logging.FileHandler(log_file, 'a', 'utf-8')  # or whatever
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')  # or whatever
handler.setFormatter(formatter)  # Pass handler as a parameter, not assign
root_logger.addHandler(handler)
sys.stderr.write = root_logger.error
sys.stdout.write = root_logger.info

