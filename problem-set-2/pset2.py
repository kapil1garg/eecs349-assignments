import CSVReader as csv
import MetaReader as meta
import DecisionTree as DT

########################################################################
####################### LOAD NECESSARY DATA ############################
########################################################################

# Load training set
training_set = csv.CSVReader(raw_input("Please enter the full filepath of the TRAINING DATA below: \n"))
training_header, training_data = training_set.readFile()

# Load meta data
meta_reader = meta.MetaReader(raw_input("\nPlease enter the full filepath of the META DATA below: \n"))
meta_data = meta_reader.parseMetaData()

# Load validation set
validation_set = csv.CSVReader(raw_input("\nPlease enter the full filepath of the VALIDATION DATA below: \n"))
validate_header, validate_data = validation_set.readFile()

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
# print "Unpruned Tree"
# print json.dumps(prunedTree, indent = 1)

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
positive_classification = []
negative_classification = []
def dict_dfs(tree, output = ""):
    if not (type(tree) is dict):
        last_opp = output.rfind(" ^ ")
        output = output[:last_opp]
        if int(tree) == 1:
            positive_classification.append(output)
        else:
            negative_classification.append(output)
        # output += ": " + str(tree)
        # print output
    else:
        output += str(tree.keys()[0])
        for i in tree[tree.keys()[0]].keys():
            # output += " is " + str(i)
            dict_dfs(tree[tree.keys()[0]][i], output + " is " + str(i) + " ^ ")
