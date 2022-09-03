# -*- coding: utf-8 -*-
# Created by: PyQt5 UI code generator 5.15.4

import traceback
import subprocess
from xhtml2pdf import pisa
import re
import os
import sys
import shutil
from datetime import datetime
from PyQt5 import QtCore, QtGui, QtWidgets
from db import (check_if_actions_service_data_exist, Service_data, service_session, check_if_reason_service_data_exist,
                fetch_service_reasons, fetch_service_actions,get_consumables_from_service_id, Service,
                get_spare_part_from_code_from_all_db, get_consumable_from_id, store_session , fetch_service_technicians,
                )

from settings import VERSION, root_logger, today, SPARE_PARTS_ROOT, user
from add_spare_part_from_store import Ui_Add_Spare_Part_From_Store
from view_files_window import Ui_View_Files_Window
from add_spare_part_not_from_store import Ui_Add_Spare_Part_Not_From_Store
from send_email import Ui_Send_Email_Window

sys.stderr.write = root_logger.error
sys.stdout.write = root_logger.info


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


class Ui_Add_Service_Window(QtWidgets.QWidget):
    window_closed = QtCore.pyqtSignal()  # Το Signal πρεπει να είναι εκτός __init__ δεν δουλευει αλλιως

    def __init__(self):
        super(Ui_Add_Service_Window, self).__init__()
        self.selected_machine = None
        self.new_service = None
        self.images_path = None
        self.files = None

        self.font_14_bold = QtGui.QFont()
        self.font_14_bold.setFamily("Calibri")
        self.font_14_bold.setPointSize(14)
        self.font_14_bold.setBold(True)
        self.font_14_bold.setWeight(75)

        self.font_12 = QtGui.QFont()
        self.font_12.setFamily("Calibri")
        self.font_12.setPointSize(12)
        self.font_12.setBold(False)
        self.font_12.setWeight(75)

        self.font_12_bold = QtGui.QFont()
        self.font_12_bold.setFamily("Calibri")
        self.font_12_bold.setPointSize(12)
        self.font_12_bold.setBold(True)
        self.font_12_bold.setWeight(75)

        self.font_13 = QtGui.QFont()
        self.font_13.setFamily("Calibri")
        self.font_13.setPointSize(13)
        self.font_13.setBold(False)
        self.font_13.setWeight(75)

        self.font_13_bold = QtGui.QFont()
        self.font_13_bold.setFamily("Calibri")
        self.font_13_bold.setPointSize(13)
        self.font_13_bold.setBold(True)
        self.font_13_bold.setWeight(75)

        self.print_icon = QtGui.QIcon()
        self.print_icon.addPixmap(QtGui.QPixmap("icons/print_it.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)

    def setupUi(self, Add_Service_Window):
        Add_Service_Window.setObjectName("Edit_Task_Window")
        Add_Service_Window.resize(800, 600)
        Add_Service_Window.setMaximumSize(QtCore.QSize(16777213, 16777215))
        Add_Service_Window.setWindowTitle(f"Επεξεργασία εργασίας {VERSION}")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icons/service.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Add_Service_Window.setWindowIcon(icon)
        Add_Service_Window.setWindowFilePath("")
        self.gridLayout_3 = QtWidgets.QGridLayout(Add_Service_Window)
        self.gridLayout_3.setObjectName("gridLayout_3")

        # Top Label
        self.top_label = QtWidgets.QLabel(Add_Service_Window)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.top_label.sizePolicy().hasHeightForWidth())
        self.top_label.setSizePolicy(sizePolicy)
        self.top_label.setMinimumSize(QtCore.QSize(0, 30))
        self.top_label.setFont(self.font_14_bold)
        self.top_label.setStyleSheet("background-color: rgb(0, 85, 127);\n"
                                     "color: rgb(255, 255, 255);")
        self.top_label.setAlignment(QtCore.Qt.AlignCenter)
        self.top_label.setObjectName("top_label")
        self.gridLayout_3.addWidget(self.top_label, 0, 0, 1, 3)


        # Tabs Καρτέλες
        self.tabWidget = QtWidgets.QTabWidget(Add_Service_Window)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setFont(self.font_13_bold)
        self.tabWidget.setTabPosition(QtWidgets.QTabWidget.North)
        self.tabWidget.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.tabWidget.setIconSize(QtCore.QSize(25, 25))
        self.tabWidget.setMovable(True)
        self.tabWidget.setObjectName("tabWidget")

        # Εργασία καρτέλα tab
        self.work_tab = QtWidgets.QWidget()
        self.work_tab.setObjectName("work_tab")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.work_tab)
        self.gridLayout_2.setObjectName("gridLayout_2")

        # Ημερομηνία date Label
        self.date_label = QtWidgets.QLabel(self.work_tab)
        self.date_label.setMinimumSize(QtCore.QSize(0, 25))
        self.date_label.setFont(self.font_12_bold)
        self.date_label.setStyleSheet("background-color: rgb(93, 93, 93);\n"
                                      "color: rgb(255, 255, 255);")
        self.date_label.setAlignment(QtCore.Qt.AlignCenter)
        self.date_label.setObjectName("date_label")
        self.gridLayout_2.addWidget(self.date_label, 0, 0, 1, 1)
        # date edit
        self.dateEdit = QtWidgets.QDateEdit(self.work_tab)
        self.dateEdit.setMinimumSize(QtCore.QSize(150, 35))
        self.dateEdit.setFont(self.font_13_bold)
        self.dateEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.dateEdit.setDisplayFormat("dd/MM/yyyy")
        self.dateEdit.setCalendarPopup(True)
        self.dateEdit.setObjectName("dateEdit")
        self.gridLayout_2.addWidget(self.dateEdit, 1, 0, 1, 1)

        # technician label
        self.technician_label = QtWidgets.QLabel(self.work_tab)
        self.technician_label.setMinimumSize(QtCore.QSize(0, 25))
        self.technician_label.setFont(self.font_12_bold)
        self.technician_label.setStyleSheet("background-color: rgb(93, 93, 93);\n"
                                            "color: rgb(255, 255, 255);")
        self.technician_label.setAlignment(QtCore.Qt.AlignCenter)
        self.technician_label.setObjectName("technician_label")
        self.gridLayout_2.addWidget(self.technician_label, 0, 1, 1, 1)
        # Τεχνικός edit
        self.technician_lineEdit = QtWidgets.QLineEdit(self.work_tab)
        self.technician_lineEdit.setMinimumSize(QtCore.QSize(0, 35))
        self.technician_lineEdit.setFont(self.font_13)
        self.technician_lineEdit.setObjectName("technician_lineEdit")
        self.technician_combobox = QtWidgets.QComboBox(self.work_tab)
        self.technician_combobox.setFont(self.font_13)
        self.technician_combobox.setLineEdit(self.technician_lineEdit)
        self.gridLayout_2.addWidget(self.technician_combobox, 1, 1, 1, 1)

        # counter label
        self.counter_label = QtWidgets.QLabel(self.work_tab)
        self.counter_label.setMinimumSize(QtCore.QSize(0, 25))
        self.counter_label.setFont(self.font_12_bold)
        self.counter_label.setStyleSheet("background-color: rgb(93, 93, 93);\n"
                                         "color: rgb(255, 255, 255);")
        self.counter_label.setAlignment(QtCore.Qt.AlignCenter)
        self.counter_label.setObjectName("counter_label")
        self.gridLayout_2.addWidget(self.counter_label, 0, 2, 1, 2)
        # counter edit
        self.counter_lineEdit = QtWidgets.QLineEdit(self.work_tab)
        self.counter_lineEdit.setMinimumSize(QtCore.QSize(0, 35))
        self.counter_lineEdit.setFont(self.font_13)
        self.counter_lineEdit.setText("")
        self.counter_lineEdit.setObjectName("counter_lineEdit")
        self.gridLayout_2.addWidget(self.counter_lineEdit, 1, 2, 1, 2)

        # next service label
        self.next_service_label = QtWidgets.QLabel(self.work_tab)
        self.next_service_label.setMinimumSize(QtCore.QSize(220, 25))
        self.next_service_label.setFont(self.font_12_bold)
        self.next_service_label.setStyleSheet("background-color: rgb(93, 93, 93);\n"
                                              "color: rgb(255, 255, 255);")
        self.next_service_label.setAlignment(QtCore.Qt.AlignCenter)
        self.next_service_label.setObjectName("next_service_label")
        self.gridLayout_2.addWidget(self.next_service_label, 0, 4, 1, 1)
        # next service edit
        self.next_service_lineEdit = QtWidgets.QLineEdit(self.work_tab)
        self.next_service_lineEdit.setMinimumSize(QtCore.QSize(0, 35))
        self.next_service_lineEdit.setFont(self.font_13)
        self.next_service_lineEdit.setText("")
        self.next_service_lineEdit.setObjectName("next_service_lineEdit")
        self.gridLayout_2.addWidget(self.next_service_lineEdit, 1, 4, 1, 1)

        # reason label
        self.reason_label = QtWidgets.QLabel(self.work_tab)
        self.reason_label.setMinimumSize(QtCore.QSize(0, 25))
        self.reason_label.setFont(self.font_12_bold)
        self.reason_label.setStyleSheet("background-color: rgb(255, 170, 0);\n"
                                        "color: rgb(255, 255, 255);")
        self.reason_label.setAlignment(QtCore.Qt.AlignCenter)
        self.reason_label.setObjectName("reason_label")
        self.gridLayout_2.addWidget(self.reason_label, 2, 0, 1, 4)
        # reason edit
        self.reason_lineEdit = QtWidgets.QLineEdit(self.work_tab)
        self.reason_lineEdit.setMinimumSize(QtCore.QSize(0, 35))
        self.reason_lineEdit.setFont(self.font_13)
        self.reason_lineEdit.setObjectName("reason_lineEdit")
        self.reason_combobox = QtWidgets.QComboBox(self.work_tab)
        self.reason_combobox.setFont(self.font_13)
        self.reason_combobox.setLineEdit(self.reason_lineEdit)
        self.gridLayout_2.addWidget(self.reason_combobox, 3, 0, 1, 3)

        # dte label
        self.dte_label = QtWidgets.QLabel(self.work_tab)
        self.dte_label.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.dte_label.setFont(self.font_12_bold)
        self.dte_label.setStyleSheet("background-color: rgb(255, 170, 0);")
        self.dte_label.setText("ΔΤΕ")
        self.dte_label.setTextFormat(QtCore.Qt.RichText)
        self.dte_label.setScaledContents(True)
        self.dte_label.setAlignment(QtCore.Qt.AlignCenter)
        self.dte_label.setWordWrap(True)
        self.dte_label.setObjectName("dte_label")
        self.gridLayout_2.addWidget(self.dte_label, 2, 4, 1, 1)
        # dte edit
        self.dte_lineEdit = QtWidgets.QLineEdit(self.work_tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dte_lineEdit.sizePolicy().hasHeightForWidth())
        self.dte_lineEdit.setSizePolicy(sizePolicy)
        self.dte_lineEdit.setMinimumSize(QtCore.QSize(0, 35))
        self.dte_lineEdit.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.dte_lineEdit.setFont(self.font_12_bold)
        self.dte_lineEdit.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.dte_lineEdit.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.dte_lineEdit.setPlaceholderText("")
        self.dte_lineEdit.setObjectName("dte_lineEdit")
        self.gridLayout_2.addWidget(self.dte_lineEdit, 3, 4, 1, 1)

        # Ενέργειες label
        self.action_label = QtWidgets.QLabel(self.work_tab)
        self.action_label.setMinimumSize(QtCore.QSize(0, 25))
        self.action_label.setFont(self.font_12_bold)
        self.action_label.setStyleSheet("background-color: rgb(0, 85, 127);\n"
                                        "color: rgb(255, 255, 255);")
        self.action_label.setAlignment(QtCore.Qt.AlignCenter)
        self.action_label.setObjectName("action_label")
        self.gridLayout_2.addWidget(self.action_label, 4, 0, 1, 4)
        # action edit
        self.action_lineEdit = QtWidgets.QLineEdit(self.work_tab)
        self.action_lineEdit.setMinimumSize(QtCore.QSize(0, 35))
        self.action_lineEdit.setFont(self.font_13)
        self.action_lineEdit.setObjectName("action_lineEdit")
        self.actions_combobox = QtWidgets.QComboBox(self.work_tab)
        self.actions_combobox.setFont(self.font_13)
        self.actions_combobox.setLineEdit(self.action_lineEdit)
        self.gridLayout_2.addWidget(self.actions_combobox, 5, 0, 1, 3)

        # cost label
        self.cost_label = QtWidgets.QLabel(self.work_tab)
        self.cost_label.setMinimumSize(QtCore.QSize(0, 25))
        self.cost_label.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.cost_label.setFont(self.font_12_bold)
        self.cost_label.setStyleSheet("background-color: rgb(0, 85, 127);\n"
                                        "color: rgb(255, 255, 255);")
        self.cost_label.setAlignment(QtCore.Qt.AlignCenter)
        self.cost_label.setObjectName("cost_label")
        self.gridLayout_2.addWidget(self.cost_label, 4, 4, 1, 1)
        # cost edit
        self.cost_lineEdit = QtWidgets.QLineEdit(self.work_tab)
        self.cost_lineEdit.setMinimumSize(QtCore.QSize(0, 35))
        self.cost_lineEdit.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.cost_lineEdit.setFont(self.font_13)
        self.cost_lineEdit.setObjectName("cost_lineEdit")
        self.gridLayout_2.addWidget(self.cost_lineEdit, 5, 4, 1, 1)

        # Σημειώσεις Label notes
        self.notes_label = QtWidgets.QLabel(self.work_tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.notes_label.sizePolicy().hasHeightForWidth())
        self.notes_label.setSizePolicy(sizePolicy)
        self.notes_label.setMinimumSize(QtCore.QSize(0, 30))
        self.notes_label.setFont(self.font_12_bold)
        self.notes_label.setStyleSheet("background-color: rgb(93, 93, 93);\n"
                                       "color: rgb(255, 255, 255);")
        self.notes_label.setAlignment(QtCore.Qt.AlignCenter)
        self.notes_label.setObjectName("notes_label")
        self.gridLayout_2.addWidget(self.notes_label, 6, 0, 1, 5)
        # notes edit
        self.notes_textEdit = QtWidgets.QTextEdit(self.work_tab)
        self.notes_textEdit.setFont(self.font_13)
        self.notes_textEdit.setObjectName("notes_textEdit")
        self.gridLayout_2.addWidget(self.notes_textEdit, 7, 0, 1, 5)

        # Save btn
        self.save_toolButton = QtWidgets.QToolButton(Add_Service_Window)
        self.save_toolButton.setFont(self.font_12_bold)
        self.save_toolButton.setStyleSheet("background-color: rgb(103, 103, 103);\n"
                                           "color: rgb(255, 255, 255);")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("icons/Save.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.save_toolButton.setIcon(icon3)
        self.save_toolButton.setIconSize(QtCore.QSize(30, 30))
        self.save_toolButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.save_toolButton.setObjectName("save_toolButton")
        self.save_toolButton.clicked.connect(self.save_service)
        self.gridLayout_3.addWidget(self.save_toolButton, 2, 2, 1, 1)

        # Email btn
        self.email_toolButton = QtWidgets.QToolButton(Add_Service_Window)
        self.email_toolButton.setFont(self.font_12_bold)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("icons/send_mail.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.email_toolButton.setIcon(icon4)
        self.email_toolButton.setIconSize(QtCore.QSize(30, 30))
        self.email_toolButton.setObjectName("email_toolButton")
        self.email_toolButton.clicked.connect(self.send_mail)
        self.gridLayout_3.addWidget(self.email_toolButton, 2, 0, 1, 1)

        # Print btn
        self.print_toolButton = QtWidgets.QToolButton(Add_Service_Window)
        self.print_toolButton.setFont(self.font_12_bold)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("icons/print_it.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.print_toolButton.setIcon(icon2)
        self.print_toolButton.setIconSize(QtCore.QSize(30, 30))
        self.print_toolButton.setObjectName("print_toolButton")
        self.print_toolButton.clicked.connect(self.print_to_pdf)
        self.gridLayout_3.addWidget(self.print_toolButton, 2, 1, 1, 1)

        # add action btn
        self.add_action_toolButton = QtWidgets.QToolButton(self.work_tab)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("icons/add_to_service_data2.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.add_action_toolButton.setIcon(icon5)
        self.add_action_toolButton.setIconSize(QtCore.QSize(30, 30))
        self.add_action_toolButton.setObjectName("add_action_toolButton")
        self.add_action_toolButton.clicked.connect(self.add_action_to_db)
        self.gridLayout_2.addWidget(self.add_action_toolButton, 5, 3, 1, 1)

        # add reason brn
        self.add_reason_toolButton = QtWidgets.QToolButton(self.work_tab)
        self.add_reason_toolButton.setIcon(icon5)
        self.add_reason_toolButton.setIconSize(QtCore.QSize(30, 30))
        self.add_reason_toolButton.setObjectName("add_reason_toolButton")
        self.add_reason_toolButton.clicked.connect(self.add_reason_to_db)
        self.gridLayout_2.addWidget(self.add_reason_toolButton, 3, 3, 1, 1)

        # Spare part tab
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap("icons/service.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tabWidget.addTab(self.work_tab, icon7, "")
        self.spare_parts_tab = QtWidgets.QWidget()
        self.spare_parts_tab.setObjectName("spare_parts_tab")
        self.gridLayout = QtWidgets.QGridLayout(self.spare_parts_tab)
        self.gridLayout.setObjectName("gridLayout")
        # add spare part from store btn
        self.add_spare_part_from_store_toolButton = QtWidgets.QToolButton(self.spare_parts_tab)
        self.add_spare_part_from_store_toolButton.setMinimumSize(QtCore.QSize(0, 50))
        self.add_spare_part_from_store_toolButton.setMaximumSize(QtCore.QSize(16777215, 50))
        self.add_spare_part_from_store_toolButton.setFont(self.font_12_bold)
        self.add_spare_part_from_store_toolButton.setStyleSheet("background-color: rgb(0, 85, 0);\n"
                                                                "color: rgb(255, 255, 255);")
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap("icons/add_spare_parts.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.add_spare_part_from_store_toolButton.setIcon(icon8)
        self.add_spare_part_from_store_toolButton.setIconSize(QtCore.QSize(30, 30))
        self.add_spare_part_from_store_toolButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.add_spare_part_from_store_toolButton.setObjectName("add_spare_part_from_store_toolButton")
        self.add_spare_part_from_store_toolButton.clicked.connect(self.show_add_spare_part_from_store_window)
        self.gridLayout.addWidget(self.add_spare_part_from_store_toolButton, 2, 0, 1, 1)

        # add files btn
        self.add_files_toolButton = QtWidgets.QToolButton(self.spare_parts_tab)
        self.add_files_toolButton.setMinimumSize(QtCore.QSize(0, 50))
        self.add_files_toolButton.setMaximumSize(QtCore.QSize(16777215, 50))
        self.add_files_toolButton.setFont(self.font_12_bold)
        self.add_files_toolButton.setStyleSheet("background-color: rgb(0, 85, 0);\n"
                                                "color: rgb(255, 255, 255);")
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap("icons/add_files.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.add_files_toolButton.setIcon(icon9)
        self.add_files_toolButton.setIconSize(QtCore.QSize(30, 30))
        self.add_files_toolButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.add_files_toolButton.setObjectName("add_files_toolButton")
        self.add_files_toolButton.clicked.connect(self.add_file)
        self.gridLayout.addWidget(self.add_files_toolButton, 3, 0, 1, 1)

        self.delete_spare_part_toolButton = QtWidgets.QToolButton(self.spare_parts_tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.delete_spare_part_toolButton.sizePolicy().hasHeightForWidth())
        self.delete_spare_part_toolButton.setSizePolicy(sizePolicy)
        self.delete_spare_part_toolButton.setMinimumSize(QtCore.QSize(160, 50))
        self.delete_spare_part_toolButton.setMaximumSize(QtCore.QSize(200, 50))
        self.delete_spare_part_toolButton.setFont(self.font_12_bold)
        self.delete_spare_part_toolButton.setStyleSheet("background-color: rgb(103, 103, 103);\n"
                                                        "color: rgb(255, 255, 255);")
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap("icons/delete_spare_parts.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.delete_spare_part_toolButton.setIcon(icon10)
        self.delete_spare_part_toolButton.setIconSize(QtCore.QSize(30, 30))
        self.delete_spare_part_toolButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.delete_spare_part_toolButton.setObjectName("delete_spare_part_toolButton")
        self.delete_spare_part_toolButton.clicked.connect(self.delete_spare_part)
        self.gridLayout.addWidget(self.delete_spare_part_toolButton, 2, 2, 1, 1)

        self.view_files_toolButton = QtWidgets.QToolButton(self.spare_parts_tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.view_files_toolButton.sizePolicy().hasHeightForWidth())
        self.view_files_toolButton.setSizePolicy(sizePolicy)
        self.view_files_toolButton.setMinimumSize(QtCore.QSize(160, 50))
        self.view_files_toolButton.setMaximumSize(QtCore.QSize(200, 50))
        self.view_files_toolButton.setFont(self.font_12_bold)
        self.view_files_toolButton.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.view_files_toolButton.setAutoFillBackground(False)
        self.view_files_toolButton.setStyleSheet("background-color: rgb(103, 103, 103);\n"
                                                 "color: rgb(255, 255, 255);")
        icon11 = QtGui.QIcon()
        icon11.addPixmap(QtGui.QPixmap("icons/view_files_new.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.view_files_toolButton.setIcon(icon11)
        self.view_files_toolButton.setIconSize(QtCore.QSize(30, 30))
        self.view_files_toolButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.view_files_toolButton.setObjectName("view_files_toolButton")
        self.view_files_toolButton.hide()
        self.view_files_toolButton.clicked.connect(self.view_files)
        self.gridLayout.addWidget(self.view_files_toolButton, 3, 2, 1, 1)

        # Treewidget
        self.spare_parts_treeWidget = QtWidgets.QTreeWidget(self.spare_parts_tab)
        self.spare_parts_treeWidget.setMinimumSize(QtCore.QSize(0, 350))
        self.spare_parts_treeWidget.setMaximumSize(QtCore.QSize(16777215, 350))
        self.spare_parts_treeWidget.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.spare_parts_treeWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.spare_parts_treeWidget.setAlternatingRowColors(True)
        self.spare_parts_treeWidget.setWordWrap(True)
        self.spare_parts_treeWidget.setFont(self.font_12_bold)
        self.spare_parts_treeWidget.setObjectName("spare_parts_treeWidget")
        self.spare_parts_treeWidget.header().setStretchLastSection(True)
        self.gridLayout.addWidget(self.spare_parts_treeWidget, 1, 0, 1, 3)

        self.add_spare_part_toolButton = QtWidgets.QToolButton(self.spare_parts_tab)
        self.add_spare_part_toolButton.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.add_spare_part_toolButton.sizePolicy().hasHeightForWidth())
        self.add_spare_part_toolButton.setSizePolicy(sizePolicy)
        self.add_spare_part_toolButton.setFont(self.font_12_bold)
        self.add_spare_part_toolButton.setStyleSheet("background-color: rgb(0, 85, 127);\n"
                                                     "color: rgb(255, 255, 255);")
        icon12 = QtGui.QIcon()
        icon12.addPixmap(QtGui.QPixmap("icons/add_gears.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.add_spare_part_toolButton.setIcon(icon12)
        self.add_spare_part_toolButton.setIconSize(QtCore.QSize(30, 30))
        self.add_spare_part_toolButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.add_spare_part_toolButton.setObjectName("add_spare_part_toolButton")
        self.add_spare_part_toolButton.clicked.connect(self.show_add_spare_part_not_from_store_window)
        self.gridLayout.addWidget(self.add_spare_part_toolButton, 2, 1, 1, 1)
        self.spare_parts_label = QtWidgets.QLabel(self.spare_parts_tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spare_parts_label.sizePolicy().hasHeightForWidth())
        self.spare_parts_label.setSizePolicy(sizePolicy)
        self.spare_parts_label.setMinimumSize(QtCore.QSize(0, 30))
        self.spare_parts_label.setFont(self.font_14_bold)
        self.spare_parts_label.setStyleSheet("background-color: rgb(83, 83, 83);\n"
                                             "color: rgb(255, 255, 255);")
        self.spare_parts_label.setAlignment(QtCore.Qt.AlignCenter)
        self.spare_parts_label.setObjectName("spare_parts_label")
        self.gridLayout.addWidget(self.spare_parts_label, 0, 0, 1, 3)
        icon13 = QtGui.QIcon()
        icon13.addPixmap(QtGui.QPixmap("icons/gears.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tabWidget.addTab(self.spare_parts_tab, icon13, "")
        self.gridLayout_3.addWidget(self.tabWidget, 1, 0, 1, 3)

        # Esc
        self.shortcut_esc = QtWidgets.QShortcut(QtGui.QKeySequence('Escape'), Add_Service_Window)
        self.shortcut_esc.activated.connect(self.close)

        self.retranslateUi(Add_Service_Window)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Add_Service_Window)
        self.make_new_service()
        self.fetch_service_data()
        self.show_spare_parts()
        self.update_files()

    def retranslateUi(self, Add_Service_Window):
        _translate = QtCore.QCoreApplication.translate
        self.top_label.setText(_translate("Add_Service_Window", "Επεξεργασία εργασίας"))
        self.save_toolButton.setText(_translate("Add_Service_Window", "Αποθήκευση"))
        self.email_toolButton.setText(_translate("Add_Service_Window", "..."))
        self.action_label.setText(_translate("Add_Service_Window", "Ενέργειες"))
        self.notes_label.setText(_translate("Add_Service_Window", "Σημειώσεις"))
        self.date_label.setText(_translate("Add_Service_Window", "Ημερομηνία"))
        self.reason_label.setText(_translate("Add_Service_Window", "Σκοπός εργασίας"))
        self.add_action_toolButton.setText(_translate("Add_Service_Window", "..."))
        self.next_service_label.setText(_translate("Add_Service_Window", "Επ. Service"))
        self.cost_label.setText(_translate("Add_Service_Window", "Κόστος"))
        self.add_reason_toolButton.setText(_translate("Add_Service_Window", "..."))
        self.technician_label.setText(_translate("Add_Service_Window", "Τεχνικός"))
        self.counter_label.setText(_translate("Add_Service_Window", "Μετρητής"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.work_tab), _translate("Add_Service_Window", "Εργασία"))
        self.add_spare_part_from_store_toolButton.setText(_translate("Add_Service_Window", "  Προσθήκη ανταλλ. \n"
                                                                                         "  εντός αποθήκης"))
        self.add_files_toolButton.setText(_translate("Add_Service_Window", "  Προσθήκη αρχείων"))
        self.delete_spare_part_toolButton.setText(_translate("Add_Service_Window", "    Διαγραφή ανταλλ."))
        self.view_files_toolButton.setText(_translate("Add_Service_Window", "   Προβολή αρχείων"))
        self.spare_parts_treeWidget.setSortingEnabled(True)
        self.add_spare_part_toolButton.setText(_translate("Add_Service_Window", "Προσθήκη ανταλλ. \n"
                                                                              " εκτός αποθήκης"))
        self.spare_parts_label.setText(_translate("Add_Service_Window", "Ανταλλακτικά"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.spare_parts_tab),
                                  _translate("Add_Service_Window", "Ανταλλακτικά"))

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
        self.reason_lineEdit.setText("")

        self.actions_completer = QtWidgets.QCompleter(self.service_actions)
        self.actions_completer.popup().setFont(self.font_13)
        self.action_lineEdit.setCompleter(self.actions_completer)
        self.actions_combobox.clear()
        self.actions_combobox.addItems(self.service_actions)
        self.action_lineEdit.setText("")

    def make_new_service(self):
        if self.selected_machine is None:
            return
        self.dateEdit.setDate(QtCore.QDate.currentDate())
        self.notes_textEdit.setText(f"-------------------------------- {user} {today.replace(' ', '/')} --------------------------------\n")
        self.selected_service = Service(Ημερομηνία=today.replace(" ", "/"),
                                   Σκοπός_Επίσκεψης="",
                                   Ενέργειες="",
                                   Τεχνικός="",
                                   Σημειώσεις=self.notes_textEdit.toPlainText(),
                                   Μετρητής="",
                                   Επ_Service="",
                                   Copier_ID=self.selected_machine.ID,
                                   ΔΤΕ="",
                                   Price="")
        service_session.add(self.selected_service)

    def show_spare_parts(self):
        # Spare parts
        self.spare_parts_treeWidget.setHeaderLabels(
            ["ID", "Κωδικός", "Περιγραφή", "Τεμάχια", "Part No.", "Σημειώσεις"])
        self.spare_parts_treeWidget.headerItem().setTextAlignment(0, QtCore.Qt.AlignLeft)
        self.spare_parts_treeWidget.headerItem().setTextAlignment(1, QtCore.Qt.AlignCenter)
        self.spare_parts_treeWidget.headerItem().setTextAlignment(2, QtCore.Qt.AlignCenter)
        self.spare_parts_treeWidget.headerItem().setTextAlignment(3, QtCore.Qt.AlignCenter)
        self.spare_parts_treeWidget.headerItem().setTextAlignment(4, QtCore.Qt.AlignCenter)
        self.spare_parts_treeWidget.header().setStyleSheet(u"background-color: rgb(203, 203, 203);" "color: black;"
                                                           "font-style: normal;font-size: 13pt;font-weight: bold;")
        self.selected_service_spare_parts = get_consumables_from_service_id(self.selected_service.ID)
        self.spare_parts_treeWidget.clear()
        for item in self.selected_service_spare_parts:
            self.spare_part_item = TreeWidgetItem(self.spare_parts_treeWidget,
                                                  [str(item.ID),
                                                   str(item.ΚΩΔΙΚΟΣ),
                                                   str(item.ΠΕΡΙΓΡΑΦΗ),
                                                   str(item.ΤΕΜΑΧΙΑ),
                                                   str(item.PARTS_NR),
                                                   str(item.ΠΑΡΑΤΗΡΗΣΗΣ)])
            self.spare_part_item.setTextAlignment(0, QtCore.Qt.AlignLeft)
            self.spare_part_item.setTextAlignment(1, QtCore.Qt.AlignCenter)
            self.spare_part_item.setTextAlignment(2, QtCore.Qt.AlignCenter)
            self.spare_part_item.setTextAlignment(3, QtCore.Qt.AlignCenter)
            self.spare_part_item.setTextAlignment(4, QtCore.Qt.AlignCenter)

            self.spare_parts_treeWidget.setStyleSheet("QTreeView::item { padding: 5px }")
            # Χρωματισμός πεδίων
            if "C/M/Y" in item.ΠΕΡΙΓΡΑΦΗ:
                self.spare_part_item.setBackground(2, QtGui.QColor('green'))
                self.spare_part_item.setForeground(2, QtGui.QColor('white'))
            elif "CYAN" in item.ΠΕΡΙΓΡΑΦΗ:
                self.spare_part_item.setBackground(2, QtGui.QColor('#0517D2'))
                self.spare_part_item.setForeground(2, QtGui.QColor('white'))
            elif "MAGENTA" in item.ΠΕΡΙΓΡΑΦΗ:
                self.spare_part_item.setBackground(2, QtGui.QColor('#D205CF'))
                self.spare_part_item.setForeground(2, QtGui.QColor('white'))
            elif "YELLOW" in item.ΠΕΡΙΓΡΑΦΗ:
                self.spare_part_item.setBackground(2, QtGui.QColor('yellow'))
                self.spare_part_item.setForeground(2, QtGui.QColor('black'))
            elif "GRAY" in item.ΠΕΡΙΓΡΑΦΗ:
                self.spare_part_item.setBackground(2, QtGui.QColor("gray"))
                self.spare_part_item.setForeground(2, QtGui.QColor('white'))
            elif "BLACK" in item.ΠΕΡΙΓΡΑΦΗ:
                self.spare_part_item.setBackground(2, QtGui.QColor("black"))
                self.spare_part_item.setForeground(2, QtGui.QColor('white'))

            self.spare_parts_treeWidget.addTopLevelItem(self.spare_part_item)
            self.spare_parts_treeWidget.resizeColumnToContents(2)
        self.spare_parts_treeWidget.setColumnWidth(0, 1)
        self.spare_parts_treeWidget.setColumnWidth(1, 80)
        self.spare_parts_treeWidget.setColumnWidth(2, 350)
        self.spare_parts_treeWidget.setColumnWidth(3, 80)
        self.spare_parts_treeWidget.setColumnWidth(4, 80)
        self.spare_parts_treeWidget.sortByColumn(2, QtCore.Qt.AscendingOrder)

    def update_files(self):
        try:
            date = datetime.strptime(self.selected_service.Ημερομηνία, "%d/%m/%Y")
            year = date.year
        except ValueError:  # Οταν δεν έχουμε βάλει Ημερομηνία στο service
            year = datetime.year
        self.images_path = os.path.join(SPARE_PARTS_ROOT, f"{year}", f"{self.selected_service.ID}")
        if os.path.exists(self.images_path):
            self.files = os.listdir(self.images_path)
            if len(self.files) > 0:  # Μπορεί να υπάρχει ο φάκελος αλλά να μήν έχει αρχεία μέσα
                                    # --> οταν τα σβήνουμε μενει αδειος
                self.view_files_toolButton.show()
                self.view_files_toolButton.setText(f"   Προβολή {len(self.files)} αρχείων")
            else:
                self.view_files_toolButton.hide()

    def add_reason_to_db(self):
        try:
            if check_if_reason_service_data_exist(self.reason_lineEdit.text().upper()):
                QtWidgets.QMessageBox.warning(None, "Προσοχή", f"Το '{self.reason_lineEdit.text().upper()}' υπάρχει")
                return
            reason = Service_data(Σκοπός=self.reason_lineEdit.text().upper())
            service_session.add(reason)
            service_session.commit()
            self.fetch_service_data()
            QtWidgets.QMessageBox.information(None, "Πληροφορία!", "Αποθηκεύτηκε")
        except Exception:
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
            traceback.print_exc()
            return

    def add_file(self):
        options = QtWidgets.QFileDialog.Options()
        new_files, _ = QtWidgets.QFileDialog.getOpenFileNames(self, "QFileDialog.getOpenFileNames()", "",
                                                    "Υποστηριζόμενα αρχεία .bmp .gif .png .jpeg .jpg .pdf (*.bmp "
                                                    "*.gif *.png *.jpeg *.jpg *.pdf)", options=options)
        if new_files:
            if not os.path.exists(self.images_path):
                os.makedirs(self.images_path)

            # Εισαγωγη αρχείων
            # Αν υπάρχουν αρχεία Ελεγχος αν το αρχείο υπάρχει σε αυτο το προιόν
            for new_file in new_files:
                basename = os.path.basename(new_file).replace(" ", "_")
                if not os.path.exists(os.path.join(self.images_path, os.path.basename(new_file))):
                    shutil.copy(new_file, os.path.join(self.images_path, basename), follow_symlinks=False)
                    QtWidgets.QMessageBox.information(None, "Επιτυχία", f'Το αρχεία {os.path.basename(new_file)} προστέθηκε '
                                                              f'επιτυχώς')
                    # Να εμφανίσει το αρχείο
                    self.update_files()
                else:
                    QtWidgets.QMessageBox.warning(None, "Σφάλμα",
                                        f"Το αρχείο {os.path.basename(new_file)} υπάρχει.\nΠαρακαλώ αλλάξτε όνομα ή "
                                        f"επιλεξτε διαφορετικό αρχείο")

    # Αποστολή email
    def send_mail(self):
        status = "Απο προσθήκη συντήρησης"
        data = [self.dateEdit.date().toString("dd/MM/yyyy"),
                self.reason_lineEdit.text(),
                self.technician_lineEdit.text(),
                self.action_lineEdit.text(),
                self.counter_lineEdit.text(),
                " ",  # self.timeEdit.time().toString('HH:mm')
                " ",  # self.phones_lineEdit.text()
                self.notes_textEdit.toHtml(),
                self.dte_lineEdit.text(),
                status]

        self.show_send_email_window = QtWidgets.QWidget()
        # self.show_add_new_customer_window.setWindowTitle("Προσθήκη νέου πελάτη")
        self.show_send_email = Ui_Send_Email_Window()
        self.show_send_email.selected_customer = self.selected_service.machine.Customer.Επωνυμία_Επιχείρησης
        self.show_send_email.selected_machine = self.selected_service.machine.Εταιρεία
        self.show_send_email.data_to_send = data
        self.show_send_email.files_path = self.images_path
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
        outputFilename = f"{prints_dir}/Service_Book_" + f"{self.selected_service.machine.Εταιρεία}".\
            replace(" ", "_").\
            replace("*", "_") + \
            f"_{self.selected_service.ID}" + ".pdf"
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
                mark.red {
                color:#ff0000;
                background: none;
                }
                mark.green {
                color:#2af406;
                background: none;
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
        html_spare_parts = []  # ΚΩΔΙΚΟΣ ΠΕΡΙΓΡΑΦΗ
        for index, spare_part in enumerate(self.selected_service_spare_parts):
            html_spare_parts.append(f"""{index+1}. <mark class="red">Κωδικός: {spare_part.ΚΩΔΙΚΟΣ} </mark> --> 
            {spare_part.ΠΕΡΙΓΡΑΦΗ} <mark class="green">Τεμάχια: {spare_part.ΤΕΜΑΧΙΑ} </mark> <br>
                                    """.replace('\n', ""))

        sourceHtml = f"""<html>

            <meta http-equiv=Content-Type content="text/html;charset=utf-8"></meta>
            <style>
            @font-face {font}
            </style>
            <body>
            <font size = "6"> 
            <h2 style="text-align: center;"><span style="text-decoration: underline;">
            <img style="float: right;" src="{src}logo-small-orange.png" alt="" width="150" height="108"/> 
            Δελτίο τεχνικής εξυπηρέτησης
            </span></h2>
            <table  border="1">


            <tbody>
            <tr style="height: 18px;">
            <td style="width: 26.4204%; height: 30px; text-align: center;">
            <h4><strong>Ημερομηνία</strong></h4>
            </td>
            <td style="width: 73.5796%; height: 30px; text-align: center;"> {self.dateEdit.date().toString("dd/MM/yyyy")}</td>
            </tr>
            
            <tr style="height: 18px;">
            <td style="width: 26.4204%; height: 30px; text-align: center;">
            <h4><strong>Μηχάνημα</strong></h4>
            </td>
            <td style="width: 73.5796%; height: 30px; text-align: center;"> {self.selected_service.machine.Εταιρεία}</td>
            </tr>
            <tr style="height: 18px;">
            <td style="width: 26.4204%; height: 30px; text-align: center;">
            <h4><strong>Μετρητής</strong></h4>
            </td>
            <td style="width: 73.5796%; height: 30px; text-align: center;"> <mark class="red">{self.counter_lineEdit.text()}</mark></td>
            </tr>
            <tr style="height: 18px;">
            <td style="width: 26.4204%; height: 30px; text-align: center;">
            <h4><strong>Επόμενο Service</strong></h4>
            </td>
            <td style="width: 73.5796%; height: 30px; text-align: center;"> <mark class="red">{self.next_service_lineEdit.text()}</mark></td>
            </tr>
            <tr style="height: 18px;">
            <td style="width: 26.4204%; height: 30px; text-align: center;">
            <h4><strong>Περιγραφή προβλήματος</strong></h4>
            </td>
            <td style="width: 73.5796%; height: 30px; text-align: center;"> {self.reason_lineEdit.text()}</td>
            </tr>
            
            <tr style="height: 18px;">
            <td style="width: 26.4204%; height: 30px; text-align: center;">
            <h4><strong>Ενέργειες</strong></h4>
            </td>
            <td style="width: 73.5796%; height: 30px; text-align: center;"><mark class="green">{self.action_lineEdit.text()}</mark></td>
            </tr>
            <tr style="height: 35px;">
            <td style="width: 26.4204%; height: 30px; text-align: center;">
            <h4><strong>Τεχνικός</strong></h4>
            </td>
            <td style="width: 73.5796%; height: 30px; text-align: center;"> {self.technician_lineEdit.text()}</td>
            </tr>
            <tr style="height: 210px;">
            <td style="width: 26.4204%; height: 300px; text-align: center;">
            <h4><strong>Σημειώσεις</strong></h4>
            </td>
            <td style="width: 73.5796%; height: 300px; text-align: left; vertical-align:top;"> {notes}</td>
            </tr>
            <tr style="height: 18px;">
            <td style="width: 26.4204%; height: 150px; text-align: center;">
            <p><span style="color: #ff0000;"><strong>Ανταλλακτικά</strong></span></p>
            </td>
            <td style="width: 73.5796%; height: 150px; vertical-align:top;">{html_spare_parts}</td>
            </tr>
            <tr style="height: 18px;">
            <td style="width: 26.4204%; height: 25px; text-align: center;">
            <p><span style="color: #ff0000;"><strong>Ενημερώθηκε</strong></span></p>
            </td>
            <td style="width: 73.5796%; height: 25px;">&nbsp;</td>
            </tr>
            <tr style="height: 18px;">
            <td style="width: 26.4204%; height: 25px; text-align: center;">
            <p><span style="color: #ff0000;"><strong>Ολοκληρώθηκε</strong></span></p>
            </td>
            <td style="width: 73.5796%; height: 25px;">&nbsp;</td>
            </tr>
            <tr style="height: 18px;">
            <td style="width: 26.4204%; height: 25px; text-align: center;">
            <p><span style="color: #ff0000;"><strong>Παραδόθηκε</strong></span></p>
            </td>
            <td style="width: 73.5796%; height: 25px;">&nbsp;</td>
            </tr>
            <tr style="height: 18px;">
            <td style="width: 26.4204%; height: 25px; text-align: center;">
            <p><span style="color: #ff0000;"><strong>Ημρ. παραδόσης</strong></span></p>
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
        # self.printed = 1

    def closeEvent(self, event):
        self.window_closed.emit()
        event.accept()
        # event.ignore()  # if you want the window to never be closed

    def show_add_spare_part_from_store_window(self):
        self.add_spare_part_from_store_window = QtWidgets.QWidget()
        self.add_spare_part_from_store = Ui_Add_Spare_Part_From_Store()
        self.add_spare_part_from_store.selected_service = self.selected_service
        # Αρχικοποιηση των κουμπιων, γραμμων επεξεργασίας κτλπ
        self.add_spare_part_from_store.setupUi(self.add_spare_part_from_store_window)
        self.add_spare_part_from_store.window = self.add_spare_part_from_store_window  # Αν θέλουμε να ανοιγουν πολλα παράθυρα
        self.add_spare_part_from_store_window.show()
        self.add_spare_part_from_store.window_closed.connect(lambda: (self.show_spare_parts(), self.add_spare_part_from_store_window.close()))

    def show_add_spare_part_not_from_store_window(self):
        self.add_spare_part_not_from_store_window = QtWidgets.QWidget()
        # self.show_add_new_customer_window.setWindowTitle("Προσθήκη νέου πελάτη")
        # self.show_add_new_customer_window.setWindowTitle("Προσθήκη νέου πελάτη")
        self.add_spare_part_not_from_store = Ui_Add_Spare_Part_Not_From_Store()
        self.add_spare_part_not_from_store.selected_service_id = self.selected_service.ID
        self.add_spare_part_not_from_store.selected_machine = self.selected_service.machine
        self.add_spare_part_not_from_store.selected_customer_id = self.selected_service.machine.Πελάτη_ID
        # Αρχικοποιηση των κουμπιων, γραμμων επεξεργασίας κτλπ
        self.add_spare_part_not_from_store.setupUi(self.add_spare_part_not_from_store_window)

        self.add_spare_part_not_from_store.window = self.add_spare_part_not_from_store_window  # Αν θέλουμε να ανοιγουν πολλα παράθυρα
        self.add_spare_part_not_from_store_window.show()
        self.add_spare_part_not_from_store.window_closed.connect(lambda: (self.show_spare_parts(), self.add_spare_part_not_from_store_window.close()))

    def view_files(self):
        self.view_files_window = QtWidgets.QWidget()
        # self.show_add_new_customer_window.setWindowTitle("Προσθήκη νέου πελάτη")
        self.view_files = Ui_View_Files_Window()
        self.view_files.images_path = self.images_path
        self.view_files.files = self.files
        self.view_files.setupUi(self.view_files_window)
        self.view_files.show_file()
        self.view_files.window = self.view_files_window  # Αν θέλουμε να ανοιγουν πολλα παράθυρα
        self.view_files_window.show()
        self.view_files.window_closed.connect(lambda: (self.update_files(), self.view_files_window.close()))

    def delete_spare_part(self):
        selected_consumable = self.spare_parts_treeWidget.selectedItems()

        if len(selected_consumable) < 1: # ΑΝ δεν επιλέξει κανένα και πατηση διαγραφή
            return
        else:
            selected_consumable_id = selected_consumable[0].text(0)
            selected_consumable_code = selected_consumable[0].text(1)
            spare_part_obj_from_store = get_spare_part_from_code_from_all_db(selected_consumable_code)
            consumable_obj = get_consumable_from_id(selected_consumable_id)
            # Αφαίρεση ανταλλακτικού απο την εργασία
            answer = QtWidgets.QMessageBox.warning(None, "Προσοχή!", f"Σίγουρα θέλετε να διαγράψετε τον κωδικό "
                                                                     f"{selected_consumable_code};",
                                                   QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                   QtWidgets.QMessageBox.No)
            if answer == QtWidgets.QMessageBox.Yes:  # Προσθήκη πίσω στην αποθήκη
                answer2 = QtWidgets.QMessageBox.warning(None, "Προσοχή!", f"Να προστεθεί το τεμάχιο πίσω στην αποθήκη;",
                                                       QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                       QtWidgets.QMessageBox.No)
                # Ενημέρωση αποθήκης
                if answer2 == QtWidgets.QMessageBox.Yes:
                    self.update_store(consumable_obj, spare_part_obj_from_store, selected_consumable_code)
                    self.delete_consumable_from_task(consumable_obj, selected_consumable_code)
                else:
                    self.delete_consumable_from_task(consumable_obj, selected_consumable_code)

    def update_store(self, consumable_obj, spare_part_obj_from_store, selected_consumable_code):
        """
        Ενημερώνει την αποθήκη αν επιλέγουμε να βάλει το προιον πισω στην αποθήκη οταν διαγραφουμε προιόν
        απο την κληση-task-εργασία

        :param consumable_obj:
        :param spare_part_obj_from_store:
        :param selected_consumable_code:
        :return:
        """
        if spare_part_obj_from_store is None:  # Αν δεν το βρή στην βάση
            QtWidgets.QMessageBox.critical(None, "Προσοχή!", f"Ο κωδικός {selected_consumable_code}"
                                                             f" δεν βρέθηκε στην βάση!")
            return
        try:  # Ελεγχος για τα τεμάχια
            old_pieces = int(spare_part_obj_from_store.ΤΕΜΑΧΙΑ)
            new_pieces = old_pieces + int(consumable_obj.ΤΕΜΑΧΙΑ) # Να προσθέση όσα είχαμε βάλει στον πελάτη
            spare_part_obj_from_store.ΤΕΜΑΧΙΑ = new_pieces
            store_session.commit()
        except ValueError:  # Οταν τα τεμάχια δεν είναι αριθμός
            new_pieces = spare_part_obj_from_store.ΤΕΜΑΧΙΑ
            spare_part_obj_from_store.ΤΕΜΑΧΙΑ = new_pieces
            store_session.commit()
        except Exception:
            store_session.rollback()
            traceback.print_exc()
            QtWidgets.QMessageBox.critical(None, "Προσοχή!", f"Κάτι δεν πήγε καλά ο κωδικός {selected_consumable_code}"
                                                             f" δεν προστέθηκε στην βάση")
            return

    def delete_consumable_from_task(self, consumable_obj, selected_consumable_code):
        try:
            service_session.delete(consumable_obj)
            service_session.commit()
            self.show_spare_parts()
            return
        except Exception:
            service_session.rollback()
            traceback.print_exc()
            QtWidgets.QMessageBox.critical(None, "Προσοχή!",
                                           f"Κάτι δεν πήγε καλά!\n"
                                           f"Ο κωδικός {selected_consumable_code} δεν διαγράφτηκε!")
            self.show_spare_parts()
            return

    def save_service(self):
        try:
            self.selected_service.Ημερομηνία = self.dateEdit.date().toString('dd/MM/yyyy')
            self.selected_service.Σκοπός_Επίσκεψης = self.reason_lineEdit.text()
            self.selected_service.Ενέργειες = self.action_lineEdit.text()
            self.selected_service.Τεχνικός = self.technician_lineEdit.text()
            self.selected_service.Σημειώσεις = self.notes_textEdit.toPlainText()
            self.selected_service.ΔΤΕ = self.dte_lineEdit.text()
            self.selected_service.Μετρητής = self.counter_lineEdit.text()
            self.selected_service.Επ_Service = self.next_service_lineEdit.text()
            self.selected_service.Price = self.cost_lineEdit.text()
            service_session.commit()
            QtWidgets.QMessageBox.information(None, "Πληροφορία", f"Η κλήση Αποθηκεύτηκε!")
            self.safe_to_close = True
            self.close()
        except Exception:
            service_session.rollback()
            traceback.print_exc()
            QtWidgets.QMessageBox.critical(None, "Προσοχή!", f"Κάτι δεν πήγε καλά!\n" f"Τίποτα ΔΕΝ αποθηκεύτηκε!")
            return


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")
    Add_Service_Window = QtWidgets.QWidget()
    ui = Ui_Add_Service_Window()
    ui.setupUi(Add_Service_Window)
    Add_Service_Window.show()
    sys.exit(app.exec_())
