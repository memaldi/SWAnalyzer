from swanalyzer.sparql_analyzer import SPARQLAnalyzer
from common_test import checkEnpoints, basicTest

sparql_endpoint = 'http://helheim.deusto.es/linkedstats/sparql'
invalid_enpoint = 'http://dbpedia.org/sparql/NOT_FOUND'

DB_NAME = 'test'
DB_FILE = 'NONE' #uses SPARQL Endpoint directly

checkEnpoints(sparql_endpoint, invalid_enpoint)

sparql_analyzer = SPARQLAnalyzer(sparql_endpoint)

basicTest(sparql_analyzer)

