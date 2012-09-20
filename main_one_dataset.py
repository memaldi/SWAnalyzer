from sparql_analyzer import SPARQLAnalyzer
from time import strftime, localtime

print '[%s] Starting analysis...' % (strftime("%a, %d %b %Y %H:%M:%S", localtime()))
#sparql_analyzer = SPARQLAnalyzer('http://www.morelab.deusto.es/joseki/articles', 'morelab')
sparql_analyzer = SPARQLAnalyzer('http://lod.b3kat.de/sparql', 'b3kat')
sparql_analyzer.open()
sparql_analyzer.load_graph()

print '[%s] URI pattern: %s' % (strftime("%a, %d %b %Y %H:%M:%S", localtime()), sparql_analyzer.uri_pattern)
print '[%s] Number of triples: %s' % (strftime("%a, %d %b %Y %H:%M:%S", localtime()), len(sparql_analyzer.graph))
num_classes = sparql_analyzer.get_classes()
print '[%s] Number of classes: %s' % (strftime("%a, %d %b %Y %H:%M:%S", localtime()), len(num_classes))
num_properties = sparql_analyzer.get_properties()
print '[%s] Number of properties: %s' % (strftime("%a, %d %b %Y %H:%M:%S", localtime()), len(num_properties))
num_subjects = sparql_analyzer.get_subjects()
print '[%s] Number of subjects: %s' % (strftime("%a, %d %b %Y %H:%M:%S", localtime()), len(num_subjects))
num_objects = sparql_analyzer.get_objects()
print '[%s] Number of objects: %s' % (strftime("%a, %d %b %Y %H:%M:%S", localtime()), len(num_objects))
num_entities = sparql_analyzer.get_entities()
print '[%s] Number of entities: %s' % (strftime("%a, %d %b %Y %H:%M:%S", localtime()), len(num_entities))
num_linksets = sparql_analyzer.get_linksets()
print '[%s] Linksets: ' % (strftime("%a, %d %b %Y %H:%M:%S", localtime()))
for key in num_linksets.keys():
    print '|%s' % (key)
    d = num_linksets[key]
    for key in d.keys():
        print '|--------%s: %s' % (key, d[key])
print '[%s] Finished!'% (strftime("%a, %d %b %Y %H:%M:%S", localtime()))


sparql_analyzer.close()
