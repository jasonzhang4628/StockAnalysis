from ysq import *

# For testing
sample_prices =  [450, 449, 448, 460, 452,444,450,452]

# Input
a = input("Please enter a stock ticker: ")
changes = []

#Get ticker's information
price, fifty, twohundred = get_info(a)

def get_info(ticker):
    return get_price(ticker), get_50day_moving_avg(ticker), get_200day_moving_avg(symbol)

for delta in changes:
    
    if delta < 0:
        print("Drop is " + str(abs(delta)))
	
    elif delta >= 0:
        print("Gain is " + str(delta))


def calc_gains(stockname, low = 0, high = 0):
    def update(stock):
        return get_price(stock)

    if high == 0:
        high = low

    buy_price = 0
    total_gains = 0
    open_price = update(stockname)
    price_low = open_price - low
    price_high = open_price + high
    while(True):
        live_price = update(stockname)
        if live_price < price_low:
            buy_price = live_price
        elif live_price > price_high:
            buy_price = live_price
        else:
            if buy_price == 0:
                print "Nothing bought yet"
            else:
                total_gains += live_price - buy_price
        print live_price
        print total_gains

calc_gains("AAPL", 0.1, 0.1)

