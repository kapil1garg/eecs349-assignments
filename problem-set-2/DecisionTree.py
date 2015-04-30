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

    def DTL(examples, attributes):
        """Fills a tree

        Returns:
            tree DecTree: the filled decision tree
        """
      if not examples: #FIX THIS LINE- should be if examples is empt
        return None
      tempClassification = 0 #first example's classification
      if True = true:

      if sameClass(examples):
        return tempClassification

      if not attributes:
        return mode(examples)
      bestAtt = chooseAttribute(examples, attributes)
      #TREE + NEW DT WITH ROOT TEST bestAtt

      #for the following for-loop, check attribute-type to determine the type of split to check for
      
    # DONE
    def mode(examples):
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
    def sameClass(examples):
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
        
    def splitData(examples, attribute, split):
        """Makes sublists with data matching attribute
        
        Returns:
            list[]: the data fitting along the split
            list[]: the data fitting outside the split
        """
        #switch based on type
        #loop and add em
        
        pass
        
        
        #TODO: WRITE METADATALISTS FOR NOMINAL VALUES, AND CALL IT "values" (and numeric- at least ranges would     be nice; max, min; call it "stats"; stats[0] = min, stats[1] = max, stats[2] = range)  (Kapil)


    def chooseAttribute(examples, attributes):
        """Chooses best attribute to split on

        Returns:
            element bestAt: the best attribute to split on
            number bestSplit: the best split for bestAt
        """
        #for each attribute -- calculate entropy at multiple points, compare them all together to find smallest
        entropies = []
        splits = []
        #Set each value to be an array itself
        for i in range(len(attributes)):
            entropies[i] = []
            splits[i] = []
        
        counter = 0
        for attribute in attributes:
            if meta[attribute]["type"] == "nominal":
                rowcount = 0
                for value in meta[attribute][values]:
                    entropies[counter][rowcount] = entropy(examples, attribute, splitData(examples, attribute, value))
                    splits[counter][rowcount] = value
                    rowcount += 1
            elif meta[attribute]["type"] == "numeric":
                rowcount = 0
                for i in range(meta[attribute][stats][0], meta[attribute][stats][1], meta[attribute][stats][2]/10):
                    entropies[counter][rowcount] = entropy(examples, attribute, es[counter][rowcount] = entropy(examples, attribute, splitData(examples, attribute, i))
                    splits[counter][rowcount] = i
                    rowcount += 1
            counter += 1
        
        minEntropy = 1
        minOuterKey
        minInnerKey
        counter = 0
        for cats in entropies:
            rowcount = 0
            for sub in cats:
                if entropies[counter][rowcount] < minEntropy:
                    minEntropy = entropies[counter][rowcount]
                    minOuterKey = counter
                    minInnerKey = rowcount
                rowcount += 1
            counter += 1
        
        bestAtt = attributes[minOuterKey]
        bestSplit = splits[minOuterKey][minInnerKey]
        return bestAtt, bestSplit
                    

    NON_ZERO_ADDITION = 1e-10 # must be added to avoid issues with log(0)
    def entropy(self, examples, attribute):
      """Calculate entropy of given att/spl
      
      Args:
          examples: training set of data as array of arrays
          attribute: string attribute to calculate entropy for
      
      Returns:
          int: entropy of the attribute at the split
      """
      #1) Look through every example and tally the ones that correctly fall on either side of the split
      #2) Calculate the proportion of these to the total number (ie proportion of correct classifications)
      #3) entropy(S) = -p1log2(p1) - p2log2(p2)
      
      attribute_index = self.meta[attribute]["index"]
      

    def prune(tree):
      """Prune the given tree

      Returns:
          dt prunedTree: pruned tree
      """
      #lolgoodluck
      pass