# Ejecución de test

#### 2 formas de hacer test

1.  Comandos 

     -BL, --blevensh       basic levenshtein distance.
     -RL, --rlevensh       restricted levenshtein distance.
     -IL, --ilevensh       intermediate levenshtein distance.
     -Th threshold, --threshold threshold

```shell
python searcher.py index/2015_index.bin -T .\test\test.txt -BL -Th 2
```

​	Hay que cambiar codigo en la linea 94 del searcher.py para utilizar diferentes estrategias de distancias. Por ejemplo : 

```python
query, reference = aux[0], aux[1] # corresponde con basic levenshtein, threshold=1
query, reference = aux[0], aux[2] # corresponde con basic levenshtein, threshold=2
query, reference = aux[0], aux[3] # corresponde con basic levenshtein, threshold=3
query, reference = aux[0], aux[4] # corresponde con  restricted levenshtein, threshold=1
query, reference = aux[0], aux[5] # corresponde con  restricted levenshtein, threshold=2
...
...
query, reference = aux[0], aux[9] # corresponde con intermediate levenshtein, threshold=3
```



2.  test.py

   El unittest hace automáticamente los tests que corresponden a cada una de las estrategias de distancias.

```shell
 python .\test\test.py            
```

