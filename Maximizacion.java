package com.mycompany.toio;

public class Maximizacion {

    public static void main(String[] args) {
        //Tabla que debe contener los datos ingresados
        float tablaSimplex[][] = {
            {-1, -3, -2, 0, 0, 0, 0},
            {2, 4, 1, 1, 0, 0, 6},
            {-1, 6, 1, 0, 1, 0, 1},
            {1, 8, 3, 0, 0, 1, 2}
        };

        int numVariables = 4; // Número de variables en la función objetivo, necesario para luego
        int numRestricciones = 2; // Número de restricciones, necesario para luego
        int numRestriccionesM = 0; // Número de restricciones, necesario para luego, hay que arreglar los M
        float funcionObj[] = {1, 3, 2};
        int colPiv, filPiv, iteracion = 0;

        mostrarTabla(tablaSimplex, iteracion);

        while (hayNegativos(tablaSimplex)) {
            hayNegativos(tablaSimplex);
            colPiv = columnaPivote(tablaSimplex);
            filPiv = filaPivote(tablaSimplex, colPiv);
            dividirPorPivote(tablaSimplex, filPiv, colPiv);
            iteracion++;
            eliminarFilas(tablaSimplex, filPiv, colPiv);
            mostrarTabla(tablaSimplex, iteracion);
        }
        calculoFunObj(tablaSimplex, funcionObj);
        

    }
    
    //Funcion que simplemente muestra la tabla, sea su estado, y el numro de iteracion que pasa

    public static void mostrarTabla(float tabla[][], int iteracion) {
        System.out.println("Iteracion #" + iteracion);
        for (int i = 0; i < tabla.length; i++) {
            for (int j = 0; j < tabla[0].length; j++) {
                System.out.print(tabla[i][j] + "\t");
            }
            System.out.println("");
        }
    }

    //Verificacion de no negativos en Z de la tabla simplex
    public static boolean hayNegativos(float tabla[][]) {
        for (int i = 0; i < tabla[0].length; i++) {
            if (tabla[0][i] < 0) {
                System.out.println("Aun hay negativos");
                return true;
            }
        }
        return false;
    }
    
    //Elige la columna pivote, el numero mas negativo

    public static int columnaPivote(float tabla[][]) {
        int colPivote = 0;
        for (int i = 0; i < tabla[0].length - 1; i++) {
            if (tabla[0][i] < tabla[0][colPivote]) {
                colPivote = i;
            }
        }
        System.out.println("La columna pivote tiene el numero " + tabla[0][colPivote] + " posición " + (colPivote + 1));
        return colPivote;
    }

    public static int filaPivote(float tabla[][], int columnaPivote) {

        float cocientes[] = new float[tabla.length];
        for (int i = 0; i < tabla.length; i++) {
            if (tabla[i][columnaPivote] > 0) {
                cocientes[i] = tabla[i][tabla[0].length - 1] / tabla[i][columnaPivote];
            } else {
                cocientes[i] = 5000000;
            }
        }
        int menor = 0, filaPivote = 0;
        for (int i = 0; i < cocientes.length; i++) {
            if ((cocientes[i] < cocientes[menor]) && (cocientes[i] > 0)) {

                menor = i;
                filaPivote = i;
            }
        }
        System.out.println("La fila pivote tiene el numero " + tabla[filaPivote][columnaPivote] + " posicion " + (filaPivote + 1));
        return filaPivote;
    }

    public static void dividirPorPivote(float tabla[][], int filaPivote, int columnaPivote) {
        float num = tabla[filaPivote][columnaPivote];
        System.out.println("El numero para dividir es: " + num);
        for (int i = 0; i < tabla[filaPivote].length; i++) {
            tabla[filaPivote][i] /= num;
            System.out.print(tabla[filaPivote][i] + " ");
        }
        System.out.println("");
    }

    public static void eliminarFilas(float tabla[][], int filaPivote, int columnaPivote) {
        float multiplicador;
        for (int i = 0; i < tabla.length; i++) {
            if (i != filaPivote) {
                multiplicador = tabla[i][columnaPivote];
                for (int j = 0; j < tabla[i].length; j++) {
                    tabla[i][j] -= multiplicador * tabla[filaPivote][j];
                }
            }
        }
    }
    
    public static void calculoFunObj(float tabla [][], float funcionObj[]) {
        float valorOptimo=0;
        for (int i = 1; i <= tabla.length-1; i++) {
            
                for (int j = 0; j < (tabla[0].length-funcionObj.length-1); j++) {
                    if(tabla[i][j]==1){
                        System.out.println("Valor optimo en fila " + i + " columna "+ j+ " x" + (j+1) + " es " + tabla[i][tabla[0].length - 1]);
                        valorOptimo += tabla[i][tabla[0].length - 1]*funcionObj[j];
                    }
                }
            
        }
        System.out.println("El valor optimo de la solucion es " + valorOptimo);
        
    }

}
