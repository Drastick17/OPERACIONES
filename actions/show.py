import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QGridLayout, QVBoxLayout, QPushButton


class MyWidget(QWidget):
    def __init__(self):
        super().__init__()

        # Arreglo de tablas
        self.arregloTablas = [
            [[1, 2, 3], [4, 5, 6]],
            [[7, 8, 9], [10, 11, 12]],
            [[13, 14, 15], [16, 17, 18]]
        ]

        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout()

        self.toggle_button1 = QPushButton('Mostrar tabla 1')
        self.toggle_button1.clicked.connect(lambda: self.show_grid(0))
        self.layout.addWidget(self.toggle_button1)

        self.toggle_button2 = QPushButton('Mostrar tabla 2')
        self.toggle_button2.clicked.connect(lambda: self.show_grid(1))
        self.layout.addWidget(self.toggle_button2)

        self.grid_widget = QWidget()
        self.grid_layout = QGridLayout(self.grid_widget)
        self.layout.addWidget(self.grid_widget)

        self.setLayout(self.layout)

    def show_grid(self, tabla_index):
        tabla = self.arregloTablas[tabla_index]
        self.clear_grid()

        for i, fila in enumerate(tabla):
            for j, valor in enumerate(fila):
                line_edit = QLineEdit(str(valor))
                self.grid_layout.addWidget(line_edit, i, j)

        self.grid_widget.show()

    def clear_grid(self):
        while self.grid_layout.count():
            child = self.grid_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = MyWidget()
    widget.show()
    sys.exit(app.exec_())
