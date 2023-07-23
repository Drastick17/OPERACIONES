from __future__ import division
from numpy import *

from fractions import Fraction

class TableMaxStandard:

    def __init__(self, obj):
        self.obj = [1] + obj
        self.rows = []
        self.cons = []
        self.nro_variables = len(obj)
        self.nro_restricciones = 0
        self.mostrar_en_fracion = False  # set True to output in fraction
        self.iteraciones = []

    def añadir_restriccion(self, expression, value):
        self.rows.append([0] + expression)
        self.cons.append(value)
        self.nro_restricciones += 1
        self.header_tabla = ["Basic"] + ["x"+str(i+1) for i in range(self.nro_variables)] \
                                        + ["s"+str(i+1) for i in range(self.nro_restricciones)] \
                                        + ["Solution"]

        self.basic_variables = ["s"+str(i+1)
                                for i in range(self.nro_restricciones)]

    def columna_pivote(self):
        low = 0
        idx = 0
        for i in range(1, len(self.obj)-1):
            if self.obj[i] < low:
                low = self.obj[i]
                idx = i
        if idx == 0:
            return -1
        return idx

    def fila_pivote(self, col):
        rhs = [self.rows[i][-1] for i in range(len(self.rows))]
        lhs = [self.rows[i][col] for i in range(len(self.rows))]
        ratio = []
        for i in range(len(rhs)):
            if lhs[i] == 0:
                ratio.append(99999999 * abs(max(rhs)))
                continue
            ratio.append(rhs[i]/lhs[i])
        return argmin(ratio)

    def mostrar_tabla(self):
        self.iteraciones.append([])
        self.iteraciones[len(self.iteraciones) - 1].append(self.obj)
        for i in range(len(self.rows) - 1):
          self.iteraciones[len(self.iteraciones) - 1].append(self.rows[i])
        if self.mostrar_en_fracion:
            fmt = '{:<8}'.format("Basic") \
                  + "".join(['{:>12}'.format("x"+str(i+1)) for i in range(self.nro_variables)])   \
                  + "".join(['{:>12}'.format("s"+str(i+1)) for i in range(self.nro_restricciones)]) \
                  + '{:>12}'.format("Sol.")

            fmt += "\n" 
            fmt += '{:<8}'.format("z") + "".join(["{:>12}".format(str(Fraction(item).limit_denominator(100))) for item in self.obj[1:]])

            for i, row in enumerate(self.rows):
                fmt += "\n" 
                fmt += '{:<8}'.format(self.basic_variables[i]) \
                       + "".join(["{:>12}".format(str(Fraction(item).limit_denominator(100))) for item in row[1:]])
            print(fmt)
        else:
            fmt = '{:<8}'.format("Basic") \
                  + "".join(['{:>8}'.format("x"+str(i+1)) for i in range(self.nro_variables)])   \
                  + "".join(['{:>8}'.format("s"+str(i+1)) for i in range(self.nro_restricciones)]) \
                  + '{:>8}'.format("Sol.")

            fmt += "\n"
            fmt += '{:<8}'.format("z") + \
                "".join(["{:>8.2f}".format(item) for item in self.obj[1:]])

            for i, row in enumerate(self.rows):
                fmt += "\n"
                fmt += '{:<8}'.format(self.basic_variables[i]) \
                       + "".join(["{:>8.2f}".format(item) for item in row[1:]])
            print(fmt)


    def pivote(self, row, col):
        e = self.rows[row][col]
        self.rows[row] /= e
        for r in range(len(self.rows)):
            if r == row:
                continue
            self.rows[r] = self.rows[r] - self.rows[r][col]*self.rows[row]
        self.obj = self.obj - self.obj[col]*self.rows[row]

    def revisar(self):
        if min(self.obj[1:-1]) >= 0:
            return 1
        return 0

    def resolver(self):
        for i in range(len(self.rows)):
            self.obj += [0]
            ident = [0 for r in range(len(self.rows))]
            ident[i] = 1
            self.rows[i] += ident + [self.cons[i]]
            self.rows[i] = array(self.rows[i], dtype=float)
        self.obj = array(self.obj + [0], dtype=float)

        self.mostrar_tabla()
        while not self.revisar():
            c = self.columna_pivote()
            r = self.fila_pivote(c)
            self.pivote(r, c)
            # print('\n')
            # print('Entering Variable: ', self.header_tableau[c])
            # print('Leaving Variable : ', self.basic_variables[r])
            # print('\n')
            for index, item in enumerate(self.basic_variables):
                if self.basic_variables[index] == self.basic_variables[r]:
                    self.basic_variables[index] = self.header_tabla[c]

            self.mostrar_tabla()


if __name__ == '__main__':

    """
    max z = 2x + 3y + 2z
    st
    2x + y + z <= 4
    x + 2y + z <= 7
    z          <= 5
    x,y,z >= 0
    """

    t = TableMaxStandard([-1, -3, -2])
    t.añadir_restriccion([2, 4, 1,], -6)
    t.añadir_restriccion([-1, 6, 1], 1)
    t.añadir_restriccion([1, 8, 3], 2)
    t.mostrar_en_fracion = True
    t.resolver()
    for i in range(len(t.iteraciones)):
        for fila in t.iteraciones[i]:
            print(fila)
