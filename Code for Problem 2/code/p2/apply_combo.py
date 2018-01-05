import csv

combos = []
items = []
prices = {}
losses = {}
discount = 0

y = 20
k = 0

with open('combos.csv') as csvfile:

    reader = csv.reader(csvfile, delimiter=',')

    for record in reader:

        combos.append(frozenset(record))


with open('dec/decRecords.csv') as csvfile:

    reader = csv.reader(csvfile, delimiter=',')

    for record in reader:

        items.append(frozenset(record))


with open('../Dataset/monthwisePriceList.csv') as csvfile:

    reader = csv.reader(csvfile, delimiter=',')

    next(reader)

    for record in reader:
        prices[record[0]] = record[-1]


for c in combos:

    c = tuple(c)

    old_price = int(prices[c[0]]) + int(prices[c[1]])

    k = len(c)

    new_price = old_price * (100 - y / k) / 100

    losses[c] = old_price - new_price


for record in items:

    offers = []

    for combo in combos:

        if combo.issubset(record):
            offers.append(combo)

    def f(x):
        return losses[tuple(x)]

    if len(offers) > 0:
        discount += losses[tuple(max(offers, key=f))]

print(discount)
