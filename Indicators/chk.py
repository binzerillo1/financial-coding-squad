# Stage 2 Confirmation Script
# Brian Inzerillo 11.1.2019

import yfinance as yf
import numpy as np
import datetime as dt
import pandas as pd
from array import *

stock_name = input("Enter any stock: ")

while (stock_name != 'quit'):
    # importing stock data as a Pandas Series
    print("")
    start_date = input("Enter date of pull in YYYY-MM-DD format:")
    print("Grabbing Stocks...")
    now = dt.datetime.now()
    data = yf.download(stock_name, '2017-01-01', start_date)
    print("")

    # computing the various criteria values
    current = float(data.Close[-1:])
    moving_avg_15 = sum(data.Close[-15:])/15
    moving_avg_20 = sum(data.Close[-20:])/20
    moving_avg_30 = sum(data.Close[-30:])/30
    moving_avg_50 = sum(data.Close[-50:])/50
    moving_avg_150 = sum(data.Close[-150:])/150
    moving_avg_200 = sum(data.Close[-200:])/200

    # computing percent values
    low_of_52wk = float(min(data.Close[-250:]))
    percent_above_52wk_low = (current - low_of_52wk)/low_of_52wk*100
    high_of_52wk = float(max(data.Close[-250:]))
    percent_below_52wk_high = (current - high_of_52wk)/high_of_52wk*100

    # computing trends
    i = 1
    tim = [0]
    moving_avg_200_trend = [moving_avg_200]*60
    while (i < 60):
        # time portion
        tim.append(i)
        i = i + 1
        # 200-day moving avg
        moving_avg_200_trend[60-i] = sum(data.Close[(-200-i):-i])/200
    m_200,b_200 = np.polyfit(tim, moving_avg_200_trend, 1)

    # calculate the exponential moving averages for full dataset
    red_ema = []
    blue_ema = []
    red_ema_ranges = [3, 5, 8, 10, 12, 15]
    blue_ema_ranges = [30, 35, 40, 45, 50, 60]

    # array format: array[date index][ema index]
    for i in red_ema_ranges:
        ema_temp = data.Close.ewm(span=i, adjust=False).mean()
        red_ema.append(ema_temp.to_numpy())

    for i in blue_ema_ranges:
        ema_temp = data.Close.ewm(span=i, adjust=False).mean()
        blue_ema.append(ema_temp.to_numpy())
    
    j = len(ema_temp) - 1
    
    # determine RWB
    red_min = min(red_ema[0][j], red_ema[1][j], 
                  red_ema[2][j], red_ema[3][j], 
                  red_ema[4][j], red_ema[5][j],)
    red_max = max(red_ema[0][j], red_ema[1][j], 
                  red_ema[2][j], red_ema[3][j], 
                  red_ema[4][j], red_ema[5][j],)
    blue_min = min(blue_ema[0][j], blue_ema[1][j], 
                   blue_ema[2][j], blue_ema[3][j],
                   blue_ema[4][j], blue_ema[5][j],)
    blue_max = max(blue_ema[0][j], blue_ema[1][j], 
                   blue_ema[2][j], blue_ema[3][j],
                   blue_ema[4][j], blue_ema[5][j],)
    if(red_min > blue_max):
        RWB = True
    else:
        RWB = False 
    if(blue_min > red_max):
        BWR = True
    else:
        BWR = False 
    # Stochastic Calculations
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
    cur_d4 = temp
    #print (cur_d4)
    d4_stoch_arr = pd.Series(d4_stoch)
    #print(d4_stoch_arr)
    k4_stoch = []
    j = 0
    while (j < 6):
        temp = round(sum(d4_stoch_arr[j:j+4])/4,2)
        k4_stoch = k4_stoch + [temp]
        j = j + 1
    cur_d44 = temp
    #print (cur_d44)
    k4_stoch_arr = pd.Series(k4_stoch)
    
    # Bollinger Band Calculations
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
    
    cur_bb = float(bb_arr[-1:])
    last_bb = float(bb_arr[-2:-1])
    nex_bb = float(bb_arr[-3:-2])
    if ( cur_bb > last_bb or last_bb > nex_bb):
        bb_exp = True
    else:
        bb_exp = False
        
    # Bounces
    two_day_low = float(min(data.Low[-2:]))
    if(two_day_low < moving_avg_30 ):
        if(current > moving_avg_30 ):
            thirty_day_bounce = True
        else:
            thirty_day_bounce = False
    else:
        thirty_day_bounce = False    
        
    if(two_day_low < moving_avg_50):
        if(current > moving_avg_50):
            ten_wk_bounce = True
        else:
            ten_wk_bounce = False
    else:
        ten_wk_bounce = False
        
    if(two_day_low < moving_avg_150):
        if(current > moving_avg_150):
            thirty_wk_bounce = True
        else:
            thirty_wk_bounce = False
    else:
        thirty_wk_bounce = False
        
    if(two_day_low < (moving_avg_15 - 2*cur_bb)):
        lbbx = True
    else:
        lbbx = False
        
    # down bounces
    two_day_high = float(max(data.High[-2:]))
    if(two_day_high > moving_avg_30):
        if(current < moving_avg_30):
            thirty_day_bounce_down = True
        else:
            thirty_day_bounce_down = False
    else:
        thirty_day_bounce_down = False
        
    if(two_day_high > moving_avg_50):
        if(current < moving_avg_50):
            fifty_day_bounce_down = True
        else:
            fifty_day_bounce_down = False
    else:
        fifty_day_bounce_down = False
        
    if(two_day_high > moving_avg_150):
        if(current < moving_avg_150):
            thirty_week_bounce_down = True
        else:
            thirty_week_bounce_down = False
    else:
        thirty_week_bounce_down = False
        
    if(two_day_high > (moving_avg_15 + cur_bb)):
        ubbx = True
    else:
        ubbx = False
        
    # print each criteria
    # print("Max: $" + str(round(max, 2)))
    print("Stock: " + stock_name)
    print("")
    print("Basics")
    print("---------------------------------------------------")
    print("Current: $" + str(round(current, 2)))
    print("52 Week Low: $" + str(round(low_of_52wk, 2)))
    print("52 Week High: $" + str(round(high_of_52wk,2 )))
    print("Current Price / 52 week Low: " + str(round(current/low_of_52wk, 2)))
    print("Percent Below 52 Week High: " + str(round(percent_below_52wk_high,2)) + "%")
    
    print("")
    print("Evidence of Uptrend")
    print("---------------------------------------------------")
    
    if ( current > moving_avg_30):
        print("C > 30 day avg: YES")
    else:
        print("C > 30 day avg: NO")

    if ( current > moving_avg_50):
        print("C > 50 day avg: YES")
    else:
        print("C > 50 day avg: NO")
        
    if ( current > moving_avg_50):
        print("C > 10 wk avg: YES")
    else:
        print("C > 10 wk avg: NO")

    if ( current > moving_avg_150):
        print("C > 30 wk avg: YES")
    else:
        print("C > 30 wk avg: NO")
        
    if ( RWB == True):
        print("Daily RWB: YES")
    else:
        print("Daily RWB: NO")
        
    print("Above Last Green Line: IP")
    print("MACD histogram rising: IP")
    
    if( cur_d4 > cur_d44):
        print("Stoch D10.4 > Stoch D10.4.4: YES")
    else:
        print("Stoch D10.4 > Stoch D10.4.4: NO")
    
    if( bb_exp == True):
        print("BBD 15.2 upward expansion: YES")
    else:
        print("BBD 15.2 upward expansion: NO")
    
    print("RS SPY > 30-day avg RS: IP")
    print("RS SPY Rising: IP")

    if(max(data.High[-2:]) > round(high_of_52wk-.03,2)):
        print("52 wk high today/yesterday: YES")
    else:
        print("52 wk high today/yesterday: NO")
    
    if(current > 2*data.Close[-250]):
        print("C>2*C250: YES")
    else:
        print("C>2*250: NO")
    
    print("GLB within the wk on High Volume: IP")
    print("")    
    
    print("")
    print("Evidence of Uptrend - Overextended")
    print("---------------------------------------------------")
    
    if(thirty_day_bounce == True):
        print("Bounce 30 day or 50 day: YES")
    else:
        print("Bounce 30 day or 50 day: NO")
    
    if(ten_wk_bounce == True):
        print("Bounce 10 wk: YES")
    else:
        print("Bounce 10 wk: NO")
    
    if(thirty_wk_bounce == True):
        print("Bounce 30 wk: YES")
    else:
        print("Bounce 30 wk: NO")
        
    if(cur_d4 < 50):
        print("Stoch D10.4 < 50: YES")
    else:
        print("Stoch D10.4 < 50: NO")
        
    if( cur_d4 > cur_d44):
        print("Stoch D10.4 > Stoch D10.4.4: YES")
    else:
        print("Stoch D10.4 > Stoch D10.4.4: NO")    
        
    if( lbbx ):
        print("L1 or L1 < Lower BB D 15.2: YES")
    else:
        print("L1 or L1 < Lower BB D 15.2: NO")   
    
    print("")
    print("Evidence of Downtrend")
    print("---------------------------------------------------")
    
    if ( current < moving_avg_30):
        print("C < 30 day avg: YES")
    else:
        print("C < 30 day avg: NO")

    if ( current < moving_avg_50):
        print("C < 50 day avg: YES")
    else:
        print("C < 50 day avg: NO")
        
    if ( current < moving_avg_50):
        print("C < 10 wk avg: YES")
    else:
        print("C < 10 wk avg: NO")

    if ( current < moving_avg_150):
        print("C < 30 wk avg: YES")
    else:
        print("C < 30 wk avg: NO")
        
    if ( moving_avg_20 < moving_avg_50 and moving_avg_50 < moving_avg_150 ):
        print("4wk < 10wk < 30wk: YES")
    else:
        print("4wk < 10wk < 30wk: NO")
        
    if ( BWR == True):
        print("Daily BWR: YES")
    else:
        print("Daily BWR: NO")
        
    print("MACD histogram falling: IP")

    if ( cur_d4 < cur_d44 ):
        print("Stoch D10.4 < Stoch D10.4.4: YES")
    else: 
        print("Stoch D10.4 < Stoch D10.4.4: NO")
        
    print("Upper Bollinger Band downward expansion: IP")
    
    print("")
    print("Evidence of Downtrend - not extended")
    print("---------------------------------------------------")
    
    if(thirty_day_bounce_down == True):
        print("Bounce 30 day: YES")
    else:
        print("Bounce 30 day: NO")
    
    if(fifty_day_bounce_down == True):
        print("Bounce 10 wk: YES")
    else:
        print("Bounce 10 wk: NO")
    
    if(thirty_week_bounce_down == True):
        print("Bounce 30 wk: YES")
    else:
        print("Bounce 30 wk: NO")
        
    if(cur_d4 > 50):
        print("Stoch D10.4 > 50: YES")
    else:
        print("Stoch D10.4 > 50: NO")
    
    if( ubbx ):
        print("H1 or H1 < Upper BB D 15.2: YES")
    else:
        print("H1 or H1 < Upper BB D 15.2: NO")
    
    print("")
    stock_name = input("Enter any stock(quit to exit): ")