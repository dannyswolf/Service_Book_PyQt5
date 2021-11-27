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
                fetch_service_reasons, fetch_service_technicians, fetch_service_actions, get_calendar_data_from_id,
                get_consumables_from_service_id, get_spare_part_from_code_from_all_db, get_consumable_from_id,
                store_session, get_service_from_id, check_if_technician_service_data_exist)

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


class Ui_Edit_Task_Window(QtWidgets.QWidget):
    window_closed = QtCore.pyqtSignal()  # Το Signal πρεπει να είναι εκτός __init__ δεν δουλευει αλλιως

    def __init__(self):
        super(Ui_Edit_Task_Window, self).__init__()
        self.selected_calendar_id = None
        self.selected_calendar = None
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

    def setupUi(self, Edit_Task_Window):
        self.screen = Edit_Task_Window.screen()
        self.size = self.screen.size()
        # print('Size: %d x %d' % (self.size.width(), self.size.height()))
        Edit_Task_Window.setObjectName("Edit_Task_Window")
        Edit_Task_Window.setWindowModality(QtCore.Qt.WindowModal)
        Edit_Task_Window.resize(800, self.size.height() - 200)
        Edit_Task_Window.setMaximumSize(QtCore.QSize(16777213, 16777215))
        Edit_Task_Window.setWindowTitle(f"Επεξεργασία εργασίας {VERSION}")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icons/add_scheduled_tasks.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Edit_Task_Window.setWindowIcon(icon)
        Edit_Task_Window.setWindowFilePath("")
        self.gridLayout_3 = QtWidgets.QGridLayout(Edit_Task_Window)
        self.gridLayout_3.setObjectName("gridLayout_3")

        # Top Label
        self.top_label = QtWidgets.QLabel(Edit_Task_Window)
        # sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        # sizePolicy.setHorizontalStretch(0)
        # sizePolicy.setVerticalStretch(0)
        # sizePolicy.setHeightForWidth(self.top_label.sizePolicy().hasHeightForWidth())
        # self.top_label.setSizePolicy(sizePolicy)
        self.top_label.setMinimumSize(QtCore.QSize(0, 30))
        self.top_label.setFont(self.font_14_bold)
        self.top_label.setStyleSheet("background-color: rgb(0, 85, 127);\n"
                                     "color: rgb(255, 255, 255);")
        self.top_label.setAlignment(QtCore.Qt.AlignCenter)
        self.top_label.setObjectName("top_label")
        self.gridLayout_3.addWidget(self.top_label, 0, 0, 1, 4)

        # Tabs Καρτέλες
        self.tabWidget = QtWidgets.QTabWidget(Edit_Task_Window)
        # sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        # sizePolicy.setHorizontalStretch(0)
        # sizePolicy.setVerticalStretch(0)
        # sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        # self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setFont(self.font_13_bold)
        self.tabWidget.setTabPosition(QtWidgets.QTabWidget.North)
        self.tabWidget.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.tabWidget.setIconSize(QtCore.QSize(25, 25))
        self.tabWidget.setMovable(True)
        self.tabWidget.setObjectName("tabWidget")

        # Εργασεία καρτέλα tab
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

        # customer label
        self.customer_label = QtWidgets.QLabel(self.work_tab)
        self.customer_label.setMinimumSize(QtCore.QSize(0, 25))
        self.customer_label.setFont(self.font_12_bold)
        self.customer_label.setStyleSheet("background-color: rgb(93, 93, 93);\n"
                                          "color: rgb(255, 255, 255);")
        self.customer_label.setAlignment(QtCore.Qt.AlignCenter)
        self.customer_label.setObjectName("customer_label")
        self.gridLayout_2.addWidget(self.customer_label, 0, 1, 1, 4)
        # customer edit
        self.customer_lineEdit = QtWidgets.QLineEdit(self.work_tab)
        self.customer_lineEdit.setMinimumSize(QtCore.QSize(300, 35))
        self.customer_lineEdit.setFont(self.font_13)
        self.customer_lineEdit.setObjectName("customer_lineEdit")
        self.gridLayout_2.addWidget(self.customer_lineEdit, 1, 1, 1, 4)

        # time label
        self.time_label = QtWidgets.QLabel(self.work_tab)
        self.time_label.setMinimumSize(QtCore.QSize(0, 25))
        self.time_label.setFont(self.font_12_bold)
        self.time_label.setStyleSheet("background-color: rgb(93, 93, 93);\n"
                                      "color: rgb(255, 255, 255);")
        self.time_label.setAlignment(QtCore.Qt.AlignCenter)
        self.time_label.setObjectName("time_label")
        self.gridLayout_2.addWidget(self.time_label, 3, 0, 1, 1)
        # time edit
        self.timeEdit = QtWidgets.QTimeEdit(self.work_tab)
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
        self.gridLayout_2.addWidget(self.timeEdit, 4, 0, 1, 1)

        # responsible label
        self.responsible_label = QtWidgets.QLabel(self.work_tab)
        self.responsible_label.setMinimumSize(QtCore.QSize(0, 25))
        self.responsible_label.setFont(self.font_12_bold)
        self.responsible_label.setStyleSheet("background-color: rgb(93, 93, 93);\n"
                                             "color: rgb(255, 255, 255);")
        self.responsible_label.setAlignment(QtCore.Qt.AlignCenter)
        self.responsible_label.setObjectName("responsible_label")
        self.gridLayout_2.addWidget(self.responsible_label, 3, 1, 1, 1)
        # responsible edit
        self.responsible_lineEdit = QtWidgets.QLineEdit(self.work_tab)
        self.responsible_lineEdit.setMinimumSize(QtCore.QSize(0, 35))
        self.responsible_lineEdit.setFont(self.font_13)
        self.responsible_lineEdit.setObjectName("responsible_lineEdit")
        self.responsible_lineEdit.setReadOnly(True)
        self.gridLayout_2.addWidget(self.responsible_lineEdit, 4, 1, 1, 1)

        # phones label
        self.phones_label = QtWidgets.QLabel(self.work_tab)
        self.phones_label.setMinimumSize(QtCore.QSize(0, 25))
        self.phones_label.setFont(self.font_12_bold)
        self.phones_label.setStyleSheet("background-color: rgb(93, 93, 93);\n"
                                        "color: rgb(255, 255, 255);")
        self.phones_label.setAlignment(QtCore.Qt.AlignCenter)
        self.phones_label.setObjectName("phones_label")
        self.gridLayout_2.addWidget(self.phones_label, 3, 2, 1, 3)
        # Phones Edit
        self.phones_lineEdit = QtWidgets.QLineEdit(self.work_tab)
        self.phones_lineEdit.setMinimumSize(QtCore.QSize(0, 35))
        self.phones_lineEdit.setFont(self.font_13)
        self.phones_lineEdit.setObjectName("phones_lineEdit")
        self.gridLayout_2.addWidget(self.phones_lineEdit, 4, 2, 1, 3)

        # address label
        self.address_label = QtWidgets.QLabel(self.work_tab)
        self.address_label.setMinimumSize(QtCore.QSize(0, 25))
        self.address_label.setFont(self.font_12_bold)
        self.address_label.setStyleSheet("background-color: rgb(93, 93, 93);\n"
                                         "color: rgb(255, 255, 255);")
        self.address_label.setAlignment(QtCore.Qt.AlignCenter)
        self.address_label.setObjectName("address_label")
        self.gridLayout_2.addWidget(self.address_label, 5, 0, 1, 1)
        # address edit
        self.address_lineEdit = QtWidgets.QLineEdit(self.work_tab)
        self.address_lineEdit.setMinimumSize(QtCore.QSize(0, 35))
        self.address_lineEdit.setFont(self.font_13)
        self.address_lineEdit.setObjectName("address_lineEdit")
        self.address_lineEdit.setReadOnly(True)
        self.gridLayout_2.addWidget(self.address_lineEdit, 6, 0, 1, 1)

        # machine label
        self.machine_label = QtWidgets.QLabel(self.work_tab)
        self.machine_label.setMinimumSize(QtCore.QSize(0, 25))
        self.machine_label.setFont(self.font_12_bold)
        self.machine_label.setStyleSheet("background-color: rgb(93, 93, 93);\n"
                                         "color: rgb(255, 255, 255);")
        self.machine_label.setAlignment(QtCore.Qt.AlignCenter)
        self.machine_label.setObjectName("machine_label")
        self.gridLayout_2.addWidget(self.machine_label, 5, 1, 1, 4)
        # Μηχάνημα Edit
        self.machine_lineEdit = QtWidgets.QLineEdit(self.work_tab)
        self.machine_lineEdit.setMinimumSize(QtCore.QSize(0, 35))
        self.machine_lineEdit.setFont(self.font_13)
        self.machine_lineEdit.setObjectName("machine_lineEdit")
        self.machine_lineEdit.setReadOnly(True)
        self.gridLayout_2.addWidget(self.machine_lineEdit, 6, 1, 1, 4)



        # counter label
        self.counter_label = QtWidgets.QLabel(self.work_tab)
        self.counter_label.setMinimumSize(QtCore.QSize(0, 25))
        self.counter_label.setFont(self.font_12_bold)
        self.counter_label.setStyleSheet("background-color: rgb(93, 93, 93);\n"
                                         "color: rgb(255, 255, 255);")
        self.counter_label.setAlignment(QtCore.Qt.AlignCenter)
        self.counter_label.setObjectName("counter_label")
        self.gridLayout_2.addWidget(self.counter_label, 7, 0, 1, 1)
        # counter edit
        self.counter_lineEdit = QtWidgets.QLineEdit(self.work_tab)
        self.counter_lineEdit.setMinimumSize(QtCore.QSize(0, 35))
        self.counter_lineEdit.setFont(self.font_13)
        self.counter_lineEdit.setText("")
        self.counter_lineEdit.setObjectName("counter_lineEdit")
        self.gridLayout_2.addWidget(self.counter_lineEdit, 8, 0, 1, 1)

        # next service label
        self.next_service_label = QtWidgets.QLabel(self.work_tab)
        self.next_service_label.setMinimumSize(QtCore.QSize(220, 25))
        self.next_service_label.setFont(self.font_12_bold)
        self.next_service_label.setStyleSheet("background-color: rgb(93, 93, 93);\n"
                                              "color: rgb(255, 255, 255);")
        self.next_service_label.setAlignment(QtCore.Qt.AlignCenter)
        self.next_service_label.setObjectName("next_service_label")
        self.gridLayout_2.addWidget(self.next_service_label, 7, 1, 1, 1)
        # next service edit
        self.next_service_lineEdit = QtWidgets.QLineEdit(self.work_tab)
        self.next_service_lineEdit.setMinimumSize(QtCore.QSize(0, 35))
        self.next_service_lineEdit.setFont(self.font_13)
        self.next_service_lineEdit.setText("")
        self.next_service_lineEdit.setObjectName("next_service_lineEdit")
        self.gridLayout_2.addWidget(self.next_service_lineEdit, 8, 1, 1, 1)

        # technician label
        self.technician_label = QtWidgets.QLabel(self.work_tab)
        self.technician_label.setMinimumSize(QtCore.QSize(150, 25))
        self.technician_label.setFont(self.font_12_bold)
        self.technician_label.setStyleSheet("background-color: rgb(93, 93, 93);\n"
                                            "color: rgb(255, 255, 255);")
        self.technician_label.setAlignment(QtCore.Qt.AlignCenter)
        self.technician_label.setObjectName("technician_label")
        self.gridLayout_2.addWidget(self.technician_label, 9, 0, 1, 3)
        # Τεχνικός edit
        self.technician_lineEdit = QtWidgets.QLineEdit(self.work_tab)
        self.technician_lineEdit.setMinimumSize(QtCore.QSize(0, 35))
        self.technician_lineEdit.setFont(self.font_13)
        self.technician_lineEdit.setObjectName("technician_lineEdit")
        self.technician_combobox = QtWidgets.QComboBox(self.work_tab)
        self.technician_combobox.setMinimumSize(QtCore.QSize(0, 35))
        self.technician_combobox.setFont(self.font_13)
        self.technician_combobox.setLineEdit(self.technician_lineEdit)
        self.gridLayout_2.addWidget(self.technician_combobox, 10, 0, 1, 2)

        # cost label
        self.cost_label = QtWidgets.QLabel(self.work_tab)
        self.cost_label.setMinimumSize(QtCore.QSize(0, 25))
        self.cost_label.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.cost_label.setFont(self.font_12_bold)
        self.cost_label.setStyleSheet("background-color: rgb(93, 93, 93);\n"
                                      "color: rgb(255, 255, 255);")
        self.cost_label.setAlignment(QtCore.Qt.AlignCenter)
        self.cost_label.setObjectName("cost_label")
        self.gridLayout_2.addWidget(self.cost_label, 9, 4, 1, 1)
        # cost edit
        self.cost_lineEdit = QtWidgets.QLineEdit(self.work_tab)
        self.cost_lineEdit.setMinimumSize(QtCore.QSize(0, 35))
        self.cost_lineEdit.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.cost_lineEdit.setFont(self.font_13)
        self.cost_lineEdit.setObjectName("cost_lineEdit")
        self.gridLayout_2.addWidget(self.cost_lineEdit, 10, 4, 1, 1)

        # reason label
        self.reason_label = QtWidgets.QLabel(self.work_tab)
        self.reason_label.setMinimumSize(QtCore.QSize(0, 25))
        self.reason_label.setFont(self.font_12_bold)
        self.reason_label.setStyleSheet("background-color: rgb(255, 170, 0);\n"
                                        "color: rgb(255, 255, 255);")
        self.reason_label.setAlignment(QtCore.Qt.AlignCenter)
        self.reason_label.setObjectName("reason_label")
        self.gridLayout_2.addWidget(self.reason_label, 11, 0, 1, 3)
        # reason edit
        self.reason_lineEdit = QtWidgets.QLineEdit(self.work_tab)
        self.reason_lineEdit.setMinimumSize(QtCore.QSize(500, 35))
        self.reason_lineEdit.setFont(self.font_13)
        self.reason_lineEdit.setObjectName("reason_lineEdit")
        self.gridLayout_2.addWidget(self.reason_lineEdit, 12, 0, 1, 3)

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
        self.gridLayout_2.addWidget(self.dte_label, 11, 4, 1, 1)
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
        self.gridLayout_2.addWidget(self.dte_lineEdit, 12, 4, 1, 1)

        # Ενέργειες label
        self.action_label = QtWidgets.QLabel(self.work_tab)
        self.action_label.setMinimumSize(QtCore.QSize(0, 25))
        self.action_label.setFont(self.font_12_bold)
        self.action_label.setStyleSheet("background-color: rgb(0, 85, 127);\n"
                                        "color: rgb(255, 255, 255);")
        self.action_label.setAlignment(QtCore.Qt.AlignCenter)
        self.action_label.setObjectName("action_label")
        self.gridLayout_2.addWidget(self.action_label, 13, 0, 1, 3)
        # action edit
        self.action_lineEdit = QtWidgets.QLineEdit(self.work_tab)
        self.action_lineEdit.setMinimumSize(QtCore.QSize(600, 35))
        self.action_lineEdit.setFont(self.font_13)
        self.action_lineEdit.setObjectName("action_lineEdit")
        self.gridLayout_2.addWidget(self.action_lineEdit, 14, 0, 1, 3)

        # finished Label
        self.finished_label = QtWidgets.QLabel(self.work_tab)
        self.finished_label.setMinimumSize(QtCore.QSize(0, 25))
        self.finished_label.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.finished_label.setFont(self.font_12_bold)
        self.finished_label.setStyleSheet("background-color: rgb(0, 170, 0);\n"
                                          "color: rgb(255, 255, 255);")
        self.finished_label.setAlignment(QtCore.Qt.AlignCenter)
        self.finished_label.setObjectName("finished_label")
        self.gridLayout_2.addWidget(self.finished_label, 13, 4, 1, 1)
        # check box
        self.checkBox = QtWidgets.QCheckBox(self.work_tab)
        self.checkBox.setMouseTracking(False)
        self.done_icon = QtGui.QIcon()
        self.done_icon.addPixmap(QtGui.QPixmap("icons/done_samll.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.not_done_icon = QtGui.QIcon()
        self.not_done_icon.addPixmap(QtGui.QPixmap("icons/not_done_samll.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.checkBox.setIcon(self.not_done_icon)
        self.checkBox.setIconSize(QtCore.QSize(30, 30))
        self.checkBox.setObjectName("checkBox")
        self.checkBox.stateChanged.connect(self.change_color_of_check_box)
        self.gridLayout_2.addWidget(self.checkBox, 14, 4, 1, 1, QtCore.Qt.AlignRight)

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
        self.gridLayout_2.addWidget(self.notes_label, 15, 0, 1, 5)
        # notes edit
        self.notes_textEdit = QtWidgets.QTextEdit(self.work_tab)
        self.notes_textEdit.setFont(self.font_13)
        self.notes_textEdit.setObjectName("notes_textEdit")
        self.gridLayout_2.addWidget(self.notes_textEdit, 16, 0, 1, 5)

        # Save btn
        self.save_toolButton = QtWidgets.QToolButton(Edit_Task_Window)
        self.save_toolButton.setFont(self.font_12_bold)
        self.save_toolButton.setStyleSheet("background-color: rgb(103, 103, 103);\n"
                                           "color: rgb(255, 255, 255);")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("icons/Save.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.save_toolButton.setIcon(icon3)
        self.save_toolButton.setIconSize(QtCore.QSize(30, 30))
        self.save_toolButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.save_toolButton.setObjectName("save_toolButton")
        self.save_toolButton.clicked.connect(self.save_task)
        self.gridLayout_3.addWidget(self.save_toolButton, 2, 3, 1, 1)

        # Email btn
        self.email_toolButton = QtWidgets.QToolButton(Edit_Task_Window)
        self.email_toolButton.setFont(self.font_12_bold)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("icons/send_mail.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.email_toolButton.setIcon(icon4)
        self.email_toolButton.setIconSize(QtCore.QSize(30, 30))
        self.email_toolButton.setObjectName("email_toolButton")
        self.email_toolButton.clicked.connect(self.send_mail)
        self.gridLayout_3.addWidget(self.email_toolButton, 2, 0, 1, 1)

        # Print btn
        self.print_toolButton = QtWidgets.QToolButton(Edit_Task_Window)
        self.print_toolButton.setFont(self.font_12_bold)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("icons/print_it.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.print_toolButton.setIcon(icon2)
        self.print_toolButton.setIconSize(QtCore.QSize(30, 30))
        self.print_toolButton.setObjectName("print_toolButton")
        self.print_toolButton.clicked.connect(self.print_to_pdf)
        self.gridLayout_3.addWidget(self.print_toolButton, 2, 2, 1, 1)

        # add action btn
        self.add_action_toolButton = QtWidgets.QToolButton(self.work_tab)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("icons/add_to_service_data2.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.add_action_toolButton.setIcon(icon5)
        self.add_action_toolButton.setIconSize(QtCore.QSize(30, 30))
        self.add_action_toolButton.setObjectName("add_action_toolButton")
        self.add_action_toolButton.clicked.connect(self.add_action_to_db)
        self.gridLayout_2.addWidget(self.add_action_toolButton, 14, 3, 1, 1)

        # Προσθήκη τεχνικού
        self.add_technician_toolButton = QtWidgets.QToolButton(self.work_tab)
        self.add_technician_toolButton.setFont(self.font_13_bold)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("icons/add_service.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.add_technician_toolButton.setIcon(icon1)
        self.add_technician_toolButton.setIconSize(QtCore.QSize(30, 30))
        self.add_technician_toolButton.setObjectName("add_technician_toolButton")
        self.add_technician_toolButton.clicked.connect(self.add_technician_to_db)
        self.gridLayout_2.addWidget(self.add_technician_toolButton, 10, 3, 1, 1)

        # add reason brn
        self.add_reason_toolButton = QtWidgets.QToolButton(self.work_tab)
        self.add_reason_toolButton.setIcon(icon5)
        self.add_reason_toolButton.setIconSize(QtCore.QSize(30, 30))
        self.add_reason_toolButton.setObjectName("add_reason_toolButton")
        self.add_reason_toolButton.clicked.connect(self.add_reason_to_db)
        self.gridLayout_2.addWidget(self.add_reason_toolButton, 12, 3, 1, 1)

        # Spare part tab
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap("icons/service.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tabWidget.addTab(self.work_tab, icon7, "")
        self.spare_parts_tab = QtWidgets.QWidget()
        self.spare_parts_tab.setObjectName("spare_parts_tab")
        self.gridLayout = QtWidgets.QGridLayout(self.spare_parts_tab)
        self.gridLayout.setObjectName("gridLayout")

        # Delete Task
        self.delete_task_toolButton = QtWidgets.QToolButton(self.spare_parts_tab)
        # sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        # sizePolicy.setHorizontalStretch(0)
        # sizePolicy.setVerticalStretch(0)
        # sizePolicy.setHeightForWidth(self.delete_task_toolButton.sizePolicy().hasHeightForWidth())
        # self.delete_task_toolButton.setSizePolicy(sizePolicy)
        self.delete_task_toolButton.setFont(self.font_12_bold)
        self.delete_task_toolButton.setStyleSheet("background-color: rgb(170, 0, 0);\n"
                                                  "color: rgb(255, 255, 255);")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("icons/delete_task.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.delete_task_toolButton.setIcon(icon1)
        self.delete_task_toolButton.setIconSize(QtCore.QSize(30, 30))
        self.delete_task_toolButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.delete_task_toolButton.setObjectName("delete_task_toolButton")
        self.delete_task_toolButton.clicked.connect(self.delete_task)
        self.gridLayout.addWidget(self.delete_task_toolButton, 0, 2, 1, 1)

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
        self.gridLayout.addWidget(self.spare_parts_label, 0, 0, 1, 2)
        icon13 = QtGui.QIcon()
        icon13.addPixmap(QtGui.QPixmap("icons/gears.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tabWidget.addTab(self.spare_parts_tab, icon13, "")
        self.gridLayout_3.addWidget(self.tabWidget, 1, 0, 1, 4)

        # Esc
        self.shortcut_esc = QtWidgets.QShortcut(QtGui.QKeySequence('Escape'), Edit_Task_Window)
        self.shortcut_esc.activated.connect(self.close)

        self.retranslateUi(Edit_Task_Window)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Edit_Task_Window)
        self.fetch_service_data()
        self.get_calendar_data()

    def retranslateUi(self, Edit_Task_Window):
        _translate = QtCore.QCoreApplication.translate
        self.delete_task_toolButton.setText(_translate("Edit_Task_Window", "   Διαγραφή\n   εργασίας"))
        self.top_label.setText(_translate("Edit_Task_Window", "Επεξεργασία εργασίας"))
        self.save_toolButton.setText(_translate("Edit_Task_Window", "Αποθήκευση"))
        self.email_toolButton.setText(_translate("Edit_Task_Window", "..."))
        self.action_label.setText(_translate("Edit_Task_Window", "Ενέργειες"))
        self.finished_label.setText(_translate("Edit_Task_Window", "Ολοκληρώθηκε"))
        self.notes_label.setText(_translate("Edit_Task_Window", "Σημειώσεις"))
        self.date_label.setText(_translate("Edit_Task_Window", "Ημερομηνία"))
        self.address_label.setText(_translate("Edit_Task_Window", "Διεύθυνση"))
        self.reason_label.setText(_translate("Edit_Task_Window", "Σκοπός εργασίας"))
        self.add_action_toolButton.setText(_translate("Edit_Task_Window", "..."))
        self.next_service_label.setText(_translate("Edit_Task_Window", "Επ. Service"))
        self.time_label.setText(_translate("Edit_Task_Window", "Ωρα"))
        self.customer_label.setText(_translate("Edit_Task_Window", "Πελάτης"))
        self.cost_label.setText(_translate("Edit_Task_Window", "Κόστος"))
        self.add_reason_toolButton.setText(_translate("Edit_Task_Window", "..."))
        self.phones_label.setText(_translate("Edit_Task_Window", "Τηλέφωνο - Κινητό"))
        self.machine_label.setText(_translate("Edit_Task_Window", "Μηχάνημα"))
        self.responsible_label.setText(_translate("Edit_Task_Window", "Υπεύθυνος"))
        self.technician_label.setText(_translate("Edit_Task_Window", "Τεχνικός"))
        self.counter_label.setText(_translate("Edit_Task_Window", "Μετρητής"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.work_tab), _translate("Edit_Task_Window", "Εργασία"))
        self.add_spare_part_from_store_toolButton.setText(_translate("Edit_Task_Window", "  Προσθήκη ανταλλ. \n"
                                                                                         "  εντός αποθήκης"))
        self.add_files_toolButton.setText(_translate("Edit_Task_Window", "  Προσθήκη αρχείων"))
        self.delete_spare_part_toolButton.setText(_translate("Edit_Task_Window", "    Διαγραφή ανταλλ."))
        self.view_files_toolButton.setText(_translate("Edit_Task_Window", "   Προβολή αρχείων"))
        self.spare_parts_treeWidget.setSortingEnabled(True)
        self.add_spare_part_toolButton.setText(_translate("Edit_Task_Window", "Προσθήκη ανταλλ. \n"
                                                                              " εκτός αποθήκης"))
        self.spare_parts_label.setText(_translate("Edit_Task_Window", "Ανταλλακτικά"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.spare_parts_tab),
                                  _translate("Edit_Task_Window", "Ανταλλακτικά"))

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
        self.reason_lineEdit.setCompleter(self.reason_completer)

        self.action_completer = QtWidgets.QCompleter(self.service_actions)
        self.action_lineEdit.setCompleter(self.action_completer)

    def get_calendar_data(self):
        if self.selected_calendar_id is not None:
            self.selected_calendar = get_calendar_data_from_id(self.selected_calendar_id)
            self.selected_service = get_service_from_id(self.selected_calendar.Service_ID)

            self.dateEdit.setDate(QtCore.QDate.fromString(self.selected_calendar.Ημερομηνία, "dd'/'MM'/'yyyy"))
            self.customer_lineEdit.setText(self.selected_calendar.Πελάτης)
            self.customer_lineEdit.setReadOnly(True)
            if self.selected_calendar.Επείγων == "":
                self.timeEdit.setTime(QtCore.QTime.currentTime())
            else:
                if QtCore.QTime.isValid(QtCore.QTime.fromString(self.selected_calendar.Επείγων, "HH:mm")):

                    self.timeEdit.setTime(QtCore.QTime.fromString(self.selected_calendar.Επείγων, "HH:mm"))
                else:
                    self.timeEdit.setTime(QtCore.QTime.currentTime())

            self.responsible_lineEdit.setText(self.selected_calendar.machine.Customer.Ονοματεπώνυμο)
            self.phones_lineEdit.setText(self.selected_calendar.Τηλέφωνο)
            self.address_lineEdit.setText(self.selected_calendar.machine.Customer.Διεύθυνση)
            self.machine_lineEdit.setText(self.selected_calendar.machine.Εταιρεία + f"  Serial: {self.selected_calendar.machine.Serial}")
            self.technician_lineEdit.setText(self.selected_calendar.Τεχνικός)
            self.counter_lineEdit.setText(self.selected_calendar.Μετρητής)
            self.next_service_lineEdit.setText(self.selected_calendar.Επ_Service)
            self.cost_lineEdit.setText(self.selected_calendar.Price)
            self.reason_lineEdit.setText(self.selected_calendar.Σκοπός)
            self.dte_lineEdit.setText(self.selected_calendar.ΔΤΕ)
            self.action_lineEdit.setText(self.selected_calendar.Ενέργειες)
            self.notes_textEdit.setText(self.selected_calendar.Σημειώσεις)
            old_text =  self.notes_textEdit.toPlainText()
            append_text = f"-------------------------------- {user} {today.replace(' ', '/')} --------------------------------\n"
            len_append_text = len(append_text)
            if old_text[-len_append_text:] != append_text:
                self.notes_textEdit.append(append_text)
            if len(old_text) <= 1:  # Αν είναι κενό να το βάλει γιατί το self.notes_textEdit.append(append_text) αφηνει κενα
                self.notes_textEdit.setText(append_text)  # Ισα με 1 γιατι βάζει το \n

            if self.selected_calendar.Κατάσταση:
                self.checkBox.setChecked(False)
                self.checkBox.setIcon(self.not_done_icon)
                self.finished_label.setStyleSheet("background-color: red;\n"
                                                  "color: white;")
            else:
                self.checkBox.setChecked(True)
                self.checkBox.setIcon(self.done_icon)
                self.finished_label.setStyleSheet("background-color: rgb(0, 170, 0);\n"
                                                  "color: rgb(255, 255, 255);")
            # Spare Parts
            self.show_spare_parts()
            # Show images
            self.update_files()

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
        self.selected_calendar_spare_parts = get_consumables_from_service_id(self.selected_calendar.Service_ID)
        self.spare_parts_treeWidget.clear()
        for index, item in enumerate(self.selected_calendar_spare_parts):
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
            date = datetime.strptime(self.selected_calendar.Ημερομηνία, "%d/%m/%Y")
            year = date.year
        except ValueError:  # Οταν δεν έχουμε βάλει Ημερομηνία στη κλήση
            year = datetime.year
        self.images_path = os.path.join(SPARE_PARTS_ROOT, f"{year}", f"{self.selected_calendar.Service_ID}")
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
        if self.checkBox.isChecked():
            status = "Ολοκληρώθηκε"
        else:
            status = "Δεν έχει ολοκληρωθεί"
        data = [self.dateEdit.date().toString("dd/MM/yyyy"),
                self.reason_lineEdit.text(),
                self.technician_lineEdit.text(),
                self.action_lineEdit.text(),
                self.counter_lineEdit.text(),
                self.timeEdit.time().toString('HH:mm'),
                self.phones_lineEdit.text(),
                self.notes_textEdit.toHtml(),
                self.dte_lineEdit.text(),
                status]

        self.show_send_email_window = QtWidgets.QWidget()
        # self.show_add_new_customer_window.setWindowTitle("Προσθήκη νέου πελάτη")
        self.show_send_email = Ui_Send_Email_Window()
        self.show_send_email.selected_calendar = self.selected_calendar
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
        outputFilename = f"{prints_dir}/Service_Book_" + f"{self.customer_lineEdit.text()}".replace(" ", "_") + \
                         f"_{self.selected_calendar.Service_ID}" + ".pdf"
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
        for index, spare_part in enumerate(self.selected_calendar_spare_parts):
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
                <td style="width: 26.4204%; height: 30px; text-align: center; vertical-align:bottom;">
                    Ημερομηνία
                </td>
                <td style="width: 73.5796%; height: 30px; text-align: center; vertical-align:bottom;"> 
                    {self.dateEdit.date().toString("dd/MM/yyyy")}
                </td>
            </tr>
            
            <tr style="height: 18px;">
                <td style="width: 26.4204%; height: 30px; text-align: center; vertical-align:bottom;">
                    Πελάτης
                </td>
                <td style="width: 73.5796%; height: 30px; text-align: center; vertical-align:bottom;"> 
                    {self.customer_lineEdit.text()}
                </td>
            </tr>
            
            <tr style="height: 18px;">
            <td style="width: 26.4204%; height: 30px; text-align: center; vertical-align:bottom;">
            Υπεύθυνος
            </td>
            <td style="width: 73.5796%; height: 30px; text-align: center; vertical-align:bottom;"> {self.responsible_lineEdit.text()}</td>
            </tr>
            <tr style="height: 18px;">
            <td style="width: 26.4204%; height: 30px; text-align: center; vertical-align:bottom;">
            Διεύθυνση
            </td>
            <td style="width: 73.5796%; height: 30px; text-align: center; vertical-align:bottom;"> {self.address_lineEdit.text()}</td>
            </tr>
            <tr style="height: 18px;">
            <td style="width: 26.4204%; height: 30px; text-align: center; vertical-align:bottom;">
            Τηλέφωνα
            </td>
            <td style="width: 73.5796%; height: 30px; text-align: center; vertical-align:bottom;"> {self.phones_lineEdit.text()}</td>
            </tr>
            <tr style="height: 18px;">
            <td style="width: 26.4204%; height: 30px; text-align: center; vertical-align:bottom;">
            Μηχάνημα
            </td>
            <td style="width: 73.5796%; height: 30px; text-align: center; vertical-align:bottom;"> {self.machine_lineEdit.text()}</td>
            </tr>
            
            
            <tr style="height: 18px;">
            <td style="width: 26.4204%; height: 30px; text-align: center; vertical-align:bottom;">
            Μετρητής
            </td>
            <td style="width: 73.5796%; height: 30px; text-align: center; vertical-align:bottom;"> <mark class="red">{self.counter_lineEdit.text()}</mark></td>
            </tr>
            <tr style="height: 18px;">
            <td style="width: 26.4204%; height: 30px; text-align: center; vertical-align:bottom;">
            Περιγραφή προβλήματος
            </td>
            <td style="width: 73.5796%; height: 30px; text-align: center; vertical-align:bottom;"> {self.reason_lineEdit.text()}</td>
            </tr>
            
            <tr style="height: 18px;">
            <td style="width: 26.4204%; height: 30px; text-align: center; vertical-align:bottom;">
            Ενέργειες
            </td>
            <td style="width: 73.5796%; height: 30px; text-align: center; vertical-align:bottom;"><mark class="green">{self.action_lineEdit.text()}</mark></td>
            </tr>
            <tr style="height: 35px;">
            <td style="width: 26.4204%; height: 30px; text-align: center; vertical-align:bottom;">
            Τεχνικός
            </td>
            <td style="width: 73.5796%; height: 30px; text-align: center; vertical-align:bottom;"> {self.technician_lineEdit.text()}</td>
            </tr>
            <tr style="height: 18px;">
            <td style="width: 26.4204%; height: 30px; text-align: center; vertical-align:bottom;">
            Ωρα
            </td>
            <td style="width: 73.5796%; height: 30px; text-align: center; vertical-align:bottom;"> {self.timeEdit.time().toString('HH:mm')}</td>
            </tr>
            <tr style="height: 210px;">
            <td style="width: 26.4204%; height: 300px; text-align: center;">
            Σημειώσεις
            </td>
            <td style="width: 73.5796%; height: 300px; text-align: left; vertical-align:top;"> {notes}</td>
            </tr>
            <tr style="height: 18px;">
            <td style="width: 26.4204%; height: 150px; text-align: center;">
            <p><span style="color: #ff0000;">Ανταλλακτικά</span></p>
            </td>
            <td style="width: 73.5796%; height: 150px; vertical-align:top;">{html_spare_parts}</td>
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
            <p><span style="color: #ff0000;">Ημρ. παραδόσης</span></p>
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
        self.add_spare_part_from_store.selected_calendar = self.selected_calendar
        # Αρχικοποιηση των κουμπιων, γραμμων επεξεργασίας κτλπ
        self.add_spare_part_from_store.setupUi(self.add_spare_part_from_store_window)
        self.add_spare_part_from_store.window = self.add_spare_part_from_store_window  # Αν θέλουμε να ανοιγουν πολλα παράθυρα
        self.add_spare_part_from_store_window.show()
        self.add_spare_part_from_store.window_closed.connect(lambda: (self.show_spare_parts(), self.add_spare_part_from_store_window.close()))

    def show_add_spare_part_not_from_store_window(self):
        self.add_spare_part_not_from_store_window = QtWidgets.QWidget()
        # self.show_add_new_customer_window.setWindowTitle("Προσθήκη νέου πελάτη")
        self.add_spare_part_not_from_store = Ui_Add_Spare_Part_Not_From_Store()
        self.add_spare_part_not_from_store.selected_calendar_id = self.selected_calendar.ID
        self.add_spare_part_not_from_store.selected_service_id = self.selected_calendar.Service_ID
        self.add_spare_part_not_from_store.selected_machine = self.selected_calendar.machine
        self.add_spare_part_not_from_store.selected_customer_id = self.selected_calendar.Customer_ID
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

    def delete_task(self):
        if self.selected_calendar_spare_parts:
            QtWidgets.QMessageBox.critical(None, "Προσοχή!", f"Παρακαλώ αφαιρέστε πρώτα τα προιόντα!")
            return
        elif self.files:
            QtWidgets.QMessageBox.critical(None, "Προσοχή!", f"Παρακαλώ αφαιρέστε πρώτα τα αρχεία!")
            return
        else:

                answer = QtWidgets.QMessageBox.warning(None, "Προσοχή!", f"Σίγουρα θέλετε να διαγράψετε την εργασία;",
                                                        QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                        QtWidgets.QMessageBox.No)
                if answer == QtWidgets.QMessageBox.Yes:
                    try:
                        service_session.delete(self.selected_calendar)
                        service_session.delete(self.selected_service)
                        service_session.commit()
                        QtWidgets.QMessageBox.information(None, "Προσοχή!", f"H εργασία διαγράφτηκε!")
                        self.close()
                    except Exception:
                        service_session.rollback()
                        traceback.print_exc()
                        QtWidgets.QMessageBox.critical(None, "Προσοχή!",
                                                       f"Κάτι δεν πήγε καλά η εργασία δεν διαγράφτηκε!")
                        return
                else:
                    return

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

    def save_task(self):
        try:
            self.selected_calendar.Ημερομηνία = self.dateEdit.date().toString('dd/MM/yyyy')
            self.selected_calendar.Σκοπός = self.reason_lineEdit.text()
            self.selected_calendar.Ενέργειες = self.action_lineEdit.text()
            self.selected_calendar.Τεχνικός = self.technician_lineEdit.text()
            self.selected_calendar.Ημ_Ολοκλ = today.replace(" ", "/")
            self.selected_calendar.Επείγων = self.timeEdit.time().toString("HH:mm")
            self.selected_calendar.Τηλέφωνο = self.phones_lineEdit.text()
            self.selected_calendar.Σημειώσεις = self.notes_textEdit.toPlainText()
            self.selected_calendar.ΔΤΕ = self.dte_lineEdit.text()
            self.selected_calendar.Μετρητής = self.counter_lineEdit.text()
            self.selected_calendar.Επ_Service = self.next_service_lineEdit.text()
            self.selected_calendar.Price = self.cost_lineEdit.text()
            if self.checkBox.isChecked():
                self.selected_calendar.Κατάσταση = 0
            else:
                self.selected_calendar.Κατάσταση = 1

            self.selected_service.Ημερομηνία = today.replace(" ", "/")
            self.selected_service.Σκοπός_Επίσκεψης = self.reason_lineEdit.text()
            self.selected_service.Ενέργειες = self.action_lineEdit.text()
            self.selected_service.Τεχνικός = self.technician_lineEdit.text()
            self.selected_service.Σημειώσεις = self.notes_textEdit.toPlainText()
            self.selected_service.Μετρητής = self.counter_lineEdit.text()
            self.selected_service.Επ_Service = self.next_service_lineEdit.text()
            self.selected_service.ΔΤΕ = self.dte_lineEdit.text()
            self.selected_service.Price = self.cost_lineEdit.text()

            service_session.commit()
            QtWidgets.QMessageBox.information(None, "Πληροφορία", f"Η κλήση Αποθυκεύτηκε!")
            self.close()
        except Exception:
            service_session.rollback()
            traceback.print_exc()
            QtWidgets.QMessageBox.critical(None, "Προσοχή!", f"Κάτι δεν πήγε καλά!\n" f"Η κλήση ΔΕΝ αποθυκεύτηκε!")
            return

    def change_color_of_check_box(self):
        if self.checkBox.isChecked():
            self.checkBox.setChecked(True)
            self.checkBox.setIcon(self.done_icon)
            self.finished_label.setStyleSheet("background-color: rgb(0, 170, 0);\n"
                                              "color: rgb(255, 255, 255);")
        else:
            self.checkBox.setChecked(False)
            self.checkBox.setIcon(self.not_done_icon)
            self.finished_label.setStyleSheet("background-color: red;\n"
                                              "color: white;")




if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")
    Edit_Task_Window = QtWidgets.QWidget()
    ui = Ui_Edit_Task_Window()
    ui.setupUi(Edit_Task_Window)
    Edit_Task_Window.show()
    sys.exit(app.exec_())
