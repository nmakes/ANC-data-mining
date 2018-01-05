# Different representations of time slots. slots3 is used. The others are discarded
slots = { "16":1, "17":2, "18":3, "19":4, "20":5, "21":6, "22":7, "23":8, "0":9, "00":9, "1":10, "01":10, "2":11, "02":11}
slots2 = { "16":"4:30 PM", "17":"5:30 PM", "18":"6:30 PM", "19":"7:30 PM", "20":"8:30 PM", "21":"9:30 PM", "22":"10:30 PM", "23":"11:30 PM", "00":"12:30 AM", "01":"1:30 AM", "02":"2:30 AM"}
slots3 = { "16":"4-5 PM", "17":"5-6 PM", "18":"6-7 PM", "19":"7-8 PM", "20":"8-9 PM", "21":"9-10 PM", "22":"10-11 PM", "23":"11-12 AM", "00":"12-1 AM", "24":"12-1 AM", "01":"1-2 AM", "25":"1-2 AM", "02":"2-3 AM", "26":"2-3 AM"}

INF = 100
ZERO = 0

minsup = 0.09
minconf = 3
maxsup = INF
maxconf = INF

def updateMinSup(newVal):
	global minsup
	minsup = newVal

def updateMinConf(newVal):
	global minconf
	minconf = newVal

param_X = 0.05 # 5%

param_Y = 0.20 # 20%
param_M = 10
param_Z = 0.08 # 8%

monthFileNameList = ['./Dataset/augSales.csv','./Dataset/sepSales.csv','./Dataset/octSales.csv','./Dataset/novSales.csv']
monthWisePricelistFile = "./Dataset/monthwisePriceList.csv"
origNewPriceFileName = "./Dataset/origNewPrices.csv"
newPriceFileName = "./newPrices.csv"
decemberFileName = "./Dataset/decSales.csv"
pricingFileName = './frequent.csv'

resultsFileName = "./results.txt"
configFileName = "./configFile.txt"