# -*- coding: utf-8 -*-
# Created by: PyQt5 UI code generator 5.15.4
import traceback
import sys
from db import (fetch_service_reasons, fetch_service_actions, fetch_companies_data, Service_data, Companies, service_session,
                check_if_reason_service_data_exist, check_if_actions_service_data_exist, check_if_company_exist,
                fetch_companies_katigories_data, check_if_category_exist, fetch_service_technicians, check_if_technician_service_data_exist)
from PyQt5 import QtCore, QtGui, QtWidgets
from settings import VERSION, root_logger


sys.stderr.write = root_logger.error
sys.stdout.write = root_logger.info


class Ui_Edit_Service_Data_Window(QtWidgets.QWidget):
    window_closed = QtCore.pyqtSignal()  # Το Signal πρεπει να είναι εκτός __init__ δεν δουλευει αλλιως

    def __init__(self):
        super(Ui_Edit_Service_Data_Window, self).__init__()
        self.all_service_reasons = fetch_service_reasons()
        self.service_reasons = [reason[0] for reason in self.all_service_reasons]
        self.all_service_actions = fetch_service_actions()
        self.service_actions = [action[0] for action in self.all_service_actions]
        self.all_companies = fetch_companies_data()
        self.companies = [company[0] for company in self.all_companies]
        self.all_categories = fetch_companies_katigories_data()
        self.categories = [category[0] for category in self.all_categories]
        self.all_technicians = fetch_service_technicians()
        self.technicians = [technician[0] for technician in self.all_technicians]

        self.font_13 = QtGui.QFont()
        self.font_13.setFamily("Calibri")
        self.font_13.setPointSize(13)
        self.font_13.setBold(False)
        self.font_13.setWeight(50)


        self.font_13_bold = QtGui.QFont()
        self.font_13_bold.setFamily("Calibri")
        self.font_13_bold.setPointSize(14)
        self.font_13_bold.setBold(True)
        self.font_13_bold.setWeight(75)

    def setupUi(self, Edit_Service_Data_Window):
        Edit_Service_Data_Window.setObjectName("Edit_Service_Data_Window")
        # Edit_Service_Data_Window.setWindowModality(QtCore.Qt.WindowModal)
        # Edit_Service_Data_Window.resize(637, 350)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icons/icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Edit_Service_Data_Window.setWindowIcon(icon)
        self.gridLayout = QtWidgets.QGridLayout(Edit_Service_Data_Window)
        self.gridLayout.setObjectName("gridLayout")
        self.top_label = QtWidgets.QLabel(Edit_Service_Data_Window)
        self.top_label.setMinimumSize(QtCore.QSize(0, 30))
        self.top_label.setMaximumSize(QtCore.QSize(16777215, 40))

        self.top_label.setFont(self.font_13_bold)
        self.top_label.setStyleSheet("background-color: rgb(0, 85, 127);\n"
                                     "color: rgb(255, 255, 255);")
        self.top_label.setAlignment(QtCore.Qt.AlignCenter)
        self.top_label.setObjectName("top_label")
        self.gridLayout.addWidget(self.top_label, 0, 0, 1, 6)
        self.reason_label = QtWidgets.QLabel(Edit_Service_Data_Window)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.reason_label.sizePolicy().hasHeightForWidth())
        self.reason_label.setSizePolicy(sizePolicy)
        self.reason_label.setMinimumSize(QtCore.QSize(0, 25))
        self.reason_label.setMaximumSize(QtCore.QSize(16777215, 35))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.reason_label.setFont(font)
        self.reason_label.setStyleSheet("background-color: rgb(93, 93, 93);\n"
                                        "color: rgb(255, 255, 255);")
        self.reason_label.setAlignment(QtCore.Qt.AlignCenter)
        self.reason_label.setObjectName("reason_label")
        self.gridLayout.addWidget(self.reason_label, 1, 0, 1, 6)

        # Τεχνικός label
        self.technician_label = QtWidgets.QLabel(Edit_Service_Data_Window)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.reason_label.sizePolicy().hasHeightForWidth())
        self.technician_label.setSizePolicy(sizePolicy)
        self.technician_label.setMinimumSize(QtCore.QSize(0, 25))
        self.technician_label.setMaximumSize(QtCore.QSize(16777215, 35))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.technician_label.setFont(font)
        self.technician_label.setStyleSheet("background-color: rgb(93, 93, 93);\n"
                                        "color: rgb(255, 255, 255);")
        self.technician_label.setAlignment(QtCore.Qt.AlignCenter)
        self.technician_label.setObjectName("technician_label")
        self.gridLayout.addWidget(self.technician_label, 9, 0, 1, 6)

        # Reason Edit
        self.reason_lineEdit = QtWidgets.QLineEdit(Edit_Service_Data_Window)
        self.reason_lineEdit.setMinimumSize(QtCore.QSize(0, 35))
        self.reason_lineEdit.setFont(self.font_13)
        self.reason_lineEdit.setObjectName("reason_lineEdit")
        self.reason_combobox = QtWidgets.QComboBox(self)
        self.reason_combobox.setFont(self.font_13)
        self.reason_combobox.setMinimumSize(300, 35)
        self.reason_combobox.addItems(self.service_reasons)
        self.reason_combobox.setLineEdit(self.reason_lineEdit)
        self.reason_completer = QtWidgets.QCompleter(self.service_reasons)
        self.reason_completer.popup().setFont(self.font_13)
        self.reason_lineEdit.setCompleter(self.reason_completer)
        self.gridLayout.addWidget(self.reason_combobox, 2, 0, 1, 1)

        # Actions Edit
        self.actions_lineEdit = QtWidgets.QLineEdit(Edit_Service_Data_Window)
        self.actions_lineEdit.setMinimumSize(QtCore.QSize(0, 35))
        self.actions_lineEdit.setFont(self.font_13)
        self.actions_lineEdit.setObjectName("actions_lineEdit")
        self.actions_combobox = QtWidgets.QComboBox(self)
        self.actions_combobox.setFont(self.font_13)
        self.actions_combobox.setMinimumSize(300, 35)
        self.actions_combobox.addItems(self.service_actions)
        self.actions_combobox.setLineEdit(self.actions_lineEdit)
        self.actions_completer = QtWidgets.QCompleter(self.service_actions)
        self.actions_completer.popup().setFont(self.font_13)
        self.actions_lineEdit.setCompleter(self.actions_completer)
        self.gridLayout.addWidget(self.actions_combobox, 4, 0, 1, 1)

        # Company Edit
        self.company_lineEdit = QtWidgets.QLineEdit(Edit_Service_Data_Window)
        self.company_lineEdit.setMinimumSize(QtCore.QSize(0, 35))

        self.company_lineEdit.setFont(self.font_13)
        self.company_lineEdit.setObjectName("company_lineEdit")
        self.companies_combobox = QtWidgets.QComboBox(self)
        self.companies_combobox.setFont(self.font_13)
        self.companies_combobox.setMinimumSize(300, 35)
        self.companies_combobox.addItems(self.companies)
        self.companies_combobox.setLineEdit(self.company_lineEdit)
        self.companies_completer = QtWidgets.QCompleter(self.companies)
        self.companies_completer.popup().setFont(self.font_13)
        self.company_lineEdit.setCompleter(self.companies_completer)
        self.gridLayout.addWidget(self.companies_combobox, 6, 0, 1, 1)

        # Κατηγορία_μηχανήματος
        self.category_lineEdit = QtWidgets.QLineEdit(Edit_Service_Data_Window)
        self.category_lineEdit.setMinimumSize(QtCore.QSize(0, 35))
        self.category_lineEdit.setFont(self.font_13)
        self.category_lineEdit.setObjectName("category_lineEdit")
        self.categories_combobox = QtWidgets.QComboBox(self)
        self.categories_combobox.setFont(self.font_13)
        self.categories_combobox.setMinimumSize(300, 35)
        self.categories_combobox.addItems(self.categories)
        self.categories_combobox.setLineEdit(self.category_lineEdit)
        self.catigories_completer = QtWidgets.QCompleter(self.categories)
        self.catigories_completer.popup().setFont(self.font_13)
        self.gridLayout.addWidget(self.categories_combobox, 8, 0, 1, 1)

        # technician Edit
        self.technician_lineEdit = QtWidgets.QLineEdit(Edit_Service_Data_Window)
        self.technician_lineEdit.setMinimumSize(QtCore.QSize(0, 35))
        self.technician_lineEdit.setFont(self.font_13)
        self.technician_lineEdit.setObjectName("technician_lineEdit")
        self.technician_combobox = QtWidgets.QComboBox(self)
        self.technician_combobox.setFont(self.font_13)
        self.technician_combobox.setMinimumSize(300, 35)
        self.technician_combobox.addItems(self.technicians)
        self.technician_combobox.setLineEdit(self.technician_lineEdit)
        self.technician_completer = QtWidgets.QCompleter(self.technicians)
        self.technician_completer.popup().setFont(self.font_13)
        self.technician_lineEdit.setCompleter(self.technician_completer)
        self.gridLayout.addWidget(self.technician_combobox, 10, 0, 1, 1)
        # Delete technician
        self.delete_technician_toolButton = QtWidgets.QToolButton(Edit_Service_Data_Window)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.delete_technician_toolButton.setFont(font)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("icons/remove_from_list.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.delete_technician_toolButton.setIcon(icon1)
        self.delete_technician_toolButton.setIconSize(QtCore.QSize(30, 30))
        self.delete_technician_toolButton.setObjectName("delete_reason_toolButton")
        self.delete_technician_toolButton.clicked.connect(self.delete_technician)
        self.gridLayout.addWidget(self.delete_technician_toolButton, 10, 4, 1, 1)
        # Save technician
        self.save_technician_toolButton = QtWidgets.QToolButton(Edit_Service_Data_Window)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.save_technician_toolButton.setFont(font)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("icons/add_to_service_data2.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.save_technician_toolButton.setIcon(icon2)
        self.save_technician_toolButton.setIconSize(QtCore.QSize(30, 30))
        self.save_technician_toolButton.setObjectName("save_reason_toolButton")
        self.save_technician_toolButton.clicked.connect(self.save_technician_to_db)
        self.gridLayout.addWidget(self.save_technician_toolButton, 10, 1, 1, 3)

        # Delete Reason
        self.delete_reason_toolButton = QtWidgets.QToolButton(Edit_Service_Data_Window)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.delete_reason_toolButton.setFont(font)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("icons/remove_from_list.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.delete_reason_toolButton.setIcon(icon1)
        self.delete_reason_toolButton.setIconSize(QtCore.QSize(30, 30))
        self.delete_reason_toolButton.setObjectName("delete_reason_toolButton")
        self.delete_reason_toolButton.clicked.connect(self.delete_reason)
        self.gridLayout.addWidget(self.delete_reason_toolButton, 2, 4, 1, 1)

        # Save Reason
        self.save_reason_toolButton = QtWidgets.QToolButton(Edit_Service_Data_Window)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.save_reason_toolButton.setFont(font)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("icons/add_to_service_data2.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.save_reason_toolButton.setIcon(icon2)
        self.save_reason_toolButton.setIconSize(QtCore.QSize(30, 30))
        self.save_reason_toolButton.setObjectName("save_reason_toolButton")
        self.save_reason_toolButton.clicked.connect(self.save_reason_to_db)
        self.gridLayout.addWidget(self.save_reason_toolButton, 2, 1, 1, 3)

        # Save Company
        self.save_company_toolButton = QtWidgets.QToolButton(Edit_Service_Data_Window)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.save_company_toolButton.setFont(font)
        self.save_company_toolButton.setIcon(icon2)
        self.save_company_toolButton.setIconSize(QtCore.QSize(30, 30))
        self.save_company_toolButton.setObjectName("save_company_toolButton")
        self.save_company_toolButton.clicked.connect(self.save_company_to_db)
        self.gridLayout.addWidget(self.save_company_toolButton, 6, 1, 1, 1)

        self.company_label = QtWidgets.QLabel(Edit_Service_Data_Window)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.company_label.sizePolicy().hasHeightForWidth())
        self.company_label.setSizePolicy(sizePolicy)
        self.company_label.setMinimumSize(QtCore.QSize(0, 25))
        self.company_label.setMaximumSize(QtCore.QSize(16777215, 35))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.company_label.setFont(font)
        self.company_label.setStyleSheet("background-color: rgb(93, 93, 93);\n"
                                         "color: rgb(255, 255, 255);")
        self.company_label.setAlignment(QtCore.Qt.AlignCenter)
        self.company_label.setObjectName("company_label")
        self.gridLayout.addWidget(self.company_label, 5, 0, 1, 6)

        # Categories
        self.categories_label = QtWidgets.QLabel(Edit_Service_Data_Window)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.company_label.sizePolicy().hasHeightForWidth())
        self.categories_label.setSizePolicy(sizePolicy)
        self.categories_label.setMinimumSize(QtCore.QSize(0, 25))
        self.categories_label.setMaximumSize(QtCore.QSize(16777215, 35))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.categories_label.setFont(font)
        self.categories_label.setStyleSheet("background-color: rgb(93, 93, 93);\n"
                                         "color: rgb(255, 255, 255);")
        self.categories_label.setAlignment(QtCore.Qt.AlignCenter)
        self.categories_label.setObjectName("categories_label")
        self.gridLayout.addWidget(self.categories_label, 7, 0, 1, 6)

        # Delete Company
        self.delete_company_toolButton = QtWidgets.QToolButton(Edit_Service_Data_Window)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.delete_company_toolButton.setFont(font)
        self.delete_company_toolButton.setIcon(icon1)
        self.delete_company_toolButton.setIconSize(QtCore.QSize(30, 30))
        self.delete_company_toolButton.setObjectName("delete_company_toolButton")
        self.delete_company_toolButton.clicked.connect(self.delete_company)
        self.gridLayout.addWidget(self.delete_company_toolButton, 6, 4, 1, 1)


        self.actions_label = QtWidgets.QLabel(Edit_Service_Data_Window)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.actions_label.sizePolicy().hasHeightForWidth())
        self.actions_label.setSizePolicy(sizePolicy)
        self.actions_label.setMinimumSize(QtCore.QSize(0, 25))
        self.actions_label.setMaximumSize(QtCore.QSize(16777215, 35))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.actions_label.setFont(font)
        self.actions_label.setStyleSheet("background-color: rgb(93, 93, 93);\n"
                                         "color: rgb(255, 255, 255);")
        self.actions_label.setAlignment(QtCore.Qt.AlignCenter)
        self.actions_label.setObjectName("actions_label")
        self.gridLayout.addWidget(self.actions_label, 3, 0, 1, 6)

        # Save actions
        self.save_actions_toolButton = QtWidgets.QToolButton(Edit_Service_Data_Window)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.save_actions_toolButton.setFont(font)
        self.save_actions_toolButton.setIcon(icon2)
        self.save_actions_toolButton.setIconSize(QtCore.QSize(30, 30))
        self.save_actions_toolButton.setObjectName("save_actions_toolButton")
        self.save_actions_toolButton.clicked.connect(self.save_action_to_db)
        self.gridLayout.addWidget(self.save_actions_toolButton, 4, 1, 1, 1)
        self.delete_actions_toolButton = QtWidgets.QToolButton(Edit_Service_Data_Window)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.delete_actions_toolButton.setFont(font)
        self.delete_actions_toolButton.setIcon(icon1)
        self.delete_actions_toolButton.setIconSize(QtCore.QSize(30, 30))
        self.delete_actions_toolButton.setObjectName("delete_actions_toolButton")
        self.delete_actions_toolButton.clicked.connect(self.delete_action)
        self.gridLayout.addWidget(self.delete_actions_toolButton, 4, 4, 1, 1)

        # Save category
        self.save_category_toolButton = QtWidgets.QToolButton(Edit_Service_Data_Window)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.save_category_toolButton.setFont(font)
        self.save_category_toolButton.setIcon(icon2)
        self.save_category_toolButton.setIconSize(QtCore.QSize(30, 30))
        self.save_category_toolButton.setObjectName("save_actions_toolButton")
        self.save_category_toolButton.clicked.connect(self.save_category_to_db)
        self.gridLayout.addWidget(self.save_category_toolButton, 8, 1, 1, 1)
        # Delete category
        self.delete_category_toolButton = QtWidgets.QToolButton(Edit_Service_Data_Window)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.delete_category_toolButton.setFont(font)
        self.delete_category_toolButton.setIcon(icon1)
        self.delete_category_toolButton.setIconSize(QtCore.QSize(30, 30))
        self.delete_category_toolButton.setObjectName("delete_company_toolButton")
        self.delete_category_toolButton.clicked.connect(self.delete_category)
        self.gridLayout.addWidget(self.delete_category_toolButton, 8, 4, 1, 1)

        # Esc
        self.shortcut_esc = QtWidgets.QShortcut(QtGui.QKeySequence('Escape'), Edit_Service_Data_Window)
        self.shortcut_esc.activated.connect(self.close)

        self.retranslateUi(Edit_Service_Data_Window)
        QtCore.QMetaObject.connectSlotsByName(Edit_Service_Data_Window)

    def retranslateUi(self, Edit_Service_Data_Window):
        _translate = QtCore.QCoreApplication.translate
        Edit_Service_Data_Window.setWindowTitle(_translate("Edit_Service_Data_Window", f"Ρυθμίσεις Δεδομένων {VERSION}"))
        self.top_label.setText(_translate("Edit_Service_Data_Window", "Ρυθμήσεις Δεδομένων"))
        self.reason_label.setText(_translate("Edit_Service_Data_Window", "Περιγραφή Προβλήματος"))
        self.delete_reason_toolButton.setText(_translate("Edit_Service_Data_Window", "..."))
        self.save_company_toolButton.setText(_translate("Edit_Service_Data_Window", "..."))
        self.company_label.setText(_translate("Edit_Service_Data_Window", "Εταιρείες"))
        self.categories_label.setText(_translate("Edit_Service_Data_Window", "Κατηγορίες μηχανημάτων"))
        self.technician_label.setText(_translate("Edit_Service_Data_Window", "Τεχνικοί"))
        self.delete_company_toolButton.setText(_translate("Edit_Service_Data_Window", "..."))
        self.actions_label.setText(_translate("Edit_Service_Data_Window", "Ενέργεις Επισκευής"))
        self.save_actions_toolButton.setText(_translate("Edit_Service_Data_Window", "..."))
        self.delete_actions_toolButton.setText(_translate("Edit_Service_Data_Window", "..."))

    def refresh_all_data(self):
        self.all_service_reasons = fetch_service_reasons()
        self.service_reasons = [reason[0] for reason in self.all_service_reasons]
        self.reason_combobox.clear()
        self.reason_completer = QtWidgets.QCompleter(self.service_reasons)
        self.reason_completer.popup().setFont(self.font_13)
        self.reason_combobox.addItems(self.service_reasons)

        self.all_service_actions = fetch_service_actions()
        self.service_actions = [action[0] for action in self.all_service_actions]
        self.actions_combobox.clear()
        self.actions_completer = QtWidgets.QCompleter(self.service_actions)
        self.actions_completer.popup().setFont(self.font_13)
        self.actions_combobox.addItems(self.service_actions)

        self.all_companies = fetch_companies_data()
        self.companies = [company[0] for company in self.all_companies]
        self.companies_combobox.clear()
        self.companies_completer_completer = QtWidgets.QCompleter(self.companies)
        self.companies_completer_completer.popup().setFont(self.font_13)
        self.companies_combobox.addItems(self.companies)

        self.all_categories = fetch_companies_katigories_data()
        self.categories = [category[0] for category in self.all_categories]
        self.categories_combobox.clear()
        self.catigories_completer = QtWidgets.QCompleter(self.categories)
        self.catigories_completer.popup().setFont(self.font_13)
        self.categories_combobox.addItems(self.categories)

        self.all_technicians = fetch_service_technicians()
        self.technicians = [technician[0] for technician in self.all_technicians]
        self.technician_combobox.clear()
        self.technician_completer = QtWidgets.QCompleter(self.technicians)
        self.technician_completer.popup().setFont(self.font_13)
        self.technician_combobox.addItems(self.technicians)

    def save_reason_to_db(self):
        try:
            if check_if_reason_service_data_exist(self.reason_lineEdit.text().upper()):
                QtWidgets.QMessageBox.warning(None, "Προσοχή", f"Το '{self.reason_lineEdit.text().upper()}' υπάρχει")
                return
            reason = Service_data(Σκοπός=self.reason_lineEdit.text().upper())
            service_session.add(reason)
            service_session.commit()
            self.refresh_all_data()
            QtWidgets.QMessageBox.information(None, "Πληροφορία!", "Αποθηκεύτηκε")
        except Exception:
            service_session.rollback()
            traceback.print_exc()
            QtWidgets.QMessageBox.critical(None, "Σφάλμα!", "Κάτι δεν πήγε καλά τίποτα ΔΕΝ αποθηκεύτηκε")
            return

    def save_action_to_db(self):
        try:
            if check_if_actions_service_data_exist(self.actions_lineEdit.text().upper()):
                QtWidgets.QMessageBox.warning(None, "Προσοχή", f"Το '{self.actions_lineEdit.text().upper()}' υπάρχει")
                return
            action = Service_data(Ενέργειες=self.actions_lineEdit.text().upper())
            service_session.add(action)
            service_session.commit()
            self.refresh_all_data()
            QtWidgets.QMessageBox.information(None, "Πληροφορία!", "Αποθηκεύτηκε")
        except Exception:
            service_session.rollback()
            traceback.print_exc()
            QtWidgets.QMessageBox.critical(None, "Σφάλμα!", "Κάτι δεν πήγε καλά τίποτα ΔΕΝ αποθηκεύτηκε")
            return

    def save_company_to_db(self):
        try:
            if check_if_company_exist(self.company_lineEdit.text().upper()):
                QtWidgets.QMessageBox.warning(None, "Προσοχή", f"Το '{self.company_lineEdit.text().upper()}' υπάρχει")
                return
            company = Companies(Εταιρεία=self.company_lineEdit.text().upper())
            service_session.add(company)
            service_session.commit()
            self.refresh_all_data()
            QtWidgets.QMessageBox.information(None, "Πληροφορία!", "Αποθηκεύτηκε")
        except Exception:
            service_session.rollback()
            traceback.print_exc()
            QtWidgets.QMessageBox.critical(None, "Σφάλμα!", "Κάτι δεν πήγε καλά τίποτα ΔΕΝ αποθηκεύτηκε")
            return

    def save_category_to_db(self):
        try:
            if check_if_category_exist(self.category_lineEdit.text().upper()):
                QtWidgets.QMessageBox.warning(None, "Προσοχή", f"H Κατηγορία '{self.category_lineEdit.text().upper()}' υπάρχει")
                return
            category = Companies(Κατηγορία_μηχανήματος=self.category_lineEdit.text().upper())
            service_session.add(category)
            service_session.commit()
            self.refresh_all_data()
            QtWidgets.QMessageBox.information(None, "Πληροφορία!", "Αποθηκεύτηκε")
        except Exception:
            service_session.rollback()
            traceback.print_exc()
            QtWidgets.QMessageBox.critical(None, "Σφάλμα!", "Κάτι δεν πήγε καλά τίποτα ΔΕΝ αποθηκεύτηκε")
            return

    def save_technician_to_db(self):
        try:
            if check_if_technician_service_data_exist(self.technician_lineEdit.text().upper()):
                QtWidgets.QMessageBox.warning(None, "Προσοχή", f"Ο τεχνικός '{self.technician_lineEdit.text().upper()}' υπάρχει")
                return
            technician = Service_data(Τεχνικός=self.technician_lineEdit.text().upper())
            service_session.add(technician)
            service_session.commit()
            self.refresh_all_data()
            QtWidgets.QMessageBox.information(None, "Πληροφορία!", "Αποθηκεύτηκε")
        except Exception:
            service_session.rollback()
            traceback.print_exc()
            QtWidgets.QMessageBox.critical(None, "Σφάλμα!", "Κάτι δεν πήγε καλά τίποτα ΔΕΝ αποθηκεύτηκε")
            return

    def delete_technician(self):
        technician_index = self.technician_combobox.currentIndex()
        selected_technician = self.all_technicians[technician_index]
        selected_technician_id = selected_technician[1]  # Είναι το id που έρχεται απο το fetch_service_reasons
        service_data_obj = service_session.query(Service_data).get(selected_technician_id)
        answer = QtWidgets.QMessageBox.question(None, "Προσοχή!", f"Σίγουρα θέλετε να διαγράφετε τον {selected_technician[0]};",
                                       QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                       QtWidgets.QMessageBox.No)
        if answer == QtWidgets.QMessageBox.Yes:
            service_data_obj.Τεχνικός = ""
            service_session.commit()
            QtWidgets.QMessageBox.information(None, "Πληροφορία!", "Διαγράφτηκες")
            self.refresh_all_data()

    def delete_reason(self):
        reason_index = self.reason_combobox.currentIndex()
        selected_reason = self.all_service_reasons[reason_index]
        selected_reason_id = selected_reason[1]  # Είναι το id που έρχεται απο το fetch_service_reasons
        service_data_obj = service_session.query(Service_data).get(selected_reason_id)
        answer = QtWidgets.QMessageBox.question(None, "Προσοχή!", f"Σίγουρα θέλετε να διαγράφετε το {selected_reason[0]};",
                                       QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                       QtWidgets.QMessageBox.No)
        if answer == QtWidgets.QMessageBox.Yes:
            service_data_obj.Σκοπός = ""
            service_session.commit()
            QtWidgets.QMessageBox.information(None, "Πληροφορία!", "Διαγράφτηκες")
            self.refresh_all_data()

    def delete_action(self):
        action_index = self.actions_combobox.currentIndex()
        selected_action = self.all_service_actions[action_index]
        selected_reason_id = selected_action[1]  # Είναι το id που έρχεται απο το fetch_service_actions
        service_data_obj = service_session.query(Service_data).get(selected_reason_id)
        answer = QtWidgets.QMessageBox.question(None, "Προσοχή!", f"Σίγουρα θέλετε να διαγράφετε το {selected_action[0]};",
                                       QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                       QtWidgets.QMessageBox.No)
        if answer == QtWidgets.QMessageBox.Yes:
            service_data_obj.Ενέργειες = ""
            service_session.commit()
            QtWidgets.QMessageBox.information(None, "Πληροφορία!", "Διαγράφτηκες")
            self.refresh_all_data()

    def delete_company(self):
        company_index = self.companies_combobox.currentIndex()
        selected_company = self.all_companies[company_index]
        selected_company_id = selected_company[1]  # Είναι το id που έρχεται απο το fetch_service_actions
        service_company_obj = service_session.query(Companies).get(selected_company_id)
        answer = QtWidgets.QMessageBox.question(None, "Προσοχή!", f"Σίγουρα θέλετε να διαγράφετε το "
                                                                  f"{selected_company[0]};",
                                       QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                       QtWidgets.QMessageBox.No)
        if answer == QtWidgets.QMessageBox.Yes:
            service_company_obj.Εταιρεία = ""
            service_session.commit()
            QtWidgets.QMessageBox.information(None, "Πληροφορία!", "Διαγράφτηκες")
            self.refresh_all_data()

    def delete_category(self):
        category_index = self.categories_combobox.currentIndex()
        selected_category = self.all_categories[category_index]
        selected_category_id = selected_category[1]  # Είναι το id που έρχεται απο το fetch_service_actions
        category_obj = service_session.query(Companies).get(selected_category_id)
        answer = QtWidgets.QMessageBox.question(None, "Προσοχή!", f"Σίγουρα θέλετε να διαγράφετε το "
                                                                  f"{selected_category[0]};",
                                       QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                       QtWidgets.QMessageBox.No)
        if answer == QtWidgets.QMessageBox.Yes:
            category_obj.Κατηγορία_μηχανήματος = ""
            service_session.commit()
            QtWidgets.QMessageBox.information(None, "Πληροφορία!", "Διαγράφτηκες")
            self.refresh_all_data()

    def closeEvent(self, event):
        self.window_closed.emit()
        event.accept()
        # event.ignore()  # if you want the window to never be closed


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")
    Edit_Service_Data_Window = QtWidgets.QWidget()
    ui = Ui_Edit_Service_Data_Window()
    ui.setupUi(Edit_Service_Data_Window)
    Edit_Service_Data_Window.show()
    sys.exit(app.exec_())
