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
    
    for att in self.meta:
        if self.meta[att]["type"] == "binary":
            self.binary_index = self.meta[att]["index"]
            # self.exclude = [att]
            self.binary_att = att

    self.preprocessing()

  def preprocessing(self):
    """Removes any unclassified instances from the training data and validation data"""
    processed_data = [[] for _ in range(len(self.data))]
    for i in range(len(self.data[0])): 
      if self.data[self.binary_index][i] != "?":
        for j in range(len(self.data)):
          processed_data[j].append(self.data[j][i])
    self.data = processed_data

    # Add min, max, range for numeric attributes
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

    # Add values for nominal attributes
    for att in self.meta:
      if self.meta[att]["type"] == "nominal":
        att_index = self.meta[att]["index"]
        nominal_values = []

        for i in self.data[att_index]:
          if i != "?" and not i in nominal_values:
            nominal_values.append(i)
        self.meta[att]["values"] = nominal_values

  def treeMaker(self):
    """Creates the tree

    Returns:
        dt (list): the complete decision tree (also stores this value in dt)
    """
    attributes = [att for att in self.meta.keys() if att != self.binary_att]
    dt = self.DTL(self.data, attributes)
    return dt

  def DTL(self, examples, attributes, default = None):
    """Builds a decision tree recursively

    Args: 
      examples (list of list): list of lists containing all data
      attribute (string): attribute to split on and calculate gain
      default (obj): value to use when examples are empty, None if no value specified

    Returns:
        TreeElement: the filled decision tree
    """
    print attributes
    if len(examples[0]) == 0:
      print "No examples: ",
      print default
      return default
    elif self.sameClass(examples[self.binary_index]):
      print "Is same class: ", 
      #print examples[self.binary_index][0],
      print attributes,
      print examples
      return examples[self.binary_index][0]
    elif len(attributes) == 0:
      print "No attributes: ",
      print self.mode(examples[self.binary_index])
      return self.mode(examples[self.binary_index])
    else:
      bestAtt, bestSplits = self.chooseAttribute(examples, attributes)
      split_examples = self.splitData(examples, bestAtt, bestSplits)
      if self.meta[bestAtt]["type"] == "numeric":
        string_lessequal = "<=" + str(bestSplits)
        string_greater = ">" + str(bestSplits)
        bestSplits = [string_lessequal, string_greater]

      print "Best Splits: ",
      print bestSplits
      print "Split exampels length: ",
      print len(split_examples)

      tree = {bestAtt: {}}
      # tree.set_splits(bestSplits)
      # self.exclude.append(bestAtt)

     #useAtts = []
      #for att in attributes:
      #  if self.exclude[att] == False:
      #    useAtts.append(att)

      for split_index in range(len(split_examples)):
       # print "Run for each split_example"
        #print len(split_index[0])
        subtree = self.DTL(split_examples[split_index], [att for att in attributes if att != bestAtt],
         self.mode(examples[self.binary_index]))
        #print " You made a subtree"
        tree[bestAtt][bestSplits[split_index]] = subtree
        # print " You added the subtree ",
        # print tree
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
        if element == "1":
            num1 += 1
        else:
            num0 += 1
    print "Mode calculations: 0: " + str(num0) + " 1: "+ str(num1)
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

    subtrees = []
    questions = [[] for _ in range(len(examples))]
    attribute_index = self.meta[attribute]["index"]

    if self.meta[attribute]["type"] == "numeric":
      print "    numeric"
      subtrees = [[] for _ in range(2)]
      lessThan = [[] for _ in range(len(examples))]
      greaterThan = [[] for _ in range(len(examples))]
      for row in range(len(examples[0])): #for each row/element in examples
        if examples[attribute_index][row] == "?":
          for element in range(len(examples)): #for each column/attribute in examples
            questions[element].append(copy.deepcopy(examples[element][row]))
        elif float(examples[attribute_index][row]) <= float(splits):
          for element in range(len(examples)): #for each column/attribute in examples
            lessThan[element].append(copy.deepcopy(examples[element][row]))
        elif float(examples[attribute_index][row]) > float(splits):
          for element in range(len(examples)): #for each column/attribute in examples
            greaterThan[element].append(copy.deepcopy(examples[element][row]))
      subtrees[0] = copy.deepcopy(lessThan)
      subtrees[1] = copy.deepcopy(greaterThan)
    
    elif self.meta[attribute]["type"] == "nominal":
      print "    nominal"
      counter = 0
      subtrees = [[] for _ in range(len(splits))]
      for split in splits:
        tempTree = [[] for _ in range(len(examples))]
        subtrees[counter] = copy.deepcopy(tempTree)
        counter += 1
      counter = 0
      for row in range(len(examples[0])):
        if examples[attribute_index][row] == "?": #THIS IS TRUE A CRAZY NUMBER OF TIMES
          for element in range(len(examples)): #for each column/attribute in examples
            questions[element].append(copy.deepcopy(examples[element][row]))
        else:
          counter = 0
          while counter < len(splits):
            if examples[attribute_index][row] == splits[counter]:
              for element in range(len(examples)): #for each column/attribute in examples
                subtrees[counter][element].append(copy.deepcopy(examples[element][row]))
            counter += 1


    #print "Length of subtree: " + str(len(subtrees[0][0]))   
    #print "Length of questions: " + str(len(questions[0]))
    #print "          Only once per runthrough"
    biggestTree = 0
    largestSize = 0
    for i in range(len(subtrees)):
      if len(subtrees[i][0]) > largestSize:
        largestSize = len(subtrees[i][0])
        biggestTree = i

    for i in range(len(questions[0])):
      for k in range(len(questions)):
        if(len(subtrees)>0):
          subtrees[biggestTree][k].append(questions[k][i])
    #print "subtree size after ?: " + str(len(subtrees))
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
    #gains = [[] for _ in range(len([att for att in attributes if att not in self.exclude]))]
    #splits = [[] for _ in range(len([att for att in attributes if att not in self.exclude]))]
    gains = [[] for _ in range(len(attributes))]
    splits = [[] for _ in range(len(attributes))]
    #Set each value to be an array itself
    names = []

    counter = 0
    # for attribute in [att for att in attributes if att not in self.exclude]:
    for attribute in attributes:
      if self.meta[attribute]["type"] == "nominal":
        gains[counter] = self.gain(examples, attribute, self.meta[attribute]["values"])
        splits[counter] = (self.meta[attribute]["values"]) #IT WORKS WITHOUT THIS LINE, BUT IT REALLY SHOULDN'T

      elif self.meta[attribute]["type"] == "numeric":
        midpoint = (self.meta[attribute]["stats"][2] / 2) + self.meta[attribute]["stats"][0]; 
        splits[counter] = (midpoint)
        gains[counter] = self.gain(examples, attribute, splits[counter])
      names.append(attribute)
      counter += 1

    print gains
    print splits
    
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
      if i == "1":
        binary_1_count += 1
      elif i == "0":
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
      all_examples += (split[self.binary_index])
    all_count = len(all_examples)

    # split examples and count
    for split in split_examples:
      total_gain -= (split[self.binary_index].count("1")/float(all_count)) * self.entropy(split[self.binary_index])

    total_gain += self.entropy(all_examples)
    print "Gain: " + str(total_gain)
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