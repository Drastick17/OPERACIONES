from PyQt5.QtWidgets import QApplication, QVBoxLayout, QWidget, QPushButton, QLineEdit, QGridLayout
from PyQt5.QtCore import Qt
import sys
import time


class TableWidget(QWidget):
    def __init__(self, iteraciones):
        super().__init__()
        self.setMinimumSize(500, 180)
        self.index = 0
        print(iteraciones)
        self.iteraciones = iteraciones

        self.init_ui()
        self.show_grid(0)

    def init_ui(self):
        self.layout = QVBoxLayout()

        self.grid_widget = QWidget()
        self.grid_layout = QGridLayout(self.grid_widget)
        self.layout.addWidget(self.grid_widget)

        self.prev_button = QPushButton('Anterior')
        self.prev_button.clicked.connect(lambda: self.prev())
        self.layout.addWidget(self.prev_button)

        self.next_button = QPushButton('Siguiente')
        self.next_button.clicked.connect(lambda: self.next())
        self.layout.addWidget(self.next_button)

        self.setLayout(self.layout)

    def next(self):
        if self.index < len(self.iteraciones) - 1:
            self.index += 1
        self.show_grid(self.index)

    def prev(self):
        if self.index > 0:
            self.index -= 1
        self.show_grid(self.index)

    def show_grid(self, tabla_index):
        tablas = self.recuperar_iteraciones()
        tabla = tablas[tabla_index]
        self.clear_grid()
        
        for i, fila in enumerate(tabla):
            print(fila)
            for j, valor in enumerate(fila):
                print(valor)
                line_edit = QLineEdit(str(valor))
                self.grid_layout.addWidget(line_edit, i, j)

        self.grid_widget.show()

    def clear_grid(self):
        while self.grid_layout.count():
            child = self.grid_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def recuperar_iteraciones(self):
        return self.iteraciones

if __name__ == '__main__':
    app = QApplication(sys.argv)

    iteraciones = [
        [
            [-1, -3, -2, 0, 0, 0, 0],
            [2, 4, 1, 1, 0, 0, 6],
            [-1, 6, 1, 0, 1, 0, 1],
            [1, 8, 3, 0, 0, 1, 2]
        ],
        [
            [-2, -3, -2, 0, 0, 0, 0],
            [2, 6, 1, 1, 3, 0, 5],
            [-1, 6, 2, 1, 3, 0, 1],
            [1, 8, 3, 0, 0, 1, 2]
        ],
    ]

    table_widget = TableWidget(iteraciones)
    table_widget.show()

    sys.exit(app.exec_())
