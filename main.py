from math import factorial
import pandas as pd
import re
import numpy as np
from sec import Security, NAMES, ACTIONS
data = pd.read_excel('Input.xlsx', sheet_name='Activities')

securities= [Security('invalid')]


def getSecurity(symbol: str)-> Security:
    for item in securities:
        if symbol == item.ticker:
            return item
    return Security(symbol)

for index, row in data.iterrows():
    if(row['Action'] == 'Buy'):
        secu = getSecurity(row['Symbol'])
        secu.buy(row['Quantity'], row['Price'], row['Commission'], row['Transaction Date'])

Security.df.to_excel('Output.xlsx', index = None) 
        
        