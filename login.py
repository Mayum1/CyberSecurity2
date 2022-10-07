import sys
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QHBoxLayout, QVBoxLayout, QGridLayout, QPushButton, QLabel
import psycopg2
import os

conn = psycopg2.connect(database="cs2", user="postgres", password="123", host="localhost", port="5432")
cursor = conn.cursor()


class Login(QWidget):

    def _sign_in(self):
        login = self.login_input.text()
        password = self.pass_input.text()
        cursor.execute("SELECT * FROM service.users WHERE login=%s AND password=%s;", (str(login), str(password)))
        records = list(cursor.fetchall())
        if len(records):
            password = str(int(password) + 5)
            while len(password) < 8:
                password = '0' + password

            cursor.execute('UPDATE service.users SET password=%s WHERE login=%s;', (str(password), str(login)))
            conn.commit()

            os.startfile("cyber_security.pdf")
        else:
            self.error.setText('Неправильный логин или пароль!')

    def _sign_up(self):
        widget.setCurrentIndex(1)

    def __init__(self):
        super(Login, self).__init__()

        self.vbox = QVBoxLayout(self)
        self.hbox_login_text = QHBoxLayout()
        self.hbox_login_input = QHBoxLayout()
        self.hbox_pass_text = QHBoxLayout()
        self.hbox_pass_input = QHBoxLayout()
        self.hbox_error = QHBoxLayout()
        self.hbox_sign_in = QHBoxLayout()
        self.hbox_sign_up = QHBoxLayout()

        self.vbox.addLayout(self.hbox_login_text)
        self.vbox.addLayout(self.hbox_login_input)
        self.vbox.addLayout(self.hbox_pass_text)
        self.vbox.addLayout(self.hbox_pass_input)
        self.vbox.addLayout(self.hbox_error)
        self.vbox.addLayout(self.hbox_sign_in)
        self.vbox.addLayout(self.hbox_sign_up)

        self.login_text = QLabel('Имя пользователя', self)
        self.hbox_login_text.addWidget(self.login_text)

        self.login_input = QLineEdit(self)
        self.hbox_login_input.addWidget(self.login_input)

        self.pass_text = QLabel('Пароль', self)
        self.hbox_pass_text.addWidget(self.pass_text)

        self.pass_input = QLineEdit(self)
        self.hbox_pass_input.addWidget(self.pass_input)

        self.error = QLabel('', self)
        self.hbox_error.addWidget(self.error)

        self.sign_in = QPushButton("Войти", self)
        self.hbox_sign_in.addWidget(self.sign_in)

        self.sign_up = QPushButton("Регистрация", self)
        self.hbox_sign_up.addWidget(self.sign_up)

        self.sign_in.clicked.connect(self._sign_in)
        self.sign_up.clicked.connect(self._sign_up)


class SignUp(QWidget):

    def _save(self):
        login = self.login_line.text()
        password = self.password_line.text()
        name = self.name_line.text()
        birthday = self.birthday_line.text()
        city = self.city_line.text()
        phone = self.phone_line.text()
        cursor.execute('SELECT * FROM service.users WHERE login = %s', [str(login)])
        records = list(cursor.fetchall())
        if (login == '') or (password == '') or (name == '') or (birthday == '') or (city == '') or (phone == ''):
            self.error.setText("Пожалуйста, заполните все поля!")
        elif len(records):
            self.error.setText("Имя пользователя занято!")
        elif not (password.isdigit()) or (len(password) != 8):
            self.error.setText("Пароль должен состоять из 8 цифр!")
        else:
            cursor.execute('INSERT INTO service.users (login, password, full_name, birthday, city, phone) VALUES (%s, %s, %s, %s, %s, %s);', (str(login), str(password), str(name), str(birthday), str(city), str(phone)))
            conn.commit()
            widget.setCurrentIndex(0)

    def __init__(self):
        super(SignUp, self).__init__()

        self.lo = QGridLayout()
        self.setLayout(self.lo)

        self.login_label = QLabel('Имя пользователя', self)
        self.login_label.setAlignment(Qt.AlignRight)
        self.lo.addWidget(self.login_label, 0, 0)
        self.login_line = QLineEdit(self)
        self.lo.addWidget(self.login_line, 0, 1)

        self.password_label = QLabel('Пароль', self)
        self.password_label.setAlignment(Qt.AlignRight)
        self.lo.addWidget(self.password_label, 1, 0)
        self.password_line = QLineEdit(self)
        self.lo.addWidget(self.password_line, 1, 1)

        self.name_label = QLabel('ФИО', self)
        self.name_label.setAlignment(Qt.AlignRight)
        self.lo.addWidget(self.name_label, 2, 0)
        self.name_line = QLineEdit(self)
        self.lo.addWidget(self.name_line, 2, 1)

        self.birthday_label = QLabel('Дата рождения', self)
        self.birthday_label.setAlignment(Qt.AlignRight)
        self.lo.addWidget(self.birthday_label, 3, 0)
        self.birthday_line = QLineEdit(self)
        self.lo.addWidget(self.birthday_line, 3, 1)

        self.city_label = QLabel('Город рождения', self)
        self.city_label.setAlignment(Qt.AlignRight)
        self.lo.addWidget(self.city_label, 4, 0)
        self.city_line = QLineEdit(self)
        self.lo.addWidget(self.city_line, 4, 1)

        self.phone_label = QLabel('Номер телефона', self)
        self.phone_label.setAlignment(Qt.AlignRight)
        self.lo.addWidget(self.phone_label, 5, 0)
        self.phone_line = QLineEdit(self)
        self.lo.addWidget(self.phone_line, 5, 1)

        self.error = QLabel("", self)
        self.lo.addWidget(self.error, 6, 0, 1, 2)

        self.save_button = QPushButton("Сохранить", self)
        self.lo.addWidget(self.save_button, 7, 0, 2, 2)

        self.save_button.clicked.connect(self._save)


app = QApplication(sys.argv)
widget = QtWidgets.QStackedWidget()
main_win = Login()
signup_win = SignUp()
widget.addWidget(main_win)
widget.addWidget(signup_win)
widget.setFixedHeight(200)
widget.setFixedWidth(250)
widget.show()
app.exec_()
