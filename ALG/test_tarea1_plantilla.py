import numpy as np

##INCOMPLETO#######################################################
def dp_levenshtein_backwards(x, y) :
    return 0


##INCOMPLETO#######################################################
def dp_restricted_damerau_backwards(x, y) :
    return 0


##INCOMPLETO#######################################################
def dp_intermediate_damerau_backwards(x, y) :
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
            if i+j+1 < np.abs(i-j) : matriz[i-1][j-1]
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
