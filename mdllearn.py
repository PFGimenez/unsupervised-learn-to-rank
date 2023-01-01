import aaailearn

def learn(dataset, initial_model):
    best_score = None
    best_model = None
    l = initial_model
    while True:
        l,s = modify_and_evaluate(dataset, l)
        if best_score is None or s < best_score:
            best_model = l
            best_score = s
            print("Current MDL:",l.get_MDL(dataset))
        else:
            break
    return best_model

def modify_and_evaluate(dataset, model):
    neighbors = model.get_neighbors()
    best_score = None
    best_model = None
    for n in neighbors:
        if n is None:
            continue
        score = n.get_MDL(dataset)
        if best_score is None or score < best_score:
            best_score = score
            best_model = n
    return (best_model, best_score)
