import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from windows.register import RegisterWindow
from db import DatabaseManager
from windows.restricciones import Table

style_sheet = """
            QWidget { 
              background-color: white; 
            }
            QLabel {
                color: #333;
            }
            QLineEdit {
                color:#333;
                border: 2px solid #ccc;
                border-radius: 5px;
                padding: 5px;
                font-size: 16px;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px 20px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QWidget#login_widget {
                background-color: #f2f2f2;
            }
        """


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.database_manager = DatabaseManager()
        self.register_ui = RegisterWindow(self)
        self.restriciones_ui = Table()

    def init_ui(self):
        self.setWindowTitle('Calculadora Simplex')
        self.setGeometry(100, 100, 700, 500)
        self.setFixedSize(700, 500)
        title_font = self.font()
        title_font.setPointSize(24)

        self.username_label = QLabel('Usuario:')
        self.username_input = QLineEdit()
        self.password_label = QLabel('Contraseña:')
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.login_button = QPushButton('Iniciar sesión')
        self.register_button = QPushButton('Registrarte')

        self.login_button.setCursor(Qt.PointingHandCursor)
        self.login_button.clicked.connect(self.login)

        self.register_button.setCursor(Qt.PointingHandCursor)
        self.register_button.clicked.connect(self.register)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        title_label = QLabel('Calculadora SIMPLEX')
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(title_font)
        layout.addWidget(title_label)

        # Logo personalizado
        logo_label = QLabel(self)
        pixmap = QPixmap('../ucacue.png')
        #logo_label.setPixmap(pixmap.scaledToWidth(100))
        logo_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(logo_label)

        form_layout = QVBoxLayout()
        form_layout.addWidget(self.username_label)
        form_layout.addWidget(self.username_input)
        form_layout.addWidget(self.password_label)
        form_layout.addWidget(self.password_input)

        layout.addLayout(form_layout)
        layout.addWidget(self.login_button)
        layout.addWidget(self.register_button)

        self.setLayout(layout)

        # Aplicar los estilos CSS
        self.setStyleSheet(style_sheet)

    def login(self):
        name = self.username_input.text()
        password = self.password_input.text()
        user = self.database_manager.validate_user( name, password)
        if (user):
            self.show_message_box('Success', 'Crendenciales Correctas')
            self.hide()
            self.restriciones_ui.show()
        else:
            self.show_message_box('Error', 'Crendenciales Incorrectas')

    def show_message_box(self, title, message):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.exec_()
    
    def register(self):
        self.hide()
        self.register_ui.show()

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     login_window = LoginWindow()
#     login_window.show()
#     sys.exit(app.exec_())
