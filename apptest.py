

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout
from PyQt5 import uic
from PyQt5.QtGui import QPalette, QColor
from sqlite import setConnection, validate_user
from widgets.Table import Table
import sys  


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.cursor = setConnection()
        self.setWindowTitle("Calculadora SIMLEX")
        self.resize(600, 180)
        
        # Cargar Vistas
        self.GUI_TABLE = uic.loadUi("./ui/BaseLayout.ui")
        self.GUI_LOGIN = uic.loadUi("ui/Login.ui")

        self.GUI_LOGIN.show()

        self.set_actions()

    def login(self):
        name = self.GUI_LOGIN.textbox_user.text()
        password = self.GUI_LOGIN.textbox_pass.text()
        user = validate_user(self.cursor, name, password)
        if user:
            self.GUI_LOGIN.hide()

              # Obtener Widget Custom
            self.table_widget = Table()
            layout = QVBoxLayout()
            layout.addWidget(self.table_widget)
            self.GUI_TABLE.setLayout(layout)
            self.GUI_TABLE.show()
            # self.GUI_SOLUTION.show()

            # tabla_simplex = [
            #     [-1, -3, -2, 0, 0, 0, 0],
            #     [2, 4, 1, 1, 0, 0, 6],
            #     [-1, 6, 1, 0, 1, 0, 1],
            #     [1, 8, 3, 0, 0, 1, 2]
            # ]
            # funcion_obj = [1, 3, 2]
            # self.maximize_table(tabla_simplex, funcion_obj)
        else:
            self.GUI_LOGIN.error_user.setText('Usuario incorrecto')
            self.GUI_LOGIN.error_password.setText('Contraseña incorrecta')
            # SET STYLES
            self.set_text_error_style(self.GUI_LOGIN.error_user)
            self.set_text_error_style(self.GUI_LOGIN.error_password)

    def set_error_style(self, line_edit):
      palette = line_edit.palette()
      palette.setColor(QPalette.Base, QColor(255, 0, 0))
      line_edit.setPalette(palette)

    def set_text_error_style(self, label):
        label.setStyleSheet("color: red; font-weight: bold;")      


    def set_actions(self):
        self.GUI_LOGIN.btn_login.clicked.connect(self.login)

        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())