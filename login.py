import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
import apiW3
import dashbord
class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.doc = apiW3.CorporateStorage
        self.setWindowTitle("Вход в систему")
        self.setGeometry(100, 100, 300, 200)

        layout = QVBoxLayout()

        self.label = QLabel("Для входа в систему введите данные:")
        layout.addWidget(self.label)

        self.login_input = QLineEdit(self)
        self.login_input.setPlaceholderText("Например example.ru")
        layout.addWidget(self.login_input)

        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("Введите ваш пароль")
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)

        self.submit_button = QPushButton("Отправить", self)
        self.submit_button.clicked.connect(self.login)
        layout.addWidget(self.submit_button)

        self.setLayout(layout)

    def login(self):
        login = self.login_input.text()
        password = self.password_input.text()
        if self.doc.Authorisation(login, password):
            QMessageBox.information(self, "Успех", "Успешный вход в систему!")
            w = dashbord.Dashboard
            w.show()
            self.close()  # Закрывает текущее окно


        else:
            QMessageBox.warning(self, "Ошибка", "Введите корректные данные!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec_())