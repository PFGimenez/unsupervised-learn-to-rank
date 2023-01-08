import outcome
import aaailearn
import mdllearn
import cpnet

def open_dataset(file):
    d = []
    with open(file, mode='r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            d.append(row)
    return d

if __name__ == "__main__":
    csv = outcome.read_csv("datasets/renault_smallest.csv")
    h = outcome.Dataset(csv)

    net = cpnet.CPNet(h.vars)
    net.update_cpt(h)
    net.add_child(net.nodes[0], net.nodes[1])
    net.add_child(net.nodes[1], net.nodes[2])
    net.merge_nodes(net.nodes[1], net.nodes[0])
    print(net.get_MDL(h))
    # net.add_child(net.nodes[0], net.nodes[1])
    # net.add_child(net.nodes[2], net.nodes[1])
    net.update_cpt(h)
    net.export("cpnet.dot")
    # print(net.get_MDL(h))

    # l = aaailearn.learn_lptree(h, 500, 1)
    # l.root.export("out.dot")
    # print("Initial LP-tree obtained")
    # print("Empirical mean rank:",l.get_mean_rank(h))
    # l = mdllearn.learn(h, l)
    # print("Empirical mean rank:",l.get_mean_rank(h))
    # l.root.export("out2.dot")

    # l = aaailearn.learn_lptree(h, 1000, 1)
    # l.root.export("out.dot")
    # print("Empirical mean rank:",l.get_mean_rank(h))
    # print("Model MDL:",l.get_model_MDL())
    # print("Data MDL:",l.get_data_MDL(h))
    # print("Total MDL:",l.get_MDL(h))
    # l,_ = mdllearn.modify_and_evaluate(h, l)
    # l.root.export("out2.dot")
    # print("Empirical mean rank:",l.get_mean_rank(h))
    # print("Model MDL:",l.get_model_MDL())
    # print("Data MDL:",l.get_data_MDL(h))
    # print("Total MDL:",l.get_MDL(h))
