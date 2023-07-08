import math
from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QPalette, QColor
from sqlite import setConnection, validate_user
import actions.max as Max


app = QtWidgets.QApplication([])
cursor = setConnection()

GUI_LOGIN = uic.loadUi("ui/Login.ui")
GUI_FORM = uic.loadUi("ui/FORM.ui")

GUI_MATRIZ = uic.loadUi("ui/Matriz.ui")
GUI_SOLUTION = uic.loadUi("ui/Solution.ui")
GUI_REST = uic.loadUi("ui/Restricciones.ui")

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
    if user:
        GUI_LOGIN.hide()

        GUI_SOLUTION.show()
        tabla_simplex = [
            [-1, -3, -2, 0, 0, 0, 0],
            [2, 4, 1, 1, 0, 0, 6],
            [-1, 6, 1, 0, 1, 0, 1],
            [1, 8, 3, 0, 0, 1, 2]
        ]
        funcion_obj = [1, 3, 2]
        maximize_table(tabla_simplex, funcion_obj)
        #GUI_REST.show()
        # GUI_FORM.show()
    else:
        GUI_LOGIN.error_user.setText('Usuario incorrecto')
        GUI_LOGIN.error_password.setText('Contraseña incorrecta')
        # SET STYLES
        set_text_error_style(GUI_LOGIN.error_user)
        set_text_error_style(GUI_LOGIN.error_password)
        set_error_style(GUI_LOGIN.textbox_user)
        set_error_style(GUI_LOGIN.textbox_pass)


def register():
    pass


# ENTER DATA
def enter_data_maximize():
    vars = int(GUI_REST.vars.text())
    restrictions = int(GUI_REST.restrictions.text())
    GUI_REST.hide()
    GUI_FORM.show()
    table_widget = GUI_FORM.findChild(
        QtWidgets.QTableWidget, "tableWidget")
    layout = QtWidgets.QVBoxLayout(GUI_FORM)

    table_widget.setRowCount(restrictions + 1)
    table_widget.setColumnCount(vars + 2)  # Agregar 2 columnas adicionales

    sign_options = ["<=", ">=", "="]

    for row in range(restrictions + 1):
        for col in range(vars + 2):
            if col == vars:  
                combo_box = QtWidgets.QComboBox()
                combo_box.addItems(sign_options)
                table_widget.setCellWidget(row, col, combo_box)
            else:
                item = QtWidgets.QTableWidgetItem()
                table_widget.setItem(row, col, item)

# GET DATA

def get_table_values():
    table_widget = GUI_FORM.findChild(QtWidgets.QTableWidget, "tableWidget")
    rows = table_widget.rowCount()
    cols = table_widget.columnCount()

    first_row_values = []
    table_values = []

    for row in range(rows):
        row_values = []
        for col in range(cols):
            if col == cols - 1:  # Última columna (signos)
                combo_box = table_widget.cellWidget(row, col)
                sign = combo_box.currentText()
                row_values.append(sign)
            else:
                item = table_widget.item(row, col)
                if item is None or item.text() == '':
                    value = 0  # Establecer valor predeterminado en 0
                else:
                    value = float(item.text())
                row_values.append(value)
        if row == 0:
            first_row_values = row_values
        else:
            table_values.append(row_values)

    return first_row_values, table_values



# MAXIMIZE

current_table = 0


def set_data(data):
    table_widget = GUI_SOLUTION.findChild(
        QtWidgets.QTableWidget, "tableWidget")

    table_widget.setRowCount(len(data[0]))
    table_widget.setColumnCount(len(data)+1)

    for i, row in enumerate(data[current_table]):
        for j, value in enumerate(row):
            item = QtWidgets.QTableWidgetItem(str(math.floor(value)))
            table_widget.setItem(i, j, item)


def maximize_table(table, function_obj):
    table_data = Max.calc_table(table, function_obj)
    set_data(table_data["solution_tables"])
    layout = QtWidgets.QVBoxLayout(GUI_SOLUTION)
    GUI_SOLUTION.result.setText(",\n".join(table_data["optimal_values"]))


    previus_button = GUI_SOLUTION.previus_button
    next_button = GUI_SOLUTION.next_button

    if current_table == 0:
        previus_button.hide()
        #label.setVisible(False)

    if current_table >= len(table_data["solution_tables"]):
        next_button.hide()


def decrement_current_table():
    global current_table
    current_table -= 1
    print("Valor de current_table decrementado:", current_table)


def increment_current_table():
    global current_table
    current_table += 1
    print("Valor de current_table incrementado:", current_table)


def connect_signals():
    GUI_LOGIN.btn_login.clicked.connect(login)
    GUI_SOLUTION.previus_button.clicked.connect(decrement_current_table)
    GUI_SOLUTION.next_button.clicked.connect(increment_current_table)
    GUI_REST.btn_maximize.clicked.connect(enter_data_maximize)


# ADD GUI ACTIONS
connect_signals()

app.exec()
