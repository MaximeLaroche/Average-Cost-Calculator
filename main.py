from math import factorial
import pandas as pd
import re
import numpy as np
from stock import Stock, NAMES, ACTIONS
from option import Option
import filter
data = pd.read_excel('Input.xlsx', sheet_name='Activities')



data = filter.removeBadData(data)
data.sort_values(by=[ 'Transaction Date'], ascending=[True], inplace=True)


securities= [Stock('invalid', 'CAD')]


def getSecurity(symbol: str, type: str, description, currency: str)-> Stock:
    for item in securities:
        if item.isRightSecurity(symbol, description):
            return item
    if(type == 'Option'):
        secu = Option(symbol, description, currency)
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
    if(row['Action'] == 'Buy'):
        secu = getSecurity(row['Symbol'], type, row['Description'], row['Currency'])
        secu.buy(row['Quantity'], row['Price'], row['Commission'], row['Transaction Date'], row['Description'])
    elif(row['Action']== 'Sell'):
        secu = getSecurity(row['Symbol'], type, row['Description'], row['Currency'])
        secu.sell(row['Quantity'], row['Price'], row['Commission'], row['Transaction Date'], row['Description'])
    elif(row['Action'] == 'ADJ'):
        secu = getSecurity(row['Symbol'], type, row['Description'], row['Currency'])
        

Option.export()
Stock.export()       
        