import csv

class CSVReader:
    """Read CSV files

    Attributes: 
        header: list of strings compromising the header row
        data: list of lists with parsed data
        file: string of file to be parsed
    """

    def __init__(self, filename):
        self.header = []
        self.data = []
        self.file = filename


    def readFile(self):
        """Reads file line by line, assigning values for header row and data

        Returns:
            list header: list of header values
            list data: list where each element is a row of data
        """
        csv_input = csv.reader(open(self.file, "rb"), skipinitialspace = True, delimiter = ",", quoting = csv.QUOTE_NONE)

        row_count = 0
        for row in csv_input:
            if row_count == 0:
                self.header = row
            else:
                self.data.append(row)
            row_count += 1

        return self.header, self.data