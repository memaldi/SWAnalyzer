import abc
import os
import ld_utils
from rdflib import plugin
from rdflib.store import Store
from rdflib.graph import Graph
from tempfile import mkdtemp

class SWAnalyzer:
    def __init__(self):
        store = plugin.get('SQLite', Store)('voidstore')
        self.path = mkdtemp()
        self.configString = self.path + 'temp.db'
        self.graph = Graph(store="SQLite")

    def open(self):
        self.graph.open(self.configString, create=True)

    def close(self):
        self.graph.close()
        for f in os.listdir(self.path):
            os.unlink(self.path+'/'+f)
            os.rmdir(self.path)

    @abc.abstractmethod
    def load_graph():
        return

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
        query = 'SELECT DISTINCT ?s WHERE { ?s a [] . FILTER ((!isBlank(?s)) && regex(str(?s), "^' + self.get_uri_pattern() + '"))}'
        print query
        qres = self.graph.query(query)
        return qres.result

    def get_all_links(self):
        query = '''SELECT ?o WHERE { ?s ?p ?o . 
                   FILTER (!isLiteral(?o) && (str(?p) != "http://www.w3.org/1999/02/22-rdf-syntax-ns#type") && (str(?p) != "http://purl.org/dc/elements/1.1/type"))}'''
        qres = self.graph.query(query)
        return qres.result

    def get_uri_pattern(self):
        subjects = self.get_subjects()
        return self.get_patterns(subjects)

    def get_patterns(self, collection):
        uri_patterns = {}
        for subject in collection:
            if len(uri_patterns) == 0 and subject[0].find('http://') != -1:
                uri_patterns[str(subject[0])] = 1
            else:
                for key in uri_patterns.keys():
                    temp_substr = ld_utils.LongestCommonSubstring(key, str(subject[0]))
                    if temp_substr.find('http://') != -1:
                        if temp_substr in uri_patterns.keys():
                            uri_patterns[temp_substr] = uri_patterns[temp_substr] + 1
                        else:
                            uri_patterns[temp_substr] = 1
        high_index = -1
        high_index_key = ''
        for key in uri_patterns.keys():
            if high_index < uri_patterns[key]:
                high_index = uri_patterns[key]
                high_index_key = key
        return high_index_key
