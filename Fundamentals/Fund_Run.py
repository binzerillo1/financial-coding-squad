# Fundamental Sorting List
# Brian Inzerillo 11.1.2019
# Reads the fundamental stock data and rate them based on 
# good fundamental values
# also determines whether the stock is in an uptrend or not

# imports

import yfinance as yf
import numpy as np
import xlrd
import datetime as dt

# uptrend function
def uptrend_conf(stock_name, RSI):
    now = dt.datetime.now()
    data = yf.download(stock_name, '2017-01-01', now)
    max_val = max(data.Close)
    current = float(data.Close[-1:])
    moving_avg_50 = sum(data.Close[-50:])/50
    moving_avg_150 = sum(data.Close[-150:])/150
    moving_avg_200 = sum(data.Close[-200:])/200
    low_of_52wk = float(min(data.Close[-260:]))
    percent_above_52wk_low = (current - low_of_52wk)/low_of_52wk*100
    high_of_52wk = float(max(data.Close[-260:]))
    percent_below_52wk_high = (current - high_of_52wk)/high_of_52wk*100
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
    if (current > moving_avg_150 and current > moving_avg_200):
        crit_1 = True
    else :
        crit_1 = False
    if (moving_avg_150 > moving_avg_200):
        crit_2 = True
    else :
        crit_2 = False
    if (m_200 > 0):
        crit_3 = True
    else :
        crit_3 = False
    if (moving_avg_50 > moving_avg_150 and moving_avg_50 > moving_avg_200):
        crit_4 = True
    else :
        crit_4 = False
    if (percent_above_52wk_low > 25):
        crit_5 = True
    else :
        crit_5 = False
    if (abs(percent_below_52wk_high) < 25):
        crit_6 = True
    else :
        crit_6 = False
    if (RSI > 70):
        crit_7 = True
    else :
        crit_7 = False
    if (current > moving_avg_50):
        crit_8 = True
    else :
        crit_8 = False
    if (crit_1 == True and crit_2 == True and crit_3 == True and crit_4 == True and crit_5 == True and crit_6 == True and crit_7 == True and crit_8 == True):
        uptrend = True
    else:
        uptrend = False
    uptrend_result = [uptrend, crit_1, crit_2, crit_3, crit_4, crit_5, crit_6, crit_7, crit_8]
    return uptrend_result

# excel stock name retreival
# UPDATE THIS TO THE EXCEL SHEET WITH SYMBOLS YOU WANT TO SEARCH
loc = 'C:/Users/brian/Desktop/USB/Finance/Richard Fundamentals_1_18_20.xlsx'
wb = xlrd.open_workbook(loc)
sheet = wb.sheet_by_index(0) 
sheet.cell_value(0, 0)  
stock_list = []
num = 0
lower = 121
upper = 160

# begin to anaylze stocks
for j in range(lower,upper):
    stock = {
        'SYMBOL':sheet.cell_value(j, 9),
        'RS':sheet.cell_value(j, 13),
        'EPS':sheet.cell_value(j, 18),
        'EPS_1Q':sheet.cell_value(j,19),
        'EPS_2Q':sheet.cell_value(j, 20),
        'EPS_FQ':sheet.cell_value(j,25),
        'SALES':sheet.cell_value(j, 34),
        'SALES_YR':sheet.cell_value(j, 35),
        'SALES_2Q':sheet.cell_value(j, 39),
        'ROE':sheet.cell_value(j, 52),
        'Ind. Rank':sheet.cell_value(j, 40),
    }
    message = "Stock " + str(j) + " of " + str(upper) + ":"
    
    print(message)
    
    uptrend_res = uptrend_conf(stock["SYMBOL"], stock["RS"])
    
    if (uptrend_res[0] == True):
        stock["UPTRD"] = " YES "
    else :
        stock["UPTRD"] = "  NO "
        
    if (stock["RS"] > 70):
        stock_list.append(stock)
        num =  num + 1;
        
print()

print("| SYM  | SCORE | RS | EPSFQ |  EPS |  E1Q |  E2Q |  SALES | SALES_2Q | SALES_YR |  ROE | UPTRD ")

