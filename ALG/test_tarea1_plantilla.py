import numpy as np

##INCOMPLETO#######################################################
def dp_levenshtein_backwards(x, y) :
    return 0


##INCOMPLETO#######################################################
def dp_restricted_damerau_backwards(x, y) :
    lengthx = len(x)#guardamos la longitud de la cadena x
    lengthy = len(y)#guardamos la longitud de la cadena y
    #la matriz tendrá tantas filas y columnas como dimensiones
    # (x,y)
    matrizLev = np.zeros((lengthx,lengthy),dtype = int)
    B={}
    ############## HE INTRODUCIDO LAS 2 POSIBLES FORMAS DE HACERLO, ITERATIVO O RECURSIVO, Y SIN EMBARGO, AMBAS DAN MAL EL ULTIMO CASO ################
    ############## QUEDA PENDIENTE SABER PORQUÉ DA 2 EN VEZ DE 3 EL CASO DE ACB Y BA ##################################################################
    #Esto es terrible a todos los niveles del ser humano pero ya funciona como el output del archivo marca#
    #He añadido -1 en cada "comprobacion" de algun elemento de las listas de las cadenas de entrada porque si no esto explotaba o no funcionaba#
    #Es lento como sus muertos, ya se optimizará TODO#
    def recLR(i,j,cx,cy,B):
        D=[]
        if (i,j) in B:
            return B[i,j]
        if i==0 and j == 0:
            return 0
        if i > 0:
            D.append(recLR(i-1,j,cx,cy,B) + 1)
        if j > 0:
            D.append(recLR(i,j-1,cx,cy,B) + 1)
        if i > 0 and j > 0 and cx[i-1] == cy[j-1]:
            D.append(recLR(i-1,j-1,cx,cy,B))
        if i > 0 and j > 0 and cx[i-1] != cy[j-1]:
            D.append(recLR(i-1,j-1,cx,cy,B) + 1)
        if i > 1 and j > 1 and cx[i-2] == cy[j-1] and cx[i-1] == cy[j-2]:
            D.append(recLR(i-2,j-2,cx,cy,B) + 1)
        B[i,j] = min(D)
        return min(D)

    matrizLev[lengthx-1][lengthy-1] = recLR(lengthx,lengthy,x,y,B)
    return matrizLev[lengthx-1][lengthy-1]


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
