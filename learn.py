def learn(dataset, model):
    for i in range(100):
        model.random_init()
    pass

def modify_and_evaluate(dataset, model):
    neighbors = model.get_neighbors()
    best_score = None
    best_model = None
    for n in neighbors:
        score = n.get_MDL_length()
        for o in dataset:
            score += n.get_MDL_encoding(o)
        if best_score is None or score > best_score:
            best_score = score
            best_model = n
    return (best_model, best_score)
