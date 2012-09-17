import abc
import os
import ld_utils
import namespace_finder
import time
from rdflib import plugin
from rdflib.store import Store
from rdflib.graph import Graph
from tempfile import mkdtemp

class SWAnalyzer:
    def __init__(self):
        store = plugin.get('SQLite', Store)('voidstore')
        self.path = mkdtemp()
        self.configString = self.path + '/temp.db'
        self.graph = Graph(store="SQLite")

    def open(self):
        self.graph.open(self.configString, create=True)

    def close(self):
        self.graph.close()
        for f in os.listdir(self.path):
            os.unlink(self.path + '/' + f)
            os.rmdir(self.path)

    def load_graph(self):
        self.uri_pattern = self.get_uri_pattern()[1]

    def get_classes(self):    
        query = 'SELECT DISTINCT ?class WHERE { [] a ?class }'
        qres = self.graph.query(query)
        return qres.result
        
    def get_properties(self):
        query = 'SELECT DISTINCT ?p WHERE { ?s ?p ?o }'
        qres = self.graph.query(query)
        return qres.result
        
    def get_subjects(self):
        query = 'SELECT DISTINCT ?s WHERE { ?s ?p ?o }'
        qres = self.graph.query(query)
        subject_list = []
        '''for subject in qres.result:
            subject_list.append(str(subject[0]))
        f = open('subjects', 'w')
        f.write(str(subject_list))
        f.close()'''
        return qres.result
        
    def get_objects(self):
        query = 'SELECT DISTINCT ?o WHERE { ?s ?p ?o }'
        qres = self.graph.query(query)
        return qres.result
        
    def get_class_instances(self, class_name):
        query = 'SELECT DISTINCT ?s WHERE { ?s a <' + class_name + '> }'
        qres = self.graph.query(query)
        return qres.result
        
    def get_property_count(self, property_name):
        query = 'SELECT * WHERE { ?s <' + property_name + '> ?o }'
        qres = self.graph.query(query)
        return qres.result
        
    def get_entities(self):
        query = 'SELECT DISTINCT ?s WHERE { ?s a [] . FILTER ((!isBlank(?s)) && regex(str(?s), "^' + self.uri_pattern + '"))}'
        qres = self.graph.query(query)
        return qres.result

    def get_all_links(self):
        query = '''SELECT ?o WHERE { ?s ?p ?o . 
                   FILTER (!isLiteral(?o) && (str(?p) != "http://www.w3.org/1999/02/22-rdf-syntax-ns#type") && (str(?p) != "http://purl.org/dc/elements/1.1/type"))}'''
        qres = self.graph.query(query)
        return qres.result

    def get_outgoing_links(self):
        query = '''SELECT ?o WHERE { ?s ?p ?o . 
FILTER ((!isBlank(?o)) && !regex(str(?o), "''' + self.uri_pattern + '''") && isIRI(?o) && (str(?p) != "http://www.w3.org/1999/02/22-rdf-syntax-ns#type") && (str(?p) != "http://purl.org/dc/elements/1.1/type"))}'''
        qres = self.graph.query(query)
        return qres.result

    def get_uri_pattern(self):
        subjects = self.get_subjects()
        subject_list = []
        for subject in subjects:
            subject_list.append(str(subject[0]))
        return self.get_patterns(subject_list)

    def get_patterns(self, collection):
        processes = 10
        collection = [e for e in collection if e.find('http://') == 0]
        #initial = time.time()
        result = namespace_finder.find_pattern(collection, branches = processes, subprocesses = True, verbose = False)
        #end = time.time()
        #print "%s elements. %s processes, result: %s; time: %.2f second" % (len(collection), processes, str(result), end - initial)
        #print result
        return result
