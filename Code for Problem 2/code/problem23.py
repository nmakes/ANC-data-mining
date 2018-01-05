import csv

monthFile = "p2/nov/nov2rules.csv"

with open(monthFile) as csvfile:

    reader = csv.reader(csvfile, delimiter=',')

    data = []

    for record in reader:
        data.append(record)


with open('p2/average_rating.csv') as csvfile:

    reader = csv.reader(csvfile, delimiter=',')

    ratings = []

    for record in reader:
        ratings.append(record)


for i in range(len(data)):

    data[i][1] = float(data[i][1])
    data[i][2] = float(data[i][2])

valid_rules = []

for d in data:

    if d[1] >= 0.01 and d[1] < 0.02:
        valid_rules.append(d)


for i in range(len(valid_rules)):

    left = str(valid_rules[i][0].split(' ')[0])
    right = str(valid_rules[i][0].split(' ')[2])

    for record in ratings:

        if left == record[0]:
            valid_rules[i].append(record[1])
            break

    for record in ratings:

        if right == record[0]:
            valid_rules[i].append(record[1])
            break


with open('p2/nov/nov2rulesFinal.csv', 'w') as csvfile:

    writer = csv.writer(csvfile, delimiter=',')

    for v in valid_rules:

        writer.writerow(v[:3])
        writer.writerow(v[3:])
        writer.writerow('')
