import math

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
        return get_model_MDL() + self.get_data_MDL()

    def get_neighbors(self):
        return []

    def get_mean_rank(self, dataset):
        sum_ranks = 0
        for instance in dataset.dataset:
            sum_ranks += self.get_rank(instance)
        return sum_ranks / len(dataset.dataset)

    def get_rank(self, o):
        r = 1 + self.tree.get_lp_rank(o, 0)
        return r

    def compare(self, o1, o2):
        return False
