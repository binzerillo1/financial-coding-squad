# Indicator Calculator
# Brian Inzerillo 3.25.2020
# Input a stock ticker, and output certain indicators

import yfinance as yf
import numpy as np
import datetime as dt
import pandas as pd

stock_name = input("Enter Stock Ticker: ")

now = dt.datetime.now()
while (stock_name != 'quit'):
    data = yf.download(stock_name, '2019-01-01', now)
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

    #print (d4_stoch)

    d4_stoch_arr = pd.Series(d4_stoch)

    k4_stoch = []

    j = 0
    while (j < 6):
        temp = round(sum(d4_stoch_arr[j:j+4])/4,2)
        k4_stoch = k4_stoch + [temp]
        j = j + 1

    #print (k4_stoch)

    k4_stoch_arr = pd.Series(k4_stoch)
    day = 1
    stoch_xover = False

    while ( stoch_xover == False and day < 6 ):
        if ( d4_stoch_arr[day-1] > k4_stoch_arr[day-1] and d4_stoch_arr[day] < k4_stoch_arr[day] ):
            stoch_xover = True
            print ("Stochastic Crossover " + str(day) + " day(s) ago.")
            stoch_xover == True
        else:
            day = day + 1
            
    if (stoch_xover == False): print("No Stochastic Crossover recently")
    stock_name = input("Next stock: ")