# -*- coding: utf-8 -*-

import abc
import os
import ld_utils
import namespace_finder
import time
import httplib
from rdflib import plugin
from rdflib import store
from rdflib.store import Store
from rdflib.graph import Graph
from rdflib.term import URIRef
from tempfile import mkdtemp
from django.core.validators import URLValidator
from urlparse import urlparse
from multiprocessing import Pool
from itertools import repeat
import urllib2
from rdflib_sparqlstore import SPARQLStore

def get_obj_from_prefix(prefix, graph, uri_pattern):
    query = 'SELECT DISTINCT ?o WHERE {?s ?p ?o . FILTER (regex(str(?o), "^' + prefix + '", "i") && !regex(str(?o), "^' + uri_pattern + '", "i"))}'
    qres = graph.query(query)
    return qres.result

def check_for_semantic((dataset, uri_pattern, identifier, configString)):
    #print configString
    #print identifier
    g = Graph(store='PostgreSQL', identifier=identifier)
    #print identifier, configString
    g.open(configString, create=False)
    #print len(g)
    #print g
    objs = get_obj_from_prefix(dataset, g, uri_pattern)
    #print objs
    #headers = {"Accept": "application/rdf+xml"}
    linksets = {}
    #print dataset, len(objs)
    for obj in objs:
        try:
            #conn = httplib.HTTPConnection(url.netloc, timeout=30)
            #conn.request("GET", url.path, "", headers)
            #print str(obj[0])
            request = urllib2.Request(str(obj[0]))
            request.add_header('Accept', 'application/rdf+xml')
            response = urllib2.urlopen(request)
            #response = conn.getresponse()
            
            #print response.headers['content-type']
            #print str(obj[0]), response.code
            if 'application/rdf+xml' in response.headers['content-type']:
                query = 'SELECT ?p WHERE {?s ?p <' + str(obj[0]) + '>}'
                qres = g.query(query)
                result = qres.result
                for p in result:
                    if dataset in linksets:
                        if str(p[0]) in linksets[dataset]:
                            linksets[dataset][str(p[0])] = linksets[dataset][str(p[0])] + 1
                        else:
                            linksets[dataset][str(p[0])] = 1
                    else:
                        linksets[dataset] = {str(p[0]): 1}
        except Exception as e:
            print e
            #print dataset + ' timed out!'
            return linksets
    #print linksets
    return linksets

