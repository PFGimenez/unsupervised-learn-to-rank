import random

def recommendation_in_config(test_set, model):
    correct = [0]*len(test_set.vars)
    total = [0]*len(test_set.vars)
    var_order = test_set.vars.copy()
    for instance in test_set.dataset:
        partial_inst = {}
        random.shuffle(var_order)
        i = 0
        for v in var_order:
            predict, _ = model.get_preferred_extension(partial_inst)
            if predict.get(v) == instance[v]: # correct
                correct[i] += 1
            total[i] += 1
            partial_inst[v] = instance[v] # give another clue
            i += 1
    print(sum(correct),"/",sum(total),", ",(100*sum(correct)/sum(total)),"%")
    return sum(correct)/sum(total)
