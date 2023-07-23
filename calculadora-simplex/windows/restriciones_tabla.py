from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QComboBox, QLineEdit, QPushButton, QGridLayout, QVBoxLayout, QStackedLayout
from PyQt5.QtCore import Qt
from methods.SimplexMethod import SimplexMethod
# from windows.tabla_simplex import TableWidget
import numpy as np
class TablaRestricciones(QWidget):
    def __init__(self, regresar, filas, columnas):
        super().__init__()
        self.filas = filas
        self.columnas = columnas
        self.regresar = regresar
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.grid_layout = QGridLayout()
        layout.addLayout(self.grid_layout)
        self.setStyleSheet("""
            QGridLayout {
                background-color: #F5F5F5;
            }
            QLineEdit, QComboBox {
                background-color: #F5F5F5;
                padding: 5px;
                border: 1px solid #CCCCCC;
                color: #000000;
                font-size: 14px;
                min-width:40px;
            }
            QLabel {
                font-size: 14px;
                font-weight: bold;
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

        self.crear_tabla()

    def crear_tabla(self):
        try:
            for fila in range(self.filas + 2):
                for columna in range(self.columnas + 2):
                    if fila == 0:
                        label_encabezado = QLabel(
                            f"X{columna + 1}", alignment=Qt.AlignCenter)
                        if columna == self.columnas:
                            label_encabezado.setText("")
                        elif columna == self.columnas + 1:
                            label_encabezado.setText("R")
                        self.grid_layout.addWidget(
                            label_encabezado, fila, columna)
                    elif columna == self.columnas:
                        if fila == 1:
                            pass
                        else:
                            combo_box = QComboBox()
                            combo_box.addItems(["<=", ">="])
                            combo_box.setObjectName(
                                f"cell_{fila - 1}_{columna}")
                            self.grid_layout.addWidget(
                                combo_box, fila, columna)
                    else:
                        if columna == self.columnas + 1 and fila == 1:
                            pass
                        else:
                            line_edit = QLineEdit()
                            line_edit.setText('0')
                            line_edit.setObjectName(
                                f"cell_{fila - 1}_{columna}")
                            self.grid_layout.addWidget(
                                line_edit, fila, columna)

            button_maximizar = QPushButton("Maximizar")
            button_minimizar = QPushButton("Minimizar")
            button_regresar = QPushButton("Regresar")

            self.grid_layout.addWidget(
                button_maximizar, self.filas + 2, 0, 1, self.columnas + 2)
            self.grid_layout.addWidget(
                button_minimizar, self.filas + 3, 0, 1, self.columnas + 2)
            self.grid_layout.addWidget(
                button_regresar, self.filas + 5, 0, 1, self.columnas + 2)

            button_maximizar.clicked.connect(self.maximizar)
            button_minimizar.clicked.connect(self.limpiar_tabla)
            button_regresar.clicked.connect(self.regresar)

        except ValueError:
            print("Error: Ingrese un número válido para filas y columnas.")

    def maximizar(self):
        restricciones, resultantes, desigualdades, funcion_obj = self.obtener_valores(1)
        np_rests = np.array(restricciones.copy())



        print(np_rests, np_results, np_desi, np_func)
        solver = SimplexMethod()
        solver.simplex('max',np_rests, np_results, np_func, np_desi, 100 )
        # print(filas)

        # maxMethod = SimplexMax(filas,  restricciones, self.filas,  funcion_obj)
        # iteraciones = []
        # maxMethod.maximizacion(iteraciones)
        # table_ui = TableWidget(iteraciones)
        # table_ui.show()
        
    def obtener_valores(self, esMaximizacion):

        restricciones = []
        desigualdades = []
      
        # recuperar restricciones
        for fila in range(2, self.filas + 2):
            fila_actual = []
            for columna in range(0, self.columnas + 2):
                cell_object = self.grid_layout.itemAtPosition(fila, columna)
                if cell_object is not None and cell_object.widget() is not None:
                    if isinstance(cell_object.widget(), QLineEdit):
                        valor = cell_object.widget().text()
                        if valor != '':
                            fila_actual.append(int(valor))
                        else:
                            fila_actual.append(0)    
                    elif isinstance(cell_object.widget(), QComboBox):
                        # cambiar el texto del signo por el -1, 1 y agregarlo a la fila restricciones y su valor
                        valor = cell_object.widget().currentText()
                        if valor == '>=':
                            fila_actual.append(-1)
                            desigualdades.append(-1)
                        else:
                            fila_actual.append(1)
                            desigualdades.append(1)
            restricciones.append(fila_actual)
        
        # recuperar funcion objetivo
        funcion_obj = []

        for columna in range(self.columnas + 2):
            cell_object = self.grid_layout.itemAtPosition(1, columna)
            if cell_object is not None and cell_object.widget() is not None:
                if isinstance(cell_object.widget(), QLineEdit) or isinstance(cell_object.widget(), QComboBox):
                    valor_texto = cell_object.widget().text()
                    if valor_texto:
                        try:
                            valor = float(valor_texto) 
                            funcion_obj.append(valor)
                        except ValueError:
                            funcion_obj.append(0)  


        # (provisional) eliminar restricciones
        for fila in restricciones:
            index = len(fila) 
            del fila[index - 2]

        # multiplicar por -1
        restricciones.insert(0, funcion_obj.copy())
        for i in range(len(restricciones[0])):
            restricciones[0][i] *= -1

        resultantes = []
        for i in range(1, len(restricciones)):
            resultante = restricciones[i].pop()
            resultantes.append([resultante])
        
        #Agregar z a las desigualdades
        desigualdades.insert(0, 0)

        # print(f"desigualdades: {desigualdades}")
        # print(f"resultantes: {resultantes}")
        # print(f"restricciones: {restricciones} ")
        # print(f"funcion_obj {funcion_obj}")

        return restricciones, resultantes, desigualdades, funcion_obj

    def limpiar_tabla(self):
        pass

if __name__ == '__main__':
    import sys

    def regresar():
        app.quit()

    app = QApplication(sys.argv)
    window = TablaRestricciones(regresar, 3, 3)
    window.show()
    sys.exit(app.exec_())


# from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QComboBox, QLineEdit, QPushButton, QGridLayout, QVBoxLayout, QStackedLayout
# from PyQt5.QtCore import Qt
# from methods.max import SimplexMax


# class TablaRestricciones(QWidget):
#     def __init__(self, regresar, filas, columnas):
#         super().__init__()
#         self.filas = filas
#         self.c # for i in range(len(filas)):
        #     valor = tabla_s[i].copy()
        #     filas[i].extend(valor)
    
        # #print(tabla_s)
        # print(f"restricciones: {filas}")
        # print(f"funcion_obj: {funcion_obj}")
        # olumnas = columnas
#         self.regresar = regresar
#         layout = QVBoxLayout()
#         self.setLayout(layout)

#         self.grid_layout = QGridLayout()
#         layout.addLayout(self.grid_layout)
#         self.setStyleSheet("""
#             QGridLayout {
#                 background-color: #F5F5F5;
#             }
#             QLineEdit, QComboBox {
#                 background-color: #F5F5F5;
#                 padding: 5px;
#                 border: 1px solid #CCCCCC;
#                 color: #000000;
#                 font-size: 14px;
#             }
#             QLabel {
#                 font-size: 14px;
#                 font-weight: bold;
#             }
#             QLabel#space{
#                 padding-bottom:20px;
#             }
#             QPushButton {
#                 background-color: #4CAF50;
#                 color: white;
#                 border: none;
#                 border-radius: 5px;
#                 padding: 10px 20px;
#                 font-size: 16px;
#             }
#             QPushButton#back{
#                 background-color: #0000ff;
#             }
#             QPushButton:hover {
#                 background-color: #45a049;
#             }
#         """)

#         self.crear_tabla()

#     def crear_tabla(self):
#         try:
#             for fila in range(self.filas + 2):
#                 for columna in range(self.columnas + 2):
#                     if fila == 0:
#                         label_encabezado = QLabel(
#                             f"X{columna + 1}", alignment=Qt.AlignCenter)
#                         if columna == self.columnas:
#                             label_encabezado.setText("")
#                         elif columna == self.columnas + 1:
#                             label_encabezado.setText("R")
#                         self.grid_layout.addWidget(
#                             label_encabezado, fila, columna)
#                     elif columna == self.columnas:
#                         if fila == 1:
#                             pass
#                         else:
#                             combo_box = QComboBox()
#                             combo_box.addItems(["<=", ">="])
#                             combo_box.setObjectName(
#                                 f"cell_{fila - 1}_{columna}")
#                             self.grid_layout.addWidget(
#                                 combo_box, fila, columna)
#                     else:
#                         if columna == self.columnas + 1 and fila == 1:
#                             pass
#                         else:
#                             line_edit = QLineEdit()
#                             line_edit.setText('0')
#                             line_edit.setObjectName(
#                                 f"cell_{fila - 1}_{columna}")
#                             self.grid_layout.addWidget(
#                                 line_edit, fila, columna)

#             button_maximizar = QPushButton("Maximizar")
#             button_minimizar = QPushButton("Minimizar")
#             button_regresar = QPushButton("Regresar")

#             self.grid_layout.addWidget(
#                 button_maximizar, self.filas + 2, 0, 1, self.columnas + 2)
#             self.grid_layout.addWidget(
#                 button_minimizar, self.filas + 3, 0, 1, self.columnas + 2)
#             self.grid_layout.addWidget(
#                 button_regresar, self.filas + 5, 0, 1, self.columnas + 2)

#             button_maximizar.clicked.connect(self.maximizar)
#             button_minimizar.clicked.connect(self.limpiar_tabla)
#             button_regresar.clicked.connect(self.regresar)

#         except ValueError:
#             print("Error: Ingrese un número válido para filas y columnas.")

#     def maximizar(self):
#         self.obtener_valores(1)

#     def obtener_valores(self, esMaximizacion):

#         filas = []
#         restricciones = [esMaximizacion, 0]

#         # recuperar restricciones
#         for fila in range(2, self.filas + 2):
#             fila_actual = []
#             for columna in range(0, self.columnas + 2):
#                 cell_object = self.layout.itemAtPosition(fila, columna)
#                 if cell_object is not None and cell_object.widget() is not None:

#                     if isinstance(cell_object.widget(), QLineEdit):
#                         valor = cell_object.widget().text()
#                         if (valor != ''):
#                             fila_actual.append(int(valor))
#                         else:
#                             fila_actual.append(0)
#                     elif isinstance(cell_object.widget(), QComboBox):
#                         # cambiar el texto del signo por el -1, 1 y agregarlo a la fila restricciones y su valor
#                         valor = cell_object.widget().currentText()
#                         if (valor == '>='):
#                             fila_actual.append(1)
#                             restricciones.append(1)
#                         else:
#                             fila_actual.append(-1)
#                             restricciones.append(-1)
#             filas.append(fila_actual)

#         # recuperar funcion objetivo
#         funcion_obj = []

#         for columna in range(self.columnas + 2):
#             cell_object = self.layout().itemAtPosition(1, columna)
#             if cell_object is not None and cell_object.widget() is not None:
#                 if isinstance(cell_object.widget(), QLineEdit) or isinstance(cell_object.widget(), QComboBox):
#                     valor_texto = cell_object.widget().text()
#                     if valor_texto:
#                         try:
#                             valor = float(valor_texto)
#                             funcion_obj.append(valor)
#                         except ValueError:
#                             funcion_obj.append(0)

#         funcion_obj.extend([0] * 1)

#         # (proivisional) eliminar restricciones

#         for fila in filas:
#             index = len(fila)
#             restriccion = fila.pop(index - 2)
#             restricciones.append(restriccion)

#         # multiplicar por -1

#         filas.insert(0, funcion_obj.copy())

#         for i in range(len(filas[0])):
#             filas[0][i] *= -1

#         tabla_s = []

#         # arreglo 0 y 1
#         for i in range(len(filas) - 1):
#             long = len(filas)
#             fila = [0] * (long - 1)
#             if i < len(filas[0]):
#                 fila[i] = 1
#             tabla_s.append(fila)

#         tabla_s.insert(0, [0] * len(tabla_s))

#         # insertar resultante
#         for i in range(len(filas)):
#             valor = filas[i].pop()
#             tabla_s[i].append(valor)

#         for i in range(len(filas)):
#             valor = tabla_s[i].copy()
#             filas[i].extend(valor)

#         longitud = len(filas) + 1
#         fila_zm = [0] * longitud

#         filas.insert(1, fila_zm)
#         # print(tabla_s)
#         print(f"restricciones:{filas}")
#         print(f"funcion_obj: {funcion_obj}")
#         print(f"restricciones en numeros: {restricciones}")
#         # print(tabla_simplex)
#         # return filas, funcion_obj

#     def limpiar_tabla(self):
#         pass
