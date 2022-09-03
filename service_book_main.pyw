# -*- coding: utf-8 -*-
# Created by: PyQt5 UI code generator 5.15.4
#

"""  -------------------------------------- Notes---------------------------------------------------
"V 1.0.7"  03/09/2022   -- Αφαίρεση "self.technician_lineEdit.setText("Ιορδάνης")"

"V 1.0.6"  24/08/2022   -- Fix Προσθήκη Ημερομηνία λήξης κλήσης

"V 1.0.5"  09/07/2022   -- Προσθήκη Ημερομηνία λήξης κλήσης
                        -- Προσθήκη ανοιγμα αρχείων εγγύησης, περιφέριας και δήμου

"V 1.0.4"  28/06/2022   -- Δεν εκτύπωνε τις κλήσεις σε pdf
                        -- downgrade xhtml2pdf==0.2.5 + reportlab==3.6.5

"V 1.0.3"  26/06/2022   -- Διόρθωση επανάληψης εμφάνισης μηχανημάτων πελάτη
                        -- history_clicked() line 1984

"V 1.0.2"  20/05/2022   -- Δεν αλλάζει ημερομηνία όταν επεξεργαζόμαστε την κλήση
                        -- εμφάνιση ποιο αρχείο βλέπουμε στο view_files_window
                        -- Δυο παράθυρα επεξεργασίας κλήσης και συντήρησης ταυτόχρονα

TODO  *************************** ΠΡΟΒΛΗΜΑ  ***************************
--- Αν βάλουμε προιόν όταν προσθέτουμε συντήρηση απο το κουμπί προσθήκη συντρηρησης
--- τότε αυτόματα αποθηκέυεται η συντήρηση ακόμα και αν διαγραψουμε τα ανταλλακτικα
--- να κάνω το παράθυρο να μην κλήνει δεν είναι καλή ιδέα


todo ανάλυση συναρτίσεων
            todo στον πίνακα Service_data να βάλω πεδίο Τεχνικός -------------------- done
            todo στον πίνακα Companies να αλλάξω το πεδίο Μοντέλο σε  Κατηγορία_μηχανήματος -------------------- done
            todo Νέος Πίνακας Support με πεδία ID, IsActive, (INTEGER) και Activation_date (TEXT) -------------- done
            todo προβολή κουμπή ανοιχτής κλήσης στο ιστορικό μηχανήματος -  27/11/2021
            todo νεο παράθυρο αποστολής email   --------------------------  25/11/2021
            todo νεο παράθυρο ενεργοποιήσης υποστήριξης  -----------------  22/11/2021
            todo νέα παράθυρο επεξεργασίας αποθήκης ----------------------  22/11/2021
            todo Σημειώσεις απο τα ανταλλακτικά δεν φένονται πουθενά -----  22/11/2021
            todo επεξεργασία ανταλλακτών στην λίστα ανταλλακτικών --------  22/11/2021
            todo να αλλάξω θέση στο κουμπί διαγραφή ----------------------  22/11/2021
            todo νέο παράθυρο εισαγωγής συντήρησης -----------------------  21/11/2021
            todo προσθήκη Κατηγορία_μηχανήματος --------------------------  20/11/2021
            todo προσθήκη τεχνικός σαν combobox --------------------------  20/11/2021
            todo edit email και service data  ----------------------------  19/11/2021
            todo edit task επεξεργασία εργασίας --------------------------  18/11/2021
            todo νεο παράθυρο μεταφοράς μηχανήματος  ---------------------  15/11/2021
            TODO προσθήκη εργασίας ---------------------------------------  14/11/2021
            todo μεταφορά μηχανήματος σε νέο πελάτη ----------------------  12/11/2021
            todo προβολή ιστορικό μεταφορών μηχανήματος ------------------  10/11/2021
            todo ενεργοποιήση μηχανήματος --------------------------------  09/11/2021
            todo ενεργοποιήση πελάτη    ----------------------------------  09/11/2021
            todo προσθήκη μηχανήματος  -----------------------------------  08/11/2021
            todo προσθήκη νέου πελάτη  -----------------------------------  07/11/2021
            todo search στην συντήρηση και errors  -----------------------  07/11/2021
            todo short by date στο tasks και παντου ----------------------  05/11/2021

# -----------------------------------------------------------------------------------------------
"""
# ******************************************Pyinstaller Imports******************************************
from reportlab import Version as __RL_Version__
from reportlab.graphics.barcode import ecc200datamatrix
from reportlab.graphics.barcode.common import *
from reportlab.graphics.barcode.code39 import *
from reportlab.graphics.barcode.code93 import *
from reportlab.graphics.barcode.code128 import *
from reportlab.graphics.barcode.usps import *
from reportlab.graphics.barcode.usps4s import USPS_4State
from reportlab.graphics.barcode.qr import QrCodeWidget
from reportlab.platypus import Spacer, SimpleDocTemplate, Table, TableStyle, Preformatted, PageBreak
from reportlab.lib.units import inch, cm
from reportlab.lib import colors
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus.paragraph import Paragraph
from reportlab.platypus.frames import Frame
from reportlab.platypus.flowables import XBox, KeepTogether
from reportlab.graphics.shapes import Drawing, Rect, Line
from reportlab.graphics.barcode import getCodes, getCodeNames, createBarcodeDrawing, createBarcodeImageInMemory
from reportlab.pdfbase import _fontdata_enc_winansi
from reportlab.pdfbase import _fontdata_enc_macroman
import babel.numbers

import time
import os
import pathlib  # Για backup
import re
import shutil  # Για backup
import sys
import traceback

import pandas as pd  # To excel
from PyQt5 import QtCore, QtGui, QtWidgets
from sqlalchemy import select  # To excel

from db import (fetch_active_customers, fetch_completed_calendar, fetch_active_calendar,
                fetch_active_machines, get_customer_from_id, get_machines_from_id, fetch_active_calendar_on_selected_machine,
                search_on_customers, search_on_machines, search_on_selected_customer_machines, search_on_calendar,
                search_for_dte_on_tasks, search_for_dte_on_service, fetch_active_calendar_on_selected_date,
                get_spare_parts, Brother, Canon, Epson, Konica, Kyocera, Lexmark, Oki, Ricoh, Samsung, Sharp,
                Melanakia, Melanotainies, Toner, Copiers, get_consumable_from_id, check_if_support_exist,
                search_on_spare_parts, search_on_consumables, search_on_customer_consumables, store_conn,
                service_session, check_if_customer_has_active_machines, get_machine_from_history, search_on_service,
                search_for_errors_on_service, get_DTE_from_calendar_id, get_calendar_from_service_id, get_service_from_id)

from settings import VERSION, root_logger, dbase, spare_parts_db, today
from add_new_customer_window import Ui_add_new_customer_window
from add_new_machine_window import Ui_add_new_machine_window
from enable_customer_window import Ui_enable_customer_window
from enable_machine_window import Ui_enable_machine_window
from transport_machine_window import Ui_Transport_Machine_Window
from transfers_logs_window import Ui_transfers_logs_window
from add_task_window import Ui_Add_Task_Window
from edit_task_window import Ui_Edit_Task_Window
from edit_email_settings_window import Ui_Edit_Email_Settings_Window
from edit_service_data_window import Ui_Edit_Service_Data_Window
from edit_service_window import Ui_Edit_Service_Window
from add_service_window import Ui_Add_Service_Window
from activation import Ui_Activation_Window
from edit_malanotainies_window import Ui_edit_melanotainies_window
from edit_spare_part_window import Ui_edit_spare_parts_window
from edit_consumables_window import Ui_edit_consumables_window

sys.stderr.write = root_logger.error
sys.stdout.write = root_logger.info

store_tables = [Brother, Canon, Epson, Konica, Kyocera, Lexmark, Oki, Ricoh, Samsung, Sharp, Melanakia, Melanotainies,
                Toner, Copiers]


# Κανουμε sub class το QTreeWidgetItem για να κανει sort τους αριθμους που ειναι σε string μορφη
class TreeWidgetItem(QtWidgets.QTreeWidgetItem):
    def __lt__(self, other):
        column = self.treeWidget().sortColumn()
        key1 = self.text(column)
        key2 = other.text(column)
        return self.natural_sort_key(key1) < self.natural_sort_key(key2)

    @staticmethod
    def natural_sort_key(key):
        regex = '(\d*\.\d+|\d+)'
        parts = re.split(regex, key)
        return tuple((e if i % 2 == 0 else float(e)) for i, e in enumerate(parts))


# Backup Αποθήκη
def backup_store(*args):
    filename = os.path.basename(spare_parts_db)
    file_without_extension = os.path.splitext(filename)
    extension = pathlib.Path(filename).suffix
    today_str = today.replace(' ', '-')
    try:
        #  file_to_save == ('/home/dannys/Desktop/add_files.png', '')
        file_to_save = QtWidgets.QFileDialog.getSaveFileName(None, 'Αποθήκευση αρχείου',
                                                             f'{file_without_extension[0]}'
                                                             + '_backup_' + f"{today_str}" + f'{extension}')

        if file_to_save[0] == "":  # file_to_save == ('', '') αν πατήση ακυρο ο χρήστης
            return

        shutil.copy(os.path.abspath(spare_parts_db), file_to_save[0], follow_symlinks=False)
        QtWidgets.QMessageBox.information(None, "Επιτυχία", f'Το αρχείο {file_to_save[0]} αποθηκεύτηκε '
                                                            f'επιτυχώς')
    except TypeError:  # Αν δεν πατησει αποθήκευση
        return


def backup_service_book():
    filename = os.path.basename(dbase)
    file_without_extension = os.path.splitext(filename)
    extension = pathlib.Path(filename).suffix
    today_str = today.replace(' ', '-')
    try:
        #  file_to_save == ('/home/dannys/Desktop/add_files.png', '')
        file_to_save = QtWidgets.QFileDialog.getSaveFileName(None, 'Αποθήκευση αρχείου',
                                                             f'{file_without_extension[0]}'
                                                             + '_backup_' + f"{today_str}" + f'{extension}')

        if file_to_save[0] == "":  # file_to_save == ('', '') αν πατήση ακυρο ο χρήστης
            return

        shutil.copy(os.path.abspath(spare_parts_db), file_to_save[0], follow_symlinks=False)
        QtWidgets.QMessageBox.information(None, "Επιτυχία", f'Το αρχείο {file_to_save[0]} αποθηκεύτηκε '
                                                            f'επιτυχώς')
    except TypeError:  # Αν δεν πατησει αποθήκευση
        return


def to_excel():
    needed_tables = [Brother, Canon, Epson, Konica, Kyocera, Lexmark, Oki, Ricoh, Samsung, Sharp, Melanakia,
                     Melanotainies, Toner, Copiers]
    data_frames = []

    filename = os.path.basename(spare_parts_db)
    file_without_extension = os.path.splitext(filename)
    today_str = today.replace(' ', '-')
    # try:
    #  file_to_save == ('/home/dannys/Desktop/add_files.png', '')
    file_to_save = QtWidgets.QFileDialog.getSaveFileName(None, 'Αποθήκευση αρχείου',
                                                         f'{file_without_extension[0]}'
                                                         + f"_{today_str}" + '.xlsx')
    if file_to_save[0] == "":  # file_to_save == ('', '') αν πατήση ακυρο ο χρήστης
        return
    # Create a Pandas Excel writer using XlsxWriter as the engine.
    writer = pd.ExcelWriter(file_to_save[0], engine="xlsxwriter")
    for table in needed_tables:
        df_query = select([table])
        df_data = pd.read_sql(df_query, con=store_conn)
        df_data.to_excel(writer, sheet_name=table.__tablename__, index=False)
    writer.save()
    QtWidgets.QMessageBox.information(None, "Επιτυχία", f'Το αρχεία {file_to_save[0]} αποθηκεύτηκε '
                                                        f'επιτυχώς')

    os.startfile(file_to_save[0])


