import CSVReader as csv

class MetaReader:
    """Read CSV file containing meta data

    Attributes: 
        attributes: list of strings indicating attributes
        types: list of strings indicating type of attributes
    """

    def __init__(self, filename):
        metaCSV = csv.CSVReader(filename)
        self.attributes, self.types = metaCSV.readFile()

    def parseMetaData(self):
        """Parses attributes and types into a meta data dictionary

        Returns:
            dictionary: each key is an attribute with array value of column index and type
        """
        meta_data = {}

        for i in range(len(self.attributes)):
            meta_data[self.attributes[i]] = {'index': i, 'type': self.types[i][0]}

        return meta_data