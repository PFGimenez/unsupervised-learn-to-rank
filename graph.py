class Node:

    def __init__(self, var, parent, children):
        self.var = var
        self.parents = parents
        self.children = children

    def add_parent(self, p):
        append(self.parents, p)
        p._add_child(self)

    def _add_parent(self, p):
        append(self.parents, p)

    def add_child(self, c)
        append(self.children, c)
        c._add_parent(self)

    def _add_child(self, c)
        append(self.children, c)

class Edge:

    def __init__(self, label=None):
        self.label = label
