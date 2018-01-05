import csv

combos = []
prices = {}

with open('combos.csv') as csvfile:

    reader = csv.reader(csvfile, delimiter=',')

    for record in reader:
        combos.append(record[0].split(' -> '))


with open('../Dataset/monthwisePriceList.csv') as csvfile:

    reader = csv.reader(csvfile, delimiter=',')

    next(reader)

    for record in reader:
        prices[record[0]] = record[-1]
