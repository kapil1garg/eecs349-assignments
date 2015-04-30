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

    def treeMaker():
    	"""Creates the tree

        Returns:
            tree dt: the complete decision tree (also stores this value in dt)
        """
        #dt = DTL(data, meta)
        #if dt:
        #	dt = prune(dt)
        #return dt
        pass

    def DTL(examples, attributes):
    	"""Fills a tree

    	Returns:
    		tree DecTree: the filled decision tree
    	"""
      if not examples:
        return None
      tempClassification = #first example's classification
      ifTrue = true;
      if sameClass(examples)
        return tempClassification
      if not attributes
        return mode(examples)
      bestAtt = chooseAttribute(examples, attributes)
      #TREE + NEW DT WITH ROOT TEST bestAtt

      #for the following for-loop, check attribute-type to determine the type of split to check for

    def mode(examples):
      """Most common value

      Returns:
        number val: most common binary output
      """
      num0 = 0
      num1 = 0
      for element examples:
        if:#classification is 0
          num0 += 1
        else:
         if:#classifcation is 1
          num1 += 1

      if num0>num1
        return 0
      return 1

    def sameClass(examples):
      """If all examples have same classification

      Returns:
        boolean yes/no: if all examples are the same class.
      """
      tempClassification = #first example's classification
      for element examples:
        if:#this classification != tempClassification
          return False
      return True


   	def chooseAttribute(examples, attributes):
   		"""Chooses best attribute to split on

   		Returns:
   			element bestAt: the best attribute to split on
   			number bestSplit: the best split for bestAt
   		"""
   		#ohgodnoidea
   		pass

   	def entropy(examples, attribute, split):
   		"""Calculate entropy of given att/spl

   		Returns:
   			number entropy: entropy of the attribute at the split
   		"""
   		#1) Look through every example and tally the ones that correctly fall on either side of the split
      #2) Calculate the proportion of these to the total number (ie proportion of correct classifications)
      #3) entropy(S) = -p1log2(p1) - p2log2(p2)
   		pass

   	def prune(tree):
   		"""Prune the given tree

   		Returns:
   			dt prunedTree: pruned tree
   		"""
   		#lolgoodluck
   		pass

