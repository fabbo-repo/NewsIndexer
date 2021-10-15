from trie import Trie

#############################################################################################
#    Levenstein Trie Distance
#############################################################################################
def dp_levenshtein_trie(x, trie, th) :
    lengthX = len(x)
    lengthY = len(y)     # m

    # Initialize 1st column of the array to [0,1,2,...,m]
    prev = [i for i in range(lengthY+1)]
    current = [1]

    for i in range(lengthX) :
        for j in range(lengthY) :
            if x[i]==y[j]: current.append(min(prev[j], prev[j+1]+1, current[j]+1))
            else: current.append(min(prev[j]+1, prev[j+1]+1, current[j]+1))
            
        if(min(current) > th) : return th + 1
        
        # Empty list for next iteration
        if i!=lengthX-1:
            prev = current      # list is copied by reference
            current = [i+2]     # no longer copied by reference

    return current[-1]

#############################################################################################
#    Restricted Damerau-Levenstein Trie Distance
#############################################################################################
def dp_restricted_damerau_trie(x, trie, th) :
    lenx = len(x); leny = len(y) # x and y string length
    
    # current, prev1 y prev2 prev2 will efficiently store the distances 
    # of each character 
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
            # The minimum of the distances is added to current
            current.append(min(D))
        if(min(current) > th) : return th+1
    
    return current[-1]

#############################################################################################
#    Intermediate Damerau-Levenstein Trie Distance
#############################################################################################
def dp_intermediate_damerau_trie(x, trie, th) :
    lenx = len(x); leny = len(y)
    cte = 1 # constant preset to 1 considering cost(acb, ba)=2 and cost(ab, bca)=2

    # In this case prev3 is needed to store extra distances
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
            # Adittional conditions:
            # Having the example of x=ab and y=bca:
            elif i > 1 and j > 1+cte and x[i-2] == y[j-1] and x[i-1] == y[j-2-cte] : 
                D.append(prev2[j-3] + 2)
            # And the opposite, x=bca and y=ab:
            elif i > 1+cte and j > 1 and x[i-2-cte] == y[j-1] and x[i-1] == y[j-2] : 
                D.append(prev3[j-2] + 2)
            # The minimum of the distances is added to current
            current.append(min(D))
        
        if(min(current) > th) : return th+1
    
    return current[-1]


#############################################################################################
#    Tests:
#############################################################################################
words = ["algortimo", "algortximo","lagortimo", "agaloritom", "algormio", "ba"]
words.sort()
trie = Trie(words)

test = ["algoritmo", "acb"]
thrs = range(1, 4)

for threshold in thrs:
    print(f"threshols: {threshold:3}")
    for x in test:
        for dist,name in (
                    (dp_levenshtein_trie,"levenshtein"),
                    (dp_restricted_damerau_trie,"restricted"),
                    (dp_intermediate_damerau_trie,"intermediate"),
                    ):
            print(f"\t{x:12} \t{name}\t", end="")
            print(dist(x, trie, threshold))
                 
"""
Salida del programa:

threshols:   1
	algoritmo    	levenshtein	[]
	algoritmo    	restricted	[('algortimo', 1)]
	algoritmo    	intermediate	[('algortimo', 1)]
	acb          	levenshtein	[]
	acb          	restricted	[]
	acb          	intermediate	[]
threshols:   2
	algoritmo    	levenshtein	[('algortimo', 2)]
	algoritmo    	restricted	[('algortimo', 1), ('lagortimo', 2)]
	algoritmo    	intermediate	[('algormio', 2), ('algortimo', 1), ('lagortimo', 2), ('algortximo', 2)]
	acb          	levenshtein	[]
	acb          	restricted	[]
	acb          	intermediate	[('ba', 2)]
threshols:   3
	algoritmo    	levenshtein	[('algormio', 3), ('algortimo', 2), ('algortximo', 3)]
	algoritmo    	restricted	[('algormio', 3), ('algortimo', 1), ('lagortimo', 2), ('algortximo', 3)]
	algoritmo    	intermediate	[('algormio', 2), ('algortimo', 1), ('lagortimo', 2), ('agaloritom', 3), ('algortximo', 2)]
	acb          	levenshtein	[('ba', 3)]
	acb          	restricted	[('ba', 3)]
	acb          	intermediate	[('ba', 2)]

"""         
