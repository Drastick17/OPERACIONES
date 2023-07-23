import numpy as np

def crear_tabla(tabla, desigualdades, restricciones):
    aux = tabla[:, -1].copy()

    for i in range(2, tabla.shape[0]):
        if tabla[i, -1] < 0:
            desigualdades[i] *= -1
            tabla[i] *= -1

    contador_artificial = np.sum(desigualdades[:-1] == 1)
    tabla_art = np.zeros((tabla.shape[0], contador_artificial), dtype=int)

    for i in range(tabla.shape[0]):
        for j in range(restricciones):
            if i in (0, 1):
                tabla[i, j] = 0
            elif desigualdades[i] == -1 and i - 2 == j:
                tabla[i, j] = 1
            elif desigualdades[i] == 1 and i - 2 == j:
                tabla[i, j] = -1
            else:
                tabla[i, j] = 0

    ancho_max = tabla.shape[1] + restricciones + contador_artificial
    nueva_tabla = np.zeros((tabla.shape[0], ancho_max), dtype=float)

    nueva_tabla[:, :tabla.shape[1]] = tabla

    for i in range(tabla.shape[0]):
        nueva_tabla[i, tabla.shape[1]:tabla.shape[1] + restricciones] = tabla[i, tabla.shape[1] - 1]


    aux2 = 2
    for i in range(tabla.shape[0]):
        for j in range(contador_artificial):
            if i in (0, 1):
                tabla_art[i, j] = 0
            elif desigualdades[i] == -1 and i - aux2 == j:
                aux2 += 1
                tabla_art[i, j] = 0
            elif desigualdades[i] == 1 and i - aux2 == j:
                tabla_art[i, j] = 1
            else:
                tabla_art[i, j] = 0

    nueva_tabla[:, -1] = aux
    nueva_tabla[:, tabla.shape[1] + restricciones:] = tabla_art
    return nueva_tabla

def mostrar_tabla(tabla, iteracion):
    print(f"Iteracion #{iteracion}")
    for row in tabla:
        print("\t".join(map(str, row)))

def relacionar_tabla(tabla, desigualdades):
    z_row = tabla[0]
    zm_row = tabla[1]

    for i in range(2, tabla.shape[0]):
        if desigualdades[i] == 1:
            z_row -= tabla[i]
    zm_row[:] = z_row

def columna_pivote(tabla, fila_control):
    col_pivote = np.argmin(tabla[fila_control, :-1])
    print(f"La columna pivote tiene el numero {tabla[fila_control, col_pivote]} posición {col_pivote + 1}")
    return col_pivote

def fila_pivote(tabla, columna_pivote):
    cocientes = np.full(tabla.shape[0], 5000000, dtype=float)
    for i in range(2, tabla.shape[0]):
        if tabla[i, columna_pivote] > 0:
            cocientes[i] = tabla[i, -1] / tabla[i, columna_pivote]

    fila_pivote = np.argmin(cocientes[2:])
    print(f"La fila pivote tiene el numero {tabla[fila_pivote+2, columna_pivote]} posición {fila_pivote + 2}")
    return fila_pivote + 2

def dividir_por_pivote(tabla, fila_pivote, columna_pivote):
    num = tabla[fila_pivote, columna_pivote]
    print(f"El número para dividir es: {num}")
    tabla[fila_pivote] /= num

def eliminar_filas(tabla, fila_pivote, columna_pivote):
    for i in range(tabla.shape[0]):
        if i != fila_pivote:
            multiplicador = tabla[i, columna_pivote]
            tabla[i] -= multiplicador * tabla[fila_pivote]

def hay_negativos(tabla, fila_control):
    return np.any(tabla[fila_control, :-1] < 0)

