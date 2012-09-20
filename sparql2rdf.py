from sparql_analyzer import SPARQLAnalyzer
import httplib

sparql_analyzer = SPARQLAnalyzer('http://www.morelab.deusto.es/joseki/articles', 'test')
sparql_analyzer.open()
sparql_analyzer.load_graph()

f = open('morelab.rdf', 'w')
f.write(sparql_analyzer.graph.serialize(format='pretty-xml'))
f.close()
sparql_analyzer.close()
