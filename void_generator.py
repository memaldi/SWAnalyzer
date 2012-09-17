class VoidGenerator:

    def __init__(self, void, prefixes=None):
        self.void = void
        self.prefixes = prefixes
        pass


class Void:

    def __init__(self, void_uri, page_links=None, dc_metadata=None, contact_info=None, license=None, subjects=None, technical_features=None, sparql_endpoint=None, rdf_datadump=None, root_resources=None, lookup_endpoint=None, example_resources=None, uri_space=None, uri_regex=None, vocabularies=None, subset=None, class_partitions=None, property_partitions=None, statistics=None):
        self.void_uri = void_uri
        self.page_links = page_links
        self.dc_metadata = dc_metadata
        self.contact_info = contact_info
        self.license = license
        self.subjects = subjects
        self.technical_features = technical_features
        self.sparql_endpoint = sparql_endpoint
        self.rdf_datadump = rdf_datadump
        self.root_resources = root_resources
        self.lookup_endpoint = lookup_endpoint
        self.example_resources = example_resources
        self.uri_space = uri_space
        self.uri_regex = uri_regex
        self.vocabularies = vocabularies
        self.subset = subset
        self.class_partitions = class_partitions
        self.property_partitions = property_partitions
        self.statistics = statistics

class ClassPartition:

    def __init__(self, class_name, entities):
       self.class_name = class_name
       self.entities = entities

class PropertyPartition:

    def __init(self, property_name, triples):
        self.property_name = property_name
        self.triples = triples

class Linkset:

    def __init__(self, subjects_target, objects_target, subset=None, triples=None, link_predicate=None):
        self.subjects_target = subjects_target
        self.objects_target = objects_target
        self.subset = subset
        self.triples = triples
        self.link_predicate = link_predicate
