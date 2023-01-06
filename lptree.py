import math
import copy
import random

class LPTree:

    def __init__(self, graph, variables):
        self.root = graph
        self.vars = variables

    def get_model_MDL(self):
        return self.root.get_MDL()

    def get_data_MDL(self, dataset):
        sum_ranks = 0
        for instance in dataset.dataset:
            sum_ranks += math.log(self.get_rank(instance))
        return sum_ranks

    def get_MDL(self, dataset):
        return self.get_model_MDL() + self.get_data_MDL(dataset)

    def update_cpt(self, dataset):
        self._update_cpt(dataset, self.root)

    def _update_cpt(self, dataset, node, instance={}):
        node.cpt = dataset.get_pref_order(instance, node.variables)
        count = dataset.get_count(instance,node.variables)
        for k,v in node.children.items():
            if k is not None:
                new_inst = instance.copy()
                dataset.instantiate(new_inst, node.variables, k)
                del count[k]
            else:
                if len(node.children)==1:
                    new_inst = instance
                else:
                    top = list(sorted(count.items(), key=lambda item: -item[1]))
                    new_inst = instance.copy() # all counts are 0: no conditioning
                    if len(top) > 0:
                        dataset.instantiate(new_inst, node.variables, top[0][0])
            self._update_cpt(dataset, v, new_inst)

    # modify the model
    def get_neighbors(self, dataset):
        return self.remove_random_leaf() + self.merge_least_preferred_branches() + self.add_new_leaf()

    def merge_two_nodes(self):
        # TODO
        # merge a node with its child if the parent’s children all have the same variable
        pass

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

    def compare(self, o1, o2):
        return False
