from PyQt5.QtWidgets import QGridLayout, QApplication, QVBoxLayout, QWidget, QPushButton, QLabel, QTableWidget, QTableWidgetItem, QHeaderView
from PyQt5.QtCore import Qt
import sys
import numpy as np

class SimplexTableWindow(QWidget):
    def __init__(self, iterations):
        super().__init__()
        self.setMinimumSize(600, 400)
        self.index = 0
        self.iterations = iterations

        self.init_ui()
        self.show_table(0)

    def init_ui(self):
        self.layout = QVBoxLayout()

        self.iteration_label = QLabel()
        self.layout.addWidget(self.iteration_label)

        self.table_widget = QTableWidget(self)
        self.layout.addWidget(self.table_widget)

        self.prev_button = QPushButton('Anterior')
        self.prev_button.clicked.connect(lambda: self.prev())
        self.layout.addWidget(self.prev_button)

        self.next_button = QPushButton('Siguiente')
        self.next_button.clicked.connect(lambda: self.next())
        self.layout.addWidget(self.next_button)

        self.setLayout(self.layout)

        self.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: bold;
            }
            QTableWidget {
                background-color: #FFFFFF;
                border: 1px solid #CCCCCC;
            }
            QHeaderView::section {
                background-color: #F5F5F5;
                border: 1px solid #CCCCCC;
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
        """)

    def next(self):
        if self.index < len(self.iterations) - 1:
            self.index += 1
        self.show_table(self.index)

    def prev(self):
        if self.index > 0:
            self.index -= 1
        self.show_table(self.index)

    def show_table(self, tabla_index):
        tabla = self.iterations[tabla_index]
        num_rows = len(tabla)
        num_cols = len(tabla[0])
        self.table_widget.clear()
        self.table_widget.setRowCount(num_rows)
        self.table_widget.setColumnCount(num_cols)

        for i in range(num_rows):
            for j in range(num_cols):
                item = QTableWidgetItem(str(np.round(tabla[i][j], 2)))
                item.setTextAlignment(Qt.AlignCenter)
                self.table_widget.setItem(i, j, item)

        self.table_widget.setHorizontalHeaderLabels([f"x{i}" for i in range(num_cols)])
        self.table_widget.setVerticalHeaderLabels([f"Row {i}" for i in range(num_rows)])
        self.table_widget.resizeColumnsToContents()
        self.iteration_label.setText(f"Iteración {tabla_index + 1}")

if __name__ == '__main__':
    iterations = [[np.array([[ 498.5       ,    0.        ,  198.5       ,    0.        ,
        -199.5       , -100.        ,    0.        ,  600.5       ],
       [   2.66666667,    0.        ,    0.33333333,    1.        ,
          -0.66666667,    0.        ,    0.        ,    5.33333333],
       [  -0.16666667,    1.        ,    0.16666667,    0.        ,
           0.16666667,   -0.        ,    0.        ,    0.16666667],
       [   2.33333333,    0.        ,    1.66666667,    0.        ,
          -1.33333333,   -1.        ,    1.        ,    0.66666667]])], [np.array([[   0.        ,    0.        , -157.57142857,    0.        ,
          85.35714286,  113.64285714, -213.64285714,  458.07142857],
       [   0.        ,    0.        ,   -1.57142857,    1.        ,
           0.85714286,    1.14285714,   -1.14285714,    4.57142857],
       [   0.        ,    1.        ,    0.28571429,    0.        ,
           0.07142857,   -0.07142857,    0.07142857,    0.21428571],
       [   1.        ,    0.        ,    0.71428571,    0.        ,
          -0.57142857,   -0.42857143,    0.42857143,    0.28571429]])], [np.array([[   0.    ,    0.    ,   -1.3125,  -99.4375,    0.125 ,    0.    ,
        -100.    ,    3.5   ],
       [   0.    ,    0.    ,   -1.375 ,    0.875 ,    0.75  ,    1.    ,
          -1.    ,    4.    ],
       [   0.    ,    1.    ,    0.1875,    0.0625,    0.125 ,    0.    ,
           0.    ,    0.5   ],
       [   1.    ,    0.    ,    0.125 ,    0.375 ,   -0.25  ,    0.    ,
           0.    ,    2.    ]])], [np.array([[   0. ,   -1. ,   -1.5,  -99.5,    0. ,    0. , -100. ,    3. ],
       [   0. ,   -6. ,   -2.5,    0.5,    0. ,    1. ,   -1. ,    1. ],
       [   0. ,    8. ,    1.5,    0.5,    1. ,    0. ,    0. ,    4. ],
       [   1. ,    2. ,    0.5,    0.5,    0. ,    0. ,    0. ,    3. ]])]]
    app = QApplication(sys.argv)
    window = SimplexTableWindow(iterations)
    window.show()
    sys.exit(app.exec_())
