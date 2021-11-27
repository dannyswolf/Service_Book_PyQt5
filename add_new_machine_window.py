# -*- coding: utf-8 -*-

# Created by: PyQt5 UI code generator 5.15.4

import traceback
import sqlalchemy
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from db import (fetch_active_customers, Machine, check_if_customer_name_exist, get_customer_from_name, service_session,
                check_if_serial_exist, fetch_companies_data, fetch_companies_katigories_data)

from settings import VERSION, root_logger

sys.stderr.write = root_logger.error
sys.stdout.write = root_logger.info

all_customers = [customer.Επωνυμία_Επιχείρησης for customer in fetch_active_customers()]


class Ui_add_new_machine_window(QtWidgets.QWidget):
    window_closed = QtCore.pyqtSignal()  # Το Signal πρεπει να είναι εκτός __init__ δεν δουλευει αλλιως

    def __init__(self):
        super(Ui_add_new_machine_window, self).__init__()
        self.all_companies = fetch_companies_data()
        self.companies = [company[0] for company in self.all_companies]

        self.all_categories = fetch_companies_katigories_data()
        self.categories = [category[0] for category in self.all_categories]

        self.safe_to_save = False
        self.selected_customer = None
        self.customer_id = None

    def setupUi(self, add_new_machine_window):
        self.font_12 = QtGui.QFont()
        self.font_12.setFamily("Calibri")
        self.font_12.setPointSize(12)

        add_new_machine_window.setObjectName("add_new_machine_window")
        add_new_machine_window.resize(700, 332)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icons/add_machine.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        add_new_machine_window.setWindowIcon(icon)
        self.gridLayout = QtWidgets.QGridLayout(add_new_machine_window)
        self.gridLayout.setObjectName("gridLayout")
        self.customers_label = QtWidgets.QLabel(add_new_machine_window)
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
        self.gridLayout.addWidget(self.customers_label, 0, 0, 1, 1)

        self.combo_box = QtWidgets.QComboBox(self)
        self.combo_box.setFont(self.font_12)
        self.combo_box.addItems(all_customers)

        self.customers_lineEdit = QtWidgets.QLineEdit(add_new_machine_window)
        self.customers_lineEdit.setObjectName("customers_lineEdit")
        self.customers_lineEdit.setFont(self.font_12)
        # self.customer_name_completer = QtWidgets.QCompleter(all_customers)
        self.combo_box.setLineEdit(self.customers_lineEdit)

        if self.selected_customer:
            self.customers_lineEdit.setText(self.selected_customer.Επωνυμία_Επιχείρησης)
            self.customers_lineEdit.setReadOnly(True)
            self.gridLayout.addWidget(self.customers_lineEdit, 0, 1, 1, 2)
        else:
            # self.customers_lineEdit.setCompleter(self.customer_name_completer)
            self.customers_lineEdit.editingFinished.connect(self.check_customer)
            self.gridLayout.addWidget(self.combo_box, 0, 1, 1, 2)

        self.serial_number_label = QtWidgets.QLabel(add_new_machine_window)
        self.serial_number_label.setMaximumSize(QtCore.QSize(299, 16777215))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.serial_number_label.setFont(font)
        self.serial_number_label.setObjectName("serial_number_label")
        self.gridLayout.addWidget(self.serial_number_label, 1, 0, 1, 1)
        # Categories Label
        self.categories_label = QtWidgets.QLabel(add_new_machine_window)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.categories_label.setFont(font)
        self.categories_label.setObjectName("categories_label")
        self.gridLayout.addWidget(self.categories_label, 1, 1, 1, 1)


        self.copier_model_label = QtWidgets.QLabel(add_new_machine_window)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.copier_model_label.setFont(font)
        self.copier_model_label.setObjectName("copier_model_label")
        self.gridLayout.addWidget(self.copier_model_label, 1, 2, 1, 1)
        self.serial_number_lineEdit = QtWidgets.QLineEdit(add_new_machine_window)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.serial_number_lineEdit.sizePolicy().hasHeightForWidth())
        self.serial_number_lineEdit.setSizePolicy(sizePolicy)
        self.serial_number_lineEdit.setMaximumSize(QtCore.QSize(299, 16777215))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.serial_number_lineEdit.setFont(font)
        self.serial_number_lineEdit.setObjectName("serial_number_lineEdit")
        self.serial_number_lineEdit.editingFinished.connect(self.check_machine)
        self.gridLayout.addWidget(self.serial_number_lineEdit, 2, 0, 1, 1)
        # Categories
        self.categories_lineEdit = QtWidgets.QLineEdit(add_new_machine_window)
        self.categories_lineEdit.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.categories_lineEdit.setFont(font)
        self.categories_lineEdit.setObjectName("copier_model_lineEdit")
        # Categories combobox
        self.categories_combobox = QtWidgets.QComboBox(self)
        self.categories_combobox.setFont(font)
        self.categories_combobox.setMinimumSize(250, 35)
        self.categories_combobox.addItems(self.categories)
        self.categories_combobox.setLineEdit(self.categories_lineEdit)
        self.gridLayout.addWidget(self.categories_combobox, 2, 1, 1, 1)

        self.copier_model_lineEdit = QtWidgets.QLineEdit(add_new_machine_window)
        self.copier_model_lineEdit.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.copier_model_lineEdit.setFont(font)
        self.copier_model_lineEdit.setObjectName("copier_model_lineEdit")
        self.copier_model_lineEdit.editingFinished.connect(self.check_machine)

        self.companies_combobox = QtWidgets.QComboBox(self)
        self.companies_combobox.setFont(font)
        self.companies_combobox.setMinimumSize(250, 35)
        self.companies_combobox.addItems(self.companies)
        self.companies_combobox.setLineEdit(self.copier_model_lineEdit)
        self.gridLayout.addWidget(self.companies_combobox, 2, 2, 1, 1)

        self.start_counter_label = QtWidgets.QLabel(add_new_machine_window)
        self.start_counter_label.setMaximumSize(QtCore.QSize(305, 16777215))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.start_counter_label.setFont(font)
        self.start_counter_label.setObjectName("start_counter_label")
        self.gridLayout.addWidget(self.start_counter_label, 3, 0, 1, 1)
        self.start_date_label = QtWidgets.QLabel(add_new_machine_window)
        self.start_date_label.setMaximumSize(QtCore.QSize(147, 16777215))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.start_date_label.setFont(font)
        self.start_date_label.setObjectName("start_date_label")
        self.gridLayout.addWidget(self.start_date_label, 3, 1, 1, 1)
        self.start_counter_lineEdit = QtWidgets.QLineEdit(add_new_machine_window)
        self.start_counter_lineEdit.setMaximumSize(QtCore.QSize(299, 16777215))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.start_counter_lineEdit.setFont(font)
        self.start_counter_lineEdit.setObjectName("start_counter_lineEdit")
        self.gridLayout.addWidget(self.start_counter_lineEdit, 4, 0, 1, 1)
        self.started_date_dateEdit = QtWidgets.QDateEdit(add_new_machine_window)
        self.started_date_dateEdit.setMaximumSize(QtCore.QSize(147, 16777215))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.started_date_dateEdit.setFont(font)
        self.started_date_dateEdit.setCalendarPopup(True)
        self.started_date_dateEdit.setObjectName("started_date_dateEdit")
        self.started_date_dateEdit.setDate(QtCore.QDate.currentDate())
        self.gridLayout.addWidget(self.started_date_dateEdit, 4, 1, 1, 1)
        self.copiers_notes_textEdit = QtWidgets.QTextEdit(add_new_machine_window)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.copiers_notes_textEdit.setFont(font)
        self.copiers_notes_textEdit.setObjectName("copiers_notes_textEdit")
        self.gridLayout.addWidget(self.copiers_notes_textEdit, 6, 0, 1, 3)
        self.save_new_copier_toolButton = QtWidgets.QToolButton(add_new_machine_window)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.save_new_copier_toolButton.sizePolicy().hasHeightForWidth())
        self.save_new_copier_toolButton.setSizePolicy(sizePolicy)
        self.save_new_copier_toolButton.setMinimumSize(QtCore.QSize(0, 30))
        self.save_new_copier_toolButton.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.save_new_copier_toolButton.setFont(font)
        self.save_new_copier_toolButton.setStyleSheet("background-color: rgb(104, 104, 104);\n"
"color: rgb(255, 255, 255);")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("icons/Save.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.save_new_copier_toolButton.setIcon(icon1)
        self.save_new_copier_toolButton.setIconSize(QtCore.QSize(40, 40))
        self.save_new_copier_toolButton.setShortcut("Ctrl+S")
        self.save_new_copier_toolButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.save_new_copier_toolButton.setAutoRaise(False)
        self.save_new_copier_toolButton.setObjectName("save_new_copier_toolButton")
        self.save_new_copier_toolButton.clicked.connect(self.save_new_machine)
        self.gridLayout.addWidget(self.save_new_copier_toolButton, 7, 0, 1, 2, QtCore.Qt.AlignHCenter)
        self.copier_notes_label = QtWidgets.QLabel(add_new_machine_window)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(13)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.copier_notes_label.setFont(font)
        self.copier_notes_label.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.copier_notes_label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.copier_notes_label.setStyleSheet("background-color: rgb(89, 89, 89);\n"
"color: rgb(255, 255, 255);")
        self.copier_notes_label.setLocale(QtCore.QLocale(QtCore.QLocale.Greek, QtCore.QLocale.Greece))
        self.copier_notes_label.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.copier_notes_label.setAlignment(QtCore.Qt.AlignCenter)
        self.copier_notes_label.setObjectName("copier_notes_label")
        self.gridLayout.addWidget(self.copier_notes_label, 5, 0, 1, 3)

        # Esc
        self.shortcut_esc = QtWidgets.QShortcut(QtGui.QKeySequence('Escape'), add_new_machine_window)
        self.shortcut_esc.activated.connect(self.close)

        self.retranslateUi(add_new_machine_window)
        QtCore.QMetaObject.connectSlotsByName(add_new_machine_window)

    def retranslateUi(self, add_new_machine_window):
        _translate = QtCore.QCoreApplication.translate
        add_new_machine_window.setWindowTitle(_translate("add_new_machine_window", f"Προσθήκη μηχανήματος {VERSION}"))
        if self.selected_customer:
            self.customers_label.setText(_translate("add_new_machine_window", "Πελάτης"))
        else:
            self.customers_label.setText(_translate("add_new_machine_window", "Πελατολόγιο"))
        self.serial_number_label.setText(_translate("add_new_machine_window", "Σειριακός αριθμός"))
        self.categories_label.setText(_translate("add_new_machine_window", "Κατηγορία - Μηχανήματος"))
        self.copier_model_label.setText(_translate("add_new_machine_window", "Εταιρεία - Μοντέλο"))
        self.start_counter_label.setText(_translate("add_new_machine_window", "Μετρητής Εναρξης"))
        self.start_date_label.setText(_translate("add_new_machine_window", "Ημηρομηνία  εναρξης"))
        self.save_new_copier_toolButton.setText(_translate("add_new_machine_window", "  Αποθήκευση"))
        self.copier_notes_label.setText(_translate("add_new_machine_window", "Σημειώσεις"))

    def save_new_machine(self):
        self.check_customer()
        self.check_machine()
        if self.safe_to_save:
            try:
                new_machine = Machine(Εταιρεία=self.categories_lineEdit.text() + "  " + self.copier_model_lineEdit.text().upper(),
                                      Serial=self.serial_number_lineEdit.text().replace(" ", "").upper(),
                                      Εναρξη=self.started_date_dateEdit.date().toString('dd/MM/yyyy'),
                                      Μετρητής_έναρξης=self.start_counter_lineEdit.text(),
                                      Σημειώσεις=self.copiers_notes_textEdit.toPlainText(), Πελάτη_ID=self.customer_id)
                service_session.add(new_machine)
                service_session.commit()
                QtWidgets.QMessageBox.information(None, "Πληροφορία", "Το μηχάνημα αποθηκεύτηκε!")
                self.close()
            except sqlalchemy.exc.IntegrityError as error:
                print(__name__, "Γραμμή: ", 248)
                print("ERROR ", error)
                traceback.print_exc()
                QtWidgets.QMessageBox.critical(None, "Σφάλμα!", "Error: sqlalchemy.exc.IntegrityError\n"
                                                                "Παρακαλώ ελέξτε τα κόκκινα πεδία"
                                                                f"\n{error}")
                return
            except Exception:
                service_session.rollback()
                traceback.print_exc()
                QtWidgets.QMessageBox.critical(None, "Σφάλμα!", "Κάτι δεν πήγε καλά!\nΤο μηχάνημα ΔΕΝ αποθηκεύτηκε!")
                return

    def check_customer(self):
        # Αν υπάρχει ο πελάτης
        # Αν έχουμε επιλεγμένο πελάτη απο το service_book_main δεν χρειαζεται να παρουμε το ID το εχουμε
        if self.selected_customer:
            self.customer_id = self.selected_customer.ID
            self.safe_to_save = True
            return
        else:
            if check_if_customer_name_exist(self.customers_lineEdit.text()):

                customer = get_customer_from_name(self.customers_lineEdit.text())
                # To get the number of entities represented by the query you can use the count method:
                if customer.count() > 1:  # Αν Βρέθηκαν πολλοί πελάτες
                    self.safe_to_save = False
                    QtWidgets.QMessageBox.critical(None, "Σφάλμα", "Βρέθηκαν πολλοί πελάτες με αυτήν την επωνυμία!")
                    return
                else:
                    self.customer_id = customer[0].ID
                    self.customers_lineEdit.setStyleSheet("background-color: green;\n"
                                                          "color: white;")
                    self.safe_to_save = True
            else:
                self.customers_lineEdit.setStyleSheet("background-color: red;\n"
                                                      "color: white;")
                self.safe_to_save = False

    def check_machine(self):
        if len(self.serial_number_lineEdit.text().replace(" ", "")) < 1 or \
                check_if_serial_exist(self.serial_number_lineEdit.text().replace(" ", "").upper()):
            self.serial_number_lineEdit.setStyleSheet("background-color: red;\n"
                                                      "color: white;")
            self.safe_to_save = False
            return

        else:
            self.serial_number_lineEdit.setStyleSheet("background-color: green;\n"
                                                      "color: white;")
            self.safe_to_save = True

            if len(self.copier_model_lineEdit.text().replace(" ", "")) < 3:
                self.copier_model_lineEdit.setStyleSheet("background-color: red;\n"
                                                          "color: white;")
                self.safe_to_save = False

            else:
                self.copier_model_lineEdit.setStyleSheet("background-color: green;\n"
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
    add_new_machine_window = QtWidgets.QWidget()
    ui = Ui_add_new_machine_window()
    ui.setupUi(add_new_machine_window)
    add_new_machine_window.show()
    sys.exit(app.exec_())