def main():
    # Tabla que debe contener los datos ingresados
    tabla = np.array([
        [-1, -3, -2, 0],
        [0, 0, 0, 0],
        [2, 4, 1, -6],
        [-1, 6, 1, 1],
        [1, 8, 3, 2]
    ], dtype=float)

    desigualdades = np.array([1, 0, 1, -1, 1], dtype=int)  # 1 es Maximizacion y >=; -1 es Minimizacion y <=

    num_variables = 3  # Número de variables en la función objetivo, necesario para luego
    num_restricciones = 3  # Número de restricciones
    funcion_obj = np.array([1, 3, 2], dtype=float)
    col_piv, fil_piv, iteracion = 0, 0, 0

    tabla_simplex = crear_tabla(tabla, desigualdades, num_restricciones)

    relacionar_tabla(tabla_simplex, desigualdades)

    mostrar_tabla(tabla_simplex, iteracion)

    fila_control = 0

    for i in range(desigualdades.shape[0]):
        if desigualdades[i] == 1:
            fila_control = 1

    while hay_negativos(tabla_simplex, fila_control):
        col_piv = columna_pivote(tabla_simplex, fila_control)
        fil_piv = fila_pivote(tabla_simplex, col_piv)
        dividir_por_pivote(tabla_simplex, fil_piv, col_piv)
        iteracion += 1
        eliminar_filas(tabla_simplex, fil_piv, col_piv)
        mostrar_tabla(tabla_simplex, iteracion)
        
    # Ahora verificamos y ajustamos las filas Z y ZM
    if not np.all(tabla_simplex[0, :-1] >= 0):
        z_min_value = np.min(tabla_simplex[0, :-1])
        col_min = np.argmin(tabla_simplex[0, :-1])
        tabla_simplex[1, col_min] += z_min_value
        tabla_simplex[0, :-1] -= z_min_value * tabla_simplex[1, :-1]

    print("\nTabla final:")
    mostrar_tabla(tabla_simplex, iteracion)

    # Calculamos el valor óptimo de la solución
    valor_optimo = np.sum(tabla_simplex[1, :-1] * funcion_obj)
    print(f"\nEl valor óptimo de la solución es {valor_optimo:.2f}")

if __name__ == "__main__":
    main()


# import numpy as np

# class SimplexMax:
#     def __init__(self, tabla, desigualdades, restricciones, funcion_obj):
#         self.tabla = tabla
#         self.desigualdades = desigualdades
#         self.restricciones = restricciones
#         self.funcion_obj = funcion_obj
#         self.num_variables = len(funcion_obj)
#         self.num_iteraciones = 0

#     def crear_tabla(self):
#         tabla_nueva = []
#         for i in range(1, len(self.tabla)):
#             restriccion = self.tabla[i]
#             if self.desigualdades[i] == 1:  # Restricción >=
#                 nueva_restriccion = [0] * (len(self.tabla[0]) - 1)
#                 nueva_restriccion[self.restricciones + i - 1] = 1  # Variable de exceso
#                 nueva_restriccion += restriccion[:-1] + [restriccion[-1]]  # Variables existentes + Valor constante
#                 tabla_nueva.append(nueva_restriccion)
#             else:  # Restricción <=
#                 nueva_restriccion = [0] * (len(self.tabla[0]) - 1)
#                 nueva_restriccion[self.restricciones + i - 1] = -1  # Variable de holgura
#                 nueva_restriccion += restriccion[:-1] + [restriccion[-1]]  # Variables existentes + Valor constante
#                 tabla_nueva.append(nueva_restriccion)

#         # Agregar la fila Z
#         fila_z = [1 if i < self.num_variables else 0 for i in range(len(tabla_nueva[0]) - 1)] + [0]  # Coeficientes de Z
#         tabla_nueva.insert(0, fila_z)

#         # Agregar la fila Zm
#         fila_zm = [-1 if i < self.num_variables else 0 for i in range(len(tabla_nueva[0]) - 1)] + [0]  # Coeficientes de Zm
#         tabla_nueva.insert(1, fila_zm)

#         # Convertir la tabla en una matriz de numpy
#         tabla_np = np.array(tabla_nueva, dtype=float)

#         return tabla_np

#     def mostrar_tabla(self, iteracion):
#         print(f"Iteracion #{iteracion}")
#         for fila in self.tabla:
#             print("\t".join(str(round(valor, 2)) for valor in fila))

#     def relaacionar_tabla(self):
#         for i in range(2, len(self.tabla)):
#             if self.desigualdades[i] == 1:
#                 self.tabla[1] = [self.tabla[1][j] - self.tabla[i][j] for j in range(len(self.tabla[0]))]

