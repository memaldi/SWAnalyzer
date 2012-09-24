import unittest
import cProfile
import time
from sparql_analyzer import SPARQLAnalyzer
from dump_analyzer import DumpAnalyzer

class SPARQLAnalyzerTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.sparql_analyzer = SPARQLAnalyzer('http://www.morelab.deusto.es/joseki/articles', 'test')
        self.sparql_analyzer.open()
        self.sparql_analyzer.load_graph()


    @classmethod
    def tearDownClass(self):
        self.sparql_analyzer.close()

    def test_get_classes(self):
        expected_classes = 13
        result_classes = len(self.sparql_analyzer.get_classes())
        self.assertEqual(result_classes, expected_classes)

    def test_get_properties(self):
        expected_properties = 79
        result_properties = len(self.sparql_analyzer.get_properties())
        self.assertEqual(result_properties, expected_properties)

    def test_get_subjects(self):
        expected_subjects = 241
        result_subjects = len(self.sparql_analyzer.get_subjects())
        self.assertEqual(result_subjects, expected_subjects)

    def test_get_objects(self):
        expected_objects = 1341
        result_objects = len(self.sparql_analyzer.get_objects())
        self.assertEqual(result_objects, expected_objects)

    def test_get_class_instances(self):
        expected_class_instances = 57
        result_class_instances = len(self.sparql_analyzer.get_class_instances('http://swrc.ontoware.org/ontology#Article'))
        self.assertEqual(result_class_instances, expected_class_instances)

    def test_get_property_count(self):
        expected_property_count = 478
        result_property_count = len(self.sparql_analyzer.get_property_count('http://xmlns.com/foaf/0.1/maker'))
        self.assertEqual(result_property_count, expected_property_count)

    def test_get_all_links(self):
        expected_links = 1877
        result_links = len(self.sparql_analyzer.get_all_links())
        self.assertEqual(result_links, expected_links)

    def test_get_uri_pattern(self):
        #t1 = time.time()
        expected_uri_pattern = 'http://www.morelab.deusto.es/resource/'
        result_uri_pattern = self.sparql_analyzer.get_uri_pattern()
        #t2 = time.time()
        #print t2-t1
        #print result_uri_pattern
        self.assertEqual(result_uri_pattern[1], expected_uri_pattern)

    def test_get_entities(self):
        expected_entities = 192
        result_entities = len(self.sparql_analyzer.get_entities())
        self.assertEqual(result_entities, expected_entities)

    def test_get_outgoing_links(self):
        expected_outgoing_links = 997
        result_outgoing_links = len(self.sparql_analyzer.get_outgoing_links())
        self.assertEqual(result_outgoing_links, expected_outgoing_links)

    '''def test_get_patterns(self):
        expected_pattern = 'http://www.morelab.deusto.es/resource/'
        result_pattern = self.sparql_analyzer.get_patterns(url_list)
        self.assertEqual(result_pattern, expected_pattern)'''

    def test_get_linksets(self):
        expected_linksets = eval("{'http://dbpedia.org/': {'http://xmlns.com/foaf/0.1/based_near': 1, 'http://xmlns.com/foaf/0.1/topic_interest': 5, 'http://xmlns.com/foaf/0.1/interest': 42}, 'http://dblp.rkbexplorer.com/id/': {'http://www.w3.org/2002/07/owl#sameAs': 36}, 'http://dx.doi.org/': {'http://www.w3.org/2000/01/rdf-schema#seeAlso': 18}}")
        result_linksets = self.sparql_analyzer.get_linksets()
        self.assertEqual(result_linksets, expected_linksets)

class SPARQLAnalyzerInitialitation(unittest.TestCase):

    def setUp(self):
        self.sparql_analyzer = SPARQLAnalyzer('http://www.morelab.deusto.es/joseki/articles', 'test')
        self.sparql_analyzer.open()

    def tearDown(self):
        self.sparql_analyzer.close()

    def test_load_graph(self):
        expected_triples = 3843
        self.sparql_analyzer.load_graph()
        result_triples = len(self.sparql_analyzer.graph)
        self.assertEqual(result_triples, expected_triples)

class DumpAnalyzerTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.sparql_analyzer = DumpAnalyzer('morelab.rdf', 'test')
        self.sparql_analyzer.open()
        self.sparql_analyzer.load_graph()

    @classmethod
    def tearDownClass(self):
        self.sparql_analyzer.close()

    def test_get_classes(self):
        expected_classes = 13
        result_classes = len(self.sparql_analyzer.get_classes())
        self.assertEqual(result_classes, expected_classes)

    def test_get_properties(self):
        expected_properties = 79
        result_properties = len(self.sparql_analyzer.get_properties())
        self.assertEqual(result_properties, expected_properties)

    def test_get_subjects(self):
        expected_subjects = 241
        result_subjects = len(self.sparql_analyzer.get_subjects())
        self.assertEqual(result_subjects, expected_subjects)

    def test_get_objects(self):
        expected_objects = 1341
        result_objects = len(self.sparql_analyzer.get_objects())
        self.assertEqual(result_objects, expected_objects)

    def test_get_class_instances(self):
        expected_class_instances = 57
        result_class_instances = len(self.sparql_analyzer.get_class_instances('http://swrc.ontoware.org/ontology#Article'))
        self.assertEqual(result_class_instances, expected_class_instances)

    def test_get_property_count(self):
        expected_property_count = 478
        result_property_count = len(self.sparql_analyzer.get_property_count('http://xmlns.com/foaf/0.1/maker'))
        self.assertEqual(result_property_count, expected_property_count)

    def test_get_all_links(self):
        expected_links = 1877
        result_links = len(self.sparql_analyzer.get_all_links())
        self.assertEqual(result_links, expected_links)

    def test_get_uri_pattern(self):
        #t1 = time.time()
        expected_uri_pattern = 'http://www.morelab.deusto.es/resource/'
        result_uri_pattern = self.sparql_analyzer.get_uri_pattern()
        #t2 = time.time()
        #print t2-t1
        #print result_uri_pattern
        self.assertEqual(result_uri_pattern[1], expected_uri_pattern)

    def test_get_entities(self):
        expected_entities = 192
        result_entities = len(self.sparql_analyzer.get_entities())
        self.assertEqual(result_entities, expected_entities)

    def test_get_outgoing_links(self):
        expected_outgoing_links = 997
        result_outgoing_links = len(self.sparql_analyzer.get_outgoing_links())
        self.assertEqual(result_outgoing_links, expected_outgoing_links)

    '''def test_get_patterns(self):
        expected_pattern = 'http://www.morelab.deusto.es/resource/'
        result_pattern = self.sparql_analyzer.get_patterns(url_list)
        self.assertEqual(result_pattern, expected_pattern)'''

    def test_get_linksets(self):
        expected_linksets = eval("{'http://dbpedia.org/': {'http://xmlns.com/foaf/0.1/based_near': 1, 'http://xmlns.com/foaf/0.1/topic_interest': 5, 'http://xmlns.com/foaf/0.1/interest': 42}, 'http://dblp.rkbexplorer.com/id/': {'http://www.w3.org/2002/07/owl#sameAs': 36}, 'http://dx.doi.org/': {'http://www.w3.org/2000/01/rdf-schema#seeAlso': 18}}")
        result_linksets = self.sparql_analyzer.get_linksets()
        self.assertEqual(result_linksets, expected_linksets)

if __name__ == '__main__':
    unittest.main()
