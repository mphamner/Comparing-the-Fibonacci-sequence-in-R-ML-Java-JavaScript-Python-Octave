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

print('This program is for you to compare two companies within an industry, or.')
print('a company and a relevant index, across two industries.\n')
print('So, you will need to enter the names of the industries and stock tickers for')
print('four companies.')
print('\nYou can enter and retrieve data for up to four stock tickers ')
print('using this program.\n\n')

firstInd = input('Enter the name of the first industry you are interested in: ')
print('You entered', firstInd)
co1 = input('Enter the stock ticker for the first company:  ')
print('You entered ', co1)
co2 = input('Enter the stock ticker for the second company:  ')
print('You entered ', co2)
secondInd = input('Enter the name of the second industry you are interested in: ')
print('You entered', secondInd)
co3 = input('Enter the stock ticker for the third company:  ')
print('You entered ', co3)
co4 = input('Enter the stock ticker for the third company:  ')
print('You entered ', co4)

# companies = ['CVX', 'XOM', 'AMZN', 'WMT']
industries = [firstInd, secondInd]
print('The industries you entered are: ', industries)
companies = [co1, co2, co3, co4]
print('The stock tickers you entered are: ', companies)


url = ('https://www.google.com/finance/historical?output=csv&q=' + co1 + '&startdate=' +
    strtmonth + '+' + strtday + '%2C+' + strtyear + '&enddate=' + ndmonth + '+' + ndday +
    '%2C+' + ndyear)

datFile = 'datDownload_0.xls'
urllib.request.urlretrieve(url, datFile)
print('Getting ',datFile)
firstCo = pd.read_csv(datFile)

url = ('https://www.google.com/finance/historical?output=csv&q=' + co2 + '&startdate=' +
    strtmonth + '+' + strtday + '%2C+' + strtyear + '&enddate=' + ndmonth + '+' + ndday +
    '%2C+' + ndyear)

datFile = 'datDownload_1.xls'
urllib.request.urlretrieve(url, datFile)
print('Getting ',datFile)
secondCo = pd.read_csv(datFile)

url = ('https://www.google.com/finance/historical?output=csv&q=' + co3 + '&startdate=' +
    strtmonth + '+' + strtday + '%2C+' + strtyear + '&enddate=' + ndmonth + '+' + ndday +
    '%2C+' + ndyear)

datFile = 'datDownload_2.xls'
urllib.request.urlretrieve(url, datFile)
print('Getting ',datFile)
thirdCo = pd.read_csv(datFile)

url = ('https://www.google.com/finance/historical?output=csv&q=' + co4 + '&startdate=' +
    strtmonth + '+' + strtday + '%2C+' + strtyear + '&enddate=' + ndmonth + '+' + ndday +
    '%2C+' + ndyear)

datFile = 'datDownload_3.xls'
urllib.request.urlretrieve(url, datFile)
print('Getting ',datFile)
fourthCo = pd.read_csv(datFile)

print('Finished reading in data.')


# Perform data munging

   # First work on 'Date' to get in the proper format to index
   # In its current string format will sort on Month first not chronologically

import datetime

firstCo['Date'] = pd.to_datetime(firstCo['Date'])
secondCo['Date'] = pd.to_datetime(secondCo['Date'])
thirdCo['Date'] = pd.to_datetime(thirdCo['Date'])
fourthCo['Date'] = pd.to_datetime(fourthCo['Date'])

   # Now set the Date as the index

#firstCo = firstCo.set_index('Date')
#secondCo = secondCo.set_index('Date')
#thirdCo = thirdCo.set_index('Date')
#fourthCo = fourthCo.set_index('Date')

   #Sort the data in ascending date order

firstCo = firstCo.sort_index(ascending=True)
secondCo = secondCo.sort_index(ascending=True)
thirdCo = thirdCo.sort_index(ascending=True)
fourthCo = fourthCo.sort_index(ascending=True)

firstCo.set_index('Date', inplace=True)
secondCo.set_index('Date', inplace=True)
thirdCo.set_index('Date', inplace=True)
fourthCo.set_index('Date', inplace=True)


   #Number of rows does not match so reduce Walmart by one row
#Walmart = Walmart[:-1]

a = len(firstCo)
print('a = ' + str(a))
print(firstCo.head())
b = len(secondCo)
print('b = ' + str(b))
print(secondCo.head())
c = len(thirdCo)
print('c = ' + str(c))
print(thirdCo.head())
d = len(fourthCo)
print('d = ' + str(d))
print(fourthCo.head())

if a < b:
    secondCo = secondCo.reindex(firstCo.index, method='nearest')
    print('1. Difference in lengths was ' + str(abs(a-b)))
    print('Now ' + co2 + ' has ' + str(len(secondCo)) + ' records.')
if b < a:
    firstCo = firstCo.reindex(secondCo.index, method='nearest')
    print('2. Difference in lengths was ' + str(abs(a-b)))
    print('Now ' + co1 + ' has ' + str(len(firstCo)) + ' records.')
if c < d:
    fourthCo = fourthCo.reindex(thirdCo.index, method='nearest')
    print('3. Difference in lengths was ' + str(abs(a-b)))
    print('Now ' + co4 + ' has ' + str(len(fourthCo)) + ' records.')
