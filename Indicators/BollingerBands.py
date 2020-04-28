# Bollinger Bands Calculator
# Brian Inzerillo 3.25.2020
# Input a stock ticker, and output certain indicators

import yfinance as yf
import numpy as np
import datetime as dt
import pandas as pd

stock_name = input("Enter Stock Ticker: ")

now = dt.datetime.now()

data = yf.download(stock_name, '2019-01-01', now)

prices =  data.Close[-30:]

period = 15
bb = []

i = 0

while(i < 16):
    price_period = prices[i:i+period]
    mean = price_period.mean()
    var = 0
    for j in range(0, 15):
        var = (price_period[j]-mean)*(price_period[j]-mean) + var
    std = np.sqrt(var/15)
    bb = bb + [round(2*std,2)]
    i = i + 1

bb_arr = pd.Series(bb)
print(bb_arr)

sum = 0
for j in range(0, len(bb)-1):
    sum = sum + bb_arr[j+1] - bb_arr[j]
slope = sum/(len(bb)-1)

print("Normalized Bollinger Band Slope: " + str(round(slope/float(bb_arr[-1:]),2)))
    