import json


class FactorGraph:
    def __init__(self):
        self.vars = {}
        self.funcs = {}
        self.func_calc = None
        self.graph = None

    def load(self, graph, function_calculator):
        self.func_calc = function_calculator
        self.graph = graph

        fg = json.loads(open(self.graph, 'r').read())

        self.vars = fg['variables']
        self.funcs = fg['functions']

        for v in self.vars:
            self.vars[v]['value'] = 0
            self.vars[v]['size'] = len(self.vars[v]['domain'])

    def get_value(self, name):
        if name in self.vars:
            value = self.vars[name]['domain'][self.vars[name]['value']]
        elif name in self.funcs:
            value = getattr(self.func_calc, name)()
        else:
            raise Exception('Invalid function of variable.')

        return value

    def get_neighbour_variables(self, var):
        nvars = set()
        for f in self.vars[var]['functions']:
            for v in self.funcs[f]['variables']:
                if v != var:
                    nvars.add(v)
        return list(nvars)
