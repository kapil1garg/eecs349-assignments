import math
import TreeElement
import copy

class DecisionTree:
  """Creates and stores a decision tree

  Attributes: 
      data: list of lists with parsed data
      meta: dictionary identifying headers
      dt: the full decision tree
      nLeaves: number of leaves in unpruned tree
      pruneLeaves: number of leaves after pruning tree
  """

  def __init__(self, tempdata, tempmeta):
    self.data = tempdata
    self.meta = tempmeta
    self.dt = []
    self.nLeaves = 0
    self.pruneLeaves = 0
    
    #Find the "solutions" column and label it
    for att in self.meta:
        if self.meta[att]["type"] == "binary":
            self.binary_index = self.meta[att]["index"]
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
              if float(i) < float(min_val):
                min_val = i
              elif float(i) > float(max_val): 
                max_val = i
        stat_vector = [float(min_val), float(max_val), float(max_val) - float(min_val)] # min, max, range
        self.meta[att]["stats"] = stat_vector

    # Add values for nominal attributes
    for att in self.meta:
      if self.meta[att]["type"] == "nominal":
        att_index = self.meta[att]["index"]
        nominal_values = []

        for i in self.data[att_index]:
          if i != "?" and not (i in nominal_values):
            nominal_values.append(i)
        self.meta[att]["values"] = nominal_values

  def treeMaker(self):
    """Creates the tree

    Returns:
        dt (list): the complete decision tree (also stores this value in dt)
    """

    #Generate attributes list
    attributes = [att for att in self.meta.keys() if att != self.binary_att]

    #create tree
    self.dt = self.DTL(self.data, attributes)
    return self.dt

  def DTL(self, examples, attributes, default = None):
    """Builds a decision tree recursively

    Args: 
      examples (list of list): list of lists containing all data
      attribute (string): attribute to split on and calculate gain
      default (obj): value to use when examples are empty, None if no value specified

    Returns:
        TreeElement: the filled decision tree
    """
    if len(examples[0]) == 0: #A leaf-node
      self.nLeaves += 1
      return str(default)
    elif self.sameClass(examples[self.binary_index]): #Should be a leaf-node
      self.nLeaves += 1
      return str(examples[self.binary_index][0])
    elif len(attributes) == 0: #Run out of attributes
      self.nLeaves += 1
      return str(self.mode(examples[self.binary_index]))
    else:
      bestAtt, bestSplits = self.chooseAttribute(examples, attributes)
      if bestAtt ==  None: #if there is no best to choose
        return str(self.mode(examples[self.binary_index]))
      split_examples = self.splitData(examples, bestAtt, bestSplits)
      if self.meta[bestAtt]["type"] == "numeric":
        string_lessequal = "<=" + str(bestSplits)
        string_greater = ">" + str(bestSplits)
        bestSplits = [string_lessequal, string_greater]

      tree = {bestAtt: {}}

      #create the subtrees recursively
      for split_index in range(len(split_examples)):
        subtree = self.DTL(split_examples[split_index], [att for att in attributes if att != bestAtt],
         self.mode(examples[self.binary_index]))
        tree[bestAtt][bestSplits[split_index]] = subtree
    return tree
    
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
    return 0 if (num0 > num1) else 1

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

    #If it's a numeric, split into two lists
    #Less than or equal to, and greater than
    if self.meta[attribute]["type"] == "numeric":
      subtrees = [[] for _ in range(2)]
      lessThan = [[] for _ in range(len(examples))]
      greaterThan = [[] for _ in range(len(examples))]
      for row in range(len(examples[0])): 
        if examples[attribute_index][row] == "?":
          for element in range(len(examples)): 
            questions[element].append(examples[element][row])
        elif float(examples[attribute_index][row]) <= float(splits):
          for element in range(len(examples)): 
            lessThan[element].append(examples[element][row])
        elif float(examples[attribute_index][row]) > float(splits):
          for element in range(len(examples)): 
            greaterThan[element].append(examples[element][row])
      subtrees[0] = lessThan
      subtrees[1] = greaterThan
    
    #If it's a nominal, split into several lists
    #Organized by type of nominal
    elif self.meta[attribute]["type"] == "nominal":
      counter = 0
      subtrees = [[] for _ in range(len(splits))]
      for split in splits:
        tempTree = [[] for _ in range(len(examples))]
        subtrees[counter] = tempTree
        counter += 1
      counter = 0
      for row in range(len(examples[0])):
        if examples[attribute_index][row] == "?": 
          for element in range(len(examples)): 
            questions[element].append(examples[element][row])
        else:
          counter = 0
          while counter < len(splits):
            if examples[attribute_index][row] == splits[counter]:
              for element in range(len(examples)): 
                subtrees[counter][element].append(examples[element][row])
            counter += 1

    #Find the largest subtree
    biggestTree = 0
    largestSize = 0
    for i in range(len(subtrees)):
      if len(subtrees[i][0]) > largestSize:
        largestSize = len(subtrees[i][0])
        biggestTree = i

    #Put the examples with unknown attribute values into the largest split
    for i in range(len(questions[0])):
      for k in range(len(questions)):
        if(len(subtrees)>0):
          subtrees[biggestTree][k].append(questions[k][i])
    return subtrees


  def chooseAttribute(self, examples, attributes):
    """Chooses best attribute to split on

    Args: 
      examples (list of list): list of lists containing all data
      attribute (string): attribute to split on and calculate gain

    Returns:
        element bestAt: the best attribute to split on
        number bestSplits: the lits of best splits for bestAt
    """
    gains = [[] for _ in range(len(attributes))]
    splits = [[] for _ in range(len(attributes))]

    names = []

    counter = 0
    for attribute in attributes:
      #If it's nominal, calculate the gains for all of it's subtrees
      if self.meta[attribute]["type"] == "nominal":
        tempGain = self.gain(examples, attribute, self.meta[attribute]["values"])
        gains[counter] = tempGain
        splits[counter] = (self.meta[attribute]["values"]) 

      #If it's numeric, calculate gains on a split at the midpoint
      elif self.meta[attribute]["type"] == "numeric":
        midpoint = (self.meta[attribute]["stats"][0] + self.meta[attribute]["stats"][1])/2
        tempGain = self.gain(examples, attribute, midpoint)
        gains[counter] = tempGain
        splits[counter] = (midpoint)
      names.append(attribute)
      counter += 1
    
    #Find attribute that provides maximum gain
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

    binary_1_count = classification.count("1")
    binary_0_count = classification.count("0")
    total_rows = float(binary_1_count + binary_0_count) + EPSILON

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
    total_gain = 0.0

    # total examples and count
    for split in split_examples:
      all_examples += (split[self.binary_index])
    all_count = len(all_examples)

    total_gain += self.entropy(all_examples)
    total_split_gain = 0

    # split examples and count
    for split in split_examples:
      total_split_gain += (split[self.binary_index].count("1")/float(all_count)) * self.entropy(split[self.binary_index])
    
    total_gain = total_gain - total_split_gain
    return total_gain

  def remove_blank(self, data):
    #Remove blank examples from data set
    processed_data = [[] for _ in range(len(data))]
    for i in range(len(data[0])): 
      if data[self.binary_index][i] != "?":
        for j in range(len(data)):
          processed_data[j].append(data[j][i])
    return processed_data

  def classify(self, tree, data):
    #Determine the outputs by running through tree
    data_length = len(data[0])
    data_indices = range(data_length)
    classifications = [""] * data_length

    for i in data_indices:
      current_instance = []
      for j in data:
        current_instance.append(j[i])
      classifications[i] = self.recursive_classify(tree, current_instance)
    return classifications

  def recursive_classify(self, tree, instance):
    if not tree:
      return None
    elif not (type(tree) is dict):
      return tree
    else:
      current_key = tree.keys()[0] #Attribute
      current_splits = tree[current_key].keys()
      att_index = self.meta[current_key]["index"]
      att_type = self.meta[current_key]["type"]

      if instance[att_index] == "?":
        return self.recursive_classify(tree[current_key][current_splits[0]], instance)
      elif att_type == "numeric": #If it's numeric, remove the string segment and classify accordingly
        numeric_key = current_splits[0]
        if "<=" in numeric_key:
          numeric_key = float(numeric_key.replace("<=", ""))
          if float(instance[att_index]) <= numeric_key:
            return self.recursive_classify(tree[current_key][current_splits[0]], instance)
          else:
            return self.recursive_classify(tree[current_key][current_splits[1]], instance)
        else:
          numeric_key = float(numeric_key.replace(">", ""))
          if float(instance[att_index]) > numeric_key:
            return self.recursive_classify(tree[current_key][current_splits[0]], instance)
          else:
            if len(tree[current_key]) > 1:
              return self.recursive_classify(tree[current_key][current_splits[1]], instance)
      else: #If it's nominal, classify the splits normally
        for split in current_splits:
          if instance[att_index] == split:
            return self.recursive_classify(tree[current_key][split], instance)
            break


  def accuracy(self, trueData, testData):
    """Determines accuracy of testData

    Returns:
      float error: error of testData compared to trueData
    """
    EPSILON = math.exp(-100) # must be added to avoid issues with 0/0
    numDiff = 0
    total = 0
    true_length = len(trueData[self.binary_index])
    true_indicies = range(true_length)
    if testData == 1 or testData == 0:
      for row in true_indicies:
        total += 1
        if trueData[self.binary_index][row] != str(testData):
          numDiff += 1
    else:
      for row in true_indicies:
        total += 1
        if trueData[self.binary_index][row] != testData[row]:
          numDiff += 1
    acc = (float(total)-float(numDiff))/(float(total) + EPSILON)
    return acc


  def prune(self, tree, examples):
    """Prune the given tree

    Returns:
      int accuracy: pruned tree
    """
    #If tree is a leaf-node
    if not(type(tree) is dict):
      return tree

    #Check pruning state
    classification = self.classify(tree, examples)
    thisAccuracy = self.accuracy(examples, classification)
    thisMode = self.mode(examples[self.binary_index])
    modeAccuracy = self.accuracy(examples, thisMode)
    if modeAccuracy-thisAccuracy>0.2:
      return str(thisMode)

    #Attribute
    key = tree.keys()[0]

    splits = []
    #For each split in the splits
    for spl in tree[key].keys(): 
      if "<=" in spl:
        splits = spl.replace("<=", "")
        break
      elif ">" in spl:
        splits = spl.replace(">", "")
        break
      else:
        splits.append(spl)

    newTree = {key: {}}

    split_examples = self.splitData(examples, key, splits) 

    #If it's a numeric, make two splits accordingly
    if type(splits) != list: 
      new_splits = []
      new_splits.append("<=" + splits)
      new_splits.append(">" + splits)
      splits = new_splits

    #for each split, recurse 
    for spl in range(len(split_examples)):
      subtree = self.prune(tree[key][splits[spl]], split_examples[spl])
      newTree[key][splits[spl]] = subtree
    return newTree

  def pruneLeafCount(self, tree):
    if not (type(tree) is dict):
      self.pruneLeaves += 1
    else:
        for i in tree[tree.keys()[0]].keys():
            self.pruneLeafCount(tree[tree.keys()[0]][i]) 