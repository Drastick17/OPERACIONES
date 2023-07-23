from PyQt5.QtWidgets import QApplication, QWidget, QTableWidget
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QVBoxLayout, QTableWidgetItem, QLabel, QPushButton


class Maximizacion:
    def __init__(self):
        self.iterations = []

    def mostrar_tabla(self, tabla, iteracion):
        print("Iteración #" + str(iteracion))
        for fila in tabla:
            for valor in fila:
                print(valor, end="\t")
            print("")

    def hay_negativos(self, tabla):
        for valor in tabla[0]:
            if valor < 0:
                print("Aún hay negativos")
                return True
        return False

    def columna_pivote(self, tabla):
        col_pivote = 0
        for i in range(len(tabla[0]) - 1):
            if tabla[0][i] < tabla[0][col_pivote]:
                col_pivote = i
        print("La columna pivote tiene el número " +
              str(tabla[0][col_pivote]) + " posición " + str(col_pivote + 1))
        return col_pivote

    def fila_pivote(self, tabla, columna_pivote):
        cocientes = []
        for fila in tabla:
            if fila[columna_pivote] > 0:
                cocientes.append(fila[-1] / fila[columna_pivote])
            else:
                cocientes.append(5000000)
        menor = 0
        fila_pivote = 0
        for i in range(len(cocientes)):
            if cocientes[i] < cocientes[menor] and cocientes[i] > 0:
                menor = i
                fila_pivote = i
        print("La fila pivote tiene el número " +
              str(tabla[fila_pivote][columna_pivote]) + " posición " + str(fila_pivote + 1))
        return fila_pivote

    def dividir_por_pivote(self, tabla, fila_pivote, columna_pivote):
        num = tabla[fila_pivote][columna_pivote]
        print("El número para dividir es: " + str(num))
        for i in range(len(tabla[fila_pivote])):
            tabla[fila_pivote][i] /= num
            print(tabla[fila_pivote][i], end=" ")
        print("")

    def eliminar_filas(self, tabla, fila_pivote, columna_pivote):
        multiplicador = 0
        for i in range(len(tabla)):
            if i != fila_pivote:
                multiplicador = tabla[i][columna_pivote]
                for j in range(len(tabla[i])):
                    tabla[i][j] -= multiplicador * tabla[fila_pivote][j]

    def calculo_fun_obj(self, tabla, funcion_obj):
        valor_optimo = 0
        for i in range(1, len(tabla)):
            for j in range(len(tabla[i]) - len(funcion_obj) - 1):
                if tabla[i][j] == 1:
                    print("Valor óptimo en fila " + str(i) + " columna " +
                          str(j) + " x" + str(j + 1) + " es " + str(tabla[i][-1]))
                    valor_optimo += tabla[i][-1] * funcion_obj[j]
        print("El valor óptimo de la solución es " + str(valor_optimo))

    def maximizacion(self, tabla_simplex, funcion_obj):
        # tabla_simplex = [
        #     [-1, -3, -2, 0, 0, 0, 0],
        #     [2, 4, 1, 1, 0, 0, 6],
        #     [-1, 6, 1, 0, 1, 0, 1],
        #     [1, 8, 3, 0, 0, 1, 2]
        # ]

        # num_variables = 4
        # num_restricciones = 2
        # num_restricciones_m = 0
        # funcion_obj = [1, 3, 2]
        iteracion = 0

        self.mostrar_tabla(tabla_simplex, iteracion)
        self.iterations.append(tabla_simplex.copy())

        while self.hay_negativos(tabla_simplex):
            self.iterations.append(tabla_simplex.copy())
            col_piv = self.columna_pivote(tabla_simplex)
            fil_piv = self.fila_pivote(tabla_simplex, col_piv)
            self.dividir_por_pivote(tabla_simplex, fil_piv, col_piv)
            iteracion += 1
            self.eliminar_filas(tabla_simplex, fil_piv, col_piv)
            self.mostrar_tabla(tabla_simplex, iteracion)

        self.calculo_fun_obj(tabla_simplex, funcion_obj)

    def iteraciones(self):
        return self.iterations


# if __name__ == "__main__":
#     app = QApplication(sys.ar)
