import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, QLineEdit,
                             QComboBox, QGridLayout, QVBoxLayout, QDateEdit, QDialog,
                             QMessageBox)
from PyQt5.QtCore import Qt, QDate


class AddClientDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Добавить клиента")

        layout = QGridLayout()

        layout.addWidget(QLabel("Уникальный идентификатор:"), 0, 0)
        self.id_edit = QLineEdit()
        layout.addWidget(self.id_edit, 0, 1)

        layout.addWidget(QLabel("Тип клиента:"), 1, 0)
        self.type_combo = QComboBox()
        self.type_combo.addItems(["Физическое лицо", "Юридическое лицо"])
        layout.addWidget(self.type_combo, 1, 1)

        layout.addWidget(QLabel("Имя или название компании:"), 2, 0)
        self.name_edit = QLineEdit()
        layout.addWidget(self.name_edit, 2, 1)

        layout.addWidget(QLabel("Дата рождения:"), 3, 0)
        self.birthdate_edit = QDateEdit(QDate.currentDate())
        self.birthdate_edit.setCalendarPopup(True)
        layout.addWidget(self.birthdate_edit, 3, 1)

        layout.addWidget(QLabel("Дата регистрации:"), 4, 0)
        self.registration_edit = QDateEdit(QDate.currentDate())
        self.registration_edit.setCalendarPopup(True)
        layout.addWidget(self.registration_edit, 4, 1)

        layout.addWidget(QLabel("ИНН:"), 5, 0)
        self.tin_edit = QLineEdit()
        layout.addWidget(self.tin_edit, 5, 1)

        layout.addWidget(QLabel("Контактная информация:"), 6, 0)
        self.contact_edit = QLineEdit()
        layout.addWidget(self.contact_edit, 6, 1)

        button_box = QHBoxLayout()
        add_button = QPushButton("Добавить")
        add_button.clicked.connect(self.accept)  # Принимает данные и закрывает диалог
        cancel_button = QPushButton("Отмена")
        cancel_button.clicked.connect(self.reject) # Закрывает диалог без сохранения данных
        button_box.addWidget(add_button)
        button_box.addWidget(cancel_button)

        main_layout = QVBoxLayout()
        main_layout.addLayout(layout)
        main_layout.addLayout(button_box)
        self.setLayout(main_layout)

    def get_data(self):
        return {
            "id": self.id_edit.text(),
            "type": self.type_combo.currentIndex() + 1,
            "name": self.name_edit.text(),
            "birthDate": self.birthdate_edit.date().toString("yyyy-MM-dd"),
            "registrationDate": self.registration_edit.date().toString("yyyy-MM-dd"),
            "tin": self.tin_edit.text(),
            "contactInfo": self.contact_edit.text()
        }

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Панель управления")
        layout = QGridLayout()

        # Кнопка "Добавить клиента"
        add_client_button = QPushButton("Добавить клиента")
        add_client_button.clicked.connect(self.show_add_client_dialog)
        layout.addWidget(add_client_button, 0, 0)


        self.setLayout(layout)

    def show_add_client_dialog(self):
        dialog = AddClientDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_data()
            # Здесь вы должны отправить данные `data` на сервер (например, с помощью requests)
            QMessageBox.information(self, "Успех", "Клиент добавлен!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())