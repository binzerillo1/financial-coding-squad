# Brian Inzerillo 2.14.2020
# Backtest program to test trading stratagies

# imports
import yfinance as yf
import numpy as np
import xlrd
import datetime as dt
import pandas as pd
from array import *
    
# define stock or etf to backtest
stock_name = 'TQQQ'
    
# define total range of data pull
start_date = '2011-01-01' # tqqq created in 2010
end_date = dt.datetime.now()

# download this data from yfinance
data = yf.download(stock_name, start_date, end_date)

# add a numerical index
# indices = np.array(range(0, len(data)))
# data["Indices"] = pd.Series(indices, index=data.index)

# add a small diff to help show a stronger rwb

gap = float(input("Gap: "))

# calculate the exponential moving averages for full dataset
red_ema = []
blue_ema = []
red_ema_ranges = [5, 5, 8, 10, 12, 15]
blue_ema_ranges = [30, 35, 40, 45, 50, 60]

# array format: array[date index][ema index]
for i in red_ema_ranges:
    ema_temp = data.Close.ewm(span=i, adjust=False).mean()
    red_ema.append(ema_temp.to_numpy())

for i in blue_ema_ranges:
    ema_temp = data.Close.ewm(span=i, adjust=False).mean()
    blue_ema.append(ema_temp.to_numpy())
 
# create Buy_Rating array and populate items
buy_rating = []
for j in range(0, len(data)):
    
    # determine RWB
    red_min = min(red_ema[0][j], red_ema[1][j], 
                  red_ema[2][j], red_ema[3][j], 
                  red_ema[4][j], red_ema[5][j],)
    blue_max = max(blue_ema[0][j], blue_ema[1][j], 
                   blue_ema[2][j], blue_ema[3][j],
                   blue_ema[4][j], blue_ema[5][j],)
    
    # check for RWB conditions
    if((red_min-gap) > blue_max):
        buy_rating.append(True)
    else:
        buy_rating.append(False)

# add buy rating to the dataFrame
buy_rating1 = np.array(buy_rating)
data["Buy_Rating"] = pd.Series(buy_rating1, index=data.index)

# define backtest time period
backtest_start = '2019-01-01'
backtest_end =  '2020-01-01' # dt.datetime.now()

# create a smaller dataset to work with
backtest_data = data[backtest_start:backtest_end]
# print(backtest_data)

# Assume uninvested to start
invested = False
gain_or_loss = 1
buy_price = 0
sell_price = 0
inactive_days = 0

# Find the results of the strategy by iterating through the time period
for j in range(0, len(backtest_data)):
    
    # if invested, check to sell
    if(invested):
        if(backtest_data.Buy_Rating[j]):
            # print("-")
            inactive_days += 1
        else:
            print("Sell on " + str(backtest_data.index[j]))
            invested = False
            sell_price = backtest_data.Close[j]
            percent_profit = round((sell_price - buy_price)/buy_price*100, 2)
            gain_or_loss = gain_or_loss * (percent_profit/100+1)
            print("Profit on Trade: " + str(percent_profit) + "%")
            print("Profit to Date: " + str(round((gain_or_loss - 1)*100, 2)) + "%")
   
    # if not invested, check to buy
    else:
        if(backtest_data.Buy_Rating[j]):
            print("Buy on " + str(backtest_data.index[j]))
            invested = True
            buy_price = backtest_data.Close[j]
        else:
            # print("-")
            inactive_days += 1
            
# check to see if still invested, divest if so
if(invested):
    sell_price = backtest_data.Close[j]
    percent_profit = round((sell_price - buy_price)/buy_price*100, 2)
    gain_or_loss = gain_or_loss * (percent_profit/100+1)
    print("Profit on Trade: " + str(percent_profit) + "%")
    inactive_days -= 2

print()
print("Overall Results")
print("---------------")
print("Profit to Date: " + str(round((gain_or_loss - 1)*100, 2)) + "%")
print("Number of Trades: " + str(int((j-inactive_days)/2)))
print("Total Days: " + str(j))
print("Performace over Test Period: " + str(round((backtest_data.Close[j] - backtest_data.Close[0])/backtest_data.Close[0]*100 , 2)) + "%")

print()
# print(red_ema[0])
# print(red_ema[1])
# print(red_ema[0][len(red_ema[0])-1])