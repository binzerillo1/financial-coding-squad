#import relevant libraries
import yfinance as yf
import datetime as dt
import pandas as pd
from pandas_datareader import data as pdr
import matplotlib.pyplot as plt

yf.pdr_override() #activate yahoo finance workaround
start = dt.datetime(2020,3,1) #Sets start point of dataframe
now = dt.datetime.now() #Sets end point of dataframe

stock = input("Enter the stock symbol : ") #Asks for stock ticker

while stock != "quit": #Runs this loop until user enters 'quit' (can do many stocks in a row)

  df = pdr.get_data_yahoo(stock, start, now) #Fetches stock price data, saves as data frame

  df['High'].plot(label='close') #Plots high values of the stock

  pivots=[] #Stores pivot values
  dates=[]  #Stores Dates corresponding to those pivot values
  counter=0 #Will keep track of whether a certain value is a pivot
  lastPivot=0 #Will store the last Pivot value

  Range=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0] #Array used to iterate through stock prices
  dateRange=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0] #Array used to iterate through corresponding dates
  for i in df.index: #Iterates through the price history
    currentMax=max(Range, default=0) #Determines the maximum value of the 10 item array, identifying a potential pivot
    value=round(df["High"][i],2) #Receives next high value from the dataframe

    Range=Range[1:9] # Cuts Range array to only the most recent 9 values
    Range.append(value) #Adds newest high value to the array
    dateRange=dateRange[1:9]  #Cuts Date array to only the most recent 9 values
    dateRange.append(i) #Adds newest date to the array

    if currentMax == max(Range, default=0): #If statement that checks is the max stays the same
      counter+=1 #if yes add 1 to counter
    else:
      counter=0 #Otherwise new potential pivot so reset the counter
    if counter==5: # checks if we have identified a pivot
      lastPivot=currentMax #assigns last pivot to the current max value
      dateloc=Range.index(lastPivot) #finds index of the Range array that is that pivot value
      lastDate=dateRange[dateloc] #Gets date corresponding to that index
      pivots.append(currentMax) #Adds pivot to pivot array
      dates.append(lastDate) #Adds pivot date to date array
  print()

  timeD=dt.timedelta(days=30) #Sets length of dotted line on chart

  for index in range(len(pivots)) : #Iterates through pivot array

    print(str(pivots[index])+": "+str(dates[index])) #Prints Pivot, Date couple

    plt.plot_date([dates[index]-(timeD*.075), dates[index]+timeD], #Plots horizontal line at pivot value
                [pivots[index], pivots[index]], linestyle=":", linewidth=2, marker=',')
  plt.show() #Shows matplotlib plot
  print()
  stock = input("Enter the stock symbol : ") #Asks for new pivot
