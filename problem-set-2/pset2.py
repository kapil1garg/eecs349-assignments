import CSVReader as csv
import CSVWriter
import MetaReader as meta
import DecisionTree as DT

########################################################################
####################### LOAD NECESSARY DATA ############################
########################################################################

# Load training set
training_set = csv.CSVReader(raw_input("Please enter the full filepath of the TRAINING DATA below: \n"))
# training_set = csv.CSVReader("./data/btrain.csv")
training_header, training_data = training_set.readFile()

# Load meta data
meta_reader = meta.MetaReader(raw_input("\nPlease enter the full filepath of the META DATA below: \n"))
# meta_reader = meta.MetaReader("./data/bmeta.csv")
meta_data = meta_reader.parseMetaData()

# Load validation set
validation_set = csv.CSVReader(raw_input("\nPlease enter the full filepath of the VALIDATION DATA below: \n"))
# validation_set = csv.CSVReader("./data/bvalidate.csv")
validate_header, validate_data = validation_set.readFile()

# Load test set 
test_set = csv.CSVReader(raw_input("\nPlease enter the full filepath of the TEST DATA below: \n"))
# test_set = csv.CSVReader("./data/btest.csv")
test_header, test_data = test_set.readFile()

print "\nAll data loaded successfully.\nBuilding model and classifying...\n"

########################################################################
#################### MAKE REGULAR AND PRUNED TREE ######################
########################################################################

# Make DecisionTree class object
thisTree = DT.DecisionTree(training_data, meta_data)

# Remove any unclassifed (? in binary)
training_data = thisTree.remove_blank(training_data)
validate_data = thisTree.remove_blank(validate_data)

# Store binary index for use in classification
class_index = thisTree.binary_index 

# Make unpruned tree
tree = thisTree.treeMaker()
unpruned_leaf_count = thisTree.nLeaves

# Create pruned tree
prunedTree = thisTree.prune(tree, validate_data)
thisTree.pruneLeafCount(prunedTree)
pruned_leaf_count = thisTree.pruneLeaves

import json
# Print unpruned tree
# print "Unpruned Tree"
# print json.dumps(tree, indent = 1)

# Print pruned tree
print "Pruned Tree"
print json.dumps(prunedTree, indent = 1)

########################################################################
#################### CLASSIFY AND FIND ACCURACY ########################
########################################################################

# Accuracy function
def classificationAccuracy(true_class, predicted_class):
    correct = 0.0
    incorrect = 0.0

    true_class_len = len(true_class)
    predicted_class_len = len(predicted_class)
    if true_class_len != predicted_class_len:
        print "Classification Accurary: Input and output lengths are not equal!"
        return None, None
    else:
        for i in range(true_class_len):
            if true_class[i] != predicted_class[i]:
                incorrect += 1
            else:
                correct += 1
        return 100*(correct/true_class_len), 100*(incorrect/true_class_len), true_class_len

# Classify training set
unpruned_training_classification = thisTree.classify(tree, training_data)
unpruned_training_correct, unpruned_training_incorrect, unpruned_training_instances = classificationAccuracy(training_data[class_index], unpruned_training_classification)

pruned_training_classification = thisTree.classify(prunedTree, training_data)
pruned_training_correct, pruned_training_incorrect, pruned_training_instances = \
    classificationAccuracy(training_data[class_index], pruned_training_classification)

# Classify validation set
unpruned_validate_classification = thisTree.classify(tree, validate_data)
unpruned_validate_correct, unpruned_validate_incorrect, unpruned_validate_instances = \
    classificationAccuracy(validate_data[class_index], unpruned_validate_classification)

pruned_validate_classification = thisTree.classify(prunedTree, validate_data)
pruned_validate_correct, pruned_validate_incorrect, pruned_validate_instances = \
    classificationAccuracy(validate_data[class_index], pruned_validate_classification)

print "Unpruned Tree: Number leaves = " + str(thisTree.nLeaves)
print "Pruned Tree: Number leaves = " + str(thisTree.pruneLeaves)
print "Percent leaves pruned = " + str((100.0 * (thisTree.nLeaves - thisTree.pruneLeaves))/thisTree.nLeaves) + "% \n"

print "Percentage Correct on Training set w/o Pruning: " + str(unpruned_training_correct) + "%"        
print "Percentage Incorrect on Training set w/o Pruning: " + str(unpruned_training_incorrect) + "%"
print "Total Instances classified: " + str(unpruned_training_instances) + "\n"