class SWAnalyzer:
    def __init__(self, sparql_endpoint, identifier, configstring, store=None, proxy=None, subprocess=True):
        self.sparql_endpoint = sparql_endpoint
        self.store = store
        
        if store is None:
            print 'Creating SPARQLStore for %s' % self.sparql_endpoint
            store = SPARQLStore(self.sparql_endpoint)
            self.graph = Graph(store)
        else:
            self.identifier = URIRef(identifier)
            self.configstring = configstring
            self.graph = Graph(store, identifier=self.identifier)
            
        self.subprocess = subprocess
            
        if proxy != None:
            print 'Initilizing proxy...'
            proxy = urllib2.ProxyHandler({'http': urlparse(proxy).netloc})
            opener = urllib2.build_opener(proxy)
            urllib2.install_opener(opener)

    #@abc.abstractmethod
    def open(self):
        if self.store is not None:
            self.graph.open(self.configstring, create=True)

    def close(self):
        if self.store is not None:
            self.graph.destroy(self.configstring)
            
        self.graph.close()

    def load_graph(self):
        self.uri_pattern = self.get_uri_pattern()[1]

    def get_triples(self):
        query = 'SELECT DISTINCT * { ?s ?p ?o }'
        qres = self.graph.query(query)
        return qres.result
        
    def get_triples_count(self):
        query = 'SELECT (COUNT(*) AS ?no) { ?s ?p ?o  }'
        qres = self.graph.query(query)
        return int(qres.result[0][0])

    def get_classes(self):    
        query = 'SELECT DISTINCT ?class WHERE { [] a ?class }'
        qres = self.graph.query(query)
        return qres.result
        
    def get_classes_count(self):
        query = 'SELECT COUNT(distinct ?o) AS ?no { ?s rdf:type ?o }'
        qres = self.graph.query(query)
        return int(qres.result[0][0])
        
    def get_properties(self):
        query = 'SELECT DISTINCT ?p WHERE { ?s ?p ?o }'
        qres = self.graph.query(query)
        return qres.result
        
    def get_properties_count(self):
        query = 'SELECT COUNT(distinct ?p) AS ?no WHERE { ?s ?p ?o }'
        qres = self.graph.query(query)
        return int(qres.result[0][0])
        
    def get_subjects(self):
        query = 'SELECT DISTINCT ?s WHERE { ?s ?p ?o }'
        qres = self.graph.query(query)
        return qres.result
        
    def get_subjects_count(self):
        query = 'SELECT COUNT(distinct ?s) WHERE { ?s ?p ?o }'
        qres = self.graph.query(query)
        return int(qres.result[0][0])
        
    def get_properties_count(self):
        query = 'SELECT COUNT(distinct ?s) AS ?no WHERE { ?s ?p ?o }'
        qres = self.graph.query(query)
        return int(qres.result[0][0])
        
    def get_objects(self):
        query = 'SELECT DISTINCT ?o WHERE { ?s ?p ?o }'
        qres = self.graph.query(query)
        return qres.result
        
    def get_objects_count(self):
        query = 'SELECT COUNT(distinct ?o) AS ?no WHERE { ?s ?p ?o }'
        qres = self.graph.query(query)
        return int(qres.result[0][0])
        
    def get_class_instances(self, class_name):
        query = 'SELECT DISTINCT ?s WHERE { ?s a <' + class_name + '> }'
        qres = self.graph.query(query)
        return qres.result
        
    def get_class_instances_count(self, class_name):
        query = 'SELECT COUNT(distinct ?s) AS ?no WHERE { ?s a <' + class_name + '> }'
        qres = self.graph.query(query)
        return int(qres.result[0][0])
        
    def get_all_classes_instances(self):
        instances = {}
        for c in self.get_classes():
            clazz = str(c[0].encode('utf-8'))
            instances[clazz] = self.get_class_instances_count(clazz)
        return instances
        
    def get_all_predicate_triples(self):
        predicates = {}
        for p in self.get_properties():
            predicate = str(p[0].encode('utf-8'))
            predicates[predicate] = self.get_property_count(predicate)
        return predicates
        
    def get_property(self, property_name):
        query = 'SELECT * WHERE { ?s <' + property_name + '> ?o }'
        qres = self.graph.query(query)
        return qres.result
        
    def get_property_count(self, property_name):
        query = 'SELECT (COUNT(*) AS ?no) WHERE { ?s <' + property_name + '> ?o }'
        qres = self.graph.query(query)
        return int(qres.result[0][0])
                
    def get_entities(self):
        query = 'SELECT DISTINCT ?s WHERE { ?s a [] . FILTER ((!isBlank(?s)) && regex(str(?s), "^' + self.uri_pattern + '"))}'
        qres = self.graph.query(query)
        return qres.result
        
    def get_entities_count(self):
        query = 'SELECT COUNT(distinct ?s) AS ?no WHERE { ?s a [] . FILTER ((!isBlank(?s)) && regex(str(?s), "^' + self.uri_pattern + '"))}'
        qres = self.graph.query(query)
        return int(qres.result[0][0])
        
    def get_all_links(self):
        query = '''SELECT * WHERE { ?s ?p ?o . 
                   FILTER (!isBlank(?s) && !isBlank(?o) && isIRI(?s) && isIRI(?o) && (str(?p) != "http://www.w3.org/1999/02/22-rdf-syntax-ns#type") && (str(?p) != "http://purl.org/dc/elements/1.1/type"))}'''
        qres = self.graph.query(query)
        return qres.result
        
    def get_all_links_count(self):
        query = '''SELECT (COUNT(*) AS ?no) WHERE { ?s ?p ?o . 
                   FILTER (!isBlank(?s) && !isBlank(?o) && isIRI(?s) && isIRI(?o) && (str(?p) != "http://www.w3.org/1999/02/22-rdf-syntax-ns#type") && (str(?p) != "http://purl.org/dc/elements/1.1/type"))}'''
        qres = self.graph.query(query)
        return int(qres.result[0][0])

    def get_ingoing_links(self):
        query = '''SELECT * WHERE { ?s ?p ?o . 
FILTER (!isBlank(?s) && !isBlank(?o) && !regex(str(?s), "''' + self.uri_pattern + '''") && isIRI(?s) && regex(str(?o), "''' + self.uri_pattern + '''") && isIRI(?o) && (str(?p) != "http://www.w3.org/1999/02/22-rdf-syntax-ns#type") && (str(?p) != "http://purl.org/dc/elements/1.1/type"))}'''
        qres = self.graph.query(query)
        return qres.result

    def get_ingoing_links_count(self):
        query = '''SELECT (COUNT(*) AS ?no) WHERE { ?s ?p ?o . 
FILTER (!isBlank(?s) && !isBlank(?o) && !regex(str(?s), "''' + self.uri_pattern + '''") && isIRI(?s) && regex(str(?o), "''' + self.uri_pattern + '''") && isIRI(?o) && (str(?p) != "http://www.w3.org/1999/02/22-rdf-syntax-ns#type") && (str(?p) != "http://purl.org/dc/elements/1.1/type"))}'''
        qres = self.graph.query(query)
        return int(qres.result[0][0])

    def get_outgoing_links(self):
        query = '''SELECT * WHERE { ?s ?p ?o . 
FILTER (!isBlank(?s) && !isBlank(?o) && regex(str(?s), "''' + self.uri_pattern + '''") && isIRI(?s) && !regex(str(?o), "''' + self.uri_pattern + '''") && isIRI(?o) && (str(?p) != "http://www.w3.org/1999/02/22-rdf-syntax-ns#type") && (str(?p) != "http://purl.org/dc/elements/1.1/type"))}'''
        qres = self.graph.query(query)
        return qres.result
        
    def get_outgoing_links_count(self):
        query = '''SELECT (COUNT(*) AS ?no) WHERE { ?s ?p ?o . 
FILTER (!isBlank(?s) && !isBlank(?o) && regex(str(?s), "''' + self.uri_pattern + '''") && isIRI(?s) && !regex(str(?o), "''' + self.uri_pattern + '''") && isIRI(?o) && (str(?p) != "http://www.w3.org/1999/02/22-rdf-syntax-ns#type") && (str(?p) != "http://purl.org/dc/elements/1.1/type"))}'''
        qres = self.graph.query(query)
        return int(qres.result[0][0])

    def get_inner_links(self):
        query = '''SELECT * WHERE { ?s ?p ?o . 
FILTER (!isBlank(?s) && !isBlank(?o) && regex(str(?s), "''' + self.uri_pattern + '''") && isIRI(?s) && regex(str(?o), "''' + self.uri_pattern + '''") && isIRI(?o) && (str(?p) != "http://www.w3.org/1999/02/22-rdf-syntax-ns#type") && (str(?p) != "http://purl.org/dc/elements/1.1/type"))}'''
        qres = self.graph.query(query)
        return qres.result
        
    def get_inner_links_count(self):
        query = '''SELECT (COUNT(*) AS ?no) WHERE { ?s ?p ?o . 
FILTER (!isBlank(?s) && !isBlank(?o) && regex(str(?s), "''' + self.uri_pattern + '''") && isIRI(?s) && regex(str(?o), "''' + self.uri_pattern + '''") && isIRI(?o) && (str(?p) != "http://www.w3.org/1999/02/22-rdf-syntax-ns#type") && (str(?p) != "http://purl.org/dc/elements/1.1/type"))}'''
        qres = self.graph.query(query)
        return int(qres.result[0][0])
        
    def get_vocabularies(self):
        property_list = [str(p[0].encode('utf-8')) for p in self.get_properties()]
        return self.get_patterns(property_list)

    def get_uri_pattern(self):
        subjects = self.get_subjects()
        subject_list = []
        for subject in subjects:
            subject_list.append(str(subject[0].encode('utf-8')))
        return self.get_pattern(subject_list)

    def get_pattern(self, collection):
        processes = 10
        collection = [e for e in collection if e.find('http://') == 0]
        result = namespace_finder.find_pattern(collection, branches = processes, subprocesses = False, verbose = False)
        return result

    def get_patterns(self, uri_list):
        temp_list = []
        temp_list += uri_list

        patterns = []
        while len(temp_list) > 0:
            pos = temp_list[0].rfind('#')
            if pos == -1:
                pos = temp_list[0].rfind('/')
            if pos > -1:
                pattern = temp_list[0][:pos]
                patterns.append(pattern)
                temp_list = [e for e in temp_list if not e.startswith(pattern)]
        return patterns

    def map_subprocess(self, data):
        if self.subprocess:
            pool = Pool(branches)
            result = pool.map(check_for_semantic, data)
            pool.close()
            pool.terminate()
            return result
        else:
            return map(check_for_semantic, data)

    def get_linksets(self, branches=5):
        temp_links = self.get_outgoing_links()
        empty = False
        out_datasets = []
        outgoing_links = []
        val = URLValidator(verify_exists=False)
        for obj in temp_links:
            try:
                val(str(obj[0].encode('utf-8')))
                outgoing_links.append(str(obj[0].encode('utf-8')))
            except:
                pass
        while not empty:
            out_pattern = self.get_pattern(outgoing_links)
            outgoing_links = [e for e in outgoing_links if (e.find(out_pattern[1]) != 0) and ((e + '/').find(out_pattern[1]) != 0)]
            out_datasets.append(out_pattern[1])
            if len(outgoing_links) == 0:
                empty = True
        if len(out_datasets) < branches:
            branches = len(out_datasets)
        #print len(self.graph)
        #print self.graph

        result = self.map_subprocess(zip(out_datasets, repeat(self.uri_pattern), repeat(self.identifier), repeat(self.configstring)))

        #print result
        linksets = {}
        for item in result:
            temp_dict = eval(str(item))
            for key in temp_dict.keys():
                linksets[key] = temp_dict[key]
        return linksets
