import math

iterations = []
optimal_values = []


def show_table_terminal(table, i):
    print("Iteracion #" + str(i))
    for row in table:
        for value in row:
            print(math.floor(value), end="\t")
        print("")
    iterations.append(table.copy()) 

def has_negatives(table):
    for value in table[0]:
        if value < 0:
            print("Aun hay negativos")
            return True
    return False

def column_pivote(table):
    col_pivote = 0
    for i in range(len(table[0]) - 1):
        if table[0][i] < table[0][col_pivote]:
            col_pivote = i
    print("La columna pivote tiene el numero",
          table[0][col_pivote], "posición", (col_pivote + 1))
    return col_pivote

def row_pivote(table, column_pivote):
    quotients = []
    for i in range(len(table)):
        if table[i][column_pivote] > 0:
            quotients.append(
                table[i][len(table[0]) - 1] / table[i][column_pivote])
        else:
            quotients.append(5000000)
    less = 0
    row_pivote = 0
    for i in range(len(quotients)):
        if quotients[i] < quotients[less] and quotients[i] > 0:
            less = i
            row_pivote = i
    print("La fila pivote tiene el numero",
          table[row_pivote][column_pivote], "posicion", (row_pivote + 1))
    return row_pivote

def split_by_pivote(table, row_pivote, column_pivote):
    num = table[row_pivote][column_pivote]
    print("El numero para dividir es:", num)
    for i in range(len(table[row_pivote])):
        table[row_pivote][i] /= num
        print(table[row_pivote][i], end=" ")
    print("")

def delete_rows(table, row_pivote, column_pivote):
    multiplier = 0
    for i in range(len(table)):
        if i != row_pivote:
            multiplier = table[i][column_pivote]
            for j in range(len(table[i])):
                table[i][j] -= multiplier * table[row_pivote][j]

def calc_fun_obj(table, funcion_obj):
    valor_optimo = 0
    for i in range(1, len(table)):
        for j in range(len(table[0]) - len(funcion_obj) - 1):
            if table[i][j] == 1:
                #optimal_values.append(f"Valor óptimo en fila {i}, columna {j} (x{j+1}): {math.floor(table[i][len(table[0]) - 1])}")
                optimal_values.append(f"(x{j+1}): {math.floor(table[i][len(table[0]) - 1])}")
                print("Valor optimo en fila", i, "columna", j, "x" + str(j + 1), "es", math.floor(table[i][len(table[0]) - 1]))
                valor_optimo += table[i][len(table[0]) - 1] * funcion_obj[j]
    print("El valor optimo de la solucion es", math.floor(valor_optimo))

def solutionObj():
    result = {
        "optimal_values": optimal_values,
        "solution_tables": iterations
    }
    return result

def calc_table(table, function_obj):


    iteracion = 0

    show_table_terminal(table, iteracion)

    while has_negatives(table):
        col_piv = column_pivote(table)
        fil_piv = row_pivote(table, col_piv)
        split_by_pivote(table, fil_piv, col_piv)
        iteracion += 1
        delete_rows(table, fil_piv, col_piv)
        show_table_terminal(table, iteracion)

    calc_fun_obj(table, function_obj)

    solution = solutionObj()
    return solution
