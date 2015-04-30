import math

class DecisionTree:
  """Creates and stores a decision tree

  Attributes: 
      data: list of lists with parsed data
      meta: dictionary identifying headers
      dt: the full decision tree
  """

  def __init__(self, tempdata, tempmeta):
    self.data = tempdata
    self.meta = tempmeta
    self.dt = []
    self.exclude = [] # TODO: THIS WILL BE USED TO HOLD ALL ATTRIBUTES ALREADY CHECKED
    
    for att in self.meta:
        if self.meta[att]["type"] == "binary":
            self.binary_index = self.meta[att]["index"]

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

  def DTL(self, examples, attributes):
    """Fills a tree

    Returns:
        tree DecTree: the filled decision tree
    """
    if not examples: #FIX THIS LINE- should be if examples is empt
      return None
    tempClassification = 0 #first example's classification
    if True:
      pass

    if sameClass(examples):
      return tempClassification

    if not attributes:
      return mode(examples)
    bestAtt = chooseAttribute(examples, attributes)
    #TREE + NEW DT WITH ROOT TEST bestAtt

    #for the following for-loop, check attribute-type to determine the type of split to check for
    
  # DONE
  def mode(self, examples):
    """Most common value in list
    
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
    first_classification = examples[0]
    for element in examples:
      if element != first_classification:
        return False
    return True

    #TODO: WRITE splitData function (Aaron)
      
  def splitData(self, examples, attribute, split):
    """Makes sublists with data matching attribute
    
    Returns:
        list[]: the data fitting along the split
        list[]: the data fitting outside the split
    """
    #switch based on type
    #loop and add em
    
    pass
      
      
  #TODO: WRITE METADATALISTS FOR NOMINAL VALUES, AND CALL IT "values" (and numeric- at least ranges would     be nice; max, min; call it "stats"; stats[0] = min, stats[1] = max, stats[2] = range)  (Kapil)
  #TODO: WRITE GAIN(examples, attribute, value). This should split data and caluclate the right half of that equation (DONT INCLUDE THE NEGATIVE SIGN)

  def chooseAttribute(self, examples, attributes):
    """Chooses best attribute to split on

    Returns:
        element bestAt: the best attribute to split on
        number bestSplit: the best split for bestAt
    """
    #for each attribute -- calculate entropy at multiple points, compare them all together to find smallest
    gains = []
    splits = []
    #Set each value to be an array itself
    for i in range(len(attributes)):
      gains[i] = []
      splits[i] = []
    entropyS = entropy(examples);
    counter = 0
    for attribute in attributes:
      if meta[attribute]["type"] == "nominal":
        rowcount = 0
        for value in meta[attribute][values]:
          gains[counter][rowcount] = entropyS - gain(examples, attribute, value)
          splits[counter][rowcount] = value
          rowcount += 1
      elif meta[attribute]["type"] == "numeric":
        rowcount = 0
        midpoint = (meta[attribute][stats][2] / 2) + meta[attribute][stats][0];
        gains[counter][rowcount] = entropyS - gain(examples, attribute, midpoint)
        splits[counter][rowcount] = midpoint
        rowcount += 1
      counter += 1
    
    maxGain = 0
    maxOuterKey
    maxInnerKey
    counter = 0
    for cats in gains:
      rowcount = 0
      for sub in cats:
        if gains[counter][rowcount] > maxGain:
          maxGain = gains[counter][rowcount]
          maxOuterKey = counter
          maxInnerKey = rowcount
        rowcount += 1
      counter += 1
    
    bestAtt = attributes[maxOuterKey]
    bestSplit = splits[maxOuterKey][maxInnerKey]
    return bestAtt, bestSplit
                  

  EPSILON = math.exp(-100) # must be added to avoid issues with log(0)
  #TODO: DO NOT USE AN ATTRIBUTE, ONLY EXAMPLES
  def entropy(self, examples):
    """Calculate entropy of given att/spl
    
    Args:
        examples: training set of data as array of arrays
    
    Returns:
        float: entropy of the attribute at the split
    """
    binary_1_count = 0
    binary_0_count = 0
    total_rows = 0

    for i in examples[self.binary_index]:
      if i == 1:
        binary_1_count += 1
      elif i == 0:
        binary_0_count += 1
      total_rows += 1

    total_rows = float(total_rows)
    return (-(binary_1_count/total_rows) * math.log(EPSILON + (binary_1_count/total_rows), 2)) - ((binary_0_count/total_rows) * math.log(EPSILON + (binary_0_count/total_rows), 2))

  def gain(self, examples, attribute, splits):
    """Calculates information gain for 
    """
    # if numeric, --> less than, equal to 
    total_gain = 0


    if self.meta[attribute]["type"] == "numeric":
      last_split = None
      next_split = splits[0]

      for split in splits:
        if not last_split:
          pass

    else:
      pass


  def prune(self, tree):
    """Prune the given tree

    Returns:
        dt prunedTree: pruned tree
    """
    #lolgoodluck
    pass