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


securities= [Stock('invalid', 'CAD')]


def makeOption(symbol: str, description: str, currency: str)-> Option:
    type: str = description.split(' ')[0]
    ticker = description.split(' ')[1]
    expString = description.split(' ')[2]
    exp: datetime = datetime.strptime(expString,'%m/%d/%y')
    strike: number = float(description.split(' ')[3])
    option = Option(symbol,currency, type, ticker,exp, strike)
    return option

def getOption(symbol: str, description, currency: str)-> Option:
    for item in securities:
        if item.isRightSecurity(symbol, description):
            item.isRightSecurity(symbol, description)
            return item
    
    secu = makeOption(symbol, description, currency)
    securities.append(secu)

    return secu

def getSecurity(symbol: str, type: str, description, currency: str)-> Stock:
    for item in securities:
        if item.isRightSecurity(symbol, description):
            item.isRightSecurity(symbol, description)
            return item
    if(type == 'Option'):
        secu = makeOption(symbol, description, currency)
        securities.append(secu)

        return secu
    secu = Stock(symbol, currency)
    securities.append(secu)
    return secu


type = ''
for index, row in data.iterrows():
    if('PUT' in row['Description'] or 'CALL' in row['Description']):
        type = 'Option'
    else:
        type = 'Stock'
    date = row['Transaction Date']
    if(row['Action'] == 'Buy'):
        secu = getSecurity(row['Symbol'], type, row['Description'], row['Currency'])
        secu.buy(row['Quantity'], row['Price'], row['Commission'], date, row['Description'])
    elif(row['Action']== 'Sell'):
        secu = getSecurity(row['Symbol'], type, row['Description'], row['Currency'])
        secu.sell(row['Quantity'], row['Price'], row['Commission'], date, row['Description'])
    elif(row['Action'] == 'ADJ'):
        secu = getOption(row['Symbol'], row['Description'], row['Currency'])
        newSym = row['Description'].split(' ')[-1]
        symbols = [row['Symbol'], newSym]
        secu.addSymbols(symbols)
        fractionStrings = re.findall('[0-9]+:[0-9]+', row['Description'])
        for frString in fractionStrings:
            num = int(frString.split(':')[0])
            den = int(frString.split(':')[1])
            ratio: float = num/den
            secu.adj(date, row['Description'], ratio)
    elif(row['Action'] == 'EXP'):
        secu = getOption(row['Symbol'], row['Description'], row['Currency'])
        secu.expire(row['Quantity'], date, row['Description'])
    elif(row['Action'] == 'ASN'):
        secu = getOption(row['Symbol'], row['Description'], row['Currency'])
        secu.assign(row['Quantity'], date, row['Description'])

     
export()