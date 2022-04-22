from math import factorial
import pandas as pd
import re
import numpy as np
from stock import Stock, NAMES, ACTIONS
from option import Option
import filter
data = pd.read_excel('Input.xlsx', sheet_name='Activities')



data = filter.removeBadData(data)
data.sort_values(by=['Symbol', 'Transaction Date'], ascending=[True,True], inplace=True)


securities= [Stock('invalid')]


def getSecurity(symbol: str, type: str, description)-> Stock:
    for item in securities:
        if symbol == item.ticker:
            return item
    if(type == 'Option'):
        return Option(description)
    return Stock(symbol)
type = ''
for index, row in data.iterrows():
    if('PUT' in row['Description'] or 'CALL' in row['Description']):
        type = 'Option'
    else:
        type = 'Stock'
    if(row['Action'] == 'Buy'):
        secu = getSecurity(row['Symbol'], type, row['Description'])
        secu.buy(row['Quantity'], row['Price'], row['Commission'], row['Transaction Date'])
    elif(row['Action']== 'Sell'):
        secu = getSecurity(row['Symbol'], type, row['Description'])
        secu.sell(row['Quantity'], row['Price'], row['Commission'], row['Transaction Date'])
        

Stock.df.to_excel('Stocks.xlsx', index = None) 
Option.df.to_excel('Options.xlsx', index = None)        
        