import math
import TreeElement
import copy

class DecisionTree:
  """Creates and stores a decision tree

  Attributes: 
      data: list of lists with parsed data
      meta: dictionary identifying headers
      dt: the full decision tree
      exclude: holds all attributes already checked
  """

  def __init__(self, tempdata, tempmeta):
    self.data = tempdata
    self.meta = tempmeta
    self.dt = []
    # TODO: THIS WILL BE USED TO HOLD ALL ATTRIBUTES ALREADY CHECKED
    
    for att in self.meta:
        if self.meta[att]["type"] == "binary":
            self.binary_index = self.meta[att]["index"]
            self.exclude = [att]

    self.preprocessing()

  def preprocessing(self):
    """Removes any unclassified instances from the training data and validation data"""
    processed_data = [[] for _ in range(len(self.data))]
    for i in range(len(self.data[0])): 
      if self.data[self.binary_index][i] != "?":
        for j in range(len(self.data)):
          processed_data[j].append(self.data[j][i])
    self.data = processed_data

    # Add min, max, range
    for att in self.meta:
      if self.meta[att]["type"] == "numeric":
        att_index = self.meta[att]["index"]

        min_val = 0
        max_val = 0
        counter = 0
        while min_val == 0:
          if self.data[att_index][counter] != "?":
            min_val = self.data[att_index][counter]
            max_val = self.data[att_index][counter]
          counter += 1

        for i in self.data[att_index]:
            if i != "?":
              if i < min_val:
                min_val = i
              elif i > max_val: 
                max_val = i
        stat_vector = [float(min_val), float(max_val), float(max_val) - float(min_val)] # min, max, range
        self.meta[att]["stats"] = stat_vector



  def treeMaker(self):
    """Creates the tree

    Returns:
        dt (list): the complete decision tree (also stores this value in dt)
    """
    dt = self.DTL(self.data, self.meta)
    print dt
    return dt

    #dt = DTL(data, meta)
    #if dt:
    #   dt = prune(dt)
    #return dt

  def DTL(self, examples, attributes, default = None):
    """Builds a decision tree recursively

    Args: 
      examples (list of list): list of lists containing all data
      attribute (string): attribute to split on and calculate gain
      default (obj): value to use when examples are empty, None if no value specified

    Returns:
        TreeElement: the filled decision tree
    """
    if len(examples[0]) == 0:
      return default
    elif self.sameClass(examples[self.binary_index]):
      return examples[self.binary_index][0]
    elif len(attributes) == 0:
      return self.mode(examples[self.binary_index])
    else:
      bestAtt, bestSplits = self.chooseAttribute(copy.deepcopy(examples), copy.deepcopy(attributes))
      split_examples = self.splitData(copy.deepcopy(examples), copy.deepcopy(bestAtt), copy.deepcopy(bestSplits))

      print bestAtt

      tree = TreeElement.TreeElement(copy.deepcopy(bestAtt))
      self.exclude.append(copy.deepcopy(bestAtt))

      print self.exclude
      #useAtts = []
      #for att in attributes:
      #  if self.exclude[att] == False:
      #    useAtts.append(att)

      for split_index in split_examples:
        print "Run for each split_example"
        print len(split_index[0])
        subtree = self.DTL(copy.deepcopy(split_index), [copy.deepcopy(att) for att in attributes if att not in self.exclude], self.mode(copy.deepcopy(examples[self.binary_index])))
        print " You made a subtree"
        tree.add_branch(TreeElement.TreeElement(subtree))
        print " You added the subtree"
      return tree
    
  # DONE
  def mode(self, examples):
    """Most common binary value in a list
    
    Args:
      examples (list): values to check, must be binary
    
    Returns:
      int: most common binary option
    """
    num0 = 0
    num1 = 0
    for element in examples:
        if element:
            num1 += 1
        else:
            num0 += 1

    return 0 if (num0 > num1) else 1

  # DONE
  def sameClass(self, examples):
    """If all examples have same classification
    
    Args:
        examples (list): values to check.

    Returns:
      boolean: whether all examples are of the same class.
    """
    return all(x == examples[0] for x in examples)
      
  def splitData(self, examples, attribute, splits):
    """Makes sublists with data matching attribute

    Args: 
      examples (list of list): list of lists containing all data
      attribute (string): attribute to split on
      splits (list): items to split examples on
    
    Returns:
        list[]: the data fitting along the split
        list[]: the data fitting outside the split
    """
    subtrees = [[]]*len(splits)
    questions = [[]]*len(examples)
    processed_data = [[] for _ in range(len(examples))]

    if self.meta[attribute]["type"] == "numeric":
      subtrees = [[]]*2
      subtrees[0] = [[]]*len(examples)
      subtrees[1] = [[]]*len(examples)
      for i in range(len(examples[0])):
        if examples[self.meta[attribute]["index"]][i] <= splits[0]:
          for j in range(len(examples)):
            subtrees[0][j].append(examples[j][i])
        elif examples[self.meta[attribute]["index"]][i] > splits[0]:
          for j in range(len(examples)):
            subtrees[1][j].append(examples[j][i])
        else:
          for k in range(len(examples)):
            questions[k].append(examples[k][i])

    elif self.meta[attribute]["type"] == "nominal":
      for i in range(len(splits)):
        subtrees[i] = [[]]*len(examples)
      for i in range(len(examples[0])):
        for j in range(len(splits)):
          if examples[self.meta[attribute]["index"]][i] == splits[j]:
            for k in range(len(examples)):
              subtrees[j][k].append(examples[k][i])
          elif examples[self.meta[attribute]["index"]][i] == "?":
            for k in range(len(examples)):
              questions[k].append(examples[k][i])

    biggestTree = 0
    largestSize = 0
    for i in range(len(subtrees)):
      if len(subtrees[i][0]) > largestSize:
        largestSize = len(subtrees[i][0])
        biggestTree = i



    print "splitData on: " + attribute
    print "Largest Tree Size: " + str(largestSize)
    print "subtree size before ?: " + str(len(subtrees[0][1]))

    for i in range(len(questions[0])):
      for k in range(len(questions)):
        subtrees[biggestTree][k].append(questions[k][i])

    print "subtree size after ?: " + str(len(subtrees[0][0]))
    return subtrees


  def getRow(self, examples, numRow):
    """Returns the row in examples

    Returns:
      list[]: the row from examples
    """

    row = []
    for att in examples:
      row.append(att[numRow])

    return row

  def chooseAttribute(self, examples, attributes):
    """Chooses best attribute to split on

    Args: 
      examples (list of list): list of lists containing all data
      attribute (string): attribute to split on and calculate gain

    Returns:
        element bestAt: the best attribute to split on
        number bestSplits: the lits of best splits for bestAt
    """
    #for each attribute -- calculate entropy at multiple points, compare them all together to find smallest
    gains = [[]]*len([att for att in attributes if att not in self.exclude])

    splits = [[]]*len([att for att in attributes if att not in self.exclude])
    #Set each value to be an array itself
    names = []*len([att for att in attributes if att not in self.exclude])

    counter = 0
    for attribute in [att for att in attributes if att not in self.exclude]:
      if self.meta[attribute]["type"] == "nominal":
        for value in self.meta[attribute]:#[values]:
          splits[counter].append(value)
        temp = self.gain(examples, attribute, splits[counter])
        print temp
        gains[counter] = temp

      elif self.meta[attribute]["type"] == "numeric":
        midpoint = (self.meta[attribute]["stats"][2] / 2) + self.meta[attribute]["stats"][0]; 
        splits[counter].append(midpoint)
        temp = self.gain(examples, attribute, splits[counter])
        print temp
        gains[counter] = temp
      names.append(attribute)
      counter += 1
    
    maxGain = 0
    maxOuterKey = 0
    counter = 0
    for cats in gains:
      if gains[counter] > maxGain:
        maxGain = gains[counter]
        maxOuterKey = counter
      counter += 1

    bestAtt = names[maxOuterKey]
    bestSplits = splits[maxOuterKey]
    return bestAtt, bestSplits
                  

  
  def entropy(self, classification):
    """Calculate entropy of given att/spl
    
    Args:
        classification: list of classifications for training set
    
    Returns:
        float: entropy of the attribute at the split
    """
    EPSILON = math.exp(-100) # must be added to avoid issues with log(0)
    binary_1_count = 0
    binary_0_count = 0
    total_rows = 0

    for i in classification:
      if i == 1:
        binary_1_count += 1
      elif i == 0:
        binary_0_count += 1
      total_rows += 1

    total_rows = float(total_rows) + EPSILON

    positive_probability = (binary_1_count/total_rows)
    negative_probability = (binary_0_count/total_rows)
    return (-positive_probability * math.log(EPSILON + positive_probability, 2)) - (negative_probability * math.log(EPSILON + negative_probability, 2))


  def gain(self, examples, attribute, splits):
    """Calculates information gain for an attribute among all its splits.

    Args: 
      examples (list of list): list of lists containing all data
      attribute (string): attribute to split on and calculate gain
      splits (list): items to split examples on

    Returns:
      (float): gain acquired from splitting on attribute  
    """
    split_examples = self.splitData(examples, attribute, splits)
    all_examples = []
    all_count = 0
    total_gain = 0

    # total examples and count
    # print len(split_examples[0])
    for split in split_examples:
      all_examples.append(split[self.binary_index])
    all_count = len(all_examples)
    # print all_examples
    # print all_count

    # split examples and count
    for split in split_examples:
      total_gain -= (len(split[self.binary_index])/all_count) * self.entropy(split[self.binary_index])

    total_gain += self.entropy(all_examples)
    print total_gain
    return total_gain

  def sort_attributes(self, attribute, output):
    """Sorts a numeric attribute and its corresponding classfication

    Args:
      attribute (array): list of values to be sorted
      output (array): list of classifications corresponding to attribute

    Returns: 
      (array), (array): first array is sorted attribute, second is corresponding classification
    """
    sorted_tuples = sorted(zip(attribute, output))
    return [att for (att, classification) in sorted_tuples], [classify for (att, classification) in sorted_tuples]



  def prune(self, tree):
    """Prune the given tree

    Returns:
        dt prunedTree: pruned tree
    """
    #lolgoodluck
    pass