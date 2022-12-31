class LPTree:

    def __init__(self, graph, variables):
        self.tree = graph
        self.vars = variables

    def get_MDL_length(self):
        return self.tree.get_MDL_length()

    def get_MDL_encoding(self, o):
        return 0

    def get_neighbors(self):
        return []

    def get_mean_rank(self, dataset):
        sum_ranks = 0
        for instance in dataset.dataset:
            sum_ranks += self.get_rank(instance)
        return sum_ranks / len(dataset.dataset)

    def get_rank(self, o):
        r = 1+self.tree.get_lp_rank(o, 0)
        return r

    def compare(self, o1, o2):
        return False
