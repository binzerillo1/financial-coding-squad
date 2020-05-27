# Watchlist Setups Analysis
# The purpose of this program to take the first 100 stocks from my 
# fundamentals ranking sheet and crank out some analysis for them
# I want it to indicate setups and technical features of the stock
# Brian Inzerillo 5.21.2020

import yfinance as yf
import numpy as np
import datetime as dt
import pandas as pd
import os

# ----------------------------------------------------------------
# Crank Function - takes a stock name as input and returns an 
# list of all the desired technical quanitities
# output list format:
# green_dot, green_dot_days, boll_band_sq, boll_band_sq_days,
# boll_band_dip, green_line_price,
# green_line_prox, green_line_prox_perc, daily_rwb, stochastic,
# stoch_under, stage_two, dist_days, dist_days_limit, below_green
# NOTE: if a number is undefined, it will be given as 6969
def Crank(stck):
    
    start = dt.datetime(2019, 6, 1)
    now = dt.datetime.now()
    data = yf.download(stck, start, now)
    
    current = float(data.Close[-1:])
    moving_avg_15 = sum(data.Close[-15:])/15
    moving_avg_20 = sum(data.Close[-20:])/20
    moving_avg_30 = sum(data.Close[-30:])/30
    moving_avg_50 = sum(data.Close[-50:])/50
    moving_avg_150 = sum(data.Close[-150:])/150
    moving_avg_200 = sum(data.Close[-200:])/200
    
    low_of_52wk = float(min(data.Close[-250:]))
    percent_above_52wk_low = (current - low_of_52wk)/low_of_52wk*100
    high_of_52wk = float(max(data.Close[-250:]))
    percent_below_52wk_high = (current - high_of_52wk)/high_of_52wk*100

    # determine RWB
    # calculate the exponential moving averages
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
    
    red_min =  min(red_ema[0][j], red_ema[1][j], 
                   red_ema[2][j], red_ema[3][j], 
                   red_ema[4][j], red_ema[5][j],)
    red_max =  max(red_ema[0][j], red_ema[1][j], 
                   red_ema[2][j], red_ema[3][j], 
                   red_ema[4][j], red_ema[5][j],)
    blue_min = min(blue_ema[0][j], blue_ema[1][j], 
                   blue_ema[2][j], blue_ema[3][j],
                   blue_ema[4][j], blue_ema[5][j],)
    blue_max = max(blue_ema[0][j], blue_ema[1][j], 
                   blue_ema[2][j], blue_ema[3][j],
                   blue_ema[4][j], blue_ema[5][j],)
    if(red_min > blue_max):
        daily_rwb = True
    else:
        daily_rwb = False
    
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
    
    stoch = []
    x = -1
    while (x > -20) :
        if ( x < -1):
            low_last_ten = float(min(data.Low[x-9:x+1]))
            high_last_ten = float(max(data.High[x-9:x+1]))
        else:
            low_last_ten = float(min(data.Low[x-9:]))
            high_last_ten = float(max(data.High[x-9:]))
            
        new = (float(data.Close[x]) - low_last_ten) / ( high_last_ten - low_last_ten )
        stoch = stoch + [new]
        x = x - 1
        
    stoch_arr = pd.Series(stoch)
    
    d4_stoch = []
    i = 0
    while (i < 10):
        temp = round(sum(stoch_arr[i:i+4])/4*100,2)
        d4_stoch = d4_stoch + [temp]
        i = i + 1
    cur_d4 = temp
    #print (cur_d4)
    d4_stoch_arr = pd.Series(d4_stoch)
    # print(d4_stoch_arr)
    k4_stoch = []
    j = 0
    while (j < 6):
        temp = round(sum(d4_stoch_arr[j:j+4])/4,2)
        k4_stoch = k4_stoch + [temp]
        j = j + 1
    cur_d44 = temp
    #print (cur_d44)
    k4_stoch_arr = pd.Series(k4_stoch)
    stochastic = d4_stoch_arr[0]
    
    sxday = 1
    stoch_xover = False

    while ( stoch_xover == False and sxday < 6 ):
        if ( d4_stoch_arr[sxday-1] > k4_stoch_arr[sxday-1] and d4_stoch_arr[sxday] < k4_stoch_arr[sxday] and d4_stoch_arr[sxday] < 70):
            stoch_xover = True
        else:
            sxday = sxday + 1
            
    if (stoch_xover == False): 
        green_dot = False
        green_dot_days = 6969
    else: 
        green_dot = True
        green_dot_days = sxday
    
    if(stochastic < 80): stoch_under = True
    else: stoch_under = False
    
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
         
    boll_band_sq_days = 0
    
    for g in range(0, 5):
        if( (bb_arr[15-g] - bb_arr[14-g]) < 0):
            boll_band_sq_days += 1
    
    if (boll_band_sq_days > 4):
        boll_band_sq = True
    else:
        boll_band_sq = False
        boll_band_sq_days = 6969
        
    if (data.Low[-1] < moving_avg_15 - bb_arr[len(bb)-1]):
        boll_band_dip = True
    else:
        boll_band_dip = False
    
    
    numbers = [green_dot, green_dot_days,boll_band_sq,boll_band_sq_days, boll_band_dip, 'IP', 'IP', 'IP', daily_rwb, stochastic, stoch_under, 'IP', 'IP', 'IP','IP']
    return numbers
# ----------------------------------------------------------------


# checks to see if dataset is already present, deletes if so
if(os.path.isfile("dataset.txt")):
    os.remove("dataset.txt")

# here is where I store my top 100,  file should be updated wkly
file = open('fundamental_100.txt', 'r')
input = file.readlines()
file.close()

# pull stock names
stock_name = []
for i in range(0, len(input)):
    stock_name.append(str(input[i]).rstrip())  
    
nums = []
file = open("dataset.txt", 'w')

# run through each stock and store technicals
for j in range(0, len(stock_name)):
    nums = Crank(stock_name[j])
    
    line = stock_name[j] + " "
    for k in range(0, len(nums) - 1):
        line += str(nums[k]) + " "
    line += str(nums[14]) + "\n"
    
    file.write(line)
    
    line = ""
    nums.clear()
file.close()