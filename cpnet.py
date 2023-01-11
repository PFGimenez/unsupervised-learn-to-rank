import math
import outcome
import copy

class CPNet:

    def __init__(self, all_vars, dataset=None):
        # non-cylic CP-net only
        self.nodes = []
        for v in all_vars:
            self.nodes.append(Node([v]))
        self.topo_order = list(self.nodes)
        if dataset is not None:
            self.update_cpt(dataset)

    def get_neighbors(self, dataset):
        cpnets = self.update_edges_neighbors() #+ self.merge_nodes_neighbors()# + self.split_nodes_neighbors()
        for net in cpnets:
            net.update_cpt(dataset)
        # print("Nb neighbors:",len(cpnets))
        return cpnets


    def update_edges_neighbors(self):
        out = []
        for i in range(len(self.nodes)):
            for j in range(len(self.nodes)):
                if i != j:
                    # already an edge
                    if self.nodes[i] in self.nodes[j].children or self.nodes[j] in self.nodes[i].children:
                        new_cpnet = copy.deepcopy(self) # reverse
                        n1 = new_cpnet.nodes[i]
                        n2 = new_cpnet.nodes[j]
                        done = new_cpnet.reverse_edge(n1, n2)
                        if done:
                            out.append(new_cpnet)
                        else:
                            del new_cpnet
                        new_cpnet2 = copy.deepcopy(self) # reverse
                        n1 = new_cpnet2.nodes[i]
                        n2 = new_cpnet2.nodes[j]
                        if self.nodes[i] in self.nodes[j].children: # remove
                            new_cpnet2.remove_child(n2,n1)
                        else:
                            new_cpnet2.remove_child(n1,n2)
                        out.append(new_cpnet2)
                    else: # add an edge
                        new_cpnet = copy.deepcopy(self) # n1 -> n2
                        n1 = new_cpnet.nodes[i]
                        n2 = new_cpnet.nodes[j]
                        done = new_cpnet.add_child(n1,n2)
                        if done:
                            out.append(new_cpnet)
                        else:
                            del new_cpnet
                        new_cpnet2 = copy.deepcopy(self) # n2 -> n1
                        n1 = new_cpnet2.nodes[i]
                        n2 = new_cpnet2.nodes[j]
                        done = new_cpnet2.add_child(n2,n1)
                        if done:
                            out.append(new_cpnet2)
                        else:
                            del new_cpnet2
        return out

    def merge_nodes_neighbors(self):
        out = []
        for i in range(len(self.nodes)):
            for j in range(len(self.nodes)):
                if i != j:
                    if len(self.nodes[i].variables) + len(self.nodes[j].variables) < 5:
                        # merge into i
                        new_cpnet = copy.deepcopy(self)
                        new_cpnet.merge_nodes(new_cpnet.nodes[i],new_cpnet.nodes[j])
                        out.append(new_cpnet)
                        # merge into j
                        new_cpnet2 = copy.deepcopy(self)
                        new_cpnet2.merge_nodes(new_cpnet2.nodes[j],new_cpnet2.nodes[i])
                        out.append(new_cpnet2)
        return out

    # def split_nodes_neighbors(self):
    #     out = []
    #     for n in self.nodes:
    #         if len(n.variables) > 1:
    #             sets = utils.powerset(set(n.variables))
    #             print(sets)
    #     return out

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

    def reverse_edge(self, n1, n2):
        if n1 in n2.children:
            n1,n2 = n2,n1 # normalize: we want to change n1 -> n2 to n2 -> n1
        n1.children.remove(n2)
        n2.parents.remove(n1)
        n1.parents.append(n2)
        n2.children.append(n1)
        return self.update_topo_order()

    def remove_child(self, p, c):
        p.children.remove(c)
        c.parents.remove(p)
        self.update_topo_order()

    def add_child(self, p, c):
        # if c not in p.children:
            p.children.append(c)
            c.parents.append(p)
            done = self.update_topo_order()
            if not done: # not a DAG anymore, go back to previous status
                p.children.remove(c)
                c.parents.remove(p)
            return done
        # return False # no change

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
                if len(str(v.cpt)) < 100: # short CPT
                    f.write(str(id(v))+" [label=\""+str(v.variables)+"\nCPT:"+str(v.cpt)+"\"];\n");
                else:
                    f.write(str(id(v))+" [label=\""+str(v.variables)+"\"];\n");
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
        for n in self.nodes:
            l += len(n.parents) * math.log(len(self.nodes)) # parents encoding
            any_cpt = list(n.cpt.values())[0]
            l += len(n.cpt) * (len(any_cpt) - 1) * (math.log(len(any_cpt))) # cpt
        # print("model MDL:",l)
        return l

    def get_preferred_extension(self, instance):
        instance = instance.copy()
        for n in self.topo_order:
            var = []
            for p in n.parents:
                var += p.variables
            value_parents = tuple([instance[k] for k in var])
            l = n.cpt[value_parents]
            for o in l:
                instance2 = {}
                outcome.instantiate(instance2, n.variables, o)
                if outcome.is_compatible(instance2, instance):
                    outcome.instantiate(instance, n.variables, o)
        var_order = []
        for n in self.topo_order:
            var_order += n.variables
        return instance, var_order

    def get_data_MDL2(self, dataset):
        sum_score = 0
        for instance in dataset.uniques:
            sum_score += dataset.counts[repr(instance)] * self.get_path_length(instance.copy())*math.log(len(dataset.vars))
        # print("data MDL:",sum_score)
        return sum_score

    def get_path_length(self, instance):
        length = 0
        redo = True
        while redo:
            redo = False
            for n in reversed(self.topo_order):
                var = []
                for p in n.parents:
                    var += p.variables
                value_parents = tuple([instance[k] for k in var])
                l = n.cpt[value_parents]
                value_node = tuple([instance[k] for k in n.variables])
                index = l.index(value_node)
                if index > 0:
                    redo = True
                    length += index
                    outcome.instantiate(instance, n.variables, l[0])
                    break
        return length

    def get_MDL(self, dataset):
        return self.get_model_MDL() + self.get_data_MDL(dataset)

class Node:

    def __init__(self, variables):
        self.variables = variables
        self.cpt = {} # dict. Key: parent value. Value: list of values
        self.children = []
        self.parents = []
