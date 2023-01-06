from PyQt5 import QtCore, QtGui, QtWidgets
import hashlib
import psycopg2
from config import config
import re
from main import Ui_MainWindow
from iforgot import Ui_IForgot

class LoginWindow(object):

    loggedSignal = QtCore.pyqtSignal()

    def messageBox(self, title, icon, text, infoText="", detailText=""):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(icon)
        msg.setText(text)
        msg.setInformativeText(infoText)
        msg.setWindowTitle(title)
        msg.setDetailedText(detailText)
        msg.exec_()

    def checkLoginData(self, email, haslo):
        conn = None
        try:
            params = config()                       # wczytujemy paramtery połaczenia z bazą
            conn = psycopg2.connect(**params)       # łączenie z bazą
            cur = conn.cursor()                     # tworzenie kursora do bazy
            query = f"SELECT haslo FROM uzytkownicy WHERE email = \'{email}\'" # query
            cur.execute(query)
            result = cur.fetchone()[0]
        except (Exception, psycopg2.DatabaseError) as err:
            print(f"Błąd połączenia z bazą: {err}")
            return False
        finally:
            if conn is not None:
                conn.close()                        # zamknięcie konektora do bazy
        
        if result == haslo:
            return True

    def login(self):

        email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

        email = self.lineEdit.text()
        haslo = self.lineEdit_2.text()
        if len(email) == 0 or len(haslo) == 0:
            self.messageBox("Logowanie nie powiodło się", QtWidgets.QMessageBox.Warning, "Wpisz adres e-mail i hasło.")
        elif not re.fullmatch(email_regex, email):
            self.messageBox("Logowanie nie powiodło się", QtWidgets.QMessageBox.Warning, "Niewłaściwy email. Adres musi zawierać znaki @ i .")
        else:
            haslo_md5 = hashlib.md5(haslo.encode('utf-8')).hexdigest()
            if(self.checkLoginData(email, haslo_md5)):
                self.messageBox("Logowanie powiodło się!", QtWidgets.QMessageBox.Information, "Zostałeś zalogowany.")
                global Form
                Form.close()
                Ui_MainWindow.show(self)
            else:
                self.messageBox("Logowanie nie powiodło się", QtWidgets.QMessageBox.Warning, "Adres e-mail lub hasło jest nieprawidłowe.")
    
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(589, 358)
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(240, 20, 341, 61))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(24)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setGeometry(QtCore.QRect(0, 70, 591, 21))
        self.label_4.setObjectName("label_4")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(10, 10, 71, 71))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("ui/../login.png"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.layoutWidget = QtWidgets.QWidget(Form)
        self.layoutWidget.setGeometry(QtCore.QRect(170, 90, 251, 241))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_3 = QtWidgets.QLabel(self.layoutWidget)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.lineEdit = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEdit.setObjectName("lineEdit")
        self.verticalLayout.addWidget(self.lineEdit)
        self.label_5 = QtWidgets.QLabel(self.layoutWidget)
        self.label_5.setObjectName("label_5")
        self.verticalLayout.addWidget(self.label_5)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.verticalLayout.addWidget(self.lineEdit_2)
        self.pushButton = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.pushButton)
        self.pushButton_2 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.verticalLayout.addWidget(self.pushButton_2)

        # Mój kod

        self.pushButton.clicked.connect(self.login)
        self.pushButton_2.clicked.connect(Ui_IForgot)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Logowanie"))
        self.label_2.setText(_translate("Form", "Dziennik - Logowanie"))
        self.label_4.setText(_translate("Form", "_________________________________________________________________________________________________"))
        self.label_3.setText(_translate("Form", "Adres e-mail"))
        self.label_5.setText(_translate("Form", "Hasło"))
        self.pushButton.setText(_translate("Form", "Zaloguj"))
        self.pushButton_2.setText(_translate("Form", "Zapomniałeś hasła?"))