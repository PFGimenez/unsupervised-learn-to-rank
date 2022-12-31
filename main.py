import cpt
import aaailearn

def open_dataset(file):
    d = []
    with open(file, mode='r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            d.append(row)
    return d

if __name__ == "__main__":
    h = cpt.Dataset("datasets/renault_smaller.csv")
    # print(h.get_count({"v1":"0","v2":"2","v3":"0","v41":"1"},["v7","v6","v4"]))
    # print(h.get_domain(["v7","v6"]))
    l = aaailearn.learn_lptree(h, 1000, 1)
    l.tree.export("out.dot")
    print("Empirical mean rank:",l.get_mean_rank(h))
    print("Model MDL:",l.get_model_MDL())
    print("Data MDL:",l.get_data_MDL(h))
