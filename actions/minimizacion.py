from fractions import Fraction
from decimal import Decimal
import math


def crear_tabla(tabla, desigualdades, restricciones):
    aux = [fila[-1] for fila in tabla]

    for i in range(2, len(tabla)):
        if tabla[i][-1] < 0:
            desigualdades[i] *= -1
            tabla[i] = [-valor for valor in tabla[i]]

    contador_artificial = sum(
        1 for desigualdad in desigualdades[:-1] if desigualdad == 1)
    tabla_art = [[0] * contador_artificial for _ in range(len(tabla))]

    tabla_res = [[0] * restricciones for _ in range(len(tabla))]
    for i in range(len(tabla)):
        for j in range(restricciones):
            if i in (0, 1):
                tabla_res[i][j] = 0
            elif desigualdades[i] == -1 and i - 2 == j:
                tabla_res[i][j] = 1
            elif desigualdades[i] == 1 and i - 2 == j:
                tabla_res[i][j] = -1

    ancho_max = len(tabla[0]) + len(tabla_res[0]) + len(tabla_art[0])
    nueva_tabla = [[0] * ancho_max for _ in range(len(tabla))]

    for i in range(len(tabla)):
        nueva_tabla[i][:len(tabla[0])] = tabla[i]

    for i in range(len(tabla)):
        nueva_tabla[i][len(tabla[0]):len(tabla[0]) +
                       len(tabla_res[0])] = tabla_res[i]

    for i in range(len(tabla)):
        nueva_tabla[i][len(tabla[0]) + len(tabla_res[0]):] = tabla_art[i]

    for i in range(len(tabla)):
        nueva_tabla[i][-1] = aux[i]

    return nueva_tabla


def mostrar_tabla(tabla, iteracion):
    print(f"Iteracion #{iteracion}")
    for fila in tabla:
        print("\t".join(str(Fraction(Decimal(valor))) for valor in fila))


def relacionar_tabla(tabla, desigualdades):
    for i in range(2, len(tabla)):
        if desigualdades[i] == 1:
            tabla[1] = [tabla[1][j] + tabla[i][j]
                        for j in range(len(tabla[0]))]


def columna_pivote(tabla, fila_control):
    col_pivote = 0
    for i in range(len(tabla[0]) - 1):
        if tabla[fila_control][i] > tabla[fila_control][col_pivote]:
            col_pivote = i
    print(
        f"La columna pivote tiene el número {tabla[fila_control][col_pivote]}, posición {col_pivote + 1}")
    return col_pivote


def fila_pivote(tabla, columna_pivote):
    cocientes = [0] * len(tabla)
    cocientes[0] = 5000000
    cocientes[1] = 5000000
    for i in range(2, len(tabla)):
        if tabla[i][columna_pivote] > 0:
            cocientes[i] = tabla[i][-1] / tabla[i][columna_pivote]
    menor = fila_pivote = 0
    for i in range(len(cocientes)):
        if cocientes[i] < cocientes[menor] and cocientes[i] > 0:
            menor = i
            fila_pivote = i
    print(
        f"La fila pivote tiene el número {tabla[fila_pivote][columna_pivote]}, posición {fila_pivote + 1}")
    return fila_pivote


def dividir_por_pivote(tabla, fila_pivote, columna_pivote):
    num = tabla[fila_pivote][columna_pivote]
    print(f"El número para dividir es: {num}")
    tabla[fila_pivote] = [Decimal(valor) / Decimal(num)
                          for valor in tabla[fila_pivote]]
    print("\t".join(str(valor) for valor in tabla[fila_pivote]))


def eliminar_filas(tabla, fila_pivote, columna_pivote):
    for i in range(len(tabla)):
        if i != fila_pivote:
            multiplicador = tabla[i][columna_pivote]
            tabla[i] = [Decimal(tabla[i][j]) - Decimal(multiplicador) *
                        Decimal(tabla[fila_pivote][j]) for j in range(len(tabla[0]))]


def hay_positivos(tabla, fila_control):
    for i in range(fila_control, len(tabla[fila_control])):
        if tabla[fila_control][i] > 0:
            print("Aún hay postivos")
            return True
    return False


def minimizacion(tabla, desigualdades, restricciones, funcion_obj):
    num_variables = len(funcion_obj)
    num_iteraciones = 0

    ancho_tabla_nueva = len(tabla[0])
    for i in range(2, len(desigualdades)):
        ancho_tabla_nueva += 1
        if desigualdades[i] == 1:
            ancho_tabla_nueva += 1

    tabla_simplex = crear_tabla(tabla, desigualdades, restricciones)
    relacionar_tabla(tabla_simplex, desigualdades)

    mostrar_tabla(tabla_simplex, num_iteraciones)

    fila_control = 0
    for i in range(len(desigualdades)):
        if desigualdades[i] == 1:
            fila_control = 1

    while hay_positivos(tabla_simplex, fila_control):
        col_piv = columna_pivote(tabla_simplex, fila_control)
        fil_piv = fila_pivote(tabla_simplex, col_piv)
        dividir_por_pivote(tabla_simplex, fil_piv, col_piv)
        num_iteraciones += 1
        eliminar_filas(tabla_simplex, fil_piv, col_piv)
        mostrar_tabla(tabla_simplex, num_iteraciones)

#     calculo_fun_obj(tabla_simplex, funcion_obj)

# def calculo_fun_obj(tabla, funcion_obj):
#     valor_optimo = 0
#     for i in range(2, len(tabla) - 1):
#         contador = sum(1 for valor in tabla[i][:-1] if valor == 1)
#         if contador == 1:
#             columna = i + 1
#             valor = tabla[i][-1]
#             print(f"Valor óptimo en fila {i} columna {columna} x{columna} es {valor}")
#             valor_optimo += valor * funcion_obj[i - 2]
#     print(f"El valor óptimo de la solución es {valor_optimo}")


# Ejemplo de uso
tabla = [
    [Decimal(-3), Decimal(-3), Decimal(-2), Decimal(0)],
    [Decimal(0), Decimal(0), Decimal(0), Decimal(0)],
    [Decimal(2), Decimal(4), Decimal(1), Decimal(4)],
    [Decimal(-1), Decimal(6), Decimal(1), Decimal(1)],
    [Decimal(1), Decimal(8), Decimal(3), Decimal(2)]
]
# 1 es Maximización y >=; -1 es Minimización y <=
desigualdades = [-1, 0, 1, -1, 1]

restricciones = 3  # Número de restricciones
funcion_obj = [3, 3, 2]

minimizacion(tabla, desigualdades, restricciones, funcion_obj)
