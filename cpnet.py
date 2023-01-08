import math
import outcome

class CPNet:

    def __init__(self, all_vars):
        # non-cylic CP-net only
        self.roots = all_vars.copy()
        self.topo_order = all_vars.copy()
        self.all_vars = all_vars
        self.nodes = {}
        for v in all_vars:
            self.nodes[v] = Node([v])

    def add_child(self, p, c):
        if c not in self.nodes[p].children:
            self.nodes[p].children.append(c)
            self.nodes[c].parents.append(p)
            if c in self.roots:
                self.roots.remove(c)
            new_order = self.update_topo_order()
            if new_order is False: # not a DAG anymore
                self.nodes[p].children.remove(c)
                self.nodes[c].parents.remove(p)

    def update_cpt(self, dataset):
        for v in self.all_vars:
            self.nodes[v].cpt = {}
            parents = self.nodes[v].parents
            dom = dataset.get_domain(parents)
            for val in dom:
                instance = {}
                outcome.instantiate(instance, parents, val)
                self.nodes[v].cpt[val] = dataset.get_pref_order(instance, [v])

    def export(self, filename):
        with open(filename, "w") as f:
            f.write("digraph G { \n");
            f.write("ordering=out;\n");
            for v in self.topo_order:
                f.write(v+" [label=\""+str(v)+"\nCPT:"+str(self.nodes[v].cpt)+"\"];\n");
                for c in self.nodes[v].children:
                    f.write(v+" -> "+c+";\n");
            f.write("}\n");

    def update_topo_order(self):
        # TODO: order of node, not variables
        # Kahn’s algorithm
        topo_order = []
        roots = self.roots.copy()
        while len(roots) > 0:
            # print("Iter",roots)
            n = roots.pop()
            topo_order.append(n)
            for c in self.nodes[n].children:
                has_parent = False
                for p in self.nodes[c].parents:
                    if p not in topo_order:
                        has_parent = True
                        break
                if not has_parent:
                    roots.append(c)
        if len(topo_order) < len(self.all_vars):
            # there is a cycle
            return False
        else:
            # update the topological order
            self.topo_order = topo_order
            return True

    def get_model_MDL(self):
        l = 0
        for v in self.all_vars:
            node = self.nodes[v]
            l += len(node.parents) * math.log(len(self.all_vars)) # parents encoding
            any_cpt = list(node.cpt.values())[0]
            l += len(node.cpt) * (len(any_cpt) - 1) * (math.log(len(any_cpt))) # cpt
        return l

    def get_data_MDL(self, dataset):
        sum_score = 0
        for instance in dataset.dataset:
            print("MDL of",instance)
            sum_score += self.get_path_length(instance)
            return sum_score # FIXME

    def get_path_length(self, instance):
        print("Instance",instance)
        for v in reversed(self.topo_order):
            n = self.nodes[v]
            value_parents = tuple([instance[k] for k in n.parents])
            l = n.cpt[value_parents]
            value_node = tuple([instance[k] for k in n.variables])
            print("Node var:",n.variables)
            print("Par:",value_parents,"node:",value_node)
            print(l)
            index = l.index(value_node)
            if index == 0:
                print("Preferred")
            else:
                outcome.instantiate(instance, value_node, n.variables)
                return index
                # return index + self.get_path_length(instance)
        return 0

    def get_MDL(self, dataset):
        return self.get_model_MDL() + self.get_data_MDL(dataset)

class Node:

    def __init__(self, variables):
        self.variables = variables
        self.cpt = {} # dict. Key: parent value. Value: list of values
        self.children = []
        self.parents = []
