import csv

# Enter file name here
file_name = ('dec/decMod.csv')

output = []

final = {}

count = {}

with open(file_name, 'r') as csv_file:

    reader = csv.reader(csv_file, delimiter=',')

    support_count = {}
    support_count_ant = {}
    price_dict = {}

    for i in reader:

        output.append(i + [False])


for n in range(len(output)):

    i = output[n]

    if i[-1] is True:
        continue

    output[n][-1] = True

    record = [i[0]]

    current_count = 1

    if i[-2] in count:
        count[i[-2]] += 1
        current_count = count[i[-2]]

    else:
        count[i[-2]] = 1

    for m in range(n + 1, len(output)):

        j = output[m]

        if j[-1] is True:
            continue

        if i[-2] != j[-2]:
            break

        if i[1] == j[1]:

            val = abs(int(i[2].split(':')[0]) - int(j[2].split(':')[0]))

            if val == 0 or val == 1:

                record.append(j[0])
                output[m][-1] = True

    final[(i[-2], current_count)] = record


with open('dec/decFinal.csv', 'w') as csvfile:

    writer = csv.writer(csvfile, delimiter=',')

    for f in final:

        writer.writerow([f, final[f]])
