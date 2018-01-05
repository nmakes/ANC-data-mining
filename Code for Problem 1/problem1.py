import config
import os
import time
import csv
from sys import stdout

minsup = 20
minconf = 20

maxPPratio = 0
# The minsup and minconf values which give the highest profit / penalty ratio
maxPPratioMinSup = 0
maxPPratioMinConf = 0

class P1: # class for Problem 1
	

	# For every test case, we need to reinitialize the value of minsup and minconf
	@staticmethod
	def initialize():
		with open(config.configFileName) as configFile:
			
			global minsup
			global minconf

			minsup = float(configFile.readline().split('\n')[0])
			minconf = float(configFile.readline())

			print "minsup:", minsup, "%"
			print "minconf:", minconf, "%"


	@staticmethod
	def getSegmentWeight(segment):
		# Desc: returns the segment weight
		# Args:
		# 	- segment = student segment as mentioned

		if segment=='F1':
			return 12
		elif segment=='F2':
			return 32
		elif segment=='F3':
			return 30
		elif segment=='F4':
			return 20
		elif segment=='F5':
			return 3
		elif segment=='H1':
			return 2
		elif segment=='H1':
			return 2
		else:
			return 1


	@staticmethod
	def getHourWeight(hours):
		# Desc: returns the hour weight for the number of hours
		# Args:
		# 	- hours = number of hours the pricing is active for

		if hours > 6:
			return 6**2
		else:
			return (hours ** 2)	# this is the pattern in the given problem statement


	@staticmethod
	def runAutoGenOnFiles(monthWisePricelistFileName, monthFileNameList, pricingFileName):
		# Desc: runs generateAutomatedPricingFile on each month
		# Args:
		# 	- monthWisePricelistFileName: the name of the file corresponding to the monthWisePricelistFile
		#	- monthFileNameList: list of the names of the files corresponding to each month (eg. novSales.csv).
		#	- pricingFileName: this is the intermediate file in which association rules of the form
		#						F2, 17 --> 128

		with open(monthWisePricelistFileName) as monthWisePricelistFile:
			for i in monthFileNameList:
				with open(i) as monthFileList:	
					row = ["#,", (i.split('/'))[1][0:3]]
					monthWisePricelistFile.seek(0,0)
					P1.generateAutomatedPricingFile(monthFileList, monthWisePricelistFile, pricingFileName)

	@staticmethod
	def generateAutomatedPricingFile(monthFile, monthWisePricelistFile, pricingFileName):	
		'''
			Obtain associations of the form:

				student_gp , time_slot -> item

			where,
			student_gp: student group (or segment)
			time_slot: hour in which the purchase is made
			item: the item that was purchased
		'''
		with open(pricingFileName, 'a') as pricingFile:
			
			outputFileWriter = csv.writer(pricingFile, delimiter=',')
			reader = csv.reader(monthFile, delimiter=',')
			next(reader)

			support_count = {}
			support_count_ant = {}
			price_dict = {}

			total_entries = 0

			for i in reader:
				itemID = i[1]
				absHour = (((i[3].split())[1]).split(':'))[0]
				group = i[5][0:2]
				price = i[4]

				total_entries += 1

				price_dict[itemID] = price

				if((group, absHour, itemID) in support_count.keys()):
					support_count[(group, absHour, itemID)] += 1
					if int(itemID) > 1400:
						print i
				else:
					support_count[(group, absHour, itemID)] = 1

				if (group, absHour) in support_count_ant.keys():
					support_count_ant[(group, absHour)] += 1
				else:
					support_count_ant[(group, absHour)] = 1

			priceListReader = csv.reader(monthWisePricelistFile, delimiter=',')
			next(priceListReader)

			items = {}

			for i in priceListReader:
				items[i[0]] = (i[1], i[6]) # (item name, selling price dec)

			outputCount = 0

			for keys in support_count.keys():
				
				(group, absHour, itemID) = keys
				sup = float(support_count[keys]) * 100 / float(total_entries)
				conf = float( float(support_count[keys]) * 100 / float(support_count_ant[(group, absHour)]))

				if ( sup > minsup ) and ( sup < config.maxsup ) and ( conf > minconf ) and ( conf < config.maxconf ):
					outputCount += 1
					if absHour =='00': absHour = '24'
					elif absHour =='01': absHour = '25'
					elif absHour =='02': absHour = '26' 
					#print group, ",", absHour, ",", itemID, ",", items[itemID][1]
					outputFileWriter.writerow([group, absHour, itemID, items[itemID][1]])

	@staticmethod
	def generateNewPriceCSVFromPricingFile(pricingFile):

		with open(pricingFile) as pf:
			reader = csv.reader(pf, delimiter=',')
			month = None
			segments = ['F1','F2','F3','F4','F5','H1','H2','oth']
			hours = [16,17,18,19,20,21,22,23,24,25,26]

			with open(config.newPriceFileName, 'w') as np:
				writer = csv.writer(np, delimiter=',')

				newPrices, _ = P1.readNewPrices()
				#print newPrices
				
				for line in reader:

					if len(line)!=0:
						if line[0]=="#":
							month = line[1]
						else:
							itemID = int(line[2])
							hour = int(line[1])
							seg = line[0].strip()
							price = int(line[3])

							if (0.1 * price < 10):
								pr = 1.1 * price
							else:
								pr = 10

							if seg!= 'F0':
								#print itemID, seg, hour

								if itemID in newPrices:
									if seg in newPrices[itemID]:
										newPrices[itemID]['price'] = price
										newPrices[itemID][seg][hour] = pr
									else:
										newPrices[itemID][seg] = {}
										newPrices[itemID][seg][hour] = pr
								else:
									newPrices[itemID] = {}
									newPrices[itemID][seg] = {}
									newPrices[itemID][seg][hour] = pr
											
				writer.writerow(["ItemID", "SellingPriceDec", "times", "new F1", "new F2", "new F3", 'new F4', 'new F5', 'new H1', 'new H2', 'new others'])

				for itemID in newPrices:
					for hour in hours:
						row = [itemID, 
								newPrices[itemID]['price'], 
								hour, 
								newPrices[itemID]['F1'][hour],
								newPrices[itemID]['F2'][hour],
								newPrices[itemID]['F3'][hour],
								newPrices[itemID]['F4'][hour],
								newPrices[itemID]['F5'][hour],
								newPrices[itemID]['H1'][hour],
								newPrices[itemID]['H2'][hour],
								newPrices[itemID]['oth'][hour]
							]
						writer.writerow(row)

	# CALCULATING PROFIT

	@staticmethod
	def readNewPrices():
		
		newPrices = {}
		segments = ['F1','F2','F3','F4','F5','H1','H2','oth']
		hours = [16,17,18,19,20,21,22,23,24,25,26]
		i = 0

		with open(config.origNewPriceFileName) as newPriceFile:
			
			newPriceReader = csv.reader(newPriceFile, delimiter=',')
			headRead = True

			i = 0

			for line in newPriceReader:
				
				if headRead:
					header = line
					# print header
					headRead = False
				else:
					itemID = int(line[0])
					hour = int(line[2])
					price = float(line[1])

					if itemID not in newPrices:
						newPrices[itemID] = {}

					newPrices[itemID]['price'] = float(price)

					i = 3

					for segment in segments:
						if segment not in newPrices[itemID]:
							newPrices[itemID][segment] = {}

						nPrice = float(line[i])
						newPrices[itemID][segment][hour] = nPrice

						i += 1

		# for key in newPrices:
		# 	print key, ":", newPrices[key]

		return newPrices, None

	@staticmethod
	def readNewGeneratedPrices():
		
		newPrices = {}
		segments = ['F1','F2','F3','F4','F5','H1','H2','oth']
		hours = [16,17,18,19,20,21,22,23,24,25,26]
		i = 0

		with open(config.newPriceFileName) as newPriceFile:
			
			newPriceReader = csv.reader(newPriceFile, delimiter=',')
			headRead = True

			i = 0

			for line in newPriceReader:
				if len(line) != 0:
					if line[0] != "":
						if headRead:
	 						header = line
							# print header
							headRead = False
						else:
							itemID = int(line[0])
							hour = int(line[2])
							price = float(line[1])

							if itemID not in newPrices:
								newPrices[itemID] = {}

							newPrices[itemID]['price'] = float(price)

							i = 3

							for segment in segments:
								if segment not in newPrices[itemID]:
									newPrices[itemID][segment] = {}

								nPrice = float(line[i])
								newPrices[itemID][segment][hour] = nPrice

								i += 1

		# for key in newPrices:
		# 	print key, ":", newPrices[key]

		return newPrices, None

	@staticmethod
	def calculateProfitAndPenalty():

		'''
			decemberData[itemID] = qty
			where qty is the quantity of item <itemID> sold in december
		'''
		decemberData = {}
		decSellingPrice = {}
		totalItemsSold = 0
		totalRevenue = 0
		profit = 0
		penalty = 0

		with open(config.monthWisePricelistFile) as mwplFile:

			mwplReader = csv.reader(mwplFile, delimiter = ',')
			next(mwplReader)

			for l in mwplReader:
				decSellingPrice[int(l[0])] = int(l[6])

		with open(config.decemberFileName) as decemberFile:

			decReader = csv.reader(decemberFile)
			
			ignoreHead = True

			for line in decReader:

				if ignoreHead:
					ignoreHead = False
				else:

					# print line
					itemID = int(line[2])
					hour = int(((((line[5].split())[1]).split(':'))[0]))
					if hour==0: hour = 24
					if hour==1: hour = 25
					if hour==2: hour = 26
					seg = line[4][0:2]
					# print hour
					qty = int(line[3])

					totalRevenue += decSellingPrice[itemID] * qty

					# print itemID, qty

					if itemID in decemberData.keys():
						if seg in decemberData[itemID].keys():
							if hour in decemberData[itemID][seg].keys():
								decemberData[ itemID ][ seg ][hour] += qty
							else:
								decemberData[ itemID ][ seg ][hour] = qty
						else:
							decemberData[ itemID ][ seg ] = {}
							decemberData[ itemID ][ seg ][hour] = qty
					else:
						decemberData[itemID] = {}
						decemberData[itemID][seg] = {}
						decemberData[ itemID ][ seg ][hour] = qty

		newPrices, hourCount = P1.readNewGeneratedPrices()
		
		for itemID in newPrices.keys():
			if itemID in decemberData.keys():

				for seg in newPrices[itemID]:
					if seg in decemberData[itemID].keys(): # removes the 'price' segment
				
						num_hours = 0
						change_in_price = 0
						
						for hour in newPrices[itemID][seg]:
							if hour in decemberData[itemID][seg].keys():
								
								priceDiff = (newPrices[itemID][seg][hour] - newPrices[itemID]['price'])
								
								if priceDiff > 0:
									change_in_price = priceDiff
									num_hours += 1
									
								profit += change_in_price * decemberData[itemID][seg][hour]

						penalty += change_in_price * P1.getHourWeight(num_hours) * P1.getSegmentWeight(seg)

		profitPercent = float(float(profit) / totalRevenue) * 100
		ppRatio = float(profit)/float(penalty) # measure of how well the profit measures against the penalty

		print 'minsup: ', minsup
		print 'minconf: ', minconf
		print 'profit: ', 'profit: ' + str(profitPercent) + "% ( Rs. " + str(profit) + " )"
		print 'penalty: ', penalty
		print 'ppRatio: ', ppRatio
		print '----'
		stdout.flush()

		with open(config.resultsFileName, 'a') as resFile:
			resFile.write('minsup: ' + str(minsup) + "\n")
			resFile.write('minconf: ' + str(minconf) + "\n")
			resFile.write('profit: ' + str(profitPercent) + "% ( Rs. " + str(profit) + " )" + "\n")
			resFile.write('penalty: ' + str(penalty) + "\n")
			resFile.write('profit/penalty: ' + str(ppRatio) + "\n\n")


