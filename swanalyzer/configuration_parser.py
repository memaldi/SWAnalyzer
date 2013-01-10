class ConfigurationParser(object):
    def __init__(self, f):
            self._filename = f
            self._global_variables = {}
            self.reload()

    def reload(self):
            self._global_variables.clear()
            execfile(self._filename, self._global_variables, self._global_variables)

    def __getattribute__(self, name):
        if name in ('reload','get') or name.startswith('_'):
            return object.__getattribute__(self, name)
        else:
            try:
                return self._global_variables[name]
            except KeyError:
                raise AttributeError('Missing field: %s' % name)

    def __getitem__(self, name):
        return self._global_variables[name]

    def get(self, name, default = None):
        return getattr(self, name, default)
