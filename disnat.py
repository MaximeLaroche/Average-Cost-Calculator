from locale import currency
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

data = pd.read_csv('disnat.csv', sep=';',  encoding = "ISO-8859-1", engine='python')

data = data.dropna(subset=['Date de règlement'])
data['Date de règlement'] = data['Date de règlement'].apply(lambda date: datetime.strptime(date, '%Y-%m-%d'))
data.sort_values(by=['Date de règlement'], ascending=[True], inplace=True)
securities= [Stock('invalid', 'CAD')]
print(data)


def makeOption(symbol: str, currency: str)-> Option:
    type: str = re.findall('[0-9][P|C][0-9]', symbol)[0]
    if 'P' == type:
        type = 'PUT'
    elif 'C' == type:
        type = 'CALL'
    ticker = re.split('[0-9]', symbol)[0]
    dateString: str = re.findall('[0-9]{6}', symbol)[0]
    year = int(dateString[:2])
    month = int(dateString[2:4])
    day = int(dateString[4:6])
    exp: datetime = datetime(year, month, day)
    strikeString = re.split('[0-9]{6}[P|C]', symbol)[1]
    strike: number = makeNum(re.findall('[0-9]+[.]{0,1}[0-9]+', strikeString)[0])
    option = Option(symbol,currency, type, ticker,exp, strike)
    return option

def getOption(symbol: str, currency: str)-> Option:
    for item in securities:
        if item.isRightSecurity(symbol, symbol):
            item.isRightSecurity(symbol, symbol)
            return item
    
    secu = makeOption(symbol, currency)
    securities.append(secu)

    return secu

def getSecurity(symbol: str, description, currency: str)-> Stock:
    for item in securities:
        if item.isRightSecurity(symbol, description):
            item.isRightSecurity(symbol, description)
            return item
        
    secu = Stock(symbol, currency)
    securities.append(secu)
    return secu

def makeNum(num)->float:
    floatType = type(3.5)
    intType = type(3)
    strType = type('Bonjour')
    if type(num) == floatType or type(num) == intType:
        return num
    elif type(num) == strType:
        num = num.replace(',', '.')
        numeric = float(num)
        return numeric
    raise 'Trying to make a number out of invalid types'

secType = ''
for index, row in data.iterrows():
    secType = row["Classification d''actif"]
    date = row['Date de règlement']
    if secType == 'Actions':

        if 'ACHAT' in row['Type de transaction']:
            secu = getSecurity(row['Symbole'], row['Description'], row['Devise du prix'])
            secu.buy(int(row['Quantité']), makeNum(row['Prix']), makeNum(row['Commission payée']), date, row['Description'] )
        elif 'VENTE' in row['Type de transaction']:
            secu = getSecurity(row['Symbole'], row['Description'], row['Devise du prix'])
            secu.sell(int(row['Quantité']), makeNum(row['Prix']), makeNum(row['Commission payée']), date, row['Description'] )

    if secType == 'Options':

        if 'ACHAT' in row['Type de transaction']:
            secu = getOption(row['Symbole'], row['Devise du prix'])
            secu.buy(int(row['Quantité']), makeNum(row['Prix']), makeNum(row['Commission payée']), date, row['Description'] )
        if 'VENTE' in row['Type de transaction']:
            secu = getOption(row['Symbole'], row['Devise du prix'])
            secu.sell(int(row['Quantité']), makeNum(row['Prix']), makeNum(row['Commission payée']), date, row['Description'] )
        
         
export()