import math

class Graph:

    def __init__(self, nodes):
        self.nodes = nodes

    def add_node(self, n):
        append(self.nodes, n)

    def del_node(self, n):
        self.nodes.remove(n)

class Node:

    def __init__(self, variables, domain_size, cpt, all_vars, space_size):
        self.domain_size = domain_size
        self.variables = variables
        self.all_vars = all_vars
        self.space_size = space_size
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

    def get_branching_nodes(self): # return the list of nodes that have a least two outgoing branches
        l = []
        if len(self.children) >= 2: # it’s a branching node
            l.append(self)
        for v in self.children.values():
            l += v.get_branching_nodes()
        return l

    def merge_branches(self):
        if self.children.get(None) is None:
            self.children[None] = self.children[self.cpt[-2]]
            del self.children[-2]
            del self.children[-1]
        else:
            for v in reversed(self.cpt):
                if self.children.get(v) is not None:
                    self.children[None] = self.children[v]
                    del self.children[v]
                    break

    def get_leaves(self): # return the list of couples (node, value) such as the child of node with the label "value" is a leaf
        l = []
        for k,v in self.children.items():
            if len(v.children) == 0: # it’s a leaf
                l.append((self,k))
            else:
                l += v.get_leaves()
        return l

    def get_uncompleted_branches(self, variables=[]):
        l = []
        variables += self.variables
        if len(self.children) == 0: # it’s a leaf
            if len(variables) == len(all_vars): # not possible to add a new node
                return []
            else: # possible to add a new node
                return [(self, variables)]
        for k,v in self.children.items():
            l += v.get_uncompleted_branches(variables.copy())
        return l

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

    def get_lp_rank(self, o):
        return self._get_lp_rank(o, 0, self.space_size)

    def _get_lp_rank(self, o, curr, rest):
        nb = 0
        rest = rest/self.domain_size
        for k in self.cpt:
            if k is None or k==(o[self.variables[0]],): # TODO plusieurs variables
                c = self.children.get(k)
                if c is None: # maybe no label
                    c = self.children.get(None)
                # print("Var",self.variables[0],"rank",nb)
                curr = curr*self.domain_size+nb
                if c is None: # it’s a leaf
                    return curr*rest+(rest-1)/2
                else:
                    return c._get_lp_rank(o, curr, rest)
            nb += 1
        assert False


class Edge:

    def __init__(self, label=None):
        self.label = label
