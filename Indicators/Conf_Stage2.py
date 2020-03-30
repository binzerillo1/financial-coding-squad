# Stage 2 Confirmation Script
# Brian Inzerillo 11.1.2019

import yfinance as yf
import numpy as np
import datetime as dt

stock_name = input("Enter any stock: ")

while (stock_name != 'quit'):
    # importing stock data as a Pandas Series
    print("")
    print("Grabbing Stocks...")
    now = dt.datetime.now()
    data = yf.download(stock_name, '2017-01-01', now)
    print("")

    # computing the various criteria values
    max_val = max(data.Close)
    current = float(data.Close[-1:])
    moving_avg_50 = sum(data.Close[-50:])/50
    moving_avg_150 = sum(data.Close[-150:])/150
    moving_avg_200 = sum(data.Close[-200:])/200

    # computing percent values
    low_of_52wk = float(min(data.Close[-260:]))
    percent_above_52wk_low = (current - low_of_52wk)/low_of_52wk*100
    high_of_52wk = float(max(data.Close[-260:]))
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

    print("Moving Strength: " + str(round((m_200),4)))

    # computing relative strength
    diff = []
    gains = []
    losses = []
    for j in range(2, 17):
        diff.append(data.Close[-1*(j-1)] - data.Close[-j])
        if (diff[j-2] > 0):
            gains.append(diff[j-2])
        else :
            losses.append(diff[j-2])    
    avg_gains_per_day = sum(gains)/15
    avg_losses_per_day = sum(losses)/15
    RS = avg_gains_per_day/abs(avg_losses_per_day)
    RSI = 100 - 100*(1/(1+RS))

    # print each criteria
    # print("Max: $" + str(round(max, 2)))
    print("Stock: " + stock_name)
    print("")
    print("Current: $" + str(round(current, 2)))
    print("")
    print("50-day Moving Average: $" + str(round(moving_avg_50, 2)))
    print("150-day Moving Average: $" + str(round(moving_avg_150, 2)))
    print("200-day Moving Average: $" + str(round(moving_avg_200, 2)))
    print("")
    print("52 Week Low: $" + str(round(low_of_52wk, 2)))
    print("52 Week High: $" + str(round(high_of_52wk, 2)))
    print("Percent Above 52 Week Low: " + str(round(percent_above_52wk_low,2)) + "%")
    print("Percent Below 52 Week High: " + str(round(percent_below_52wk_high,2)) + "%")
    print("")
    print("RSI: " + str(round(RSI,0)))
    print("")


    # Criteria for Stage 2

    # 1. Stock price is above both 150-day and 200-day moving average
    if (current > moving_avg_150 and current > moving_avg_200):
        print("Criteria 1 Met!")
        crit_1 = True
    else :
        print("Criteria 1 NOT Met :")
        print("Stock price is not above both 150-day and 200-day moving averages")
        crit_1 = False

    # 2. 150-day Moving Average is above 200-day Moving Average
    if (moving_avg_150 > moving_avg_200):
        print("Criteria 2 Met!")
        crit_2 = True
    else :
        print("Criteria 2 NOT Met :")
        print("150-day is not above 200-day moving average")
        crit_2 = False
        
    # 3. The 200-day moving avg is trending up for at least 1-month, if not 4-5
    # Note: I'm going to stick with 3 months for now, but this is scorable
    if (m_200 > 0):
        print("Criteria 3 Met!")
        crit_3 = True
    else :
        print("Criteria 3 NOT Met :")
        print("200-day moving average is not trending up")
        crit_3 = False

    # 4. The 50-day moving avg is above 150-day and 200-day moving avg
    if (moving_avg_50 > moving_avg_150 and moving_avg_50 > moving_avg_200):
        print("Criteria 4 Met!")
        crit_4 = True
    else :
        print("Criteria 4 NOT Met :")
        print("50-day moving avg is not above 150-day and 200-day moving averages")
        crit_4 = False
        
    # 5. The current stock price is up at least 25% above 52-week low_of_52wk
    # Note: best stocks tend be around 100-300% or more between large advances
    if (percent_above_52wk_low > 25):
        print("Criteria 5 Met!")
        crit_5 = True
    else :
        print("Criteria 5 NOT Met :")
        print("Stock price is less than 25% above 52-week low") 
        crit_5 = False
        
    # 6. The current stock price is within 25% of its 52-week high_of_52wk
    # Note: Lower percentage is better
    if (abs(percent_below_52wk_high) < 25):
        print("Criteria 6 Met!")
        crit_6 = True
    else :
        print("Criteria 6 NOT Met :")
        print("Stock price is not within 25% of its 52-week high")
        crit_6 = False
        
    # 7. The relative strength (RS) is no less than 70, but preferably above 90
    # Note: Later, I'd like to add some sort of trend detection for RS
    # if (RSI > 70):
    #     print("Criteria 7 Met!")
    #     crit_7 = True
    # else :
    #     print("Criteria 7 NOT Met :")
    #     print("Stock's RSI is not above 70")
    #     crit_7 = False
    crit_7 = True
    # 8. Current Price is above the 50-day moving avg following a base
    # Note: I can't determine a base via coding (yet), so this would need confirmation
    if (current > moving_avg_50):
        print("Criteria 8 Met!")
        crit_8 = True
    else :
        print("Criteria 8 NOT Met :")
        print("Stock price is not above it's 50-day moving average")
        crit_8 = False
        
    print("")    
    if (crit_1 == True and crit_2 == True and crit_3 == True and crit_4 == True and crit_5 == True and crit_6 == True and crit_7 == True and crit_8 == True):
        print(stock_name + " is in a Stage 2 Trend.")
    else:
        print(stock_name + " is NOT in a Stage 2 Trend.")
    stock_name = input("Enter any stock: ")

    
    
    
    
    
    
    