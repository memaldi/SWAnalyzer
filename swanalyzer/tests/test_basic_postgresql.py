from swanalyzer.sparql_analyzer import SPARQLAnalyzer
from common_test import checkEnpoints, basicTest

sparql_endpoint = 'http://www.morelab.deusto.es/joseki/articles'
invalid_enpoint = 'http://helheim.deusto.es/NOT_FOUND/'

USER = 'test_user'
PASS = 'test'
HOST = 'localhost'
DB_NAME = 'rdfstore'

checkEnpoints(sparql_endpoint, invalid_enpoint)

sparql_analyzer = SPARQLAnalyzer(sparql_endpoint, 'test', 'user=%s password=%s host=%s dbname=%s' % (USER, PASS, HOST, DB_NAME), 'PostgreSQL')

basicTest(sparql_analyzer)


