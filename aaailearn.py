import itertools
import lptree

def powerset(iterable, k):
    s = list(iterable)
    return list(itertools.chain.from_iterable(itertools.combinations(s, r) for r in range(1,k+1)))

def compare_two_sets(set1, set2, dataset, instance):
    pass

def learn_lptree(dataset, tau, k):
    return lptree.LPTree(_learn_lptree(dataset, tau, k), dataset.vars)

def _learn_lptree(dataset, tau, k, seen_vars=[], instance={}):
    # print("Search node. Instance:",instance,"seen vars:",seen_vars)
    # todo leaf
    best_var = None
    score_best = None

    sets = powerset(set(dataset.vars).difference(seen_vars),k)

    # for x in set(dataset.vars).difference(seen_vars):
    for x in sets:
        x = list(x)
        # x = [x]
        score = 0
        count = dataset.get_count(instance,x)
        i = 0
        for _,v in count.items():
            i += 1
            # print(i,v)
            score += i*v
        score /= dataset.get_domain_size(x) - 1
        # print("Score:",score)
        if score_best is None or score < score_best:
            score_best = score
            best_var = x
    # print(best_var)
    # print("Chosed",best_var)
    count = dataset.get_count(instance,best_var)
    # print(best_var,count)
    label_edges = True
    seen_vars = seen_vars.copy()
    seen_vars += best_var
    n = lptree.Node(best_var, dataset.get_domain_size(best_var), dataset.get_pref_order(instance, best_var), dataset.vars, dataset.space_size)

    # leaf
    if len(seen_vars) == len(dataset.vars):
        return n

    if True: # new behavior, with both labeled and unlabeled edges
        total_count = 0
        for _,v in count.items():
            total_count += v
        for v in n.cpt:
            co = count[v]
            if co >= tau and total_count - co >= tau:
                new_inst = instance.copy()
                dataset.instantiate(new_inst, best_var, v)
                c = _learn_lptree(dataset, tau, k, seen_vars, new_inst)
                n.add_child(c, v)
                total_count -= co
            else:
                new_inst = instance.copy()
                dataset.instantiate(new_inst, best_var, v)
                c = _learn_lptree(dataset, tau, k, seen_vars, new_inst)
                n.add_child(c) # create a branch with all the other values
                # learn with the most common value instantiated
                break

                new_inst = instance.copy()
                dataset.instantiate(new_inst, best_var, v)

    else: # Legacy behavior (AAAI’18), with either labeled or unlabeled edges
        if len(count.keys()) < dataset.get_domain_size(best_var):
            label_edges = False
        else:
            for _,v in count.items():
                if v < tau: # not enough examples
                    label_edges = False
                    # print("No labelled edge")
                    break
        if label_edges:
            for v in dataset.get_domain(best_var):
                new_inst = instance.copy()
                dataset.instantiate(new_inst, best_var, v)
                c = _learn_lptree(dataset, tau, k, seen_vars, new_inst)
                n.add_child(c, v)
        else:
            c = _learn_lptree(dataset, tau, k, seen_vars, instance)
            n.add_child(c)

    return n
