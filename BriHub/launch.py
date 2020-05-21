import tkinter as tk
import yfinance as yf
import numpy as np
import datetime as dt
import pandas as pd

# pull data from the txt file
# raw.txt is formatted as:
# STOCK TICKER
# BUY DATE MM/DD/YYYY
# BUY PRICE
# STOP PRICE
# NEXT EARNINGS DATE MM/DD/YYYY
# each stock is listed after another


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
stop_percent = []

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
    
    s_per = (stop_price[j] - buy_price[j])/(buy_price[j])*100
    stop_percent.append(round(s_per, 2))

# setup the GUI

root = tk.Tk()

# set window title
root.wm_title("Command Station")
root.geometry("800x600") # length by width

for k in range(0, stocks_held):
    
    # col 0
    tk.Label(root, text = stock_name[k], padx = 30).grid(row = k*4 + 1, column = 0)
    
    # col 1
    tk.Label(root, text = "Purchase Price:").grid(row = k*4, column = 1)
    tk.Label(root, text = "Shares Purchased:").grid(row = k*4+1, column = 1)
    tk.Label(root, text = "Purchase Date:").grid(row = k*4+2, column = 1)
    
    # col 2
    tk.Label(root, text = "$" + str(buy_price[k])).grid(row = k*4, column = 2)
    tk.Label(root, text = number_shares[k]).grid(row = k*4+1, column = 2)
    tk.Label(root, text = buy_date[k]).grid(row = k*4+2, column = 2)

    # col 3
    tk.Label(root, text = "Current Price:", padx = 10).grid(row = k*4, column = 3)
    tk.Label(root, text = "Total Gain/Loss:", padx = 10).grid(row = k*4+1, column = 3)
    tk.Label(root, text = "Length Held:", padx = 10).grid(row = k*4+2, column = 3)
    
    # col 4
    tk.Label(root, text = current_price[k]).grid(row = k*4, column = 4)
    tk.Label(root, text = "$" + str(profit[k])).grid(row = k*4+1, column = 4)
    tk.Label(root, text = str(length_held[k]) + " days").grid(row = k*4+2, column = 4)

    # col 5
    tk.Label(root, text = "Percent Change: " + str(percent_change[k]) + "%", padx = 20).grid(row = k*4+1, column = 5)

    # col 6
    tk.Label(root, text = "Stop Price:", padx = 10).grid(row = k*4, column = 6)
    tk.Label(root, text = "Stop Percent Change:", padx = 10).grid(row = k*4+1, column = 6)
    tk.Label(root, text = "Days Until Earnings:", padx = 10).grid(row = k*4+2, column = 6)
    
    # col 7
    tk.Label(root, text = "$" + str(stop_price[k])).grid(row = k*4, column = 7)
    tk.Label(root, text = str(stop_percent[k]) + "%").grid(row = k*4+1, column = 7)
    tk.Label(root, text = str(days_to_earnings[k]) + " days").grid(row = k*4+2, column = 7)
    
    # in between entries, spacing row
    tk.Label(root, text="", pady = 10).grid(row = 4*k+3, column = 1)


# show window
root.mainloop()