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
    h = cpt.Dataset("datasets/renault_small.csv")
    # h = cpt.Dataset("datasets/test.csv")
    print(len(h.get_compatible({"v1":"0","v2":"2","v3":"0","v41":"1"})))
    print(h.get_count({"v1":"0","v2":"2","v3":"0","v41":"1"},"v7"))
    print(h.get_pref_order({"v1":"0","v2":"2","v3":"0","v41":"1"},"v7"))
    aaailearn.learn_lptree(h, 100)
