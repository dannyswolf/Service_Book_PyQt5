# -*- coding: utf-8 -*-
# Created by: PyQt5 UI code generator 5.15.4

import sqlalchemy
import sys
import traceback
from db import fetch_receiver_emails_data, fetch_sender_emails_data, Sender_emails, Receiver_emails, service_session
from PyQt5 import QtCore, QtGui, QtWidgets
from settings import VERSION, root_logger

sys.stderr.write = root_logger.error
sys.stdout.write = root_logger.info


class Ui_Edit_Email_Settings_Window(QtWidgets.QWidget):
    window_closed = QtCore.pyqtSignal()  # Το Signal πρεπει να είναι εκτός __init__ δεν δουλευει αλλιως

    def __init__(self):
        super(Ui_Edit_Email_Settings_Window, self).__init__()
        self.all_receivers = fetch_receiver_emails_data()
        self.all_senders = fetch_sender_emails_data()
        self.receivers = [receiver.Receiver_email for receiver in self.all_receivers]
        self.senders = [sender.sender_email for sender in self.all_senders]
        # ------------------------------------------ Fonts -----------------------
        self.font_14_bold = QtGui.QFont()
        self.font_14_bold.setFamily("Calibri")
        self.font_14_bold.setPointSize(14)
        self.font_14_bold.setBold(True)
        self.font_14_bold.setWeight(75)

        self.font_12_bold = QtGui.QFont()
        self.font_12_bold.setFamily("Calibri")
        self.font_12_bold.setPointSize(12)
        self.font_12_bold.setBold(True)
        self.font_12_bold.setWeight(75)

        self.font_13 = QtGui.QFont()
        self.font_13.setFamily("Calibri")
        self.font_13.setPointSize(13)
        self.font_13.setBold(False)
        self.font_13.setWeight(50)

        self.font_13_bold = QtGui.QFont()
        self.font_13_bold.setFamily("Calibri")
        self.font_13_bold.setPointSize(13)
        self.font_13_bold.setBold(True)
        self.font_13_bold.setWeight(75)

    def setupUi(self, Edit_Email_Settings_Window):
        Edit_Email_Settings_Window.setObjectName("Edit_Email_Settings_Window")
        Edit_Email_Settings_Window.setWindowModality(QtCore.Qt.WindowModal)
        Edit_Email_Settings_Window.resize(500, 500)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icons/icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Edit_Email_Settings_Window.setWindowIcon(icon)
        Edit_Email_Settings_Window.setWindowFilePath("")
        self.gridLayout = QtWidgets.QGridLayout(Edit_Email_Settings_Window)
        self.gridLayout.setObjectName("gridLayout")

        # Sender Email
        self.sender_email_combobox = QtWidgets.QComboBox(self)
        self.sender_email_combobox.setFont(self.font_13_bold)
        self.sender_email_combobox.setMinimumSize(250, 35)
        self.sender_email_combobox.addItems(self.senders)
        self.sender_email_combobox.currentIndexChanged.connect(self.show_selected_sender_details)
        self.gridLayout.addWidget(self.sender_email_combobox, 3, 0, 1, 5)


        # Sender Name
        self.sender_name_lineEdit = QtWidgets.QLineEdit(Edit_Email_Settings_Window)
        self.sender_name_lineEdit.setMinimumSize(QtCore.QSize(0, 35))
        self.sender_name_lineEdit.setFont(self.font_13)
        self.sender_name_lineEdit.setObjectName("sender_name_lineEdit")
        self.gridLayout.addWidget(self.sender_name_lineEdit, 5, 0, 1, 1)

        # Password
        self.password_lineEdit = QtWidgets.QLineEdit(Edit_Email_Settings_Window)
        self.password_lineEdit.setMinimumSize(QtCore.QSize(0, 35))
        self.password_lineEdit.setFont(self.font_13)
        self.password_lineEdit.setObjectName("password_lineEdit")
        self.password_lineEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.gridLayout.addWidget(self.password_lineEdit, 5, 1, 1, 4)

        # Smtp
        self.smtp_server_lineEdit = QtWidgets.QLineEdit(Edit_Email_Settings_Window)
        self.smtp_server_lineEdit.setMinimumSize(QtCore.QSize(0, 35))
        self.smtp_server_lineEdit.setFont(self.font_13)
        self.smtp_server_lineEdit.setObjectName("smtp_server_lineEdit")
        self.gridLayout.addWidget(self.smtp_server_lineEdit, 8, 0, 1, 1)

        # Port
        self.port_lineEdit = QtWidgets.QLineEdit(Edit_Email_Settings_Window)
        self.port_lineEdit.setMinimumSize(QtCore.QSize(0, 35))
        self.port_lineEdit.setMaximumSize(QtCore.QSize(100, 16777215))
        self.port_lineEdit.setFont(self.font_13)
        self.port_lineEdit.setObjectName("port_lineEdit")
        self.gridLayout.addWidget(self.port_lineEdit, 8, 1, 1, 1)

        # Receiver
        self.receiver_lineEdit = QtWidgets.QLineEdit(Edit_Email_Settings_Window)
        self.receiver_lineEdit.setMinimumSize(QtCore.QSize(0, 35))
        self.receiver_lineEdit.setFont(self.font_13)
        self.receiver_lineEdit.setObjectName("receiver_lineEdit")

        self.receiver_combobox = QtWidgets.QComboBox(self)
        self.receiver_combobox.setFont(self.font_13_bold)
        self.receiver_combobox.setMinimumSize(250, 35)
        self.receiver_combobox.addItems(self.receivers)
        # self.receiver_combobox.currentIndexChanged.connect(self.check_if_machine_exist_from_combobox)
        self.receiver_combobox.setLineEdit(self.receiver_lineEdit)
        self.gridLayout.addWidget(self.receiver_combobox, 12, 0, 1, 2)

        self.sender_name_label = QtWidgets.QLabel(Edit_Email_Settings_Window)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sender_name_label.sizePolicy().hasHeightForWidth())
        self.sender_name_label.setSizePolicy(sizePolicy)
        self.sender_name_label.setMinimumSize(QtCore.QSize(0, 25))
        self.sender_name_label.setMaximumSize(QtCore.QSize(16777215, 35))
        self.sender_name_label.setFont(self.font_12_bold)
        self.sender_name_label.setStyleSheet("background-color: rgb(93, 93, 93);\n"
"color: rgb(255, 255, 255);")
        self.sender_name_label.setAlignment(QtCore.Qt.AlignCenter)
        self.sender_name_label.setObjectName("sender_name_label")
        self.gridLayout.addWidget(self.sender_name_label, 4, 0, 1, 1)
        self.receiver_label = QtWidgets.QLabel(Edit_Email_Settings_Window)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.receiver_label.sizePolicy().hasHeightForWidth())
        self.receiver_label.setSizePolicy(sizePolicy)
        self.receiver_label.setMinimumSize(QtCore.QSize(0, 25))
        self.receiver_label.setMaximumSize(QtCore.QSize(16777215, 35))
        self.receiver_label.setFont(self.font_12_bold)
        self.receiver_label.setStyleSheet("background-color: rgb(93, 93, 93);\n"
"color: rgb(255, 255, 255);")
        self.receiver_label.setAlignment(QtCore.Qt.AlignCenter)
        self.receiver_label.setObjectName("receiver_label")
        self.gridLayout.addWidget(self.receiver_label, 10, 0, 1, 5)
        self.smtp_server_label = QtWidgets.QLabel(Edit_Email_Settings_Window)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.smtp_server_label.sizePolicy().hasHeightForWidth())
        self.smtp_server_label.setSizePolicy(sizePolicy)
        self.smtp_server_label.setMinimumSize(QtCore.QSize(0, 25))
        self.smtp_server_label.setMaximumSize(QtCore.QSize(16777215, 35))
        self.smtp_server_label.setFont(self.font_12_bold)
        self.smtp_server_label.setStyleSheet("background-color: rgb(93, 93, 93);\n"
"color: rgb(255, 255, 255);")
        self.smtp_server_label.setAlignment(QtCore.Qt.AlignCenter)
        self.smtp_server_label.setObjectName("smtp_server_label")
        self.gridLayout.addWidget(self.smtp_server_label, 7, 0, 1, 1)
        self.port_label = QtWidgets.QLabel(Edit_Email_Settings_Window)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.port_label.sizePolicy().hasHeightForWidth())
        self.port_label.setSizePolicy(sizePolicy)
        self.port_label.setMinimumSize(QtCore.QSize(0, 25))
        self.port_label.setMaximumSize(QtCore.QSize(100, 35))
        self.port_label.setFont(self.font_12_bold)
        self.port_label.setStyleSheet("background-color: rgb(93, 93, 93);\n"
"color: rgb(255, 255, 255);")
        self.port_label.setAlignment(QtCore.Qt.AlignCenter)
        self.port_label.setObjectName("port_label")
        self.gridLayout.addWidget(self.port_label, 7, 1, 1, 1)

        # save sender
        self.save_sender_toolButton = QtWidgets.QToolButton(Edit_Email_Settings_Window)
        self.save_sender_toolButton.setFont(self.font_12_bold)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("icons/add_to_service_data2.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.save_sender_toolButton.setIcon(icon1)
        self.save_sender_toolButton.setIconSize(QtCore.QSize(30, 30))
        self.save_sender_toolButton.setObjectName("save_sender_toolButton")
        self.save_sender_toolButton.clicked.connect(self.save_sender)
        self.gridLayout.addWidget(self.save_sender_toolButton, 8, 2, 1, 1)

        # Delete Sender
        self.delete_sender_toolButton = QtWidgets.QToolButton(Edit_Email_Settings_Window)
        self.delete_sender_toolButton.setFont(self.font_12_bold)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("icons/remove_from_list.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.delete_sender_toolButton.setIcon(icon2)
        self.delete_sender_toolButton.setIconSize(QtCore.QSize(30, 30))
        self.delete_sender_toolButton.setObjectName("delete_sender_toolButton")
        self.delete_sender_toolButton.clicked.connect(self.delete_sender)
        self.gridLayout.addWidget(self.delete_sender_toolButton, 8, 4, 1, 1)


        self.password_label = QtWidgets.QLabel(Edit_Email_Settings_Window)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.password_label.sizePolicy().hasHeightForWidth())
        self.password_label.setSizePolicy(sizePolicy)
        self.password_label.setMinimumSize(QtCore.QSize(0, 25))
        self.password_label.setMaximumSize(QtCore.QSize(16777215, 35))
        self.password_label.setFont(self.font_12_bold)
        self.password_label.setStyleSheet("background-color: rgb(93, 93, 93);\n"
"color: rgb(255, 255, 255);")
        self.password_label.setAlignment(QtCore.Qt.AlignCenter)
        self.password_label.setObjectName("password_label")
        self.gridLayout.addWidget(self.password_label, 4, 1, 1, 4)

        # Save Receiver
        self.save_receiver_toolButton = QtWidgets.QToolButton(Edit_Email_Settings_Window)
        self.save_receiver_toolButton.setFont(self.font_12_bold)
        self.save_receiver_toolButton.setIcon(icon1)
        self.save_receiver_toolButton.setIconSize(QtCore.QSize(30, 30))
        self.save_receiver_toolButton.setObjectName("save_receiver_toolButton")
        self.save_receiver_toolButton.clicked.connect(self.save_receiver)
        self.gridLayout.addWidget(self.save_receiver_toolButton, 12, 2, 1, 1)

        # Delete Receiver
        self.delete_receiver_toolButton = QtWidgets.QToolButton(Edit_Email_Settings_Window)
        self.delete_receiver_toolButton.setFont(self.font_12_bold)
        self.delete_receiver_toolButton.setIcon(icon2)
        self.delete_receiver_toolButton.setIconSize(QtCore.QSize(30, 30))
        self.delete_receiver_toolButton.setObjectName("delete_receiver_toolButton")
        self.delete_receiver_toolButton.clicked.connect(self.delete_receiver)
        self.gridLayout.addWidget(self.delete_receiver_toolButton, 12, 4, 1, 1)


        self.sender_email_label = QtWidgets.QLabel(Edit_Email_Settings_Window)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sender_email_label.sizePolicy().hasHeightForWidth())
        self.sender_email_label.setSizePolicy(sizePolicy)
        self.sender_email_label.setMinimumSize(QtCore.QSize(0, 25))
        self.sender_email_label.setMaximumSize(QtCore.QSize(16777215, 35))
        self.sender_email_label.setFont(self.font_12_bold)
        self.sender_email_label.setStyleSheet("background-color: rgb(93, 93, 93);\n"
"color: rgb(255, 255, 255);")
        self.sender_email_label.setAlignment(QtCore.Qt.AlignCenter)
        self.sender_email_label.setObjectName("sender_email_label")
        self.gridLayout.addWidget(self.sender_email_label, 2, 0, 1, 5)
        self.top_label = QtWidgets.QLabel(Edit_Email_Settings_Window)
        self.top_label.setMinimumSize(QtCore.QSize(0, 30))
        self.top_label.setMaximumSize(QtCore.QSize(16777215, 50))
        self.top_label.setFont(self.font_14_bold)
        self.top_label.setStyleSheet("background-color: #005900;\n"
"color: rgb(255, 255, 255);")
        self.top_label.setAlignment(QtCore.Qt.AlignCenter)
        self.top_label.setObjectName("top_label")
        self.gridLayout.addWidget(self.top_label, 0, 0, 1, 5)
        self.top_label_2 = QtWidgets.QLabel(Edit_Email_Settings_Window)
        self.top_label_2.setMinimumSize(QtCore.QSize(0, 30))
        self.top_label_2.setMaximumSize(QtCore.QSize(16777215, 50))
        self.top_label_2.setFont(self.font_14_bold)
        self.top_label_2.setStyleSheet("background-color: rgb(0, 85, 127);\n"
"color: rgb(255, 255, 255);")
        self.top_label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.top_label_2.setObjectName("top_label_2")
        self.gridLayout.addWidget(self.top_label_2, 9, 0, 1, 5)

        # Esc
        self.shortcut_esc = QtWidgets.QShortcut(QtGui.QKeySequence('Escape'), Edit_Email_Settings_Window)
        self.shortcut_esc.activated.connect(self.close)

        self.retranslateUi(Edit_Email_Settings_Window)
        QtCore.QMetaObject.connectSlotsByName(Edit_Email_Settings_Window)

        self.show_first_sender()

    def retranslateUi(self, Edit_Email_Settings_Window):
        _translate = QtCore.QCoreApplication.translate
        Edit_Email_Settings_Window.setWindowTitle(_translate("Edit_Email_Settings_Window", f"Ρυθμίσεις Email {VERSION}"))
        self.sender_name_label.setText(_translate("Edit_Email_Settings_Window", "Ονομα χρήστη"))
        self.receiver_label.setText(_translate("Edit_Email_Settings_Window", "Email"))
        self.smtp_server_label.setText(_translate("Edit_Email_Settings_Window", "Smtp Server"))
        self.port_label.setText(_translate("Edit_Email_Settings_Window", "Port"))
        self.delete_sender_toolButton.setText(_translate("Edit_Email_Settings_Window", "..."))
        self.password_label.setText(_translate("Edit_Email_Settings_Window", "Κωδικός"))
        self.save_receiver_toolButton.setText(_translate("Edit_Email_Settings_Window", "..."))
        self.delete_receiver_toolButton.setText(_translate("Edit_Email_Settings_Window", "..."))
        self.sender_email_label.setText(_translate("Edit_Email_Settings_Window", "Email"))
        self.top_label.setText(_translate("Edit_Email_Settings_Window", "Αποστολέας"))
        self.top_label_2.setText(_translate("Edit_Email_Settings_Window", "Παραλήπτες"))

    def refresh_senders_and_receivers(self):
        self.sender_email_combobox.clear()
        self.receiver_combobox.clear()
        self.all_receivers = fetch_receiver_emails_data()
        self.all_senders = fetch_sender_emails_data()
        self.receivers = [receiver.Receiver_email for receiver in self.all_receivers]
        self.senders = [sender.sender_email for sender in self.all_senders]
        self.sender_email_combobox.addItems(self.senders)
        self.receiver_combobox.addItems(self.receivers)

    def show_first_sender(self):
        try:
            self.selected_sernder = self.all_senders[0]
            self.sender_name_lineEdit.setText(self.selected_sernder.sender_email)
            self.password_lineEdit.setText(self.selected_sernder.password)
            self.smtp_server_lineEdit.setText(self.selected_sernder.smtp_server)
            self.port_lineEdit.setText(str(self.selected_sernder.port))
        except IndexError:
            self.sender_name_lineEdit.setText("")
            self.password_lineEdit.setText("")
            self.smtp_server_lineEdit.setText("")
            self.port_lineEdit.setText("")


    def show_selected_sender_details(self):
        selected_index = self.sender_email_combobox.currentIndex()
        self.selected_sernder = self.all_senders[selected_index]
        self.sender_name_lineEdit.setText(self.selected_sernder.sender_email)
        self.password_lineEdit.setText(self.selected_sernder.password)
        self.smtp_server_lineEdit.setText(self.selected_sernder.smtp_server)
        self.port_lineEdit.setText(str(self.selected_sernder.port))

    def closeEvent(self, event):
        self.window_closed.emit()
        event.accept()
        # event.ignore()  # if you want the window to never be closed

    def save_sender(self):
        try:
            sender = Sender_emails(sender_email=self.sender_name_lineEdit.text(),
                                   password=self.password_lineEdit.text(),
                                   smtp_server=self.smtp_server_lineEdit.text(),
                                   port=self.port_lineEdit.text())
            service_session.add(sender)
            service_session.commit()
            self.refresh_senders_and_receivers()
            QtWidgets.QMessageBox.information(None, "Πληροφορία!", "Ο αποστολέας αποθηκέυτηκε")
        except sqlalchemy.exc.IntegrityError:  # Οταν δεν αλλάζουμε το email τότε υπάρχει Γιατί στην βάση ειναι unique
            service_session.rollback()
            self.selected_sernder.password = self.password_lineEdit.text()
            self.selected_sernder.smtp_server = self.smtp_server_lineEdit.text()
            self.selected_sernder.port = self.port_lineEdit.text()
            service_session.commit()
            self.refresh_senders_and_receivers()
            QtWidgets.QMessageBox.information(None, "Πληροφορία!", "Οι αλλαγές αποθηκέυτηκαν")
        except Exception:
            service_session.rollback()
            traceback.print_exc()
            QtWidgets.QMessageBox.critical(None, "Σφάλμα!", "Κάτι δεν πήγε καλά!\nO αποστολέας ΔΕΝ αποθηκέυτηκε")

    def delete_sender(self):
        selected_index = self.sender_email_combobox.currentIndex()
        selected_sernder = self.all_senders[selected_index]
        answer = QtWidgets.QMessageBox.question(None, "Προσοχή!", "Σίγουρα θέλετε να σβήσετε τον αποστολέα;",
                                                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                QtWidgets.QMessageBox.No)
        if answer == QtWidgets.QMessageBox.Yes:
            try:
                service_session.delete(selected_sernder)
                service_session.commit()
                self.refresh_senders_and_receivers()
                QtWidgets.QMessageBox.information(None, "Πληροφορία!", "O αποστολέας διαγράφτηκε")
            except Exception:
                service_session.rollback()
                traceback.print_exc()
                QtWidgets.QMessageBox.critical(None, "Σφάλμα!", "Κάτι δεν πήγε καλά!\nO αποστολέας ΔΕΝ διαγράφτηκε")

    def save_receiver(self):
        try:
            receiver = Receiver_emails(Receiver_email=self.receiver_lineEdit.text())
            service_session.add(receiver)
            service_session.commit()
            self.refresh_senders_and_receivers()
            QtWidgets.QMessageBox.information(None, "Πληροφορία!", "Ο παραλήπτης αποθηκέυτηκε")
        except sqlalchemy.exc.IntegrityError:  # Οταν δεν αλλάζουμε το email τότε υπάρχει Γιατί στην βάση ειναι unique
            service_session.rollback()
            QtWidgets.QMessageBox.information(None, "Πληροφορία!", "Ο παραλήπτης δεν άλλαξε")
            return
        except Exception:
            service_session.rollback()
            traceback.print_exc()
            QtWidgets.QMessageBox.critical(None, "Σφάλμα!", "Κάτι δεν πήγε καλά!\nO παραλήπτης ΔΕΝ αποθηκέυτηκε")

    def delete_receiver(self):
        selected_index = self.receiver_combobox.currentIndex()
        self.selected_receiver = self.all_receivers[selected_index]
        answer = QtWidgets.QMessageBox.question(None, "Προσοχή!", "Σίγουρα θέλετε να σβήσετε τον παραλήπτη;",
                                                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                QtWidgets.QMessageBox.No)
        if answer == QtWidgets.QMessageBox.Yes:
            try:
                service_session.delete(self.selected_receiver)
                service_session.commit()
                self.refresh_senders_and_receivers()
                QtWidgets.QMessageBox.information(None, "Πληροφορία!", "O παραλήπτης διαγράφτηκε")
            except Exception:
                service_session.rollback()
                traceback.print_exc()
                QtWidgets.QMessageBox.critical(None, "Σφάλμα!", "Κάτι δεν πήγε καλά!\nO παραλήπτης ΔΕΝ διαγράφτηκε")


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")
    Edit_Email_Settings_Window = QtWidgets.QWidget()
    ui = Ui_Edit_Email_Settings_Window()
    ui.setupUi(Edit_Email_Settings_Window)
    Edit_Email_Settings_Window.show()
    sys.exit(app.exec_())
