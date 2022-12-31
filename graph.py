import math

class Graph:

    def __init__(self, nodes):
        self.nodes = nodes

    def add_node(self, n):
        append(self.nodes, n)

    def del_node(self, n):
        self.nodes.remove(n)

class Node:

    def __init__(self, variables, domain_size, cpt, all_vars):
        self.domain_size = domain_size
        self.variables = variables
        self.all_vars = all_vars
        self.cpt = cpt # list of labels
        self.children = {} # Key: label. Value: child node

    def add_child(self, c, label=None):
        self.children[label] = c

    def export(self, filename):
        with open(filename, "w") as f:
            f.write("digraph G { \n");
            f.write("ordering=out;\n");
            self._export(f)
            f.write("}\n");

    def _export(self, f):
        f.write(str(id(self))+" [label=\""+str(self.variables)+"\nCPT:"+str(self.cpt)+"\"];\n");
        for k in self.cpt:
            self._export_one_child(f, k) # if labeled edges
        self._export_one_child(f, None) # if unlabeled edge

    def _export_one_child(self, f, k):
        v = self.children.get(k)
        if v is not None:
            v._export(f)
            if k is None:
                k=""
            f.write(str(id(self))+" -> "+str(id(v))+" [label=\""+str(k)+"\"];\n");

    def get_MDL(self):
        l = math.log(len(self.all_vars))*(len(self.variables)+1)+len(self.cpt)*(math.log(len(self.cpt))-1) # Stirling’s approximation
        for k in self.cpt:
            c = self.children.get(k)
            if c is not None:
                l += c.get_MDL()
        c = self.children.get(None)
        if c is not None:
            l += c.get_MDL()
        return l

    def get_lp_rank(self, o, curr):
        nb = 0
        for k in self.cpt:
            if k is None or k==(o[self.variables[0]],): # TODO plusieurs variables
                c = self.children.get(k)
                if c is None: # maybe no label
                    c = self.children.get(None)
                # print("Var",self.variables[0],"rank",nb)
                curr = curr*self.domain_size+nb
                if c is None:
                    return curr
                else:
                    return c.get_lp_rank(o, curr)
            nb += 1
        assert False


class Edge:

    def __init__(self, label=None):
        self.label = label
