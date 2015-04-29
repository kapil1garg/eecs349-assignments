import csv

numCat = 14
categories = []
data = []

#skipinitialspace removes starting spaces from elements
cr = csv.reader(open("btest.csv","rb"), skipinitialspace=True, delimiter=",", quoting=csv.QUOTE_NONE)

tempCount = 0
for row in cr:
	if tempCount == 0:
		categories = row
	else:
		# data [tempCount - 1] = row
		data.append(row)
	tempCount += 1

print categories

