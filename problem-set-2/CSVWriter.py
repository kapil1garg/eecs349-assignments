import csv

class CSVWriter:
    """Writes CSV files

    Attributes: 
        data: list of lists with parsed data
        header: list of strings compromising the header row
        file: string of file to be written to
    """

    def __init__(self, data, header, filename):
        self.header = header
        self.data = data
        self.file = filename

        self.parseRows()

    def parseRows(self):
        """Parses data into rows"""
        row_data = []
        row_data.append(self.header)

        for i in range(len(self.data[0])):
            temp_row = []
            for j in range(len(self.data)):
                temp_row.append(self.data[j][i])
            row_data.append(temp_row)

        self.data = row_data

    def writeFile(self):
        """Writes file line by line"""
        with open(self.file, 'w') as csvfile:
            my_writer = csv.writer(csvfile, delimiter=',')
            my_writer.writerows(self.data)