import outcome
import aaailearn
import mdllearn
import cpnet
import experiment
import ensemble
import sklearn.cluster
import pandas as pd

def open_dataset(file):
    d = []
    with open(file, mode='r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            d.append(row)
    return d

if __name__ == "__main__":
    csv = outcome.read_csv("datasets/renault_smaller_train.csv")
    h = outcome.Dataset(csv)

    csv_test = outcome.read_csv("datasets/renault_smaller_test.csv")
    # csv_test = csv_test.head(2)
    h_test = outcome.Dataset(csv_test)

    # net = cpnet.CPNet(["A","B","C"])
    # net.add_child(net.nodes[0], net.nodes[1])
    # net.add_child(net.nodes[1], net.nodes[2])
    # net.nodes[0].cpt = {(): [("a1",),("a2",)]}
    # net.nodes[1].cpt = {("a1",): [("b1",),("b2",)],("a2",): [("b2",),("b1",)]}
    # net.nodes[2].cpt = {("b1",): [("c1",),("c2",)],("b2",): [("c2",),("c1",)]}
    # print(net.get_path_length({"A": "a2", "B": "b1", "C": "c1"}))
    # net.export("cpnet2.dot")

    # net2 = cpnet.CPNet(h.vars)
    # net2.add_child(net2.nodes[0], net2.nodes[1])
    # net2.update_cpt(h)
    # net2.export("cpnet2.dot")
    # print("Manual MDL:",net2.get_MDL(h))


    # nb_clusters = 2
    # kmeans = sklearn.cluster.KMeans(nb_clusters).fit(csv)
    # models1 = []
    # models2 = []
    # for k in range(nb_clusters):
    #     data = csv.loc[kmeans.labels_ == k]
    #     h_train = outcome.Dataset(data)
    #     print("Cluster size:",len(h_train.dataset))
    #     h_train.domains = h.domains.copy()
    #     h_train.space_size = h.space_size
    #     models1.append(aaailearn.learn_lptree(h_train, 20, 2))
    #     net = cpnet.CPNet(h.vars, h)
    #     models2.append(mdllearn.learn(h_train, net))
    # print("Ensemble,",nb_clusters,"LP-trees")
    # e1 = ensemble.Ensemble(models1)
    # experiment.recommendation_in_config(h_test, e1)
    # print("Ensemble,",nb_clusters,"CP-nets")
    # e2 = ensemble.Ensemble(models2)
    # experiment.recommendation_in_config(h_test, e2)


    print("CP-net learning (baseline)")
    net = cpnet.CPNet(h.vars, h)
    experiment.recommendation_in_config(h, net)
    print("CP-net learning (MDL)")
    net = mdllearn.learn(h, net)
    net.export("cpnet.dot")
    experiment.recommendation_in_config(h, net)

    print("LP-tree learning (AAAI)")
    l = aaailearn.learn_lptree(h, 20, 2)
    # l = mdllearn.learn(h, l)
    l.export("lptree.dot")
    print("Data MDL:",mdllearn.get_data_MDL(l, h_test))

    print("LP-tree learning (MDL)")
    l2 = mdllearn.learn(h, l)
    l2.export("lptree2.dot")

    # print("Data MDL AAAI:",mdllearn.get_data_MDL(l, h_test))
    # print("Data MDL new:",mdllearn.get_data_MDL(l2, h_test))
    experiment.recommendation_in_config(h_test, l)
    experiment.recommendation_in_config(h_test, l2)

    # print("Ensemble, one LP-tree, one CP-net")
    # e = ensemble.Ensemble([l2, net])
    # experiment.recommendation_in_config(h_test, e)



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
