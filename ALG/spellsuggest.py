# -*- coding: utf-8 -*-
import re
import test_tarea2 as distan #import of the test_tarea2.py with another name
from trie import Trie

class SpellSuggester:

    """
    Clase que implementa el método suggest para la búsqueda de términos.
    """

    def __init__(self, vocab_file_path):
        """Método constructor de la clase SpellSuggester

        Construye una lista de términos únicos (vocabulario),
        que además se utiliza para crear un trie.

        Args:
            vocab_file (str): ruta del fichero de texto para cargar el vocabulario.

        """

        self.vocabulary  = self.build_vocab(vocab_file_path, tokenizer=re.compile("\W+"))

    def build_vocab(self, vocab_file_path, tokenizer):
        """Método para crear el vocabulario.

        Se tokeniza por palabras el fichero de texto,
        se eliminan palabras duplicadas y se ordena
        lexicográficamente.

        Args:
            vocab_file (str): ruta del fichero de texto para cargar el vocabulario.
            tokenizer (re.Pattern): expresión regular para la tokenización.
        """
        with open(vocab_file_path, "r", encoding='utf-8') as fr:
            vocab = set(tokenizer.split(fr.read().lower()))
            vocab.discard('') # por si acaso
            return sorted(vocab)

    def suggest(self, term, distance="levenshtein", threshold=2):

        """Método para sugerir palabras similares siguiendo la tarea 3.

        A completar.

        Args:
            term (str): término de búsqueda.
            distance (str): algoritmo de búsqueda a utilizar
                {"levenshtein", "restricted", "intermediate"}.
            threshold (int): threshold para limitar la búsqueda
                puede utilizarse con los algoritmos de distancia mejorada de la tarea 2
                o filtrando la salida de las distancias de la tarea 2
        """

        assert distance in ["levenshtein", "restricted", "intermediate"]

        results = {} # diccionario termino:distancia
        # TODO
        #Saving the length of the term
        lengthAuxiliar = len(term)
        #Check the type of edit distance its given
        if distance == 'levenshtein':
            callAux =  distan.dp_levenshtein_threshold
        elif distance == 'restricted':
            callAux = distan.dp_restricted_damerau_threshold
        elif distance == 'intermediate':
            callAux = distan.dp_intermediate_damerau_threshold
        #Loop to check the distance between each word on the vocabulary and the term we have on the arguments
        for word in self.vocabulary:
            #Getting the actual distance
            distancia = callAux(word,term,threshold)
            #Check if the actual distance is lower than the threshold, if not, get the next word
            if distancia <= threshold:
                #We check if the word was already on the result dictionary
                if word in results:
                    #if it was already in the voc , just add the distance to that word
                    results[word].append(distancia)
                else:
                    results[word] = distancia
        return results

class TrieSpellSuggester(SpellSuggester):
    """
    Clase que implementa el método suggest para la búsqueda de términos y añade el trie
    """
    def __init__(self, vocab_file_path):
        super().__init__(vocab_file_path)
        self.trie = Trie(self.vocabulary)
    
if __name__ == "__main__":
    spellsuggester = TrieSpellSuggester("./quijote.txt")
    print(spellsuggester.suggest("casa"))
    # cuidado, la salida es enorme print(suggester.trie)

    
