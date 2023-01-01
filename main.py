import cpt
import aaailearn
import mdllearn

def open_dataset(file):
    d = []
    with open(file, mode='r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            d.append(row)
    return d

if __name__ == "__main__":
    csv = cpt.read_csv("datasets/renault_smaller.csv")
    h = cpt.Dataset(csv)
    l = aaailearn.learn_lptree(h, 1000, 1)
    l.tree.export("out.dot")
    print("Initial LP-tree obtained")
    print("Empirical mean rank:",l.get_mean_rank(h))
    l = mdllearn.learn(h, l)
    print("Empirical mean rank:",l.get_mean_rank(h))
    l.tree.export("out2.dot")
    # l = aaailearn.learn_lptree(h, 1000, 1)
    # l.tree.export("out.dot")
    # print("Empirical mean rank:",l.get_mean_rank(h))
    # print("Model MDL:",l.get_model_MDL())
    # print("Data MDL:",l.get_data_MDL(h))
    # print("Total MDL:",l.get_MDL(h))
    # l,_ = mdllearn.modify_and_evaluate(h, l)
    # l.tree.export("out2.dot")
    # print("Empirical mean rank:",l.get_mean_rank(h))
    # print("Model MDL:",l.get_model_MDL())
    # print("Data MDL:",l.get_data_MDL(h))
    # print("Total MDL:",l.get_MDL(h))