# ----------------------------------------------------------------------------------------------------------------------------------------

# TESTCASES: To test out various combinations of minsup and minconf, find associations 
# and derive at what level the profit is above 5% and penalty is the lowest.
# Each test case in testcaselist is a tuple denoting (minsup, minconf)

testcaselist = [(0.08,6), (0.09,6), (0.10,6), (0.11,6), (0.12,6), (0.13,6), (0.14,6), (0.15,6), (0.16,6),
				(0.08,5), (0.09,5), (0.10,5), (0.11,5), (0.12,5), (0.13,5), (0.14,5), (0.15,5), (0.16,5),
				(0.08,4), (0.09,4), (0.10,4), (0.11,4), (0.12,4), (0.13,4), (0.14,4), (0.15,4), (0.16,4),
				(0.08,3), (0.09,3), (0.10,3), (0.11,3), (0.12,3), (0.13,3), (0.14,3), (0.15,3), (0.16,3),
				(0.08,2), (0.09,2), (0.10,2), (0.11,2), (0.12,2), (0.13,2), (0.14,2), (0.15,2), (0.16,2),
				(0.08,1), (0.09,1), (0.10,1), (0.11,1), (0.12,1), (0.13,1), (0.14,1), (0.15,1), (0.16,1),
				(0.08,0), (0.09,0), (0.10,0), (0.11,0), (0.12,0), (0.13,0), (0.14,0), (0.15,0), (0.16,0)
				]

