from swanalyzer.sparql_analyzer import SPARQLAnalyzer
from common_test import checkEnpoints, basicTest

sparql_endpoint = 'http://www.morelab.deusto.es/joseki/articles'
invalid_enpoint = 'http://helheim.deusto.es/NOT_FOUND/'

DB_NAME = 'test'
DB_FILE = 'swanalyzer.sqlite'

checkEnpoints(sparql_endpoint, invalid_enpoint)

sparql_analyzer = SPARQLAnalyzer(sparql_endpoint, DB_NAME, DB_FILE, store='SQLite')

basicTest(sparql_analyzer)

