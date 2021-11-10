# NewsIndexer

The purpose of this project is the implementation in python3 of a news indexing and retrieval system. It mainly consists of the following files:

* indexer.py: Main program for news indexing. Creates a class SAR_Project to extract news from a hosted document collection in a local directory, indexes them and saves them to disk by the object instance.
* searcher.py: Main program for news retrieval. Disk loading an instance of class SAR_Project to respond to queries made to it.
* lib.py: This is the only file that provide the basic operation of the project (indexing and retrieval of news).


-------------------------------------
## Testing:
Execution sample for *2015* indexation:
~~~
python indexer.py corpora/news/2015 index/2015_index.bin
~~~
Output:
~~~
======================================== \
Number of indexed days: 285 
----------------------------------------
Number of indexed news: 803
----------------------------------------
TOKENS:
        # of tokens in 'article': 44684
----------------------------------------
Positional queries are NOT allowed.
========================================
Time indexing: 4.70s.
Time saving: 0.08s.
~~~
Execute a query:
~~~
python searcher.py -Q 'isla AND valencia AND pero' index/2015_index.bin
~~~
Output:
~~~
========================================
Query: isla AND valencia AND pero
Number of results: 2
--------------------
#1
0
2
date: 2015-01-03
title: Las Fuerzas Armadas: un paso al frente y dos atrás en derechos sociales
keywords: frente,derechos,Fuerzas,Armadas,sociales
#2
0
107
date: 2015-03-25
title: Diez motivos para querer vivir en Palma de Mallorca
keywords: mallorca,palma,vivir,motivos
~~~

-----------------------------------------------------------
## Project tree
~~~
NewsIndexer
├── corpora
│   ├── 2015
│   │   ├── 01
│   │   │   ├── 2015-01-02.json
│   │   │   └── ...
│   │   └── ...
│   ├── 2016
│   │   ├── 01
│   │   │   ├── 2016-01-01.json
│   │   │   └── ...
│   │   └── ...
│   └── quijote.txt
│
├── distances
│   ├── basic_distances.py
│   ├── data
│   │   ├── plot10000.png
│   │   ├── ...
│   │   └── table6000.csv
│   ├── generate_distance_results.py
│   ├── read_results.py
│   ├── results
│   │   ├── result_intermediate_quijote.txt
│   │   ├── result_levenshtein_quijote.txt
│   │   └── result_restricted_quijote.txt
│   ├── spellsuggest.py
│   ├── spellsuggest_time.py
│   ├── test
│   │   └── meld.txt
│   ├── threshold_distances.py
│   ├── trie_distances.py
│   └── utils
│       ├── graphing.py
│       ├── tables.py
│       └── trie.py
│
├── indexer.py
│
├── lib_Alterno.py
│
├── lib.py
│
├── query_results
│   ├── queries_full.txt
│   └── ...
│
├── reports
│   ├── basic_query_report.pdf
│   └── distances_query_report.pdf
│
├── searcher.py
│
├── index
│   └── ...
│
└── statistics
    ├── stats_2015_M.txt
    └── ...
~~~
