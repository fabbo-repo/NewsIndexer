#############################################################################################
#    Distancia de Levenstein
#############################################################################################
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

#############################################################################################
#    Distancia de Damerau-Levenstein restringida
#############################################################################################
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
    return current[-1]

#############################################################################################
#    Distancia de Damerau-Levenstein intermedia
#############################################################################################
def dp_intermediate_damerau_backwards(x, y) :
    lenx = len(x) # longitud de la cadena x
    leny = len(y) # longitud de la cadena y
    cte = 1 # constante prefijada a 1 considerando coste(acb, ba)=2 y coste(ab, bca)=2

    # current, prev1, prev2 y prev3 almacenaran las distancias de cada caracter
    # de forma eficiente
    prev2 = []; prev1 = []; current = []
    for i in range(0, lenx+1) : 
        prev3 = prev2; prev2 = prev1; prev1 = current; current = []
        for j in range(0, leny+1) :
            D=[]
            if i==0 and j == 0 : D.append(0)
            if i > 0 : D.append(prev1[j] + 1)
            if j > 0 : D.append(current[j-1] + 1)
            if i > 0 and j > 0 :
                D.append(prev1[j-1] + (x[i-1] != y[j-1]))
            if i > 1 and j > 1 and x[i-2] == y[j-1] and x[i-1] == y[j-2] :
                D.append(prev2[j-2] + 1)

            # Condiciones adicionales:
            # Teniendo el ejemplo de x=ab e y=bca :
            elif i > 1 and j > 1+cte and x[i-2] == y[j-1] and x[i-1] == y[j-2-cte] : 
                D.append(prev2[j-3] + 2)
            # Y lo contrario, x=bca e y=ab :
            elif i > 1+cte and j > 1 and x[i-2-cte] == y[j-1] and x[i-1] == y[j-2] : 
                D.append(prev3[j-2] + 2)

            # Se añade el mínimo de las distancias a current
            current.append(min(D))
    return current[-1]


#############################################################################################
#    Pruebas:
#############################################################################################
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
