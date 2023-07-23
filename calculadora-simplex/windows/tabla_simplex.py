from PyQt5.QtWidgets import QApplication, QVBoxLayout, QWidget, QPushButton, QLabel, QGridLayout
from PyQt5.QtCore import Qt
import sys

class TableWidget(QWidget):
    def __init__(self, iteraciones):
        super().__init__()
        self.setMinimumSize(500, 180)
        self.index = 0
        self.iteraciones = iteraciones

        self.init_ui()
        self.show_table(0)

    def init_ui(self):
        self.layout = QVBoxLayout()

        self.iteration_label = QLabel()
        self.layout.addWidget(self.iteration_label)

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

        self.setStyleSheet("""
            QGridLayout {
                background-color: #F5F5F5;
            }
            QLabel {
                border: 1px solid #CCCCCC;
                padding: 5px;
                font-size: 14px;
            }
            QLabel#space{
                padding-bottom:20px;
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
        """)

    def next(self):
        if self.index < len(self.iteraciones) - 1:
            self.index += 1
        self.show_table(self.index)

    def prev(self):
        if self.index > 0:
            self.index -= 1
        self.show_table(self.index)

    def show_table(self, tabla_index):
        tabla = self.iteraciones[tabla_index]
        self.clear_grid()

        for i, fila in enumerate(tabla):
            for j, valor in enumerate(fila):
                label = QLabel(str(valor))
                label.setAlignment(Qt.AlignCenter)

                label.setStyleSheet("""
                    QLabel {
                        background-color: #FFFFFF;
                        color:#333;
                    }
                """)

                self.grid_layout.addWidget(label, i, j)

        self.iteration_label.setText(f"Iteración {tabla_index + 1}")

        self.grid_widget.show()

    def clear_grid(self):
        while self.grid_layout.count():
            child = self.grid_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

# if __name__ == '__main__':
#     app = QApplication(sys.argv)

#     iteraciones = [
#         [
#             [-1, -3, -2, 0, 0, 0, 0],
#             [2, 4, 1, 1, 0, 0, 6],
#             [-1, 6, 1, 0, 1, 0, 1],
#             [1, 8, 3, 0, 0, 1, 2]
#         ],
#         [
#             [-2, -3, -2, 0, 0, 0, 0],
#             [2, 6, 1, 1, 3, 0, 5],
#             [-1, 6, 2, 1, 3, 0, 1],
#             [1, 8, 3, 0, 0, 1, 2]
#         ],
#     ]

#     table_widget = TableWidget(iteraciones)
#     table_widget.show()

#     sys.exit(app.exec_())
