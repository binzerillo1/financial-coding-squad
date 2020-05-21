import yfinance as yf
import numpy as np
import datetime as dt
import pandas as pd

# pull data from the txt file

file = open('raw.txt', 'r')

input = file.readlines()

if ( len(input) % 6 == 0 ):

    stock_name = []
    buy_date = []
    buy_price = []
    stop_price = []
    number_shares = []
    earnings_date = []
    
    stocks_held = int(len(input)/6)

    for i in range(0, stocks_held):
    
       stock_name.append(str(input[0+(i*6)].rstrip()))
       buy_date.append(input[1+(i*6)].rstrip())
       buy_price.append(float(input[2+(i*6)].rstrip()))
       stop_price.append(float(input[3+(i*6)].rstrip()))
       number_shares.append(int(input[4+(i*6)].rstrip()))  
       earnings_date.append(input[5+(i*6)].rstrip())

else:
    print('raw.txt is formatted wrong.')
    
file.close()

# given this data, calculate the desired values

current_price = []
days_to_earnings = []
length_held = []
percent_change = []
profit = []

now = dt.datetime.now()

for j in range(0, stocks_held):
    
    b_date = buy_date[j]
    e_date = earnings_date[j]
    
    b_year = int(b_date[6:10])
    b_month = int(b_date[0:2])
    b_day = int(b_date[3:5])
    e_year = int(e_date[6:10])
    e_month = int(e_date[0:2])
    e_day = int(e_date[3:5])
    
    date_of_buy = dt.datetime(b_year, b_month, b_day)
    date_of_earnings = dt.datetime(e_year, e_month, e_day)
    
    diff = now - date_of_buy
    length_held.append(diff.days)
    
    diff = date_of_earnings - now
    days_to_earnings.append(diff.days)
    
    data = yf.download(stock_name[j], '2019-01-01', now)
    current_price.append(round(float(data.Close[-1]), 2))
    
    per = (current_price[j] - buy_price[j])/(buy_price[j])*100
    percent_change.append(round(per, 2))
    
    prof = (current_price[j] - buy_price[j])*number_shares[j]
    profit.append(round(prof, 2))
    
    

print(stock_name)
print(buy_date)
print(buy_price)
print(stop_price)
print(number_shares)
print(earnings_date)
print(current_price)
print(days_to_earnings)
print(length_held)
print(percent_change)
print(profit)