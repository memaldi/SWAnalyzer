from sw_analyzer import SWAnalyzer

class DumpAnalyzer(SWAnalyzer):

    def __init__(self, path, identifier, configstring, proxy=None):
        SWAnalyzer.__init__(self, identifier, configstring, proxy=proxy)
        self.path = path

    def open(self):
        SWAnalyzer.open(self)

    def load_graph(self):
        self.graph.parse(self.path)
        self.graph.commit()
        SWAnalyzer.load_graph(self)
