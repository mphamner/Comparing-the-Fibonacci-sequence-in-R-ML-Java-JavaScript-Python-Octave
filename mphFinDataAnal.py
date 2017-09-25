# -*- coding: utf-8 -*-
"""
Created on Tue Jul 18 16:26:41 2017

@author: Marvine_2
"""

import pandas as pd
import matplotlib.pyplot as plt
import pylab
import urllib.request

from IPython import get_ipython
get_ipython().run_line_magic('matplotlib', 'inline')

# First get the data you need

    #First get the beginning and ending dates for the analysis

strtmonth = input('Enter the month for the starting date spelled out, e.g. January:  ')
strtday = input('Enter the day of the starting month as two digits, e.g. 01 or 29:  ')  
strtyear = input('Enter the starting year as four digits, e.g. 1990 or 2007:  ')
strt = strtmonth + ' ' +  strtday + ', ' + strtyear
print('The starting date is ',strt)

ndmonth = input('Enter the month for the ending date spelled out, e.g. December:  ')
ndday = input('Enter the day of the ending month as two digits, e.g. 01 or 29:  ')  
ndyear = input('Enter the ending year as four digits, e.g. 1990 or 2007:  ')
nddate = ndmonth + ' ' +  ndday + ', ' + ndyear
print('The ending date is ',nddate)


print('\n\nYou will get data for four stock tickers in this program.\n\n')

companies = ['CVX', 'XOM', 'AMZN', 'WMT']

url = ('https://www.google.com/finance/historical?output=csv&q=' + 'CVX' + '&startdate=' +
    strtmonth + '+' + strtday + '%2C+' + strtyear + '&enddate=' + ndmonth + '+' + ndday +
    '%2C+' + ndyear)

datFile = 'datDownload_0.xls'
urllib.request.urlretrieve(url, datFile)
print('Getting ',datFile)
Chevron = pd.read_csv(datFile)

url = ('https://www.google.com/finance/historical?output=csv&q=' + 'XOM' + '&startdate=' +
    strtmonth + '+' + strtday + '%2C+' + strtyear + '&enddate=' + ndmonth + '+' + ndday +
    '%2C+' + ndyear)

datFile = 'datDownload_1.xls'
urllib.request.urlretrieve(url, datFile)
print('Getting ',datFile)
Exxon = pd.read_csv(datFile)

url = ('https://www.google.com/finance/historical?output=csv&q=' + 'AMZN' + '&startdate=' +
    strtmonth + '+' + strtday + '%2C+' + strtyear + '&enddate=' + ndmonth + '+' + ndday +
    '%2C+' + ndyear)

datFile = 'datDownload_2.xls'
urllib.request.urlretrieve(url, datFile)
print('Getting ',datFile)
Amazon = pd.read_csv(datFile)

url = ('https://www.google.com/finance/historical?output=csv&q=' + 'WMT' + '&startdate=' +
    strtmonth + '+' + strtday + '%2C+' + strtyear + '&enddate=' + ndmonth + '+' + ndday +
    '%2C+' + ndyear)

datFile = 'datDownload_3.xls'
urllib.request.urlretrieve(url, datFile)
print('Getting ',datFile)
Walmart = pd.read_csv(datFile)

print('Finished reading in data.')


# Perform data munging

   # First work on 'Date' to get in the proper format to index
   # In its current string format will sort on Month first not chronologically

import datetime

Chevron['Date'] = pd.to_datetime(Chevron['Date'])
Exxon['Date'] = pd.to_datetime(Exxon['Date'])
Amazon['Date'] = pd.to_datetime(Amazon['Date'])
Walmart['Date'] = pd.to_datetime(Walmart['Date'])

   # Now set the Date as the index

Chevron = Chevron.set_index('Date')
Exxon = Exxon.set_index('Date')
Amazon = Amazon.set_index('Date')
Walmart = Walmart.set_index('Date')

   #Sort the data in ascending date order

Chevron = Chevron.sort_index(ascending=True)
Exxon = Exxon.sort_index(ascending=True)
Amazon = Amazon.sort_index(ascending=True)
Walmart = Walmart.sort_index(ascending=True)

