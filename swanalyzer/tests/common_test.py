from swanalyzer.sparql_analyzer import check_sparql_endpoint

def checkEnpoints(valid, invalid):
	print 'SPARQL status of %s: %s' % (valid, check_sparql_endpoint(valid))
	print 'SPARQL status of %s: %s' % (invalid, check_sparql_endpoint(invalid))

def basicTest(sparql_analyzer):
	sparql_analyzer.open()
	sparql_analyzer.load_graph()
	
	print 'Graph loaded'
	
	print 'URI pattern', sparql_analyzer.get_uri_pattern()
	
	print ''
	print 'Triples:', sparql_analyzer.count_triples()
	print 'Classes:', sparql_analyzer.count_classes()
	print 'All links:', sparql_analyzer.count_all_links()
	print 'Ingoing links:', sparql_analyzer.count_ingoing_links()
	print 'Outgoing links:', sparql_analyzer.count_outgoing_links()
	print 'Inner links:', sparql_analyzer.count_inner_links()

	property_list = []
	for p in sparql_analyzer.get_properties():
		property_list.append(str(p[0].encode('utf-8')))

	print sparql_analyzer.get_patterns(property_list)

	sparql_analyzer.close();