for j in range(0,num):
    s = stock_list[j] 
    
    s["SCORE"] = 0    
    
    delta_0 = s["EPS_FQ"] - s["EPS"]
    delta_1 = s["EPS"] - s["EPS_1Q"]
    delta_2 = s["EPS_1Q"] - s["EPS_2Q"]

    if( delta_0 > 0 ):
        s["SCORE"] += 2
        if( delta_0 > 25 ):
            s["SCORE"] += 2
            if( delta_0 > 100):
                s["SCORE"] += 4
    
    if( delta_1 > 0 ):
        s["SCORE"] += 1
        if( delta_1 > 25 ):
            s["SCORE"] += 1
            if( delta_1 > 100):
                s["SCORE"] += 2
                
    if( delta_2 > 0 ):
        s["SCORE"] += 1
        if( delta_2 > 25 ):
            s["SCORE"] += 1
            if( delta_2 > 100):
                s["SCORE"] += 2
    
    if( s["EPS"] > 20):
        s["SCORE"] += 2
        if( s["EPS"] > 40):
            s["SCORE"] += 1
            if( s["EPS"] > 60):
                s["SCORE"] += 1
                if( s["EPS"] > 80):
                    s["SCORE"] += 2
                    if( s["EPS"] > 100):
                        s["SCORE"] += 2
                        
    if( s["EPS_FQ"] > 20):
        s["SCORE"] += 2
        if( s["EPS_FQ"] > 40):
            s["SCORE"] += 1
            if( s["EPS_FQ"] > 60):
                s["SCORE"] += 1
                if( s["EPS_FQ"] > 80):
                    s["SCORE"] += 2
                    if( s["EPS_FQ"] > 100):
                        s["SCORE"] += 2
                        
    if( s["EPS_1Q"] > 20):
        s["SCORE"] += 1
        if( s["EPS_1Q"] > 40):
            s["SCORE"] += 1
            if( s["EPS_1Q"] > 80):
                s["SCORE"] += 2
                if( s["EPS_1Q"] > 100):
                    s["SCORE"] += 2
                        
    if( s["EPS_2Q"] > 20):
        s["SCORE"] += 1
        if( s["EPS_2Q"] > 40):
            s["SCORE"] += 1
            if( s["EPS_2Q"] > 80):
                s["SCORE"] += 1
                if( s["EPS_2Q"] > 100):
                    s["SCORE"] += 1
                    
    if( s["RS"] > 70):
        s["SCORE"] += 2
        if( s["RS"] > 75):
            s["SCORE"] += 1
            if( s["RS"] > 80):
                s["SCORE"] += 2
                if( s["RS"] > 85):
                    s["SCORE"] += 1
                    if( s["RS"] > 90):
                        s["SCORE"] += 1
                        if( s["RS"] > 95):
                            s["SCORE"] += 2
                            if( s["RS"] > 98):
                                s["SCORE"] += 1
    if( s["SALES"] > 20):
        s["SCORE"] += 2
        if( s["SALES"] > 50):
            s["SCORE"] += 2
            if( s["SALES"] > 100):
                s["SCORE"] += 3
    
    if( s["SALES_2Q"] > 20):
        s["SCORE"] += 2
        if( s["SALES_2Q"] > 50):
            s["SCORE"] += 2
            if( s["SALES_2Q"] > 100):
                s["SCORE"] += 3
                   
    if( s["SALES_YR"] > 20):
        s["SCORE"] += 2
        if( s["SALES_YR"] > 50):
            s["SCORE"] += 2
            if( s["SALES_YR"] > 100):
                s["SCORE"] += 2
                
    if( s["ROE"] > 20):
        s["SCORE"] += 2
        if( s["ROE"] > 25):
            s["SCORE"] += 1
            if( s["ROE"] > 30):
                s["SCORE"] += 1
                if( s["ROE"] > 35):
                    s["SCORE"] += 1
                    if( s["ROE"] > 40):
                        s["SCORE"] += 1
                        if( s["ROE"] > 60):
                            s["SCORE"] += 2
                            if( s["ROE"] > 100):
                                s["SCORE"] += 2

    s["EPS"] = str(int(s["EPS"]))
    s["EPS_FQ"] = str(int(s["EPS_FQ"]))
    s["EPS_1Q"] = str(int(s["EPS_1Q"]))
    s["EPS_2Q"] = str(int(s["EPS_2Q"]))
    s["SALES"] = str(int(s["SALES"]))
    s["SALES_YR"] = str(int(s["SALES_YR"]))
    s["SALES_2Q"] = str(int(s["SALES_2Q"]))
    s["ROE"] = str(int(s["ROE"]))
    s["Ind. Rank"] = str(int(s["Ind. Rank"]))
    s["SCORE"] = str(int(s["SCORE"]))
    
    while( len(s["SYMBOL"]) < 4):
        s["SYMBOL"] = s["SYMBOL"] + " "
    while( len(s["EPS"]) < 4):
        s["EPS"] = " " + s["EPS"] 
    while( len(s["EPS_FQ"]) < 5):
        s["EPS_FQ"] = " " + s["EPS_FQ"]
    while( len(s["EPS_1Q"]) < 4):
        s["EPS_1Q"] = " " + s["EPS_1Q"]
    while( len(s["EPS_2Q"]) < 4):
        s["EPS_2Q"] = " " + s["EPS_2Q"]
    while( len(s["SALES"]) < 6):
        s["SALES"] = " " + s["SALES"]
    while( len(s["SALES_YR"]) < 8):
        s["SALES_YR"] = " " + s["SALES_YR"]
    while( len(s["SALES_2Q"]) < 8):
        s["SALES_2Q"] = " " + s["SALES_2Q"]
    while( len(s["ROE"]) < 4):
        s["ROE"] = " " + s["ROE"]
    while( len(s["Ind. Rank"]) < 9):
        s["Ind. Rank"] = " " + s["Ind. Rank"]   
    while( len(s["SCORE"]) < 5):
        s["SCORE"] = " " + s["SCORE"]
    
    mess = "| " + s["SYMBOL"] + " | " + s["SCORE"] + " | " + str(int(s["RS"])) + " |"
    mess = mess + " " + s["EPS_FQ"] + " | " + s["EPS"] + " | " + s["EPS_1Q"] + " | " + s["EPS_2Q"] + " | "
    mess = mess + s["SALES"] + " | " + s["SALES_2Q"] + " | " + s["SALES_YR"] + " | " + s["ROE"] + " | "
    mess = mess + s["UPTRD"] 
    print (mess)
    #print(" ----------------------------------------------------------------")