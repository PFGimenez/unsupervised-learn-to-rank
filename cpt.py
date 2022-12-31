import csv
import itertools

class Dataset:

    def __init__(self, file):
        d = []
        self.memoize = {}
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

    def get_domain_size(self, variables):
        out = 1
        for v in variables:
            out *= len(self.domains[v])
        return out

    def get_domain(self, variables):
        domains = [self.domains[v] for v in variables]
        return list(itertools.product(*domains))

    def get_compatible(self, instance):
        out = []
        for h in self.dataset:
            if instance.items() <= h.items():
                out.append(h)
        return out

    def instantiate(self, instance, variables, value):
        for i in range(len(variables)):
            instance[variables[i]] = value[i]

    def get_count(self, instance, variables):
        out = self.memoize.get((tuple(sorted(instance.items())), tuple(variables)))
        if out is not None:
            return out
        l = self.get_compatible(instance)
        order = {}
        for v in variables:
            assert(instance.get(v) is None)
        for i in l:
            val = tuple([i[v] for v in variables])
            order[val] = order.get(val, 0) + 1
        self.memoize[(tuple(sorted(instance.items())),tuple(variables))] = order
        return order

    def get_pref_order(self, instance, variables):
        order = self.get_count(instance, variables) # get counts
        order = list(sorted(order.items(), key=lambda item: -item[1])) # sort counts
        l = [u for (u,v) in order] # keep only labels
        for d in self.get_domain(variables): # add labels absent from counts
            if d not in l:
                l.append(d)
        return l

        return list(set(self.get_count(instance, variables).keys()).union(set(self.get_domain(variables))))

class ConditionalPreferenceTable:

    def __init__(self, orders):
        self.orders = orders
