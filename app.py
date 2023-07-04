from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QPalette, QColor
from sqlite import setConnection,validate_user

app = QtWidgets.QApplication([])
cursor = setConnection()

GUI_LOGIN = uic.loadUi("ui/Login.ui")
GUI_FORM = uic.loadUi("ui/Formulario.ui")
GUI_REST = uic.loadUi("ui/Restricciones.ui")
GUI_MATRIZ = uic.loadUi("ui/Matriz.ui")

# GUI LOGIN
GUI_LOGIN.show()

# STYLES
def set_error_style(line_edit):
    palette = line_edit.palette()
    palette.setColor(QPalette.Base, QColor(255, 0, 0))  
    line_edit.setPalette(palette)

def set_text_error_style(label):
    label.setStyleSheet("color: red; font-weight: bold;")  

# ACTIONS
def login():
    name = GUI_LOGIN.textbox_user.text()
    password = GUI_LOGIN.textbox_pass.text()
    user = validate_user(cursor, name, password)
    if(user):
        GUI_LOGIN.hide()
        GUI_FORM.show()
    else:
        GUI_LOGIN.error_user.setText('Usuario incorrecto')
        GUI_LOGIN.error_password.setText('Contraseña incorrecta')
        #SET STYLES
        set_text_error_style(GUI_LOGIN.error_user)
        set_text_error_style(GUI_LOGIN.error_password)
        set_error_style(GUI_LOGIN.textbox_user)
        set_error_style(GUI_LOGIN.textbox_pass)

def register():
    pass

# ADD GUI ACTIONS
GUI_LOGIN.btn_login.clicked.connect(login)

app.exec()