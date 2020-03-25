# Indicator Calculator
# Brian Inzerillo 3.25.2020
# Input a stock ticker, and output certain indicators

import yfinance as yf
import numpy as np
import datetime as dt
import pandas as pd

#stock_name = input("Enter Stock Ticker: ")
stock_name = 'aapl'

#now = dt.datetime.now()
#while (stock_name != 'quit'):
data = yf.download(stock_name, '2019-01-01', '2020-03-25')
stoch = []

x = -1
while (x > -20) :
    if ( x < -1):
        low_last_ten = float(min(data.Low[x-9:x+1]))
        # print(low_last_ten)
        high_last_ten = float(max(data.High[x-9:x+1]))
        # print(high_last_ten)
    else:
        low_last_ten = float(min(data.Low[x-9:]))
        # print(low_last_ten)
        high_last_ten = float(max(data.High[x-9:]))
        # print(high_last_ten)

    new = (float(data.Close[x]) - low_last_ten) / ( high_last_ten - low_last_ten )
    stoch = stoch + [new]
    x = x - 1
    
stoch_arr = pd.Series(stoch)
# print (stoch)

d4_stoch = []

i = 0
while (i < 10):
    temp = round(sum(stoch_arr[i:i+4])/4*100,2)
    d4_stoch = d4_stoch + [temp]
    i = i + 1

print (d4_stoch)

d4_stoch_arr = pd.Series(d4_stoch)

k4_stoch = []

j = 0
while (j < 6):
    temp = round(sum(d4_stoch_arr[j:j+4])/4,2)
    k4_stoch = k4_stoch + [temp]
    j = j + 1

print (k4_stoch)





