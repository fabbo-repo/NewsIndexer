#import numpy as np

##INCOMPLETO#######################################################
def dp_levenshtein_backwards(x, y) :
    lengthX = len(x)
    lengthY = len(y)  # m

    # Inicializar columna Y a [0,1,2,...,m]
    prev = [i for i in range(lengthY+1)]
    current = [1]

    for i in range(lengthX):
        for j in range(lengthY):
            if x[i]==y[j]: current.append(min(prev[j], prev[j+1]+1, current[j]+1))
            else: current.append(min(prev[j]+1, prev[j+1]+1, current[j]+1))

        # print(current) para ver la matriz transpuesta
        # Vaciar lista para siguiente iteración
        if i!=lengthX-1:
            prev = current  # paso por referencia
            current = [i+2]  # ahora ya no por referencia

    return current[-1]

#########################################################
def dp_restricted_damerau_backwards(x, y) :
    lenx = len(x) # longitud de la cadena x
    leny = len(y) # longitud de la cadena y
    
    # current, prev1 y prev2 almacenaran las distancias de cada caracter
    # de forma eficiente
    prev1 = []; current = []
    for i in range(0, lenx+1) : 
        prev2 = prev1; prev1 = current; current = []
        for j in range(0, leny+1) :
            D=[]
            if i==0 and j == 0 : D.append(0)
            if i > 0 : D.append(prev1[j] + 1)
            if j > 0 : D.append(current[j-1] + 1)
            if i > 0 and j > 0 :
                D.append(prev1[j-1] + (x[i-1] != y[j-1]))
            if i > 1 and j > 1 and x[i-2] == y[j-1] and x[i-1] == y[j-2] :
                D.append(prev2[j-2] + 1)
            # Se añade el mínimo de las distancias a current
            current.append(min(D))
        #print(current)
    return current[leny]


##INCOMPLETO#######################################################
def dp_intermediate_damerau_backwards(x, y) :
    return 0
    lenx = len(x); leny = len(y)
    cte = 1
    # matriz tendrá tantas filas como caracteres en x
    # y tantas columnas como caracteres en y 
    matriz = np.zeros( (lenx, leny) , dtype=int)
    for i in range(0, lenx) : 
        for j in range(0, leny) :
            D = []
            if i==0 and j==0 : D.append(0)
            if i>0 : D.append(matriz[i-1][j] + 1)
            if j>0 : D.append(matriz[i][j-1] + 1)
            if i>0 and j>0 : 
                D.append(matriz[i-1][j-1] + (x[i]!=y[j]))
            # Condicion adicional
            # if i+j+1 < np.abs(i-j) : matriz[i-1][j-1]
            matriz[i][j] = min(D)
    return matriz[lenx-1][leny-1]

test = [("algoritmo","algortimo"),
        ("algoritmo","algortximo"),
        ("algoritmo","lagortimo"),
        ("algoritmo","agaloritom"),
        ("algoritmo","algormio"),
        ("acb","ba")]

for x,y in test:
    print(f"{x:12} {y:12}",end="")
    for dist,name in ((dp_levenshtein_backwards,"levenshtein"),
                      (dp_restricted_damerau_backwards,"restricted"),
                      (dp_intermediate_damerau_backwards,"intermediate")):
        print(f" {name} {dist(x,y):2}",end="")
    print()
                 
"""
Salida del programa:

algoritmo    algortimo    levenshtein  2 restricted  1 intermediate  1
algoritmo    algortximo   levenshtein  3 restricted  3 intermediate  2
algoritmo    lagortimo    levenshtein  4 restricted  2 intermediate  2
algoritmo    agaloritom   levenshtein  5 restricted  4 intermediate  3
algoritmo    algormio     levenshtein  3 restricted  3 intermediate  2
acb          ba           levenshtein  3 restricted  3 intermediate  2
"""         
