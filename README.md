SWAnalyzer
==========

An statistical library for Semantic Web and Linked Data.

Required Python libraries:

* rdflib
* rdflib-sqlite
* rdflib-postgresql (https://github.com/RDFLib/rdflib-postgresql) (Optional)

 Installation
--------------

Install package 

	python setup.py install

Examples
	
	cd swanalyzer/tests
	python test_basic_sqlite.py
	
If you want to use PostgreSQL support install the following dependencies (optional)
	
	pip install -e git+https://github.com/RDFLib/rdflib-postgresql.git#egg=rdflib_postgresql
	
Create user *test_user* with pass *test*

	sudo -u postgres createuser -SDRP test_user
	
Create database *rdfstore*

	sudo -u postgres createdb -O test_user rdfstore -E utf-8
	
Run postgresql example
	
	python test_basic_postgresql.py

