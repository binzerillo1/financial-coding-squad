
import yfinance as yf
import datetime as dt
import pandas as pd
from pandas_datareader import data as pdr

yf.pdr_override() # <== that's all it takes :-)
start = dt.datetime(1980,12,1)
now = dt.datetime.now()
stock=""


stock = input("Enter the stock symbol : ") 
while stock != "quit":
 # df= web.DataReader(stock, 'yahoo', start,now)
  df = pdr.get_data_yahoo(stock, start, now)

  dfmonth=df.groupby(pd.Grouper(freq='M'))['High'].max()

  DOH=0
  GLV=0
  DOHc=""
  GLVc=0
  counter=0
  for index, value in dfmonth.items():
    if value> GLVc:
      GLVc=value
      DOHc=index
      counter=0
    if value < GLVc:
      counter=counter+1
      if counter==3 and ((index.month != now.month) or (index.year != now.year) ):
        GLV=GLVc
        counter=0
 
  #print("Date of GL: "+str(DOH))
  print("Last Green Line: "+str(GLV))
  a=df.iloc[-1]['Close']
  print("Last Closing Price: "+str(a)+"\n")
  stock = input("Enter the stock symbol : ") 