import math
from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QPalette, QColor
from sqlite import setConnection, validate_user
import actions.max as Max
import widgets.Table as Table


class Main:
    def __init__(self):
        self.app = QtWidgets.QApplication([])
        self.cursor = setConnection()
        self.GUI_LOGIN = uic.loadUi("ui/Login.ui")
        # self.GUI_FORM = uic.loadUi("ui/FORM.ui")
        # self.GUI_MATRIZ = uic.loadUi("ui/Matriz.ui")
        # self.GUI_SOLUTION = uic.loadUi("ui/Solution.ui")
        self.current_table = 0
        self.Maximize = Max.MaxSimplex()

        # GUI LOGIN
        self.GUI_LOGIN.show()

        # ADD GUI ACTIONS
        self.connect_signals()

    def set_error_style(self, line_edit):
        palette = line_edit.palette()
        palette.setColor(QPalette.Base, QColor(255, 0, 0))
        line_edit.setPalette(palette)

    def set_text_error_style(self, label):
        label.setStyleSheet("color: red; font-weight: bold;")

    def connect_signals(self):
        self.GUI_LOGIN.btn_login.clicked.connect(self.login)
        # self.GUI_SOLUTION.previus_button.clicked.connect(
        #     self.decrement_current_table)
        # self.GUI_SOLUTION.next_button.clicked.connect(
        #     self.increment_current_table)
        # self.GUI_REST.btn_maximize.clicked.connect(self.enter_data_maximize)
        # self.GUI_FORM.btn_calc.clicked.connect(self.get_table_values)

    def login(self):
        name = self.GUI_LOGIN.textbox_user.text()
        password = self.GUI_LOGIN.textbox_pass.text()
        user = validate_user(self.cursor, name, password)
        if user:
            self.GUI_LOGIN.hide()
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

    def enter_data_maximize(self):
        vars = int(self.GUI_REST.vars.text())
        restrictions = int(self.GUI_REST.restrictions.text())
        self.GUI_REST.hide()
        self.GUI_FORM.show()
        table_widget = self.GUI_FORM.findChild(
            QtWidgets.QTableWidget, "tableWidget")
        layout = QtWidgets.QVBoxLayout(self.GUI_FORM)

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

    def get_table_values(self):
        table_widget = self.GUI_FORM.findChild(
            QtWidgets.QTableWidget, "tableWidget")
        rows = table_widget.rowCount()
        cols = table_widget.columnCount()

        first_row_data = []
        table_data = []

        for row in range(rows):
            row_data = []
            for col in range(cols):
                if col == cols - 1:
                    cell_widget = table_widget.cellWidget(row, col)
                    if isinstance(cell_widget, QtWidgets.QComboBox):
                        sign = cell_widget.currentText()
                        value_item = table_widget.item(row, col - 1)
                        if value_item is None or value_item.text() == '':
                            value = 0
                        else:
                            value = float(value_item.text())
                        row_data.append(sign)
                        row_data.append(value)
                    else:
                        row_data.append("")
                        row_data.append(0)
                else:
                    item = table_widget.item(row, col)
                    if item is None or item.text() == '':
                        value = 0
                    else:
                        value = float(item.text())
                    row_data.append(value)
            if row == 0:
                first_row_data = row_data
            else:
                table_data.append(row_data)

        print(first_row_data, table_data)

    def set_data(self, data):
        table_widget = self.GUI_SOLUTION.findChild(
            QtWidgets.QTableWidget, "tableWidget")
        table_widget.setRowCount(len(data[0]))
        table_widget.setColumnCount(len(data) + 1)

        for i, row in enumerate(data[self.current_table]):
            for j, value in enumerate(row):
                item = QtWidgets.QTableWidgetItem(str(math.floor(value)))
                table_widget.setItem(i, j, item)

    def maximize_table(self, table, function_obj):
        table_data = self.Maximize.calc_fun_obj(table, function_obj)
        self.set_data(self.Maximize.iterations)
        # layout = QtWidgets.QVBoxLayout(self.GUI_SOLUTION)
        self.GUI_SOLUTION.result.setText(
            ",\n".join(table_data["optimal_values"]))

        previus_button = self.GUI_SOLUTION.previus_button
        next_button = self.GUI_SOLUTION.next_button

        if self.current_table == 0:
            previus_button.hide()

        if self.current_table >= len(table_data["solution_tables"]):
            next_button.hide()

    def decrement_current_table(self):
        self.current_table -= 1
        print("Valor de current_table decrementado:", self.current_table)

    def increment_current_table(self):
        self.current_table += 1
        print("Valor de current_table incrementado:", self.current_table)

    def run(self):
        self.app.exec()


app = Main()
app.run()
