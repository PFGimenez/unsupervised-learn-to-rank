import aaailearn
import random
import math

# # random order
# def get_data_MDL2(model, dataset):
#     sum_score = 0
#     var_order = dataset.vars.copy()
#     for instance in dataset.uniques:
#         # print("Score for",instance)
#         partial_inst = {}
#         random.shuffle(var_order)
#         for v in var_order:
#             predict, correction_order = model.get_preferred_extension(partial_inst)
#             # print("Extension of",partial_inst,"is",predict)
#             if predict != instance: # error
#                 sum_score += dataset.counts[repr(instance)]
#                 partial_inst[v] = instance[v] # give another clue
#                 # print("Error")
#             else:
#                 # print("All good")
#                 break
#     return sum_score

# # always correct a variable
# def get_data_MDL3(model, dataset):
#     sum_score = 0
#     for instance in dataset.uniques:
#         print("Score for",instance)
#         partial_inst = {}
#         while True:
#             print(partial_inst)
#             predict, correction_order = model.get_preferred_extension(partial_inst)
#             print("Prediction:",predict)
#             for k in correction_order:
#                 # predict may miss values
#                 if predict.get(k) is None:
#                     predict[k] = dataset.get_pref_order(predict, [k])[0]
#                     print("Fill with most common:",predict[k])
#                     # predict[k] = dataset.domain[k]
#                 if instance[k] != predict[k]: # error
#                     print("Error for",k)
#                     sum_score += dataset.counts[repr(instance)] * math.log(len(dataset.vars)) # TODO: how to count?
#                     partial_inst[k] = instance[k] # give one clue
#                 else:
#                     print("No error")
#             break # no error
#     return sum_score

def get_data_MDL_one_instance(model, instance):
    # print("Score for",instance)
    var_order = list(instance.keys())
    for i in range(len(var_order)):
        random.shuffle(var_order)
        # print("A",i,var_order)
        partial_inst = {}
        for j in range(i):
            partial_inst[var_order[j]] = instance[var_order[j]]

        predict = model.get_preferred_extension(partial_inst)

        if predict == instance: # found it
            break
    return i * math.log(len(instance))


# one prediction per order
def get_data_MDL(model, dataset):
    random.seed(0)
    sum_score = 0
    # for instance in dataset.dataset:
    for instance in dataset.uniques:
        for i in range(3):
            sum_score += get_data_MDL_one_instance(model, instance) * dataset.counts[repr(instance)] / 3
    return sum_score


def get_MDL(model, dataset):
    # return model.get_MDL(dataset) # version with log(rank)
    model_MDL = model.get_model_MDL()
    data_MDL = get_data_MDL(model, dataset)
    # print(model_MDL, data_MDL, model_MDL+data_MDL)
    return model_MDL + data_MDL

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
