from swanalyzer.sparql_analyzer import SPARQLAnalyzer
from common_test import checkEnpoints, basicTest

sparql_endpoint = 'http://dbpedia.org/sparql'
invalid_enpoint = 'http://helheim.deusto.es/NOT_FOUND/'

DB_NAME = 'test'
DB_FILE = 'NONE' #uses SPARQL Endpoint directly

checkEnpoints(sparql_endpoint, invalid_enpoint)

sparql_analyzer = SPARQLAnalyzer(sparql_endpoint, DB_NAME, DB_FILE)

basicTest(sparql_analyzer)

