import copy

"""Create an element for a tree with n branches

  Attributes: 
      data: object stored in element
      branches: list of branches at each element
  """
class TreeElement(object):
    def __init__(self, data):
        self.data = data
        self.splits = []
        self.branches = []

    def __str__(self):
        return str(self.data) + "  " + str(self.splits)

    def set_splits(self, split):
      self.splits = copy.deepcopy(split)

    def add_branch(self, obj):
        self.branches.append(obj)
