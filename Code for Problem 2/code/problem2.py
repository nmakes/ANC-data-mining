import csv

minSup = 0.001
minConf = 0.1

monthFile = "p2/aug/augGroups.csv"

with open(monthFile) as csvfile:

    reader = csv.reader(csvfile, delimiter=',')

    data = []

    for line in reader:
        data.append(set([int(x) for x in line]))


two = []
length = float(len(data))

with open('p2/aug/augTwoGroups.csv', 'r') as csvfile:

    reader = csv.reader(csvfile, delimiter=',')

    for line in reader:
        two.append(set([int(x) for x in line]))

rules = []


for pair in two:

    count = 0.

    for record in data:

        if pair.issubset(record):
            count += 1.

    if (count / length) > minSup:

        count0 = 0.
        count1 = 0.

        pair = list(pair)

        for d in data:

            if pair[0] in d:
                count0 += 1.

            if pair[1] in d:
                count1 += 1.

        if (count0 > count1) and (count / count1 > minConf):
            rules.append([str(pair[1]) + ' -> ' + str(pair[0]), count / length,
                          count / count1])

        elif (count1 > count0) and (count / count0 > minConf):
            rules.append([str(pair[0]) + ' -> ' + str(pair[1]), count / length,
                          count / count0])


with open('p2/aug/aug2rules.csv', 'w') as csvfile:

    writer = csv.writer(csvfile, delimiter=',')

    for r in rules:
        writer.writerow(r)
