class Graph:

    def __init__(self, nodes):
        self.nodes = nodes

    def add_node(self, n):
        append(self.nodes, n)

    def del_node(self, n):
        self.nodes.remove(n)

class NodeBak:

    def __init__(self, var, cpt, parent=None, children=None):
        self.var = var
        self.cpt = cpt
        self.parents = parents
        self.children = children

    def add_parent(self, p):
        append(self.parents, p)
        p._add_child(self)

    def _add_parent(self, p):
        append(self.parents, p)

    def add_child(self, c):
        append(self.children, c)
        c._add_parent(self)

    def _add_child(self, c):
        append(self.children, c)

class Node:

    def __init__(self, var, cpt, children={}):
        self.var = var
        self.cpt = cpt
        self.children = children

    def add_child(self, c, label: None):
        self.children[label] = c

    def export(self, filename):
        pass

class Edge:

    def __init__(self, label=None):
        self.label = label
