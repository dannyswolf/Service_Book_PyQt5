# -*- coding: utf-8 -*-
# Created by: PyQt5 UI code generator 5.15.4

import re
import sys
import subprocess
import os
import shutil
import pathlib  # Για αποθήκευση αρχείου να πάρουμε μόνο την κατάληξει .svg.png
from settings import today, root_logger, SPARE_PARTS_ROOT, VERSION
import sqlalchemy
from sqlalchemy.sql import exists
import traceback
from PyQt5.QtCore import pyqtSignal
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_View_Files_Window(QtWidgets.QWidget):
    window_closed = pyqtSignal()  # Το Signal πρεπει να είναι εκτός __init__ δεν δουλευει αλλιως

    def __init__(self, *args, **kwargs):
        super(Ui_View_Files_Window, self).__init__(*args, **kwargs)
        self.selected_id = None

        self.images_path = None
        self.files = None
        self.file = None  # αρχείο που εμφανίζεται
        self.file_index = None  # Δεικτης για το ποιο αρχείο εμφανίζεται

    def setupUi(self, View_Files_Window):
        View_Files_Window.setObjectName("edit_spare_parts_window")
        View_Files_Window.resize(883, 662)
        self.gridLayout = QtWidgets.QGridLayout(View_Files_Window)
        self.gridLayout.setObjectName("gridLayout")
        self.image_label = QtWidgets.QLabel(View_Files_Window)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.image_label.sizePolicy().hasHeightForWidth())
        self.image_label.setSizePolicy(sizePolicy)
        self.image_label.setSizeIncrement(QtCore.QSize(2, 2))
        self.image_label.setText("")
        self.image_label.setAlignment(QtCore.Qt.AlignCenter)
        self.image_label.setObjectName("image_label")
        self.gridLayout.addWidget(self.image_label, 0, 0, 2, 4)

        self.save_file_btn = QtWidgets.QToolButton(View_Files_Window)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.save_file_btn.sizePolicy().hasHeightForWidth())
        self.save_file_btn.setSizePolicy(sizePolicy)
        self.save_file_btn.setStyleSheet("font: 75 14pt \"Calibri\";\n"
"color: rgb(255, 255, 255);\n"
"background-color: rgb(85, 170, 0);")
        self.save_file_btn.setObjectName("save_file_btn")
        self.save_file_btn.clicked.connect(self.save_file)
        self.gridLayout.addWidget(self.save_file_btn, 5, 1, 1, 2)

        # Νεο κουμπί ανοιγμα pdf
        self.open_pdf_file_btn = QtWidgets.QToolButton(View_Files_Window)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.open_pdf_file_btn.sizePolicy().hasHeightForWidth())
        self.open_pdf_file_btn.setSizePolicy(sizePolicy)
        self.open_pdf_file_btn.setStyleSheet("font: 75 14pt \"Calibri\";\n"
                                             "color: rgb(255, 255, 255);\n"
                                             "background-color: rgb(85, 170, 0);")
        self.open_pdf_file_btn.setObjectName("open_pdf_file_btn")
        self.gridLayout.addWidget(self.open_pdf_file_btn, 5, 1, 1, 2)
        self.open_pdf_file_btn.hide()  # να είναι κρυφό το εμφανίζει το show_file οταν χρειάζεται

        # Delete File
        self.delete_file_btn = QtWidgets.QToolButton(View_Files_Window)
        self.delete_file_btn.setStyleSheet("font: 75 14pt \"Calibri\";\n"
"color: rgb(255, 255, 255);\n"
"background-color: rgb(255, 0, 0);")
        self.delete_file_btn.setObjectName("delete_file_btn")
        self.delete_file_btn.clicked.connect(self.delete_file)
        self.gridLayout.addWidget(self.delete_file_btn, 5, 3, 1, 1)

        # Next
        self.next_image_btn = QtWidgets.QToolButton(View_Files_Window)
        self.next_image_btn.setStyleSheet("font: 75 14pt \"Calibri\";\n"
"background-color: rgb(255, 255, 0);")
        self.next_image_btn.setObjectName("next_image_btn")
        self.next_image_btn.clicked.connect(self.next_file)
        self.gridLayout.addWidget(self.next_image_btn, 3, 2, 1, 1)

        # Previous
        self.previous_image_btn = QtWidgets.QToolButton(View_Files_Window)
        self.previous_image_btn.setStyleSheet("font: 75 14pt \"Calibri\";\n"
"background-color: rgb(255, 255, 0);")
        self.previous_image_btn.setObjectName("previwes_image_btn")
        self.previous_image_btn.clicked.connect(self.previous_file)
        self.gridLayout.addWidget(self.previous_image_btn, 3, 1, 1, 1)

        # Add file
        self.add_file_btn = QtWidgets.QToolButton(View_Files_Window)
        self.add_file_btn.setStyleSheet("font: 75 14pt \"Calibri\";\n"
"color: rgb(255, 255, 255);\n"
"background-color: rgb(0, 170, 127);")
        self.add_file_btn.setObjectName("add_file_btn")
        self.add_file_btn.clicked.connect(self.add_file)
        self.gridLayout.addWidget(self.add_file_btn, 5, 0, 1, 1)

        # Αριθμός αρχείων
        self.no_of_files_label = QtWidgets.QLabel(View_Files_Window)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.no_of_files_label.setFont(font)
        self.no_of_files_label.setObjectName("no_of_files_label")
        # self.no_of_files_label.setText(f"Αρχείο {self.file_index}  απο {len(self.files)}")
        self.gridLayout.addWidget(self.no_of_files_label, 3, 0, 1, 1)

        # Esc
        self.shortcut_esc = QtWidgets.QShortcut(QtGui.QKeySequence('Escape'), View_Files_Window)
        self.shortcut_esc.activated.connect(lambda: self.close())

        self.retranslateUi(View_Files_Window)
        QtCore.QMetaObject.connectSlotsByName(View_Files_Window)

    def retranslateUi(self, View_Files_Window):
        _translate = QtCore.QCoreApplication.translate
        View_Files_Window.setWindowTitle(_translate("View_Files_Window", f"Προβολή αρχείων {VERSION}"))
        self.save_file_btn.setText(_translate("View_Files_Window", "Αποθήκευση αρχείου"))
        self.delete_file_btn.setText(_translate("View_Files_Window", "Διαγραφή αρχείου"))
        self.next_image_btn.setText(_translate("View_Files_Window", "Επόμενο"))
        self.previous_image_btn.setText(_translate("View_Files_Window", "Προηγούμενο"))
        self.add_file_btn.setText(_translate("View_Files_Window", "Προσθήκη αρχείου"))
        self.open_pdf_file_btn.setText(_translate("View_Files_Window", "Ανοιγμα αρχείου pdf"))

    def add_file(self):
        options = QtWidgets.QFileDialog.Options()
        new_files, _ = QtWidgets.QFileDialog.getOpenFileNames(None, "QFileDialog.getOpenFileNames()", "",
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
                    self.files = os.listdir(self.images_path)
                    self.show_file()
                else:
                    QtWidgets.QMessageBox.warning(None, "Σφάλμα",
                                        f"Το αρχείο {os.path.basename(new_file)} υπάρχει.\nΠαρακαλώ αλλάξτε όνομα ή "
                                        f"επιλεξτε διαφορετικό αρχείο")

    def show_file(self):  # Εμφάνησει πρώτου αρχείου όταν ανοιγει το παράθυρο η συνάρτηση καλειτε απο το store.py
        try:

            if self.files[0]:  # αν δεν υπάρχει βγαζει IndexError:  δλδ δεν υπάρχει αχρείο
                self.file_index = 0  # Ορισμός οτι βλέπουμε το πρώτο αρχείο
                self.file = os.path.join(self.images_path, self.files[0])
                self.no_of_files_label.setText(f"Αρχείο {self.file_index +1}  απο {len(self.files)}")
                if pathlib.Path(self.file).suffix != ".pdf":
                    pixmap = QtGui.QPixmap(os.path.join(self.images_path, self.files[0]))
                    resized_pixmap = pixmap.scaled(600, 600, QtCore.Qt.KeepAspectRatio)
                    self.image_label.setPixmap(resized_pixmap)
                    # self.image_label.setScaledContents(True)
                    self.image_label.show()
                    self.open_pdf_file_btn.hide()  # Απόκρηψη ανοιγμα αρχείου pdf αφου δεν ειναι pdf
                    self.save_file_btn.show()  # Εμφάνηση αποθήκευσης αρχείου αφου δεν ειναι pdf
                else:  # "icons/pdf.png"
                    self.save_file_btn.hide()  # Απόκρηψη αποθήκευσης αρχείου αφου ειναι pdf
                    pixmap = QtGui.QPixmap("icons/pdf.png")
                    resized_pixmap = pixmap.scaled(200, 200, QtCore.Qt.KeepAspectRatio)
                    self.image_label.setPixmap(resized_pixmap)
                    # self.image_label.setScaledContents(True)
                    self.image_label.show()
                    self.open_pdf_file_btn.clicked.connect(self.open_pdf)
                    self.open_pdf_file_btn.show()

            if len(self.files) == 1:  # αν υπάρχει μόνο ένα αρχείο
                self.file = os.path.join(self.images_path, self.files[0])
                # απόκρηψη κουμπιών
                self.next_image_btn.hide()
                self.previous_image_btn.hide()
                if pathlib.Path(self.file).suffix != ".pdf":
                    self.open_pdf_file_btn.hide()  # Απόκρηψη ανοιγμα αρχείου pdf αφου δεν ειναι pdf
                    self.save_file_btn.show()  # Εμφάνηση αποθήκευσης αρχείου αφου δεν ειναι pdf
                else:
                    self.open_pdf_file_btn.clicked.connect(self.open_pdf)
                    self.save_file_btn.hide()  # Απόκρηψη αποθήκευσης αρχείου αφου ειναι pdf
                    self.open_pdf_file_btn.show()

                self.delete_file_btn.show()
            if len(self.files) > 1:
                self.file = os.path.join(self.images_path, self.files[0])
                self.next_image_btn.show()
                self.previous_image_btn.show()
                # self.save_file_btn.show()
                self.delete_file_btn.show()
        except (IndexError, TypeError):  # αν δεν υπάρχει κανένα αρχείο
            self.no_of_files_label.setText(f"Δεν υπάρχει κανένα αρχείο")
            # NoneType οταν ξεκοιναει απο το store.py το self.files = None
            # απόκρηψη κουμπιών
            self.close()  # Να κλείνει αν δεν έχει αρχείο
            # self.image_label.hide()
            # self.next_image_btn.hide()
            # self.previous_image_btn.hide()
            # self.save_file_btn.hide()
            # self.delete_file_btn.hide()
            # self.open_pdf_file_btn.hide()

    def next_file(self):
        try:
            if len(self.files) > 1:  # αν υπάρχει πάνω απο ένα αρχείο
                if self.files[self.file_index] == self.files[-1]:  # Αν είναι το τελευταίο αρχείο
                    self.file_index = 0  # να πάει πάλι απο την αρχή
                    self.no_of_files_label.setText(f"Αρχείο {self.file_index + 1}  απο {len(self.files)}")
                else:  # Αν δεν είναι το τελευταίο
                    self.file_index += 1  # να πάει στο επώμενο αρχείο
                    self.no_of_files_label.setText(f"Αρχείο {self.file_index + 1}  απο {len(self.files)}")
                self.file = os.path.join(self.images_path, self.files[self.file_index])  # να πάει στην δευτερη εικόνα
                if pathlib.Path(self.file).suffix != ".pdf":
                    self.open_pdf_file_btn.hide()  # Απόκρηψη ανοιγμα αρχείου pdf αφου δεν ειναι pdf
                    self.save_file_btn.show()  # Εμφάνηση αποθήκευσης αρχείου αφου δεν ειναι pdf
                    self.open_pdf_file_btn.hide()
                    pixmap = QtGui.QPixmap(os.path.join(self.images_path, self.files[self.file_index]))
                    resized_pixmap = pixmap.scaled(600, 600, QtCore.Qt.KeepAspectRatio)
                    self.image_label.setPixmap(resized_pixmap)
                    # self.image_label.setScaledContents(True)
                else:  # "icons/pdf.png"
                    self.save_file_btn.hide()  # Απόκρηψη αποθήκευσης αρχείου αφου ειναι pdf
                    pixmap = QtGui.QPixmap("icons/pdf.png")
                    resized_pixmap = pixmap.scaled(200, 200, QtCore.Qt.KeepAspectRatio)
                    self.image_label.setPixmap(resized_pixmap)
                    # self.image_label.setScaledContents(True)
                    self.open_pdf_file_btn.clicked.connect(self.open_pdf)
                    self.open_pdf_file_btn.show()  # Εμφάνηση ανοιγμα pdf
            elif len(self.files) == 1:  # αν υπάρχει μόνο ένα αρχείο
                self.file = os.path.join(self.images_path, self.files[self.file_index])
                # απόκρηψη κουμπιών
                self.next_image_btn.hide()
                self.previous_image_btn.hide()
        except TypeError:  # Αν δεν υπάρχει καποιο αρχείο
            # απόκρηψη κουμπιών
            self.next_image_btn.hide()
            self.previous_image_btn.hide()

    def previous_file(self):
        try:
            if len(self.files) > 1:  # αν υπάρχει πάνω απο ένα αρχείο
                if self.files[self.file_index] == self.files[0]:  # Αν είναι το πρώτο αρχείο
                    self.file_index = -1  # να πάει πάλι απο το τέλος
                    self.no_of_files_label.setText(f"Αρχείο {self.file_index + 1}  απο {len(self.files)}")
                else:  # Αν δεν είναι το πρώτο
                    self.file_index -= 1  # να πάει στο προηγούμενο αρχείο
                    self.no_of_files_label.setText(f"Αρχείο {self.file_index + 1}  απο {len(self.files)}")
                self.file = os.path.join(self.images_path, self.files[self.file_index])  # να πάει στην δευτερη εικόνα
                if pathlib.Path(self.file).suffix != ".pdf":
                    self.open_pdf_file_btn.hide()  # Απόκρηψη ανοιγμα αρχείου pdf αφου δεν ειναι pdf
                    self.save_file_btn.show()  # Εμφάνηση αποθήκευσης αρχείου αφου δεν ειναι pdf
                    pixmap = QtGui.QPixmap(os.path.join(self.images_path, self.files[self.file_index]))
                    resized_pixmap = pixmap.scaled(600, 600, QtCore.Qt.KeepAspectRatio)
                    self.image_label.setPixmap(resized_pixmap)
                    # self.image_label.setScaledContents(True)
                else:  # "icons/pdf.png"
                    self.save_file_btn.hide()  # Απόκρηψη αποθήκευσης αρχείου αφου ειναι pdf
                    pixmap = QtGui.QPixmap("icons/pdf.png")
                    resized_pixmap = pixmap.scaled(200, 200, QtCore.Qt.KeepAspectRatio)
                    self.image_label.setPixmap(resized_pixmap)
                    # self.image_label.setScaledContents(True)
                    self.open_pdf_file_btn.clicked.connect(self.open_pdf)
                    self.open_pdf_file_btn.show()  # Εμφάνηση ανοιγμα pdf
            elif len(self.files) == 1:  # αν υπάρχει μόνο ένα αρχείο
                self.file = os.path.join(self.images_path, self.files[self.file_index])
                # απόκρηψη κουμπιών
                self.next_image_btn.hide()
                self.previous_image_btn.hide()
        except TypeError:  # Αν δεν υπάρχει καποιο αρχείο
            # απόκρηψη κουμπιών
            self.next_image_btn.hide()
            self.previous_image_btn.hide()

    def save_file(self):
        pixmap = QtGui.QPixmap(os.path.join(self.images_path, self.files[self.file_index]))
        filename = os.path.basename(self.files[self.file_index])
        extension = pathlib.Path(filename).suffix
        try:
            #  file_to_save == ('/home/dannys/Desktop/add_files.png', '')
            file_to_save = QtWidgets.QFileDialog.getSaveFileName(self, 'Αποθήκευση αρχείου', f'{filename}', f'*{extension}')
            if file_to_save[0] == "":  # file_to_save == ('', '') αν πατήση ακυρο ο χρήστης
                return
            pixmap.save(file_to_save[0], quality=100)
            QtWidgets.QMessageBox.information(None, "Επιτυχία", f'Το αρχεία {filename} αποθηκεύτηκε '
                                                      f'επιτυχώς')
        except TypeError:  # Αν δεν πατησει αποθήκευση
            return

    def delete_file(self):
        filename = os.path.basename(self.files[self.file_index])
        answer = QtWidgets.QMessageBox.question(self, 'Quit', f"Σίγουρα θέλετε να διαγράψετε το {filename} ?",
                                      QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
        if answer == QtWidgets.QMessageBox.Yes:
            try:
                os.remove(os.path.join(self.images_path, self.files[self.file_index]))
                self.files.pop(self.file_index)
                QtWidgets.QMessageBox.information(None, "Επιτυχία", f'Το αρχεία {filename} διαγράφτηκε ' f'επιτυχώς')
            except FileNotFoundError:  # Οταν για κάποιο λόγο δεν βρισκει το αρχείο για διαγραφή
                pass
            self.show_file()

    def open_pdf(self):
        if sys.platform == "win32":
            subprocess.Popen(self.file, shell=True)
        elif sys.platform == "linux":
            os.system("okular " + self.file)

    def closeEvent(self, event):
        self.window_closed.emit()
        event.accept()
        # event.ignore() # if you want the window to never be closed


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")
    View_Files_Window = QtWidgets.QWidget()
    ui = Ui_View_Files_Window()
    ui.setupUi(View_Files_Window)
    View_Files_Window.show()
    sys.exit(app.exec_())
