import CSVReader as csv
import MetaReader as meta
import DecisionTree as DT

training_set = csv.CSVReader("./data/btrain.csv")
training_header, training_data = training_set.readFile()

meta_reader = meta.MetaReader("./data/bmeta.csv")
meta_data = meta_reader.parseMetaData()

thisTree = DT.DecisionTree(training_data, meta_data)
#tree = thisTree.treeMaker()

print tree.branches