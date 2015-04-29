import CSVReader as csv

training_set = csv.CSVReader("./data/btest.csv")
training_header, training_data = training_set.readFile()

print training_header
print training_data