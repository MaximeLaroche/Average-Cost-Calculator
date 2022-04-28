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


makeFrench()
data = pd.read_csv('disnat.csv', sep=';', encoding='utf-8', engine='python')
# data = pd.read_excel('disnat.xlsx')
def makeDate(dateString: str) -> datetime:
    if type(dateString) == type('String'):
        date = datetime.strptime(dateString, '%Y-%m-%d')
        if date.year < 100:
            newDate = datetime(date.year+2000, date.month, date.day)
            return newDate
        return date
    return None
def addSECFeesToCommission(qtyRaw: float, priceRaw: float, totalRaw: float, commissionStr: float, typeOfSec: str, typeOfTransaction: str)->float:
    qty = abs(makeNum(qtyRaw))
    price = abs(makeNum(priceRaw))
    total = abs(makeNum(totalRaw))
    commission = abs(makeNum(commissionStr))
    fees = 0
    if 'VENTE' in typeOfTransaction:
        if typeOfSec == 'Actions':
            fees = abs(qty * price - commission - total)
        elif typeOfSec == 'Options':
            fees = abs(100 * qty * price - commission - total)
    elif 'ACHAT' in typeOfTransaction:
        if typeOfSec == 'Actions':
            fees = abs(qty * price + commission - total)
        elif typeOfSec == 'Options':
            fees = abs(100 * qty * price + commission - total)
    if total == 0:
        fees = 0
    return commission + fees

data['Date de transaction'] = data['Date de transaction'].apply(
    lambda date: makeDate(date)
)
data['Date de règlement'] = data['Date de règlement'].apply(lambda date: makeDate(date))

data.sort_values(by=['Date de règlement', 'Date de transaction'], ascending=[True, True], inplace=True)
stocks= [Stock('invalid', 'CAD')]
options = [Option('invalid', 'CAD', 'CALL', 'invalid', datetime.now(),0)]


def extractOptionParams(symbol: str, currency: str):
    type: str = re.findall('[0-9][P|C][0-9]', symbol)[0][1]
    if 'P' == type:
        type = 'PUT'
    elif 'C' == type:
        type = 'CALL'
    ticker = re.split('[0-9]', symbol)[0]
    dateString: str = re.findall('[0-9]{6}', symbol)[0]
    year = int(dateString[:2])
    if year < 2000:
        year += 2000
    month = int(dateString[2:4])
    day = int(dateString[4:6])
    exp: datetime = datetime(year, month, day)
    strikeString = re.split('[0-9]{6}[P|C]', symbol)[1]
    strike: number = makeNum(re.findall('[0-9]+[.]{0,1}[0-9]+', strikeString)[0])
    return ticker, strike, type, exp
def makeOption(symbol: str, currency: str)-> Option:
    ticker, strike, type, exp = extractOptionParams(symbol, currency)
    option = Option(symbol,currency, type, ticker,exp, strike)
    return option

def getOption(symbol: str, description, currency: str, transactionDate: datetime)-> Option:
    ticker, strike, type, exp = extractOptionParams(symbol, currency)
    for item in options:
        if item.isRightOption(ticker, strike, exp, type, transactionDate):
            return item
    
    secu = makeOption(symbol, currency)
    options.append(secu)

    return secu

def defineStringField(field: str)->str:
    # if field == None or type(field) != type('string'):
    #     return ''
    return field
def getStock(symbol: str, description, currency: str)-> Stock:
    symbol = defineStringField(symbol)
    description = defineStringField(description)
    currency = defineStringField(currency)
    for item in stocks:
        if item.isRightSecurity(symbol, description):
            item.isRightSecurity(symbol, description)
            return item
        
    secu = Stock(symbol, currency)
    stocks.append(secu)
    return secu

def makeNum(num)->float:
    floatType = type(3.5)
    intType = type(3)
    strType = type('Bonjour')
    if type(num) == floatType or type(num) == intType:
        return num
    elif type(num) == strType:
        num = num.replace(',', '.').replace(' ', '').replace('$','')
        numeric = float(num)
        return numeric
    raise 'Trying to make a number out of invalid types'


secType = ''
successionTransferDate = datetime(year=2019, month=12, day=20)
debugDate = datetime(year=2021, month=7, day=14)
for index, row in data.iterrows():
    secType = row["Classification d''actif"]
    date = row['Date de transaction']
    data['Commission payée'] = addSECFeesToCommission(row['Quantité'], row['Prix'], row["Montant de l''opération"], row['Commission payée'], secType, row['Type de transaction'])
    if secType == 'Actions':
        
        if 'ACHAT' in row['Type de transaction']:
            secu = getStock(row['Symbole'], row['Description'], row['Devise du prix'])
            secu.buy(int(row['Quantité']), makeNum(row['Prix']), makeNum(row['Commission payée']), date, row['Description'] )
        elif 'VENTE' in row['Type de transaction']:
            secu = getStock(row['Symbole'], row['Description'], row['Devise du prix'])
            secu.sell(int(row['Quantité']), makeNum(row['Prix']), makeNum(row['Commission payée']), date, row['Description'] )
        elif 'TRSF' in row['Type de transaction'] and row['Date de règlement'] == successionTransferDate and (row['Prix'] != '' and row['Prix'] != None):
            secu = getStock(row['Symbole'], row['Description'], row['Devise du prix'])
            date = row['Date de règlement']
            secu.buy(int(row['Quantité']), makeNum(row['Prix']), makeNum(row['Commission payée']), date, row['Description'] + 'Transfert de succession' )
        elif 'FAILLI' in row['Type de transaction']:
            date = row['Date de règlement']
            try:
                secu = getStock(row['Symbole'], row['Description'], row['Devise du prix'])
                date = row['Date de règlement']
                sellPrice = 0
                commission = 0
                secu.sell(int(row['Quantité']), sellPrice, commission, date, row['Description'] + 'Faillite')
            except:
                print('Faillite sur ' + row['Description'] + ' le ' + str(date) + ': Veuillez entrer entrer le symbole de l\'entreprise qui a fait faillite\n')
        elif 'ECH' in row ['Type de transaction']:
            date = row['Date de règlement']
            try:
                secu = getStock(row['Symbole'], row['Description'], row['Devise du prix'])
                secu.changeTicker(row['Description'], date)
            except:
                print('Échange de nom sur ' + row['Description'] + ' le ' + str(date) + ': Veuillez entrer le vieux symbole d\'entreprise dans la rangée symbole et le nouveau symbole dans la rangée description\n')



    elif secType == 'Options':
        
        if 'ACHAT' in row['Type de transaction']:
            secu = getOption(row['Symbole'], row['Description'], row['Devise du prix'], date)
            secu.buy(int(row['Quantité']), makeNum(row['Prix']), makeNum(row['Commission payée']), date, row['Description'] )
        if 'VENTE' in row['Type de transaction']:
            secu = getOption(row['Symbole'], row['Description'], row['Devise du prix'], date)
            secu.sell(int(row['Quantité']), makeNum(row['Prix']), makeNum(row['Commission payée']), date, row['Description'] )

# Check if options expired
today = datetime.now()
for option in options:
    option.maybeExpire(today)   
        
export('Disnat')