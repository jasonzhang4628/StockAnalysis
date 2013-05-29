# Pick stocks from 'companylist.csv' and return only the stocks that follow the SMA principle
# Note this program takes quite a bit of time to make calls to Yahoo Finance! API. You need Internet connection

import csv
from ysq import *
import re


#Modular conditionals using SMAs
def cond(price, fifty, twohundred):
    if fifty < twohundred and fifty > (0.9 * twohundred):
        if price < (fifty * 1.05) or price < (fifty * 0.95):
            return True

# Gather Stock tickers from csv file
tickerList = []
with open('companylist.csv') as f:
    reader = csv.reader(f, delimiter=' ')
    print reader
    for row in reader:
        gunk = row[0].split("/")
        foo = gunk[0].split()
        tickerList.append( foo[0])

tickerList = tickerList[1:]
newList = []

# Clean up the results
for ticker in tickerList:
    #print ticker
    if not ticker.isupper():
        tickerList.remove(ticker)
    if ticker.find('^') or ticker.find('$'):
        tickerList.remove(ticker)
    #if not re.match("[A-Za-z]*$", ticker):
     #   tickerList.remove(ticker)
    ticker = ''.join(c for c in ticker if c.isupper())
    newList.append(ticker)

print newList

# Write ALL information to a new cvs file
def writeToFile(lst):
    with open("tickersAndSMA.csv", "w") as csvfile:
        print "writing"
        mywriter = csv.writer(csvfile)
        mywriter.writerow(lst)
        #stockwriter = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        #stockwriter.writerow(lst)
        csvfile.close()


#Prune all stocks with a 50 SMA > 200 SMA
def SMAprune(ticker):
    print "Getting information for " + ticker
    try:
        price = get_price(ticker)
        fifty = get_50day_moving_avg(ticker)
        twohundred = get_200day_moving_avg(ticker)
        per =  get_price_earnings_ratio(ticker)
        #print [ticker, price, fifty, twohundred]
        if cond(price, fifty, twohundred):
            return [ticker]
    except Exception as e:
        print e

#Put the good stocks in a list
completeList = []
for stock in newList:
    print completeList
    info = SMAprune(stock)
    if info != None:
        completeList.append(info)
        #writeToFile(info)
