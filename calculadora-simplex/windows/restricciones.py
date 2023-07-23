from PyQt5.QtWidgets import QApplication, QVBoxLayout, QWidget, QPushButton, QLabel, QLineEdit, QComboBox, QGridLayout
from PyQt5.QtCore import Qt
import sys
from windows.restriciones_tabla import TablaRestricciones

style_sheet = """
            QGridLayout {
                background-color: #F5F5F5;
            }
            QLineEdit, QComboBox {
                background-color: #F5F5F5;
                padding: 5px;
                border: 1px solid #CCCCCC;
                color: #000000;
                font-size: 14px;
            }
            QLabel {
                font-size: 14px;
                font-weight: bold;
            }
            QLabel#space{
              padding-bottom:20px
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px 20px;
                font-size: 16px;
            }
            QPushButton#back{
            background-color: #0000ff;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """


class Table(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tabla Inicial")
        self.setGeometry(100, 100, 700, 500)
        self.setFixedSize(700, 500)
        self.setStyleSheet(style_sheet)
        self.init_ui()

    def init_ui(self):
        self.rows_label = QLabel("Número de variables:")
        self.rows_input = QLineEdit()

        self.columns_label = QLabel("Número de restricciones:")
        self.columns_input = QLineEdit()

        self.space = QLabel("")
        self.space.setObjectName('space')

        self.crear_button = QPushButton('Crear tabla')
        self.crear_button.setCursor(Qt.PointingHandCursor)
        self.crear_button.clicked.connect(self.crear_tabla)


        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        title_label = QLabel('Crear Tabla')
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        layout.addWidget(self.rows_label)
        layout.addWidget(self.rows_input)
        layout.addWidget(self.columns_label)
        layout.addWidget(self.columns_input)
        layout.addWidget(self.space)
        layout.addWidget(self.crear_button)

        self.grid_layout = QGridLayout()
        layout.addLayout(self.grid_layout)

        self.setLayout(layout)

    def crear_tabla(self):
        if (self.rows_input.text() != '' or self.columns_input.text() != ''):
            try:
                filas = int(self.rows_input.text())
                columnas = int(self.columns_input.text())
                self.tabla_restriciones = TablaRestricciones(self.regresar, filas, columnas)
                self.hide()
                self.tabla_restriciones.show()
            except:
                pass
    def regresar(self):
        self.tabla_restriciones.hide()
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Table()
    window.show()
    sys.exit(app.exec_())
