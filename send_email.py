# -*- coding: utf-8 -*-
# Created by: PyQt5 UI code generator 5.15.4
import traceback
import os
import sys
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from settings import user, root_logger
from db import fetch_receiver_emails_data, fetch_sender_emails_data, get_consumables_from_service_id
from PyQt5 import QtCore, QtGui, QtWidgets

sys.stderr.write = root_logger.error
sys.stdout.write = root_logger.info


class Ui_Send_Email_Window(QtWidgets.QWidget):
    window_closed = QtCore.pyqtSignal()  # Το Signal πρεπει να είναι εκτός __init__ δεν δουλευει αλλιως

    def __init__(self):
        super(Ui_Send_Email_Window, self).__init__()
        self.selected_calendar = None
        self.data_to_send = None
        self.files_path = None
        self.selected_customer = None
        self.selected_machine = None
        self.selected_service_id = None

    def setupUi(self, Send_Email_Window):
        Send_Email_Window.setObjectName("Send_Email_Window")
        Send_Email_Window.resize(612, 350)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        Send_Email_Window.setFont(font)
        self.all_receivers = fetch_receiver_emails_data()
        self.all_senders = fetch_sender_emails_data()
        self.receivers = [receiver.Receiver_email for receiver in self.all_receivers]
        self.senders = [sender.sender_email for sender in self.all_senders]

        self.gridLayout = QtWidgets.QGridLayout(Send_Email_Window)
        self.gridLayout.setObjectName("gridLayout")
        self.to_label = QtWidgets.QLabel(Send_Email_Window)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.to_label.sizePolicy().hasHeightForWidth())
        self.to_label.setSizePolicy(sizePolicy)
        self.to_label.setMinimumSize(QtCore.QSize(0, 35))
        self.to_label.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.to_label.setFont(font)
        self.to_label.setStyleSheet("background-color: rgb(45, 45, 55);\n"
                                    "color: rgb(255, 255, 255);")
        self.to_label.setAlignment(QtCore.Qt.AlignCenter)
        self.to_label.setObjectName("to_label")
        self.gridLayout.addWidget(self.to_label, 2, 0, 1, 1)
        self.notes_textEdit = QtWidgets.QTextEdit(Send_Email_Window)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.notes_textEdit.sizePolicy().hasHeightForWidth())
        self.notes_textEdit.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.notes_textEdit.setFont(font)
        self.notes_textEdit.setObjectName("notes_textEdit")
        self.gridLayout.addWidget(self.notes_textEdit, 5, 0, 1, 2)
        self.send_email_toolButton = QtWidgets.QToolButton(Send_Email_Window)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.send_email_toolButton.sizePolicy().hasHeightForWidth())
        self.send_email_toolButton.setSizePolicy(sizePolicy)
        self.send_email_toolButton.setMinimumSize(QtCore.QSize(0, 40))
        self.send_email_toolButton.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.send_email_toolButton.setFont(font)
        self.send_email_toolButton.setStyleSheet("background-color: rgb(20, 177, 192);\n"
                                                 "color: rgb(255, 255, 255);")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icons/send_mail.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.send_email_toolButton.setIcon(icon)
        self.send_email_toolButton.setIconSize(QtCore.QSize(40, 40))
        self.send_email_toolButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.send_email_toolButton.setAutoRaise(False)
        self.send_email_toolButton.setObjectName("send_email_toolButton")
        self.send_email_toolButton.clicked.connect(self.send_email)
        self.gridLayout.addWidget(self.send_email_toolButton, 7, 0, 1, 1, QtCore.Qt.AlignHCenter)

        self.from_lineEdit = QtWidgets.QLineEdit(Send_Email_Window)
        self.from_lineEdit.setSizePolicy(sizePolicy)
        self.from_lineEdit.setMinimumSize(QtCore.QSize(0, 30))
        self.from_lineEdit.setObjectName("from_lineEdit")
        self.from_lineEdit.setReadOnly(True)

        self.from_combobox = QtWidgets.QComboBox(Send_Email_Window)
        self.from_combobox.setFont(font)
        # self.from_combobox.setMinimumSize(250, 35)
        self.from_combobox.addItems(self.senders)
        # self.receiver_combobox.currentIndexChanged.connect(self.check_if_machine_exist_from_combobox)
        self.from_combobox.setLineEdit(self.from_lineEdit)
        self.gridLayout.addWidget(self.from_combobox, 1, 0, 1, 1)

        self.to_lineEdit = QtWidgets.QLineEdit(Send_Email_Window)
        self.to_lineEdit.setSizePolicy(sizePolicy)
        self.to_lineEdit.setMinimumSize(QtCore.QSize(0, 30))
        self.to_lineEdit.setObjectName("to_lineEdit")
        self.to_combobox = QtWidgets.QComboBox(Send_Email_Window)
        self.to_combobox.setFont(font)
        # self.to_combobox.setMinimumSize(250, 35)
        self.to_combobox.addItems(self.receivers)
        # self.receiver_combobox.currentIndexChanged.connect(self.check_if_machine_exist_from_combobox)
        self.to_combobox.setLineEdit(self.to_lineEdit)

        self.gridLayout.addWidget(self.to_combobox, 3, 0, 1, 1)
        self.notes_label = QtWidgets.QLabel(Send_Email_Window)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.notes_label.sizePolicy().hasHeightForWidth())
        self.notes_label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(13)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.notes_label.setFont(font)
        self.notes_label.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.notes_label.setToolTip("")
        self.notes_label.setStatusTip("")
        self.notes_label.setWhatsThis("")
        self.notes_label.setAccessibleName("")
        self.notes_label.setAccessibleDescription("")
        self.notes_label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.notes_label.setStyleSheet("background-color: rgb(89, 89, 89);\n"
                                       "color: rgb(255, 255, 255);")
        self.notes_label.setLocale(QtCore.QLocale(QtCore.QLocale.Greek, QtCore.QLocale.Greece))
        self.notes_label.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.notes_label.setAlignment(QtCore.Qt.AlignCenter)
        self.notes_label.setObjectName("notes_label")
        self.gridLayout.addWidget(self.notes_label, 4, 0, 1, 2)
        self.from_label = QtWidgets.QLabel(Send_Email_Window)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.from_label.sizePolicy().hasHeightForWidth())
        self.from_label.setSizePolicy(sizePolicy)
        self.from_label.setMinimumSize(QtCore.QSize(0, 35))
        self.from_label.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.from_label.setFont(font)
        self.from_label.setToolTip("")
        self.from_label.setStatusTip("")
        self.from_label.setWhatsThis("")
        self.from_label.setAccessibleName("")
        self.from_label.setAccessibleDescription("")
        self.from_label.setStyleSheet("color: rgb(255, 255, 255);\n"
                                      "background-color: rgb(255, 170, 0);")
        self.from_label.setAlignment(QtCore.Qt.AlignCenter)
        self.from_label.setObjectName("from_label")
        self.gridLayout.addWidget(self.from_label, 0, 0, 1, 1)
        self.progressBar = QtWidgets.QProgressBar(Send_Email_Window)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.gridLayout.addWidget(self.progressBar, 6, 0, 1, 1)

        # Esc
        self.shortcut_esc = QtWidgets.QShortcut(QtGui.QKeySequence('Escape'), Send_Email_Window)
        self.shortcut_esc.activated.connect(lambda: self.close())

        self.retranslateUi(Send_Email_Window)
        QtCore.QMetaObject.connectSlotsByName(Send_Email_Window)

    def retranslateUi(self, Send_Email_Window):
        _translate = QtCore.QCoreApplication.translate
        Send_Email_Window.setWindowTitle(_translate("Send_Email_Window", "Αποστολή ηλεκτρονικού μηνύματος"))
        self.to_label.setText(_translate("Send_Email_Window", "Παραλήπτης"))
        self.send_email_toolButton.setText(_translate("Send_Email_Window", "   Αποστολή"))
        self.notes_label.setText(_translate("Send_Email_Window", "Σημειώσεις"))
        self.from_label.setText(_translate("Send_Email_Window", "Αποστολέας"))

    def send_email(self):
        if "@" not in self.to_lineEdit.text():
            self.to_lineEdit.setStyleSheet("Background-color: red; color: white;")
            return
        else:
            self.progressBar.setProperty("value", 20)
            sender_index = self.from_combobox.currentIndex()
            sender_obj = self.all_senders[sender_index]

            message = MIMEMultipart()
            date = self.data_to_send[0]

            if self.selected_calendar:  # Εν το στέλνει απο επεξεργασία κλησεις εχει calendar
                customer = self.selected_calendar.Πελάτης
                copier = self.selected_calendar.Μηχάνημα
                selected_calendar_spare_parts = get_consumables_from_service_id(self.selected_calendar.Service_ID)
                spare_parts = [
                    f"Κωδικός :{item.ΚΩΔΙΚΟΣ} --- ΠΕΡΙΓΡΑΦΗ: {item.ΠΕΡΙΓΡΑΦΗ}, --- ΤΕΜΑΧΙΑ: {item.ΤΕΜΑΧΙΑ} <br>"
                    for item in selected_calendar_spare_parts]

            elif self.selected_service_id:  # αν το στείλει απο επεξεργασία service που δεν έχει calendar
                customer = self.selected_customer
                copier = self.selected_machine
                selected_calendar_spare_parts = get_consumables_from_service_id(self.selected_service_id)
                spare_parts = [
                    f"Κωδικός :{item.ΚΩΔΙΚΟΣ} --- ΠΕΡΙΓΡΑΦΗ: {item.ΠΕΡΙΓΡΑΦΗ}, --- ΤΕΜΑΧΙΑ: {item.ΤΕΜΑΧΙΑ} <br>"
                    for item in selected_calendar_spare_parts]
            else:  # Αν το στείλει απο προσθήκη εργασίας
                customer = self.selected_customer
                copier = self.selected_machine
                spare_parts = []
            self.progressBar.setProperty("value", 40)
            message["Subject"] = "Service Book " + " " + customer + " " + copier
            message["From"] = self.from_lineEdit.text()
            message["To"] = self.to_lineEdit.text()
            purpose = self.data_to_send[1]
            technician = self.data_to_send[2]
            actions = self.data_to_send[3]
            counter = self.data_to_send[4]
            if self.files_path is not None and os.path.exists(self.files_path):
                self.files = os.listdir(self.files_path)
            else:
                self.files = "Δεν υπάρχουν αρχεία"

            urgent = self.data_to_send[5]
            phone = self.data_to_send[6]
            notes = self.data_to_send[7]
            dte = self.data_to_send[8]
            status = self.data_to_send[9]

            html = f"""\
                                        <html>
                                            <body>
            <p> <b>Ημερομηνία:  </b>  {date} <br>
                <b>Πελάτης: </b>  {customer}  <br> 
                <b>Μηχάνημα: </b>  {copier} <br>
                <b>Μετρητής:  </b>{counter} <br>
                <b>Σκοπός: </b> {purpose}   <br>
                <b>Τεχνικός : </b>  {technician} <br>
                <b>Ενέργιες:  </b>{actions} <br>
                <b>Ωρα: </b>  {urgent} <br>
                <b>Τηλέφωνο:  </b> {phone} <br>
                <b>ΔΤΕ:  </b>{dte} <br>
                <b>Κατάσταση:  </b>{status}<br> 
                <b>Ανταλλακτικά:  </b> <br>
                {spare_parts}<br>
                <b>Σημειώσεις εργασίας: </b>  {notes} <b><br>
                <b>Αρχεία: </b>   {self.files} <br>
                <b>Σημειώσεις αποστολής email: </b>  {self.notes_textEdit.toPlainText()} <b><br>
                <br>Χρήστης:  </b>{user}
                                            </body>
                                        </html>
                                        """
        if self.files != "Δεν υπάρχουν αρχεία":
            for file in self.files:
                ext = file.split('.')[-1:]
                # the attachments for the mail
                with open(os.path.join(self.files_path, file), 'rb') as file_to_send:  # Open the file as binary mode
                    attached_file = MIMEApplication(file_to_send.read(), _subtype=str(ext))
                    attached_file.add_header('content-disposition', 'attachment', filename=os.path.basename(file))
                    message.attach(attached_file)

        part2 = MIMEText(html, "html")
        # Add HTML/plain-text parts to MIMEMultipart message
        # The email client will try to render the last part first
        message.attach(part2)
        self.progressBar.setProperty("value", 50)
        try:
            session = smtplib.SMTP(sender_obj.smtp_server, sender_obj.port)  # use gmail with port
            session.starttls()  # enable security
            session.login(sender_obj.sender_email, sender_obj.password)  # login with mail_id and password
            text = message.as_string()
            session.sendmail(sender_obj.sender_email, self.to_lineEdit.text(), text)
            session.quit()
            self.progressBar.setProperty("value", 100)
            QtWidgets.QMessageBox.information(None, "Πληροφορία", f'Επιτυχία αποστολής email!')
            self.close()
        except Exception as e:
            traceback.print_exc()
            QtWidgets.QMessageBox.critical(None, "Σφάλμα", f'{e}')
            print(f'{__name__}', e)
            session.quit()

    def closeEvent(self, event):
        self.window_closed.emit()
        event.accept()
        # event.ignore()  # if you want the window to never be closed


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    Send_Email_Window = QtWidgets.QWidget()
    ui = Ui_Send_Email_Window()
    ui.setupUi(Send_Email_Window)
    Send_Email_Window.show()
    sys.exit(app.exec_())
