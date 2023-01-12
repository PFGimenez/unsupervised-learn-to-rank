import math
import copy
import random
import outcome

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
            # assert len(self.cpt) == len(self.children)
            self.children[None] = self.children[self.cpt[-2]]
            del self.children[self.cpt[-2]]
            del self.children[self.cpt[-1]]
        else:
            for v in reversed(self.cpt):
                if self.children.get(v) is not None:
                    self.children[None] = self.children[v]
                    del self.children[v]
                    break

    def get_leaves(self): # return the list of couples (node, value) such as the child of node with the label "value" is a leaf
        l = []
        for k,v in self.children.items():
            # only remove leaf if it’s the only child of its parent
            if len(v.children) == 0 and len(self.children)==1: # it’s a leaf
                l.append((self,k))
            else:
                l += v.get_leaves()
        return l

    def get_uncompleted_branches(self, variables):
        l = []
        variables += self.variables
        if len(self.children) == 0: # it’s a leaf
            if len(variables) == len(self.all_vars): # not possible to add a new node
                return []
            else: # possible to add a new node
                return [(self, variables)]
        if len(self.children.items()) == 1: # one child only: no need to copy variables
            l += self.children.get(None).get_uncompleted_branches(variables)
        else:
            for k,v in self.children.items():
                l += v.get_uncompleted_branches(variables.copy())
        return l

    def get_MDL(self):
        l = math.log(len(self.all_vars))*(len(self.variables)+1)+(len(self.cpt)-1)*(math.log(len(self.cpt)))
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
        value = tuple([o[k] for k in self.variables])
        for k in self.cpt:
            if k is None or k == value:
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

    def get_preferred_extension(self, instance):
        for o in self.cpt:
            instance2 = {}
            outcome.instantiate(instance2, self.variables, o)
            if outcome.is_compatible(instance2, instance):
                outcome.instantiate(instance, self.variables, o)
                if self.children.get(o) is not None: # take the labelled edge
                    self.children.get(o).get_preferred_extension(instance)
                elif self.children.get(None) is not None: # if not, take the unlabelled edge
                    self.children.get(None).get_preferred_extension(instance)
                # is not, it’s a leaf
                return
        assert False

    def get_data_MDL(self, instance):
        for i in range(len(self.cpt)):
            o = self.cpt[i]
            instance2 = {}
            outcome.instantiate(instance2, self.variables, o)
            if outcome.is_compatible(instance2, instance):
                outcome.instantiate(instance, self.variables, o)
                out = 0
                # print(self.variables,o,i)
                if self.children.get(o) is not None: # take the labelled edge
                    out = self.children.get(o).get_data_MDL(instance)
                elif self.children.get(None) is not None: # if not, take the unlabelled edge
                    out = self.children.get(None).get_data_MDL(instance)
                # is not, it’s a leaf
                return i + out
        assert False


class LPTree:

    def __init__(self, graph, variables):
        self.root = graph
        self.vars = variables
        self.defaults = {}

    def get_model_MDL(self):
        return self.root.get_MDL()

    # def get_data_MDL(self, dataset):
    #     sum_ranks = 0
    #     for instance in dataset.uniques:
    #         sum_ranks += dataset.counts[repr(instance)] * math.log(self.get_rank(instance))
    #     return sum_ranks

    # def get_MDL(self, dataset):
    #     return self.get_model_MDL() + self.get_data_MDL(dataset)

    def update_cpt(self, dataset):
        for v in dataset.vars:
            self.defaults[v] = dataset.get_pref_order({}, [v])[0][0]
        self._update_cpt(dataset, self.root)

    def get_preferred_extension(self, instance):
        new_inst = instance.copy()
        self.root.get_preferred_extension(new_inst)
        for v in self.vars: # branches may be incomplete
            if new_inst.get(v) is None:
                new_inst[v] = self.defaults[v]
        return new_inst

    def get_data_MDL(self, instance):
        new_inst = instance.copy()
        score = self.root.get_data_MDL(new_inst)
        # print("Score:",score,"for",instance)
        for v in self.vars: # branches may be incomplete
            if new_inst.get(v) is None:
                if new_inst[v] != self.defaults[v]:
                    score += math.log(len(instance))
        return score


    def _update_cpt(self, dataset, node, instance={}):
        node.cpt = dataset.get_pref_order(instance, node.variables)
        count = dataset.get_count(instance,node.variables).copy()
        for k,v in node.children.items():
            if k is not None:
                new_inst = instance.copy()
                outcome.instantiate(new_inst, node.variables, k)
                if count.get(k) is not None:
                    del count[k]
            else:
                if len(node.children)==1:
                    new_inst = instance
                else:
                    top = list(sorted(count.items(), key=lambda item: -item[1]))
                    new_inst = instance.copy() # all counts are 0: no conditioning
                    if len(top) > 0:
                        outcome.instantiate(new_inst, node.variables, top[0][0])
            self._update_cpt(dataset, v, new_inst)

    # modify the model
    def get_neighbors(self, dataset):
        lptrees = self.remove_random_leaf() + self.merge_least_preferred_branches() #+ self.add_new_leaf()
        for lptree in lptrees:
            lptree.update_cpt(dataset)
        return lptrees

    # def merge_two_nodes(self):
        # TODO
        # merge a node with its child if the parent’s children all have the same variable
        # pass

    def remove_random_leaf(self):
        out = []
        nb_leaves = len(self.root.get_leaves())
        # print("Leaves:",nb_leaves)
        for i in range(nb_leaves):
            # print("Removing leaf",i)
            new_tree = copy.deepcopy(self)
            l = new_tree.root.get_leaves()
            n,v = l[i]
            del n.children[v]
            out.append(new_tree)
        return out

    def merge_least_preferred_branches(self):
        out = []
        nb_branches = len(self.root.get_branching_nodes())
        # print("Branching nodes:",nb_branches)
        for i in range(nb_branches):
            # print("Merging branches",i)
            new_tree = copy.deepcopy(self)
            n = new_tree.root.get_branching_nodes()[i]
            n.merge_branches()
            out.append(new_tree)
        return out

    def add_new_leaf(self):
        # TODO
        out = []
        print("Call 1")
        nb_leaves = len(self.root.get_uncompleted_branches([]))
        # print("Leaves:",nb_leaves)
        for i in range(nb_leaves):
            # print("Adding leaf",i)
            print("Call 2")
            l = self.root.get_uncompleted_branches([])
            print(l)
            # for _,v in l:
            #     new_tree = copy.deepcopy(self)
            #     l = new_tree.root.get_uncompleted_branches()
            #     n,v = l[i]
            #     del n.children[v]
            #     out.append(new_tree)
        return out

    def get_mean_rank(self, dataset):
        sum_ranks = 0
        for instance in dataset.dataset:
            sum_ranks += self.get_rank(instance)
        return sum_ranks / len(dataset.dataset)

    def get_rank(self, o):
        r = 1 + self.root.get_lp_rank(o)
        return r

    def export(self, filename):
        with open(filename, "w") as f:
            f.write("digraph G { \n");
            f.write("ordering=out;\n");
            self.root._export(f)
            f.write("}\n");

