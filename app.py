from PyQt5 import QtWidgets, uic

app = QtWidgets.QApplication([])

GUI_LOGIN = uic.loadUi("ui/Login.ui")
GUI_FORM = uic.loadUi("ui/Formulario.ui")
GUI_REST = uic.loadUi("ui/Restricciones.ui")
GUI_MATRIZ = uic.loadUi("ui/Matriz.ui")

# GUI LOGIN
GUI_LOGIN.show()

# ACTIONS

def login():
    name = GUI_LOGIN.textbox_user.text()
    password = GUI_LOGIN.textbox_pass.text()
    if(name == "Danny" and password == "1234"):
        GUI_LOGIN.hide()
        GUI_FORM.show()

# ADD GUI ACTIONS
GUI_LOGIN.btn_login.clicked.connect(login)

app.exec()