import csv 
from ysq import *
import re


#Get all of my stock tickers from csv
my_tickerList = []
with open('chosen_stocks.csv') as csvFile:
    reader = csv.reader(csvFile, delimiter=' ')
    for row in reader:
        first = row[0].split("/")
        second = first[0].split()
        my_tickerList.append(second[0])

print "My stocks listed below. Note that Yahoo Finance! lags on SMA prices"
print my_tickerList

#Get values

def display_info(lst):
    try:
        price = get_price(ticker)
        fifty = get_50day_moving_avg(ticker)
        twohundred = get_200day_moving_avg(ticker)
        #print [ticker, price, fifty, twohundred]
        if fifty > twohundred:
            print "Sell : " + ticker
            print [ticker, price, fifty, twohundred]
    except Exception as e:
        print e


for ticker in my_tickerList:
    display_info(ticker)