# Execute problem 1 for each testcase

for i in testcaselist:

	# Store the minsup and minconf values in a file so that other functions could read it whenever called
	with open(config.configFileName, "w+") as configFile:
		print "TESTCASE:", i
		configFile.writelines(str(i[0]) + "\n")
		configFile.writelines(str(i[1]) + "\n")
		configFile.close()

	# Modify the values of minsup and minconf for use in the rest of the program
	P1.initialize()
	
	# Automatically generate best association rules of the form <seg>, <hour> --> <itemID>
	P1.runAutoGenOnFiles(config.monthWisePricelistFile, config.monthFileNameList, config.pricingFileName)
	#time.sleep(0.5) # delay to let disk IO complete

	# Read the newly generated pricing file (containing association rules) and 
	# automatically generate the newPrices.csv file by using the information from
	# the pricing file
	P1.generateNewPriceCSVFromPricingFile(config.pricingFileName)
	#time.sleep(0.5) # delay to let disk IO complete
	
	# Calculate the profit and penalty by using the new prices in the newPrices.csv file
	P1.calculateProfitAndPenalty()

	# Remove the files created (we need new files for the next test case)
	os.remove(config.pricingFileName)
	os.remove(config.newPriceFileName)
	
	#time.sleep(3) # delay to let disk IO complete