# NewsIndexer

The purpose of this project is the implementation in python3 of a news indexing and retrieval system. It mainly consists of the following files:

* indexer.py: Main program for news indexing. Creates a class SAR_Project to extract news from a hosted document collection in a local directory, indexes them and saves them to disk by the object instance.
* searcher.py: Main program for news retrieval. Disk loading an instance of class SAR_Project to respond to queries made to it.
* lib.py: This is the only file that provide the basic operation of the project (indexing and retrieval of news).
