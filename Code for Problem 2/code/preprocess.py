import csv
from itertools import combinations as com


monthFile = "p2/nov/novGroups.csv"

with open(monthFile) as csvfile:

    reader = csv.reader(csvfile, delimiter=',')

    data = []

    for line in reader:
        data.append([int(x) for x in line])

two = set()
three = set()

for record in data:

    f = com(record, 2)

    for group in f:
        two.add(frozenset(group))


for record in data:

    f = com(record, 3)

    for group in f:
        three.add(frozenset(group))


with open('p2/nov/novTwoGroups.csv', 'w') as csvfile:

    writer = csv.writer(csvfile, delimiter=',')

    for line in two:
        writer.writerow(line)


with open('p2/nov/novThreeGroups.csv', 'w') as csvfile:

    writer = csv.writer(csvfile, delimiter=',')

    for line in three:
        writer.writerow(line)