class Ui_MainWindow(object):
    def __init__(self, *args, **kwargs):
        super(Ui_MainWindow, self).__init__(*args, **kwargs)
        self.edit_task_window = None
        self.second_edit_task_window = None
        self.edit_service_window = None
        self.second_edit_service_window = None
        self.active_customers = None
        self.active_machines = None
        self.active_tasks = None
        self.selected_customer = None
        self.new_customer = None
        self.selected_customer_treewidget_item = None
        self.selected_machine = None
        self.selected_machine_open_tasks = None
        self.selected_machine_treewidget_item = None
        self.selected_customer_machines = None
        self.customer_item_from_selected_machine = None
        self.selected_table = None
        self.customers_completer = None
        self.machine_completer = None
        self.tasks_completer = None
        self.show_add_new_customer = None
        self.remaining_support_days = check_if_support_exist()
        if self.remaining_support_days <= 10:
            if self.remaining_support_days is False:
                pass
            else:
                QtWidgets.QMessageBox.information(None, "Πληροφορία", f"Η υποστήριξη σάς θα λήξει σε "
                                                                  f"{self.remaining_support_days} μέρες")

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        # MainWindow.setStyleSheet("Background-color: #aaaa7f")
        self.screen = MainWindow.screen()
        self.size = self.screen.size()
        # print('Size: %d x %d' % (self.size.width(), self.size.height()))
        MainWindow.resize(1500, self.size.height() - 100)
        self.main_window_icon = QtGui.QIcon()
        self.main_window_icon.addPixmap(QtGui.QPixmap("icons/icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(self.main_window_icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_3.setObjectName("gridLayout_3")

        # -----------------------------ICONS-------------------------------
        self.search_icon = QtGui.QIcon()
        self.search_icon.addPixmap(QtGui.QPixmap("icons/search.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.search_tasks_icon = QtGui.QIcon()
        self.search_tasks_icon.addPixmap(QtGui.QPixmap("icons/search_tasks.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)

        self.show_consumables_icon = QtGui.QIcon()
        self.show_consumables_icon.addPixmap(QtGui.QPixmap("icons/show_parts_list.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)

        self.save_icon = QtGui.QIcon()
        self.save_icon.addPixmap(QtGui.QPixmap("icons/Save.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.add_spare_part_icon = QtGui.QIcon()
        self.add_spare_part_icon.addPixmap(QtGui.QPixmap("icons/add_spare_parts.png"), QtGui.QIcon.Normal,
                                           QtGui.QIcon.Off)
        self.selected_customer_icon = QtGui.QIcon()
        self.selected_customer_icon.addPixmap(QtGui.QPixmap("icons/selected_customer.png"), QtGui.QIcon.Normal,
                                              QtGui.QIcon.Off)

        self.store_icon = QtGui.QIcon()
        self.store_icon.addPixmap(QtGui.QPixmap("icons/store.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.add_task_icon = QtGui.QIcon()
        self.add_task_icon.addPixmap(QtGui.QPixmap("icons/add_scheduled_tasks.png"), QtGui.QIcon.Normal,
                                     QtGui.QIcon.Off)
        #
        # ----------------------------------------FONTS-------------------------------------------------
        self.font_12 = QtGui.QFont()
        self.font_12.setFamily("Calibri")
        self.font_12.setPointSize(12)
        self.font_12.setBold(False)
        self.font_12.setItalic(False)
        self.font_12.setWeight(10)
        self.font_14_bold = QtGui.QFont()
        self.font_14_bold.setFamily("Calibri")
        self.font_14_bold.setPointSize(14)
        self.font_14_bold.setBold(True)
        self.font_14_bold.setWeight(75)
        self.font_12_bold = QtGui.QFont()
        self.font_12_bold.setFamily("Calibri")
        self.font_12_bold.setPointSize(12)
        self.font_12_bold.setBold(True)
        self.font_12_bold.setWeight(75)
        # ----------------------------------------Πελατολόγιο--------------------------------------------
        self.customers_label = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.customers_label.sizePolicy().hasHeightForWidth())
        self.customers_label.setSizePolicy(sizePolicy)
        self.customers_label.setMaximumSize(QtCore.QSize(300, 16777215))

        self.customers_label.setFont(self.font_14_bold)
        self.customers_label.setStyleSheet("background-color: rgb(184, 184, 184);\n"
                                           "color: rgb(255, 255, 255);")
        self.customers_label.setAlignment(QtCore.Qt.AlignCenter)
        self.customers_label.setObjectName("customers_label")
        self.gridLayout_3.addWidget(self.customers_label, 0, 0, 1, 2)
        # Αναζήτηση Πελάτη
        self.search_customer_lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.search_customer_lineEdit.sizePolicy().hasHeightForWidth())
        self.search_customer_lineEdit.setSizePolicy(sizePolicy)
        self.search_customer_lineEdit.setMinimumSize(QtCore.QSize(260, 30))
        self.search_customer_lineEdit.setMaximumSize(QtCore.QSize(260, 16777215))
        self.search_customer_lineEdit.setFont(self.font_12)
        self.search_customer_lineEdit.setObjectName("search_customer_lineEdit")
        # self.search_customer_lineEdit.setCompleter(self.customers_completer)
        self.search_customer_lineEdit.returnPressed.connect(self.search_customer)
        self.gridLayout_3.addWidget(self.search_customer_lineEdit, 1, 0, 1, 1)



        self.search_customer_toolButton = QtWidgets.QToolButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.search_customer_toolButton.sizePolicy().hasHeightForWidth())
        self.search_customer_toolButton.setSizePolicy(sizePolicy)
        self.search_customer_toolButton.setMinimumSize(QtCore.QSize(0, 30))
        self.search_customer_toolButton.setMaximumSize(QtCore.QSize(30, 30))
        self.search_customer_toolButton.setFont(self.font_12_bold)
        self.search_customer_toolButton.setStyleSheet("background-color: rgb(113, 113, 113);\n"
                                                      "color: rgb(255, 255, 255);")
        self.search_customer_toolButton.setIcon(self.search_icon)
        self.search_customer_toolButton.setIconSize(QtCore.QSize(30, 30))
        self.search_customer_toolButton.setObjectName("search_customer_toolButton")
        self.search_customer_toolButton.clicked.connect(self.search_customer)
        self.gridLayout_3.addWidget(self.search_customer_toolButton, 1, 1, 1, 1)

        # Πελάτες Treewidget
        self.customers_treeWidget = QtWidgets.QTreeWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.customers_treeWidget.sizePolicy().hasHeightForWidth())
        self.customers_treeWidget.setSizePolicy(sizePolicy)
        self.customers_treeWidget.setMinimumSize(QtCore.QSize(300, 0))
        self.customers_treeWidget.setMaximumSize(QtCore.QSize(300, 16777215))
        # self.customers_treeWidget.setSortingEnabled(True)
        self.customers_treeWidget.setWordWrap(True)
        self.customers_treeWidget.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        # self.treeWidget.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.customers_treeWidget.setLineWidth(14)
        # self.customers_treeWidget.setAlternatingRowColors(True)
        self.customers_treeWidget.setHeaderLabels(["ID", "Πελάτης"])
        self.customers_treeWidget.headerItem().setTextAlignment(1, QtCore.Qt.AlignCenter)
        # self.treeWidget.setAnimated(True)
        self.customers_treeWidget.header().setStyleSheet(u"background-color: orange;" "color: black;"
                                                         "font-style: normal;font-size: 12pt;font-weight: bold;")
        self.customers_treeWidget.setFont(self.font_12)
        self.customers_treeWidget.setObjectName("customers_treeWidget")
        self.customers_treeWidget.itemClicked.connect(self.customer_clicked)
        self.gridLayout_3.addWidget(self.customers_treeWidget, 2, 0, 1, 2)

        # ---------------------------------------Machines----------------------------------------------
        self.machines_label = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.machines_label.sizePolicy().hasHeightForWidth())
        self.machines_label.setSizePolicy(sizePolicy)
        self.machines_label.setMaximumSize(QtCore.QSize(350, 16777215))
        self.machines_label.setFont(self.font_14_bold)
        self.machines_label.setStyleSheet("background-color: rgb(67, 67, 67);\n"
                                          "color: rgb(255, 255, 255);")
        self.machines_label.setAlignment(QtCore.Qt.AlignCenter)
        self.machines_label.setObjectName("machines_label")
        self.gridLayout_3.addWidget(self.machines_label, 0, 2, 1, 2)

        # Αναζήτηση μηχανημάτων
        self.search_machine_lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.search_machine_lineEdit.sizePolicy().hasHeightForWidth())
        self.search_machine_lineEdit.setSizePolicy(sizePolicy)
        self.search_machine_lineEdit.setMinimumSize(QtCore.QSize(310, 30))
        self.search_machine_lineEdit.setMaximumSize(QtCore.QSize(310, 16777215))
        self.search_machine_lineEdit.setFont(self.font_12)
        self.search_machine_lineEdit.setObjectName("search_machine_lineEdit")
        self.search_machine_lineEdit.returnPressed.connect(self.search_machine)
        self.gridLayout_3.addWidget(self.search_machine_lineEdit, 1, 2, 1, 1)
        self.search_machine_toolButton = QtWidgets.QToolButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.search_machine_toolButton.sizePolicy().hasHeightForWidth())
        self.search_machine_toolButton.setSizePolicy(sizePolicy)
        self.search_machine_toolButton.setMinimumSize(QtCore.QSize(0, 30))
        self.search_machine_toolButton.setMaximumSize(QtCore.QSize(30, 30))
        self.search_machine_toolButton.setFont(self.font_12_bold)
        self.search_machine_toolButton.setStyleSheet("background-color: rgb(113, 113, 113);\n"
                                                     "color: rgb(255, 255, 255);")
        self.search_machine_toolButton.setText("")
        self.search_machine_toolButton.setIcon(self.search_icon)
        self.search_machine_toolButton.setIconSize(QtCore.QSize(30, 30))
        self.search_machine_toolButton.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.search_machine_toolButton.setObjectName("search_machine_toolButton")
        self.search_machine_toolButton.clicked.connect(self.search_machine)
        self.gridLayout_3.addWidget(self.search_machine_toolButton, 1, 3, 1, 1)

        # Machine Treewidget
        self.machines_treeWidget = QtWidgets.QTreeWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.machines_treeWidget.sizePolicy().hasHeightForWidth())
        self.machines_treeWidget.setSizePolicy(sizePolicy)
        self.machines_treeWidget.setMinimumSize(QtCore.QSize(350, 0))
        self.machines_treeWidget.setMaximumSize(QtCore.QSize(350, 16777215))
        self.machines_treeWidget.setFont(self.font_12)
        self.machines_treeWidget.setObjectName("machines_treeWidget")
        self.machines_treeWidget.itemClicked.connect(self.machine_clicked)
        # self.customers_treeWidget.setSortingEnabled(True)
        self.machines_treeWidget.setWordWrap(True)
        self.machines_treeWidget.setAutoFillBackground(True)
        # self.machines_treeWidget.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        # self.treeWidget.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.machines_treeWidget.setLineWidth(14)
        # self.machines_treeWidget.setAlternatingRowColors(True)
        self.machines_treeWidget.setHeaderLabels(["ID", "Μηχάνημα"])
        self.machines_treeWidget.headerItem().setTextAlignment(1, QtCore.Qt.AlignCenter)
        self.machines_treeWidget.headerItem().setTextAlignment(0, QtCore.Qt.AlignLeft)
        self.machines_treeWidget.setSortingEnabled(True)
        self.machines_treeWidget.header().setStyleSheet(u"background-color: gray;" "color: white;"
                                                        "font-style: normal;font-size: 12pt;font-weight: bold;")
        self.gridLayout_3.addWidget(self.machines_treeWidget, 2, 2, 1, 2)

        # -------------------------------------Κλήσεις------------------------------------------
        # Ημερολόγιο εργασίων
        self.tasks_label = QtWidgets.QLabel(self.centralwidget)
        self.tasks_label.setFont(self.font_14_bold)
        self.tasks_label.setStyleSheet("background-color: rgb(100, 100, 100);\n" "color: rgb(255, 255, 255);")
        self.tasks_label.setAlignment(QtCore.Qt.AlignCenter)
        self.tasks_label.setWordWrap(False)
        self.tasks_label.setObjectName("tasks_label")
        self.gridLayout_3.addWidget(self.tasks_label, 5, 0, 1, 15)

        # Προσθήκη εργασίας
        self.add_task_toolButton = QtWidgets.QToolButton(self.centralwidget)
        # sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        # sizePolicy.setHorizontalStretch(0)
        # sizePolicy.setVerticalStretch(0)
        # sizePolicy.setHeightForWidth(self.add_task_toolButton.sizePolicy().hasHeightForWidth())
        # self.add_task_toolButton.setSizePolicy(sizePolicy)
        # self.add_task_toolButton.setMaximumSize(QtCore.QSize(16777215, 30))
        self.add_task_toolButton.setFont(self.font_12_bold)
        self.add_task_toolButton.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.add_task_toolButton.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.add_task_toolButton.setAutoFillBackground(False)
        self.add_task_toolButton.setStyleSheet("background-color: rgb(0, 157, 0);\n"
                                               "color: rgb(255, 255, 255);")

        self.add_task_toolButton.setIcon(self.add_task_icon)
        self.add_task_toolButton.setIconSize(QtCore.QSize(30, 30))
        # self.add_task_toolButton.setShortcut("")
        self.add_task_toolButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.add_task_toolButton.setObjectName("add_task_toolButton")
        self.add_task_toolButton.clicked.connect(self.show_add_task_window)
        self.gridLayout_3.addWidget(self.add_task_toolButton, 6, 0, 2, 2)

        # Search Tasks
        self.search_on_tasks_label = QtWidgets.QLabel(self.centralwidget)
        self.search_on_tasks_label.setFont(self.font_12_bold)
        self.search_on_tasks_label.setAlignment(QtCore.Qt.AlignCenter)
        self.search_on_tasks_label.setObjectName("search_on_tasks_label")
        self.gridLayout_3.addWidget(self.search_on_tasks_label, 6, 5, 1, 3)

        self.search_on_tasks_lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.search_on_tasks_lineEdit.setEnabled(True)
        # sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        # sizePolicy.setHorizontalStretch(0)
        # sizePolicy.setVerticalStretch(0)
        # sizePolicy.setHeightForWidth(self.search_on_tasks_lineEdit.sizePolicy().hasHeightForWidth())
        # self.search_on_tasks_lineEdit.setSizePolicy(sizePolicy)
        # self.search_on_tasks_lineEdit.setMinimumSize(QtCore.QSize(0, 30))
        self.search_on_tasks_lineEdit.setMaximumSize(QtCore.QSize(16777215, 50))
        self.search_on_tasks_lineEdit.setFont(self.font_12)
        self.search_on_tasks_lineEdit.setObjectName("search_on_tasks_lineEdit")
        self.search_on_tasks_lineEdit.returnPressed.connect(self.search_tasks)
        self.gridLayout_3.addWidget(self.search_on_tasks_lineEdit, 7, 5, 1, 2)
        self.search_on_tasks_toolButton = QtWidgets.QToolButton(self.centralwidget)
        # sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        # sizePolicy.setHorizontalStretch(0)
        # sizePolicy.setVerticalStretch(0)
        # sizePolicy.setHeightForWidth(self.search_on_tasks_toolButton.sizePolicy().hasHeightForWidth())
        # self.search_on_tasks_toolButton.setSizePolicy(sizePolicy)
        self.search_on_tasks_toolButton.setMinimumSize(QtCore.QSize(0, 30))
        self.search_on_tasks_toolButton.setMaximumSize(QtCore.QSize(30, 30))
        self.search_on_tasks_toolButton.setFont(self.font_12_bold)
        self.search_on_tasks_toolButton.setStyleSheet("background-color: rgb(113, 113, 113);\n"
                                                      "color: rgb(255, 255, 255);")
        self.search_on_tasks_toolButton.setText("")
        self.search_on_tasks_toolButton.setIcon(self.search_icon)
        self.search_on_tasks_toolButton.setIconSize(QtCore.QSize(30, 20))
        self.search_on_tasks_toolButton.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.search_on_tasks_toolButton.setObjectName("search_on_tasks_toolButton")
        self.search_on_tasks_toolButton.clicked.connect(self.search_tasks)
        self.gridLayout_3.addWidget(self.search_on_tasks_toolButton, 7, 7, 1, 1)

        # DTE
        self.dte_label = QtWidgets.QLabel(self.centralwidget)
        self.dte_label.setFont(self.font_12_bold)
        self.dte_label.setStyleSheet("background-color: rgb(255, 170, 0);")
        self.dte_label.setText("ΔΤΕ")
        self.dte_label.setScaledContents(True)
        self.dte_label.setAlignment(QtCore.Qt.AlignCenter)
        self.dte_label.setWordWrap(True)
        self.dte_label.setObjectName("dte_label")
        self.gridLayout_3.addWidget(self.dte_label, 6, 9, 1, 2)
        self.search_dte_on_tasks_lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.search_dte_on_tasks_lineEdit.sizePolicy().hasHeightForWidth())
        self.search_dte_on_tasks_lineEdit.setSizePolicy(sizePolicy)
        self.search_dte_on_tasks_lineEdit.setMinimumSize(QtCore.QSize(0, 30))
        self.search_dte_on_tasks_lineEdit.setMaximumSize(QtCore.QSize(50, 16777215))
        self.search_dte_on_tasks_lineEdit.setFont(self.font_12)
        self.search_dte_on_tasks_lineEdit.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.search_dte_on_tasks_lineEdit.setAlignment(
            QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.search_dte_on_tasks_lineEdit.setPlaceholderText("")
        self.search_dte_on_tasks_lineEdit.setObjectName("search_dte_on_tasks_lineEdit")
        self.search_dte_on_tasks_lineEdit.returnPressed.connect(self.search_dte)
        self.gridLayout_3.addWidget(self.search_dte_on_tasks_lineEdit, 7, 9, 1, 1)
        self.search_dte_on_tasks_toolButton = QtWidgets.QToolButton(self.centralwidget)
        self.search_dte_on_tasks_toolButton.setMinimumSize(QtCore.QSize(0, 30))
        self.search_dte_on_tasks_toolButton.setStyleSheet("background-color: rgb(255, 170, 0);")
        self.search_dte_on_tasks_toolButton.setIcon(self.search_tasks_icon)
        self.search_dte_on_tasks_toolButton.setIconSize(QtCore.QSize(30, 20))
        self.search_dte_on_tasks_toolButton.setObjectName("search_dte_on_tasks_toolButton")
        self.search_dte_on_tasks_toolButton.clicked.connect(self.search_dte)
        self.gridLayout_3.addWidget(self.search_dte_on_tasks_toolButton, 7, 10, 1, 1)

        # Ολοκληρωμένες εργασίες
        self.finished_tasks_label = QtWidgets.QLabel(self.centralwidget)
        # sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        # sizePolicy.setHorizontalStretch(0)
        # sizePolicy.setVerticalStretch(0)
        # sizePolicy.setHeightForWidth(self.finished_tasks_label.sizePolicy().hasHeightForWidth())
        # self.finished_tasks_label.setSizePolicy(sizePolicy)
        self.finished_tasks_label.setFont(self.font_12_bold)
        self.finished_tasks_label.setAlignment(QtCore.Qt.AlignCenter)
        self.finished_tasks_label.setObjectName("finished_tasks_label")
        self.gridLayout_3.addWidget(self.finished_tasks_label, 6, 12, 1, 2)
        self.finished_tasks_dateEdit = QtWidgets.QDateEdit(self.centralwidget)
        # sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        # sizePolicy.setHorizontalStretch(0)
        # sizePolicy.setVerticalStretch(0)
        # sizePolicy.setHeightForWidth(self.finished_tasks_dateEdit.sizePolicy().hasHeightForWidth())
        # self.finished_tasks_dateEdit.setSizePolicy(sizePolicy)
        # self.finished_tasks_dateEdit.setMinimumSize(QtCore.QSize(0, 30))
        # self.finished_tasks_dateEdit.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.finished_tasks_dateEdit.setFont(self.font_12_bold)
        self.finished_tasks_dateEdit.setStyleSheet("background-color: rgb(125, 125, 125);\n" "color: rgb(255, 170, 0);")
        self.finished_tasks_dateEdit.setWrapping(True)
        self.finished_tasks_dateEdit.setFrame(True)
        self.finished_tasks_dateEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.finished_tasks_dateEdit.setButtonSymbols(QtWidgets.QAbstractSpinBox.UpDownArrows)
        self.finished_tasks_dateEdit.setCalendarPopup(True)
        self.finished_tasks_dateEdit.setDate(QtCore.QDate.currentDate())
        self.finished_tasks_dateEdit.dateChanged.connect(self.show_completed_tasks)
        self.finished_tasks_dateEdit.setObjectName("finished_tasks_dateEdit")
        self.gridLayout_3.addWidget(self.finished_tasks_dateEdit, 7, 12, 1, 2)

        # -------------------------------------- Calendar ---------------------------------------
        # Calendar
        self.calendarWidget = QtWidgets.QCalendarWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.calendarWidget.sizePolicy().hasHeightForWidth())
        self.calendarWidget.setSizePolicy(sizePolicy)
        self.calendarWidget.setFont(self.font_12_bold)
        self.calendarWidget.setObjectName("calendarWidget")
        self.calendarWidget.clicked.connect(self.left_calendar_clicked)
        self.gridLayout_3.addWidget(self.calendarWidget, 10, 0, 1, 2)

        # Κλήσεις Treewidget
        self.tasks_treeWidget = QtWidgets.QTreeWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tasks_treeWidget.sizePolicy().hasHeightForWidth())
        self.tasks_treeWidget.setSizePolicy(sizePolicy)
        self.tasks_treeWidget.setFont(self.font_12)
        self.tasks_treeWidget.setAutoFillBackground(True)
        self.tasks_treeWidget.setWordWrap(True)
        self.tasks_treeWidget.setObjectName("tasks_treeWidget")
        self.tasks_treeWidget.itemDoubleClicked.connect(self.show_edit_task_window)
        self.gridLayout_3.addWidget(self.tasks_treeWidget, 10, 2, 1, 13)

        #  ------------------------------------------------ Tabs---------------------------
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        # sizePolicy.setHorizontalStretch(0)
        # sizePolicy.setVerticalStretch(0)
        # sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setMinimumSize(QtCore.QSize(0, 0))
        self.tabWidget.setMaximumSize(QtCore.QSize(16777215, 450))
        self.tabWidget.setTabPosition(QtWidgets.QTabWidget.North)
        self.tabWidget.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.tabWidget.setIconSize(QtCore.QSize(25, 25))
        self.tabWidget.setElideMode(QtCore.Qt.ElideNone)
        self.tabWidget.setDocumentMode(False)
        self.tabWidget.setTabsClosable(False)
        self.tabWidget.setMovable(True)
        self.tabWidget.setTabBarAutoHide(False)
        self.tabWidget.setObjectName("tabWidget")

        # ---------------------------------------------- Παλάτης Tab ------------------------------
        # Customer Tab
        self.customer_tab = QtWidgets.QWidget()
        self.customer_tab.setObjectName("customer_tab")
        self.gridLayout = QtWidgets.QGridLayout(self.customer_tab)
        self.gridLayout.setObjectName("gridLayout")

        # Customer Name Επωνυμία
        self.customer_name_label = QtWidgets.QLabel(self.customer_tab)
        self.customer_name_label.setMinimumSize(QtCore.QSize(0, 0))
        self.customer_name_label.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.customer_name_label.setFont(self.font_12_bold)
        self.customer_name_label.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.customer_name_label.setObjectName("customer_name_label")
        self.gridLayout.addWidget(self.customer_name_label, 0, 0, 1, 1)
        self.customer_name_lineEdit = QtWidgets.QLineEdit(self.customer_tab)
        self.customer_name_lineEdit.setMinimumSize(QtCore.QSize(0, 0))
        self.customer_name_lineEdit.setFont(self.font_12)
        self.customer_name_lineEdit.setObjectName("customer_name_lineEdit")
        self.gridLayout.addWidget(self.customer_name_lineEdit, 0, 1, 1, 2)

        # Customer Address Διεύθυνση
        self.address_label = QtWidgets.QLabel(self.customer_tab)
        self.address_label.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.address_label.setFont(self.font_12_bold)
        self.address_label.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.address_label.setObjectName("address_label")
        self.gridLayout.addWidget(self.address_label, 1, 0, 1, 1)
        self.address_lineEdit = QtWidgets.QLineEdit(self.customer_tab)
        self.address_lineEdit.setMinimumSize(QtCore.QSize(0, 0))
        self.address_lineEdit.setFont(self.font_12)
        self.address_lineEdit.setObjectName("address_lineEdit")
        self.gridLayout.addWidget(self.address_lineEdit, 1, 1, 1, 2)

        # Customer Mobile
        self.mobile_label = QtWidgets.QLabel(self.customer_tab)
        self.mobile_label.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.mobile_label.setFont(self.font_12_bold)
        self.mobile_label.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.mobile_label.setObjectName("mobile_label")
        self.gridLayout.addWidget(self.mobile_label, 2, 0, 1, 1)
        self.mobile_lineEdit = QtWidgets.QLineEdit(self.customer_tab)
        self.mobile_lineEdit.setFont(self.font_12)
        self.mobile_lineEdit.setObjectName("mobile_lineEdit")
        self.gridLayout.addWidget(self.mobile_lineEdit, 2, 1, 1, 2)

        # Customer Phone Τηλέφωνο
        self.phone_label = QtWidgets.QLabel(self.customer_tab)
        self.phone_label.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.phone_label.setFont(self.font_12_bold)
        self.phone_label.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.phone_label.setObjectName("phone_label")
        self.gridLayout.addWidget(self.phone_label, 3, 0, 1, 1)
        self.phone_lineEdit = QtWidgets.QLineEdit(self.customer_tab)
        self.phone_lineEdit.setFont(self.font_12)
        self.phone_lineEdit.setObjectName("phone_lineEdit")
        self.gridLayout.addWidget(self.phone_lineEdit, 3, 1, 1, 2)

        # Email
        self.email_label = QtWidgets.QLabel(self.customer_tab)
        self.email_label.setFont(self.font_12_bold)
        self.email_label.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.email_label.setObjectName("email_label")
        self.gridLayout.addWidget(self.email_label, 4, 0, 1, 1)
        self.email_lineEdit = QtWidgets.QLineEdit(self.customer_tab)
        self.email_lineEdit.setFont(self.font_12)
        self.email_lineEdit.setObjectName("email_lineEdit")
        self.gridLayout.addWidget(self.email_lineEdit, 4, 1, 1, 2)

        # Responsible
        self.responsible_label = QtWidgets.QLabel(self.customer_tab)
        self.responsible_label.setFont(self.font_12_bold)
        self.responsible_label.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.responsible_label.setObjectName("responsible_label")
        self.gridLayout.addWidget(self.responsible_label, 0, 3, 1, 2)
        self.responsible_lineEdit = QtWidgets.QLineEdit(self.customer_tab)
        self.responsible_lineEdit.setFont(self.font_12)
        self.responsible_lineEdit.setObjectName("responsible_lineEdit")
        self.gridLayout.addWidget(self.responsible_lineEdit, 0, 5, 1, 1)

        # Customer City Πόλη
        self.city_label = QtWidgets.QLabel(self.customer_tab)
        self.city_label.setFont(self.font_12_bold)
        self.city_label.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.city_label.setObjectName("city_label")
        self.gridLayout.addWidget(self.city_label, 1, 3, 1, 1)
        self.city_lineEdit = QtWidgets.QLineEdit(self.customer_tab)
        self.city_lineEdit.setFont(self.font_12)
        self.city_lineEdit.setObjectName("city_lineEdit")
        self.gridLayout.addWidget(self.city_lineEdit, 1, 5, 1, 1)

        # Customer Area
        self.area_label = QtWidgets.QLabel(self.customer_tab)
        self.area_label.setFont(self.font_12_bold)
        self.area_label.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.area_label.setObjectName("area_label")
        self.gridLayout.addWidget(self.area_label, 2, 3, 1, 1)
        self.area_lineEdit = QtWidgets.QLineEdit(self.customer_tab)
        self.area_lineEdit.setFont(self.font_12)
        self.area_lineEdit.setObjectName("area_lineEdit")
        self.gridLayout.addWidget(self.area_lineEdit, 2, 5, 1, 1)

        # Customer Post Code Τ.κ.
        self.post_code_label = QtWidgets.QLabel(self.customer_tab)
        self.post_code_label.setFont(self.font_12_bold)
        self.post_code_label.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.post_code_label.setObjectName("post_code_label")
        self.gridLayout.addWidget(self.post_code_label, 3, 3, 1, 1)
        self.post_code_lineEdit = QtWidgets.QLineEdit(self.customer_tab)
        self.post_code_lineEdit.setFont(self.font_12)
        self.post_code_lineEdit.setObjectName("post_code_lineEdit")
        self.gridLayout.addWidget(self.post_code_lineEdit, 3, 5, 1, 1)

        # Fax
        self.fax_label = QtWidgets.QLabel(self.customer_tab)
        self.fax_label.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.fax_label.setFont(self.font_12_bold)
        self.fax_label.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.fax_label.setObjectName("fax_label")
        self.gridLayout.addWidget(self.fax_label, 4, 3, 1, 1)
        self.fax_lineEdit = QtWidgets.QLineEdit(self.customer_tab)
        self.fax_lineEdit.setFont(self.font_12)
        self.fax_lineEdit.setObjectName("fax_lineEdit")
        self.gridLayout.addWidget(self.fax_lineEdit, 4, 5, 1, 1)

        # Customer Notes
        self.customer_notes_label = QtWidgets.QLabel(self.customer_tab)
        self.customer_notes_label.setFont(self.font_14_bold)
        self.customer_notes_label.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.customer_notes_label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.customer_notes_label.setStyleSheet("background-color: rgb(89, 89, 89);\n"
                                                "color: rgb(255, 255, 255);")
        self.customer_notes_label.setLocale(QtCore.QLocale(QtCore.QLocale.Greek, QtCore.QLocale.Greece))
        self.customer_notes_label.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.customer_notes_label.setAlignment(QtCore.Qt.AlignCenter)
        self.customer_notes_label.setObjectName("customer_notes_label")
        self.gridLayout.addWidget(self.customer_notes_label, 7, 0, 1, 6)
        self.customer_notes_textEdit = QtWidgets.QTextEdit(self.customer_tab)
        self.customer_notes_textEdit.setFont(self.font_12)
        self.customer_notes_textEdit.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.customer_notes_textEdit.setObjectName("customer_notes_textEdit")
        self.gridLayout.addWidget(self.customer_notes_textEdit, 8, 0, 1, 6)

        # Save Customer Αποθύκευση
        self.save_customer_changes_toolButton = QtWidgets.QToolButton(self.customer_tab)
        self.save_customer_changes_toolButton.setMinimumSize(QtCore.QSize(0, 30))
        self.save_customer_changes_toolButton.setFont(self.font_12_bold)
        self.save_customer_changes_toolButton.setStyleSheet("background-color: rgb(104, 104, 104);\n"
                                                            "color: rgb(255, 255, 255);")
        self.save_customer_changes_toolButton.setIcon(self.save_icon)
        self.save_customer_changes_toolButton.setIconSize(QtCore.QSize(40, 40))
        self.save_customer_changes_toolButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.save_customer_changes_toolButton.setObjectName("save_customer_changes_toolButton")
        self.save_customer_changes_toolButton.clicked.connect(self.save_customer_changes)
        self.gridLayout.addWidget(self.save_customer_changes_toolButton, 9, 0, 1, 2)

        # Disable Customer Απενεργοποιήση πελάτη
        self.disable_customer_toolButton = QtWidgets.QToolButton(self.customer_tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.disable_customer_toolButton.sizePolicy().hasHeightForWidth())
        self.disable_customer_toolButton.setSizePolicy(sizePolicy)
        self.disable_customer_toolButton.setMinimumSize(QtCore.QSize(0, 30))
        self.disable_customer_toolButton.setFont(self.font_12_bold)
        self.disable_customer_toolButton.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.disable_customer_toolButton.setStyleSheet("background-color: rgb(104, 104, 104);\n"
                                                       "color: rgb(255, 255, 255);")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("icons/del_sender.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.disable_customer_toolButton.setIcon(icon3)
        self.disable_customer_toolButton.setIconSize(QtCore.QSize(40, 40))
        # self.disable_customer_toolButton.setShortcut("")
        self.disable_customer_toolButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.disable_customer_toolButton.setObjectName("disable_customer_toolButton")
        self.disable_customer_toolButton.clicked.connect(self.disable_customer)
        self.gridLayout.addWidget(self.disable_customer_toolButton, 9, 5, 1, 1)

        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("icons/search_customer.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tabWidget.addTab(self.customer_tab, icon4, "Πελάτης")

        # -------------------------------------Machine Tab -------------------------
        self.machine_tab = QtWidgets.QWidget()
        self.machine_tab.setObjectName("machine_tab")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.machine_tab)
        self.gridLayout_2.setObjectName("gridLayout_2")
        # Machine Serial No
        self.serial_number_label = QtWidgets.QLabel(self.machine_tab)
        self.serial_number_label.setMaximumSize(QtCore.QSize(299, 16777215))
        self.serial_number_label.setFont(self.font_12_bold)
        self.serial_number_label.setObjectName("serial_number_label")
        self.gridLayout_2.addWidget(self.serial_number_label, 0, 0, 1, 1)
        self.serial_number_lineEdit = QtWidgets.QLineEdit(self.machine_tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.serial_number_lineEdit.sizePolicy().hasHeightForWidth())
        self.serial_number_lineEdit.setSizePolicy(sizePolicy)
        self.serial_number_lineEdit.setMaximumSize(QtCore.QSize(299, 16777215))
        self.serial_number_lineEdit.setFont(self.font_12)
        self.serial_number_lineEdit.setObjectName("serial_number_lineEdit")
        self.gridLayout_2.addWidget(self.serial_number_lineEdit, 1, 0, 1, 2)

        # Machine Model
        self.copier_model_label = QtWidgets.QLabel(self.machine_tab)
        self.copier_model_label.setFont(self.font_12_bold)
        self.copier_model_label.setObjectName("copier_model_label")
        self.gridLayout_2.addWidget(self.copier_model_label, 0, 2, 1, 1)
        self.copier_model_lineEdit = QtWidgets.QLineEdit(self.machine_tab)
        self.copier_model_lineEdit.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.copier_model_lineEdit.setFont(self.font_12)
        self.copier_model_lineEdit.setObjectName("copier_model_lineEdit")
        self.gridLayout_2.addWidget(self.copier_model_lineEdit, 1, 2, 1, 1)

        # Machine Start counter
        self.start_counter_label = QtWidgets.QLabel(self.machine_tab)
        self.start_counter_label.setMaximumSize(QtCore.QSize(305, 16777215))
        self.start_counter_label.setFont(self.font_12_bold)
        self.start_counter_label.setObjectName("start_counter_label")
        self.gridLayout_2.addWidget(self.start_counter_label, 2, 0, 1, 2)
        self.start_counter_lineEdit = QtWidgets.QLineEdit(self.machine_tab)
        self.start_counter_lineEdit.setMaximumSize(QtCore.QSize(299, 16777215))
        self.start_counter_lineEdit.setFont(self.font_12)
        self.start_counter_lineEdit.setObjectName("start_counter_lineEdit")
        self.gridLayout_2.addWidget(self.start_counter_lineEdit, 3, 0, 1, 1)

        # Machine Started date
        self.start_date_label = QtWidgets.QLabel(self.machine_tab)
        self.start_date_label.setMaximumSize(QtCore.QSize(147, 16777215))
        self.start_date_label.setFont(self.font_12_bold)
        self.start_date_label.setObjectName("start_date_label")
        self.gridLayout_2.addWidget(self.start_date_label, 2, 2, 1, 1)
        self.started_date_dateEdit = QtWidgets.QDateEdit(self.machine_tab)
        self.started_date_dateEdit.setMaximumSize(QtCore.QSize(147, 16777215))
        self.started_date_dateEdit.setFont(self.font_12_bold)
        self.started_date_dateEdit.setCalendarPopup(True)
        self.started_date_dateEdit.setObjectName("started_date_dateEdit")
        self.gridLayout_2.addWidget(self.started_date_dateEdit, 3, 2, 1, 1)

        # Transport label
        # self.transport_machine_label = QtWidgets.QLabel(self.machine_tab)
        # self.transport_machine_label.setFont(self.font_14_bold)
        # self.transport_machine_label.setStyleSheet("background-color: rgb(170, 0, 0);\n"
        #                                            "color: rgb(255, 255, 255);")
        # self.transport_machine_label.setAlignment(QtCore.Qt.AlignCenter)
        # self.transport_machine_label.setObjectName("transport_machine_label")
        # self.gridLayout_2.addWidget(self.transport_machine_label, 4, 0, 1, 5)
        # New customer combobox
        # self.new_customer_lineEdit = QtWidgets.QLineEdit(self.machine_tab)
        # self.new_customer_lineEdit.setMinimumSize(QtCore.QSize(0, 30))
        # self.new_customer_lineEdit.setObjectName("new_customer_lineEdit")
        # self.new_customer_lineEdit.setFont(self.font_12_bold)
        #
        # self.new_customer_combobox = QtWidgets.QComboBox(self.machine_tab)
        # self.new_customer_combobox.setMinimumSize(QtCore.QSize(0, 30))
        # self.new_customer_combobox.setFont(self.font_12_bold)
        # self.new_customer_combobox.setObjectName("new_customer_combobox")
        # self.new_customer_combobox.setLineEdit(self.new_customer_lineEdit)
        # self.gridLayout_2.addWidget(self.new_customer_combobox, 5, 0, 1, 3)
        self.transport_machine_toolButton = QtWidgets.QToolButton(self.machine_tab)
        self.transport_machine_toolButton.setMinimumSize(QtCore.QSize(0, 30))
        self.transport_machine_toolButton.setMaximumSize(QtCore.QSize(16777215, 30))
        self.transport_machine_toolButton.setFont(self.font_12_bold)
        self.transport_machine_toolButton.setStyleSheet("background-color: rgb(104, 104, 104);\n"
                                                        "color: rgb(255, 255, 255);")
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap("icons/transport_copier.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.transport_machine_toolButton.setIcon(icon6)
        self.transport_machine_toolButton.setIconSize(QtCore.QSize(40, 40))
        self.transport_machine_toolButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.transport_machine_toolButton.setObjectName("transport_machine_toolButton")
        self.transport_machine_toolButton.clicked.connect(self.show_transport_machine_window)
        self.gridLayout_2.addWidget(self.transport_machine_toolButton, 5, 3, 1, 1)

        # Machine Notes
        self.copier_notes_label = QtWidgets.QLabel(self.machine_tab)
        self.copier_notes_label.setFont(self.font_14_bold)
        self.copier_notes_label.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.copier_notes_label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.copier_notes_label.setStyleSheet("background-color: rgb(89, 89, 89);\n"
                                              "color: rgb(255, 255, 255);")
        self.copier_notes_label.setLocale(QtCore.QLocale(QtCore.QLocale.Greek, QtCore.QLocale.Greece))
        self.copier_notes_label.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.copier_notes_label.setAlignment(QtCore.Qt.AlignCenter)
        self.copier_notes_label.setObjectName("copier_notes_label")
        self.gridLayout_2.addWidget(self.copier_notes_label, 7, 0, 1, 5)
        self.copiers_notes_textEdit = QtWidgets.QTextEdit(self.machine_tab)
        self.copiers_notes_textEdit.setFont(self.font_12)
        self.copiers_notes_textEdit.setObjectName("copiers_notes_textEdit")
        self.gridLayout_2.addWidget(self.copiers_notes_textEdit, 8, 0, 1, 5)

        # Machine Save
        self.save_copier_changes_toolButton = QtWidgets.QToolButton(self.machine_tab)
        self.save_copier_changes_toolButton.setMinimumSize(QtCore.QSize(0, 30))
        self.save_copier_changes_toolButton.setMaximumSize(QtCore.QSize(16777215, 30))
        self.save_copier_changes_toolButton.setFont(self.font_12_bold)
        self.save_copier_changes_toolButton.setStyleSheet("background-color: rgb(104, 104, 104);\n"
                                                          "color: rgb(255, 255, 255);")
        self.save_copier_changes_toolButton.setIcon(self.save_icon)
        self.save_copier_changes_toolButton.setIconSize(QtCore.QSize(40, 40))
        # self.save_copier_changes_toolButton.setShortcut("Ctrl+S")
        self.save_copier_changes_toolButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.save_copier_changes_toolButton.setObjectName("save_copier_changes_toolButton")
        self.save_copier_changes_toolButton.clicked.connect(self.save_machine_changes)
        self.gridLayout_2.addWidget(self.save_copier_changes_toolButton, 9, 0, 1, 1)

        # Machine Disable Απενεργοποιήση μηχανήματος
        self.disable_copier_toolButton = QtWidgets.QToolButton(self.machine_tab)
        self.disable_copier_toolButton.setMinimumSize(QtCore.QSize(0, 30))
        self.disable_copier_toolButton.setMaximumSize(QtCore.QSize(16777215, 30))
        self.disable_copier_toolButton.setFont(self.font_12_bold)
        self.disable_copier_toolButton.setStyleSheet("background-color: rgb(104, 104, 104);\n"
                                                     "color: rgb(255, 255, 255);")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("icons/disable_machine.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.disable_copier_toolButton.setIcon(icon5)
        self.disable_copier_toolButton.setIconSize(QtCore.QSize(40, 40))
        self.disable_copier_toolButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.disable_copier_toolButton.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.disable_copier_toolButton.setObjectName("disable_copier_toolButton")
        self.disable_copier_toolButton.clicked.connect(self.disable_machine)
        self.gridLayout_2.addWidget(self.disable_copier_toolButton, 9, 3, 1, 1)

        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap("icons/print.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tabWidget.addTab(self.machine_tab, icon6, "Μηχάνημα")

        # ---------------------------------------- Ιστορικό  tab ----------------------
        self.history_tab = QtWidgets.QWidget()
        self.history_tab.setObjectName("history_tab")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.history_tab)
        self.gridLayout_4.setObjectName("gridLayout_4")

        # Search History Treewidget
        self.search_maintenance_label = QtWidgets.QLabel(self.history_tab)
        self.search_maintenance_label.setFont(self.font_12_bold)
        self.search_maintenance_label.setAlignment(QtCore.Qt.AlignCenter)
        self.search_maintenance_label.setObjectName("search_maintenance_label")
        self.gridLayout_4.addWidget(self.search_maintenance_label, 1, 0, 2, 1)
        self.search_maintenance_lineEdit = QtWidgets.QLineEdit(self.history_tab)
        self.search_maintenance_lineEdit.setMinimumSize(QtCore.QSize(0, 30))
        self.search_maintenance_lineEdit.setMaximumSize(QtCore.QSize(250, 16777215))
        self.search_maintenance_lineEdit.setFont(self.font_12)
        self.search_maintenance_lineEdit.setObjectName("search_maintenance_lineEdit")
        self.search_maintenance_lineEdit.returnPressed.connect(self.search_service)
        self.gridLayout_4.addWidget(self.search_maintenance_lineEdit, 3, 0, 1, 1)
        self.search_maintenance_toolButton = QtWidgets.QToolButton(self.history_tab)
        self.search_maintenance_toolButton.setMinimumSize(QtCore.QSize(0, 30))
        self.search_maintenance_toolButton.setMaximumSize(QtCore.QSize(30, 30))
        self.search_maintenance_toolButton.setStyleSheet("background-color: rgb(113, 113, 113);\n"
                                                         "color: rgb(255, 255, 255);")
        self.search_maintenance_toolButton.setIcon(self.search_icon)
        self.search_maintenance_toolButton.setIconSize(QtCore.QSize(25, 25))
        self.search_maintenance_toolButton.setObjectName("search_maintenance_toolButton")
        self.search_maintenance_toolButton.clicked.connect(self.search_service)
        self.gridLayout_4.addWidget(self.search_maintenance_toolButton, 3, 1, 1, 1)

        # DTE Service
        self.dte_service_label = QtWidgets.QLabel(self.centralwidget)
        self.dte_service_label.setFont(self.font_12_bold)
        self.dte_service_label.setStyleSheet("background-color: rgb(255, 170, 0);")
        self.dte_service_label.setText("ΔΤΕ")
        self.dte_service_label.setScaledContents(True)
        self.dte_service_label.setAlignment(QtCore.Qt.AlignCenter)
        self.dte_service_label.setWordWrap(True)
        self.dte_service_label.setObjectName("dte_service_label")
        self.gridLayout_4.addWidget(self.dte_service_label, 1, 2, 1, 2)
        self.search_dte_on_service_lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.search_dte_on_service_lineEdit.sizePolicy().hasHeightForWidth())
        self.search_dte_on_service_lineEdit.setSizePolicy(sizePolicy)
        self.search_dte_on_service_lineEdit.setMinimumSize(QtCore.QSize(0, 30))
        self.search_dte_on_service_lineEdit.setMaximumSize(QtCore.QSize(50, 16777215))
        self.search_dte_on_service_lineEdit.setFont(self.font_12)
        self.search_dte_on_service_lineEdit.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.search_dte_on_service_lineEdit.setAlignment(
            QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.search_dte_on_service_lineEdit.setPlaceholderText("")
        self.search_dte_on_service_lineEdit.setObjectName("search_dte_on_service_lineEdit")
        self.search_dte_on_service_lineEdit.returnPressed.connect(self.search_dte_on_service)
        self.gridLayout_4.addWidget(self.search_dte_on_service_lineEdit, 3, 2, 1, 1)

        self.search_dte_on_service_toolButton = QtWidgets.QToolButton(self.centralwidget)
        self.search_dte_on_service_toolButton.setMinimumSize(QtCore.QSize(0, 30))
        self.search_dte_on_service_toolButton.setStyleSheet("background-color: rgb(255, 170, 0);")
        self.search_dte_on_service_toolButton.setIcon(self.search_tasks_icon)
        self.search_dte_on_service_toolButton.setIconSize(QtCore.QSize(30, 20))
        self.search_dte_on_service_toolButton.setObjectName("search_dte_on_service_toolButton")
        self.search_dte_on_service_toolButton.clicked.connect(self.search_dte_on_service)
        self.gridLayout_4.addWidget(self.search_dte_on_service_toolButton, 3, 3, 1, 1)

        # Search Errors
        self.search_errors_label = QtWidgets.QLabel(self.history_tab)
        self.search_errors_label.setFont(self.font_12_bold)
        self.search_errors_label.setAlignment(QtCore.Qt.AlignCenter)
        self.search_errors_label.setObjectName("search_errors_label")
        self.gridLayout_4.addWidget(self.search_errors_label, 1, 4, 1, 1)
        self.search_errors_lineEdit = QtWidgets.QLineEdit(self.history_tab)
        self.search_errors_lineEdit.setMinimumSize(QtCore.QSize(0, 30))
        self.search_errors_lineEdit.setMaximumSize(QtCore.QSize(250, 16777215))
        self.search_errors_lineEdit.setFont(self.font_12)
        self.search_errors_lineEdit.setObjectName("search_errors_lineEdit")
        self.search_errors_lineEdit.returnPressed.connect(self.search_error)
        self.gridLayout_4.addWidget(self.search_errors_lineEdit, 3, 4, 1, 1)
        self.search_errors_toolButton = QtWidgets.QToolButton(self.history_tab)
        self.search_errors_toolButton.setMinimumSize(QtCore.QSize(0, 30))
        self.search_errors_toolButton.setStyleSheet("background-color: rgb(113, 113, 113);\n"
                                                    "color: rgb(255, 255, 255);")
        self.search_errors_toolButton.setIcon(self.search_icon)
        self.search_errors_toolButton.setIconSize(QtCore.QSize(25, 25))
        self.search_errors_toolButton.setObjectName("search_errors_toolButton")
        self.search_errors_toolButton.clicked.connect(self.search_error)
        self.gridLayout_4.addWidget(self.search_errors_toolButton, 3, 5, 1, 1)

        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap("icons/service.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tabWidget.addTab(self.history_tab, icon8, "Ιστορικό")

        # History treewirget
        self.history_treeWidget = QtWidgets.QTreeWidget(self.history_tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding,
                                           QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.history_treeWidget.sizePolicy().hasHeightForWidth())
        self.history_treeWidget.setSizePolicy(sizePolicy)
        self.history_treeWidget.setFont(self.font_12)
        self.history_treeWidget.setWordWrap(True)
        self.history_treeWidget.setObjectName("history_treeWidget")
        self.history_treeWidget.setLineWidth(14)
        self.history_treeWidget.setAlternatingRowColors(True)
        self.history_treeWidget.setSortingEnabled(True)
        self.history_treeWidget.header().setSortIndicatorShown(True)
        self.history_treeWidget.setHeaderLabels(
            ["ID", "Ημερομηνία", "ΔΤΕ", "Σκοπός", "Ενέργειες", "Μετρητής", "Επ.Service"])
        self.history_treeWidget.headerItem().setTextAlignment(2, QtCore.Qt.AlignCenter)
        self.history_treeWidget.header().setStyleSheet(u"background-color: rgb(203, 203, 203);" "color: black;"
                                                       "font-style: normal;font-size: 12pt;font-weight: bold;")
        self.history_treeWidget.itemClicked.connect(self.history_clicked)
        self.history_treeWidget.itemDoubleClicked.connect(self.show_edit_service_window)
        self.gridLayout_4.addWidget(self.history_treeWidget, 4, 0, 1, 6)

        # Add history maintenance προσθήκη συντήρησης
        self.add_maintenance_toolButton = QtWidgets.QToolButton(self.history_tab)
        self.add_maintenance_toolButton.setFont(self.font_12_bold)
        self.add_maintenance_toolButton.setStatusTip("")
        self.add_maintenance_toolButton.setWhatsThis("")
        self.add_maintenance_toolButton.setAccessibleName("")
        self.add_maintenance_toolButton.setAccessibleDescription("")
        self.add_maintenance_toolButton.setStyleSheet("background-color: rgb(113, 113, 113);\n"
                                                      "color: rgb(255, 255, 255);")
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap("icons/add_service.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.add_maintenance_toolButton.setIcon(icon7)
        self.add_maintenance_toolButton.setIconSize(QtCore.QSize(30, 30))
        # self.add_maintenance_toolButton.setShortcut("")
        self.add_maintenance_toolButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.add_maintenance_toolButton.setObjectName("add_maintenance_toolButton")
        self.add_maintenance_toolButton.clicked.connect(self.show_add_service_window)
        self.gridLayout_4.addWidget(self.add_maintenance_toolButton, 5, 0, 1, 1)

        # Προβολή ανοιχτής κλήσης απο το επιλεγμένο μηχάνημα
        self.view_open_task_toolButton = QtWidgets.QToolButton(self.history_tab)
        self.view_open_task_toolButton.setFont(self.font_12_bold)
        self.view_open_task_toolButton.setStyleSheet("background-color: rgb(0, 0, 220);\n"
                                                      "color: rgb(255, 255, 255);")
        view_task_icon = QtGui.QIcon()
        view_task_icon.addPixmap(QtGui.QPixmap("icons/add_scheduled_tasks.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.view_open_task_toolButton.setIcon(view_task_icon)
        self.view_open_task_toolButton.setIconSize(QtCore.QSize(30, 30))
        # self.add_maintenance_toolButton.setShortcut("")
        self.view_open_task_toolButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.view_open_task_toolButton.setObjectName("add_maintenance_toolButton")
        self.view_open_task_toolButton.hide()
        self.view_open_task_toolButton.clicked.connect(self.view_selected_machine_open_task)
        self.gridLayout_4.addWidget(self.view_open_task_toolButton, 5, 4, 1, 1)

        # --------------------------------------------- Ανταλλακτικά πελάτη Tab ----------------------
        self.consumables_tab = QtWidgets.QWidget()
        self.consumables_tab.setObjectName("consumables_tab")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.consumables_tab)
        self.gridLayout_5.setObjectName("gridLayout_5")

        # Search ανταλλακτικα πελάτη
        self.search_consumable_lineEdit = QtWidgets.QLineEdit(self.consumables_tab)
        self.search_consumable_lineEdit.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.search_consumable_lineEdit.sizePolicy().hasHeightForWidth())
        self.search_consumable_lineEdit.setSizePolicy(sizePolicy)
        self.search_consumable_lineEdit.setMinimumSize(QtCore.QSize(0, 30))
        self.search_consumable_lineEdit.setFont(self.font_12)
        self.search_consumable_lineEdit.setObjectName("search_consumable_lineEdit")
        self.search_consumable_lineEdit.returnPressed.connect(self.search_on_customer_consumables)
        self.gridLayout_5.addWidget(self.search_consumable_lineEdit, 0, 2, 1, 1)
        self.search_consumable_toolButton = QtWidgets.QToolButton(self.consumables_tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.search_consumable_toolButton.sizePolicy().hasHeightForWidth())
        self.search_consumable_toolButton.setSizePolicy(sizePolicy)
        self.search_consumable_toolButton.setFont(self.font_12_bold)
        self.search_consumable_toolButton.setStyleSheet("background-color: rgb(173, 173, 173);\n"
                                                        "color: rgb(255, 255, 255);")
        self.search_consumable_toolButton.setIcon(self.search_tasks_icon)
        self.search_consumable_toolButton.setIconSize(QtCore.QSize(30, 30))
        self.search_consumable_toolButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.search_consumable_toolButton.setObjectName("search_consumable_toolButton")
        self.search_consumable_toolButton.clicked.connect(self.search_on_customer_consumables)
        self.gridLayout_5.addWidget(self.search_consumable_toolButton, 0, 3, 1, 1)

        # Κουμπί εμφάνησεις ανταλλακτικών
        self.show_selected_customer_consumables_toolButton = QtWidgets.QToolButton(self.consumables_tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.show_selected_customer_consumables_toolButton.sizePolicy().hasHeightForWidth())
        self.show_selected_customer_consumables_toolButton.setSizePolicy(sizePolicy)
        self.show_selected_customer_consumables_toolButton.setFont(self.font_12_bold)
        self.show_selected_customer_consumables_toolButton.setStyleSheet("background-color: rgb(173, 173, 173);\n"
                                                        "color: rgb(255, 255, 255);")
        self.show_selected_customer_consumables_toolButton.setIcon(self.show_consumables_icon)
        self.show_selected_customer_consumables_toolButton.setIconSize(QtCore.QSize(30, 30))
        self.show_selected_customer_consumables_toolButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.show_selected_customer_consumables_toolButton.setObjectName("show_selected_customer_consumables_toolButton")
        self.show_selected_customer_consumables_toolButton.clicked.connect(self.show_selected_customer_consumables)
        self.gridLayout_5.addWidget(self.show_selected_customer_consumables_toolButton, 0, 0, 1, 1)

        # Customer consumables treewidget
        self.consumables_treeWidget = QtWidgets.QTreeWidget(self.consumables_tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding,
                                           QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.consumables_treeWidget.sizePolicy().hasHeightForWidth())
        self.consumables_treeWidget.setSizePolicy(sizePolicy)
        self.consumables_treeWidget.setFont(self.font_12)
        self.consumables_treeWidget.setAlternatingRowColors(True)
        self.consumables_treeWidget.setWordWrap(True)
        self.consumables_treeWidget.setObjectName("consumables_treeWidget")
        self.consumables_treeWidget.setHeaderLabels(["ID", "ΔΤΕ", "Ημερομηνία", "Κωδικός", "Τεμάχια", "Προϊόν", "Σημειώσεις"])
        self.consumables_treeWidget.headerItem().setTextAlignment(3, QtCore.Qt.AlignCenter)
        self.consumables_treeWidget.headerItem().setTextAlignment(4, QtCore.Qt.AlignCenter)
        self.consumables_treeWidget.header().setStyleSheet(u"background-color: rgb(203, 203, 203);" "color: black;"
                                                           "font-style: normal;font-size: 12pt;font-weight: bold;")
        self.consumables_treeWidget.setSortingEnabled(True)
        self.consumables_treeWidget.itemDoubleClicked.connect(self.show_edit_spare_part_window)
        self.gridLayout_5.addWidget(self.consumables_treeWidget, 1, 0, 1, 4)

        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap("icons/spare_parts.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tabWidget.addTab(self.consumables_tab, icon9, "")

        # ------------------------------------------ Αποθήκη Tab---------------------------------
        self.store_tab = QtWidgets.QWidget()
        self.store_tab.setFont(self.font_12)
        self.store_tab.setObjectName("store_tab")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.store_tab)
        self.gridLayout_6.setObjectName("gridLayout_6")

        # Αποθήκη Εταιρεία
        self.companies_label = QtWidgets.QLabel(self.store_tab)
        self.companies_label.setFont(self.font_12_bold)
        self.companies_label.setAlignment(QtCore.Qt.AlignCenter)
        self.companies_label.setObjectName("companies_label")
        self.gridLayout_6.addWidget(self.companies_label, 0, 0, 1, 1)
        self.companies_comboBox = QtWidgets.QComboBox(self.store_tab)
        self.companies_comboBox.setObjectName("companies_comboBox")
        for table in store_tables:
            self.companies_comboBox.addItem(table.__tablename__)
        self.companies_comboBox.currentIndexChanged.connect(self.show_selected_store_table)
        self.gridLayout_6.addWidget(self.companies_comboBox, 1, 0, 1, 2)

        # Αποθήκη Treewidget
        self.store_treeWidget = QtWidgets.QTreeWidget(self.store_tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.store_treeWidget.sizePolicy().hasHeightForWidth())
        self.store_treeWidget.setSizePolicy(sizePolicy)
        self.store_treeWidget.setFont(self.font_12)
        self.store_treeWidget.setAutoFillBackground(False)
        self.store_treeWidget.setWordWrap(True)
        self.store_treeWidget.setObjectName("store_treeWidget")
        self.store_treeWidget.headerItem().setText(0, "ID")
        self.store_treeWidget.headerItem().setTextAlignment(0, QtCore.Qt.AlignCenter)
        self.store_treeWidget.headerItem().setFont(0, self.font_12_bold)
        self.store_treeWidget.headerItem().setBackground(0, QtGui.QColor(203, 203, 203))
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        self.store_treeWidget.headerItem().setForeground(0, brush)
        self.store_treeWidget.headerItem().setText(1, "Part No")
        self.store_treeWidget.headerItem().setTextAlignment(1, QtCore.Qt.AlignCenter)
        self.store_treeWidget.headerItem().setFont(1, self.font_12_bold)
        self.store_treeWidget.headerItem().setBackground(1, QtGui.QColor(203, 203, 203))
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        self.store_treeWidget.headerItem().setForeground(1, brush)
        self.store_treeWidget.headerItem().setText(2, "Κωδικός")
        self.store_treeWidget.headerItem().setTextAlignment(2, QtCore.Qt.AlignCenter)
        self.store_treeWidget.headerItem().setFont(2, self.font_12_bold)
        self.store_treeWidget.headerItem().setBackground(2, QtGui.QColor(203, 203, 203))
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        self.store_treeWidget.headerItem().setForeground(2, brush)
        self.store_treeWidget.headerItem().setText(3, "Τεμάχια")
        self.store_treeWidget.headerItem().setTextAlignment(3, QtCore.Qt.AlignCenter)
        self.store_treeWidget.headerItem().setFont(3, self.font_12_bold)
        self.store_treeWidget.headerItem().setBackground(3, QtGui.QColor(203, 203, 203))
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        self.store_treeWidget.headerItem().setForeground(3, brush)
        self.store_treeWidget.headerItem().setText(4, "Περιγραφή")
        self.store_treeWidget.headerItem().setTextAlignment(4, QtCore.Qt.AlignCenter)
        self.store_treeWidget.headerItem().setFont(4, self.font_12_bold)
        self.store_treeWidget.headerItem().setBackground(4, QtGui.QColor(203, 203, 203))
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        self.store_treeWidget.headerItem().setForeground(4, brush)
        self.store_treeWidget.setFont(self.font_12)
        self.store_treeWidget.setAlternatingRowColors(True)
        self.store_treeWidget.setSortingEnabled(True)
        self.store_treeWidget.itemDoubleClicked.connect(self.edit_store_items)
        self.gridLayout_6.addWidget(self.store_treeWidget, 2, 0, 1, 5)

        # Search Store Αποθήκη
        self.search_on_store_label = QtWidgets.QLabel(self.store_tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.search_on_store_label.sizePolicy().hasHeightForWidth())
        self.search_on_store_label.setSizePolicy(sizePolicy)
        self.search_on_store_label.setFont(self.font_12_bold)
        self.search_on_store_label.setAlignment(QtCore.Qt.AlignCenter)
        self.search_on_store_label.setObjectName("search_on_store_label")
        self.gridLayout_6.addWidget(self.search_on_store_label, 0, 1, 1, 2)
        self.search_on_store_lineEdit = QtWidgets.QLineEdit(self.store_tab)
        self.search_on_store_lineEdit.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.search_on_store_lineEdit.sizePolicy().hasHeightForWidth())
        self.search_on_store_lineEdit.setSizePolicy(sizePolicy)
        self.search_on_store_lineEdit.setMinimumSize(QtCore.QSize(0, 30))
        self.search_on_store_lineEdit.setFont(self.font_12)
        self.search_on_store_lineEdit.setObjectName("search_on_store_lineEdit")
        self.search_on_store_lineEdit.returnPressed.connect(self.search_on_selected_table_store)
        self.gridLayout_6.addWidget(self.search_on_store_lineEdit, 1, 2, 1, 1)
        self.search_on_store_toolButton = QtWidgets.QToolButton(self.store_tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.search_on_store_toolButton.sizePolicy().hasHeightForWidth())
        self.search_on_store_toolButton.setSizePolicy(sizePolicy)
        self.search_on_store_toolButton.setMaximumSize(QtCore.QSize(30, 30))
        self.search_on_store_toolButton.setFont(self.font_12_bold)
        self.search_on_store_toolButton.setStyleSheet(
            "background-color: rgb(113, 113, 113);\n" "color: rgb(255, 255, 255);")
        self.search_on_store_toolButton.setText("")
        self.search_on_store_toolButton.setIcon(self.search_icon)
        self.search_on_store_toolButton.setIconSize(QtCore.QSize(30, 30))
        self.search_on_store_toolButton.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.search_on_store_toolButton.setObjectName("search_on_store_toolButton")
        self.search_on_store_toolButton.clicked.connect(self.search_on_selected_table_store)
        self.gridLayout_6.addWidget(self.search_on_store_toolButton, 1, 3, 1, 1)

        # Προσθήκη στην Αποθήκη
        # self.add_item_to_company_toolButton = QtWidgets.QToolButton(self.store_tab)
        # sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        # sizePolicy.setHorizontalStretch(0)
        # sizePolicy.setVerticalStretch(0)
        # sizePolicy.setHeightForWidth(self.add_item_to_company_toolButton.sizePolicy().hasHeightForWidth())
        # self.add_item_to_company_toolButton.setSizePolicy(sizePolicy)
        # self.add_item_to_company_toolButton.setFont(self.font_12_bold)
        # self.add_item_to_company_toolButton.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        # self.add_item_to_company_toolButton.setLayoutDirection(QtCore.Qt.LeftToRight)
        # self.add_item_to_company_toolButton.setAutoFillBackground(False)
        # self.add_item_to_company_toolButton.setStyleSheet(
        #     "background-color: rgb(104, 104, 104);\n" "color: rgb(255, 255, 255);")
        # self.add_item_to_company_toolButton.setIcon(self.add_spare_part_icon)
        # self.add_item_to_company_toolButton.setIconSize(QtCore.QSize(30, 30))
        # # self.add_item_to_company_toolButton.setShortcut("")
        # self.add_item_to_company_toolButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        # self.add_item_to_company_toolButton.setObjectName("add_item_to_company_toolButton")
        # self.gridLayout_6.addWidget(self.add_item_to_company_toolButton, 3, 0, 1, 1)

        self.tabWidget.addTab(self.store_tab, self.store_icon, "")
        self.gridLayout_3.addWidget(self.tabWidget, 0, 4, 5, 11)

        # -------------------------------------------MENU--------------------------------
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setFont(self.font_12_bold)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1213, 21))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        self.menu.setFont(self.font_12_bold)

        self.menu_2 = QtWidgets.QMenu(self.menubar)
        self.menu_2.setObjectName("menu_2")
        self.menu_2.setFont(self.font_12_bold)

        self.menuBackup = QtWidgets.QMenu(self.menubar)
        self.menuBackup.setObjectName("menuBackup")
        self.menuBackup.setFont(self.font_12_bold)

        self.menu_3 = QtWidgets.QMenu(self.menubar)
        self.menu_3.setObjectName("menu_3")
        self.menu_3.setFont(self.font_12_bold)

        self.menuInfo = QtWidgets.QMenu(self.menubar)
        self.menuInfo.setObjectName("menuInfo")
        self.menuInfo.setFont(self.font_12_bold)

        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        self.statusbar.setFont(self.font_12_bold)
        MainWindow.setStatusBar(self.statusbar)

        # Προσθήκη πελάτη
        self.menu_add_customer_f1 = QtWidgets.QAction(MainWindow)
        self.menu_add_customer_f1.setObjectName("menu_add_customer_f1")
        self.menu_add_customer_f1.setFont(self.font_12)
        self.menu_add_customer_f1.triggered.connect(self.show_add_new_customer_window)
        # Keys  F1
        self.shortcut_f1 = QtWidgets.QShortcut(QtGui.QKeySequence('F1'), self.centralwidget)
        self.shortcut_f1.activated.connect(self.show_add_new_customer_window)

        # Key F3
        self.shortcut_f3 = QtWidgets.QShortcut(QtGui.QKeySequence('F3'), self.centralwidget)
        self.shortcut_f3.activated.connect(self.show_add_task_window)

        # Ενεργοποίηση πελάτη
        self.menu_enable_customer = QtWidgets.QAction(MainWindow)
        self.menu_enable_customer.setObjectName("menu_enable_customer")
        self.menu_enable_customer.triggered.connect(self.show_enable_customer_window)
        self.menu_enable_customer.setFont(self.font_12)

        # Exit quit εξωδος
        self.menu_exit = QtWidgets.QAction(MainWindow)
        self.menu_exit.setObjectName("menu_exit")
        self.menu_exit.setFont(self.font_12)
        self.menu_exit.triggered.connect(self.quit)

        # Προσθήκη μηχανήματος
        self.menu_add_machine_f2 = QtWidgets.QAction(MainWindow)
        self.menu_add_machine_f2.setObjectName("menu_add_machine_f2")
        self.menu_add_machine_f2.setFont(self.font_12)
        self.menu_add_machine_f2.triggered.connect(self.show_add_new_machine_window)
        # Key F2
        self.shortcut_f2 = QtWidgets.QShortcut(QtGui.QKeySequence('F2'), self.centralwidget)
        self.shortcut_f2.activated.connect(self.show_add_new_machine_window)

        # Μεταφορά μηχανήματος
        # self.menu_transport_machine = QtWidgets.QAction(MainWindow)
        # self.menu_transport_machine.setObjectName("menu_transport_machine")
        # self.menu_transport_machine.setFont(self.font_12)
        # self.menu_transport_machine.triggered.connect(self.show_transfer_machine_window)

        # Ενεργοποιήση μηχανήματος
        self.menu_enable_machine = QtWidgets.QAction(MainWindow)
        self.menu_enable_machine.setObjectName("menu_enable_machine")
        self.menu_enable_machine.triggered.connect(self.show_enable_machine_window)
        self.menu_enable_machine.setFont(self.font_12)

        # Ιστορικό μεταφορών
        self.menu_history_of_transports = QtWidgets.QAction(MainWindow)
        self.menu_history_of_transports.setObjectName("menu_history_of_transports")
        self.menu_history_of_transports.setFont(self.font_12)
        self.menu_history_of_transports.triggered.connect(self.show_transfers_logs_window)

        # Backup Service Book
        self.menu_Backup_Service_Book = QtWidgets.QAction(MainWindow)
        self.menu_Backup_Service_Book.setObjectName("menu_Backup_Service_Book")
        self.menu_Backup_Service_Book.setFont(self.font_12)
        self.menu_Backup_Service_Book.triggered.connect(backup_service_book)

        # Backup Αποθήκη store
        self.menu_backup_store_db = QtWidgets.QAction(MainWindow)
        self.menu_backup_store_db.setObjectName("menu_backup_store_db")
        self.menu_backup_store_db.setFont(self.font_12)
        self.menu_backup_store_db.triggered.connect(backup_store)

        # Export to Excel
        self.menu_export_to_excel = QtWidgets.QAction(MainWindow)
        self.menu_export_to_excel.setObjectName("menu_export_to_excel")
        self.menu_export_to_excel.setFont(self.font_12)
        self.menu_export_to_excel.triggered.connect(to_excel)

        # Email settings
        self.menu_email_settings = QtWidgets.QAction(MainWindow)
        self.menu_email_settings.setObjectName("menu_email_settings")
        self.menu_email_settings.setFont(self.font_12)
        self.menu_email_settings.triggered.connect(self.show_edit_email_settings_window)

        # Edit data
        self.menu_edit_data = QtWidgets.QAction(MainWindow)
        self.menu_edit_data.setObjectName("menu_edit_data")
        self.menu_edit_data.setFont(self.font_12)
        self.menu_edit_data.triggered.connect(self.show_edit_service_data_window)

        # Info Πληροφορίες σχετικά
        self.menu_info = QtWidgets.QAction(MainWindow)
        self.menu_info.setObjectName("menu_info")
        self.menu_info.setFont(self.font_12)
        self.menu_info.triggered.connect(self.info)

        # Υποστίρικη support
        self.menu_support = QtWidgets.QAction(MainWindow)
        self.menu_support.setObjectName("menu_support")
        self.menu_support.setFont(self.font_12)
        self.menu_support.triggered.connect(self.show_activation_window)


        self.menu.addAction(self.menu_add_customer_f1)
        self.menu.addAction(self.menu_enable_customer)
        self.menu.addSeparator()
        self.menu.addAction(self.menu_exit)
        self.menu_2.addAction(self.menu_add_machine_f2)
        # self.menu_2.addAction(self.menu_transport_machine)
        self.menu_2.addAction(self.menu_enable_machine)
        self.menu_2.addAction(self.menu_history_of_transports)
        self.menuBackup.addAction(self.menu_Backup_Service_Book)
        self.menuBackup.addAction(self.menu_backup_store_db)
        self.menuBackup.addAction(self.menu_export_to_excel)
        self.menu_3.addAction(self.menu_email_settings)
        self.menu_3.addAction(self.menu_edit_data)
        self.menuInfo.addAction(self.menu_info)
        self.menuInfo.addAction(self.menu_support)
        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())
        self.menubar.addAction(self.menuBackup.menuAction())
        self.menubar.addAction(self.menu_3.menuAction())
        self.menubar.addAction(self.menuInfo.menuAction())
        # Συντομέυσεις shortcuts
        # Keys  F1
        # self.shortcut_f1 = QtWidgets.QShortcut(QtGui.QKeySequence('F1'), self.centralwidget)
        # self.shortcut_f1.activated.connect(self.add_spare_part)
        # # Key F3
        # self.shortcut_f3 = QtWidgets.QShortcut(QtGui.QKeySequence('F3'), self.centralwidget)
        # self.shortcut_f3.activated.connect(self.show_edit_from_menu_or_F3)

        # Esc
        self.shortcut_esc = QtWidgets.QShortcut(QtGui.QKeySequence('Escape'), self.centralwidget)
        self.shortcut_esc.activated.connect(self.quit)

        # F5
        self.shortcut_f5 = QtWidgets.QShortcut(QtGui.QKeySequence('F5'), self.centralwidget)
        self.shortcut_f5.activated.connect(lambda: (self.refresh_customers(), self.refresh_active_machines()))

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # Show Data
        self.show_active_customers()
        self.show_active_machines()
        self.show_active_tasks()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", f"Service Book {VERSION}"))
        self.customers_label.setText(_translate("MainWindow", "Πελατολόγιο"))
        self.tasks_treeWidget.setSortingEnabled(True)
        self.search_on_tasks_label.setText(_translate("MainWindow", "Αναζήτηση"))
        self.tasks_label.setText(_translate("MainWindow", "Ημερολόγιο εργασίων"))
        self.machines_label.setText(_translate("MainWindow", " Μηχανήματα"))
        self.search_dte_on_tasks_toolButton.setText(_translate("MainWindow", "..."))
        self.search_dte_on_service_toolButton.setText(_translate("MainWindow", "..."))
        self.search_customer_toolButton.setText(_translate("MainWindow", "Αναζήτηση"))
        self.finished_tasks_label.setText(_translate("MainWindow", "Ολοκληρωμένες κλήσεις"))
        self.area_label.setText(_translate("MainWindow", "Περιοχή"))
        self.responsible_label.setText(_translate("MainWindow", "Υπεύθυνος"))
        self.customer_notes_label.setText(_translate("MainWindow", "Σημειώσεις"))
        self.phone_label.setText(_translate("MainWindow", "Τηλέφωνο"))
        self.customer_name_label.setText(_translate("MainWindow", "Επωνυμία"))
        self.fax_label.setText(_translate("MainWindow", "FAX"))
        self.save_customer_changes_toolButton.setText(_translate("MainWindow", "  Αποθήκευση αλλαγών"))
        # self.save_customer_changes_toolButton.setShortcut(_translate("MainWindow", "Ctrl+S"))
        self.post_code_label.setText(_translate("MainWindow", "Τ.Κ."))
        self.address_label.setText(_translate("MainWindow", "Διεύθυνση"))
        self.mobile_label.setText(_translate("MainWindow", "Κινητό"))
        self.city_label.setText(_translate("MainWindow", "Πόλη"))
        self.email_label.setText(_translate("MainWindow", "E-mail"))
        self.disable_customer_toolButton.setText(_translate("MainWindow", "  Απενεργοποίηση"))
        self.copier_notes_label.setText(_translate("MainWindow", "Σημειώσεις"))
        self.serial_number_label.setText(_translate("MainWindow", "Σειριακός αριθμός"))
        self.copier_model_label.setText(_translate("MainWindow", "Εταιρεία - Μοντέλο"))
        self.start_date_label.setText(_translate("MainWindow", "Ημηρομηνία  έναρξης"))
        self.start_counter_label.setText(_translate("MainWindow", "Μετρητής έναρξης"))
        # self.transport_machine_label.setText(_translate("MainWindow", "ΜΕΤΑΦΟΡΑ ΣΕ ΝΕΟ ΠΕΛΑΤΗ"))
        self.transport_machine_toolButton.setText(_translate("MainWindow", "   Μεταφορά"))
        self.save_copier_changes_toolButton.setText(_translate("MainWindow", "  Αποθήκευση αλλαγών"))
        self.disable_copier_toolButton.setText(_translate("MainWindow", "  Απενεργοποίηση"))
        self.add_maintenance_toolButton.setText(_translate("MainWindow", "  Προσθήκη συντήρησης"))
        self.view_open_task_toolButton.setText(_translate("MainWindow", "  Ανοιχτή κλήση"))
        self.search_maintenance_label.setText(_translate("MainWindow", "Αναζήτηση συντήρησης"))
        self.search_errors_toolButton.setText(_translate("MainWindow", "..."))
        self.search_maintenance_toolButton.setText(_translate("MainWindow", "..."))
        self.search_errors_label.setText(_translate("MainWindow", "Αναζήτηση σφαλμάτων"))
        self.search_consumable_toolButton.setText(_translate("MainWindow", "  Αναζήτηση"))
        self.show_selected_customer_consumables_toolButton.setText(_translate("MainWindow", "  Εμφάνησει ανταλλακτικών"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.consumables_tab),
                                  _translate("MainWindow", "Ανταλλακτικά"))
        self.companies_label.setText(_translate("MainWindow", "Εταιρεία"))
        self.search_on_store_label.setText(_translate("MainWindow", "Αναζήτηση"))
        # self.add_item_to_company_toolButton.setText(_translate("MainWindow", "  Προσθήκη ανταλλακτικού"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.store_tab), _translate("MainWindow", "Αποθήκη"))
        self.add_task_toolButton.setText(_translate("MainWindow", "  Προσθήκη εργασίας"))
        self.menu.setTitle(_translate("MainWindow", "Πελάτες"))
        self.menu_2.setTitle(_translate("MainWindow", "Μηχανήματα"))
        self.menuBackup.setTitle(_translate("MainWindow", "Backup"))
        self.menu_3.setTitle(_translate("MainWindow", "Ρυθμίσεις"))
        self.menuInfo.setTitle(_translate("MainWindow", "Info"))
        self.menu_add_customer_f1.setText(_translate("MainWindow", "Προσθήκη Πελάτη  F1"))
        self.menu_enable_customer.setText(_translate("MainWindow", "Ενεργοποιήση Πελατών"))
        self.menu_exit.setText(_translate("MainWindow", "Εξωδος   Esc"))
        self.menu_add_machine_f2.setText(_translate("MainWindow", "Προσθήκη Μηχανήματος  F2"))
        # self.menu_transport_machine.setText(_translate("MainWindow", "Μεταφορά Μηχανήματος"))
        self.menu_enable_machine.setText(_translate("MainWindow", "Ενεργοποιήση Μηχανήματος"))
        self.menu_history_of_transports.setText(_translate("MainWindow", "Ιστορικό Μεταφορών"))
        self.menu_Backup_Service_Book.setText(_translate("MainWindow", "Backup Service Book"))
        self.menu_backup_store_db.setText(_translate("MainWindow", "Backup Αποθήκη"))
        self.menu_export_to_excel.setText(_translate("MainWindow", "Εξαγωγή σε Excel"))
        self.menu_email_settings.setText(_translate("MainWindow", "Ρυθμίσεις Email"))
        self.menu_edit_data.setText(_translate("MainWindow", "Ρυθμίσεις Δεδομένων"))
        self.menu_info.setText(_translate("MainWindow", "Πληροφορίες"))
        self.menu_support.setText(_translate("MainWindow", "Υποστήριξη"))

    def show_active_customers(self):
        """
        Εμφάνιση μόνο ενεργών πελατών
          καλείτε
          1. στην αρχή της εφαρμογής
          2. οταν κανουμε refresh
        Οταν επιλέγουμε πελάτη να αδειαζει τα δεδομένα απο την καρτέλα μηχάνημα γιατι
        # δεν έχουμε επιλέξει ακόμα μηχάνημα και εχει το μηχάνημα απο την προηγούμενη επιλογή
        :return:
        """
        # αποκρυψη κουμπή ανοιχτής κλήσης
        self.view_open_task_toolButton.hide()
        self.selected_machine = None
        # treeWidget
        self.customers_treeWidget.clear()
        self.active_customers = fetch_active_customers()
        # Completer
        customers_names = [customer.Επωνυμία_Επιχείρησης for customer in self.active_customers]
        customers_phones = [customer.Τηλέφωνο for customer in self.active_customers]
        customers_mobiles = [customer.Κινητό for customer in self.active_customers]
        customers_details = customers_names + customers_phones + customers_mobiles
        self.customers_completer = QtWidgets.QCompleter(customers_details)
        self.customers_completer.popup().setFont(self.font_12)
        self.search_customer_lineEdit.setCompleter(self.customers_completer)
        # Ενημέρωση το πεδίο νέος πελάτης στην καρτέλα μηχάνημα
        # self.new_customer_combobox.addItems(customers_names)
        # self.new_customer_completer = QtWidgets.QCompleter(customers_names)
        # self.new_customer_lineEdit.setCompleter(self.new_customer_completer)
        # self.new_customer_combobox.setLineEdit(self.new_customer_lineEdit)

        for index, item in enumerate(self.active_customers):
            if item.Κατάσταση:  # Αν είναι ενεργός
                self.active_customer_item = QtWidgets.QTreeWidgetItem(self.customers_treeWidget,
                                                                      [str(item.ID), str(item.Επωνυμία_Επιχείρησης)])
                self.active_customer_item.setTextAlignment(0, QtCore.Qt.AlignLeft)
                self.customers_treeWidget.setStyleSheet("QTreeView::item { padding: 11px }")
                self.customers_treeWidget.addTopLevelItem(self.active_customer_item)

        self.customers_treeWidget.setColumnWidth(0, 1)
        # self.customers_treeWidget.resizeColumnToContents(0)
        # self.customers_treeWidget.itemDoubleClicked.connect(self.show_edit_spare_part_window)
        # self.gridLayout.addWidget(self.treeWidget, 11, 0, 1, 10)

    def show_active_machines(self):
        """
        Εμφάνιση μόνο ενεργών μηχανημάτων
          καλείτε
          1. στην αρχή της εφαρμογής
          2. οταν κανουμε refresh
        :return:
        """
        # αποκρυψη κουμπή ανοιχτής κλήσης
        self.view_open_task_toolButton.hide()
        self.machines_treeWidget.clear()
        self.active_machines = fetch_active_machines()
        # Completer
        machine_names = [machine.Εταιρεία for machine in self.active_machines]
        machine_serial = [machine.Serial for machine in self.active_machines]
        machine_details = machine_names + machine_serial
        self.machine_completer = QtWidgets.QCompleter(machine_details)
        self.machine_completer.popup().setFont(self.font_12)
        self.search_machine_lineEdit.setCompleter(self.machine_completer)
        # treeWidget
        for index, item in enumerate(self.active_machines):
            self.active_machine_item = QtWidgets.QTreeWidgetItem(self.machines_treeWidget,
                                                                 [str(item.ID), str(item.Εταιρεία)])
            self.active_machine_item.setTextAlignment(1, QtCore.Qt.AlignCenter)
            self.machines_treeWidget.setStyleSheet("QTreeView::item { padding: 5px }")
            self.machines_treeWidget.addTopLevelItem(self.active_machine_item)

        self.machines_treeWidget.setColumnWidth(0, 1)
        self.machines_treeWidget.sortByColumn(1, QtCore.Qt.AscendingOrder)
        # self.customers_treeWidget.resizeColumnToContents(0)
        # self.machines_treeWidget.itemClicked.connect(self.show_edit_spare_part_window)

    def show_selected_customer_consumables(self):
        """
        Εμφάνιση μόνο ανταλλακτικών επιλεγμένου πελάτη
          καλείτε
          1. οταν επιλέγουμε πελάτη customer_clicked()
          2. οταν επιλέγουμε μηχάνημα machine_clicked()
          3. οταν κανουμε refresh refresh_consumables()

        :return:
        """
        try:
            self.consumables_treeWidget.clear()  # Καθαρισμός λίστας
            for item in self.selected_customer.consumables:
                try:
                    item_DTE = item.service.ΔΤΕ
                except AttributeError:  # 'NoneType' object has no attribute 'ΔΤΕ' όταν το service.ID ειναι 0
                    item_DTE = get_DTE_from_calendar_id(item.Calendar_ID)
                self.selected_customer_consumable_item = TreeWidgetItem(self.consumables_treeWidget,
                                                                                   [str(item.ID), str(item_DTE),
                                                                                    str(item.service.Ημερομηνία),
                                                                                    str(item.ΚΩΔΙΚΟΣ),
                                                                                    str(item.ΤΕΜΑΧΙΑ),
                                                                                    str(item.ΠΕΡΙΓΡΑΦΗ),
                                                                                    str(item.ΠΑΡΑΤΗΡΗΣΗΣ)])
                self.selected_customer_consumable_item.setData(2, QtCore.Qt.DisplayRole,
                                                               QtCore.QDate.fromString(item.service.Ημερομηνία,
                                                                                       "dd'/'MM'/'yyyy"))
                self.selected_customer_consumable_item.setTextAlignment(3, QtCore.Qt.AlignCenter)
                self.selected_customer_consumable_item.setTextAlignment(4, QtCore.Qt.AlignCenter)

                self.consumables_treeWidget.setStyleSheet("QTreeView::item { padding: 5px }")
                # Χρωματισμός πεδίων
                if "C/M/Y" in item.ΠΕΡΙΓΡΑΦΗ:
                    self.selected_customer_consumable_item.setBackground(5, QtGui.QColor('green'))
                    self.selected_customer_consumable_item.setForeground(5, QtGui.QColor('white'))
                elif "CYAN" in item.ΠΕΡΙΓΡΑΦΗ:
                    self.selected_customer_consumable_item.setBackground(5, QtGui.QColor('#0517D2'))
                    self.selected_customer_consumable_item.setForeground(5, QtGui.QColor('white'))
                elif "MAGENTA" in item.ΠΕΡΙΓΡΑΦΗ:
                    self.selected_customer_consumable_item.setBackground(5, QtGui.QColor('#D205CF'))
                    self.selected_customer_consumable_item.setForeground(5, QtGui.QColor('white'))
                elif "YELLOW" in item.ΠΕΡΙΓΡΑΦΗ:
                    self.selected_customer_consumable_item.setBackground(5, QtGui.QColor('yellow'))
                    self.selected_customer_consumable_item.setForeground(5, QtGui.QColor('black'))
                elif "GRAY" in item.ΠΕΡΙΓΡΑΦΗ:
                    self.selected_customer_consumable_item.setBackground(5, QtGui.QColor("gray"))
                    self.selected_customer_consumable_item.setForeground(5, QtGui.QColor('white'))
                elif "BLACK" in item.ΠΕΡΙΓΡΑΦΗ:
                    self.selected_customer_consumable_item.setBackground(5, QtGui.QColor("black"))
                    self.selected_customer_consumable_item.setForeground(5, QtGui.QColor('white'))

                self.consumables_treeWidget.addTopLevelItem(self.selected_customer_consumable_item)
                self.consumables_treeWidget.resizeColumnToContents(4)

            self.consumables_treeWidget.setColumnWidth(0, 1)
            self.consumables_treeWidget.setColumnWidth(1, 80)
            self.consumables_treeWidget.setColumnWidth(2, 110)
            self.consumables_treeWidget.setColumnWidth(3, 80)
            self.consumables_treeWidget.setColumnWidth(4, 80)
            self.consumables_treeWidget.setColumnWidth(5, 350)
            self.consumables_treeWidget.sortByColumn(2, QtCore.Qt.DescendingOrder)
        except AttributeError:  # 'NoneType' object has no attribute 'consumables' --> οταν δεν έχουμε επιλέξει πελάτη
            return

    def show_selected_customer_machines(self):
        """
        Εμφάνιση μονο μηχανημάτων πελάτη
        καλείτε
          1. οταν επιλέγουμε πελάτη customer_clicked()
          2. οταν επιλέγουμε ιστορικό service history_clicked()
        :return:
        """
        self.machines_treeWidget.clear()  # Καθαρισμός λίστας
        self.selected_customer_machines = self.selected_customer.machines
        # Completer
        machine_names = [machine.Εταιρεία for machine in self.selected_customer.machines]
        machine_serial = [machine.Serial for machine in self.selected_customer.machines]
        machine_details = machine_names + machine_serial
        self.machine_completer = QtWidgets.QCompleter(machine_details)
        self.machine_completer.popup().setFont(self.font_12)
        self.search_machine_lineEdit.setCompleter(self.machine_completer)

        # machines treeWidget
        for item in self.selected_customer_machines:
            if item.Κατάσταση:  # Αν είναι ενεργά και όχι απενεργοποιημένα
                self.selected_customer_machine_item = QtWidgets.QTreeWidgetItem(self.machines_treeWidget,
                                                                                [str(item.ID), str(item.Εταιρεία)])
                self.selected_customer_machine_item.setTextAlignment(1, QtCore.Qt.AlignCenter)
                self.machines_treeWidget.setStyleSheet("QTreeView::item { padding: 5px }")
                self.machines_treeWidget.addTopLevelItem(self.selected_customer_machine_item)
        self.machines_treeWidget.sortByColumn(1, QtCore.Qt.AscendingOrder)
        self.machines_treeWidget.setColumnWidth(0, 1)
        self.machines_treeWidget.itemClicked.connect(self.machine_clicked)

    def show_selected_machine_details_with_history(self):
        """
        Εμφάνιση πεδίων μηχανήματος μαζί με ιστορικό
        καλείτε
          1. οταν επιλέγουμε μηχάνημα machine_clicked()
        :return:
        """
        try:
            self.copier_model_lineEdit.setText(self.selected_machine.Εταιρεία)
            self.serial_number_lineEdit.setText(self.selected_machine.Serial)

            # print(self.selected_machine.Εναρξη)  # 15/12/18
            if QtCore.QDate.isValid(QtCore.QDate.fromString(self.selected_machine.Εναρξη, "dd'/'MM'/'yyyy")):

                self.started_date_dateEdit.setDate(QtCore.QDate.fromString(self.selected_machine.Εναρξη, "dd'/'MM'/'yyyy"))
            else:
                self.started_date_dateEdit.setDate(QtCore.QDate(1979, 1, 1))
            self.start_counter_lineEdit.setText(self.selected_machine.Μετρητής_έναρξης)
            self.copiers_notes_textEdit.setText(self.selected_machine.Σημειώσεις)
            # Εμφάνιση κουμπή ανοιχτής κλήσης
            self.selected_machine_open_tasks = fetch_active_calendar_on_selected_machine(self.selected_machine.ID)
            if self.selected_machine_open_tasks.count() > 0:
                self.view_open_task_toolButton.show()
            else:
                self.view_open_task_toolButton.hide()
            # Εμφάνιση ιστορικού μηχανήματος
            self.history_treeWidget.clear()
            for item in self.selected_machine.service:
                # Ημερομηνία = QtCore.QDate.fromString(item.Ημερομηνία, "dd'/'MM'/'yyyy")
                self.history_item = QtWidgets.QTreeWidgetItem(self.history_treeWidget,
                                                              [str(item.ID), str(item.Ημερομηνία), str(item.ΔΤΕ),
                                                               str(item.Σκοπός_Επίσκεψης), str(item.Ενέργειες),
                                                               str(item.Μετρητής)
                                                                  , str(item.Επ_Service)])
                self.history_item.setData(1, QtCore.Qt.DisplayRole,
                                          QtCore.QDate.fromString(item.Ημερομηνία, "dd'/'MM'/'yyyy"))
                self.history_item.setTextAlignment(1, QtCore.Qt.AlignCenter)
                self.history_item.setTextAlignment(2, QtCore.Qt.AlignCenter)
                self.history_treeWidget.setStyleSheet("QTreeView::item { padding: 5px }")
                self.history_treeWidget.addTopLevelItem(self.history_item)
                self.history_treeWidget.resizeColumnToContents(3)
                self.history_treeWidget.resizeColumnToContents(4)
            self.history_treeWidget.setColumnWidth(0, 1)
            self.history_treeWidget.sortByColumn(1, QtCore.Qt.DescendingOrder)
            self.history_treeWidget.setColumnWidth(2, 50)
            # self.history_treeWidget.setColumnWidth(4, 250)
            # self.history_treeWidget.itemClicked.connect(self.machine_clicked)
        except AttributeError:  # Οταν το μηχάνημα δεν υπάρχει
            pass

    def show_only_selected_customer(self):
        """
        Εμφάνιση μόνο του τον πελάτη απο το μηχάνημα που επιλέξαμε
        και ενημερώνει τα πεδία του πελάτη
            καλείτε
            1. οταν επιλέγουμε μηχάνημα machine_clicked()
            2. οταν επιλέγουμε ιστορικό μηχανήματος history_clicked()
        :return:
        """
        self.customers_treeWidget.clear()
        self.machine_customer_item = QtWidgets.QTreeWidgetItem(self.customers_treeWidget,
                                                               [str(self.selected_customer.ID),
                                                                str(self.selected_customer.Επωνυμία_Επιχείρησης)])
        self.machine_customer_item.setTextAlignment(0, QtCore.Qt.AlignLeft)
        self.customers_treeWidget.setStyleSheet("QTreeView::item { padding: 11px }")
        self.customers_treeWidget.addTopLevelItem(self.machine_customer_item)

        # Εφμάνηση πεδίων πελάτη στο Tab Πελάτης
        # Καρτέλα πελάτη
        self.customer_name_lineEdit.setText(self.selected_machine.Customer.Επωνυμία_Επιχείρησης)
        self.responsible_lineEdit.setText(self.selected_machine.Customer.Ονοματεπώνυμο)
        self.address_lineEdit.setText(self.selected_machine.Customer.Διεύθυνση)
        self.city_lineEdit.setText(self.selected_machine.Customer.Πόλη)
        self.post_code_lineEdit.setText(self.selected_machine.Customer.Ταχ_Κώδικας)
        self.area_lineEdit.setText(self.selected_machine.Customer.Περιοχή)
        self.phone_lineEdit.setText(self.selected_machine.Customer.Τηλέφωνο)
        self.mobile_lineEdit.setText(self.selected_machine.Customer.Κινητό)
        self.fax_lineEdit.setText(self.selected_machine.Customer.Φαξ)
        self.email_lineEdit.setText(self.selected_machine.Customer.E_mail)
        self.customer_notes_textEdit.setText(self.selected_machine.Customer.Σημειώσεις)

    def show_active_tasks(self):
        """
        Εμφάνιση ενεργών κλησεων - εργασιών
            καλείτε
            1. οταν κανουμε refresh search_task() και search_dte()
        :return:
        """
        self.tasks_treeWidget.clear()
        self.active_tasks = fetch_active_calendar()
        # Completer
        tasks_customers = [task.Πελάτης for task in self.active_tasks]
        task_machine = [task.machine.Εταιρεία for task in self.active_tasks]
        task_details = tasks_customers + task_machine
        self.tasks_completer = QtWidgets.QCompleter(task_details)
        self.tasks_completer.popup().setFont(self.font_12)
        self.search_on_tasks_lineEdit.setCompleter(self.tasks_completer)

        self.tasks_treeWidget.setWordWrap(True)
        self.tasks_treeWidget.setAutoFillBackground(True)
        # self.machines_treeWidget.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        # self.treeWidget.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.tasks_treeWidget.setLineWidth(14)
        # self.tasks_treeWidget.setAlternatingRowColors(True)
        self.tasks_treeWidget.setHeaderLabels(["ID", "Ημερομηνία", "ΔΤΕ", "Πελάτης", "Μηχάνημα", "Σκοπός"])
        self.tasks_treeWidget.headerItem().setTextAlignment(0, QtCore.Qt.AlignLeft)
        self.tasks_treeWidget.headerItem().setTextAlignment(1, QtCore.Qt.AlignLeft)
        self.tasks_treeWidget.headerItem().setTextAlignment(2, QtCore.Qt.AlignCenter)
        self.tasks_treeWidget.headerItem().setTextAlignment(3, QtCore.Qt.AlignCenter)
        self.tasks_treeWidget.headerItem().setTextAlignment(4, QtCore.Qt.AlignCenter)
        # self.tasks_treeWidget.headerItem().setFont(2, self.font_12_bold)
        # self.tasks_treeWidget.headerItem().setBackground(2, QtGui.QColor(203, 203, 203))
        # self.treeWidget.setAnimated(True)
        self.tasks_treeWidget.header().setStyleSheet(u"background-color: rgb(203, 203, 203);" "color: black;"
                                                     "font-style: normal;font-size: 12pt;font-weight: bold;")
        for item in self.active_tasks:
            self.active_task_item = QtWidgets.QTreeWidgetItem(self.tasks_treeWidget,
                                                              [str(item.ID), str(item.Ημερομηνία), str(item.ΔΤΕ),
                                                               str(item.machine.Customer.Επωνυμία_Επιχείρησης),
                                                               str(item.machine.Εταιρεία), item.Σκοπός])
            self.active_task_item.setData(1, QtCore.Qt.DisplayRole,
                                          QtCore.QDate.fromString(item.Ημερομηνία, "dd'/'MM'/'yyyy"))
            self.active_task_item.setTextAlignment(2, QtCore.Qt.AlignCenter)
            self.active_task_item.setTextAlignment(3, QtCore.Qt.AlignCenter)
            self.active_task_item.setTextAlignment(4, QtCore.Qt.AlignCenter)
            self.tasks_treeWidget.setStyleSheet("QTreeView::item { padding: 7px }")
            self.tasks_treeWidget.addTopLevelItem(self.active_task_item)
        self.tasks_treeWidget.setColumnWidth(0, 1)
        self.tasks_treeWidget.setColumnWidth(1, 100)
        self.tasks_treeWidget.setColumnWidth(2, 90)
        self.tasks_treeWidget.setColumnWidth(3, 240)
        self.tasks_treeWidget.setColumnWidth(4, 250)
        self.tasks_treeWidget.sortByColumn(1, QtCore.Qt.DescendingOrder)
        # self.tasks_treeWidget.setColumnWidth(3, 200)
        # self.customers_treeWidget.setColumnWidth(0, 0)
        # self.customers_treeWidget.resizeColumnToContents(0)
        # self.customers_treeWidget.itemDoubleClicked.connect(self.show_edit_spare_part_window)
        # self.gridLayout.addWidget(self.treeWidget, 11, 0, 1, 10)

    def customer_clicked(self, item, column, *args):  # column ειναι η στήλη που πατησε κλικ
        """
        0. Απόκρυψη ανταλλακτικών γιατί αργεί πολύ σε πελάτη με πολλά ανταλλακτικά
        1. Εμφάνιση εικονιδίου επιλεγμένου πελάτη
        2. Οταν επιλέγουμε πελάτη να αδειαζει τα δεδομένα απο την καρτέλα μηχάνημα γιατι
           δεν έχουμε επιλέξει ακόμα μηχάνημα και εχει το μηχάνημα απο την προηγούμενη επιλογή
        3. Ενημέρωση Καρτέλας πελάτη
        4. Εμφάνιση μηχανημάτων πελάτη self.show_selected_customer_machines()

            καλείτε
            1. self.customers_treeWidget.itemClicked.connect(self.customer_clicked))
        :return:
        """
        # αποκρυψη κουμπή ανοιχτής κλήσης
        self.view_open_task_toolButton.hide()
        self.consumables_treeWidget.clear()
        item_id = item.text(0)  # item.text(0)  == ID

        self.selected_machine = None
        self.copier_model_lineEdit.setText("")
        self.copiers_notes_textEdit.setText("")
        self.start_counter_lineEdit.setText("")
        self.serial_number_lineEdit.setText("")
        self.started_date_dateEdit.setDate(QtCore.QDate.currentDate())

        try:  # Απόκρψη εικονιδίου επιλεγμένου πελάτη
            if self.selected_customer_treewidget_item:
                self.selected_customer_treewidget_item.setIcon(1, QtGui.QIcon())
                self.selected_customer_treewidget_item.setFont(1, self.font_12)
        except RuntimeError:  # σβήνετε το self.selected_customer_treewidget_item
            pass
        # Εμφάνιση εικονιδίου επιλεγμένου πελάτη
        self.selected_customer_treewidget_item = self.customers_treeWidget.currentItem()
        self.selected_customer_treewidget_item.setFont(1, self.font_12_bold)
        self.selected_customer_treewidget_item.setIcon(1, self.selected_customer_icon)

        self.selected_customer = get_customer_from_id(item_id)
        self.selected_customer_machines = self.selected_customer.machines
        # Καρτέλα πελάτη
        self.customer_name_lineEdit.setText(self.selected_customer.Επωνυμία_Επιχείρησης)
        self.responsible_lineEdit.setText(self.selected_customer.Ονοματεπώνυμο)
        self.address_lineEdit.setText(self.selected_customer.Διεύθυνση)
        self.city_lineEdit.setText(self.selected_customer.Πόλη)
        self.post_code_lineEdit.setText(self.selected_customer.Ταχ_Κώδικας)
        self.area_lineEdit.setText(self.selected_customer.Περιοχή)
        self.phone_lineEdit.setText(self.selected_customer.Τηλέφωνο)
        self.mobile_lineEdit.setText(self.selected_customer.Κινητό)
        self.fax_lineEdit.setText(self.selected_customer.Φαξ)
        self.email_lineEdit.setText(self.selected_customer.E_mail)
        self.customer_notes_textEdit.setText(self.selected_customer.Σημειώσεις)
        # Εμφάνιση μηχανημάτων πελάτη
        self.show_selected_customer_machines()

        # Εμάφνιση ανταλλακτικών --> Αργεί πολύ όταν πελάτης έχει πολλά ανταλλακτικά
        # self.show_selected_customer_consumables()

        self.history_treeWidget.clear()
        # Ενημέρωση status bar
        self.update_status_bar()

    def machine_clicked(self, item, column):
        """
        1. Εμφάνιση εικονιδίου επιλεγμένου μηχανήματος
        2. Εμφάνιση μόνο τον πελάτη απο το μηχάνημα που επιλέξαμε self.show_only_selected_customer()
        3. Εμφάνιση πληροφοριών μηχανήματος self.show_selected_machine_details_with_history()
        4. Εμφάνιση ανταλλακτικών πελάτη self.show_selected_customer_consumables()
            καλείτε
            1. self.machines_treeWidget.itemClicked.connect(self.machine_clicked)
        :return:
        """
        item_id = item.text(0)

        try:
            if self.selected_machine_treewidget_item:
                self.selected_machine_treewidget_item.setIcon(1, QtGui.QIcon())
                self.selected_machine_treewidget_item.setFont(1, self.font_12)
        except RuntimeError:  # σβήνετε το self.selected_machine_treewidget_item
            pass


        self.selected_machine_treewidget_item = self.machines_treeWidget.currentItem()
        self.selected_machine_treewidget_item.setFont(1, self.font_12_bold)
        self.selected_machine_treewidget_item.setIcon(1, self.selected_customer_icon)
        self.selected_machine = get_machines_from_id(item_id)
        # Προβολή κουμπή ειδοποιήσης ανοιχτής κλήσης
        self.selected_machine_open_tasks = fetch_active_calendar_on_selected_machine(self.selected_machine.ID)
        if self.selected_machine_open_tasks.count() > 0:
            self.view_open_task_toolButton.show()
        else:
            self.view_open_task_toolButton.hide()

        self.selected_customer = self.selected_machine.Customer
        # Εμφάνιση μόνο τον πελάτη απο το μηχάνημα που επιλέξαμε
        self.show_only_selected_customer()
        # Εμφάνιση πληροφοριών μηχανήματος
        self.show_selected_machine_details_with_history()

        # Εμφάνιση ανταλλακτικών πελάτη --> αργεί πολύ σε πελάτη με πολλά ανταλλακτικά
        # self.show_selected_customer_consumables()

        # Ενημέρωση status bar
        self.update_status_bar()

    def history_clicked(self, item, column):
        """
        1. Εμφανιση εικονιδίου επιλεγμένου μηχανήματος
        2. Εμφάνιση πεδίων μηχανήματος
        4. Εμφάνιση μονο του τον  πελάτη self.show_only_selected_customer()
            καλείτε
            1. self.history_treeWidget.itemClicked.connect(self.history_clicked)
        :return:
        """

        item_id = item.text(0)
        self.selected_machine = get_machine_from_history(item_id)
        # Αν ο πελάτής του μηχανήματος είναι ιδιος με αυτόν που έχουμε επιλεξει απο πριν
        # να μήν κάνει ξανα ανανέωση την λίστα με τα μηχανήματα γιατι αργει πολύ
        if self.selected_customer == self.selected_machine.Customer:
            return
        self.selected_customer = self.selected_machine.Customer
        self.show_selected_customer_machines()
        # Εμφάνιση μονο μηχανημάτων πελάτη
        # self.show_selected_customer_machines()  # ας μην διχνει τα μηχανήματα του πελάτη γιατι αν ειναι απο αναζήτηση
        # Εικονίδιο στο επιλεγμένο μηχάνημα             χανουμε την αναζήτηση
        items = self.machines_treeWidget.findItems(f"{self.selected_machine.ID}", QtCore.Qt.MatchExactly, 0)

        # items = list
        # try:  # Αν υπάρχει εικονίδιο να το σβήσει για να βάλει στο καινούριο
        #     if self.selected_machine_treewidget_item:
        #         self.selected_machine_treewidget_item.setIcon(1, QtGui.QIcon())
        #         self.selected_machine_treewidget_item.setFont(1, self.font_12)
        # except RuntimeError:  # σβήνετε το self.selected_machine_treewidget_item
        #     pass
        self.selected_machine_treewidget_item = items[0]
        self.selected_machine_treewidget_item.setFont(1, self.font_12_bold)
        self.selected_machine_treewidget_item.setIcon(1, self.selected_customer_icon)
        self.machines_treeWidget.setCurrentItem(items[0])

        # Εμφάνιση πεδίων μηχανήματος
        self.copier_model_lineEdit.setText(self.selected_machine.Εταιρεία)
        self.serial_number_lineEdit.setText(self.selected_machine.Serial)
        # print(self.selected_machine.Εναρξη)  # 15/12/18
        if QtCore.QDate.isValid(QtCore.QDate.fromString(self.selected_machine.Εναρξη, "dd'/'MM'/'yyyy")):

            self.started_date_dateEdit.setDate(QtCore.QDate.fromString(self.selected_machine.Εναρξη, "dd'/'MM'/'yyyy"))
        else:
            self.started_date_dateEdit.setDate(QtCore.QDate(1979, 1, 1))
        self.start_counter_lineEdit.setText(self.selected_machine.Μετρητής_έναρξης)
        self.copiers_notes_textEdit.setText(self.selected_machine.Σημειώσεις)
        self.show_only_selected_customer()
        # Ενημέρωση status bar
        self.update_status_bar()

    def search_customer(self):
        """
           1. self.refresh_customers()
           2. Αναζήτηση στους πελάτες
           3. self.history_treeWidget.clear()
               καλείτε
               1. self.search_customer_lineEdit.returnPressed.connect(self.search_customer)
               2. self.search_customer_toolButton.clicked.connect(self.search_customer)
           :return:
         """
        if self.search_customer_lineEdit.text() == "":
            self.refresh_customers()
            return
        else:
            founded_customers = search_on_customers(self.search_customer_lineEdit.text())
            self.search_customer_lineEdit.setText("")
            self.customers_treeWidget.clear()
            for  item in founded_customers:
                if item.Κατάσταση:  # Αν είναι ενεργός
                    self.founded_customer_item = QtWidgets.QTreeWidgetItem(self.customers_treeWidget,
                                                                           [str(item.ID),
                                                                            str(item.Επωνυμία_Επιχείρησης)])
                    self.founded_customer_item.setTextAlignment(0, QtCore.Qt.AlignLeft)
                    self.customers_treeWidget.setStyleSheet("QTreeView::item { padding: 11px }")
                    self.customers_treeWidget.addTopLevelItem(self.founded_customer_item)

            self.customers_treeWidget.setColumnWidth(0, 1)
        self.history_treeWidget.clear()

    def search_machine(self):
        """
           1. self.refresh_active_machines()
           2. Αναζήτηση στα μηχανήματα
           3. self.history_treeWidget.clear()
               καλείτε
               1. self.search_machine_lineEdit.returnPressed.connect(self.search_machine)
               2. self.search_machine_toolButton.clicked.connect(self.search_machine)
           :return:
         """
        if self.search_machine_lineEdit.text().replace(" ", "") == "" and not self.selected_customer:
            self.refresh_active_machines()
            return
        elif self.selected_customer:  # search_on_selected_customer_machines
            founded_machines = search_on_selected_customer_machines(self.search_machine_lineEdit.text(), self.selected_customer)
            self.search_machine_lineEdit.setText("")
            # treeWidget
            self.machines_treeWidget.clear()
            for item in founded_machines:
                self.founded_machine_item = QtWidgets.QTreeWidgetItem(self.machines_treeWidget,
                                                                      [str(item.ID), str(item.Εταιρεία)])
                self.founded_machine_item.setTextAlignment(1, QtCore.Qt.AlignCenter)
                self.machines_treeWidget.setStyleSheet("QTreeView::item { padding: 5px }")
                self.machines_treeWidget.addTopLevelItem(self.founded_machine_item)
            self.machines_treeWidget.sortByColumn(1, QtCore.Qt.AscendingOrder)
            self.machines_treeWidget.setColumnWidth(0, 1)
        else:
            founded_machines = search_on_machines(self.search_machine_lineEdit.text())
            self.search_machine_lineEdit.setText("")
            # treeWidget
            self.machines_treeWidget.clear()
            for item in founded_machines:
                self.founded_machine_item = QtWidgets.QTreeWidgetItem(self.machines_treeWidget,
                                                                      [str(item.ID), str(item.Εταιρεία)])
                self.founded_machine_item.setTextAlignment(1, QtCore.Qt.AlignCenter)
                self.machines_treeWidget.setStyleSheet("QTreeView::item { padding: 5px }")
                self.machines_treeWidget.addTopLevelItem(self.founded_machine_item)
            self.machines_treeWidget.sortByColumn(1, QtCore.Qt.AscendingOrder)
            self.machines_treeWidget.setColumnWidth(0, 1)
        self.history_treeWidget.clear()

    def search_service(self):
        """
        Ψάχνει στo ιστορικό επηλεγμένου μηχανήματος
        Δεν ψάχνει ΔΤΕ
        καλείτε
            1. self.search_on_tasks_lineEdit.returnPressed.connect(self.search_tasks)
            2. self.search_on_tasks_toolButton.clicked.connect(self.search_tasks)
        :return:
        """
        if self.search_maintenance_lineEdit.text() == "":
            self.show_selected_machine_details_with_history()
            return
        if self.selected_machine == None:
            QtWidgets.QMessageBox.warning(None, "Προσοχή!", "Δεν έχετε επιλέξει μηχάνημα!")
            return
        else:
            founded_history = search_on_service(self.selected_machine.ID, self.search_maintenance_lineEdit.text())
            self.search_maintenance_lineEdit.setText("")
            # treeWidget
            self.history_treeWidget.clear()
            for index, item in enumerate(founded_history):
                # Ημερομηνία = QtCore.QDate.fromString(item.Ημερομηνία, "dd'/'MM'/'yyyy")
                self.history_item = QtWidgets.QTreeWidgetItem(self.history_treeWidget,
                                                              [str(item.ID), str(item.Ημερομηνία), str(item.ΔΤΕ),
                                                               str(item.Σκοπός_Επίσκεψης), str(item.Ενέργειες),
                                                               str(item.Μετρητής)
                                                                  , str(item.Επ_Service)])
                self.history_item.setData(1, QtCore.Qt.DisplayRole,
                                          QtCore.QDate.fromString(item.Ημερομηνία, "dd'/'MM'/'yyyy"))
                self.history_item.setTextAlignment(1, QtCore.Qt.AlignCenter)
                self.history_item.setTextAlignment(2, QtCore.Qt.AlignCenter)
                self.history_treeWidget.setStyleSheet("QTreeView::item { padding: 5px }")
                self.history_treeWidget.addTopLevelItem(self.history_item)
                self.history_treeWidget.resizeColumnToContents(3)
                self.history_treeWidget.resizeColumnToContents(4)
            self.history_treeWidget.setColumnWidth(0, 1)
            self.history_treeWidget.sortByColumn(1, QtCore.Qt.DescendingOrder)
            self.history_treeWidget.setColumnWidth(2, 50)

    def search_error(self):
        """
        Ψάχνει σε ολα τα  ιστορικά
        Δεν ψάχνει ΔΤΕ
        καλείτε
            1. self.search_errors_lineEdit.returnPressed.connect(self.search_error)
            2. self.search_errors_toolButton.clicked.connect(self.search_error)
        :return:
        """
        # αποκρυψη κουμπή ανοιχτής κλήσης
        self.view_open_task_toolButton.hide()
        if self.search_errors_lineEdit.text() == "":
            self.show_selected_machine_details_with_history()
            return
        else:
            founded_error = search_for_errors_on_service(self.search_errors_lineEdit.text())
            self.search_errors_lineEdit.setText("")
            # treeWidget
            self.history_treeWidget.clear()
            for index, item in enumerate(founded_error):
                # Ημερομηνία = QtCore.QDate.fromString(item.Ημερομηνία, "dd'/'MM'/'yyyy")
                self.history_item = QtWidgets.QTreeWidgetItem(self.history_treeWidget,
                                                              [str(item.ID), str(item.Ημερομηνία), str(item.ΔΤΕ),
                                                               str(item.Σκοπός_Επίσκεψης), str(item.Ενέργειες),
                                                               str(item.Μετρητής)
                                                                  , str(item.Επ_Service)])
                self.history_item.setData(1, QtCore.Qt.DisplayRole,
                                          QtCore.QDate.fromString(item.Ημερομηνία, "dd'/'MM'/'yyyy"))
                self.history_item.setTextAlignment(1, QtCore.Qt.AlignCenter)
                self.history_item.setTextAlignment(2, QtCore.Qt.AlignCenter)
                self.history_treeWidget.setStyleSheet("QTreeView::item { padding: 5px }")
                self.history_treeWidget.addTopLevelItem(self.history_item)
                self.history_treeWidget.resizeColumnToContents(3)
                self.history_treeWidget.resizeColumnToContents(4)
            self.history_treeWidget.setColumnWidth(0, 1)
            self.history_treeWidget.sortByColumn(1, QtCore.Qt.DescendingOrder)
            self.history_treeWidget.setColumnWidth(2, 50)

    def search_tasks(self):
        """
        Ψάχνει στις ανοιχτές κλησεις οχι κλειστές
        Δεν ψάχνει ΔΤΕ
        καλείτε
            1. self.search_on_tasks_lineEdit.returnPressed.connect(self.search_tasks)
            2. self.search_on_tasks_toolButton.clicked.connect(self.search_tasks)
        :return:
        """
        if self.search_on_tasks_lineEdit.text() == "":
            self.show_active_tasks()
            return
        else:
            founded_tasks = search_on_calendar(self.search_on_tasks_lineEdit.text())
            self.search_on_tasks_lineEdit.setText("")
            # treeWidget
            self.tasks_treeWidget.clear()
            for index, item in enumerate(founded_tasks):
                self.founded_task_item = QtWidgets.QTreeWidgetItem(self.tasks_treeWidget,
                                                                   [str(item.ID), str(item.Ημερομηνία), str(item.ΔΤΕ),
                                                                    str(item.machine.Customer.Επωνυμία_Επιχείρησης),
                                                                    str(item.machine.Εταιρεία), item.Σκοπός])
                self.founded_task_item.setData(1, QtCore.Qt.DisplayRole,
                                               QtCore.QDate.fromString(item.Ημερομηνία, "dd'/'MM'/'yyyy"))
                self.founded_task_item.setTextAlignment(2, QtCore.Qt.AlignCenter)
                self.founded_task_item.setTextAlignment(3, QtCore.Qt.AlignCenter)
                self.founded_task_item.setTextAlignment(4, QtCore.Qt.AlignCenter)
                self.tasks_treeWidget.setStyleSheet("QTreeView::item { padding: 7px }")
                self.tasks_treeWidget.addTopLevelItem(self.founded_task_item)
            self.tasks_treeWidget.sortByColumn(1, QtCore.Qt.AscendingOrder)

    def search_dte(self):
        """
        Ψάχνει ΔΤΕ στις ανοιχτές κλησεις οχι κλειστές
        καλείτε
            1. self.search_dte_on_tasks_lineEdit.returnPressed.connect(self.search_dte)
            2. self.search_dte_on_tasks_toolButton.clicked.connect(self.search_dte)
        :return:
        """
        if self.search_dte_on_tasks_lineEdit.text() == "":
            return
        else:
            founded_dte = search_for_dte_on_tasks(self.search_dte_on_tasks_lineEdit.text())
            self.search_dte_on_tasks_lineEdit.setText("")
            # Δημιουργεία πάλι του treewidget γιατι διαφορετικα καθηστερή πολύ αν το κάνω clear
            # treeWidget
            self.tasks_treeWidget.clear()
            for index, item in enumerate(founded_dte):
                self.founded_dte_item = QtWidgets.QTreeWidgetItem(self.tasks_treeWidget,
                                                                  [str(item.ID), str(item.Ημερομηνία), str(item.ΔΤΕ),
                                                                   str(item.machine.Customer.Επωνυμία_Επιχείρησης),
                                                                   str(item.machine.Εταιρεία), item.Σκοπός])
                self.founded_dte_item.setData(1, QtCore.Qt.DisplayRole,
                                              QtCore.QDate.fromString(item.Ημερομηνία, "dd'/'MM'/'yyyy"))
                # self.active_task_item.setTextAlignment(index, QtCore.Qt.AlignCenter)
                self.tasks_treeWidget.setStyleSheet("QTreeView::item { padding: 7px }")
                self.tasks_treeWidget.addTopLevelItem(self.founded_dte_item)
            self.tasks_treeWidget.sortByColumn(1, QtCore.Qt.AscendingOrder)

    def search_dte_on_service(self):
        """
        Ψάχνει ΔΤΕ στις κλιστές κλησεις δηλαδη στο ιστορικό
        καλείτε
            1. self.search_dte_on_service_lineEdit.returnPressed.connect(self.search_dte_on_service)
            2. self.search_dte_on_service_toolButton.clicked.connect(self.search_dte_on_service)
        :return:
        """

        if self.search_dte_on_service_lineEdit.text() == "":
            return
        else:
            founded_dte_on_service = search_for_dte_on_service(self.search_dte_on_service_lineEdit.text())
            self.search_dte_on_service_lineEdit.setText("")
            # treeWidget
            self.history_treeWidget.clear()

            for index, item in enumerate(founded_dte_on_service):
                # Ημερομηνία = QtCore.QDate.fromString(item.Ημερομηνία, "dd'/'MM'/'yyyy")
                self.history_item = QtWidgets.QTreeWidgetItem(self.history_treeWidget,
                                                              [str(item.ID), str(item.Ημερομηνία), str(item.ΔΤΕ),
                                                               str(item.Σκοπός_Επίσκεψης), str(item.Ενέργειες),
                                                               str(item.Μετρητής)
                                                                  , str(item.Επ_Service)])
                self.history_item.setData(1, QtCore.Qt.DisplayRole,
                                          QtCore.QDate.fromString(item.Ημερομηνία, "dd'/'MM'/'yyyy"))
                self.history_item.setTextAlignment(1, QtCore.Qt.AlignCenter)
                self.history_item.setTextAlignment(2, QtCore.Qt.AlignCenter)
                self.history_treeWidget.setStyleSheet("QTreeView::item { padding: 5px }")
                self.history_treeWidget.addTopLevelItem(self.history_item)
                self.history_treeWidget.resizeColumnToContents(3)
                self.history_treeWidget.resizeColumnToContents(4)
            self.history_treeWidget.setColumnWidth(0, 1)
            self.history_treeWidget.sortByColumn(1, QtCore.Qt.DescendingOrder)
            self.history_treeWidget.setColumnWidth(2, 50)

    def show_completed_tasks(self, qdate):  # qdate=> PyQt5.QtCore.QDate(2021, 11, 3)
        """
        Εμφάνιση εργασιών που έχουν τελειώσει όταν επιλέγουμε ημερομηνία
        :param qdate:  οταν επιλέγουμε ημερομηνία
        Καλείτε απο
            1. self.finished_tasks_dateEdit.dateChanged.connect(self.show_completed_tasks)
        :return:
        """

        selected_date = qdate.toString('dd/MM/yyyy')
        completed_task = fetch_completed_calendar(selected_date)

        self.tasks_treeWidget.clear()
        for index, item in enumerate(completed_task):
            self.completed_task_item = QtWidgets.QTreeWidgetItem(self.tasks_treeWidget,
                                                                 [str(item.ID), str(item.Ημερομηνία), str(item.ΔΤΕ),
                                                                  str(item.machine.Customer.Επωνυμία_Επιχείρησης),
                                                                  str(item.machine.Εταιρεία), item.Σκοπός])
            self.completed_task_item.setData(1, QtCore.Qt.DisplayRole,
                                             QtCore.QDate.fromString(item.Ημερομηνία, "dd'/'MM'/'yyyy"))
            # self.active_task_item.setTextAlignment(index, QtCore.Qt.AlignCenter)
            self.tasks_treeWidget.setStyleSheet("QTreeView::item { padding: 7px }")
            self.tasks_treeWidget.addTopLevelItem(self.completed_task_item)
        self.tasks_treeWidget.sortByColumn(1, QtCore.Qt.AscendingOrder)

    def view_selected_machine_open_task(self):
        self.tasks_treeWidget.clear()
        for index, item in enumerate(self.selected_machine_open_tasks):
            self.open_task_item = QtWidgets.QTreeWidgetItem(self.tasks_treeWidget,
                                                                 [str(item.ID), str(item.Ημερομηνία), str(item.ΔΤΕ),
                                                                  str(item.machine.Customer.Επωνυμία_Επιχείρησης),
                                                                  str(item.machine.Εταιρεία), item.Σκοπός])
            self.open_task_item.setData(1, QtCore.Qt.DisplayRole,
                                             QtCore.QDate.fromString(item.Ημερομηνία, "dd'/'MM'/'yyyy"))
            # self.active_task_item.setTextAlignment(index, QtCore.Qt.AlignCenter)
            self.tasks_treeWidget.setStyleSheet("QTreeView::item { padding: 7px }")
            self.tasks_treeWidget.addTopLevelItem(self.open_task_item)
        self.tasks_treeWidget.sortByColumn(1, QtCore.Qt.AscendingOrder)

    def left_calendar_clicked(self, qdate):  # qdate=> PyQt5.QtCore.QDate(2021, 11, 3)
        """
        Εμφάνιση εργασιών που είναι ανοιχτές όταν επιλέγουμε ημερομηνία απο το ημερολόγιο
        :param qdate:  οταν επιλέγουμε ημερομηνία
        Καλείτε απο
            1. self.calendarWidget.clicked.connect(self.left_calendar_clicked)
        :return:
        """

        selected_date = self.calendarWidget.selectedDate().toString('dd/MM/yyyy')
        selected_date_active_tasks = fetch_active_calendar_on_selected_date(selected_date)

        self.tasks_treeWidget.clear()
        for index, item in enumerate(selected_date_active_tasks):
            self.selected_date_active_task_item = QtWidgets.QTreeWidgetItem(self.tasks_treeWidget,
                                                                            [str(item.ID), str(item.Ημερομηνία),
                                                                             str(item.ΔΤΕ),
                                                                             str(item.machine.Customer.Επωνυμία_Επιχείρησης),
                                                                             str(item.machine.Εταιρεία), item.Σκοπός])
            self.selected_date_active_task_item.setData(1, QtCore.Qt.DisplayRole,
                                                        QtCore.QDate.fromString(item.Ημερομηνία, "dd'/'MM'/'yyyy"))
            # self.active_task_item.setTextAlignment(index, QtCore.Qt.AlignCenter)
            self.tasks_treeWidget.setStyleSheet("QTreeView::item { padding: 7px }")
            self.tasks_treeWidget.addTopLevelItem(self.selected_date_active_task_item)
        self.tasks_treeWidget.sortByColumn(1, QtCore.Qt.AscendingOrder)

    def show_selected_store_table(self):
        """
        Εμφάνιση προιόντων αποθήκης στον επιλεγμένο πίνακα
        καλείτε
            1. self.companies_comboBox.currentIndexChanged.connect(self.show_selected_store_table)
        :return:
        """
        selected_index = self.companies_comboBox.currentIndex()
        self.selected_table = store_tables[selected_index]
        selected_table_items = get_spare_parts(self.selected_table)
        first_item = selected_table_items[0]

        try:  # Εμφάνιση ανταλλακτικών
            test = first_item.PARTS_NR  # AttributeError:  # Αν ο πίνακας δεν έχει PARTS_NR
            self.store_treeWidget = QtWidgets.QTreeWidget(self.store_tab)
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(self.store_treeWidget.sizePolicy().hasHeightForWidth())
            self.store_treeWidget.setSizePolicy(sizePolicy)
            self.store_treeWidget.setFont(self.font_12)
            self.store_treeWidget.setAutoFillBackground(False)
            self.store_treeWidget.setWordWrap(True)
            self.store_treeWidget.setAlternatingRowColors(True)
            self.store_treeWidget.setSortingEnabled(True)
            self.store_treeWidget.setHeaderLabels(["ID", "Part No", "Κωδικός", "Τεμάχια", "Περιγραφή"])
            self.store_treeWidget.header().setStyleSheet(u"background-color: rgb(203, 203, 203);" "color: black;"
                                                         "font-style: normal;font-size: 12pt;font-weight: bold;")
            for index, item in enumerate(selected_table_items):
                self.selected_table_item = TreeWidgetItem(self.store_treeWidget,
                                                          [str(item.ID), str(item.PARTS_NR), str(item.ΚΩΔΙΚΟΣ),
                                                           str(item.ΤΕΜΑΧΙΑ), str(item.ΠΕΡΙΓΡΑΦΗ)])
                self.selected_table_item.setTextAlignment(1, QtCore.Qt.AlignCenter)
                self.selected_table_item.setTextAlignment(2, QtCore.Qt.AlignCenter)
                self.selected_table_item.setTextAlignment(3, QtCore.Qt.AlignCenter)
                self.selected_table_item.setTextAlignment(4, QtCore.Qt.AlignCenter)
                self.store_treeWidget.setStyleSheet("QTreeView::item { padding: 7px }")
                self.store_treeWidget.addTopLevelItem(self.selected_table_item)
            self.store_treeWidget.setColumnWidth(0, 1)
            self.store_treeWidget.setColumnWidth(1, 120)
            self.store_treeWidget.setColumnWidth(2, 80)
            self.store_treeWidget.setColumnWidth(3, 80)
            self.store_treeWidget.setColumnWidth(4, 250)
            self.store_treeWidget.sortByColumn(4, QtCore.Qt.AscendingOrder)
            self.store_treeWidget.itemDoubleClicked.connect(self.edit_store_items)
            self.gridLayout_6.addWidget(self.store_treeWidget, 2, 0, 1, 5)
        except AttributeError:  # Αν ο πίνακας δεν έχει PARTS_NR
            # Εμφάνιση αναλώσιμων
            self.store_treeWidget = QtWidgets.QTreeWidget(self.store_tab)
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(self.store_treeWidget.sizePolicy().hasHeightForWidth())
            self.store_treeWidget.setSizePolicy(sizePolicy)
            self.store_treeWidget.setFont(self.font_12)
            self.store_treeWidget.setAutoFillBackground(False)
            self.store_treeWidget.setWordWrap(True)
            self.store_treeWidget.setAlternatingRowColors(True)
            self.store_treeWidget.setSortingEnabled(True)
            self.store_treeWidget.setHeaderLabels(["ID", "Εταιρεία", "Ποιότητα", "Αναλώσιμο", "Κωδικός", "Τεμάχια",
                                                   "Τιμή", "Περιγραφή"])
            self.store_treeWidget.header().setStyleSheet(u"background-color: rgb(203, 203, 203);" "color: black;"
                                                         "font-style: normal;font-size: 12pt;font-weight: bold;")
            self.store_treeWidget.headerItem().setTextAlignment(0, QtCore.Qt.AlignLeft)
            self.store_treeWidget.headerItem().setTextAlignment(1, QtCore.Qt.AlignCenter)
            self.store_treeWidget.headerItem().setTextAlignment(2, QtCore.Qt.AlignCenter)
            self.store_treeWidget.headerItem().setTextAlignment(3, QtCore.Qt.AlignCenter)
            self.store_treeWidget.headerItem().setTextAlignment(4, QtCore.Qt.AlignCenter)
            self.store_treeWidget.headerItem().setTextAlignment(5, QtCore.Qt.AlignCenter)
            self.store_treeWidget.headerItem().setTextAlignment(6, QtCore.Qt.AlignCenter)

            for index, item in enumerate(selected_table_items):
                self.selected_table_item = TreeWidgetItem(self.store_treeWidget,
                                                          [str(item.ID), str(item.ΕΤΑΙΡΕΙΑ),
                                                           str(item.ΠΟΙΟΤΗΤΑ), str(item.ΑΝΑΛΩΣΙΜΟ),
                                                           str(item.ΚΩΔΙΚΟΣ), str(item.ΤΕΜΑΧΙΑ),
                                                           str(item.ΤΙΜΗ), str(item.ΠΕΡΙΓΡΑΦΗ)])
                self.selected_table_item.setTextAlignment(1, QtCore.Qt.AlignCenter)
                self.selected_table_item.setTextAlignment(2, QtCore.Qt.AlignCenter)
                self.selected_table_item.setTextAlignment(3, QtCore.Qt.AlignCenter)
                self.selected_table_item.setTextAlignment(4, QtCore.Qt.AlignCenter)
                self.selected_table_item.setTextAlignment(5, QtCore.Qt.AlignCenter)
                self.selected_table_item.setTextAlignment(6, QtCore.Qt.AlignCenter)
                self.store_treeWidget.setStyleSheet("QTreeView::item { padding: 7px }")
                if "C/M/Y" in item.ΠΕΡΙΓΡΑΦΗ:
                    self.selected_table_item.setBackground(7, QtGui.QColor('green'))
                    self.selected_table_item.setForeground(7, QtGui.QColor('white'))
                elif "CYAN" in item.ΠΕΡΙΓΡΑΦΗ:
                    self.selected_table_item.setBackground(7, QtGui.QColor('#0517D2'))
                    self.selected_table_item.setForeground(7, QtGui.QColor('white'))
                elif "MAGENTA" in item.ΠΕΡΙΓΡΑΦΗ:
                    self.selected_table_item.setBackground(7, QtGui.QColor('#D205CF'))
                    self.selected_table_item.setForeground(7, QtGui.QColor('white'))
                elif "YELLOW" in item.ΠΕΡΙΓΡΑΦΗ:
                    self.selected_table_item.setBackground(7, QtGui.QColor('yellow'))
                    self.selected_table_item.setForeground(7, QtGui.QColor('black'))
                elif "GRAY" in item.ΠΕΡΙΓΡΑΦΗ:
                    self.selected_table_item.setBackground(7, QtGui.QColor("gray"))
                    self.selected_table_item.setForeground(7, QtGui.QColor('white'))
                elif "BLACK" in item.ΠΕΡΙΓΡΑΦΗ:
                    self.selected_table_item.setBackground(7, QtGui.QColor("black"))
                    self.selected_table_item.setForeground(7, QtGui.QColor('white'))
                self.store_treeWidget.addTopLevelItem(self.selected_table_item)
            self.store_treeWidget.sortByColumn(1, QtCore.Qt.AscendingOrder)
            self.store_treeWidget.itemDoubleClicked.connect(self.edit_store_items)
            self.gridLayout_6.addWidget(self.store_treeWidget, 2, 0, 1, 5)

    def search_on_selected_table_store(self):
        """
        Ανανέωση self.show_selected_store_table()
        Αναζήτηση search_on_spare_parts
        Αναζήτηση search_on_consumables
        Καλείτε
            1. self.search_on_store_lineEdit.returnPressed.connect(self.search_on_selected_table_store)
            2. self.search_on_store_toolButton.clicked.connect(self.search_on_selected_table_store)
        :return:
        """
        if self.search_on_store_lineEdit.text() == "":
            self.show_selected_store_table()  # Refresh
            return

        text_to_search = self.search_on_store_lineEdit.text()
        self.search_on_store_lineEdit.setText("")
        self.store_treeWidget.clear()
        # Αν είναι ανταλλακτικό
        if self.selected_table == Brother or self.selected_table == Canon or self.selected_table == Epson \
                or self.selected_table == Konica or self.selected_table == Kyocera or self.selected_table == Lexmark \
                or self.selected_table == Oki or self.selected_table == Ricoh or self.selected_table == Samsung or \
                self.selected_table == Sharp:

            founded_spare_parts = search_on_spare_parts(self.selected_table, text_to_search)

            for index, item in enumerate(founded_spare_parts):
                self.founded_spare_part_item = TreeWidgetItem(self.store_treeWidget,
                                                              [str(item.ID), str(item.PARTS_NR), str(item.ΚΩΔΙΚΟΣ),
                                                               str(item.ΤΕΜΑΧΙΑ), str(item.ΠΕΡΙΓΡΑΦΗ)])
                self.founded_spare_part_item.setTextAlignment(1, QtCore.Qt.AlignCenter)
                self.founded_spare_part_item.setTextAlignment(2, QtCore.Qt.AlignCenter)
                self.founded_spare_part_item.setTextAlignment(3, QtCore.Qt.AlignCenter)
                self.founded_spare_part_item.setTextAlignment(4, QtCore.Qt.AlignCenter)
                self.store_treeWidget.setStyleSheet("QTreeView::item { padding: 7px }")
                self.store_treeWidget.addTopLevelItem(self.founded_spare_part_item)
        # αν έχουμε επιλέγη πίνακα και δεν είναι ανταλλακτικό είναι αναλώσιμο
        elif self.selected_table is not None:
            founded_consumables = search_on_consumables(self.selected_table, text_to_search)
            for index, item in enumerate(founded_consumables):
                self.founded_consumable_item = TreeWidgetItem(self.store_treeWidget,
                                                              [str(item.ID), str(item.ΕΤΑΙΡΕΙΑ),
                                                               str(item.ΠΟΙΟΤΗΤΑ), str(item.ΑΝΑΛΩΣΙΜΟ),
                                                               str(item.ΚΩΔΙΚΟΣ), str(item.ΤΕΜΑΧΙΑ),
                                                               str(item.ΤΙΜΗ), str(item.ΠΕΡΙΓΡΑΦΗ)])
                self.founded_consumable_item.setTextAlignment(1, QtCore.Qt.AlignCenter)
                self.founded_consumable_item.setTextAlignment(2, QtCore.Qt.AlignCenter)
                self.founded_consumable_item.setTextAlignment(3, QtCore.Qt.AlignCenter)
                self.founded_consumable_item.setTextAlignment(4, QtCore.Qt.AlignCenter)
                self.founded_consumable_item.setTextAlignment(5, QtCore.Qt.AlignCenter)
                self.founded_consumable_item.setTextAlignment(6, QtCore.Qt.AlignCenter)
                self.store_treeWidget.setStyleSheet("QTreeView::item { padding: 7px }")
                if "C/M/Y" in item.ΠΕΡΙΓΡΑΦΗ:
                    self.founded_consumable_item.setBackground(7, QtGui.QColor('green'))
                    self.founded_consumable_item.setForeground(7, QtGui.QColor('white'))
                elif "CYAN" in item.ΠΕΡΙΓΡΑΦΗ:
                    self.founded_consumable_item.setBackground(7, QtGui.QColor('#0517D2'))
                    self.founded_consumable_item.setForeground(7, QtGui.QColor('white'))
                elif "MAGENTA" in item.ΠΕΡΙΓΡΑΦΗ:
                    self.founded_consumable_item.setBackground(7, QtGui.QColor('#D205CF'))
                    self.founded_consumable_item.setForeground(7, QtGui.QColor('white'))
                elif "YELLOW" in item.ΠΕΡΙΓΡΑΦΗ:
                    self.founded_consumable_item.setBackground(7, QtGui.QColor('yellow'))
                    self.founded_consumable_item.setForeground(7, QtGui.QColor('black'))
                elif "GRAY" in item.ΠΕΡΙΓΡΑΦΗ:
                    self.founded_consumable_item.setBackground(7, QtGui.QColor("gray"))
                    self.founded_consumable_item.setForeground(7, QtGui.QColor('white'))
                elif "BLACK" in item.ΠΕΡΙΓΡΑΦΗ:
                    self.founded_consumable_item.setBackground(7, QtGui.QColor("black"))
                    self.founded_consumable_item.setForeground(7, QtGui.QColor('white'))

                self.store_treeWidget.addTopLevelItem(self.founded_consumable_item)
            self.store_treeWidget.sortByColumn(1, QtCore.Qt.AscendingOrder)
            self.gridLayout_6.addWidget(self.store_treeWidget, 2, 0, 1, 5)

    def search_on_customer_consumables(self):
        """
        Ανανέωση self.refresh_consumables()
        Αναζήτηση στα ανταλλακτικά επιλεγμένου πελάτη search_on_customer_consumables
        Καλείτε
            1. self.search_consumable_lineEdit.returnPressed.connect(self.search_on_customer_consumables)
            2. self.search_consumable_toolButton.clicked.connect(self.search_on_customer_consumables)
        :return:
        """
        if self.selected_customer is None:
            QtWidgets.QMessageBox.warning(None, "Προσοχή!", "Παρακαλώ επιλέξτε πρώτα πελάτη")
            return
        if self.search_consumable_lineEdit.text() == "":
            self.show_selected_customer_consumables()
            return
        else:
            customer_consumables = search_on_customer_consumables(self.selected_customer,
                                                                  self.search_consumable_lineEdit.text())
            self.search_consumable_lineEdit.setText("")
            self.consumables_treeWidget.clear()  # Καθαρισμός λίστας

            for index, item in enumerate(customer_consumables):
                self.selected_customer_consumable_item = QtWidgets.QTreeWidgetItem(self.consumables_treeWidget,
                                                                                   [str(item.ID), str(item.service.ΔΤΕ),
                                                                                    str(item.service.Ημερομηνία),
                                                                                    str(item.ΚΩΔΙΚΟΣ),
                                                                                    str(item.ΤΕΜΑΧΙΑ),
                                                                                    str(item.ΠΕΡΙΓΡΑΦΗ),
                                                                                    str(item.ΠΑΡΑΤΗΡΗΣΗΣ)])
                self.selected_customer_consumable_item.setData(2, QtCore.Qt.DisplayRole,
                                                               QtCore.QDate.fromString(item.service.Ημερομηνία,
                                                                                       "dd'/'MM'/'yyyy"))
                self.selected_customer_consumable_item.setTextAlignment(3, QtCore.Qt.AlignCenter)
                self.selected_customer_consumable_item.setTextAlignment(4, QtCore.Qt.AlignCenter)

                self.consumables_treeWidget.setStyleSheet("QTreeView::item { padding: 5px }")
                # Χρωματισμός πεδίων
                if "C/M/Y" in item.ΠΕΡΙΓΡΑΦΗ:
                    self.selected_customer_consumable_item.setBackground(5, QtGui.QColor('green'))
                    self.selected_customer_consumable_item.setForeground(5, QtGui.QColor('white'))
                elif "CYAN" in item.ΠΕΡΙΓΡΑΦΗ:
                    self.selected_customer_consumable_item.setBackground(5, QtGui.QColor('#0517D2'))
                    self.selected_customer_consumable_item.setForeground(5, QtGui.QColor('white'))
                elif "MAGENTA" in item.ΠΕΡΙΓΡΑΦΗ:
                    self.selected_customer_consumable_item.setBackground(5, QtGui.QColor('#D205CF'))
                    self.selected_customer_consumable_item.setForeground(5, QtGui.QColor('white'))
                elif "YELLOW" in item.ΠΕΡΙΓΡΑΦΗ:
                    self.selected_customer_consumable_item.setBackground(5, QtGui.QColor('yellow'))
                    self.selected_customer_consumable_item.setForeground(5, QtGui.QColor('black'))
                elif "GRAY" in item.ΠΕΡΙΓΡΑΦΗ:
                    self.selected_customer_consumable_item.setBackground(5, QtGui.QColor("gray"))
                    self.selected_customer_consumable_item.setForeground(5, QtGui.QColor('white'))
                elif "BLACK" in item.ΠΕΡΙΓΡΑΦΗ:
                    self.selected_customer_consumable_item.setBackground(5, QtGui.QColor("black"))
                    self.selected_customer_consumable_item.setForeground(5, QtGui.QColor('white'))

                self.consumables_treeWidget.addTopLevelItem(self.selected_customer_consumable_item)
                self.consumables_treeWidget.resizeColumnToContents(4)
            self.consumables_treeWidget.setColumnWidth(0, 1)
            self.consumables_treeWidget.setColumnWidth(1, 80)
            self.consumables_treeWidget.setColumnWidth(2, 110)
            self.consumables_treeWidget.setColumnWidth(3, 80)
            self.consumables_treeWidget.setColumnWidth(4, 80)
            self.consumables_treeWidget.setColumnWidth(5, 350)
            self.consumables_treeWidget.sortByColumn(2, QtCore.Qt.DescendingOrder)

    def save_customer_changes(self):
        """
        Αποθήκευση αλλαγών στην καρτέλα πελάτης
        Καλείτε
            1. self.save_customer_changes_toolButton.clicked.connect(self.save_customer_changes)
        :return:
        """
        if not self.selected_customer:
            QtWidgets.QMessageBox.warning(None, "Προσοχή!", "Παρακαλώ επιλέξτε πρώτα πελάτη")
            return
        try:
            self.selected_customer.Επωνυμία_Επιχείρησης = self.customer_name_lineEdit.text()
            self.selected_customer.Ονοματεπώνυμο = self.responsible_lineEdit.text()
            self.selected_customer.Διεύθυνση = self.address_lineEdit.text()
            self.selected_customer.Πόλη = self.city_lineEdit.text()
            self.selected_customer.Ταχ_Κώδικας = self.post_code_lineEdit.text()
            self.selected_customer.Περιοχή = self.area_lineEdit.text()
            self.selected_customer.Τηλέφωνο = self.phone_lineEdit.text()
            self.selected_customer.Κινητό = self.mobile_lineEdit.text()
            self.selected_customer.Φαξ = self.fax_lineEdit.text()
            self.selected_customer.E_mail = self.email_lineEdit.text()
            self.selected_customer.Σημειώσεις = self.customer_notes_textEdit.toPlainText()
            service_session.commit()
            QtWidgets.QMessageBox.information(None, "Πληροφορία", f"Οι αλλαγές αποθήκευτηκαν!")
            return
        except Exception:
            service_session.rollback()
            traceback.print_exc()
            QtWidgets.QMessageBox.critical(None, "Σφάλμα", f"Κάτι δεν πήγε καλα!\nΟι αλλαγές δεν αποθήκευτηκαν!")
            return

    def disable_customer(self):
        """
        Απενεργοποιήση  πελάτη αν δεν έχει ενεργά μηχανήματα check_if_customer_has_active_machines(self.selected_customer)
        Καλείτε
            1. self.disable_customer_toolButton.clicked.connect(self.disable_customer)
        :return:
        """

        if not self.selected_customer:
            QtWidgets.QMessageBox.warning(None, "Προσοχή!", "Παρακαλώ επιλέξτε πρώτα πελάτη")
            return
        try:
            if check_if_customer_has_active_machines(self.selected_customer):
                QtWidgets.QMessageBox.critical(None, "Σφάλμα", f"Ο πελάτης έχει ενεργά μηχανήματα!\nΠαρακαλώ όπως "
                                                               f"μεταφέρεται τα μηχανήματα σε άλλο πελάτη ή "
                                                               f"απενεργοποιήσετε")
                return
            answer = QtWidgets.QMessageBox.question(None, 'Προσοχή', f"Σίγουρα θέλετε να απενεργοποιήσετε τον πελάτη\n"
                                                                     f"{self.selected_customer.Επωνυμία_Επιχείρησης};",
                                                    QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                    QtWidgets.QMessageBox.No)
            if answer == QtWidgets.QMessageBox.Yes:
                old_notes = self.selected_customer.Σημειώσεις
                self.selected_customer.Σημειώσεις = f"{old_notes}" + f"\n------------- Απενεργοποιήση πελάτη {today} ----------------------"
                self.selected_customer.Κατάσταση = 0
                service_session.commit()
                self.refresh_customers()
                QtWidgets.QMessageBox.information(None, "Πληροφορία", f"Ο πελάτης δεν θα ξαναέρθει!")
                return
        except Exception:
            service_session.rollback()
            traceback.print_exc()
            QtWidgets.QMessageBox.critical(None, "Σφάλμα", f"Κάτι δεν πήγε καλα!\nΟι αλλαγές δεν αποθήκευτηκαν!")
            return

    def save_machine_changes(self):
        """
        Αποθήκευση αλλαγών στην καρτέλα μηχάνημα
        Καλείτε
            1. self.save_copier_changes_toolButton.clicked.connect(self.save_machine_changes)
        :return:
        """
        if not self.selected_machine:
            QtWidgets.QMessageBox.warning(None, "Προσοχή!", "Παρακαλώ επιλέξτε πρώτα μηχάνημα")
            return
        try:
            if self.serial_number_lineEdit.text().replace(" ", "").upper() == "":
                self.serial_number_lineEdit.setStyleSheet(u"background-color: red;" "color: white;")
                return
            else:
                self.serial_number_lineEdit.setStyleSheet(u"background-color: green;" "color: white;")

            if self.copier_model_lineEdit.text().upper().replace(" ", "") == "":
                self.copier_model_lineEdit.setStyleSheet(u"background-color: red;" "color: white;")
                return
            else:
                self.copier_model_lineEdit.setStyleSheet(u"background-color: green;" "color: white;")

            self.selected_machine.Εταιρεία = self.copier_model_lineEdit.text().upper()
            self.selected_machine.Serial = self.serial_number_lineEdit.text().replace(" ", "").upper()
            self.selected_machine.Εναρξη = self.started_date_dateEdit.date().toString('dd/MM/yyyy')
            self.selected_machine.Μετρητής_έναρξης = self.start_counter_lineEdit.text()
            self.selected_machine.Σημειώσεις = self.copiers_notes_textEdit.toPlainText()
            service_session.commit()
            QtWidgets.QMessageBox.information(None, "Πληροφορία", f"Οι αλλαγές αποθήκευτηκαν!")
            return
        except Exception:
            service_session.rollback()
            traceback.print_exc()
            QtWidgets.QMessageBox.critical(None, "Σφάλμα", f"Κάτι δεν πήγε καλα!\nΟι αλλαγές δεν αποθήκευτηκαν!")
            return

    def disable_machine(self):
        """
       Απενεργοποιήση μηχανήματος
       Καλείτε
           1. self.disable_copier_toolButton.clicked.connect(self.disable_machine)
       :return:
       """

        if not self.selected_machine:
            QtWidgets.QMessageBox.warning(None, "Προσοχή!", "Παρακαλώ επιλέξτε πρώτα μηχάνημα")
            return
        try:
            answer = QtWidgets.QMessageBox.question(None, 'Προσοχή', f"Σίγουρα θέλετε να απενεργοποιήσετε το "
                                                                     f"{self.selected_machine.Εταιρεία};",
                                                    QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                    QtWidgets.QMessageBox.No)
            if answer == QtWidgets.QMessageBox.Yes:
                self.selected_machine.Κατάσταση = 0
                service_session.commit()
                self.refresh_active_machines()
                QtWidgets.QMessageBox.information(None, "Πληροφορία", f"Το μηχάνημα βγήκε στην σύνταξη!")
                self.selected_machine = None
                self.copier_model_lineEdit.setText("")
                self.copiers_notes_textEdit.setText("")
                self.start_counter_lineEdit.setText("")
                self.serial_number_lineEdit.setText("")
                self.started_date_dateEdit.setDate(QtCore.QDate.currentDate())
                return
        except Exception:
            service_session.rollback()
            traceback.print_exc()
            QtWidgets.QMessageBox.critical(None, "Σφάλμα", f"Κάτι δεν πήγε καλα!\nΟι αλλαγές δεν αποθήκευτηκαν!")
            return

    def refresh_customers(self):
        """
        Δημειουργεία ξανά του customers_treeWidget γιατι είναι πολύ αργό με το clear
        Εμφάνιση ενεργών πελατών show_active_customers
        Καθαρισμός του history_treewidget history_treeWidget.clear()
        Καλείτε
           1. οταν απενεργοποιούμε επιτυχός εναν πελάτη self.disable_customer()
           2. οταν κάνουμε αναζήτηση για πελάτη self.search_customer()
        :return:
        """

        self.customers_treeWidget = QtWidgets.QTreeWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.customers_treeWidget.sizePolicy().hasHeightForWidth())
        self.customers_treeWidget.setSizePolicy(sizePolicy)
        self.customers_treeWidget.setMinimumSize(QtCore.QSize(300, 0))
        self.customers_treeWidget.setMaximumSize(QtCore.QSize(300, 16777215))
        self.customers_treeWidget.setWordWrap(True)
        self.customers_treeWidget.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        # self.treeWidget.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.customers_treeWidget.setLineWidth(14)
        # self.customers_treeWidget.setAlternatingRowColors(True)
        self.customers_treeWidget.setHeaderLabels(["ID", "Πελάτης"])
        self.customers_treeWidget.headerItem().setTextAlignment(1, QtCore.Qt.AlignCenter)
        # self.treeWidget.setAnimated(True)
        self.customers_treeWidget.header().setStyleSheet(u"background-color: orange;" "color: black;"
                                                         "font-style: normal;font-size: 12pt;font-weight: bold;")
        self.customers_treeWidget.setFont(self.font_12)
        self.customers_treeWidget.setObjectName("customers_treeWidget")
        self.customers_treeWidget.itemClicked.connect(self.customer_clicked)
        self.gridLayout_3.addWidget(self.customers_treeWidget, 2, 0, 1, 2)
        self.customer_notes_textEdit.setText("")
        self.customer_name_lineEdit.setText("")
        self.mobile_lineEdit.setText("")
        self.phone_lineEdit.setText("")
        self.address_lineEdit.setText("")
        self.area_lineEdit.setText("")
        self.post_code_lineEdit.setText("")
        self.responsible_lineEdit.setText("")
        self.city_lineEdit.setText("")
        self.fax_lineEdit.setText("")
        self.email_lineEdit.setText("")
        self.serial_number_lineEdit.setText("")
        self.started_date_dateEdit.setDate(QtCore.QDate.currentDate())
        self.start_counter_lineEdit.setText("")
        self.copier_model_lineEdit.setText("")
        self.copiers_notes_textEdit.setText("")
        self.show_active_customers()
        self.selected_customer = None
        self.history_treeWidget.clear()  # Καθαρισμός ιστορικού
        # Ενημέρωση status bar
        self.update_status_bar()

    def refresh_active_machines(self):
        """
        Δημειουργεία ξανά του machines_treeWidget γιατι είναι πολύ αργό με το clear
        Εμφάνιση ενεργών μηχανημάτων show_active_machines
        Καθαρισμός του history_treewidget history_treeWidget.clear()
        Καλείτε
           1. οταν απενεργοποιούμε επιτυχός ενα μηχάνημα  self.disable_machine()
           2. οταν κάνουμε αναζήτηση για μηχάνημα self.search_machine()
        :return:
        """

        self.machines_treeWidget = QtWidgets.QTreeWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.machines_treeWidget.sizePolicy().hasHeightForWidth())
        self.machines_treeWidget.setSizePolicy(sizePolicy)
        self.machines_treeWidget.setMinimumSize(QtCore.QSize(350, 0))
        self.machines_treeWidget.setMaximumSize(QtCore.QSize(350, 16777215))
        self.machines_treeWidget.setFont(self.font_12)
        self.machines_treeWidget.setObjectName("machines_treeWidget")
        self.machines_treeWidget.itemClicked.connect(self.machine_clicked)
        # self.customers_treeWidget.setSortingEnabled(True)
        self.machines_treeWidget.setWordWrap(True)
        self.machines_treeWidget.setAutoFillBackground(True)
        # self.machines_treeWidget.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        # self.treeWidget.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.machines_treeWidget.setLineWidth(14)
        # self.machines_treeWidget.setAlternatingRowColors(True)
        self.machines_treeWidget.setHeaderLabels(["ID", "Μηχάνημα"])
        self.machines_treeWidget.headerItem().setTextAlignment(1, QtCore.Qt.AlignCenter)
        self.machines_treeWidget.headerItem().setTextAlignment(0, QtCore.Qt.AlignLeft)
        # self.treeWidget.setAnimated(True)
        self.machines_treeWidget.header().setStyleSheet(u"background-color: gray;" "color: white;"
                                                        "font-style: normal;font-size: 12pt;font-weight: bold;")

        self.gridLayout_3.addWidget(self.machines_treeWidget, 2, 2, 1, 2)
        self.show_active_machines()
        self.history_treeWidget.clear()
        self.selected_machine = None
        # Ενημέρωση status bar
        self.update_status_bar()

    def refresh_consumables(self):
        """
        Δημειουργεία ξανά του consumables_treeWidget γιατι είναι πολύ αργό με το clear
        Εμφάνιση ανταλλακτικών επιλεγμένου πελάτη self.show_selected_customer_consumables()
        Καλείτε
           1. οταν κάνουμε αναζήτηση για ανταλλακτικά self.search_on_customer_consumables()
        :return:
        """
        self.consumables_treeWidget = QtWidgets.QTreeWidget(self.consumables_tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding,
                                           QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.consumables_treeWidget.sizePolicy().hasHeightForWidth())
        self.consumables_treeWidget.setSizePolicy(sizePolicy)
        self.consumables_treeWidget.setFont(self.font_12)
        self.consumables_treeWidget.setAlternatingRowColors(True)
        self.consumables_treeWidget.setWordWrap(True)
        self.consumables_treeWidget.setObjectName("consumables_treeWidget")
        self.consumables_treeWidget.setHeaderLabels(["ID", "ΔΤΕ", "Ημερομηνία", "Κωδικός", "Τεμάχια", "Προϊόν", "Σημειώσεις"])
        self.consumables_treeWidget.headerItem().setTextAlignment(3, QtCore.Qt.AlignCenter)
        self.consumables_treeWidget.headerItem().setTextAlignment(4, QtCore.Qt.AlignCenter)
        self.consumables_treeWidget.header().setStyleSheet(u"background-color: rgb(203, 203, 203);" "color: black;"
                                                           "font-style: normal;font-size: 12pt;font-weight: bold;")
        self.consumables_treeWidget.itemDoubleClicked.connect(self.show_edit_spare_part_window)
        self.gridLayout_5.addWidget(self.consumables_treeWidget, 1, 0, 1, 3)
        self.show_selected_customer_consumables()

    def update_status_bar(self):
        if self.selected_customer and self.selected_machine:
            self.statusbar.showMessage(f"{self.selected_customer.Επωνυμία_Επιχείρησης} --- "
                                       f"{self.selected_machine.Εταιρεία}")
        elif self.selected_customer and not self.selected_machine:
            self.statusbar.showMessage(f"{self.selected_customer.Επωνυμία_Επιχείρησης} --- "
                                       f"Κανένα επιλεγμένο μηχάνημα")
        elif self.selected_machine and not self.selected_customer:
            self.statusbar.showMessage(f"Μή επιλεγμένος πελάτης --- "
                                       f"{self.selected_machine.Εταιρεία}")
        else:
            self.statusbar.showMessage(f"Μή επιλεγμένος πελάτης --- "
                                       f"Κανένα επιλεγμένο μηχάνημα")

    def info(self):
        QtWidgets.QMessageBox.about(None, 'Σχετικά',
                                    f"""Author     : Jordanis Ntini<br>
                                    Copyright  : Copyright © 2021<br>
                                    Credits    : ['Athanasia Tzampazi']<br>
                                    Version    : '{VERSION}'<br>
                                    Maintainer : Jordanis Ntini<br>
                                    Email      : ntinisiordanis@gmail.com<br>
                                    Status     : Development<br>
                                    Language   : <a href='https://www.python.org/'>Python</a><br>
                                    Gui        : <a href='https://pypi.org/project/PyQt5/'>PyQt5</a><br>
                                    License    : GPL V3 <a href='https://www.gnu.org/licenses/gpl-3.0.txt'>GNU GENERAL PUBLIC LICENSE</a>""")

    def quit(self, *args):
        answer = QtWidgets.QMessageBox.warning(None, 'Προσοχή!', f"Σίγουρα θέλετε να κλείσεται τo Service Book;",
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                               QtWidgets.QMessageBox.No)
        if answer == QtWidgets.QMessageBox.Yes:
            # self.close()
            sys.exit(app.exec_())
        else:
            return

    # -------------------------------------------------- Νέα παράθυρα ------------------------------------
    def show_add_new_customer_window(self):
        self.add_new_customer_window = QtWidgets.QWidget()
        # self.show_add_new_customer_window.setWindowTitle("Προσθήκη νέου πελάτη")
        self.add_new_customer = Ui_add_new_customer_window()
        # Αρχικοποιηση των κουμπιων, γραμμων επεξεργασίας κτλπ
        self.add_new_customer.setupUi(self.add_new_customer_window)
        self.add_new_customer.window = self.add_new_customer_window  # Αν θέλουμε να ανοιγουν πολλα παράθυρα
        self.add_new_customer_window.show()
        self.add_new_customer.window_closed.connect(lambda: (self.refresh_customers(),
                                                             self.add_new_customer_window.close()))

    def show_add_new_machine_window(self):
        self.add_new_machine_window = QtWidgets.QWidget()
        # self.show_add_new_customer_window.setWindowTitle("Προσθήκη νέου πελάτη")
        self.add_new_machine = Ui_add_new_machine_window()
        self.add_new_machine.selected_customer = self.selected_customer
        # Αρχικοποιηση των κουμπιων, γραμμων επεξεργασίας κτλπ
        self.add_new_machine.setupUi(self.add_new_machine_window)

        self.add_new_machine.window = self.add_new_machine_window  # Αν θέλουμε να ανοιγουν πολλα παράθυρα
        self.add_new_machine_window.show()
        self.add_new_machine.window_closed.connect(lambda: (self.refresh_active_machines(),
                                                            self.add_new_machine_window.close()))

    def show_enable_customer_window(self):
        self.enable_customer_window = QtWidgets.QWidget()
        # self.show_add_new_customer_window.setWindowTitle("Προσθήκη νέου πελάτη")
        self.enable_customer = Ui_enable_customer_window()
        # Αρχικοποιηση των κουμπιων, γραμμων επεξεργασίας κτλπ
        self.enable_customer.setupUi(self.enable_customer_window)

        self.enable_customer.window = self.enable_customer_window  # Αν θέλουμε να ανοιγουν πολλα παράθυρα
        self.enable_customer_window.show()
        self.enable_customer.window_closed.connect(lambda: (self.refresh_customers(),
                                                            self.enable_customer_window.close()))

    def show_enable_machine_window(self):
        self.enable_machine_window = QtWidgets.QWidget()
        # self.show_add_new_customer_window.setWindowTitle("Προσθήκη νέου πελάτη")
        self.enable_machine = Ui_enable_machine_window()
        # self.enable_machine.selected_customer = self.selected_customer
        # Αρχικοποιηση των κουμπιων, γραμμων επεξεργασίας κτλπ
        self.enable_machine.setupUi(self.enable_machine_window)

        self.enable_machine.window = self.enable_machine_window  # Αν θέλουμε να ανοιγουν πολλα παράθυρα
        self.enable_machine_window.show()
        self.enable_machine.window_closed.connect(lambda: (self.refresh_active_machines(),
                                                           self.enable_machine_window.close()))

    def show_transfers_logs_window(self):
        self.transfer_logs_window = QtWidgets.QWidget()
        # self.show_add_new_customer_window.setWindowTitle("Προσθήκη νέου πελάτη")
        self.transfer_log = Ui_transfers_logs_window()
        # self.enable_machine.selected_customer = self.selected_customer
        # Αρχικοποιηση των κουμπιων, γραμμων επεξεργασίας κτλπ
        self.transfer_log.setupUi(self.transfer_logs_window)

        self.transfer_log.window = self.transfer_logs_window  # Αν θέλουμε να ανοιγουν πολλα παράθυρα
        self.transfer_logs_window.show()
        self.transfer_log.window_closed.connect(lambda: self.transfer_logs_window.close())

    def show_transport_machine_window(self):
        if not self.selected_machine:
            QtWidgets.QMessageBox.warning(None, "Προσοχή", "Παρακαλώ επιλέξτε πρώτα μηχάνημα")
            return
        self.transport_machine_window = QtWidgets.QWidget()
        # self.show_add_new_customer_window.setWindowTitle("Προσθήκη νέου πελάτη")
        self.transport_machine = Ui_Transport_Machine_Window()
        # self.add_task.selected_customer = self.selected_customer
        self.transport_machine.selected_machine = self.selected_machine
        # Αρχικοποιηση των κουμπιων, γραμμων επεξεργασίας κτλπ
        self.transport_machine.setupUi(self.transport_machine_window)

        self.transport_machine.window = self.transport_machine_window  # Αν θέλουμε να ανοιγουν πολλα παράθυρα
        self.transport_machine_window.show()
        self.transport_machine.window_closed.connect(lambda: (self.refresh_active_machines(), self.transport_machine_window.close()))

    def show_add_task_window(self):
        self.add_task_window = QtWidgets.QWidget()
        # self.show_add_new_customer_window.setWindowTitle("Προσθήκη νέου πελάτη")
        self.add_task = Ui_Add_Task_Window()
        self.add_task.selected_customer = self.selected_customer
        self.add_task.selected_machine = self.selected_machine
        # Αρχικοποιηση των κουμπιων, γραμμων επεξεργασίας κτλπ
        self.add_task.setupUi(self.add_task_window)

        self.add_task.window = self.add_task_window  # Αν θέλουμε να ανοιγουν πολλα παράθυρα
        self.add_task_window.show()
        self.add_task.window_closed.connect(lambda: (self.show_active_tasks(), self.add_task_window.close()))

    def show_edit_task_window(self, item=None, column=None, calendar_id=None):
        try:
            selected_calendar_id = item.text(0)  # Οταν πατάμε διπλο click στης εργασίες
        except AttributeError:  # 'NoneType' object has no attribute 'text' Οταν πατάμε απο το history treewidget
            selected_calendar_id = calendar_id
        # Αν δεν υπάρχει edit_task_window ή αν ο χρήστης εχει κλεισει το παράθυρο απο το Χ πανω δεξια
        # ελεγχουμε αν ειναι ορατο
        if self.edit_task_window is None or not self.edit_task_window.isVisible():
            self.edit_task_window = QtWidgets.QWidget()
            self.edit_task = Ui_Edit_Task_Window()
            self.edit_task.selected_calendar_id = selected_calendar_id
            self.edit_task.setupUi(self.edit_task_window)
            self.edit_task.window = self.edit_task_window  # Αν θέλουμε να ανοιγουν πολλα παράθυρα
            self.edit_task_window.show()
            self.edit_task.window_closed.connect(lambda: (self.show_active_tasks(), self.edit_task_window.close()))
        elif self.second_edit_task_window is None or not self.second_edit_task_window.isVisible():
            self.second_edit_task_window = QtWidgets.QWidget()
            self.second_edit_task = Ui_Edit_Task_Window()
            self.second_edit_task.selected_calendar_id = selected_calendar_id
            self.second_edit_task.setupUi(self.second_edit_task_window)
            self.second_edit_task.window = self.second_edit_task_window  # Αν θέλουμε να ανοιγουν πολλα παράθυρα
            self.second_edit_task_window.show()
            self.second_edit_task.window_closed.connect(lambda: (self.show_active_tasks(), self.second_edit_task_window.close()))
        else:
            QtWidgets.QMessageBox.warning(None, 'Προσοχή!', f"Παρακαλώ κλείστε ενα απο τα ανοιχτά παράθυρα "
                                                            f"επεξεργασίας κλήσης.")
            return

    def show_edit_service_window(self, item, column):
        selected_service_id = item.text(0)
        selected_calendar = get_calendar_from_service_id(selected_service_id)
        if selected_calendar:  # Αν έχει ημερολόγιο (κλήση - εργασία) να διξει την επεξεργασία ημερολογίου
            self.show_edit_task_window(calendar_id=selected_calendar.ID)
        else:
            self.selected_service = get_service_from_id(selected_service_id)
            if self.edit_service_window is None or not self.edit_service_window.isVisible():
                self.edit_service_window = QtWidgets.QWidget()
                self.edit_service = Ui_Edit_Service_Window()
                self.edit_service.selected_service = self.selected_service
                self.edit_service.setupUi(self.edit_service_window)
                self.edit_service.get_service_data()
                self.edit_service.window = self.edit_service_window  # Αν θέλουμε να ανοιγουν πολλα παράθυρα
                self.edit_service_window.show()
                self.edit_service.window_closed.connect(self.edit_service_window.close)
            elif self.second_edit_service_window is None or not self.second_edit_service_window.isVisible():
                self.second_edit_service_window = QtWidgets.QWidget()
                self.second_edit_service = Ui_Edit_Service_Window()
                self.second_edit_service.selected_service = self.selected_service
                self.second_edit_service.setupUi(self.second_edit_service_window)
                self.second_edit_service.get_service_data()
                self.second_edit_service.window = self.second_edit_service_window  # Αν θέλουμε να ανοιγουν πολλα παράθυρα
                self.second_edit_service_window.show()
                self.second_edit_service.window_closed.connect(self.second_edit_service_window.close)
            else:
                QtWidgets.QMessageBox.warning(None, 'Προσοχή!', f"Παρακαλώ κλείστε ενα απο τα ανοιχτά παράθυρα "
                                                                f"επεξεργασίας συντήρησης.")
                return

    def show_add_service_window(self):
        if self.selected_machine is None:
            QtWidgets.QMessageBox.warning(None, "Προσοχή!", "Παρακαλώ επιλέξτε πρώτα μηχάνημα!")
            return
        self.add_service_window = QtWidgets.QWidget()
        self.add_service = Ui_Add_Service_Window()
        self.add_service.selected_machine = self.selected_machine
        self.add_service.setupUi(self.add_service_window)
        # self.add_service.fetch_service_data()
        self.add_service.window = self.add_service_window  # Αν θέλουμε να ανοιγουν πολλα παράθυρα
        self.add_service_window.show()
        self.add_service.window_closed.connect(lambda: (self.show_selected_machine_details_with_history(),
                                                        self.add_service_window.close()))

    def show_edit_email_settings_window(self):
        self.edit_email_settings_window = QtWidgets.QWidget()
        # self.show_add_new_customer_window.setWindowTitle("Προσθήκη νέου πελάτη")
        self.edit_email_settings = Ui_Edit_Email_Settings_Window()
        self.edit_email_settings.setupUi(self.edit_email_settings_window)

        self.edit_email_settings.window = self.edit_email_settings_window  # Αν θέλουμε να ανοιγουν πολλα παράθυρα
        self.edit_email_settings_window.show()
        self.edit_email_settings.window_closed.connect(lambda: self.edit_email_settings_window.close())

    def show_edit_service_data_window(self):
        self.edit_service_data_window = QtWidgets.QWidget()
        # self.show_add_new_customer_window.setWindowTitle("Προσθήκη νέου πελάτη")
        self.edit_service_data = Ui_Edit_Service_Data_Window()
        self.edit_service_data.setupUi(self.edit_service_data_window)

        self.edit_service_data.window = self.edit_service_data_window  # Αν θέλουμε να ανοιγουν πολλα παράθυρα
        self.edit_service_data_window.show()
        self.edit_service_data.window_closed.connect(lambda: self.edit_service_data_window.close())

    def show_edit_spare_part_window(self, item, column):
        selected_spare_part_id = item.text(0)
        selected_spare_part_obj = get_consumable_from_id(selected_spare_part_id)
        selected_calendar = get_calendar_from_service_id(selected_spare_part_obj.Service_ID)
        if selected_calendar:  # Αν έχει ημερολόγιο (κλήση - εργασία) να διξει την επεξεργασία ημερολογίου
            self.show_edit_task_window(calendar_id=selected_calendar.ID)
        else:
            self.selected_service = get_service_from_id(selected_spare_part_obj.Service_ID)
            self.edit_consumable_window = QtWidgets.QWidget()
            self.edit_consumable = Ui_Edit_Service_Window()
            self.edit_consumable.selected_service = self.selected_service
            self.edit_consumable.setupUi(self.edit_consumable_window)
            self.edit_consumable.get_service_data()
            self.edit_consumable.window = self.edit_consumable_window  # Αν θέλουμε να ανοιγουν πολλα παράθυρα
            self.edit_consumable_window.show()
            self.edit_consumable.window_closed.connect(lambda: (self.show_selected_machine_details_with_history(),
                                                             self.edit_consumable_window.close()))

    def show_activation_window(self):
        self.remaining_support_days = check_if_support_exist()
        if self.remaining_support_days:
            QtWidgets.QMessageBox.information(None, "Πληροφορία", f"Η υποστήριξη σάς θα λήξει σε "
                                                                  f"{self.remaining_support_days} μέρες")
        else:
            self.activation_window = QtWidgets.QWidget()
            # self.show_add_new_customer_window.setWindowTitle("Προσθήκη νέου πελάτη")
            self.activation = Ui_Activation_Window()
            self.activation.setupUi(self.activation_window)
            self.activation.window = self.activation_window  # Αν θέλουμε να ανοιγουν πολλα παράθυρα
            self.activation_window.show()
            self.activation.window_closed.connect(lambda: self.activation_window.close())

    def edit_store_items(self, item, column):
        if self.selected_table == Brother or self.selected_table == Canon or self.selected_table == Epson \
                or self.selected_table == Konica or self.selected_table == Kyocera or self.selected_table == Lexmark \
                or self.selected_table == Oki or self.selected_table == Ricoh or self.selected_table == Samsung or \
                self.selected_table == Sharp:
            self.show_edit_spare_part_from_store_window(item, column)
        elif self.selected_table == Melanotainies:
            self.show_edit_melanotainies_window(item, column)
        else:
            self.show_edit_consumables_window(item, column)

    def show_edit_melanotainies_window(self, item, column):  # column ειναι η στήλη που πατησε κλικ
        item_id = item.text(0)  # item.text(0)  == ID
        self.edit_melanotainies_window = QtWidgets.QWidget()
        self.edit_melanotainies_window.setWindowTitle("Επεξεργασία μελανοταινίας")
        self.edit_melanotainies_window.setStyleSheet(u"font: 75 13pt \"Calibri\";")
        self.edit_melanotainia = Ui_edit_melanotainies_window()
        self.edit_melanotainia.setupUi(self.edit_melanotainies_window)  # Αρχικοποιηση των κουμπιων, γραμμων επεξεργασίας κτλπ
        self.edit_melanotainia.selected_id = item_id
        self.edit_melanotainia.selected_table = self.selected_table
        self.edit_melanotainia.edit_melanotainia()  # Εμφάνηση δεδομένων απο την βάση δεδομένων
        self.edit_melanotainia.show_file()  # Εμφάνηση Αρχείων
        self.edit_melanotainia.window = self.edit_melanotainies_window  # Αν θέλουμε να ανοιγουν πολλα παράθυρα
        self.edit_melanotainies_window.show()
        self.edit_melanotainia.window_closed.connect(lambda: (self.show_selected_store_table(), self.edit_melanotainies_window.close()))

    def show_edit_spare_part_from_store_window(self, item, column):  # column ειναι η στήλη που πατησε κλικ
        item_id = item.text(0)  # item.text(0)  == ID
        # Αν δεν υπάρχει edit_spare_part_window ή αν ο χρήστης εχει κλεισει το παράθυρο απο το Χ πανω δεξια
        # ελεγχουμε αν ειναι ορατο
        self.edit_spare_part_window = QtWidgets.QWidget()
        self.edit_spare_part_window.setWindowTitle("Επεξεργασία ανταλλακτικού")
        self.edit_spare_part = Ui_edit_spare_parts_window()
        self.edit_spare_part.setupUi(self.edit_spare_part_window)  # Αρχικοποιηση των κουμπιων, γραμμων επεξεργασίας κτλπ
        self.edit_spare_part.selected_id = item_id
        self.edit_spare_part.selected_table = self.selected_table
        self.edit_spare_part.edit_spare_part()  # Εμφάνηση δεδομένων απο την βάση δεδομένων
        self.edit_spare_part.show_file()  # Εμφάνηση Αρχείων
        self.edit_spare_part.window = self.edit_spare_part_window  # Αν θέλουμε να ανοιγουν πολλα παράθυρα
        self.edit_spare_part_window.show()
        self.edit_spare_part.window_closed.connect(lambda: (self.show_selected_store_table(), self.edit_spare_part_window.close()))

    def show_edit_consumables_window(self, item, column):
        item_id = item.text(0)  # item.text(0)  == ID# column ειναι η στήλη που πατησε κλικ
        self.edit_consumables_window = QtWidgets.QWidget()
        self.edit_consumables_window.setWindowTitle(f"Επεξεργασία αναλώσιμου")
        self.edit_consumables_window.setStyleSheet(u"font: 75 13pt \"Calibri\";")
        self.edit_consumable = Ui_edit_consumables_window()
        # Αρχικοποιηση των κουμπιων, γραμμων επεξεργασίας κτλπ
        self.edit_consumable.setupUi(self.edit_consumables_window)
        self.edit_consumable.selected_id = item_id
        self.edit_consumable.selected_table = self.selected_table
        self.edit_consumable.edit_consumable()  # Εμφάνηση δεδομένων απο την βάση δεδομένων
        self.edit_consumable.show_file()  # Εμφάνηση Αρχείων
        self.edit_consumable.window = self.edit_consumables_window  # Αν θέλουμε να ανοιγουν πολλα παράθυρα
        self.edit_consumables_window.show()
        self.edit_consumable.window_closed.connect(lambda: (self.show_selected_store_table(), self.edit_consumables_window.close()))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")
    MainWindow = QtWidgets.QMainWindow()
    # MainWindow.setStyleSheet(u"font: 75 13pt \"Calibri\";")
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
