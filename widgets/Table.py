from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QLineEdit, QComboBox, QGridLayout
from PyQt5.QtCore import Qt
import sys
from actions.max import Maximizacion
from widgets.SimplexTable import TableWidget

class Table(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tabla Inicial")
        self.setMinimumSize(500, 180)
        self.init_ui()

    def init_ui(self):
        self.rows_label = QLabel("Número de variables:")
        self.rows_input = QLineEdit()

        self.columns_label = QLabel("Número de restricciones:")
        self.columns_input = QLineEdit()

        self.btn_create_table = QPushButton("Crear Tabla")
        self.btn_create_table.clicked.connect(self.crear_tabla)

        layout = QGridLayout()
        layout.addWidget(self.rows_label, 0, 0)
        layout.addWidget(self.rows_input, 0, 1)
        layout.addWidget(self.columns_label, 1, 0)
        layout.addWidget(self.columns_input, 1, 1)
        layout.addWidget(self.btn_create_table, 2, 0, 1, 2)

        self.setLayout(layout)

    def crear_tabla(self):
        filas = int(self.rows_input.text())
        columnas = int(self.columns_input.text())

        self.limpiar() # Limpiar el layout

        # Crear la tabla
        for fila in range(filas + 2):
            for columna in range(columnas + 2):
                if fila == 0:
                    label_encabezado = QLabel(f"X{columna + 1}", alignment=Qt.AlignCenter)
                    if columna == columnas:
                        label_encabezado.setText("")
                    elif columna == columnas + 1:
                        label_encabezado.setText("R")
                    self.layout().addWidget(label_encabezado, fila, columna)
                elif columna == columnas:
                    if fila == 1:
                        pass
                    else:
                        combo_box = QComboBox()
                        combo_box.addItems(["<=", ">="])
                        combo_box.setObjectName(f"cell_{fila - 1}_{columna}")
                        self.layout().addWidget(combo_box, fila, columna)
                else:
                    if columna == columnas + 1 and fila == 1:
                        pass
                    else:
                        line_edit = QLineEdit()
                        line_edit.setText('0')
                        line_edit.setObjectName(f"cell_{fila - 1}_{columna}")
                        self.layout().addWidget(line_edit, fila, columna)

        self.setStyleSheet("""
            QLineEdit {
                background-color: #F5F5F5;
                padding: 2px;
                border: 1px solid #CCCCCC;
                color: #000000;
            }
            QComboBox {
                background-color: #F5F5F5;
                width: 60px;
                border: 1px solid #CCCCCC;
                color: #000000;
            }
        """)

        self.btn_regresar = QPushButton("Regresar")
        self.btn_regresar.clicked.connect(self.regresar)
        self.layout().addWidget(self.btn_regresar, filas + 3, 0, 1, columnas+2, alignment=Qt.AlignCenter)

        self.btn_maximizar = QPushButton("Maximizar")
        self.btn_maximizar.clicked.connect(self.maximizar)
        self.layout().addWidget(self.btn_maximizar, filas + 3, 2, 1, columnas+2, alignment=Qt.AlignCenter)

        self.btn_minimizar = QPushButton("Minimizar")
        self.btn_minimizar.clicked.connect(lambda:self.regresar())
        self.layout().addWidget(self.btn_minimizar, filas + 3, 4, 1, columnas+2, alignment=Qt.AlignCenter)
        
    def limpiar(self):
        for i in reversed(range(self.layout().count())):
            self.layout().itemAt(i).widget().setParent(None)

    def regresar(self):
        self.limpiar() # Limpiar layout
       
        self.layout().addWidget(self.rows_label, 0, 0)
        self.layout().addWidget(self.rows_input, 0, 1)
        self.layout().addWidget(self.columns_label, 1, 0)
        self.layout().addWidget(self.columns_input, 1, 1)
        self.layout().addWidget(self.btn_create_table, 2, 0, 1, 2)

    def maximizar(self):
        print("hola")
        filas, funcion_obj = self.obtener_valores(1)
        metodo = Maximizacion()
        print(filas, funcion_obj)
        metodo.maximizacion(filas, funcion_obj)
        simplex = metodo.iteraciones()
        widget = TableWidget(simplex)
        widget.show()


    def obtener_valores(self, esMaximizacion):
        filas_input = int(self.rows_input.text())
        columnas_input = int(self.columns_input.text())

        filas = []
        restricciones = [esMaximizacion, 0]
      
        #recuperar restricciones
        for fila in range(2, filas_input + 2):
            fila_actual = []
            for columna in range(0,columnas_input + 2):
                cell_object = self.layout().itemAtPosition(fila, columna)
                if cell_object is not None and cell_object.widget() is not None:
                    
                    if isinstance(cell_object.widget(), QLineEdit):
                        valor = cell_object.widget().text()
                        if(valor != ''):
                            fila_actual.append(int(valor))
                        else:
                            fila_actual.append(0)    
                    elif isinstance(cell_object.widget(), QComboBox):
                        #cambiar el texto del signo por el -1, 1 y agregarlo a la fila restricciones y su valor
                        valor = cell_object.widget().currentText()
                        if(valor == '>='):
                            fila_actual.append(1)
                            restricciones.append(1)
                        else:
                            fila_actual.append(-1)
                            restricciones.append(-1)
            filas.append(fila_actual)
        
        #recuperar funcion objetivo
        funcion_obj = []

        for columna in range(columnas_input + 2):
            cell_object = self.layout().itemAtPosition(1, columna)
            if cell_object is not None and cell_object.widget() is not None:
                if isinstance(cell_object.widget(), QLineEdit) or isinstance(cell_object.widget(), QComboBox):
                    valor_texto = cell_object.widget().text()
                    if valor_texto:
                        try:
                            valor = float(valor_texto) 
                            funcion_obj.append(valor)
                        except ValueError:
                            funcion_obj.append(0)  

        funcion_obj.extend([0] * 1)

        #(proivisional) elimar restricciones
        for fila in filas:
            index = len(fila) 
            del fila[index - 2]
        #multiplicar por -1

        filas.insert(0, funcion_obj.copy())

        for i in range(len(filas[0])):
            filas[0][i] *= -1
        
        tabla_s = []
           
        # arreglo 0 y 1
        for i in range(len(filas) - 1):
            long = len(filas)
            fila = [0] * (long - 1)
            if i < len(filas[0]):
                fila[i] = 1
            tabla_s.append(fila)

        tabla_s.insert(0, [0] * len(tabla_s))

        # insertar resultante
        for i in range(len(filas)):
            valor = filas[i].pop() 
            tabla_s[i].append(valor)

        for i in range(len(filas)):
            valor = tabla_s[i].copy()
            filas[i].extend(valor)
        
        # longitud = len(filas) + 1
        # fila_zm = [0] * longitud 

        # filas.insert(1, fila_zm)
        #print(tabla_s)
        #print(f"restricciones:{filas}")
        #print(f"funcion_obj: {funcion_obj}")
       # print(f"restricciones en numeros: {restricciones}")
        # print(tabla_simplex)
        return filas, funcion_obj
    


# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     window = Table()
#     window.show()
#     sys.exit(app.exec_())