print "Percentage Correct on Training set w/Pruning: " + str(pruned_training_correct) + "%"        
print "Percentage Incorrect on Training set w/Pruning: " + str(pruned_training_incorrect) + "%"
print "Total Instances classified: " + str(pruned_training_instances) + "\n"

print "Percentage Correct on Validation set w/o Pruning: " + str(unpruned_validate_correct) + "%"        
print "Percentage Incorrect on Validation set w/o Pruning: " + str(unpruned_validate_incorrect) + "%"
print "Total Instances classified: " + str(unpruned_validate_instances) + "\n"

print "Percentage Correct on Validation set w/Pruning: " + str(pruned_validate_correct) + "%"        
print "Percentage Incorrect on Validation set w/Pruning: " + str(pruned_validate_incorrect) + "%"
print "Total Instances classified: " + str(pruned_validate_instances) + "\n"

# Printing in Disjunctive Normal Form
def dict_dfs(tree, output = ""):
    if not (type(tree) is dict):
        last_opp = output.rfind(" ^ ")
        output = output[:last_opp]
        if int(tree) == 1:
            positive_classification.append(output)
        else:
            negative_classification.append(output)
    else:
        output += str(tree.keys()[0])
        for i in tree[tree.keys()[0]].keys():
            dict_dfs(tree[tree.keys()[0]][i], output + " is " + str(i) + " ^ ")

print "Unpruned DNF (first 16)"
positive_classification = []
negative_classification = []
dict_dfs(tree)
for i in range(16): 
    print "(",
    print positive_classification[i],
    print ") V ",

print "\nPruned DNF (first 16)"
positive_classification = []
negative_classification = []
dict_dfs(prunedTree)
for i in range(16): 
    print "(",
    print positive_classification[i],
    print ") V ",

########################################################################
################### CLASSIFY AND OUTPUT TEST SET #######################
########################################################################
print "\nClassifying Test Data"
test_data[class_index] = thisTree.classify(prunedTree, test_data)
test_csv = CSVWriter.CSVWriter(test_data, test_header, raw_input("\nPlease enter the full filepath of where you wish to output the CLASSIFIED TEST DATA below: \n"))
#test_csv = CSVWriter.CSVWriter(test_data, test_header, "./data/btest_classified.csv")
test_csv.writeFile()

########################################################################
#################### CREATE LEARNING CURVE #############################
########################################################################
print "\n\nGENERATING LEARNING CURVE DATA"
total_training_instances = len(training_data[0])
n_iterations = 10
percentiles = range(0, 101, 100/n_iterations)
percentiles = percentiles[1:]
counter = 0
unpruned_accuracies = []
pruned_accuracies = []

while counter < n_iterations: 
    min_index = 0
    max_index = ((counter + 1) * total_training_instances/n_iterations) + 1

    current_data = [[] for _ in range(len(training_data))]
    for att in range(len(training_data)):
        current_data[att] = training_data[att][min_index:max_index]
    
    # Build unpruned and pruned trees
    learning_curve = DT.DecisionTree(current_data, meta_data)
    learning_curve_tree_unpruned = learning_curve.treeMaker()
    learning_curve_tree_pruned = learning_curve.prune(learning_curve_tree_unpruned, validate_data)

    # Classify validation data using unpruned and pruned trees
    unpruned_learning_classification = learning_curve.classify(learning_curve_tree_unpruned, validate_data)
    unpruned_learning_correct, unpruned_learning_incorrect, unpruned_learning_instances = \
        classificationAccuracy(validate_data[class_index], unpruned_learning_classification)

    pruned_learning_classification = learning_curve.classify(learning_curve_tree_pruned, validate_data)
    pruned_learning_correct, pruned_learning_incorrect, pruned_learning_instances = \
        classificationAccuracy(validate_data[class_index], pruned_learning_classification)

    # Print accuracies
    print "Number of elements used for Training Set: " + str(max_index) + "(" + \
        str((100.0 * max_index)/total_training_instances) + "%)"
    print "Percentage Correct on Validation set w/o Pruning: " + str(unpruned_learning_correct) + "%" 
    print "Percentage Correct on Validation set w/Pruning: " + str(pruned_learning_correct) + "%\n"  

    # Add to lists
    unpruned_accuracies.append(unpruned_learning_correct)
    pruned_accuracies.append(pruned_learning_correct)
    counter += 1

for i in range(len(percentiles)):
    print str(percentiles[i]) + "," + str(unpruned_accuracies[i]) + "," + str(pruned_accuracies[i])