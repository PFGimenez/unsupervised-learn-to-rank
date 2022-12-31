def learn(dataset, model):
    for i in range(100):
        model.random_init()
    pass

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
    return best_model
