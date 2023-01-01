import math
import copy
import random

class LPTree:

    def __init__(self, graph, variables):
        self.tree = graph
        self.vars = variables

    def get_model_MDL(self):
        return self.tree.get_MDL()

    def get_data_MDL(self, dataset):
        sum_ranks = 0
        for instance in dataset.dataset:
            sum_ranks += math.log(self.get_rank(instance))
        return sum_ranks

    def get_MDL(self, dataset):
        return self.get_model_MDL() + self.get_data_MDL(dataset)

    # modify the model
    def get_neighbors(self):
        # return self.merge_least_preferred_branches()
        return self.remove_random_leaf() + self.merge_least_preferred_branches()

    def remove_random_leaf(self):
        out = []
        nb_leaves = len(self.tree.get_leaves())
        # print("Leaves:",nb_leaves)
        for i in range(nb_leaves):
            # print("Removing leaf",i)
            new_tree = copy.deepcopy(self)
            l = new_tree.tree.get_leaves()
            n,v = l[i]
            del n.children[v]
            out.append(new_tree)
        return out

    def merge_least_preferred_branches(self):
        out = []
        nb_branches = len(self.tree.get_branching_nodes())
        # print("Branching nodes:",nb_branches)
        for i in range(nb_branches):
            # print("Merging branches",i)
            new_tree = copy.deepcopy(self)
            n = new_tree.tree.get_branching_nodes()[i]
            n.merge_branches()
            out.append(new_tree)
        return out

    def add_new_leaf(self):
        out = []
        nb_leaves = len(self.tree.get_leaves())
        # print("Leaves:",nb_leaves)
        for i in range(nb_leaves):
            # print("Removing leaf",i)
            new_tree = copy.deepcopy(self)
            l = new_tree.tree.get_leaves()
            n,v = l[i]
            del n.children[v]
            out.append(new_tree)
        return out


    def get_mean_rank(self, dataset):
        sum_ranks = 0
        for instance in dataset.dataset:
            sum_ranks += self.get_rank(instance)
        return sum_ranks / len(dataset.dataset)

    def get_rank(self, o):
        r = 1 + self.tree.get_lp_rank(o)
        return r

    def compare(self, o1, o2):
        return False
