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
print "Number leaves: " + str(thisTree.nLeaves) + "\n"

# For printing tree nicely
import json
# print json.dumps(tree, indent = 1)

# Load validation set
validation_set = csv.CSVReader("./data/bvalidate.csv")
validate_header, validate_data = validation_set.readFile()
validate_data = thisTree.remove_blank(validate_data)

# Prune tree
# thisTree.prune(tree, validate_data)

# Classify training set
training_data = thisTree.remove_blank(training_data)
training_classification = thisTree.classify(tree, training_data)

# Calculate accuracy
correct = 0
incorrect = 0
training_length = len(training_data[0])
training_width = len(training_data)
training_indicies = range(training_length)
for i in training_indicies:
    if training_data[training_width - 1][i] != training_classification[i]:
        incorrect += 1
    else:
        correct += 1

print "Percentage Correct on Training set w/o Pruning: " + \
    str(100 * float(correct)/training_length) + "%"        
print "Percentage Incorrect on Training set w/o Pruning: " + \
    str(100 * float(incorrect)/training_length) + "%"
print "Total Instances classified: " + str(correct + incorrect) + "\n"

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
    str(100 * float(correct)/validate_length) + "%"        
print "Percentage Incorrect on Validation set w/o Pruning: " + \
    str(100 * float(incorrect)/validate_length) + "%"
print "Total Instances classified: " + str(correct + incorrect) + "\n"

# # Printing in Disjunctive Normal Form
# positive_classification = []
# negative_classification = []
# def dict_dfs(tree, output = ""):
#     if not (type(tree) is dict):
#         last_opp = output.rfind(" ^ ")
#         output = output[:last_opp]
#         if int(tree) == 1:
#             positive_classification.append(output)
#         else:
#             negative_classification.append(output)
#         # output += ": " + str(tree)
#         # print output
#     else:
#         output += str(tree.keys()[0])
#         for i in tree[tree.keys()[0]].keys():
#             # output += " is " + str(i)
#             dict_dfs(tree[tree.keys()[0]][i], output + " is " + str(i) + " ^ ")
# dict_dfs(tree) 
# counter = 0
# print_limit = 16
# while counter < print_limit:
#     print "(" + positive_classification[counter] + ") V",
#     counter += 1
# print ": 1"
# counter = 0
# while counter < print_limit:
#     print "(" + negative_classification[counter] + ") V",
#     counter += 1
# print ": 0"
# print "Total Paths: " + str(len(positive_classification) + len(negative_classification))





