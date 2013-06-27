SWAnalyzer
==========

An statistical library for Semantic Web and Linked Data.

Required Python libraries:

* rdflib
* rdflib-postgresql (https://github.com/RDFLib/rdflib-postgresql) (Optional)

 Installation
--------------

Install package 

	python setup.py install

If you want to use PostgreSQL support install the following dependencies (optional)
	
	pip install -e git+https://github.com/RDFLib/rdflib-postgresql.git#egg=rdflib_postgresql

Examples
	
	cd swanalyzer/tests
	python test_basic_sqlite.py
	python test_basic_postgresql.py (Requires rdflib-postgresql)

