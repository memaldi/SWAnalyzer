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
	print 'Triples:', len(sparql_analyzer.get_triples())
	print 'Classes:', len(sparql_analyzer.get_classes())
	print 'All links:', len(sparql_analyzer.get_all_links())
	print 'Ingoing links:', len(sparql_analyzer.get_ingoing_links())
	print 'Outgoing links:', len(sparql_analyzer.get_outgoing_links())
	print 'Inner links:', len(sparql_analyzer.get_inner_links())
	print 'Subjects:', len(sparql_analyzer.get_subjects())
	print 'Objects:', len(sparql_analyzer.get_objects())
	print 'Properties:', len(sparql_analyzer.get_properties())
	
	print ''
	print 'Class instances'
	for clazz, instances in sparql_analyzer.get_all_classes_instances().items():
		print 'Class %s: %s' % (clazz, instances)
		
	print ''
	print 'Vocabularies'
	for vocabulary in sparql_analyzer.get_vocabularies():
		print vocabulary
		
	print ''
	print 'Have predicate'
	for predicate, triples in sparql_analyzer.get_all_predicate_triples().items():
		print 'Predicate %s: %s' % (predicate, triples)

	sparql_analyzer.close();
