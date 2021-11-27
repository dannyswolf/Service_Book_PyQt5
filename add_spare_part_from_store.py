# -*- coding: utf-8 -*-
# Created by: PyQt5 UI code generator 5.15.4
import traceback
import re
# Database
from db import Brother, Canon, Epson, Konica, Kyocera, Lexmark, Oki, Ricoh, Samsung, Sharp, Melanakia, Melanotainies, \
    Toner, Copiers, service_session, store_session, Consumables, get_spare_parts, search_on_spare_parts, \
    search_on_consumables, \
    get_consumables_from_service_id, get_selected_spare_part_from_code

from PyQt5 import QtCore, QtGui, QtWidgets


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


class Ui_Add_Spare_Part_From_Store(QtWidgets.QWidget):
    window_closed = QtCore.pyqtSignal()  # Το Signal πρεπει να είναι εκτός __init__ δεν δουλευει αλλιως

    def __init__(self, *args, **kwargs):
        super(Ui_Add_Spare_Part_From_Store, self).__init__(*args, **kwargs)
        self.selected_table = None
        self.data_to_show = None
        self.selected_calendar = None
        self.selected_service = None

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

    def setupUi(self, Add_Spare_Part_From_Store):
        Add_Spare_Part_From_Store.setObjectName("MainWindow")
        Add_Spare_Part_From_Store.resize(1024, 650)
        Add_Spare_Part_From_Store.setMinimumSize(QtCore.QSize(0, 30))
        Add_Spare_Part_From_Store.setWindowTitle("Αποθήκη")
        # self.centralwidget = QtWidgets.QWidget(Add_Spare_Part_From_Store)
        # self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(Add_Spare_Part_From_Store)
        self.gridLayout.setObjectName("gridLayout")
        self.ricoh_btn = QtWidgets.QToolButton(Add_Spare_Part_From_Store)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ricoh_btn.sizePolicy().hasHeightForWidth())
        self.ricoh_btn.setSizePolicy(sizePolicy)
        self.ricoh_btn.setMinimumSize(QtCore.QSize(0, 50))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icons/RICOH.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ricoh_btn.setIcon(icon)
        self.ricoh_btn.setIconSize(QtCore.QSize(80, 50))
        self.ricoh_btn.setObjectName("ricoh_btn")
        self.ricoh_btn.clicked.connect(lambda: self.show_spare_parts(Ricoh))
        self.gridLayout.addWidget(self.ricoh_btn, 0, 8, 1, 1)

        self.search_btn = QtWidgets.QToolButton(Add_Spare_Part_From_Store)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.search_btn.sizePolicy().hasHeightForWidth())
        self.search_btn.setSizePolicy(sizePolicy)
        self.search_btn.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.search_btn.setFont(font)
        self.search_btn.setToolTip("Κουμπή αναζήτησης")
        self.search_btn.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.search_btn.setAutoFillBackground(False)
        self.search_btn.setText("Αναζήτηση")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("icons/search.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.search_btn.setIcon(icon1)
        self.search_btn.setIconSize(QtCore.QSize(30, 30))
        self.search_btn.setShortcut("")
        self.search_btn.setAutoRepeatDelay(300)
        self.search_btn.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.search_btn.setObjectName("search_btn")
        self.search_btn.clicked.connect(self.search)
        self.gridLayout.addWidget(self.search_btn, 3, 5, 1, 2)

        self.epson_btn = QtWidgets.QToolButton(Add_Spare_Part_From_Store)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.epson_btn.sizePolicy().hasHeightForWidth())
        self.epson_btn.setSizePolicy(sizePolicy)
        self.epson_btn.setMinimumSize(QtCore.QSize(0, 50))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("icons/EPSON.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.epson_btn.setIcon(icon2)
        self.epson_btn.setIconSize(QtCore.QSize(80, 50))
        self.epson_btn.setObjectName("epson_btn")
        self.epson_btn.clicked.connect(lambda: self.show_spare_parts(Epson))
        self.gridLayout.addWidget(self.epson_btn, 0, 2, 1, 1)

        self.canon_btn = QtWidgets.QToolButton(Add_Spare_Part_From_Store)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.canon_btn.sizePolicy().hasHeightForWidth())
        self.canon_btn.setSizePolicy(sizePolicy)
        self.canon_btn.setMinimumSize(QtCore.QSize(0, 50))
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("icons/CANON.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.canon_btn.setIcon(icon3)
        self.canon_btn.setIconSize(QtCore.QSize(80, 50))
        self.canon_btn.setAutoRaise(False)
        self.canon_btn.setObjectName("canon_btn")
        self.canon_btn.clicked.connect(lambda: self.show_spare_parts(Canon))
        self.gridLayout.addWidget(self.canon_btn, 0, 1, 1, 1)

        self.lexmark_btn = QtWidgets.QToolButton(Add_Spare_Part_From_Store)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lexmark_btn.sizePolicy().hasHeightForWidth())
        self.lexmark_btn.setSizePolicy(sizePolicy)
        self.lexmark_btn.setMinimumSize(QtCore.QSize(0, 50))
        self.lexmark_btn.setStyleSheet("")
        self.lexmark_btn.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("icons/LEXMARK.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.lexmark_btn.setIcon(icon4)
        self.lexmark_btn.setIconSize(QtCore.QSize(80, 50))
        self.lexmark_btn.setObjectName("lexmark_btn")
        self.lexmark_btn.clicked.connect(lambda: self.show_spare_parts(Lexmark))
        self.gridLayout.addWidget(self.lexmark_btn, 0, 6, 1, 1)

        self.oki_btn = QtWidgets.QToolButton(Add_Spare_Part_From_Store)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.oki_btn.sizePolicy().hasHeightForWidth())
        self.oki_btn.setSizePolicy(sizePolicy)
        self.oki_btn.setMinimumSize(QtCore.QSize(0, 50))
        self.oki_btn.setText("")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("icons/OKI.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.oki_btn.setIcon(icon5)
        self.oki_btn.setIconSize(QtCore.QSize(80, 50))
        self.oki_btn.setObjectName("oki_btn")
        self.oki_btn.clicked.connect(lambda: self.show_spare_parts(Oki))
        self.gridLayout.addWidget(self.oki_btn, 0, 7, 1, 1)

        self.konica_btn = QtWidgets.QToolButton(Add_Spare_Part_From_Store)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.konica_btn.sizePolicy().hasHeightForWidth())
        self.konica_btn.setSizePolicy(sizePolicy)
        self.konica_btn.setMinimumSize(QtCore.QSize(0, 50))
        self.konica_btn.setStyleSheet("")
        self.konica_btn.setText("")
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap("icons/KONICA.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.konica_btn.setIcon(icon6)
        self.konica_btn.setIconSize(QtCore.QSize(80, 50))
        self.konica_btn.setObjectName("konica_btn")
        self.konica_btn.clicked.connect(lambda: self.show_spare_parts(Konica))
        self.gridLayout.addWidget(self.konica_btn, 0, 3, 1, 2)

        self.kyocera_btn = QtWidgets.QToolButton(Add_Spare_Part_From_Store)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.kyocera_btn.sizePolicy().hasHeightForWidth())
        self.kyocera_btn.setSizePolicy(sizePolicy)
        self.kyocera_btn.setMinimumSize(QtCore.QSize(0, 50))
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap("icons/KYOCERA.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.kyocera_btn.setIcon(icon7)
        self.kyocera_btn.setIconSize(QtCore.QSize(80, 50))
        self.kyocera_btn.setObjectName("kyocera_btn")
        self.kyocera_btn.clicked.connect(lambda: self.show_spare_parts(Kyocera))
        self.gridLayout.addWidget(self.kyocera_btn, 0, 5, 1, 1)

        self.brother_btn = QtWidgets.QToolButton(Add_Spare_Part_From_Store)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.brother_btn.sizePolicy().hasHeightForWidth())
        self.brother_btn.setSizePolicy(sizePolicy)
        self.brother_btn.setMinimumSize(QtCore.QSize(0, 50))
        self.brother_btn.setToolTip("Brother Ανταλλακτικά")
        self.brother_btn.setWhatsThis("Brother Ανταλλακτικά")
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap("icons/BROTHER.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.brother_btn.setIcon(icon8)
        self.brother_btn.setIconSize(QtCore.QSize(80, 50))
        self.brother_btn.setAutoRepeatInterval(97)
        self.brother_btn.setObjectName("brother_btn")
        self.brother_btn.clicked.connect(lambda: self.show_spare_parts(Brother))
        self.gridLayout.addWidget(self.brother_btn, 0, 0, 1, 1)

        self.search_line_edit = QtWidgets.QLineEdit(Add_Spare_Part_From_Store)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.search_line_edit.sizePolicy().hasHeightForWidth())
        self.search_line_edit.setSizePolicy(sizePolicy)
        self.search_line_edit.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(13)
        self.search_line_edit.setFont(font)
        self.search_line_edit.setObjectName("search_line_edit")
        self.search_line_edit.returnPressed.connect(self.search)
        self.gridLayout.addWidget(self.search_line_edit, 3, 0, 1, 5)

        self.melanotainies_btn = QtWidgets.QToolButton(Add_Spare_Part_From_Store)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.melanotainies_btn.sizePolicy().hasHeightForWidth())
        self.melanotainies_btn.setSizePolicy(sizePolicy)
        self.melanotainies_btn.setMinimumSize(QtCore.QSize(0, 50))
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap("icons/ΜΕΛΑΝΟΤΑΙΝΙΕΣ.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.melanotainies_btn.setIcon(icon9)
        self.melanotainies_btn.setIconSize(QtCore.QSize(80, 50))
        self.melanotainies_btn.setObjectName("melanotainies_btn")
        self.melanotainies_btn.clicked.connect(lambda: self.show_melanotainies(Melanotainies))
        self.gridLayout.addWidget(self.melanotainies_btn, 1, 6, 1, 1)

        self.toner_btn = QtWidgets.QToolButton(Add_Spare_Part_From_Store)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toner_btn.sizePolicy().hasHeightForWidth())
        self.toner_btn.setSizePolicy(sizePolicy)
        self.toner_btn.setMinimumSize(QtCore.QSize(0, 50))
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap("icons/ΤΟΝΕΡ.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toner_btn.setIcon(icon10)
        self.toner_btn.setIconSize(QtCore.QSize(80, 50))
        self.toner_btn.setObjectName("toner_btn")
        self.toner_btn.clicked.connect(lambda: self.show_consumables(Toner))
        self.gridLayout.addWidget(self.toner_btn, 1, 7, 1, 1)

        self.melanakia_btn = QtWidgets.QToolButton(Add_Spare_Part_From_Store)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.melanakia_btn.sizePolicy().hasHeightForWidth())
        self.melanakia_btn.setSizePolicy(sizePolicy)
        self.melanakia_btn.setMinimumSize(QtCore.QSize(0, 50))
        icon11 = QtGui.QIcon()
        icon11.addPixmap(QtGui.QPixmap("icons/ΜΕΛΑΝΑΚΙΑ.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.melanakia_btn.setIcon(icon11)
        self.melanakia_btn.setIconSize(QtCore.QSize(80, 50))
        self.melanakia_btn.setObjectName("melanakia_btn")
        self.melanakia_btn.clicked.connect(lambda: self.show_consumables(Melanakia))
        self.gridLayout.addWidget(self.melanakia_btn, 1, 5, 1, 1)

        self.copiers_btn = QtWidgets.QToolButton(Add_Spare_Part_From_Store)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.copiers_btn.sizePolicy().hasHeightForWidth())
        self.copiers_btn.setSizePolicy(sizePolicy)
        self.copiers_btn.setMinimumSize(QtCore.QSize(0, 50))
        icon12 = QtGui.QIcon()
        icon12.addPixmap(QtGui.QPixmap("icons/ΦΩΤΟΤΥΠΙΚΑ.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.copiers_btn.setIcon(icon12)
        self.copiers_btn.setIconSize(QtCore.QSize(80, 50))
        self.copiers_btn.setObjectName("copiers_btn")
        self.copiers_btn.clicked.connect(lambda: self.show_consumables(Copiers))
        self.gridLayout.addWidget(self.copiers_btn, 1, 8, 1, 1)

        self.samsung_btn = QtWidgets.QToolButton(Add_Spare_Part_From_Store)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.samsung_btn.sizePolicy().hasHeightForWidth())
        self.samsung_btn.setSizePolicy(sizePolicy)
        self.samsung_btn.setMinimumSize(QtCore.QSize(0, 50))
        icon13 = QtGui.QIcon()
        icon13.addPixmap(QtGui.QPixmap("icons/SAMSUNG.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.samsung_btn.setIcon(icon13)
        self.samsung_btn.setIconSize(QtCore.QSize(80, 50))
        self.samsung_btn.setObjectName("samsung_btn")
        self.samsung_btn.clicked.connect(lambda: self.show_spare_parts(Samsung))
        self.gridLayout.addWidget(self.samsung_btn, 0, 9, 1, 1)

        self.sharp_btn = QtWidgets.QToolButton(Add_Spare_Part_From_Store)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sharp_btn.sizePolicy().hasHeightForWidth())
        self.sharp_btn.setSizePolicy(sizePolicy)
        self.sharp_btn.setMinimumSize(QtCore.QSize(0, 50))
        icon14 = QtGui.QIcon()
        icon14.addPixmap(QtGui.QPixmap("icons/SHARP.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.sharp_btn.setIcon(icon14)
        self.sharp_btn.setIconSize(QtCore.QSize(80, 50))
        self.sharp_btn.setObjectName("sharp_btn")
        self.sharp_btn.clicked.connect(lambda: self.show_spare_parts(Sharp))
        self.gridLayout.addWidget(self.sharp_btn, 0, 10, 1, 1)

        # self.treeView = QtWidgets.QTreeWidget(self.centralwidget)
        # font = QtGui.QFont()
        # font.setFamily("Calibri")
        # font.setPointSize(13)
        # self.treeView.setFont(font)
        # self.treeView.setObjectName("treeView")
        # self.gridLayout.addWidget(self.treeView, 4, 0, 1, 12)

        self.add_btn = QtWidgets.QToolButton(Add_Spare_Part_From_Store)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.add_btn.sizePolicy().hasHeightForWidth())
        self.add_btn.setSizePolicy(sizePolicy)
        self.add_btn.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.add_btn.setFont(font)
        self.add_btn.setToolTip("Προσθήκη ανταλλακτικού")
        self.add_btn.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.add_btn.setAutoFillBackground(False)
        self.add_btn.setStyleSheet("background-color: rgb(0, 170, 0);\n"
                                   "color: rgb(255, 255, 255);")
        self.add_btn.setText("    Προσθήκη")
        icon15 = QtGui.QIcon()
        icon15.addPixmap(QtGui.QPixmap("icons/add_spare_parts.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.add_btn.setIcon(icon15)
        self.add_btn.setIconSize(QtCore.QSize(25, 25))
        self.add_btn.setShortcut("")
        self.add_btn.setAutoRepeatDelay(300)
        self.add_btn.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.add_btn.setObjectName("add_btn")
        self.add_btn.clicked.connect(self.add_spare_part)
        self.gridLayout.addWidget(self.add_btn, 3, 9, 1, 2)
        # Esc
        self.shortcut_esc = QtWidgets.QShortcut(QtGui.QKeySequence('Escape'), Add_Spare_Part_From_Store)
        self.shortcut_esc.activated.connect(self.close)
        # Quit
        self.finish = QtWidgets.QAction("Quit", self)
        self.finish.triggered.connect(self.closeEvent)

        self.grouping_btn()

        # Add_Spare_Part_From_Store.setCentralWidget(self.centralwidget)
        # QtCore.QMetaObject.connectSlotsByName(Add_Spare_Part_From_Store)

    def show_spare_parts(self, table):
        self.selected_table = table
        self.btn_grp.buttonClicked.connect(self.change_colors_of_pressed_btn)  # αλλαγή χρώματος
        self.data_to_show = get_spare_parts(table)
        # treeWidget

        self.treeWidget = QtWidgets.QTreeWidget(self)
        self.treeWidget.setObjectName("treeWidget")
        self.treeWidget.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.treeWidget.setFrameShadow(QtWidgets.QFrame.Plain)

        self.treeWidget.setSortingEnabled(True)
        self.treeWidget.setWordWrap(True)
        self.treeWidget.setAutoFillBackground(True)
        self.treeWidget.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        # self.treeWidget.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.treeWidget.setLineWidth(14)
        self.treeWidget.setFont(self.font_13)
        self.treeWidget.setAlternatingRowColors(True)
        self.treeWidget.setHeaderLabels(["ID", "Part No", "Περιγραφή", "Κωδικός", "Τεμάχια", "Παρατηρήσεις"])
        # self.treeWidget.setAnimated(True)
        self.treeWidget.header().setStyleSheet(u"background-color: gray;" "color: white;"
                                               "font-style: normal;font-size: 14pt;font-weight: bold;")
        for index, item in enumerate(self.data_to_show):
            self.qitem = TreeWidgetItem(self.treeWidget,
                                        [str(item.ID), str(item.PARTS_NR), item.ΠΕΡΙΓΡΑΦΗ, str(item.ΚΩΔΙΚΟΣ),
                                         str(item.ΤΕΜΑΧΙΑ), item.ΠΑΡΑΤΗΡΗΣΗΣ])
            self.treeWidget.setStyleSheet("QTreeView::item { padding: 10px }")
            self.treeWidget.addTopLevelItem(self.qitem)

        self.treeWidget.setColumnWidth(2, 500)
        self.gridLayout.addWidget(self.treeWidget, 4, 0, 1, 12)

    def show_melanotainies(self, table):
        self.selected_table = table
        self.btn_grp.buttonClicked.connect(self.change_colors_of_pressed_btn)  # αλλαγή χρώματος
        self.data_to_show = get_spare_parts(table)

        # treeWidget
        self.treeWidget = QtWidgets.QTreeWidget(self)
        self.treeWidget.setObjectName("treeWidget")
        self.treeWidget.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.treeWidget.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.treeWidget.setLineWidth(2)
        self.treeWidget.setFont(self.font_13)
        self.treeWidget.setSortingEnabled(True)
        self.treeWidget.setWordWrap(True)

        self.treeWidget.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        # self.treeWidget.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.treeWidget.setAlternatingRowColors(True)
        self.treeWidget.setHeaderLabels(
            ["ID", "Εταιρεία", "Ποιότητα", "Αναλώσιμο", "Περιγραφή", "Κωδικός", "Τεμάχια",
             "Τιμή", "Σύνολο", "Πελάτες", "Παρατηρήσεις"])
        self.treeWidget.header().setStyleSheet(u"background-color: gray;" "color: white;"
                                               "font-style: normal;font-size: 14pt;font-weight: bold;")
        for index, item in enumerate(self.data_to_show):
            self.qitem = TreeWidgetItem(self.treeWidget,
                                        [str(item.ID), str(item.ΕΤΑΙΡΕΙΑ), item.ΠΟΙΟΤΗΤΑ, str(item.ΑΝΑΛΩΣΙΜΟ),
                                         str(item.ΠΕΡΙΓΡΑΦΗ), item.ΚΩΔΙΚΟΣ, item.ΤΕΜΑΧΙΑ, item.ΤΙΜΗ, item.ΣΥΝΟΛΟ,
                                         item.ΠΕΛΑΤΕΣ, item.ΠΑΡΑΤΗΡΗΣΗΣ])

            self.treeWidget.setStyleSheet("QTreeView::item { padding: 10px }")
            self.treeWidget.addTopLevelItem(self.qitem)
        self.treeWidget.setColumnWidth(4, 500)
        # self.treeWidget.resizeColumnToContents(index)
        self.gridLayout.addWidget(self.treeWidget, 4, 0, 1, 12)

    def show_consumables(self, table):
        self.selected_table = table
        self.btn_grp.buttonClicked.connect(self.change_colors_of_pressed_btn)  # αλλαγή χρώματος
        self.data_to_show = get_spare_parts(table)
        # treeWidget
        self.treeWidget = QtWidgets.QTreeWidget(self)
        self.treeWidget.setObjectName("treeWidget")
        self.treeWidget.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.treeWidget.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.treeWidget.setLineWidth(2)
        self.treeWidget.setSortingEnabled(True)
        self.treeWidget.setWordWrap(True)
        self.treeWidget.setFont(self.font_13)
        self.treeWidget.setAutoFillBackground(True)
        self.treeWidget.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        # self.treeWidget.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.treeWidget.setAlternatingRowColors(True)
        self.treeWidget.setHeaderLabels(
            ["ID", "Εταιρεία", "Ποιότητα", "Αναλώσιμο", "Περιγραφή", "Κωδικός", "Τεμάχια",
             "Τιμή", "Σύνολο", "Σελίδες", "Πελάτες", "Παρατηρήσεις"])
        self.treeWidget.setAnimated(True)
        self.treeWidget.header().setStyleSheet(u"background-color: gray;" "color: white;"
                                               "font-style: normal;font-size: 14pt;font-weight: bold;")
        for index, item in enumerate(self.data_to_show):
            self.qitem = TreeWidgetItem(self.treeWidget,
                                        [str(item.ID), item.ΕΤΑΙΡΕΙΑ, item.ΠΟΙΟΤΗΤΑ, item.ΑΝΑΛΩΣΙΜΟ,
                                         item.ΠΕΡΙΓΡΑΦΗ, item.ΚΩΔΙΚΟΣ, item.ΤΕΜΑΧΙΑ, item.ΤΙΜΗ, item.ΣΥΝΟΛΟ,
                                         item.ΣΕΛΙΔΕΣ, item.ΠΕΛΑΤΕΣ, item.ΠΑΡΑΤΗΡΗΣΗΣ])

            if "C/M/Y" in item.ΠΕΡΙΓΡΑΦΗ:
                self.qitem.setBackground(4, QtGui.QColor('green'))
                self.qitem.setForeground(4, QtGui.QColor('white'))
            elif "CYAN" in item.ΠΕΡΙΓΡΑΦΗ:
                self.qitem.setBackground(4, QtGui.QColor('#0517D2'))
                self.qitem.setForeground(4, QtGui.QColor('white'))
            elif "MAGENTA" in item.ΠΕΡΙΓΡΑΦΗ:
                self.qitem.setBackground(4, QtGui.QColor('#D205CF'))
                self.qitem.setForeground(4, QtGui.QColor('white'))
            elif "YELLOW" in item.ΠΕΡΙΓΡΑΦΗ:
                self.qitem.setBackground(4, QtGui.QColor('yellow'))
                self.qitem.setForeground(4, QtGui.QColor('black'))
            elif "GRAY" in item.ΠΕΡΙΓΡΑΦΗ:
                self.qitem.setBackground(4, QtGui.QColor("gray"))
                self.qitem.setForeground(4, QtGui.QColor('white'))
            elif "BLACK" in item.ΠΕΡΙΓΡΑΦΗ:
                self.qitem.setBackground(4, QtGui.QColor("black"))
                self.qitem.setForeground(4, QtGui.QColor('white'))
            self.treeWidget.setStyleSheet("QTreeView::item { padding: 10px }")
            self.treeWidget.addTopLevelItem(self.qitem)
        self.treeWidget.setColumnWidth(4, 500)
        # self.treeWidget.resizeColumnToContents(index)
        self.gridLayout.addWidget(self.treeWidget, 4, 0, 1, 12)

    def search(self):
        text_to_search = self.search_line_edit.text()
        if text_to_search == "" or text_to_search == " ":
            return
        self.search_line_edit.clear()
        self.treeWidget.clear()
        if self.selected_table.__tablename__ == "ΜΕΛΑΝΑΚΙΑ" or self.selected_table.__tablename__ == "ΤΟΝΕΡ" \
                or self.selected_table.__tablename__ == "ΦΩΤΟΤΥΠΙΚΑ" or self.selected_table.__tablename__ == "ΜΕΛΑΝΟΤΑΙΝΙΕΣ":
            self.data_to_show = search_on_consumables(self.selected_table, text_to_search)
        else:
            self.data_to_show = search_on_spare_parts(self.selected_table, text_to_search)
        for index, item in enumerate(self.data_to_show):
            if self.selected_table.__tablename__ == "ΜΕΛΑΝΑΚΙΑ" or self.selected_table.__tablename__ == "ΤΟΝΕΡ" \
                    or self.selected_table.__tablename__ == "ΦΩΤΟΤΥΠΙΚΑ":
                self.qitem = QtWidgets.QTreeWidgetItem(self.treeWidget,
                                                       [str(item.ID), str(item.ΕΤΑΙΡΕΙΑ), item.ΠΟΙΟΤΗΤΑ,
                                                        str(item.ΑΝΑΛΩΣΙΜΟ),
                                                        str(item.ΠΕΡΙΓΡΑΦΗ), item.ΚΩΔΙΚΟΣ, item.ΤΕΜΑΧΙΑ, item.ΤΙΜΗ,
                                                        item.ΣΥΝΟΛΟ,
                                                        item.ΣΕΛΙΔΕΣ, item.ΠΕΛΑΤΕΣ, item.ΠΑΡΑΤΗΡΗΣΗΣ])
                if "C/M/Y" in item.ΠΕΡΙΓΡΑΦΗ:
                    self.qitem.setBackground(4, QtGui.QColor('green'))
                    self.qitem.setForeground(4, QtGui.QColor('white'))
                elif "CYAN" in item.ΠΕΡΙΓΡΑΦΗ:
                    self.qitem.setBackground(4, QtGui.QColor('#0517D2'))
                    self.qitem.setForeground(4, QtGui.QColor('white'))
                elif "MAGENTA" in item.ΠΕΡΙΓΡΑΦΗ:
                    self.qitem.setBackground(4, QtGui.QColor('#D205CF'))
                    self.qitem.setForeground(4, QtGui.QColor('white'))
                elif "YELLOW" in item.ΠΕΡΙΓΡΑΦΗ:
                    self.qitem.setBackground(4, QtGui.QColor('yellow'))
                    self.qitem.setForeground(4, QtGui.QColor('black'))
                elif "GRAY" in item.ΠΕΡΙΓΡΑΦΗ:
                    self.qitem.setBackground(4, QtGui.QColor("gray"))
                    self.qitem.setForeground(4, QtGui.QColor('white'))
                elif "BLACK" in item.ΠΕΡΙΓΡΑΦΗ:
                    self.qitem.setBackground(4, QtGui.QColor("black"))
                    self.qitem.setForeground(4, QtGui.QColor('white'))
                self.treeWidget.addTopLevelItem(self.qitem)
                self.treeWidget.setColumnWidth(4, 500)
                self.treeWidget.resizeColumnToContents(index)
                # Για να μήν ψάχνει το ιδιο string στα επομενα πεδια του ιδου προιόντος
                # πχ αν βρει την λεξει "brother" στο πεδιο ΠΕΡΙΓΡΑΦΗ αν το αφήσουμε να ψαξει και στις
                # ΠΑΡΑΤΗΡΗΣΕΙΣ θα μας βγαλει δυο φορές το ιδιο προιόν στο treeWidget
                # για αυτο κανουμε break το εσωτρεικό loop
                # break
                # ΜΕΛΑΝΟΤΑΙΝΙΕΣ
            elif self.selected_table.__tablename__ == "ΜΕΛΑΝΟΤΑΙΝΙΕΣ":
                self.qitem = QtWidgets.QTreeWidgetItem(self.treeWidget,
                                                       [str(item.ID), str(item.ΕΤΑΙΡΕΙΑ), item.ΠΟΙΟΤΗΤΑ,
                                                        str(item.ΑΝΑΛΩΣΙΜΟ),
                                                        str(item.ΠΕΡΙΓΡΑΦΗ), item.ΚΩΔΙΚΟΣ, item.ΤΕΜΑΧΙΑ, item.ΤΙΜΗ,
                                                        item.ΣΥΝΟΛΟ,
                                                        item.ΠΕΛΑΤΕΣ, item.ΠΑΡΑΤΗΡΗΣΗΣ])
                self.treeWidget.addTopLevelItem(self.qitem)
                self.treeWidget.setColumnWidth(4, 500)
                self.treeWidget.resizeColumnToContents(index)
                # Για να μήν ψάχνει το ιδιο string στα επομενα πεδια του ιδου προιόντος
                # πχ αν βρει την λεξει "brother" στο πεδιο ΠΕΡΙΓΡΑΦΗ αν το αφήσουμε να ψαξει και στις
                # ΠΑΡΑΤΗΡΗΣΕΙΣ θα μας βγαλει δυο φορές το ιδιο προιόν στο treeWidget
                # για αυτο κανουμε break το εσωτρεικό loop
                # break
            else:
                self.qitem = QtWidgets.QTreeWidgetItem(self.treeWidget,
                                                       [str(item.ID), str(item.PARTS_NR), item.ΠΕΡΙΓΡΑΦΗ,
                                                        str(item.ΚΩΔΙΚΟΣ),
                                                        str(item.ΤΕΜΑΧΙΑ), item.ΠΑΡΑΤΗΡΗΣΗΣ])
                self.treeWidget.addTopLevelItem(self.qitem)
                self.treeWidget.setColumnWidth(2, 500)
                self.treeWidget.resizeColumnToContents(index)
                # Για να μήν ψάχνει το ιδιο string στα επομενα πεδια του ιδου προιόντος
                # πχ αν βρει την λεξει "brother" στο πεδιο ΠΕΡΙΓΡΑΦΗ αν το αφήσουμε να ψαξει και στις
                # ΠΑΡΑΤΗΡΗΣΕΙΣ θα μας βγαλει δυο φορές το ιδιο προιόν στο treeWidget
                # για αυτο κανουμε break το εσωτρεικό loop
                # break

    def add_spare_part(self):
        try:
            items = self.treeWidget.selectedItems()
            if len(items) == 0:  # Αν δεν επιλεξει τίποτα και πατήση προσθήκη
                return
            if self.selected_table.__tablename__ == "ΜΕΛΑΝΟΤΑΙΝΙΕΣ" or self.selected_table.__tablename__ == "ΤΟΝΕΡ" \
                    or self.selected_table.__tablename__ == "ΦΩΤΟΤΥΠΙΚΑ" or self.selected_table.__tablename__ == "ΜΕΛΑΝΑΚΙΑ":
                item_code = items[0].text(5)  # Πεδίο κωδικός
            else:
                item_code = items[0].text(3)  # Πεδίο κωδικός
            # Get obj from code
            spare_part_obj = get_selected_spare_part_from_code(self.selected_table, item_code)
            # check if exist και προσθήκη +1 στο τεμάχια
            if self.selected_service:
                existing_parts = get_consumables_from_service_id(self.selected_service.ID)
            else:
                existing_parts = get_consumables_from_service_id(self.selected_calendar.Service_ID)
            for existing_part in existing_parts:
                # Αν υπάρχει +1
                if item_code == existing_part.ΚΩΔΙΚΟΣ:
                    answer = QtWidgets.QMessageBox.critical(None, "Προσοχή!", f"Ο κωδικός {item_code} υπάρχει!\n"
                                                                              f"Θέλετε να το ξάνα προσθέσετε;",
                                                            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                            QtWidgets.QMessageBox.No)
                    if answer == QtWidgets.QMessageBox.Yes:
                        try:  # Ελεγχος για τα τεμάχια
                            old_pieces = int(existing_part.ΤΕΜΑΧΙΑ)
                            new_pieces = old_pieces + 1
                        except ValueError:  # Οταν τα τεμάχια δεν είναι αριθμός
                            new_pieces = existing_part.ΤΕΜΑΧΙΑ  # Το αφήνουμε οπως είναι

                        existing_part.ΤΕΜΑΧΙΑ = new_pieces
                        service_session.commit()
                        # Αφαίρεση απο αποθήκη
                        try:  # Ελεγχος για τα τεμάχια
                            old_pieces = int(spare_part_obj.ΤΕΜΑΧΙΑ)
                            new_pieces = old_pieces - 1
                        except ValueError:  # Οταν τα τεμάχια δεν είναι αριθμός
                            new_pieces = spare_part_obj.ΤΕΜΑΧΙΑ
                        try:  # Ενημέρωση πεδίου Πελάτες στο προιόν -- Προσθέτουμε τον πελάτη που βαλαμε το προιόν
                            old_customers = spare_part_obj.ΠΕΛΑΤΕΣ
                            if self.selected_calendar:  # Αν έχουμε καλέσει αυτό το παράθυρο απο το edit_task_window
                                # να προσθέση τον πελάτη στο ανταλλακτικό
                                if self.selected_calendar.Πελάτης not in old_customers:
                                    if old_customers[-1] != ",":
                                        new_customers = old_customers + "," + self.selected_calendar.Πελάτης + ","
                                    else:
                                        new_customers = old_customers + " " + self.selected_calendar.Πελάτης + ","
                                    spare_part_obj.ΠΕΛΑΤΕΣ = new_customers
                            else:  # Οταν έχουμε καλέσει αυτό το παράθυρο απο το edit_service_window
                                if self.selected_service.machine.Customer.Επωνυμία_Επιχείρησης not in old_customers:
                                    if old_customers[-1] != ",":
                                        new_customers = old_customers + "," + self.selected_service.machine.Customer.Επωνυμία_Επιχείρησης + ","
                                    else:
                                        new_customers = old_customers + " " + self.selected_service.machine.Customer.Επωνυμία_Επιχείρησης + ","
                                    spare_part_obj.ΠΕΛΑΤΕΣ = new_customers
                        except IndexError:  # Όταν δεν έχει κανένα πελάτη το προιόν
                            if self.selected_calendar:
                                spare_part_obj.ΠΕΛΑΤΕΣ = self.selected_calendar.Πελάτης
                            else:
                                spare_part_obj.ΠΕΛΑΤΕΣ = self.selected_service.machine.Customer.Επωνυμία_Επιχείρησης
                        except AttributeError:  # Οταν δεν υπάρχει πεδίο πελάτης ( στα spare parts  Konica, Sharp etc)
                            pass  # Οταν δεν υπάρχει πεδίο πελάτης ( στα spare parts Brother, Epson, Konica, Sharp etc)
                        spare_part_obj.ΤΕΜΑΧΙΑ = new_pieces
                        store_session.commit()
                        # update Treewidget
                        if self.selected_table.__tablename__ == "ΤΟΝΕΡ" or self.selected_table.__tablename__ == "ΦΩΤΟΤΥΠΙΚΑ" \
                                or self.selected_table.__tablename__ == "ΜΕΛΑΝΑΚΙΑ":
                            self.show_consumables(self.selected_table)
                        elif self.selected_table.__tablename__ == "ΜΕΛΑΝΟΤΑΙΝΙΕΣ":
                            self.show_melanotainies(self.selected_table)
                        else:
                            self.show_spare_parts(self.selected_table)
                        answer = QtWidgets.QMessageBox.question(None, "Ερώτηση!", f"Ο κωδικός {item_code} προστέθηκε!\n" 
                                                                f"Ο Θέλετε να προσθέσετε αλλο προιόν;",
                                                                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                                QtWidgets.QMessageBox.No)
                        if answer == QtWidgets.QMessageBox.Yes:
                            return
                        else:
                            self.close()
                            return
                    else:  # Αν δεν θέλουμε να το ξαναπροσθέσουμε
                        return
            # Προσθήκη αν δεν υπάρχει
            try:  # Ελεγχος  αν έχει PARTS_NR
                new_part_no = spare_part_obj.PARTS_NR
            except AttributeError:
                new_part_no = ""
            try:
                description = spare_part_obj.ΠΕΡΙΓΡΑΦΗ
            except AttributeError:  # Οταν δεν έχει κωδικό το προιόν
                QtWidgets.QMessageBox.critical(None, "Προσοχή!", "Το προιόν δεν έχει κωδικό\ν δεν μπορει να προστεθεί")
                return
            code = spare_part_obj.ΚΩΔΙΚΟΣ
            if self.selected_calendar:
                new_part = Consumables(PARTS_NR=new_part_no, ΠΕΡΙΓΡΑΦΗ=description, ΚΩΔΙΚΟΣ=code, ΤΕΜΑΧΙΑ=1,
                                       ΠΑΡΑΤΗΡΗΣΗΣ=spare_part_obj.ΠΑΡΑΤΗΡΗΣΗΣ, ΜΗΧΑΝΗΜΑ=self.selected_calendar.Μηχάνημα,
                                       Service_ID=self.selected_calendar.Service_ID,
                                       Customer_ID=self.selected_calendar.Customer_ID,
                                       Calendar_ID=self.selected_calendar.ID)
            else:
                new_part = Consumables(PARTS_NR=new_part_no, ΠΕΡΙΓΡΑΦΗ=description, ΚΩΔΙΚΟΣ=code, ΤΕΜΑΧΙΑ=1,
                                       ΠΑΡΑΤΗΡΗΣΗΣ=spare_part_obj.ΠΑΡΑΤΗΡΗΣΗΣ, ΜΗΧΑΝΗΜΑ=self.selected_service.machine.Εταιρεία,
                                       Service_ID=self.selected_service.ID,
                                       Customer_ID=self.selected_service.machine.Customer.ID,
                                       Calendar_ID="")
            service_session.add(new_part)
            service_session.commit()
            # Αφαίρεση απο αποθήκη
            try:  # Ελεγχος για τα τεμάχια
                old_pieces = int(spare_part_obj.ΤΕΜΑΧΙΑ)
                new_pieces = old_pieces - 1
            except ValueError:  # Οταν τα τεμάχια δεν είναι αριθμός
                new_pieces = spare_part_obj.ΤΕΜΑΧΙΑ
            try:  # Ενημέρωση πεδίου Πελάτες στο προιόν -- Προσθέτουμε τον πελάτη που βαλαμε το προιόν
                old_customers = spare_part_obj.ΠΕΛΑΤΕΣ
                if self.selected_calendar:
                    if self.selected_calendar.Πελάτης not in old_customers:
                        if old_customers[-1] != ",":
                            new_customers = old_customers + "," + self.selected_calendar.Πελάτης + ","
                        else:
                            new_customers = old_customers + " " + self.selected_calendar.Πελάτης + ","
                        spare_part_obj.ΠΕΛΑΤΕΣ = new_customers
                else:  # Οταν έχουμε καλέσει αυτό το παράθυρο απο το edit_service_window
                    if self.selected_service.machine.Customer.Επωνυμία_Επιχείρησης not in old_customers:
                        if old_customers[-1] != ",":
                            new_customers = old_customers + "," + self.selected_service.machine.Customer.Επωνυμία_Επιχείρησης + ","
                        else:
                            new_customers = old_customers + " " + self.selected_service.machine.Customer.Επωνυμία_Επιχείρησης + ","
                        spare_part_obj.ΠΕΛΑΤΕΣ = new_customers
            except IndexError:  # Όταν δεν έχει κανένα πελάτη
                if self.selected_calendar:
                    spare_part_obj.ΠΕΛΑΤΕΣ = self.selected_calendar.Πελάτης
                else:
                    spare_part_obj.ΠΕΛΑΤΕΣ = self.selected_service.machine.Customer.Επωνυμία_Επιχείρησης
            except AttributeError:  # Οταν δεν υπάρχει πεδίο πελάτης ( στα spare parts  Konica, Sharp etc)
                pass  # Οταν δεν υπάρχει πεδίο πελάτης ( στα spare parts Brother, Epson, Konica, Sharp etc)
            spare_part_obj.ΤΕΜΑΧΙΑ = new_pieces
            store_session.commit()
            # update Treewidget
            if self.selected_table.__tablename__ == "ΤΟΝΕΡ" or self.selected_table.__tablename__ == "ΦΩΤΟΤΥΠΙΚΑ" \
                    or self.selected_table.__tablename__ == "ΜΕΛΑΝΑΚΙΑ":
                self.show_consumables(self.selected_table)
            elif self.selected_table.__tablename__ == "ΜΕΛΑΝΟΤΑΙΝΙΕΣ":
                self.show_melanotainies(self.selected_table)
            else:
                self.show_spare_parts(self.selected_table)
            answer = QtWidgets.QMessageBox.question(None, "Ερώτηση!", f"Ο κωδικός {item_code} προστέθηκε!\n"
                                                                      f"Ο Θέλετε να προσθέσετε αλλο προιόν;",
                                                    QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                    QtWidgets.QMessageBox.No)
            if answer == QtWidgets.QMessageBox.Yes:
                return
            else:
                self.close()
                return
        except Exception:
            service_session.rollback()
            store_session.rollback()
            traceback.print_exc()
            QtWidgets.QMessageBox.critical(None, "Σφάλμα", f"Κάτι δεν πήγε καλά!\n Οι αλλαγές δεν αποθηκεύτηκαν!")
            return

    def grouping_btn(self):

        up_btn = [self.brother_btn, self.canon_btn, self.epson_btn, self.konica_btn, self.kyocera_btn,
                  self.lexmark_btn, self.oki_btn, self.ricoh_btn, self.samsung_btn, self.sharp_btn]
        down_btn = [self.melanakia_btn, self.melanotainies_btn, self.toner_btn, self.copiers_btn]
        all_btn = up_btn + down_btn
        # Grouping buttons
        self.btn_grp = QtWidgets.QButtonGroup()
        self.btn_grp.setExclusive(True)
        for btn in all_btn:
            self.btn_grp.addButton(btn)

    def change_colors_of_pressed_btn(self, pressed_btn):
        up_btn = [self.brother_btn, self.canon_btn, self.epson_btn, self.konica_btn, self.kyocera_btn,
                  self.lexmark_btn,
                  self.oki_btn, self.ricoh_btn, self.samsung_btn, self.sharp_btn]
        down_btn = [self.melanakia_btn, self.melanotainies_btn, self.toner_btn, self.copiers_btn]
        all_btn = up_btn + down_btn

        pressed_btn.setStyleSheet(
            f"background-color: #50f333;" "color: white;"
            "border-style: outset;" "border-width: 2px;" "border-radius: 15px;" "border-color: black;" "padding: 4px;")

        # self.selected_table_label.setStyleSheet(f"image: url(icons/{self.selected_table_label.text()}.png);"
        # "background-color: #aaff7f;" "color: white;" "border-style: outset;" "border-width: 2px;" \ "border-radius:
        # 15px;" "border-color: black;" "padding: 4px;") self.selected_table_label.setText("") needed
        for btn in all_btn:
            if btn in up_btn and btn != pressed_btn:

                btn.setStyleSheet(
                    f"background-color: #fff;" "color: white;"
                    "border-style: outset;" "border-width: 2px;" "border-radius: 15px;" "border-color: black;"
                    "padding: 4px;")
            elif btn in down_btn and btn != pressed_btn:
                btn.setStyleSheet(
                    f"background-color: #ffb907;" "color: white;"
                    "border-style: outset;" "border-width: 2px;" "border-radius: 15px;" "border-color: black;"
                    "padding: 4px;")

    def closeEvent(self, event):
        self.window_closed.emit()
        event.accept()
        # event.ignore()  # if you want the window to never be closed


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")
    Add_Spare_Part_From_Store_Window = QtWidgets.QWidget()
    ui = Ui_Add_Spare_Part_From_Store()
    ui.setupUi(Add_Spare_Part_From_Store_Window)
    Add_Spare_Part_From_Store_Window.show()
    sys.exit(app.exec_())
