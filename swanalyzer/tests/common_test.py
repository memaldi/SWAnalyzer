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
	print 'Triples:', sparql_analyzer.count_triples()
	print 'Classes:', sparql_analyzer.count_classes()
	print 'All links:', sparql_analyzer.count_all_links()
	print 'Ingoing links:', sparql_analyzer.count_ingoing_links()
	print 'Outgoing links:', sparql_analyzer.count_outgoing_links()
	print 'Inner links:', sparql_analyzer.count_inner_links()
	print 'Subjects:', sparql_analyzer.count_subjects()
	print 'Objects:', sparql_analyzer.count_objects()
	print 'Properties:', sparql_analyzer.count_properties()

	property_list = []
	for p in sparql_analyzer.get_properties():
		property_list.append(str(p[0].encode('utf-8')))

	print sparql_analyzer.get_patterns(property_list)
	
	print ''
	print 'Class instances'
	for clazz, instances in sparql_analyzer.get_all_classes_instances().items():
		print 'Class %s: %s' % (clazz, instances)
		
	print ''
	print 'Vocabularies'
	for vocabulary in sparql_analyzer.get_vocabularies():
		print vocabulary

	sparql_analyzer.close();
