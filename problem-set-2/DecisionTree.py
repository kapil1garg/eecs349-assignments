import math
import TreeElement

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
    self.exclude = [] # TODO: THIS WILL BE USED TO HOLD ALL ATTRIBUTES ALREADY CHECKED
    
    for att in self.meta:
        if self.meta[att]["type"] == "binary":
            self.binary_index = self.meta[att]["index"]

  def preprocessing(self):
    """Removes any unclassified instances from the training data and validation data"""
    processed_data = [[] for _ in range(len(self.data))]
    for i in range(len(self.data[0])): 
      if self.data[self.binary_index][i] != "?":
        for j in range(len(self.data)):
          processed_data[j].append(self.data[j][i])
    self.data = processed_data

  def treeMaker():
    """Creates the tree

    Returns:
        dt (list): the complete decision tree (also stores this value in dt)
    """
    #dt = DTL(data, meta)
    #if dt:
    #   dt = prune(dt)
    #return dt
    pass

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
    elif sameClass(examples[self.binary_index]):
      return examples[self.binary_index][0]
    elif len(attribute) == 0:
      return mode(examples[self.binary_index])
    else:
      bestAtt, bestSplits = chooseAttribute(examples, attributes)
      split_examples = splitData(examples, bestAtt, bestSplits)

      tree = TreeElement(bestAtt)
      self.exclude.append(bestAtt)

      for split_index in range(len(bestSplits)): 
        selected_examples = split_examples[split_index]
        subtree = DTL(selected_examples, [att for att in attributes if att not in self.exclude], mode(examples[binary_index]))
        tree.add_branch(TreeElement(subtrees))
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
    subtrees = []
    questions = []
    processed_data = [[] for _ in range(len(examples))]

    if self.meta[attribute]["type"] == "numeric":
      subtrees[0] = []
      subtrees[1] = []
      for i in range(len(examples[0])):
        if examples[self.meta[attribute][index]][i] <= splits[0]:
          subtrees[0].append(case)
        elif examples[self.meta[attribute][index]][i] > splits[0]:
          subtrees[1].append(case)
        else:
          questions.append(case)

    elif self.meta[attribute]["type"] == "nominal":
      for i in range(len(splits)):
        subtrees[i] = []
      for i in range(len(examples[0])):
        for j in range(len(splits)):
          if examples[self.meta[attribute][index]][i] == splits[j]:
            subtrees[j].append(case)
          elif exampes[self.meta[attribute][index][i] == "?"]:
            questions.append(case)

    biggestTree = 0
    largestSize = 0
    for i in range(len(subtrees)):
      if len(subtrees[i]) > largestSize:
        largestSize = len(subtrees[i])
        biggestTree = i
    for case in questions:
      subtrees[biggestTree].append(case)
    
    return subtrees


      
  #TODO: WRITE METADATALISTS FOR NOMINAL VALUES, AND CALL IT "values" (and numeric- at least ranges would     be nice; max, min; call it "stats"; stats[0] = min, stats[1] = max, stats[2] = range)  (Kapil)
  #TODO: WRITE GAIN(examples, attribute, value). This should split data and caluclate the right half of that equation (DONT INCLUDE THE NEGATIVE SIGN)

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
    gains = []
    splits = []
    #Set each value to be an array itself
    for i in range(len(attributes)):
      gains[i] = []
      splits[i] = []
    counter = 0
    for attribute in attributes:
      if self.meta[attribute]["type"] == "nominal":
        rowcount = 0
        for value in self.meta[attribute][values]:
          splits[counter][rowcount] = value
          rowcount += 1
        gains[counter] = gain(examples, attribute, splits[counter])
      elif self.meta[attribute]["type"] == "numeric":
        rowcount = 0
        midpoint = (self.meta[attribute][stats][2] / 2) + self.meta[attribute][stats][0]; 
        splits[counter][rowcount] = midpoint
        gains[counter] = gain(examples, attribute, splits[counter])
        rowcount += 1
      counter += 1
    
    maxGain = 0
    maxOuterKey = 0
    counter = 0
    for cats in gains:
      if gains[counter] > maxGain:
        maxGain = gains[counter]
        maxOuterKey = counter
      counter += 1
    
    bestAtt = attributes[maxOuterKey]
    bestSplits = splits[maxOuterKey]
    return bestAtt, bestSplits
                  

  EPSILON = math.exp(-100) # must be added to avoid issues with log(0)
  def entropy(self, classification):
    """Calculate entropy of given att/spl
    
    Args:
        classification: list of classifications for training set
    
    Returns:
        float: entropy of the attribute at the split
    """
    binary_1_count = 0
    binary_0_count = 0
    total_rows = 0

    for i in classification:
      if i == 1:
        binary_1_count += 1
      elif i == 0:
        binary_0_count += 1
      total_rows += 1

    total_rows = float(total_rows)

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
    split_examples = splitData(examples, attribute, splits)
    all_examples = []
    all_count = 0
    total_gain = 0

    # total examples and count
    for split in split_examples:
      all_examples += split[self.binary_index]
    all_count = len(all_examples)

    # split examples and count
    for split in split_examples:
      total_gain -= (len(split[self.binary_index])/all_count) * entropy(split[self.binary_index])

    total_gain += entropy(all_examples)
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