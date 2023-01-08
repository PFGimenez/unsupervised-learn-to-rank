import math
import outcome

class CPNet:

    def __init__(self, all_vars):
        # non-cylic CP-net only
        self.all_vars = all_vars
        self.nodes = []
        for v in all_vars:
            self.nodes.append(Node([v]))
        self.topo_order = list(self.nodes)

    def get_roots(self):
        roots = []
        for n in self.nodes:
            if len(n.parents) == 0:
                roots.append(n)
        return roots

    def merge_nodes(self, n1, n2): # merge n2 into n1
        assert n1 != n2
        if self.topo_order.index(n1) > self.topo_order.index(n2):
            # n1 is lower than n2 in the DAG: n1 gets n2’s parents (to keep a DAG)
            n1.parents = list(set(n1.parents + n2.parents))
        else:
            # n1 is higher than n2 in the DAG: n1 gets n2’s children (to keep a DAG)
            n1.children = list(set(n1.children + n2.children))
        n1.variables += n2.variables
        self.nodes.remove(n2)
        for n in self.nodes:
            if n2 in n.children:
                n.children.remove(n2)
            if n2 in n.parents:
                n.parents.remove(n2)
        self.update_topo_order()

    def split_node(self, n1, var): # create a new node with variables "var" from n1
        n2 = Node(var)
        self.nodes.append(n2)
        for v in var:
            n1.variables.remove(v)
        for n in n1.parents:
            n2.parents.append(n)
        for n in n1.children:
            n2.children.append(n)
        self.update_topo_order()

    def add_child(self, p, c):
        if c not in p.children:
            p.children.append(c)
            c.parents.append(p)
            new_order = self.update_topo_order()
            if new_order is False: # not a DAG anymore, go back to previous status
                p.children.remove(c)
                c.parents.remove(p)

    def update_cpt(self, dataset):
        for v in self.nodes:
            v.cpt = {}
            par = []
            for p in v.parents:
                par += p.variables
            dom = dataset.get_domain(par)
            for val in dom:
                instance = {}
                outcome.instantiate(instance, par, val)
                v.cpt[val] = dataset.get_pref_order(instance, v.variables)

    def export(self, filename):
        with open(filename, "w") as f:
            f.write("digraph G { \n");
            f.write("ordering=out;\n");
            for v in self.topo_order:
                f.write(str(id(v))+" [label=\""+str(v.variables)+"\nCPT:"+str(v.cpt)+"\"];\n");
                for c in v.children:
                    f.write(str(id(v))+" -> "+str(id(c))+";\n");
            f.write("}\n");

    def update_topo_order(self):
        # Kahn’s algorithm
        topo_order = []
        roots = self.get_roots()
        while len(roots) > 0:
            n = roots.pop()
            topo_order.append(n)
            for c in n.children:
                has_parent = False
                for p in c.parents:
                    if p not in topo_order:
                        has_parent = True
                        break
                if not has_parent:
                    roots.append(c)
        if len(topo_order) < len(self.nodes):
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
