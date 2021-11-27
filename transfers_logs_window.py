# -*- coding: utf-8 -*-
# Created by: PyQt5 UI code generator 5.15.4

from settings import VERSION, root_logger, today
from db import fetch_transfers_logs, search_on_copiers_log
import sys
from PyQt5 import QtCore, QtGui, QtWidgets

sys.stderr.write = root_logger.error
sys.stdout.write = root_logger.info


class Ui_transfers_logs_window(QtWidgets.QWidget):
    window_closed = QtCore.pyqtSignal()  # Το Signal πρεπει να είναι εκτός __init__ δεν δουλευει αλλιως

    def __init__(self):
        super(Ui_transfers_logs_window, self).__init__()
        self.all_logs = None

    def setupUi(self, transfers_logs_window):
        transfers_logs_window.setObjectName("transfers_logs_window")
        transfers_logs_window.resize(1024, 405)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setItalic(False)
        transfers_logs_window.setFont(font)
        transfers_logs_window.setWindowTitle(f"Ιστορικό μεταφορών μηχανημάτων {VERSION}")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icons/transport_history.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        transfers_logs_window.setWindowIcon(icon)
        self.formLayout = QtWidgets.QFormLayout(transfers_logs_window)
        self.formLayout.setObjectName("formLayout")
        self.search_line_edit = QtWidgets.QLineEdit(transfers_logs_window)
        self.search_line_edit.setMinimumSize(QtCore.QSize(0, 30))
        self.search_line_edit.setObjectName("search_line_edit")
        self.search_line_edit.returnPressed.connect(self.search)
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.search_line_edit)
        self.search_btn = QtWidgets.QToolButton(transfers_logs_window)
        self.search_btn.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.search_btn.setFont(font)
        self.search_btn.setToolTip("Κουμπή αναζήτησης")
        self.search_btn.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.search_btn.setAutoFillBackground(False)
        self.search_btn.setText("Αναζήτηση")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icons/search.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.search_btn.setIcon(icon)
        self.search_btn.setAutoRepeatDelay(300)
        self.search_btn.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.search_btn.setObjectName("search_btn")
        self.search_btn.clicked.connect(self.search)
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.search_btn)
        self.label = QtWidgets.QLabel(transfers_logs_window)
        self.label.setMinimumSize(QtCore.QSize(0, 50))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(14)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setStyleSheet("background-color: rgb(90, 90, 90);\n"
                                 "color: rgb(255, 255, 255);")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.SpanningRole, self.label)
        self.tasks_treeWidget = QtWidgets.QTreeWidget(transfers_logs_window)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tasks_treeWidget.sizePolicy().hasHeightForWidth())
        self.tasks_treeWidget.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setItalic(False)
        self.tasks_treeWidget.setFont(font)
        self.tasks_treeWidget.setAutoFillBackground(False)
        self.tasks_treeWidget.setWordWrap(True)
        self.tasks_treeWidget.setObjectName("tasks_treeWidget")
        self.tasks_treeWidget.headerItem().setText(0, "Ημερομηνία")
        self.tasks_treeWidget.headerItem().setTextAlignment(0, QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.tasks_treeWidget.headerItem().setFont(0, font)
        self.tasks_treeWidget.headerItem().setBackground(0, QtGui.QColor(203, 203, 203))
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        self.tasks_treeWidget.headerItem().setForeground(0, brush)
        self.tasks_treeWidget.headerItem().setText(1, "Μηχάνημα")
        self.tasks_treeWidget.headerItem().setTextAlignment(1, QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.tasks_treeWidget.headerItem().setFont(1, font)
        self.tasks_treeWidget.headerItem().setBackground(1, QtGui.QColor(203, 203, 203))
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        self.tasks_treeWidget.headerItem().setForeground(1, brush)
        self.tasks_treeWidget.headerItem().setText(2, "Serial")
        self.tasks_treeWidget.headerItem().setTextAlignment(2, QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.tasks_treeWidget.headerItem().setFont(2, font)
        self.tasks_treeWidget.headerItem().setBackground(2, QtGui.QColor(203, 203, 203))
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        self.tasks_treeWidget.headerItem().setForeground(2, brush)
        self.tasks_treeWidget.headerItem().setText(3, "Προηγ. πελάτης")
        self.tasks_treeWidget.headerItem().setTextAlignment(3, QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.tasks_treeWidget.headerItem().setFont(3, font)
        self.tasks_treeWidget.headerItem().setBackground(3, QtGui.QColor(203, 203, 203))
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        self.tasks_treeWidget.headerItem().setForeground(3, brush)
        self.tasks_treeWidget.headerItem().setTextAlignment(4, QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.tasks_treeWidget.headerItem().setFont(4, font)
        self.tasks_treeWidget.headerItem().setBackground(4, QtGui.QColor(203, 203, 203))
        self.tasks_treeWidget.headerItem().setTextAlignment(5, QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.tasks_treeWidget.headerItem().setFont(5, font)
        self.tasks_treeWidget.headerItem().setBackground(5, QtGui.QColor(203, 203, 203))
        self.tasks_treeWidget.setAlternatingRowColors(True)
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.SpanningRole, self.tasks_treeWidget)

        # Esc
        self.shortcut_esc = QtWidgets.QShortcut(QtGui.QKeySequence('Escape'), transfers_logs_window)
        self.shortcut_esc.activated.connect(self.close)

        self.retranslateUi(transfers_logs_window)
        QtCore.QMetaObject.connectSlotsByName(transfers_logs_window)
        self.show_all_logs()

    def retranslateUi(self, transfers_logs_window):
        _translate = QtCore.QCoreApplication.translate
        self.label.setText(_translate("transfers_logs_window", "Ιστορικό μεταφορών μηχανημάτων"))
        self.tasks_treeWidget.setSortingEnabled(True)
        self.tasks_treeWidget.headerItem().setText(4, _translate("transfers_logs_window", "Νέος πελάτης"))
        self.tasks_treeWidget.headerItem().setText(5, _translate("transfers_logs_window", "Σημειώσεις"))

    def closeEvent(self, event):
        self.window_closed.emit()
        event.accept()
        # event.ignore()  # if you want the window to never be closed

    def show_all_logs(self):
        self.all_logs = fetch_transfers_logs()
        self.tasks_treeWidget.clear()
        for index, item in enumerate(self.all_logs):
            self.log_item = QtWidgets.QTreeWidgetItem(self.tasks_treeWidget,
                                                      [str(item.Ημερομηνία), str(item.machine.Εταιρεία),
                                                       str(item.machine.Serial),
                                                       str(item.Προηγούμενος_Πελάτης),
                                                       str(item.Νέος_Πελάτης), item.Σημειώσεις])
            self.log_item.setData(0, QtCore.Qt.DisplayRole,
                                  QtCore.QDate.fromString(item.Ημερομηνία.replace(" ", "/"), "dd'/'MM'/'yyyy"))
            self.log_item.setTextAlignment(0, QtCore.Qt.AlignCenter)
            self.log_item.setTextAlignment(1, QtCore.Qt.AlignCenter)
            self.log_item.setTextAlignment(2, QtCore.Qt.AlignCenter)
            self.log_item.setTextAlignment(3, QtCore.Qt.AlignCenter)
            self.log_item.setTextAlignment(4, QtCore.Qt.AlignCenter)
            self.tasks_treeWidget.setStyleSheet("QTreeView::item { padding: 7px }")
            self.tasks_treeWidget.addTopLevelItem(self.log_item)
        self.tasks_treeWidget.setColumnWidth(0, 100)
        self.tasks_treeWidget.setColumnWidth(1, 200)
        self.tasks_treeWidget.setColumnWidth(2, 150)
        self.tasks_treeWidget.setColumnWidth(3, 200)
        self.tasks_treeWidget.setColumnWidth(4, 200)
        self.tasks_treeWidget.sortByColumn(0, QtCore.Qt.DescendingOrder)

    def search(self):
        if self.search_line_edit.text() == "":
            self.show_all_logs()
            return
        log_obj = search_on_copiers_log(self.search_line_edit.text())
        self.search_line_edit.clear()
        self.tasks_treeWidget.clear()
        for index, item in enumerate(log_obj):
            self.log_item = QtWidgets.QTreeWidgetItem(self.tasks_treeWidget,
                                                      [str(item.Ημερομηνία), str(item.machine.Εταιρεία),
                                                       str(item.machine.Serial),
                                                       str(item.Προηγούμενος_Πελάτης),
                                                       str(item.Νέος_Πελάτης), item.Σημειώσεις])
            self.log_item.setData(0, QtCore.Qt.DisplayRole,
                                  QtCore.QDate.fromString(item.Ημερομηνία.replace(" ", "/"), "dd'/'MM'/'yyyy"))
            self.log_item.setTextAlignment(2, QtCore.Qt.AlignCenter)
            self.log_item.setTextAlignment(3, QtCore.Qt.AlignCenter)
            self.log_item.setTextAlignment(4, QtCore.Qt.AlignCenter)
            self.tasks_treeWidget.setStyleSheet("QTreeView::item { padding: 7px }")
            self.tasks_treeWidget.addTopLevelItem(self.log_item)
        self.tasks_treeWidget.setColumnWidth(0, 100)
        self.tasks_treeWidget.setColumnWidth(1, 200)
        self.tasks_treeWidget.setColumnWidth(2, 150)
        self.tasks_treeWidget.setColumnWidth(3, 200)
        self.tasks_treeWidget.setColumnWidth(4, 200)
        self.tasks_treeWidget.sortByColumn(1, QtCore.Qt.AscendingOrder)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")
    transfers_logs_window = QtWidgets.QWidget()
    ui = Ui_transfers_logs_window()
    ui.setupUi(transfers_logs_window)
    transfers_logs_window.show()
    sys.exit(app.exec_())
