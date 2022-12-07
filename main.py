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
    g = aaailearn.learn_lptree(h, 1000)
    g.export("out.dot")
