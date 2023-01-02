from math import factorial
import pandas as pd
import re
import numpy as np
from stock import Stock
from option import Option
from datetime import datetime
from numpy import number
from labels import makeFrench
import filter
from dataExport import export



data = pd.read_excel('questrade.xlsx', sheet_name='Activities')
data['Transaction Date'] = data['Transaction Date'].apply(lambda date: datetime.strptime(date, '%Y-%m-%d %H:%M:%S %p'))

data = filter.removeBadData(data)
data.sort_values(by=[ 'Transaction Date'], ascending=[True], inplace=True)


stocks= [Stock('invalid', 'CAD')]
options = [Option('invalid', 'CAD', 'CALL', 'invalid', datetime.now(),0)]
def extractOptionParams(description: str, currency: str):
    type: str = description.split(' ')[0]
    ticker = description.split(' ')[1]
    expString = description.split(' ')[2]
    try:
        exp: datetime = datetime.strptime(expString,'%m/%d/%y')
    except:
        print("except in ", expString)
    strike: number = float(description.split(' ')[3])
    return ticker, strike, type, exp

def makeOption(symbol: str, description: str, currency: str)-> Option:
    ticker, strike, type, exp = extractOptionParams(description, currency)
    option = Option(symbol,currency, type, ticker,exp, strike)
    return option

def getOption(symbol: str, description, currency: str, transactionDate: datetime)-> Option:
    ticker, strike, type, exp = extractOptionParams(description, currency)
    for item in options:
        if item.isRightOption(ticker, strike, exp, type, transactionDate):
            return item
    
    secu = makeOption(symbol, description, currency)
    options.append(secu)

    return secu

def getStock(symbol: str, description, currency: str)-> Stock:
    for item in stocks:
        if item.isRightSecurity(symbol, description):
            item.isRightSecurity(symbol, description)
            return item
    
    secu = Stock(symbol, currency)
    stocks.append(secu)
    return secu


type = ''
for index, row in data.iterrows():
    if('PUT' in row['Description'] or ('CALL' in row['Description'] and 'BMO COVERED CALL UTILITIES ETF' not in row['Description'])):
        type = 'Option'
    else:
        type = 'Stock'
    date = row['Transaction Date']
    if type == 'Option':
        if(row['Action'] == 'Buy'):
            secu = getOption(row['Symbol'], row['Description'], row['Currency'], date)
            secu.buy(row['Quantity'], row['Price'], row['Commission'], date, row['Description'])
        elif(row['Action']== 'Sell'):
            secu = getOption(row['Symbol'], row['Description'], row['Currency'], date)
            secu.sell(row['Quantity'], row['Price'], row['Commission'], date, row['Description'])
        elif(row['Action'] == 'ADJ'):
            secu = getOption(row['Symbol'], row['Description'], row['Currency'], date)
            newSym = row['Description'].split(' ')[-1]
            symbols = [row['Symbol'], newSym]
            secu.addSymbols(symbols)
        elif(row['Action'] == 'EXP'):
            secu = getOption(row['Symbol'], row['Description'], row['Currency'], date)
            secu.expire(row['Quantity'], date, row['Description'])
        elif(row['Action'] == 'ASN'):
            secu = getOption(row['Symbol'], row['Description'], row['Currency'], date)
            secu.assign(row['Quantity'], date, row['Description'])
    elif type == 'Stock':
        if(row['Action'] == 'Buy'):
            secu = getStock(row['Symbol'], row['Description'], row['Currency'])
            secu.buy(row['Quantity'], row['Price'], row['Commission'], date, row['Description'])
        elif(row['Action']== 'Sell'):
            secu = getStock(row['Symbol'], row['Description'], row['Currency'])
            secu.sell(row['Quantity'], row['Price'], row['Commission'], date, row['Description'])

    
export('Questrade')