import csv

file_name = ("august.csv")

output = []


def extractData(reader):

    retList = []

    for line in reader:
        retList.append([int(x) for x in line])

    return retList


with open(file_name) as csvfile:

    reader = csv.reader(csvfile, delimiter=',')

    output = extractData(reader)

    for o in output:
        print(o)
