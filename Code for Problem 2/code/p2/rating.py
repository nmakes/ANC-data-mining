import csv

aug = open('../Dataset/augSales.csv', 'r')
sep = open('../Dataset/sepSales.csv', 'r')
octo = open('../Dataset/octSales.csv', 'r')
nov = open('../Dataset/novSales.csv', 'r')

aug_reader = csv.reader(aug, delimiter=',')
sep_reader = csv.reader(sep, delimiter=',')
oct_reader = csv.reader(octo, delimiter=',')
nov_reader = csv.reader(nov, delimiter=',')

next(aug_reader)
next(sep_reader)
next(oct_reader)
next(nov_reader)

ratings = {}
count = {}

for record in aug_reader:

    item = record[1]
    rating = record[-1]

    print(item, rating)

    if item in ratings.keys():
        ratings[item] += rating
        count[item] += 1.

    else:
        ratings[item] = rating
        count[item] = 1.

for i in ratings:
    print(i, ratings[i])
