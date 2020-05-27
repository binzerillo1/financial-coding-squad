#import relevant libraries
import yfinance as yf
import datetime as dt
import pandas as pd
from pandas_datareader import data as pdr
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
import datetime as datetime
import numpy as np
from mpl_finance import candlestick_ohlc

yf.pdr_override() #activate yahoo finance workaround

smasUsed=[10,30,50]

start =dt.datetime(2020,1,1)- dt.timedelta(days=max(smasUsed)) #Sets start point of dataframe
now = dt.datetime.now() #Sets end point of dataframe
stock = input("Enter the stock symbol : ") #Asks for stock ticker

while stock != "quit": #Runs this loop until user enters 'quit' (can do many stocks in a row)

  prices = pdr.get_data_yahoo(stock, start, now) #Fetches stock price data, saves as data frame

  fig, ax1 = plt.subplots()

  #Calculate moving averages

  for x in smasUsed: #This for loop calculates the EMAs for te stated periods and appends to dataframe
    sma=x
    prices['SMA_'+str(sma)] = prices.iloc[:,4].rolling(window=sma).mean()

  #calculate Bollinger Bands
  BBperiod=15
  stdev=2
  prices['SMA'+str(BBperiod)] = prices.iloc[:,4].rolling(window=BBperiod).mean() #calculates sma and creates a column in the dataframe
  prices['STDEV']=prices.iloc[:,4].rolling(window=BBperiod).std()
  prices['LowerBand']=prices['SMA'+str(BBperiod)]-(stdev*prices['STDEV'])
  prices['UpperBand']=prices['SMA'+str(BBperiod)]+(stdev*prices['STDEV'])
  prices["Date"]=mdates.date2num(prices.index)

  
 
  #Calculate 10.4.4 stochastic
  Period=10
  K=4
  D=4
  prices["RolHigh"] = prices["High"].rolling(window=Period).max() #calculates sma and creates a column in the dataframe
  prices["RolLow"] = prices["Low"].rolling(window=Period).min() #calculates sma and creates a column in the dataframe
  prices["stok"] = ((prices["Adj Close"]-prices["RolLow"])/(prices["RolHigh"]-prices["RolLow"]))*100
  prices["K"] = prices["stok"].rolling(window=K).mean()
  prices["D"] = prices["K"].rolling(window=D).mean() #calculates sma and creates a column in the dataframe
  prices["GD"]=prices["High"]
  ohlc = []

  #Delete extra dates
  prices=prices.iloc[max(smasUsed):]

  greenDotDate=[]
  greenDot=[]
  lastK=0
  lastD=0
  lastLow=0
  lastClose=0
  lastLowBB=0


  #Go through price history to create candlestics and GD+Blue dots
  for i in prices.index:
    #append OHLC prices to make the candlestick
    append_me = prices["Date"][i], prices["Open"][i], prices["High"][i], prices["Low"][i], prices["Adj Close"][i], prices["Volume"][i]
    ohlc.append(append_me)

    #Check for Green Dot
    if prices['K'][i]>prices['D'][i] and lastK<lastD and lastK <60:

      #plt.Circle((prices["Date"][i],prices["High"][i]),1) 
      #plt.bar(prices["Date"][i],1,1.1,bottom=prices["High"][i]*1.01,color='g')
      plt.plot(prices["Date"][i],prices["High"][i]+1, marker="o", ms=4, ls="", color='g')

      greenDotDate.append(i)
      greenDot.append(prices["High"][i])  

    #Check for Lower Bollinger Band Bounce
    if ((lastLow<lastLowBB) or (prices['Low'][i]<prices['LowerBand'][i])) and (prices['Adj Close'][i]>lastClose and prices['Adj Close'][i]>prices['LowerBand'][i]) and lastK <60:  
      plt.plot(prices["Date"][i],prices["Low"][i]-1, marker="o", ms=4, ls="", color='b')
 
    
    lastK=prices['K'][i]
    lastD=prices['D'][i]
    lastLow=prices['Low'][i]
    lastClose=prices['Adj Close'][i]
    lastLowBB=prices['LowerBand'][i]

  
  #Plot moving averages and BBands
  for x in smasUsed: #This for loop calculates the EMAs for te stated periods and appends to dataframe
    sma=x
    prices['SMA_'+str(sma)].plot(label='close') 
  prices['UpperBand'].plot(label='close',color='lightgray') 
  prices['LowerBand'].plot(label='close', color='lightgray') 

  #plot candlesticks
  candlestick_ohlc(ax1, ohlc, width=.5, colorup='k', colordown='r', alpha=0.75)

  ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d')) #change x axis back to datestamps
  ax1.xaxis.set_major_locator(mticker.MaxNLocator(8)) #add more x axis labels
  plt.tick_params(axis='x', rotation=45) #rotate dates for readability

  #Pivot Points
  pivots=[] #Stores pivot values
  dates=[]  #Stores Dates corresponding to those pivot values
  counter=0 #Will keep track of whether a certain value is a pivot
  lastPivot=0 #Will store the last Pivot value

  Range=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0] #Array used to iterate through stock prices
  dateRange=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0] #Array used to iterate through corresponding dates
  for i in prices.index: #Iterates through the price history
    currentMax=max(Range, default=0) #Determines the maximum value of the 10 item array, identifying a potential pivot
    value=round(prices["High"][i],2) #Receives next high value from the dataframe

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

    #print(str(pivots[index])+": "+str(dates[index])) #Prints Pivot, Date couple
    plt.plot_date([dates[index]-(timeD*.075), dates[index]+timeD], #Plots horizontal line at pivot value
                [pivots[index], pivots[index]], linestyle="--", linewidth=1, marker=',')
    plt.annotate(str(pivots[index]), (mdates.date2num(dates[index]), pivots[index]), xytext=(-10, 7), 
            textcoords='offset points',fontsize=7, arrowprops=dict(arrowstyle='-|>'))

  plt.xlabel('Date')
  plt.ylabel('Price')
  plt.title(stock+" - Daily")
  plt.ylim(prices["Low"].min(), prices["High"].max()*1.05)
  #plt.yscale("log")

  plt.show()
  # print()
  stock = input("Enter the stock symbol : ") #Asks for new stock
