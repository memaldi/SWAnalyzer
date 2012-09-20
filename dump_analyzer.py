from sw_analyzer import SWAnalyzer

class DumpAnalyzer(SWAnalyzer):

    def __init__(self, path, identifier):
        SWAnalyzer.__init__(self, identifier)
        self.path = path

    def open(self):
        SWAnalyzer.open(self)

    def load_graph(self):
        self.graph.parse(self.path)
        SWAnalyzer.load_graph(self)
