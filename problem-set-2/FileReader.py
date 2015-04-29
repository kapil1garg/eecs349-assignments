import csv

categories = []
data = []

#skipinitialspace removes starting spaces from elements
csv_input = csv.reader(open("./data/btest.csv","rb"), skipinitialspace=True, delimiter=",", quoting=csv.QUOTE_NONE)

row_count = 0
for row in csv_input:
	if row_count == 0:
		categories = row
	else:
		data.append(row)
	row_count += 1

print data

