from PySide6.QtWidgets import QDialog, QLineEdit, QPushButton, QVBoxLayout, QLabel

from models import User
from session import session


class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Авторизация")

        self.layout = QVBoxLayout()

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Введите логин")
        self.layout.addWidget(self.username_input)

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setPlaceholderText("Введите пароль")
        self.layout.addWidget(self.password_input)

        self.login_button = QPushButton("Войти")
        self.login_button.clicked.connect(self.authenticate)
        self.layout.addWidget(self.login_button)

        self.error_label = QLabel("")
        self.layout.addWidget(self.error_label)

        self.setLayout(self.layout)

    def authenticate(self):
        username = self.username_input.text()
        password = self.password_input.text()

        user = session.query(User).filter_by(username=username, password=password).first()
        if user:
            self.accept()
        else:
            self.error_label.setText("Неверный логин или пароль")

if __name__ == '__main__':
    print("Auth")