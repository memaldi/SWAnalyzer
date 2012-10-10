# -*- coding: utf-8 -*-

from sparql_analyzer import SPARQLAnalyzer
import httplib

sparql_analyzer = SPARQLAnalyzer('http://sparql.reegle.info/', 'test', 'user=postgres,password=p0stgr3s,host=localhost,db=rdfstore')
sparql_analyzer.open()
sparql_analyzer.load_graph()

f = open('reegle.rdf', 'w')
f.write(sparql_analyzer.graph.serialize(format='pretty-xml', encoding='utf-8'))
f.close()
sparql_analyzer.close()
