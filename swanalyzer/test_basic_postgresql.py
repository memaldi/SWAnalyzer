from sparql_analyzer import SPARQLAnalyzer, check_sparql_endpoint

sparql_endpoint = 'http://www.morelab.deusto.es/joseki/articles'

print 'SPARQL status', check_sparql_endpoint(sparql_endpoint)
print 'SPARQL status', check_sparql_endpoint('http://www.morelab.deusto.es/joseki/articlus')

sparql_analyzer = SPARQLAnalyzer(sparql_endpoint, 'test', 'user=ckanuser password=pass host=localhost dbname=rdfstore', 'PostgreSQL')
sparql_analyzer.open()
sparql_analyzer.load_graph()

print 'URI pattern', sparql_analyzer.get_uri_pattern()
print 'Triples:', len(sparql_analyzer.get_triples())
print 'All links:', len(sparql_analyzer.get_all_links())
print 'Ingoing links:', len(sparql_analyzer.get_ingoing_links())
print 'Outgoing links:', len(sparql_analyzer.get_outgoing_links())
print 'Inner links:', len(sparql_analyzer.get_inner_links())

property_list = []
for p in sparql_analyzer.get_properties():
    property_list.append(str(p[0].encode('utf-8')))

print sparql_analyzer.get_patterns(property_list)

sparql_analyzer.close();

