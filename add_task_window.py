# -*- coding: utf-8 -*-
# Created by: PyQt5 UI code generator 5.15.4

import traceback
import subprocess
from xhtml2pdf import pisa
import os
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from db import (fetch_active_customers, Service_data, service_session, check_if_reason_service_data_exist,
                fetch_service_technicians, fetch_service_reasons, fetch_service_actions, Calendar, Service,
                check_if_actions_service_data_exist, check_if_technician_service_data_exist)

from settings import VERSION, root_logger, today, user
from add_new_customer_window import Ui_add_new_customer_window
from add_new_machine_window import Ui_add_new_machine_window
from send_email import Ui_Send_Email_Window

sys.stderr.write = root_logger.error
sys.stdout.write = root_logger.info


class Ui_Add_Task_Window(QtWidgets.QWidget):
    window_closed = QtCore.pyqtSignal()  # Το Signal πρεπει να είναι εκτός __init__ δεν δουλευει αλλιως

    def __init__(self):
        super(Ui_Add_Task_Window, self).__init__()
        self.active_customers = fetch_active_customers()
        self.all_customers = [customer.Επωνυμία_Επιχείρησης for customer in self.active_customers]
        self.customer_safe_to_save = False
        self.machine_safe_to_save = False
        self.selected_customer = None
        self.customer_index = None
        self.customer_machines = None
        self.customer_id = None
        self.selected_machine = None
        self.machine_index = None

        self.font_14_bold = QtGui.QFont()
        self.font_12_bold = QtGui.QFont()
        self.font_13 = QtGui.QFont()
        self.font_13_bold = QtGui.QFont()

        self.print_icon = QtGui.QIcon()
        self.print_icon.addPixmap(QtGui.QPixmap("icons/print_it.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)

    def setupUi(self, Add_Task_Window):
        Add_Task_Window.setObjectName("Add_Task_Window")
        Add_Task_Window.setWindowModality(QtCore.Qt.WindowModal)
        Add_Task_Window.resize(700, 500)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icons/add_scheduled_tasks.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Add_Task_Window.setWindowIcon(icon)
        Add_Task_Window.setWindowFilePath("")
        self.gridLayout = QtWidgets.QGridLayout(Add_Task_Window)
        self.gridLayout.setObjectName("gridLayout")
        # ------------------------------------------ Fonts -----------------------
        self.font_14_bold.setFamily("Calibri")
        self.font_14_bold.setPointSize(14)
        self.font_14_bold.setBold(True)
        self.font_14_bold.setWeight(75)

        self.font_12_bold.setFamily("Calibri")
        self.font_12_bold.setPointSize(12)
        self.font_12_bold.setBold(True)
        self.font_12_bold.setWeight(75)

        self.font_13.setFamily("Calibri")
        self.font_13.setPointSize(13)
        self.font_13.setBold(False)
        self.font_13.setWeight(50)

        self.font_13_bold.setFamily("Calibri")
        self.font_13_bold.setPointSize(13)
        self.font_13_bold.setBold(True)
        self.font_13_bold.setWeight(75)
        # Top Label
        self.top_label = QtWidgets.QLabel(Add_Task_Window)
        self.top_label.setMinimumSize(QtCore.QSize(0, 30))
        self.top_label.setFont(self.font_14_bold)
        self.top_label.setStyleSheet("background-color: rgb(0, 85, 127);\n"
                                     "color: rgb(255, 255, 255);")
        self.top_label.setAlignment(QtCore.Qt.AlignCenter)
        self.top_label.setObjectName("top_label")
        self.gridLayout.addWidget(self.top_label, 0, 0, 1, 4)

        # Ημερομηνία Label
        self.date_label = QtWidgets.QLabel(Add_Task_Window)
        self.date_label.setMinimumSize(QtCore.QSize(250, 25))
        self.date_label.setFont(self.font_13_bold)
        self.date_label.setStyleSheet("background-color: rgb(93, 93, 93);\n"
                                      "color: rgb(255, 255, 255);")
        self.date_label.setAlignment(QtCore.Qt.AlignCenter)
        self.date_label.setObjectName("date_label")
        self.gridLayout.addWidget(self.date_label, 1, 0, 1, 1)
        # Ημερομηνία edit
        self.dateEdit = QtWidgets.QDateEdit(Add_Task_Window)
        self.dateEdit.setMinimumSize(QtCore.QSize(250, 35))
        self.dateEdit.setFont(self.font_13_bold)
        self.dateEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.dateEdit.setDisplayFormat("dd/MM/yyyy")
        self.dateEdit.setCalendarPopup(True)
        self.dateEdit.setObjectName("dateEdit")
        self.dateEdit.setDate(QtCore.QDate.currentDate())
        self.gridLayout.addWidget(self.dateEdit, 2, 0, 1, 1, QtCore.Qt.AlignHCenter)

        # Πελάτης Label
        self.customer_label = QtWidgets.QLabel(Add_Task_Window)
        self.customer_label.setMinimumSize(QtCore.QSize(0, 25))
        self.customer_label.setFont(self.font_13_bold)
        self.customer_label.setStyleSheet("background-color: rgb(93, 93, 93);\n"
                                          "color: rgb(255, 255, 255);")
        self.customer_label.setAlignment(QtCore.Qt.AlignCenter)
        self.customer_label.setObjectName("customer_label")
        self.gridLayout.addWidget(self.customer_label, 1, 1, 1, 3)
        # Πελάτης edit
        self.customer_combobox = QtWidgets.QComboBox(self)
        self.customer_combobox.setFont(self.font_13_bold)
        self.customer_combobox.addItems(self.all_customers)
        self.customer_lineEdit = QtWidgets.QLineEdit(Add_Task_Window)
        self.customer_lineEdit.setMinimumSize(QtCore.QSize(250, 35))
        self.customer_lineEdit.setFont(self.font_13_bold)
        self.customer_lineEdit.setObjectName("customer_lineEdit")
        self.customer_completer = QtWidgets.QCompleter(self.all_customers)
        self.customer_completer.popup().setFont(self.font_13)
        self.customer_lineEdit.setCompleter(self.customer_completer)
        self.customer_combobox.currentIndexChanged.connect(self.show_selected_customer_machines)
        self.customer_combobox.setLineEdit(self.customer_lineEdit)
        self.gridLayout.addWidget(self.customer_combobox, 2, 1, 1, 2)


        # Time Label
        self.time_label = QtWidgets.QLabel(Add_Task_Window)
        self.time_label.setMinimumSize(QtCore.QSize(0, 25))
        self.time_label.setFont(self.font_13_bold)
        self.time_label.setStyleSheet("background-color: rgb(93, 93, 93);\n"
                                      "color: rgb(255, 255, 255);")
        self.time_label.setAlignment(QtCore.Qt.AlignCenter)
        self.time_label.setObjectName("time_label")
        self.gridLayout.addWidget(self.time_label, 3, 0, 1, 1)
        # Time Edit
        self.timeEdit = QtWidgets.QTimeEdit(Add_Task_Window)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.timeEdit.sizePolicy().hasHeightForWidth())
        self.timeEdit.setSizePolicy(sizePolicy)
        self.timeEdit.setMinimumSize(QtCore.QSize(100, 35))
        self.timeEdit.setFont(self.font_13)
        self.timeEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.timeEdit.setDisplayFormat("HH:mm")
        self.timeEdit.setObjectName("timeEdit")
        self.timeEdit.setTime(QtCore.QTime.currentTime())
        self.gridLayout.addWidget(self.timeEdit, 4, 0, 1, 1, QtCore.Qt.AlignHCenter)

        # Υπεύθυνος responsible Label
        self.responsible_label = QtWidgets.QLabel(Add_Task_Window)
        self.responsible_label.setMinimumSize(QtCore.QSize(250, 25))
        self.responsible_label.setFont(self.font_13_bold)
        self.responsible_label.setStyleSheet("background-color: rgb(93, 93, 93);\n"
                                             "color: rgb(255, 255, 255);")
        self.responsible_label.setAlignment(QtCore.Qt.AlignCenter)
        self.responsible_label.setObjectName("responsible_label")
        self.gridLayout.addWidget(self.responsible_label, 3, 1, 1, 3)
        # Υπεύθυνος responsible Edit
        self.responsible_lineEdit = QtWidgets.QLineEdit(Add_Task_Window)
        self.responsible_lineEdit.setMinimumSize(QtCore.QSize(250, 35))
        self.responsible_lineEdit.setFont(self.font_13)
        self.responsible_lineEdit.setObjectName("responsible_lineEdit")
        self.responsible_lineEdit.setReadOnly(True)
        self.gridLayout.addWidget(self.responsible_lineEdit, 4, 1, 1, 3)

        # Διεύθυνση Label
        self.address_label = QtWidgets.QLabel(Add_Task_Window)
        self.address_label.setMinimumSize(QtCore.QSize(300, 25))
        self.address_label.setFont(self.font_13_bold)
        self.address_label.setStyleSheet("background-color: rgb(93, 93, 93);\n"
                                         "color: rgb(255, 255, 255);")
        self.address_label.setAlignment(QtCore.Qt.AlignCenter)
        self.address_label.setObjectName("address_label")
        self.gridLayout.addWidget(self.address_label, 5, 0, 1, 1)
        # Διεύθυνση Edit
        self.address_lineEdit = QtWidgets.QLineEdit(Add_Task_Window)
        self.address_lineEdit.setMinimumSize(QtCore.QSize(350, 35))
        self.address_lineEdit.setFont(self.font_13)
        self.address_lineEdit.setObjectName("address_lineEdit")
        self.address_lineEdit.setReadOnly(True)
        self.gridLayout.addWidget(self.address_lineEdit, 6, 0, 1, 1)

        # Τηλέφωνο Label
        self.phones_label = QtWidgets.QLabel(Add_Task_Window)
        self.phones_label.setMinimumSize(QtCore.QSize(0, 25))
        self.phones_label.setFont(self.font_13_bold)
        self.phones_label.setStyleSheet("background-color: rgb(93, 93, 93);\n"
                                        "color: rgb(255, 255, 255);")
        self.phones_label.setAlignment(QtCore.Qt.AlignCenter)
        self.phones_label.setObjectName("phones_label")
        self.gridLayout.addWidget(self.phones_label, 5, 1, 1, 3)
        # Τηλέφωνο edit
        self.phones_lineEdit = QtWidgets.QLineEdit(Add_Task_Window)
        self.phones_lineEdit.setMinimumSize(QtCore.QSize(0, 35))
        self.phones_lineEdit.setFont(self.font_13)
        self.phones_lineEdit.setObjectName("phones_lineEdit")
        self.gridLayout.addWidget(self.phones_lineEdit, 6, 1, 1, 3)

        # Τεχνικός Label
        self.technician_label = QtWidgets.QLabel(Add_Task_Window)
        self.technician_label.setMinimumSize(QtCore.QSize(0, 25))
        self.technician_label.setFont(self.font_13_bold)
        self.technician_label.setStyleSheet("background-color: rgb(93, 93, 93);\n"
                                            "color: rgb(255, 255, 255);")
        self.technician_label.setAlignment(QtCore.Qt.AlignCenter)
        self.technician_label.setObjectName("technician_label")
        self.gridLayout.addWidget(self.technician_label, 7, 0, 1, 2)
        # Τεχνικός Edit
        self.technician_lineEdit = QtWidgets.QLineEdit(Add_Task_Window)
        self.technician_lineEdit.setMinimumSize(QtCore.QSize(0, 35))
        self.technician_lineEdit.setFont(self.font_13)
        self.technician_lineEdit.setObjectName("technician_lineEdit")
        self.technician_combobox = QtWidgets.QComboBox(Add_Task_Window)
        self.technician_combobox.setFont(self.font_13)
        self.technician_combobox.setLineEdit(self.technician_lineEdit)
        self.gridLayout.addWidget(self.technician_combobox, 8, 0, 1, 1)


        # Μηχάνημα Label
        self.machine_label = QtWidgets.QLabel(Add_Task_Window)
        self.machine_label.setMinimumSize(QtCore.QSize(0, 25))
        self.machine_label.setFont(self.font_13_bold)
        self.machine_label.setStyleSheet("background-color: rgb(93, 93, 93);\n"
                                         "color: rgb(255, 255, 255);")
        self.machine_label.setAlignment(QtCore.Qt.AlignCenter)
        self.machine_label.setObjectName("machine_label")
        self.gridLayout.addWidget(self.machine_label, 7, 2, 1, 3)
        # Μηχάνημα Edit
        self.machine_lineEdit = QtWidgets.QLineEdit(Add_Task_Window)
        self.machine_lineEdit.setMinimumSize(QtCore.QSize(0, 35))
        self.machine_lineEdit.setFont(self.font_13)
        self.machine_lineEdit.setObjectName("machine_lineEdit")
        self.machine_lineEdit.editingFinished.connect(self.check_if_machine_exist_from_line_edit)

        self.machine_combobox = QtWidgets.QComboBox(self)
        self.machine_combobox.setFont(self.font_13_bold)
        self.machine_combobox.setMinimumSize(250, 35)
        self.machine_combobox.currentIndexChanged.connect(self.check_if_machine_exist_from_combobox)
        self.machine_combobox.setLineEdit(self.machine_lineEdit)
        self.gridLayout.addWidget(self.machine_combobox, 8, 2, 1, 1)

        # Σκοπός Label
        self.reason_label = QtWidgets.QLabel(Add_Task_Window)
        self.reason_label.setMinimumSize(QtCore.QSize(0, 25))
        self.reason_label.setFont(self.font_13_bold)
        self.reason_label.setStyleSheet("background-color: rgb(255, 170, 0);\n"
                                        "color: rgb(255, 255, 255);")
        self.reason_label.setAlignment(QtCore.Qt.AlignCenter)
        self.reason_label.setObjectName("reason_label")
        self.gridLayout.addWidget(self.reason_label, 9, 0, 1, 2)
        # Σκοπός Edit
        self.reason_lineEdit = QtWidgets.QLineEdit(Add_Task_Window)
        self.reason_lineEdit.setMinimumSize(QtCore.QSize(0, 35))
        self.reason_lineEdit.setMaximumSize(161154, 35)
        self.reason_lineEdit.setFont(self.font_13)
        self.reason_lineEdit.setObjectName("reason_lineEdit")
        self.reason_lineEdit.setFocus()
        self.reason_combobox = QtWidgets.QComboBox(Add_Task_Window)
        self.reason_combobox.setFont(self.font_13)
        self.reason_combobox.setLineEdit(self.reason_lineEdit)
        self.gridLayout.addWidget(self.reason_combobox, 10, 0, 1, 1)

        # Ενέργειες label
        self.action_label = QtWidgets.QLabel(Add_Task_Window)
        self.action_label.setMinimumSize(QtCore.QSize(0, 25))
        self.action_label.setFont(self.font_12_bold)
        self.action_label.setStyleSheet("background-color: rgb(0, 85, 127);\n"
                                        "color: rgb(255, 255, 255);")
        self.action_label.setAlignment(QtCore.Qt.AlignCenter)
        self.action_label.setObjectName("action_label")
        self.gridLayout.addWidget(self.action_label, 9, 2, 1, 2)
        # action edit
        self.action_lineEdit = QtWidgets.QLineEdit(Add_Task_Window)
        self.action_lineEdit.setMinimumSize(QtCore.QSize(0, 35))
        self.action_lineEdit.setFont(self.font_13)
        self.action_lineEdit.setObjectName("action_lineEdit")
        self.actions_combobox = QtWidgets.QComboBox(Add_Task_Window)
        self.actions_combobox.setFont(self.font_13)
        self.actions_combobox.setLineEdit(self.action_lineEdit)
        self.gridLayout.addWidget(self.actions_combobox, 10, 2, 1, 1)

        # Σημειώσεις Label
        self.notes_label = QtWidgets.QLabel(Add_Task_Window)
        self.notes_label.setMinimumSize(QtCore.QSize(0, 30))
        self.notes_label.setFont(self.font_13_bold)
        self.notes_label.setStyleSheet("background-color: rgb(93, 93, 93);\n"
                                       "color: rgb(255, 255, 255);")
        self.notes_label.setAlignment(QtCore.Qt.AlignCenter)
        self.notes_label.setObjectName("notes_label")
        self.gridLayout.addWidget(self.notes_label, 11, 0, 1, 5)
        # Σημειώσεις Edit
        self.notes_textEdit = QtWidgets.QTextEdit(Add_Task_Window)
        self.notes_textEdit.setFont(self.font_13)
        self.notes_textEdit.setObjectName("notes_textEdit")
        self.notes_textEdit.setMinimumSize(QtCore.QSize(0, 100))
        self.notes_textEdit.setText(f"-------------------------------- {user} {today.replace(' ', '/')} --------------------------------\n")
        self.gridLayout.addWidget(self.notes_textEdit, 12, 0, 1, 5)

        # Προσθήκη πελάτη
        self.add_customer_toolButton = QtWidgets.QToolButton(Add_Task_Window)
        self.add_customer_toolButton.setFont(self.font_13_bold)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("icons/add_customer.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.add_customer_toolButton.setIcon(icon1)
        self.add_customer_toolButton.setIconSize(QtCore.QSize(30, 30))
        self.add_customer_toolButton.setObjectName("add_customer_toolButton")
        self.add_customer_toolButton.clicked.connect(self.show_add_new_customer_window)
        self.gridLayout.addWidget(self.add_customer_toolButton, 2, 3, 1, 1)

        # Προσθήκη μηχανήματος κουμπί
        self.add_machine_toolButton = QtWidgets.QToolButton(Add_Task_Window)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("icons/add_machine.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.add_machine_toolButton.setIcon(icon4)
        self.add_machine_toolButton.setIconSize(QtCore.QSize(30, 30))
        self.add_machine_toolButton.setObjectName("add_machine_toolButton")
        self.add_machine_toolButton.clicked.connect(self.show_add_new_machine_window)
        self.gridLayout.addWidget(self.add_machine_toolButton, 8, 3, 1, 1)

        # Προσθήκη τεχνικού
        self.add_technician_toolButton = QtWidgets.QToolButton(Add_Task_Window)
        self.add_technician_toolButton.setFont(self.font_13_bold)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("icons/add_service.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.add_technician_toolButton.setIcon(icon1)
        self.add_technician_toolButton.setIconSize(QtCore.QSize(30, 30))
        self.add_technician_toolButton.setObjectName("add_technician_toolButton")
        self.add_technician_toolButton.clicked.connect(self.add_technician_to_db)
        self.gridLayout.addWidget(self.add_technician_toolButton, 8, 1, 1, 1)

        # Προσθήκη σκοπού στην βάση κουμπί
        self.add_reason_toolButton = QtWidgets.QToolButton(Add_Task_Window)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("icons/add_to_service_data2.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.add_reason_toolButton.setIcon(icon3)
        self.add_reason_toolButton.setIconSize(QtCore.QSize(30, 30))
        self.add_reason_toolButton.setObjectName("add_reason_toolButton")
        self.add_reason_toolButton.clicked.connect(self.add_reason_to_db)
        self.gridLayout.addWidget(self.add_reason_toolButton, 10, 1, 1, 1)

        # add action btn
        self.add_action_toolButton = QtWidgets.QToolButton(Add_Task_Window)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("icons/add_to_service_data2.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.add_action_toolButton.setIcon(icon5)
        self.add_action_toolButton.setIconSize(QtCore.QSize(30, 30))
        self.add_action_toolButton.setObjectName("add_action_toolButton")
        self.add_action_toolButton.clicked.connect(self.add_action_to_db)
        self.gridLayout.addWidget(self.add_action_toolButton, 10, 3, 1, 1)

        # Save Btn
        self.save_toolButton = QtWidgets.QToolButton(Add_Task_Window)
        self.save_toolButton.setFont(self.font_13_bold)
        self.save_toolButton.setStyleSheet("background-color: rgb(103, 103, 103);\n"
                                           "color: rgb(255, 255, 255);")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("icons/Save.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.save_toolButton.setIcon(icon5)
        self.save_toolButton.setIconSize(QtCore.QSize(30, 30))
        self.save_toolButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.save_toolButton.setObjectName("save_toolButton")
        self.save_toolButton.clicked.connect(self.save_task)
        self.gridLayout.addWidget(self.save_toolButton, 13, 2, 1, 2)

        # Email btn
        self.email_toolButton = QtWidgets.QToolButton(Add_Task_Window)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap("icons/send_mail.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.email_toolButton.setIcon(icon6)
        self.email_toolButton.setIconSize(QtCore.QSize(30, 30))
        self.email_toolButton.setObjectName("email_toolButton")
        self.email_toolButton.clicked.connect(self.send_mail)
        self.gridLayout.addWidget(self.email_toolButton, 13, 0, 1, 1)

        # Print
        self.print_toolButton = QtWidgets.QToolButton(Add_Task_Window)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.print_toolButton.setFont(font)
        self.print_toolButton.setIcon(self.print_icon)
        self.print_toolButton.setIconSize(QtCore.QSize(30, 30))
        self.print_toolButton.setObjectName("print_toolButton")
        self.print_toolButton.clicked.connect(self.print_to_pdf)
        self.gridLayout.addWidget(self.print_toolButton, 13, 1, 1, 1)

        # Esc
        self.shortcut_esc = QtWidgets.QShortcut(QtGui.QKeySequence('Escape'), Add_Task_Window)
        self.shortcut_esc.activated.connect(self.close)

        self.retranslateUi(Add_Task_Window)
        QtCore.QMetaObject.connectSlotsByName(Add_Task_Window)

        self.fetch_service_data()
        self.check_if_selected_machine()
        self.check_if_selected_customer()

    def retranslateUi(self, Add_Task_Window):
        _translate = QtCore.QCoreApplication.translate
        Add_Task_Window.setWindowTitle(_translate("Add_Task_Window", f"Προσθήκη εργασίας {VERSION}"))
        self.date_label.setText(_translate("Add_Task_Window", "Ημερομηνία"))
        # self.refresh_customers_toolButton.setText(_translate("Add_Task_Window", "..."))
        self.responsible_label.setText(_translate("Add_Task_Window", "Υπεύθυνος"))
        self.address_label.setText(_translate("Add_Task_Window", "Διεύθυνση"))
        self.technician_label.setText(_translate("Add_Task_Window", "Τεχνικός"))
        self.add_reason_toolButton.setText(_translate("Add_Task_Window", "..."))
        self.top_label.setText(_translate("Add_Task_Window", "Προσθήκη εργασίας"))
        self.customer_label.setText(_translate("Add_Task_Window", "Πελάτης"))
        self.phones_label.setText(_translate("Add_Task_Window", "Τηλέφωνο - Κινητό"))
        self.machine_label.setText(_translate("Add_Task_Window", "Μηχάνημα"))
        self.action_label.setText(_translate("Add_Task_Window", "Ενέργειες"))
        self.add_machine_toolButton.setText(_translate("Add_Task_Window", "..."))
        self.notes_label.setText(_translate("Add_Task_Window", "Σημειώσεις"))
        self.reason_label.setText(_translate("Add_Task_Window", "Σκοπός εργασίας"))
        self.time_label.setText(_translate("Add_Task_Window", "Ωρα"))
        self.save_toolButton.setText(_translate("Add_Task_Window", "   Αποθήκευση"))
        self.email_toolButton.setText(_translate("Add_Task_Window", "..."))

    def fetch_service_data(self):
        self.all_service_reasons = fetch_service_reasons()
        self.service_reasons = [service[0] for service in self.all_service_reasons]
        self.all_service_technicians = fetch_service_technicians()
        self.service_technicians = [service[0] for service in self.all_service_technicians]
        self.all_service_actions = fetch_service_actions()
        self.service_actions = [service[0] for service in self.all_service_actions]

        self.technician_completer = QtWidgets.QCompleter(self.service_technicians)
        self.technician_lineEdit.setCompleter(self.technician_completer)
        self.technician_completer.popup().setFont(self.font_13)
        self.technician_combobox.clear()
        self.technician_combobox.addItems(self.service_technicians)

        self.reason_completer = QtWidgets.QCompleter(self.service_reasons)
        self.reason_completer.popup().setFont(self.font_13)
        self.reason_lineEdit.setCompleter(self.reason_completer)
        self.reason_combobox.clear()
        self.reason_combobox.addItems(self.service_reasons)

        self.actions_completer = QtWidgets.QCompleter(self.service_actions)
        self.actions_completer.popup().setFont(self.font_13)
        self.action_lineEdit.setCompleter(self.actions_completer)
        self.actions_combobox.clear()
        self.actions_combobox.addItems(self.service_actions)

    def check_if_selected_machine(self):
        """
        Ελεγχει αν όταν καλούμε το αρχείο αυτό έχουμε αρχικοποιήση την μεταβλητη self.selected_machine
        Ορίζει τότε τον πελάτη και το μηχάνημα μη επεξεργάσιμα αφου ο χρήστης έχει επιλέξει απο πρίν μηχάνημα
        και εμφανίζει τα δεδομένα
            καλείτε :
                    όταν ανοιγει αυτό το παράθυρο
        :return:
        """
        self.reason_lineEdit.setFocus()
        if self.selected_machine:
            self.machine_safe_to_save = True
            self.customer_lineEdit.setReadOnly(True)
            self.customer_combobox.setDisabled(True)
            self.customer_safe_to_save = True
            self.machine_lineEdit.setReadOnly(True)
            self.machine_combobox.setDisabled(True)
            self.selected_customer = self.selected_machine.Customer
            self.customer_lineEdit.setText(self.selected_customer.Επωνυμία_Επιχείρησης)
            self.customer_lineEdit.setStyleSheet("background-color: green; color: white;")
            self.responsible_lineEdit.setText(self.selected_customer.Ονοματεπώνυμο)
            self.address_lineEdit.setText(self.selected_customer.Διεύθυνση)
            self.phones_lineEdit.setText(self.selected_customer.Κινητό + " Σταθερό: " + self.selected_customer.Τηλέφωνο)
            self.machine_lineEdit.setText(self.selected_machine.Εταιρεία + " Serial: " + self.selected_machine.Serial)
            self.machine_lineEdit.setStyleSheet("background-color: green; color: white;")
        else:
            self.machine_lineEdit.setText("")
            self.machine_lineEdit.setStyleSheet("background-color: red; color: white;")
            self.machine_safe_to_save = False
            self.selected_machine = None

    def check_if_selected_customer(self):
        """
        Αν ο χρήστης έχει επιλέξει απο πρίν μόνο πελάτη (self.selected_customer)
        Να γίνει επιλεγμένο το πρώτο μηχάνημα
        Ορίζει τότε τον πελάτη  μη επεξεργάσιμα αφου ο χρήστης έχει επιλέξει απο πρίν
        και εμφανίζει τα δεδομένα
            καλείτε :
                    όταν ανοιγει αυτό το παράθυρο
        :return:
        """
        if self.selected_machine is None and self.selected_customer:
            self.machine_lineEdit.setFocus()
            self.customer_lineEdit.setReadOnly(True)
            self.customer_safe_to_save = True
            self.customer_combobox.setDisabled(True)
            self.machine_combobox.clear()
            self.customer_machines = self.selected_customer.machines
            self.customer_lineEdit.setStyleSheet("background-color: green; color: white;")
            self.customer_lineEdit.setText(self.selected_customer.Επωνυμία_Επιχείρησης)
            self.responsible_lineEdit.setText(self.selected_customer.Ονοματεπώνυμο)
            self.address_lineEdit.setText(self.selected_customer.Διεύθυνση)
            self.phones_lineEdit.setText(
                self.selected_customer.Κινητό + " Σταθερό: " + self.selected_customer.Τηλέφωνο)
            self.combobox_machines = sorted([machine.Εταιρεία + f"  Serial: {machine.Serial}" for machine in
                                             self.customer_machines])
            self.machine_combobox.addItems(self.combobox_machines)
            if len(self.customer_machines) > 0:
                self.selected_machine = self.customer_machines[0]
                self.machine_lineEdit.setText("")
                self.machine_lineEdit.setStyleSheet("background-color: red; color: white;")
                self.machine_safe_to_save = False
            else:
                self.machine_lineEdit.setText("Ο πελάτης δεν έχει μηχάνημα")
                self.machine_lineEdit.setStyleSheet("background-color: red; color: white;")
                self.selected_machine = None
                self.machine_safe_to_save = False
        elif self.selected_machine is None and self.selected_customer is None:
            self.customer_lineEdit.setText("")
            self.customer_lineEdit.setStyleSheet("background-color: red; color: white;")
            self.selected_customer = None
            self.customer_safe_to_save = False
        self.reason_lineEdit.setText("")  # Να βάλουμε κενά γιατι εμφανίζει το πρώτο απο την λίστα των reasons
        self.action_lineEdit.setText("")  # Να βάλουμε κενά γιατι εμφανίζει το πρώτο απο την λίστα των actions

    def check_if_machine_exist_from_line_edit(self):
        """
        1. όταν ο χρήστης κάνει αλλαγές στο όνομα του πελάτη
        ψάχνουμε τον πελάτη με βάσει αυτό που έγραψε ο χρήτης στην λίστα self.all_customers
        Αν ο χρήστης δεν έχει επιλεξει απο πρίν πελάτη αρχικοποιει τους πελάτες
        και όριζει σαν επιλεγμένο αυτόν που γράφει το self.customer_lineEdit.text()
        2.  # Ψάχνει στα μηχανήματα του πελάτη αυτό που γράφει στο self.machine_lineEdit
            καλείτε :
                    όταν αλλάζει το self.machine_lineEdit.editingFinished.connect
        :return:
        """
        if not self.selected_customer:
            try:
                self.customer_index = self.all_customers.index(self.customer_lineEdit.text())
                self.selected_customer = self.active_customers[self.customer_index]
                self.customer_safe_to_save = True
                self.customer_lineEdit.setStyleSheet("background-color: green; color: white;")
                self.responsible_lineEdit.setText(self.selected_customer.Ονοματεπώνυμο)
                self.address_lineEdit.setText(self.selected_customer.Διεύθυνση)
                self.phones_lineEdit.setText(
                    self.selected_customer.Κινητό + " Σταθερό: " + self.selected_customer.Τηλέφωνο)
                self.customer_machines = self.selected_customer.machines
            except ValueError:  # ValueError: 'πελατησ μεγαλοσ' is not in list όταν δεν υπάρχει ο πελάτης
                traceback.print_exc()
                self.customer_lineEdit.setStyleSheet("background-color: red; color: white;")
                self.customer_safe_to_save = False
                return
        # Ψάχνει στα μηχανήματα του πελάτη
        for index, machine in enumerate(self.customer_machines):
            if self.machine_lineEdit.text() in (machine.Εταιρεία + f"  Serial: {machine.Serial}"):
                self.machine_index = index
                self.selected_machine = self.customer_machines[self.machine_index]
                self.machine_lineEdit.setText(machine.Εταιρεία + f"  Serial: {machine.Serial}")
                self.machine_lineEdit.setStyleSheet("background-color: green; color: white;")
                self.machine_safe_to_save = True
                return

            else:
                self.machine_safe_to_save = False
                self.machine_lineEdit.setStyleSheet("background-color: red; color: white;")

    def check_if_machine_exist_from_combobox(self):
        """
            1. όταν ο χρήστης αλλάζει το self.machine_combobox.currentIndexChanged
            και δέν έχουμε επιλεγμένο μηχάνημα απο το self.machine_lineEdit
            Ψάχνει να βρεί το μηχάνημα απο το index του self.combobox_machines
            και ορίζει το μηχάνημα σαν επιλεγμένο
                καλείτε :
                        όταν αλλάζει το self.machine_combobox.currentIndexChanged
        :return:
        """
        if not self.machine_safe_to_save:
            try:
                self.combobox_machines = [machine for machine in self.customer_machines]
                selected_machine_index = self.machine_combobox.currentIndex()
                self.selected_machine = self.customer_machines[selected_machine_index]
                self.machine_lineEdit.setStyleSheet("background-color: green; color: white;")
                self.machine_safe_to_save = True
            except IndexError:
                traceback.print_exc()
                self.machine_safe_to_save = False
                self.machine_lineEdit.setStyleSheet("background-color: red; color: white;")
                return
            except Exception:
                traceback.print_exc()
                return

    def show_selected_customer_machines(self):
        """
                1. Ελεγχος αν αυτό που γράφει το self.customer_lineEdit.text() υπάρχει
                2. Αρχεικοποιήση μηχανημάτων αν υπάρχει ο πελάτης
                    καλείτε :
                            όταν αλλάζει το self.customer_combobox.currentIndexChanged.connect
        :return:
        """
        if self.customer_lineEdit.text() not in self.all_customers:
            self.machine_combobox.clear()
            self.customer_lineEdit.setStyleSheet("background-color: red; color: white;")
            return
        else:
            self.machine_combobox.clear()
            self.customer_index = self.all_customers.index(self.customer_lineEdit.text())
            self.selected_customer = self.active_customers[self.customer_index]
            self.customer_safe_to_save = True
            self.customer_lineEdit.setStyleSheet("background-color: green; color: white;")
            self.responsible_lineEdit.setText(self.selected_customer.Ονοματεπώνυμο)
            self.address_lineEdit.setText(self.selected_customer.Διεύθυνση)
            self.phones_lineEdit.setText(self.selected_customer.Κινητό + " Σταθερό: " + self.selected_customer.Τηλέφωνο)
            self.customer_machines = [machine for machine in self.selected_customer.machines]
            if len(self.customer_machines) < 1:
                self.machine_lineEdit.setText("Ο πελάτης δεν έχει μηχάνημα")
                self.machine_lineEdit.setStyleSheet("Background-color: red; color: white;")
                self.machine_safe_to_save = False
                self.selected_machine = None
                return
            self.combobox_machines = sorted([machine.Εταιρεία + f"  Serial: {machine.Serial}" for machine in
                                             self.customer_machines])
            self.machine_combobox.addItems(self.combobox_machines)
            self.machine_lineEdit.setText("")
            self.machine_lineEdit.setStyleSheet("Background-color: red; color: white;")
            self.selected_machine = None
            self.machine_safe_to_save = False

    def refresh_machines(self):

        try:
            self.customer_machines = self.selected_customer.machines
            self.machine_combobox.clear()
            self.combobox_machines = sorted([machine.Εταιρεία + f"  Serial: {machine.Serial}" for machine in
                                             self.customer_machines])
            self.machine_combobox.addItems(self.combobox_machines)
            self.machine_lineEdit.setText("")
            self.machine_lineEdit.setStyleSheet("Background-color: red; color: white;")
        except AttributeError:  # Οταν εισάγουμε μηχάνημα χωρίς να έχουμε επιλέξει πελάτη
            return

    def refresh_customers(self):
        self.active_customers = fetch_active_customers()
        self.all_customers = [customer.Επωνυμία_Επιχείρησης for customer in self.active_customers]
        self.customer_combobox.clear()
        self.customer_combobox.addItems(self.all_customers)
        self.customer_completer = QtWidgets.QCompleter(self.all_customers)
        self.customer_completer.popup().setFont(self.font_13)
        self.customer_lineEdit.setCompleter(self.customer_completer)
        self.customer_lineEdit.setText("")
        self.customer_lineEdit.setStyleSheet("background-color: red; color: white;")
        self.selected_customer = None
        self.customer_safe_to_save = False

    def save_task(self):
        if not self.customer_safe_to_save:
            self.customer_lineEdit.setStyleSheet("background-color: red; color: white;")

        else:
            self.customer_lineEdit.setStyleSheet("background-color: green; color: white;")
        if not self.machine_safe_to_save:
            self.machine_lineEdit.setStyleSheet("background-color: red; color: white;")
        else:
            self.machine_lineEdit.setStyleSheet("background-color: green; color: white;")

        if self.machine_safe_to_save and self.customer_safe_to_save:

            try:
                started_date = self.dateEdit.date().toString('dd/MM/yyyy')
                time_for_task = self.timeEdit.time().toString("HH:mm")
                new_service = Service(Ημερομηνία=started_date, Σκοπός_Επίσκεψης=self.reason_lineEdit.text(),
                                      Ενέργειες=self.action_lineEdit.text(), Τεχνικός=self.technician_lineEdit.text(),
                                      Σημειώσεις=self.notes_textEdit.toPlainText(), Μετρητής="", Επ_Service="",
                                      Copier_ID=self.selected_machine.ID, ΔΤΕ="", Price="",)
                service_session.add(new_service)
                service_session.commit()
                # print("new_service.ID", new_service.ID)
                new_task = Calendar(Ημερομηνία=started_date, Πελάτης=self.selected_customer.Επωνυμία_Επιχείρησης,
                                    Μηχάνημα=self.selected_machine.Εταιρεία + f"  Serial: {self.selected_machine.Serial}",
                                    Σκοπός=self.reason_lineEdit.text(), Ενέργειες=self.action_lineEdit.text(),
                                    Τεχνικός=self.technician_lineEdit.text(), Ημ_Ολοκλ="01/01/2000",
                                    Επείγων=time_for_task, Τηλέφωνο=self.phones_lineEdit.text(),
                                    Σημειώσεις=self.notes_textEdit.toPlainText(), Copier_ID=self.selected_machine.ID,
                                    ΔΤΕ="", Service_ID=new_service.ID, Μετρητής="", Επ_Service="",
                                    Customer_ID=self.selected_customer.ID, Price="")
                service_session.add(new_task)
                service_session.commit()
                answer = QtWidgets.QMessageBox.question(None, "Εκτύπωη!", "Θέλετε να γίνει εκτύπωση;",
                                                        QtWidgets.QMessageBox.Yes
                                                        | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
                if answer == QtWidgets.QMessageBox.Yes:
                    self.print_to_pdf()
                self.close()
            except Exception:
                service_session.rollback()
                traceback.print_exc()
                QtWidgets.QMessageBox.critical(None, "Σφάλμα", f"Κάτι δεν πήγε καλα!\nΟι αλλαγές δεν αποθήκευτηκαν!")
                return
        else:

            answer = QtWidgets.QMessageBox.question(None, "Προσοχή!", "Η κλήση δεν μπορεί να αποθηκευτεί\n"
                                                                      "Μπορείτε μόνο να την εκτυπώσετε\n"
                                                                      "Θέλετε να γίνει εκτύπωση;",
                                                    QtWidgets.QMessageBox.Yes
                                                    | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
            if answer == QtWidgets.QMessageBox.Yes:
                self.print_to_pdf()
                self.close()

    def add_reason_to_db(self):
        try:
            if check_if_reason_service_data_exist(self.reason_lineEdit.text().upper()):
                QtWidgets.QMessageBox.warning(None, "Προσοχή", f"Το '{self.reason_lineEdit.text().upper()}' υπάρχει")
                return
            reason = Service_data(Σκοπός=self.reason_lineEdit.text().upper())
            service_session.add(reason)
            service_session.commit()
            self.all_service_reasons = fetch_service_reasons()
            self.service_reasons = [service[0] for service in self.all_service_reasons]
            self.reason_completer = QtWidgets.QCompleter(self.service_reasons)
            self.reason_lineEdit.setCompleter(self.reason_completer)
            QtWidgets.QMessageBox.information(None, "Πληροφορία!", "Αποθηκεύτηκε")
        except Exception:
            service_session.rollback()
            traceback.print_exc()
            return

    def add_action_to_db(self):
        try:
            if check_if_actions_service_data_exist(self.action_lineEdit.text().upper()):
                QtWidgets.QMessageBox.warning(None, "Προσοχή", f"Το '{self.action_lineEdit.text().upper()}' υπάρχει")
                return
            action = Service_data(Ενέργειες=self.action_lineEdit.text().upper())
            service_session.add(action)
            service_session.commit()
            self.fetch_service_data()
            QtWidgets.QMessageBox.information(None, "Πληροφορία!", "Αποθηκεύτηκε")
        except Exception:
            service_session.rollback()
            traceback.print_exc()
            return

    def add_technician_to_db(self):
        try:
            if check_if_technician_service_data_exist(self.technician_lineEdit.text().upper()):
                QtWidgets.QMessageBox.warning(None, "Προσοχή", f"O τεχνικός '{self.technician_lineEdit.text().upper()}' υπάρχει")
                return
            technician = Service_data(Τεχνικός=self.technician_lineEdit.text().upper())
            service_session.add(technician)
            service_session.commit()
            self.fetch_service_data()
            QtWidgets.QMessageBox.information(None, "Πληροφορία!", "Αποθηκεύτηκε")
        except Exception:
            service_session.rollback()
            traceback.print_exc()
            return

    # Αποστολή email
    def send_mail(self):
        status = "Δεν έχει ολοκληρωθεί"
        data = [self.dateEdit.date().toString("dd/MM/yyyy"),
                self.reason_lineEdit.text(),
                self.technician_lineEdit.text(),
                self.action_lineEdit.text(),
                " ",  # self.counter_lineEdit.text()
                self.timeEdit.time().toString('HH:mm'),
                self.phones_lineEdit.text(),
                self.notes_textEdit.toHtml(),
                " ",  # self.dte_lineEdit.text()
                status]

        self.show_send_email_window = QtWidgets.QWidget()
        # self.show_add_new_customer_window.setWindowTitle("Προσθήκη νέου πελάτη")
        self.show_send_email = Ui_Send_Email_Window()
        self.show_send_email.selected_customer = self.customer_lineEdit.text()
        self.show_send_email.selected_machine = self.machine_lineEdit.text()
        self.show_send_email.data_to_send = data
        # self.show_send_email.files_path = self.images_path  # Δεν έχει αρχεία στο add_task
        # Αρχικοποιηση των κουμπιων, γραμμων επεξεργασίας κτλπ
        self.show_send_email.setupUi(self.show_send_email_window)

        self.show_send_email.window = self.show_send_email_window  # Αν θέλουμε να ανοιγουν πολλα παράθυρα
        self.show_send_email_window.show()
        self.show_send_email.window_closed.connect(lambda: self.show_send_email_window.close())

    def print_to_pdf(self):
        # Define your data

        prints_dir = f'prints/{today}'.replace(" ", "_")

        if not os.path.exists(prints_dir):
            os.makedirs(prints_dir)
        # outputFilename = f"{prints_dir}/Service_Book{self.customer_lineEdit.text()}.pdf"
        outputFilename = f"{prints_dir}/Service_Book_" + f"{self.customer_lineEdit.text()}".replace(" ","_") + ".pdf"
        notes = self.notes_textEdit.toPlainText().replace("\n", "<br>")
        # Utility function
        def convertHtmlToPdf(sourceHtml, outputFilename):
            # open output file for writing (truncated binary)
            resultFile = open(outputFilename, "w+b")

            # convert HTML to PDF

            pisaStatus = pisa.CreatePDF(sourceHtml.encode('utf-8'), dest=resultFile, encoding='utf8')

            # close output file
            resultFile.close()  # close output file

            # return True (0) on success and False (1) on errors
            return pisaStatus.err

        # data = [self.dateEdit.text(), self.customer_lineEdit.text(), self.address_lineEdit.text(),
        #         self.phones_lineEdit.text(), self.technician_lineEdit.text(), self.machine_lineEdit.text(),
        #         self.reason_lineEdit.text(), self.timeEdit.time().toString("HH:mm"),
        #         self.notes_textEdit.toPlainText()]
        #
        # names = ["Ημερομηνία", "Πελάτης", "Διεύθυνση", "Τηλέφωνο", "Τεχνικός", "Μηχάνημα", "Σκοπός", "Ωρα",
        #          "Σημειώσεις"]
        #
        # images = ['icons/date.png', 'icons/customer.png', 'icons/phone.png', 'icons/copier.png',
        #           'icons/purpose.png',
        #           'icons/technician.png', 'icons/urgent.png', 'icons/notes.png']

        # https://developer.mozilla.org/en-US/docs/Web/CSS/@font-face
        font = """{
                font-family: Calibri;
                font-stretch: 50%;
                src: url('../fonts/Calibri.ttf');
                }
                body {
                font-family: Calibri;
                }
                h1 {
                font-family: Calibri;
                }
                h2 {
                font-family: Calibri;
                }
                h3 {
                font-family: Calibri;
                }
                h4 {
                font-family: Calibri;
                }
                """

        src = "../icons/"

        sourceHtml = f"""<html>

            <meta http-equiv=Content-Type content="text/html;charset=utf-8"></meta>
            <style>
            @font-face {font}
            </style>
            <body>
            <font size = "6"> 
            <h2 style="text-align: center;">
                <span style="text-decoration: underline;">
                    <img style="float: right;" src="{src}logo-small-orange.png" alt="" width="150" height="108"/> 
                        Δελτίο τεχνικής εξυπηρέτησης
                </span>
                </h2>
    <table  border="1">
            
    
<tbody>
<tr style="height: 18px;">
<td style="width: 26.4204%; height: 35px; text-align: center; vertical-align:bottom;">
Ημερομηνία
</td>
<td style="width: 73.5796%; height: 35px; text-align: center; vertical-align:bottom;"> {self.dateEdit.date().toString("dd/MM/yyyy")}</td>
</tr>
<tr style="height: 18px;">
<td style="width: 26.4204%; height: 35px; text-align: center; vertical-align:bottom;">
Πελάτης
</td>
<td style="width: 73.5796%; height: 35px; text-align: center; vertical-align:bottom;"> {self.customer_lineEdit.text()}</td>
</tr>
<tr style="height: 18px;">
<td style="width: 26.4204%; height: 35px; text-align: center; vertical-align:bottom;">
Υπεύθυνος
</td>
<td style="width: 73.5796%; height: 35px; text-align: center; vertical-align:bottom;"> {self.responsible_lineEdit.text()}</td>
</tr>
<tr style="height: 18px;">
<td style="width: 26.4204%; height: 35px; text-align: center; vertical-align:bottom;">
Διεύθυνση
</td>
<td style="width: 73.5796%; height: 35px; text-align: center; vertical-align:bottom;" > {self.address_lineEdit.text()}</td>
</tr>
<tr style="height: 18px;">
<td style="width: 26.4204%; height: 35px; text-align: center; vertical-align:bottom;">
Τηλέφωνα
</td>
<td style="width: 73.5796%; height: 35px; text-align: center; vertical-align:bottom;"> {self.phones_lineEdit.text()}</td>
</tr>
<tr style="height: 18px;">
<td style="width: 26.4204%; height: 35px; text-align: center; vertical-align:bottom;">
Μηχάνημα
</td>
<td style="width: 73.5796%; height: 35px; text-align: center; vertical-align:bottom;"> {self.machine_lineEdit.text()}</td>
</tr>
<tr style="height: 18px;">
<td style="width: 26.4204%; height: 35px; text-align: center; vertical-align:bottom;">
Περιγραφή προβλήματος
</td>
<td style="width: 73.5796%; height: 35px; text-align: center; vertical-align:bottom;"> {self.reason_lineEdit.text()}</td>
</tr>
<tr style="height: 18px;">
<td style="width: 26.4204%; height: 35px; text-align: center; vertical-align:bottom;">
Ενέργειες
</td>
<td style="width: 73.5796%; height: 35px; text-align: center; vertical-align:bottom;"> {self.action_lineEdit.text()}</td>
</tr>
<tr style="height: 35px;">
<td style="width: 26.4204%; height: 35px; text-align: center; vertical-align:bottom;">
Τεχνικός
</td>
<td style="width: 73.5796%; height: 35px; text-align: center; vertical-align:bottom;"> {self.technician_lineEdit.text()}</td>
</tr>
<tr style="height: 18px;">
<td style="width: 26.4204%; height: 35px; text-align: center; vertical-align:bottom;">
Ωρα
</td>
<td style="width: 73.5796%; height: 35px; text-align: center; vertical-align:bottom;"> {self.timeEdit.time().toString('HH:mm')}</td>
</tr>
<tr style="height: 210px;">
<td style="width: 26.4204%; height: 420px; text-align: center;">
Σημειώσεις
</td>
<td style="width: 73.5796%; height: 420px; text-align: left; vertical-align:top;"> {notes}</td>
</tr>
<tr style="height: 18px;">
<td style="width: 26.4204%; height: 25px; text-align: center; vertical-align:bottom;">
<p><span style="color: #ff0000;">Ενημερώθηκε</span></p>
</td>
<td style="width: 73.5796%; height: 25px;">&nbsp;</td>
</tr>
<tr style="height: 18px;">
<td style="width: 26.4204%; height: 25px; text-align: center; vertical-align:bottom;">
<p><span style="color: #ff0000;">Ολοκληρώθηκε</span></p>
</td>
<td style="width: 73.5796%; height: 25px;">&nbsp;</td>
</tr>
<tr style="height: 18px;">
<td style="width: 26.4204%; height: 25px; text-align: center; vertical-align:bottom;">
<p><span style="color: #ff0000;">Παραδόθηκε</span></p>
</td>
<td style="width: 73.5796%; height: 25px;">&nbsp;</td>
</tr>
<tr style="height: 18px;">
<td style="width: 26.4204%; height: 25px; text-align: center; vertical-align:bottom;">
<p><span style="color: #ff0000;">Ημερ. Παράδοσης</span></p>
</td>
<td style="width: 73.5796%; height: 25px;">&nbsp;</td>
</tr>
</tbody>
</table>
    </table>

    
    </font>
    </body>
            </html>
            """

        convertHtmlToPdf(sourceHtml, outputFilename)
        file_to_open = os.path.abspath(outputFilename)
        subprocess.Popen(file_to_open, shell=True)

    def show_add_new_customer_window(self):
        self.machine_safe_to_save = False
        self.customer_safe_to_save = False
        self.customer_combobox.setEnabled(True)
        self.customer_lineEdit.setReadOnly(False)

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
        self.machine_safe_to_save = False
        self.customer_safe_to_save = True
        self.machine_combobox.setEnabled(True)
        self.machine_lineEdit.setReadOnly(False)
        self.add_new_machine_window = QtWidgets.QWidget()
        # self.show_add_new_customer_window.setWindowTitle("Προσθήκη νέου πελάτη")
        self.add_new_machine = Ui_add_new_machine_window()
        self.add_new_machine.selected_customer = self.selected_customer
        # Αρχικοποιηση των κουμπιων, γραμμων επεξεργασίας κτλπ
        self.add_new_machine.setupUi(self.add_new_machine_window)

        self.add_new_machine.window = self.add_new_machine_window  # Αν θέλουμε να ανοιγουν πολλα παράθυρα
        self.add_new_machine_window.show()
        self.add_new_machine.window_closed.connect(lambda: (self.refresh_machines(),
                                                            self.add_new_machine_window.close()))

    def closeEvent(self, event):
        self.window_closed.emit()
        event.accept()
        # event.ignore()  # if you want the window to never be closed


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")
    Add_Task_Window = QtWidgets.QWidget()
    ui = Ui_Add_Task_Window()
    ui.setupUi(Add_Task_Window)
    Add_Task_Window.show()
    sys.exit(app.exec_())
