#!/usr/bin/env pypy

import CSVReader as csv
import MetaReader as meta
import DecisionTree as DT

# Load training set
training_set = csv.CSVReader("./data/btrain.csv")
training_header, training_data = training_set.readFile()

# Load meta data
meta_reader = meta.MetaReader("./data/bmeta.csv")
meta_data = meta_reader.parseMetaData()

# Make tree
thisTree = DT.DecisionTree(training_data, meta_data)
tree = thisTree.treeMaker()

# For printing tree nicely
import json
# print json.dumps(tree, indent = 1)

# Load validation set
validation_set = csv.CSVReader("./data/bvalidate.csv")
validate_header, validate_data = validation_set.readFile()
validate_data = thisTree.remove_blank(validate_data)

# Classify validation set
validate_classification = thisTree.classify(tree, validate_data)
# print validate_classification

# Calculate accuracy
correct = 0
incorrect = 0
validate_length = len(validate_data[0])
validate_width = len(validate_data)
validate_indicies = range(validate_length)
for i in validate_indicies:
    if validate_data[validate_width - 1][i] != validate_classification[i]:
        incorrect += 1
    else:
        correct += 1

print "Percentage Correct on Validation set w/o Pruning: " + \
    str(100 * correct/validate_length) + "%"        
print "Percentage Incorrect on Validation set w/o Pruning: " + \
    str(100 * incorrect/validate_length) + "%"
