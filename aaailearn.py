import graph

def learn_lptree(dataset, tau, seen_vars=[], instance={}):
    # print("Search node. Instance:",instance,"seen vars:",seen_vars)
    # todo leaf
    best_var = None
    score_best = None
    for x in dataset.vars:
        # check non-instanced variables only
        if x in seen_vars:
            continue
        score = 0
        count = dataset.get_count(instance,x)
        # print(x)
        i = 0
        for k,v in count.items():
            i += 1
            # print(i,v)
            score += i*v
        score /= len(dataset.domains[x]) - 1
        # print(score)
        if score_best is None or score < score_best:
            score_best = score
            best_var = x
    # print(best_var)
    label_edges = True
    count = dataset.get_count(instance,best_var)
    # print(best_var,count)
    seen_vars = seen_vars.copy()
    seen_vars.append(best_var)
    n = graph.Node(best_var, dataset.get_pref_order(instance, best_var))
    # leaf
    if len(seen_vars) == len(dataset.vars):
        return n

    if len(count.keys()) < len(dataset.domains[best_var]):
        label_edges = False
    else:
        for k,v in count.items():
            if v < tau: # not enough examples
                label_edges = False
                # print("No labelled edge")
                break
    if label_edges:
        for v in dataset.domains[best_var]:
            new_inst = instance.copy()
            new_inst[best_var] = v
            c = learn_lptree(dataset, tau, seen_vars, new_inst)
            n.add_child(c, v)
    else:
        c = learn_lptree(dataset, tau, seen_vars, instance)
        n.add_child(c)
    return n
