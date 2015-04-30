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
    	#see lectures
    	pass

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
   		#dunnomate
   		pass

   	def prune(tree):
   		"""Prune the given tree

   		Returns:
   			dt prunedTree: pruned tree
   		"""
   		#lolgoodluck
   		pass