#     def columna_pivote(self, fila_control):
#         col_pivote = 0
#         for i in range(len(self.tabla[0]) - 1):
#             if self.tabla[fila_control][i] < self.tabla[fila_control][col_pivote]:
#                 col_pivote = i
#         print(f"La columna pivote tiene el número {self.tabla[fila_control][col_pivote]}, posición {col_pivote + 1}")
#         return col_pivote

#     def fila_pivote(self, columna_pivote):
#         cocientes = [0] * len(self.tabla)
#         cocientes[0] = 5000000
#         cocientes[1] = 5000000
#         for i in range(2, len(self.tabla)):
#             if self.tabla[i][columna_pivote] > 0:
#                 cocientes[i] = self.tabla[i][-1] / self.tabla[i][columna_pivote]
#         menor = fila_pivote = 0
#         for i in range(len(cocientes)):
#             if cocientes[i] < cocientes[menor] and cocientes[i] > 0:
#                 menor = i
#                 fila_pivote = i
#         print(f"La fila pivote tiene el número {self.tabla[fila_pivote][columna_pivote]}, posición {fila_pivote + 1}")
#         return fila_pivote

#     def dividir_por_pivote(self, fila_pivote, columna_pivote):
#         num = self.tabla[fila_pivote][columna_pivote]
#         print(f"El número para dividir es: {num}")
#         self.tabla[fila_pivote] = [valor / num for valor in self.tabla[fila_pivote]]
#         print("\t".join(str(valor) for valor in self.tabla[fila_pivote]))

#     def eliminar_filas(self, fila_pivote, columna_pivote):
#         for i in range(len(self.tabla)):
#             if i != fila_pivote:
#                 multiplicador = self.tabla[i][columna_pivote]
#                 self.tabla[i] = [self.tabla[i][j] - multiplicador * self.tabla[fila_pivote][j] for j in range(len(self.tabla[0]))]

#     def hay_negativos(self, fila_control):
#         for i in range(fila_control, len(self.tabla)):
#             if self.tabla[fila_control][i] < 0:
#                 print("Aún hay negativos")
#                 return True
#         return False

#     def maximizacion(self, iteraciones):
#         ancho_tabla_nueva = len(self.tabla[0])
#         for i in range(2, len(self.desigualdades)):
#             ancho_tabla_nueva += 1
#             if self.desigualdades[i] == 1:
#                 ancho_tabla_nueva += 1

#         self.tabla = self.crear_tabla()
#         self.relacionar_tabla()

#         self.mostrar_tabla(iteraciones)

#         fila_control = 0
#         for i in range(len(self.desigualdades)):
#             if self.desigualdades[i] == 1:
#                 fila_control = 1

#         while self.hay_negativos(fila_control):
#             col_piv = self.columna_pivote(fila_control)
#             fil_piv = self.fila_pivote(col_piv)
#             self.dividir_por_pivote(fil_piv, col_piv)
#             self.num_iteraciones += 1
#             self.eliminar_filas(fil_piv, col_piv)
#             self.mostrar_tabla(iteraciones)

#         self.ciclos = 1
#         if fila_control == 1:
#             fila_control = 0
#             while self.hay_negativos(fila_control):
#                 col_piv = self.columna_pivote(fila_control)
#                 fil_piv = self.fila_pivote(col_piv)
#                 self.dividir_por_pivote(fil_piv, col_piv)
#                 self.num_iteraciones += 1
#                 self.eliminar_filas(fil_piv, col_piv)
#                 self.mostrar_tabla(iteraciones)
#                 self.ciclos += 1

#         print("El valor óptimo de la solución es", self.tabla[0][-1])

# # Ejemplo de uso
# tabla = [
#     [-1, -3, -2, 0],
#     [0, 0, 0, 0],
#     [2, 4, 1, -6],
#     [-1, 6, 1, 1],
#     [1, 8, 3, 2]
# ]
# funcion_obj = [1, 3, 2]

# desigualdades = [1, 0, 1, -1, 1]  # 1 es Maximización y >=; -1 es Minimización y <=

# restricciones = 3  # Número de restricciones

# solver = SimplexMax(tabla, desigualdades, restricciones, funcion_obj)
# iteraciones = []
# solver.maximizacion(iteraciones)
