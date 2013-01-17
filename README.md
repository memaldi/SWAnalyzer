SWAnalyzer
==========

An statistical library for Semantic Web and Linked Data.

Required Python libraries:

* rdflib 3.2.1
* rdfextras 0.2
* rdflib-postgresql 0.1 (https://github.com/RDFLib/rdflib-postgresql)

 Installation
--------------

Install package 

	python setup.py install

If you want to use PostreSQL support install the following dependencies
	
	pip install -e git+https://github.com/RDFLib/rdflib-postgresql.git#egg=rdflib_posgresql