print('Finished data munging')



# Examples for plotting data

pylab.rcParams['figure.figsize'] = (10, 6) #Change the size of the plots

plt.plot(Chevron['Close'])
plt.title('Chevron (CVX) Close')
plt.xlabel('Date (Year)')
plt.ylabel('Close')
plt.show()

plt.plot(Exxon['Close'])
plt.title('Exxon (XOM) Close')
plt.xlabel('Date (Year)')
plt.ylabel('Close')
plt.show()


plt.plot(Chevron['Volume'])
plt.title('Chevron (CVX) Volume')
plt.xlabel('Date (Year)')
plt.ylabel('Volume')
plt.show()

plt.plot(Exxon['Volume'], Chevron['Volume'], 'r.')
plt.title('CVX versus XOM Volume')
plt.xlabel('XOM Volume')
plt.ylabel('CVX Volume')
plt.show()


# Now process the data

   # Calculate daily returns

Chevron_rets = Chevron['Close'].pct_change()
Exxon_rets = Exxon['Close'].pct_change()
Amazon_rets = Amazon['Close'].pct_change()
Walmart_rets = Walmart['Close'].pct_change()

   #Calculate and plot one-year moving correlations

oneYrEnergy = pd.rolling_corr(Chevron_rets, Exxon_rets, 250).plot()
plt.title('One Year Rolling Correlation - 2 Energy Companies')
plt.show()
oneYrRetail = pd.rolling_corr(Amazon_rets, Walmart_rets, 250).plot()
plt.title('One Year Rolling Correlation - 2 Retail Companies')
plt.show()

   # Consider volatility
   # Build a least-squares regression to model the dynamic relationship


import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.sandbox.regression.predstd import wls_prediction_std
import numpy as np
from patsy import dmatrices



y = Chevron['Close']
x = Exxon['Close']
X = sm.add_constant(x)
print(y.head())
print('y type is ',y.dtype)
print(X.head())
print('X type is ',X.dtypes)

energyModel = sm.OLS(y, X)
energyFit = energyModel.fit()
print(energyFit.summary())

print('Completed the first linear model.')

   #Consider the second industry
   #First plot some data

   #Number of rows does not match so reduce Walmart by one row
Walmart = Walmart[:-1]

plt.plot(Amazon['Volume'])
plt.title('Amaxon (AMZN) Volume')
plt.xlabel('Date (Year)')
plt.ylabel('Volume')
plt.show()

plt.plot(Walmart['Volume'])
plt.title('Walmart (WMT) Volume')
plt.xlabel('Date (Year)')
plt.ylabel('Volume')
plt.show()

plt.plot(Walmart['Volume'], Amazon['Volume'], 'r.')
plt.title('AMZN versus WMT Volume')
plt.xlabel('WMT Volume')
plt.ylabel('AMZN Volume')
plt.show()

plt.plot(Amazon['Close'])
plt.title('Amaxon (AMZN) Close')
plt.xlabel('Date (Year)')
plt.ylabel('Close')
plt.show()

plt.plot(Walmart['Close'])
plt.title('Walmart (WMT) Close')
plt.xlabel('Date (Year)')
plt.ylabel('Close')
plt.show()

plt.plot(Walmart['Close'], Amazon['Close'], 'r.')
plt.title('AMZN versus WMT Close')
plt.xlabel('WMT Close')
plt.ylabel('AMZN Close')
plt.show()

s1 = pd.Series(Amazon['Close'])
s2 = pd.Series(Walmart['Close'])
df = pd.DataFrame({'AMZN':s1, 'WMT':s2}, index=Amazon.index)
print(df.head(10))
print('')


y2 = df['AMZN']
x2 = df['WMT']
X2 = sm.add_constant(x2)
print(y2.head())
print('y type is ',y2.dtype)
print(X2.head())
print('X type is ',X2.dtypes)

retailModel = sm.OLS(y2, X2)
print('OLS ran')
retailFit = retailModel.fit()
print(retailFit.summary())

