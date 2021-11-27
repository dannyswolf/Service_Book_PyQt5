# -*- coding: utf-8 -*-
# Created by: PyQt5 UI code generator 5.15.4

import sys
import traceback
import sqlalchemy
from db import service_session, Customer, fetch_inactive_customers, check_if_customer_name_is_inactive, get_inactive_customer_from_name
from PyQt5 import QtCore, QtGui, QtWidgets
from settings import VERSION, root_logger, today

sys.stderr.write = root_logger.error
sys.stdout.write = root_logger.info


class Ui_enable_customer_window(QtWidgets.QWidget):
    window_closed = QtCore.pyqtSignal()  # Το Signal πρεπει να είναι εκτός __init__ δεν δουλευει αλλιως

    def __init__(self):
        super().__init__()
        self.safe_to_save = True
        self.customer_name_completer = None
        self.customer_phone_completer = None
        self.customer_mobile_completer = None
        self.customer = None
        self.all_customers = [customer for customer in fetch_inactive_customers()]
        self.all_customers_names = [customer.Επωνυμία_Επιχείρησης for customer in self.all_customers]

    def setupUi(self, enable_customer_window):
        enable_customer_window.setObjectName("enable_customer_window")
        enable_customer_window.resize(646, 387)
        enable_customer_window.setWindowTitle(f"Ενεργοποιήση πελάτη {VERSION}")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icons/add_customer.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        enable_customer_window.setWindowIcon(icon)
        self.gridLayout = QtWidgets.QGridLayout(enable_customer_window)
        self.gridLayout.setObjectName("gridLayout")
        # Font
        self.font_12_bold = QtGui.QFont()
        self.font_12_bold.setFamily("Calibri")
        self.font_12_bold.setPointSize(12)
        self.font_12_bold.setBold(True)
        self.font_12_bold.setWeight(75)
        self.font_12 = QtGui.QFont()
        self.font_12.setFamily("Calibri")
        self.font_12.setPointSize(12)

        self.customers_label = QtWidgets.QLabel(enable_customer_window)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.customers_label.sizePolicy().hasHeightForWidth())
        self.customers_label.setSizePolicy(sizePolicy)
        self.customers_label.setMaximumSize(QtCore.QSize(300, 16777215))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.customers_label.setFont(font)
        self.customers_label.setStyleSheet(u"background-color: orange;" "color: black;"
                                           "font-style: normal;font-size: 12pt;font-weight: bold;")
        self.customers_label.setAlignment(QtCore.Qt.AlignCenter)
        self.customers_label.setObjectName("customers_label")
        self.gridLayout.addWidget(self.customers_label, 0, 0, 1, 2)

        self.combo_box = QtWidgets.QComboBox(self)
        self.combo_box.setFont(self.font_12)
        self.combo_box.addItems(self.all_customers_names)

        self.customers_lineEdit = QtWidgets.QLineEdit(enable_customer_window)
        self.customers_lineEdit.setObjectName("customers_lineEdit")
        self.customers_lineEdit.setFont(self.font_12)
        self.customer_name_completer = QtWidgets.QCompleter(self.all_customers_names)
        self.combo_box.setLineEdit(self.customers_lineEdit)
        self.combo_box.currentIndexChanged.connect(self.show_customer_details)
        self.customers_lineEdit.setCompleter(self.customer_name_completer)
        self.customers_lineEdit.editingFinished.connect(self.show_customer_details)
        self.gridLayout.addWidget(self.combo_box, 0, 2, 1, 4)


        # Επωνυμία
        self.customer_name_label = QtWidgets.QLabel(enable_customer_window)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.customer_name_label.sizePolicy().hasHeightForWidth())
        self.customer_name_label.setSizePolicy(sizePolicy)
        self.customer_name_label.setMinimumSize(QtCore.QSize(0, 0))
        self.customer_name_label.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.customer_name_label.setFont(self.font_12_bold)
        self.customer_name_label.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.customer_name_label.setObjectName("customer_name_label")
        self.gridLayout.addWidget(self.customer_name_label, 1, 0, 1, 1, QtCore.Qt.AlignHCenter)
        self.customer_name_lineEdit = QtWidgets.QLineEdit(enable_customer_window)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.customer_name_lineEdit.sizePolicy().hasHeightForWidth())
        self.customer_name_lineEdit.setSizePolicy(sizePolicy)
        self.customer_name_lineEdit.setMinimumSize(QtCore.QSize(250, 0))
        self.customer_name_lineEdit.setFont(self.font_12)
        self.customer_name_lineEdit.setObjectName("customer_name_lineEdit")
        self.customer_name_lineEdit.setReadOnly(True)
        self.gridLayout.addWidget(self.customer_name_lineEdit, 1, 1, 1, 2)

        # Διεύθυνση
        self.address_label = QtWidgets.QLabel(enable_customer_window)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.address_label.sizePolicy().hasHeightForWidth())
        self.address_label.setSizePolicy(sizePolicy)
        self.address_label.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.address_label.setFont(self.font_12_bold)
        self.address_label.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.address_label.setObjectName("address_label")
        self.gridLayout.addWidget(self.address_label, 2, 0, 1, 1, QtCore.Qt.AlignHCenter)
        self.address_lineEdit = QtWidgets.QLineEdit(enable_customer_window)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.address_lineEdit.sizePolicy().hasHeightForWidth())
        self.address_lineEdit.setSizePolicy(sizePolicy)
        self.address_lineEdit.setMinimumSize(QtCore.QSize(0, 0))
        self.address_lineEdit.setFont(self.font_12)
        self.address_lineEdit.setObjectName("address_lineEdit")
        self.address_lineEdit.setReadOnly(True)
        self.gridLayout.addWidget(self.address_lineEdit, 2, 1, 1, 2)

        # Mobile
        self.mobile_label = QtWidgets.QLabel(enable_customer_window)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mobile_label.sizePolicy().hasHeightForWidth())
        self.mobile_label.setSizePolicy(sizePolicy)
        self.mobile_label.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.mobile_label.setFont(self.font_12_bold)
        self.mobile_label.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.mobile_label.setObjectName("mobile_label")
        self.gridLayout.addWidget(self.mobile_label, 3, 0, 1, 1, QtCore.Qt.AlignHCenter)
        self.mobile_lineEdit = QtWidgets.QLineEdit(enable_customer_window)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mobile_lineEdit.sizePolicy().hasHeightForWidth())
        self.mobile_lineEdit.setSizePolicy(sizePolicy)
        self.mobile_lineEdit.setFont(self.font_12)
        self.mobile_lineEdit.setObjectName("mobile_lineEdit")
        self.mobile_lineEdit.setReadOnly(True)
        self.gridLayout.addWidget(self.mobile_lineEdit, 3, 1, 1, 2)

        # Τηλέφωνο
        self.phone_label = QtWidgets.QLabel(enable_customer_window)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.phone_label.sizePolicy().hasHeightForWidth())
        self.phone_label.setSizePolicy(sizePolicy)
        self.phone_label.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.phone_label.setFont(self.font_12_bold)
        self.phone_label.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.phone_label.setObjectName("phone_label")
        self.gridLayout.addWidget(self.phone_label, 4, 0, 1, 1, QtCore.Qt.AlignHCenter)
        self.phone_lineEdit = QtWidgets.QLineEdit(enable_customer_window)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.phone_lineEdit.sizePolicy().hasHeightForWidth())
        self.phone_lineEdit.setSizePolicy(sizePolicy)
        self.phone_lineEdit.setFont(self.font_12)
        self.phone_lineEdit.setObjectName("phone_lineEdit")
        self.phone_lineEdit.setReadOnly(True)
        self.gridLayout.addWidget(self.phone_lineEdit, 4, 1, 1, 2)

        # Εmail
        self.email_label = QtWidgets.QLabel(enable_customer_window)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.email_label.sizePolicy().hasHeightForWidth())
        self.email_label.setSizePolicy(sizePolicy)
        self.email_label.setFont(self.font_12_bold)
        self.email_label.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.email_label.setObjectName("email_label")
        self.gridLayout.addWidget(self.email_label, 5, 0, 1, 1, QtCore.Qt.AlignHCenter)
        self.email_lineEdit = QtWidgets.QLineEdit(enable_customer_window)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.email_lineEdit.sizePolicy().hasHeightForWidth())
        self.email_lineEdit.setSizePolicy(sizePolicy)
        self.email_lineEdit.setFont(self.font_12)
        self.email_lineEdit.setObjectName("email_lineEdit")
        self.email_lineEdit.setReadOnly(True)
        self.gridLayout.addWidget(self.email_lineEdit, 5, 1, 1, 2)

        # Υπευθυνος
        self.responsible_label = QtWidgets.QLabel(enable_customer_window)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.responsible_label.sizePolicy().hasHeightForWidth())
        self.responsible_label.setSizePolicy(sizePolicy)
        self.responsible_label.setFont(self.font_12_bold)
        self.responsible_label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.responsible_label.setObjectName("responsible_label")
        self.gridLayout.addWidget(self.responsible_label, 1, 3, 1, 1, QtCore.Qt.AlignHCenter)
        self.responsible_lineEdit = QtWidgets.QLineEdit(enable_customer_window)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.responsible_lineEdit.sizePolicy().hasHeightForWidth())
        self.responsible_lineEdit.setSizePolicy(sizePolicy)
        self.responsible_lineEdit.setFont(self.font_12)
        self.responsible_lineEdit.setObjectName("responsible_lineEdit")
        self.responsible_lineEdit.setReadOnly(True)
        self.gridLayout.addWidget(self.responsible_lineEdit, 1, 4, 1, 1)

        # Πόλη
        self.city_label = QtWidgets.QLabel(enable_customer_window)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.city_label.sizePolicy().hasHeightForWidth())
        self.city_label.setSizePolicy(sizePolicy)
        self.city_label.setFont(self.font_12_bold)
        self.city_label.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.city_label.setObjectName("city_label")
        self.gridLayout.addWidget(self.city_label, 2, 3, 1, 1, QtCore.Qt.AlignHCenter)
        self.city_lineEdit = QtWidgets.QLineEdit(enable_customer_window)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.city_lineEdit.sizePolicy().hasHeightForWidth())
        self.city_lineEdit.setSizePolicy(sizePolicy)
        self.city_lineEdit.setFont(self.font_12)
        self.city_lineEdit.setObjectName("city_lineEdit")
        self.city_lineEdit.setReadOnly(True)
        self.gridLayout.addWidget(self.city_lineEdit, 2, 4, 1, 1)

        # Περιοχή
        self.area_label = QtWidgets.QLabel(enable_customer_window)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.area_label.sizePolicy().hasHeightForWidth())
        self.area_label.setSizePolicy(sizePolicy)
        self.area_label.setFont(self.font_12_bold)
        self.area_label.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.area_label.setObjectName("area_label")
        self.gridLayout.addWidget(self.area_label, 3, 3, 1, 1, QtCore.Qt.AlignHCenter)
        self.area_lineEdit = QtWidgets.QLineEdit(enable_customer_window)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.area_lineEdit.sizePolicy().hasHeightForWidth())
        self.area_lineEdit.setSizePolicy(sizePolicy)
        self.area_lineEdit.setFont(self.font_12)
        self.area_lineEdit.setObjectName("area_lineEdit")
        self.area_lineEdit.setReadOnly(True)
        self.gridLayout.addWidget(self.area_lineEdit, 3, 4, 1, 1)

        # Post code
        self.post_code_label = QtWidgets.QLabel(enable_customer_window)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.post_code_label.sizePolicy().hasHeightForWidth())
        self.post_code_label.setSizePolicy(sizePolicy)
        self.post_code_label.setFont(self.font_12_bold)
        self.post_code_label.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.post_code_label.setObjectName("post_code_label")
        self.gridLayout.addWidget(self.post_code_label, 4, 3, 1, 1, QtCore.Qt.AlignHCenter)
        self.post_code_lineEdit = QtWidgets.QLineEdit(enable_customer_window)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.post_code_lineEdit.sizePolicy().hasHeightForWidth())
        self.post_code_lineEdit.setSizePolicy(sizePolicy)
        self.post_code_lineEdit.setFont(self.font_12)
        self.post_code_lineEdit.setObjectName("post_code_lineEdit")
        self.post_code_lineEdit.setReadOnly(True)
        self.gridLayout.addWidget(self.post_code_lineEdit, 4, 4, 1, 1)

        # Fax
        self.fax_label = QtWidgets.QLabel(enable_customer_window)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fax_label.sizePolicy().hasHeightForWidth())
        self.fax_label.setSizePolicy(sizePolicy)
        self.fax_label.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.fax_label.setFont(self.font_12_bold)
        self.fax_label.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.fax_label.setObjectName("fax_label")
        self.gridLayout.addWidget(self.fax_label, 5, 3, 1, 1, QtCore.Qt.AlignHCenter)
        self.fax_lineEdit = QtWidgets.QLineEdit(enable_customer_window)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fax_lineEdit.sizePolicy().hasHeightForWidth())
        self.fax_lineEdit.setSizePolicy(sizePolicy)
        self.fax_lineEdit.setFont(self.font_12)
        self.fax_lineEdit.setObjectName("fax_lineEdit")
        self.fax_lineEdit.setReadOnly(True)
        self.gridLayout.addWidget(self.fax_lineEdit, 5, 4, 1, 1)

        # Σελίδες πακέτου
        self.pages_label = QtWidgets.QLabel(enable_customer_window)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pages_label.sizePolicy().hasHeightForWidth())
        self.pages_label.setSizePolicy(sizePolicy)
        self.pages_label.setFont(self.font_12_bold)
        self.pages_label.setStyleSheet("background-color: rgb(24, 124, 255);\n"
                                       "color: rgb(255, 255, 255);")
        self.pages_label.setAlignment(QtCore.Qt.AlignCenter)
        self.pages_label.setObjectName("pages_label")
        self.gridLayout.addWidget(self.pages_label, 6, 0, 1, 2)
        self.pages_lineEdit = QtWidgets.QLineEdit(enable_customer_window)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pages_lineEdit.sizePolicy().hasHeightForWidth())
        self.pages_lineEdit.setSizePolicy(sizePolicy)
        self.pages_lineEdit.setFont(self.font_12)
        self.pages_lineEdit.setObjectName("pages_lineEdit")
        self.pages_lineEdit.setReadOnly(True)
        self.gridLayout.addWidget(self.pages_lineEdit, 7, 0, 1, 2)

        # Cost of pages
        self.cost_of_pages_label = QtWidgets.QLabel(enable_customer_window)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cost_of_pages_label.sizePolicy().hasHeightForWidth())
        self.cost_of_pages_label.setSizePolicy(sizePolicy)
        self.cost_of_pages_label.setFont(self.font_12_bold)
        self.cost_of_pages_label.setStyleSheet("background-color: rgb(24, 124, 255);\n"
                                               "color: rgb(255, 255, 255);")
        self.cost_of_pages_label.setAlignment(QtCore.Qt.AlignCenter)
        self.cost_of_pages_label.setObjectName("cost_of_pages_label")
        self.gridLayout.addWidget(self.cost_of_pages_label, 6, 4, 1, 1)
        self.cost_of_pages_lineEdit = QtWidgets.QLineEdit(enable_customer_window)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cost_of_pages_lineEdit.sizePolicy().hasHeightForWidth())
        self.cost_of_pages_lineEdit.setSizePolicy(sizePolicy)
        self.cost_of_pages_lineEdit.setFont(self.font_12)
        self.cost_of_pages_lineEdit.setObjectName("cost_of_pages_lineEdit")
        self.cost_of_pages_lineEdit.setReadOnly(True)
        self.gridLayout.addWidget(self.cost_of_pages_lineEdit, 7, 4, 1, 1)

        # Σημειώσεις
        self.customer_notes_label = QtWidgets.QLabel(enable_customer_window)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.customer_notes_label.sizePolicy().hasHeightForWidth())
        self.customer_notes_label.setSizePolicy(sizePolicy)
        self.customer_notes_label.setFont(self.font_12_bold)
        self.customer_notes_label.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.customer_notes_label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.customer_notes_label.setStyleSheet("background-color: rgb(89, 89, 89);\n"
"color: rgb(255, 255, 255);")
        self.customer_notes_label.setLocale(QtCore.QLocale(QtCore.QLocale.Greek, QtCore.QLocale.Greece))
        self.customer_notes_label.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.customer_notes_label.setAlignment(QtCore.Qt.AlignCenter)
        self.customer_notes_label.setObjectName("customer_notes_label")
        self.gridLayout.addWidget(self.customer_notes_label, 8, 0, 1, 5)
        self.customer_notes_textEdit = QtWidgets.QTextEdit(enable_customer_window)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.customer_notes_textEdit.sizePolicy().hasHeightForWidth())
        self.customer_notes_textEdit.setSizePolicy(sizePolicy)
        self.customer_notes_textEdit.setFont(self.font_12)
        self.customer_notes_textEdit.setObjectName("customer_notes_textEdit")
        self.customer_notes_textEdit.setReadOnly(True)
        self.gridLayout.addWidget(self.customer_notes_textEdit, 9, 0, 1, 5)

        # Save
        self.save_customer_changes_toolButton = QtWidgets.QToolButton(enable_customer_window)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.save_customer_changes_toolButton.sizePolicy().hasHeightForWidth())
        self.save_customer_changes_toolButton.setSizePolicy(sizePolicy)
        self.save_customer_changes_toolButton.setMinimumSize(QtCore.QSize(0, 30))
        self.save_customer_changes_toolButton.setFont(self.font_12_bold)
        self.save_customer_changes_toolButton.setStyleSheet("background-color: rgb(104, 104, 104);\n"
                                                            "color: rgb(255, 255, 255);")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("icons/Save.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.save_customer_changes_toolButton.setIcon(icon1)
        self.save_customer_changes_toolButton.setIconSize(QtCore.QSize(40, 40))
        self.save_customer_changes_toolButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.save_customer_changes_toolButton.setObjectName("save_customer_changes_toolButton")
        self.save_customer_changes_toolButton.clicked.connect(self.activate_customer)
        self.gridLayout.addWidget(self.save_customer_changes_toolButton, 10, 0, 1, 2)

        # Συντομέυσεις
        # Esc
        self.shortcut_esc = QtWidgets.QShortcut(QtGui.QKeySequence('Escape'), enable_customer_window)
        self.shortcut_esc.activated.connect(lambda: self.close())

        self.retranslateUi(enable_customer_window)
        QtCore.QMetaObject.connectSlotsByName(enable_customer_window)

    def retranslateUi(self, enable_customer_window):
        _translate = QtCore.QCoreApplication.translate
        self.customers_label.setText(_translate("enable_customer_window", "Πελάτης"))
        self.responsible_label.setText(_translate("enable_customer_window", "Υπεύθυνος"))
        self.customer_name_label.setText(_translate("enable_customer_window", "Επωνυμία"))
        self.save_customer_changes_toolButton.setText(_translate("enable_customer_window", "  Αποθήκευση"))
        self.save_customer_changes_toolButton.setShortcut(_translate("enable_customer_window", "Ctrl+S"))
        self.fax_label.setText(_translate("enable_customer_window", "FAX"))
        self.area_label.setText(_translate("enable_customer_window", "Περιοχή"))
        self.email_label.setText(_translate("enable_customer_window", "E-mail"))
        self.city_label.setText(_translate("enable_customer_window", "Πόλη"))
        self.address_label.setText(_translate("enable_customer_window", "Διεύθυνση"))
        self.post_code_label.setText(_translate("enable_customer_window", "Τ.Κ."))
        self.pages_label.setText(_translate("enable_customer_window", "Σελίδες πακέτου"))
        self.mobile_label.setText(_translate("enable_customer_window", "Κινητό"))
        self.customer_notes_label.setText(_translate("enable_customer_window", "Σημειώσεις"))
        self.phone_label.setText(_translate("enable_customer_window", "Τηλέφωνο"))
        self.cost_of_pages_label.setText(_translate("enable_customer_window", "Κόστος πακέτου"))

    def activate_customer(self):
        if self.customers_lineEdit.text().replace(" ", "") == "" or not self.safe_to_save:
            self.customers_lineEdit.setStyleSheet("background-color: red;" "color: white;")
            QtWidgets.QMessageBox.warning(None, "Προσοχή", f"Παρακαλώ ελέξτε τα πεδία")
            return
        else:
            old_notes = self.customer.Σημειώσεις
            self.customer.Σημειώσεις =  f"{old_notes}" + f"\n------------- Ενεργοποιήση πελάτη {today} ----------------------"
            self.customer.Κατάσταση = 1
            service_session.commit()
            QtWidgets.QMessageBox.information(None, "Πληροφορία", f"Ο πελάτης ενεργοποιήθηκε")
            self.close()

    def show_customer_details(self):
        customer_query = get_inactive_customer_from_name(self.customers_lineEdit.text())
        if customer_query.count() > 1:
            self.safe_to_save = False
            QtWidgets.QMessageBox.critical(None, "Σφάλμα", "Βρέθηκαν πολλοί πελάτες με αυτήν την επωνυμία!")
            return
        else:
            try:
                self.customer = customer_query[0]
                self.customer_notes_textEdit.setText(self.customer.Σημειώσεις)
                self.customer_name_lineEdit.setText(self.customer.Επωνυμία_Επιχείρησης)
                self.address_lineEdit.setText(self.customer.Διεύθυνση)
                self.city_lineEdit.setText(self.customer.Πόλη)
                self.mobile_lineEdit.setText(self.customer.Κινητό)
                self.post_code_lineEdit.setText(self.customer.Ταχ_Κώδικας)
                self.responsible_lineEdit.setText(self.customer.Ονοματεπώνυμο)
                self.area_lineEdit.setText(self.customer.Περιοχή)
                self.phone_lineEdit.setText(self.customer.Τηλέφωνο)
                self.fax_lineEdit.setText(self.customer.Φαξ)
                self.email_lineEdit.setText(self.customer.E_mail)
                self.cost_of_pages_lineEdit.setText(self.customer.Κόστος_πακέτου)
                self.pages_lineEdit.setText(self.customer.Σελίδες_πακέτου)
                self.customers_lineEdit.setStyleSheet("background-color: green;" "color: white;")
                self.safe_to_save = True
            except IndexError:  # list index out of range οταν δεν υπάρχει πελάτης με αυτό το όνομα
                traceback.print_exc()
                self.customers_lineEdit.setStyleSheet("background-color: red;" "color: white;")
                self.safe_to_save = False

    def closeEvent(self, event):
        self.window_closed.emit()
        event.accept()
        # event.ignore()  # if you want the window to never be closed


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")
    enable_customer_window = QtWidgets.QWidget()
    ui = Ui_enable_customer_window()
    ui.setupUi(enable_customer_window)
    enable_customer_window.show()
    sys.exit(app.exec_())
