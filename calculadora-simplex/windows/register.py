import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from db import DatabaseManager


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

class RegisterWindow(QWidget):
    def __init__(self, login_ui):
        super().__init__()
        self.database_manager = DatabaseManager()
        self.login_ui = login_ui
        self.init_ui()     

    def init_ui(self):
        self.setWindowTitle('Calculadora Simplex - Registro')
        self.setGeometry(100, 100, 700, 500)
        self.setFixedSize(700, 500)
        title_font = self.font()
        title_font.setPointSize(24)

        self.username_label = QLabel('Nombre de usuario:')
        self.username_input = QLineEdit()
        self.password_label = QLabel('Contraseña:')
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.repeat_password_label = QLabel('Repita su contraseña:')
        self.repeat_password_input = QLineEdit()
        self.repeat_password_input.setEchoMode(QLineEdit.Password)
        self.register_button = QPushButton('Registrarse')
        self.regresar_button = QPushButton('Regresar')

        self.register_button.setCursor(Qt.PointingHandCursor)
        self.register_button.clicked.connect(self.register)

        self.regresar_button.setCursor(Qt.PointingHandCursor)
        self.regresar_button.clicked.connect(self.regresar)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        
        title_label = QLabel('Registrarse en Calculadora SIMPLEX')
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
        form_layout.addWidget(self.repeat_password_label)
        form_layout.addWidget(self.repeat_password_input)

        layout.addLayout(form_layout)
        layout.addWidget(self.register_button)
        layout.addWidget(self.regresar_button)

        self.setLayout(layout)

        # Aplicar los estilos CSS
        self.setStyleSheet(style_sheet)

    def register(self):
        name = self.username_input.text()
        password = self.password_input.text()
        repeat_password = self.repeat_password_input.text()
        message = self.database_manager.register_user(name, repeat_password, password)
        if(message == 'create'):
          self.show_message_box('Exito', 'Se a registrado el usuario')
        elif(message == 'no same'):
          self.show_message_box('Advertencia', 'Las contraseña no son iguales')
        else:
          self.show_message_box('Error', 'ERROR') 

    def show_message_box(self, title, message):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.exec_()

    def regresar(self):
      self.hide()
      self.login_ui.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    register_window = RegisterWindow()
    register_window.show()
    sys.exit(app.exec_())
