import aaailearn
import random
import math

# random order
def get_data_MDL2(model, dataset):
    sum_score = 0
    var_order = dataset.vars.copy()
    for instance in dataset.uniques:
        # print("Score for",instance)
        partial_inst = {}
        random.shuffle(var_order)
        for v in var_order:
            predict, correction_order = model.get_preferred_extension(partial_inst)
            # print("Extension of",partial_inst,"is",predict)
            if predict != instance: # error
                sum_score += dataset.counts[repr(instance)]
                partial_inst[v] = instance[v] # give another clue
                # print("Error")
            else:
                # print("All good")
                break
    return sum_score

# always correct a variable
def get_data_MDL3(model, dataset):
    sum_score = 0
    for instance in dataset.uniques:
        print("Score for",instance)
        partial_inst = {}
        while True:
            print(partial_inst)
            predict, correction_order = model.get_preferred_extension(partial_inst)
            print("Prediction:",predict)
            for k in correction_order:
                # predict may miss values
                if predict.get(k) is None:
                    predict[k] = dataset.get_pref_order(predict, [k])[0]
                    print("Fill with most common:",predict[k])
                    # predict[k] = dataset.domain[k]
                if instance[k] != predict[k]: # error
                    print("Error for",k)
                    sum_score += dataset.counts[repr(instance)] * math.log(len(dataset.vars)) # TODO: how to count?
                    partial_inst[k] = instance[k] # give one clue
                else:
                    print("No error")
            break # no error
    return sum_score

# one prediction per order
def get_data_MDL(model, dataset):
    random.seed(0)
    sum_score = 0
    var_order = dataset.vars.copy()
    # for instance in dataset.dataset:
    for instance in dataset.uniques:
        # print("Score for",instance)
        for i in range(len(dataset.vars)):
            random.shuffle(var_order)
            partial_inst = {}
            for j in range(i):
                partial_inst[var_order[j]] = instance[var_order[j]]

            predict, _ = model.get_preferred_extension(partial_inst)
            for v in var_order:
                if predict.get(v) is None:
                    predict[v] = dataset.get_pref_order(predict, [v])[0]
                    # print("Fill with most common:",predict[v])

            if predict != instance: # error
                # sum_score += 1
                sum_score += dataset.counts[repr(instance)]
            else:
                # print("All good")
                break
    return sum_score


def get_MDL(model, dataset):
    # return model.get_MDL(dataset) # version with log(rank)
    return model.get_model_MDL() + get_data_MDL(model, dataset) # version with MPE

def learn(dataset, initial_model):
    l = initial_model
    best_model = l
    best_score = get_MDL(l, dataset)
    print("Initial MDL:",best_score)
    while True:
        l,s = modify_and_evaluate(dataset, l)
        if best_score is None or s < best_score:
            best_model = l
            best_score = s
            print("Current MDL:",s)
        else:
            break
    return best_model

def modify_and_evaluate(dataset, model):
    neighbors = model.get_neighbors(dataset)
    best_score = None
    best_model = None
    for n in neighbors:
        if n is None:
            continue
        score = get_MDL(n,dataset)
        # print("Neighbor MDL:",score)
        if best_score is None or score < best_score:
            best_score = score
            best_model = n
    return (best_model, best_score)
