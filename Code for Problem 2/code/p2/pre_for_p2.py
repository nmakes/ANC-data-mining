import csv

# Enter file name here
file_name = 'dec/decMod.csv'

file_output = {}

output = []

with open(file_name, 'r') as csv_file:

    reader = csv.reader(csv_file, delimiter=',')

    for i in reader:

        itemID = i[0]
        date = i[3]
        date = date.split(' ')[0]

        # if date in file_output:
        #
        #     file_output[date].append(itemID)
        #
        # else:
        #     file_output[date] = [itemID]


for i in file_output:

    print([i[0], i[1], file_output[i]])


# with open('decFinal.csv', 'w') as csvfile:
#
#     writer = csv.writer(csvfile, delimiter=',')
#
#     for i in file_output:
#
#         writer.writerow([i[0], i[1], file_output[i]])
#
#         print[i[0], i[1], file_output[i]]
