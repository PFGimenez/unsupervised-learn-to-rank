import csv

class Dataset:

    def __init__(self, file):
        d = []
        self.vars = None
        with open(file, mode='r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                d.append(row)
                if self.vars is None:
                    self.vars = list(row.keys())
        self.dataset = d
        self.domains = {}
        for v in self.vars:
            self.domains[v] = set([])
            for i in self.dataset:
                self.domains[v].add(i[v])
            self.domains[v] = list(self.domains[v])
        print("Variables:",self.vars)
        print("Domains:", self.domains)

    def get_compatible(self, instance):
        out = []
        for h in self.dataset:
            if instance.items() <= h.items():
                out.append(h)
        return out

    def get_count(self, instance, var):
        l = self.get_compatible(instance)
        order = {}
        assert(instance.get(var) is None)
        for i in l:
            val = i[var]
            order[val] = order.get(val, 0) + 1
        order = dict(sorted(order.items(), key=lambda item: -item[1]))
        return order

    def get_pref_order(self, instance, var):
        return self.get_count(instance, var).keys()

class ConditionalPreferenceTable:

    def __init__(self, orders):
        self.orders = orders
