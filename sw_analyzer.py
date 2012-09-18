#encoding: utf-8

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
from tempfile import mkdtemp
from django.core.validators import URLValidator
from urlparse import urlparse
from multiprocessing import Pool

def get_obj_from_prefix(prefix, graph, uri_pattern):
        query = 'SELECT DISTINCT ?o WHERE {?s ?p ?o . FILTER (regex(str(?o), "^' + prefix + '", "i") && !regex(str(?o), "' + uri_pattern + '", "i"))}'
        qres = graph.query(query)
        return qres.result

def check_for_semantic(args):
    out_datasets = args[0]
    graph = args[1]
    print 'GRAPHHHH!!: ' + str(len(graph))
    uri_pattern = args[2]
    print args
    for item in out_datasets:
        #print item
        objs = get_obj_from_prefix(item, graph, uri_pattern='')
        for obj in objs:
            #print str(obj[0])
            url = urlparse(str(obj[0]))
            conn = httplib.HTTPConnection(url.netloc)
            conn.request("GET", url.path, "", headers)
            response = conn.getresponse()
            #print response.status
            if response.status in [202, 303]:
                query = 'SELECT ?p WHERE {?s ?p <' + str(obj[0]) + '>}'
                qres = graph.query(query)
                result = qres.result
                for p in result:
                    if item in linksets:
                        if str(p[0]) in linksets[item]:
                            linksets[item][str(p[0])] = linksets[item][str(p[0])] + 1
                        else:
                            linksets[item][str(p[0])] = 1
                    else:
                        linksets[item] = {str(p[0]): 1}

class SWAnalyzer:
    def __init__(self):
        #store = plugin.get('PostgreSQL', Store)('rdfstore')
        self.configString="user=postgres,password=p0stgr3s,host=localhost,db=rdfstore"
        plugin.register('PostgreSQL', store.Store,'rdflib_postgresql.PostgreSQL', 'PostgreSQL')
        self.graph = Graph(store='PostgreSQL')
        #self.graph.destroy(None)

    #@abc.abstractmethod
    def open(self):
       self.graph.open(self.configString, create=True)
       return

    def close(self):
        self.graph.destroy(self.configString)
        self.graph.close()
        '''for f in os.listdir(self.path):
            os.unlink(self.path + '/' + f)
            os.rmdir(self.path)'''

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
        qres = self.graph.query(query, processor='sparql')
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

    def get_linksets(self):
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
            out_pattern = self.get_patterns(outgoing_links)
            outgoing_links = [e for e in outgoing_links if (e.find(out_pattern[1]) != 0) and ((e + '/').find(out_pattern[1]) != 0)]
            #print outgoing_links
            #print out_pattern
            #print len(outgoing_links)
            out_datasets.append(out_pattern[1])
            if len(outgoing_links) == 0:
                empty = True
        headers = {"Accept": "application/rdf+xml"}
        linksets = {}
        pool = Pool(5)
        print pool.map(check_for_semantic, (out_datasets, self.graph, self.uri_pattern))
        #print linksets
        return linksets

    