if d < c:
    thirdCo = thirdCo.reindex(fourthCo.index, method='nearest')
    print('4. Difference in lengths was ' + str(abs(a-b)))
    print('Now ' + co3 + ' has ' + str(len(thirdCo)) + ' records.')



print('Finished data munging')



# Examples for plotting data

pylab.rcParams['figure.figsize'] = (10, 6) #Change the size of the plots

plt.plot(firstCo['Close'])
plt.title('Closing price for ' + co1)
plt.xlabel('Date (Year)')
plt.ylabel('Close')
plt.show()


plt.plot(secondCo['Close'])
plt.title('Closing price for ' + co2)
plt.xlabel('Date (Year)')
plt.ylabel('Close')
plt.show()


plt.plot(thirdCo['Volume'])
plt.title('Volume for ' + co1)
plt.xlabel('Date (Year)')
plt.ylabel('Volume')
plt.show()

plt.plot(secondCo['Volume'], firstCo['Volume'], 'r.')
plt.title('Cross-plot of Volume for ' + co1 + ' and ' + co2)
ttl = ('Volume (' + co2 + ')')
plt.xlabel(ttl)
ttl = ('Volume (' + co1 + ')')
plt.ylabel(ttl)
plt.show()


# Now process the data

   # Calculate daily returns

firstCo_rets = firstCo['Close'].pct_change()
secondCo_rets = secondCo['Close'].pct_change()
thirdCo_rets = thirdCo['Close'].pct_change()
fourthCo_rets = fourthCo['Close'].pct_change()

   #Calculate and plot one-year moving correlations

oneYrEnergy = pd.rolling_corr(firstCo_rets, secondCo_rets, 250).plot()
ttl = ('One Year Rolling Correlation between 2 ' + firstInd + ' Companies')
plt.title(ttl)
plt.show()
oneYrRetail = pd.rolling_corr(thirdCo_rets, fourthCo_rets, 250).plot()
ttl = ('One year Rolling Correlation between 2 ' + secondInd + ' Companies')
plt.title(ttl)
plt.show()

   # Consider volatility
   # Build a least-squares regression to model the dynamic relationship


import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.sandbox.regression.predstd import wls_prediction_std
import numpy as np
from patsy import dmatrices


print('The length of co1 is ' + str(len(firstCo)))
print('The length of co2 is ' + str(len(secondCo)))

y = firstCo['Close']
x = secondCo['Close']
X = sm.add_constant(x)
print(y.head())
print('y type is ',y.dtype)
print(X.head())
print('X type is ',X.dtypes)

firstIndModel = sm.OLS(y, X)
firstIndFit = firstIndModel.fit()
print(firstIndFit.summary())

print('Completed the first linear model.')

   #Consider the second industry
   #First plot some data

plt.plot(thirdCo['Volume'])
ttl = ('Volume (' + co3 + ')')
plt.title(ttl)
plt.xlabel('Date (Year)')
ttl = ('Volume (' + co4 + ')')
plt.ylabel(ttl)
plt.show()

plt.plot(fourthCo['Volume'])
ttl = ('Volume (' + co4 + ')')
plt.title(ttl)
plt.xlabel('Date (Year)')
ttl = ('Volume (' + co3 + ')')
plt.ylabel(ttl)
plt.show()

plt.plot(fourthCo['Volume'], thirdCo['Volume'], 'r.')
ttl = (co3 + ' versus ' + co4 + ' Volume')
plt.title(ttl)
ttl = ('Volume (' + co4 + ')')
plt.xlabel(ttl)
ttl = ('Volume (' + co3 + ')')
plt.ylabel(ttl)
plt.show()

plt.plot(thirdCo['Close'])
ttl = (co3 + ' Close')
plt.title(ttl)
plt.xlabel('Date (Year)')
ttl = (co4 + ' Close')
plt.ylabel(ttl)
plt.show()

plt.plot(fourthCo['Close'])
ttl = (co4 + ' Close')
plt.title(ttl)
plt.xlabel('Date (Year)')
ttl = (co3 + ' Close')
plt.ylabel(ttl)
plt.show()

plt.plot(fourthCo['Close'], thirdCo['Close'], 'r.')
ttl = (co3 + ' versus ' + co4 + ' Close')
plt.title(ttl)
ttl = (co4 + ' Close')
plt.xlabel(ttl)
ttl = (co3 + ' Close')
plt.ylabel(ttl)
plt.show()

# Put the time series data in a single data frame, if desired
s3 = pd.Series(thirdCo['Close'])
s4 = pd.Series(fourthCo['Close'])
df = pd.DataFrame({co3:s3, co4:s4}, index=thirdCo.index)
print(df.head(10))
print('')

# Build the linear model for the second industry
y2 = df[co3]
x2 = df[co4]
X2 = sm.add_constant(x2)
print(y2.head())
print('y type is ',y2.dtype)
print(X2.head())
print('X type is ',X2.dtypes)

secondIndModel = sm.OLS(y2, X2)
print('OLS ran')
secondIndFit = secondIndModel.fit()
print(secondIndFit.summary())

