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
	print 'Triples:', sparql_analyzer.get_triples_count()
	print 'Classes:', sparql_analyzer.get_classes_count()
	
	print 'Subjects:', sparql_analyzer.get_subjects_count()
	print 'Objects:', sparql_analyzer.get_objects_count()
	print 'Properties:', sparql_analyzer.get_properties_count()
	
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
		
	print 'Ingoing links:', sparql_analyzer.get_ingoing_links_count()
	print 'Inner links:', sparql_analyzer.get_inner_links_count()
	print 'Outgoing links:', sparql_analyzer.get_outgoing_links_count()
	print 'All links:', sparql_analyzer.get_all_links_count()

	sparql_analyzer.close();
