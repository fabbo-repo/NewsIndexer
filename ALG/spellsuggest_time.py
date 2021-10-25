# -*- coding: utf-8 -*-
import re
import collections
import basic_distances as basic_distan
import threshold_distances as thres_distan
import trie_distances as trie_distan
from trie import Trie
from spellsuggest import SpellSuggester, TrieSpellSuggester
import sys
import time
import random

def dummy_function() :
    pass

def measure_time(function, arguments, prepare = dummy_function, prepare_args=()) :
    """
        Mide el tiempo de ejecutar function(*arguments)
        IMPORTANTE: como se puede ejecutar varias veces puede que sea
        necesario pasarle una función que establezca las condiciones
        necesarias para medir adecuadamente (ej: si mides el tiempo de
        ordenar algo y lo deja ordenado, la próxima vez que ordenes no
        estará desordenado)
        DEVUELVE: tiempo y el valor devuelto por la función
    """
    count, accum = 0, 0

    while accum < 0.1:
        prepare(*prepare_args)
        t_ini = time.process_time()
        returned_value = function(*arguments)
        accum += time.process_time()-t_ini
        count += 1
    
    return accum/count, returned_value


class TimeSpellSuggester:

    def __init__(self, vocab_file_path, talla):
        """Método constructor de la clase SpellSuggester

        Construye una lista de términos únicos (vocabulario),
        que además se utiliza para crear un trie.

        Args:
            vocab_file (str): ruta del fichero de texto para cargar el vocabulario.

        """

        tokenizer = re.compile("\W+")
        with open(vocab_file_path, "r", encoding='utf-8') as fr:
            c = collections.Counter(tokenizer.split(fr.read().lower()))
            if '' in c :
                del c['']
            
            reversed_c = [(freq, word) for (word,freq) in c.items()]
            sorted_reversed = sorted(reversed_c, reverse=True)
            sorted_vocab = [word for (freq,word) in sorted_reversed]
        
        self.vocabulary = sorted_vocab
        self.reduced_vocabulary = self.vocabulary[0:talla]
        self.trie = Trie(sorted(self.sorted_vocabulary))

    def suggest(self, term, distance="levenshtein", threshold=2, use_thres=True):

        """Método para sugerir palabras similares siguiendo la tarea 3.

        Args:
            term (str): término de búsqueda.
            distance (str): algoritmo de búsqueda a utilizar
                {"levenshtein", "restricted", "intermediate", "trielevenshtein"}.
            threshold (int): threshold para limitar la búsqueda
                puede utilizarse con los algoritmos de distancia mejorada de la tarea 2
                o filtrando la salida de las distancias de la tarea 2
            use_thres (bool): indica si va a usar o no el threshold
        """

        assert distance in ["levenshtein", "restricted", "intermediate","trielevenshtein"]
        
        results = {} # diccionario termino:distancia
        # Check the type of edit distance its given
        if distance == 'levenshtein' and not use_thres:
            callAux =  basic_distan.dp_levenshtein_backwards
        elif distance == 'restricted' and not use_thres:
            callAux = basic_distan.dp_restricted_damerau_backwards
        elif distance == 'intermediate' and not use_thres:
            callAux = basic_distan.dp_intermediate_damerau_backwards
        if distance == 'levenshtein' and use_thres:
            callAux =  thres_distan.dp_levenshtein_threshold
        elif distance == 'restricted' and use_thres:
            callAux = thres_distan.dp_restricted_damerau_threshold
        elif distance == 'intermediate' and use_thres:
            callAux = thres_distan.dp_intermediate_damerau_threshold
        elif distance == "trielevenshtein"  and use_thres:
            return trie_distan.dp_levenshtein_trie(term, self.trie, threshold)
        
        # Loop to check the distance between each word on the vocabulary 
        # and the term we have on the arguments
        for word in self.vocabulary:
            # Optimistic level of difference between lengths
            if(use_thres and abs(len(word)-len(term)) > threshold) : 
                distancia = threshold+1
            # Optimistic level based on the number of ocurrences of each character
            elif(use_thres and distance == 'levenshtein' and \
                self.count_distance(word,term) > threshold) : 
                distancia = threshold+1
            elif(use_thres) : 
                distancia = callAux(word,term,threshold)
            else : 
                distancia = callAux(word,term)
            
            # Check if the actual distance is lower than the threshold, 
            # if not, get the next word
            if distancia <= threshold:
                if word in results:
                    results[word].append(distancia)
                else:
                    results[word] = distancia
        
        return results

    
if __name__ == "__main__":
    try:
        if(len(sys.argv) != 3) :
            print('\nFaltan argumentos, deben ser 2:\
                \n\t1- path del fichero a analizar\
                \n\t2- lista de thresholds ( [1,2,3,4,...] ) \
                (levenshtein, restricted, intermediate, trielevenshtein)\
                \n\nPrueba con:\
                \n\tpython spellsuggest_time.py ../corpora/quijote.txt [1,2,3,4,5]\n')
            exit()

        path = sys.argv[1]
        # list of thresholds
        thresholds = sys.argv[2].strip('][').split(',')    # Convert a string representation of list into list

        spellsuggester = SpellSuggester(path)
        spellsuggester_trie = TrieSpellSuggester(path)
        
        # k words are chosen randomly, without repeating them
        words = random.sample(spellsuggester_trie.vocabulary, k = 10)

        t_lev = t_res = t_int = t_trie = 0
        for thres in thresholds:
            print( "\n### Threshold " + thres + " ")
            for w in words:
                # Levenstein
                t_lev += measure_time(spellsuggester.suggest,
                        [w, "levenshtein", int(thres)])[0]
                # Restricted
                t_res += measure_time(spellsuggester.suggest,
                        [w, "restricted", int(thres)])[0]
                # Intermediate
                t_int += measure_time(spellsuggester.suggest,
                        [w, "intermediate", int(thres)])[0]
                # Trielevenshtein
                t_trie += measure_time(spellsuggester_trie.suggest, 
                        [w, "trielevenshtein", int(thres)])[0]

            print("* levenstein average: " +str(t_lev/len(words)) + "\n"
                    "* restricted average: " + str(t_res/len(words)) + "\n"
                    "* intermediate average: "  + str(t_int/len(words)) + "\n"
                    "* trielevenshtein average: "  + str(t_trie/len(words)) + "\n")

    except Exception as err:
        print("\n spellsuggest class error :",sys.exc_info[0])
        sys.exit(-1)
