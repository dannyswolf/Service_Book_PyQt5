# -*- coding: utf-8 -*-
# Created by: PyQt5 UI code generator 5.15.4

import sys
import traceback
import sqlalchemy
from db import service_session, Customer, fetch_active_customers, check_if_customer_name_exist
from PyQt5 import QtCore, QtGui, QtWidgets
from settings import VERSION, root_logger

sys.stderr.write = root_logger.error
sys.stdout.write = root_logger.info

all_customers = [customer for customer in fetch_active_customers()]

all_phones = [customer.Τηλέφωνο for customer in all_customers]
str_all_phones = [str(customer.Τηλέφωνο).replace(" ", "") for customer in all_customers]
all_customers_names = [customer.Επωνυμία_Επιχείρησης for customer in all_customers]
upper_all_customers_names = [str(customer.Επωνυμία_Επιχείρησης).upper().replace(" ", "") for customer in all_customers]
all_mobiles = [customer.Κινητό for customer in all_customers]
str_all_mobiles = [str(customer.Κινητό).replace(" ", "") for customer in all_customers]


class Ui_add_new_customer_window(QtWidgets.QWidget):
    window_closed = QtCore.pyqtSignal()  # Το Signal πρεπει να είναι εκτός __init__ δεν δουλευει αλλιως

    def __init__(self):
        super().__init__()
        self.safe_to_save = True
        self.customer_name_completer = None
        self.customer_phone_completer = None
        self.customer_mobile_completer = None

    def setupUi(self, add_new_customer_window):
        add_new_customer_window.setObjectName("add_new_customer_window")
        add_new_customer_window.resize(646, 387)
        add_new_customer_window.setWindowTitle(f"Προσθήκη νέου πελάτη {VERSION}")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icons/add_customer.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        add_new_customer_window.setWindowIcon(icon)
        self.gridLayout = QtWidgets.QGridLayout(add_new_customer_window)
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

        # Επωνυμία
        self.customer_name_label = QtWidgets.QLabel(add_new_customer_window)
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
        self.gridLayout.addWidget(self.customer_name_label, 0, 0, 1, 1, QtCore.Qt.AlignHCenter)
        self.customer_name_lineEdit = QtWidgets.QLineEdit(add_new_customer_window)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.customer_name_lineEdit.sizePolicy().hasHeightForWidth())
        self.customer_name_lineEdit.setSizePolicy(sizePolicy)
        self.customer_name_lineEdit.setMinimumSize(QtCore.QSize(250, 0))
        self.customer_name_lineEdit.setFont(self.font_12)
        self.customer_name_lineEdit.setObjectName("customer_name_lineEdit")
        self.customer_name_completer = QtWidgets.QCompleter(all_customers_names)
        self.customer_name_lineEdit.setCompleter(self.customer_name_completer)
        self.customer_name_lineEdit.editingFinished.connect(self.check_customer_name)
        self.gridLayout.addWidget(self.customer_name_lineEdit, 0, 1, 1, 2)

        # Διεύθυνση
        self.address_label = QtWidgets.QLabel(add_new_customer_window)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.address_label.sizePolicy().hasHeightForWidth())
        self.address_label.setSizePolicy(sizePolicy)
        self.address_label.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.address_label.setFont(self.font_12_bold)
        self.address_label.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.address_label.setObjectName("address_label")
        self.gridLayout.addWidget(self.address_label, 1, 0, 1, 1, QtCore.Qt.AlignHCenter)
        self.address_lineEdit = QtWidgets.QLineEdit(add_new_customer_window)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.address_lineEdit.sizePolicy().hasHeightForWidth())
        self.address_lineEdit.setSizePolicy(sizePolicy)
        self.address_lineEdit.setMinimumSize(QtCore.QSize(0, 0))
        self.address_lineEdit.setFont(self.font_12)
        self.address_lineEdit.setObjectName("address_lineEdit")
        self.gridLayout.addWidget(self.address_lineEdit, 1, 1, 1, 2)

        # Mobile
        self.mobile_label = QtWidgets.QLabel(add_new_customer_window)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mobile_label.sizePolicy().hasHeightForWidth())
        self.mobile_label.setSizePolicy(sizePolicy)
        self.mobile_label.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.mobile_label.setFont(self.font_12_bold)
        self.mobile_label.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.mobile_label.setObjectName("mobile_label")
        self.gridLayout.addWidget(self.mobile_label, 2, 0, 1, 1, QtCore.Qt.AlignHCenter)
        self.mobile_lineEdit = QtWidgets.QLineEdit(add_new_customer_window)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mobile_lineEdit.sizePolicy().hasHeightForWidth())
        self.mobile_lineEdit.setSizePolicy(sizePolicy)
        self.mobile_lineEdit.setFont(self.font_12)
        self.mobile_lineEdit.setObjectName("mobile_lineEdit")
        self.customer_mobile_completer = QtWidgets.QCompleter(all_mobiles)
        self.mobile_lineEdit.setCompleter(self.customer_mobile_completer)
        self.mobile_lineEdit.editingFinished.connect(self.check_customer_mobile)
        self.gridLayout.addWidget(self.mobile_lineEdit, 2, 1, 1, 2)

        # Τηλέφωνο
        self.phone_label = QtWidgets.QLabel(add_new_customer_window)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.phone_label.sizePolicy().hasHeightForWidth())
        self.phone_label.setSizePolicy(sizePolicy)
        self.phone_label.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.phone_label.setFont(self.font_12_bold)
        self.phone_label.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.phone_label.setObjectName("phone_label")
        self.gridLayout.addWidget(self.phone_label, 3, 0, 1, 1, QtCore.Qt.AlignHCenter)
        self.phone_lineEdit = QtWidgets.QLineEdit(add_new_customer_window)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.phone_lineEdit.sizePolicy().hasHeightForWidth())
        self.phone_lineEdit.setSizePolicy(sizePolicy)
        self.phone_lineEdit.setFont(self.font_12)
        self.phone_lineEdit.setObjectName("phone_lineEdit")
        self.customer_phone_completer = QtWidgets.QCompleter(all_phones)
        self.phone_lineEdit.setCompleter(self.customer_phone_completer)
        self.phone_lineEdit.editingFinished.connect(self.check_customer_phone)
        self.gridLayout.addWidget(self.phone_lineEdit, 3, 1, 1, 2)

        # Εmail
        self.email_label = QtWidgets.QLabel(add_new_customer_window)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.email_label.sizePolicy().hasHeightForWidth())
        self.email_label.setSizePolicy(sizePolicy)
        self.email_label.setFont(self.font_12_bold)
        self.email_label.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.email_label.setObjectName("email_label")
        self.gridLayout.addWidget(self.email_label, 4, 0, 1, 1, QtCore.Qt.AlignHCenter)
        self.email_lineEdit = QtWidgets.QLineEdit(add_new_customer_window)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.email_lineEdit.sizePolicy().hasHeightForWidth())
        self.email_lineEdit.setSizePolicy(sizePolicy)
        self.email_lineEdit.setFont(self.font_12)
        self.email_lineEdit.setObjectName("email_lineEdit")
        self.gridLayout.addWidget(self.email_lineEdit, 4, 1, 1, 2)

        # Υπευθυνος
        self.responsible_label = QtWidgets.QLabel(add_new_customer_window)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.responsible_label.sizePolicy().hasHeightForWidth())
        self.responsible_label.setSizePolicy(sizePolicy)
        self.responsible_label.setFont(self.font_12_bold)
        self.responsible_label.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.responsible_label.setObjectName("responsible_label")
        self.gridLayout.addWidget(self.responsible_label, 0, 3, 1, 1, QtCore.Qt.AlignHCenter)
        self.responsible_lineEdit = QtWidgets.QLineEdit(add_new_customer_window)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.responsible_lineEdit.sizePolicy().hasHeightForWidth())
        self.responsible_lineEdit.setSizePolicy(sizePolicy)
        self.responsible_lineEdit.setFont(self.font_12)
        self.responsible_lineEdit.setObjectName("responsible_lineEdit")
        self.gridLayout.addWidget(self.responsible_lineEdit, 0, 4, 1, 1)

        # Πόλη
        self.city_label = QtWidgets.QLabel(add_new_customer_window)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.city_label.sizePolicy().hasHeightForWidth())
        self.city_label.setSizePolicy(sizePolicy)
        self.city_label.setFont(self.font_12_bold)
        self.city_label.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.city_label.setObjectName("city_label")
        self.gridLayout.addWidget(self.city_label, 1, 3, 1, 1, QtCore.Qt.AlignHCenter)
        self.city_lineEdit = QtWidgets.QLineEdit(add_new_customer_window)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.city_lineEdit.sizePolicy().hasHeightForWidth())
        self.city_lineEdit.setSizePolicy(sizePolicy)
        self.city_lineEdit.setFont(self.font_12)
        self.city_lineEdit.setObjectName("city_lineEdit")
        self.gridLayout.addWidget(self.city_lineEdit, 1, 4, 1, 1)

        # Περιοχή
        self.area_label = QtWidgets.QLabel(add_new_customer_window)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.area_label.sizePolicy().hasHeightForWidth())
        self.area_label.setSizePolicy(sizePolicy)
        self.area_label.setFont(self.font_12_bold)
        self.area_label.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.area_label.setObjectName("area_label")
        self.gridLayout.addWidget(self.area_label, 2, 3, 1, 1, QtCore.Qt.AlignHCenter)
        self.area_lineEdit = QtWidgets.QLineEdit(add_new_customer_window)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.area_lineEdit.sizePolicy().hasHeightForWidth())
        self.area_lineEdit.setSizePolicy(sizePolicy)
        self.area_lineEdit.setFont(self.font_12)
        self.area_lineEdit.setObjectName("area_lineEdit")
        self.gridLayout.addWidget(self.area_lineEdit, 2, 4, 1, 1)

        # Post code
        self.post_code_label = QtWidgets.QLabel(add_new_customer_window)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.post_code_label.sizePolicy().hasHeightForWidth())
        self.post_code_label.setSizePolicy(sizePolicy)
        self.post_code_label.setFont(self.font_12_bold)
        self.post_code_label.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.post_code_label.setObjectName("post_code_label")
        self.gridLayout.addWidget(self.post_code_label, 3, 3, 1, 1, QtCore.Qt.AlignHCenter)
        self.post_code_lineEdit = QtWidgets.QLineEdit(add_new_customer_window)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.post_code_lineEdit.sizePolicy().hasHeightForWidth())
        self.post_code_lineEdit.setSizePolicy(sizePolicy)
        self.post_code_lineEdit.setFont(self.font_12)
        self.post_code_lineEdit.setObjectName("post_code_lineEdit")
        self.gridLayout.addWidget(self.post_code_lineEdit, 3, 4, 1, 1)

        # Fax
        self.fax_label = QtWidgets.QLabel(add_new_customer_window)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fax_label.sizePolicy().hasHeightForWidth())
        self.fax_label.setSizePolicy(sizePolicy)
        self.fax_label.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.fax_label.setFont(self.font_12_bold)
        self.fax_label.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.fax_label.setObjectName("fax_label")
        self.gridLayout.addWidget(self.fax_label, 4, 3, 1, 1, QtCore.Qt.AlignHCenter)
        self.fax_lineEdit = QtWidgets.QLineEdit(add_new_customer_window)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fax_lineEdit.sizePolicy().hasHeightForWidth())
        self.fax_lineEdit.setSizePolicy(sizePolicy)
        self.fax_lineEdit.setFont(self.font_12)
        self.fax_lineEdit.setObjectName("fax_lineEdit")
        self.gridLayout.addWidget(self.fax_lineEdit, 4, 4, 1, 1)

        # Σημειώσεις
        self.customer_notes_label = QtWidgets.QLabel(add_new_customer_window)
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
        self.gridLayout.addWidget(self.customer_notes_label, 7, 0, 1, 5)
        self.customer_notes_textEdit = QtWidgets.QTextEdit(add_new_customer_window)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.customer_notes_textEdit.sizePolicy().hasHeightForWidth())
        self.customer_notes_textEdit.setSizePolicy(sizePolicy)
        self.customer_notes_textEdit.setFont(self.font_12)
        self.customer_notes_textEdit.setObjectName("customer_notes_textEdit")
        self.gridLayout.addWidget(self.customer_notes_textEdit, 8, 0, 1, 5)

        # Save
        self.save_customer_changes_toolButton = QtWidgets.QToolButton(add_new_customer_window)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.save_customer_changes_toolButton.sizePolicy().hasHeightForWidth())
        self.save_customer_changes_toolButton.setSizePolicy(sizePolicy)
        self.save_customer_changes_toolButton.setMinimumSize(QtCore.QSize(0, 30))
        self.save_customer_changes_toolButton.setFont(self.font_12_bold)
        self.save_customer_changes_toolButton.setToolTip("")
        self.save_customer_changes_toolButton.setStatusTip("")
        self.save_customer_changes_toolButton.setWhatsThis("")
        self.save_customer_changes_toolButton.setAccessibleName("")
        self.save_customer_changes_toolButton.setAccessibleDescription("")
        self.save_customer_changes_toolButton.setStyleSheet("background-color: rgb(104, 104, 104);\n"
                                                            "color: rgb(255, 255, 255);")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("icons/Save.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.save_customer_changes_toolButton.setIcon(icon1)
        self.save_customer_changes_toolButton.setIconSize(QtCore.QSize(40, 40))
        self.save_customer_changes_toolButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.save_customer_changes_toolButton.setObjectName("save_customer_changes_toolButton")
        self.save_customer_changes_toolButton.clicked.connect(self.save_new_customer)
        self.gridLayout.addWidget(self.save_customer_changes_toolButton, 9, 0, 1, 2)

        # Συντομέυσεις
        # Esc
        self.shortcut_esc = QtWidgets.QShortcut(QtGui.QKeySequence('Escape'), add_new_customer_window)
        self.shortcut_esc.activated.connect(lambda: self.close())

        self.retranslateUi(add_new_customer_window)
        QtCore.QMetaObject.connectSlotsByName(add_new_customer_window)

    def retranslateUi(self, add_new_customer_window):
        _translate = QtCore.QCoreApplication.translate
        self.responsible_label.setText(_translate("add_new_customer_window", "Υπεύθυνος"))
        self.customer_name_label.setText(_translate("add_new_customer_window", "Επωνυμία"))
        self.save_customer_changes_toolButton.setText(_translate("add_new_customer_window", "  Αποθήκευση"))
        self.save_customer_changes_toolButton.setShortcut(_translate("add_new_customer_window", "Ctrl+S"))
        self.fax_label.setText(_translate("add_new_customer_window", "FAX"))
        self.area_label.setText(_translate("add_new_customer_window", "Περιοχή"))
        self.email_label.setText(_translate("add_new_customer_window", "E-mail"))
        self.city_label.setText(_translate("add_new_customer_window", "Πόλη"))
        self.address_label.setText(_translate("add_new_customer_window", "Διεύθυνση"))
        self.post_code_label.setText(_translate("add_new_customer_window", "Τ.Κ."))
        self.mobile_label.setText(_translate("add_new_customer_window", "Κινητό"))
        self.customer_notes_label.setText(_translate("add_new_customer_window", "Σημειώσεις"))
        self.phone_label.setText(_translate("add_new_customer_window", "Τηλέφωνο"))

    def save_new_customer(self):
        if self.customer_name_lineEdit.text().replace(" ", "") == "":
            self.customer_name_lineEdit.setStyleSheet("background-color: red;\n"
                                                      "color: white;")
            QtWidgets.QMessageBox.warning(None, "Προσοχή", f"Παρακαλώ ελέξτε τα πεδία")
            self.safe_to_save = False
            return
        given_name = self.customer_name_lineEdit.text()

        new = Customer(Επωνυμία_Επιχείρησης=self.customer_name_lineEdit.text(),  # Μόνο κεφαλαία ονόματα
                       Ονοματεπώνυμο=self.responsible_lineEdit.text(), Διεύθυνση=self.address_lineEdit.text(),
                       Πόλη=self.city_lineEdit.text(), Ταχ_Κώδικας=self.post_code_lineEdit.text(),
                       Περιοχή=self.area_lineEdit.text(), Τηλέφωνο=self.phone_lineEdit.text(),
                       Κινητό=self.mobile_lineEdit.text(), Φαξ=self.fax_lineEdit.text(),
                       E_mail=self.email_lineEdit.text(),
                       Σημειώσεις=self.customer_notes_textEdit.toPlainText())
        if self.safe_to_save:
            try:
                service_session.add(new)
                service_session.commit()
                QtWidgets.QMessageBox.information(None, "Πληροφορία", "Ο πελάτης αποθηκεύτηκε")
                self.close()
                return
            except sqlalchemy.exc.IntegrityError:
                service_session.rollback()
                traceback.print_exc()
                QtWidgets.QMessageBox.warning(None, "Προσοχή", f"Error: sqlalchemy.exc.IntegrityError\n"
                                                               f"Η Επωνυμία Επιχείρησης {given_name} υπάρχει")
                return
            except Exception:
                service_session.rollback()
                traceback.print_exc()
                QtWidgets.QMessageBox.critical(None, "Σφάλμα", f"Κάτι δεν πήγε καλα!\nΟι αλλαγές δεν αποθήκευτηκαν!")
                return
        else:
            QtWidgets.QMessageBox.warning(None, "Προσοχή", f"Παρακαλώ ελέξτε τα πεδία")
            return

    def check_customer_name(self):
        given_name = self.customer_name_lineEdit.text()
        if check_if_customer_name_exist(given_name):
            self.customer_name_lineEdit.setStyleSheet("background-color: red;\n"
                                                      "color: white;")
            QtWidgets.QMessageBox.warning(None, "Προσοχή", f"Η Επωνυμία Επιχείρησης {given_name} υπάρχει")
            self.safe_to_save = False
            return
        else:
            self.customer_name_lineEdit.setStyleSheet("background-color: green;\n"
                                                      "color: white;")
            self.safe_to_save = True

    def check_customer_phone(self):
        given_phone = self.phone_lineEdit.text()

        if given_phone.replace(" ", "") in str_all_phones or len(given_phone.replace(" ", "")) < 10:
            self.phone_lineEdit.setStyleSheet("background-color: red;\n"
                                              "color: white;")
            self.safe_to_save = False
        else:
            self.phone_lineEdit.setStyleSheet("background-color: green;\n"
                                              "color: white;")
            self.safe_to_save = True

    def check_customer_mobile(self):
        mobile = self.mobile_lineEdit.text()
        if mobile.replace(" ", "") in str_all_mobiles or len(mobile.replace(" ", "")) < 10:
            self.mobile_lineEdit.setStyleSheet("background-color: red;\n"
                                               "color: white;")
            self.safe_to_save = False
        else:
            self.mobile_lineEdit.setStyleSheet("background-color: green;\n"
                                               "color: white;")
            self.safe_to_save = True

    def closeEvent(self, event):
        self.window_closed.emit()
        event.accept()
        # event.ignore()  # if you want the window to never be closed


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")
    add_new_customer_window = QtWidgets.QWidget()
    ui = Ui_add_new_customer_window()
    ui.setupUi(add_new_customer_window)
    add_new_customer_window.show()
    sys.exit(app.exec_())
