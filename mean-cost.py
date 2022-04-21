from math import factorial
import pandas as pd
import re
import numpy as np
raw = pd.read_excel('Input.xlsx', sheet_name='Activities')


def removeTFSA(df: pd.DataFrame) -> pd.DataFrame:
    df = df.drop(df[df["Account Type"] == "Individual TFSA"].index)
    return df

def removeUnusedCol(df: pd.DataFrame) -> pd.DataFrame:
    df.drop(['Account #', 'Activity Type', 'Account Type','Settlement Date'], axis = 1, inplace = True) 
    return df

data = removeTFSA(raw)
data = removeUnusedCol(data)
data.sort_values(by=['Symbol', 'Transaction Date'], ascending=[True,True], inplace=True)

# CAD = data[(data["Currency"] == 'CAD')]
# USD = data[(data["Currency"] == 'USD')]

data["average cost"] = 0
data["total ammount of shares"] = 0
data['Errors'] = ''
data['Other Symbols'] = ''
data['Type'] = ''
# Calculate cumulative averave cost
type = ''
avg = 0
tot = 0
sym = []
for index, row in data.iterrows():
    if('PUT' in row['Description'] or 'CALL' in row['Description']):
        type = 'Option'
    else:
        type = 'Stock'
    if row['Symbol'] not in sym :
        sym = [row['Symbol']]
        avg = 0
        tot = 0
    if row['Action'] == 'Buy' and tot >= 0: # we have some and are buying
        if(type == 'Option'):
            avg = (avg * tot - row['Net Amount']/100) / (row['Quantity'] + tot)
        else:
            avg = (avg * tot - row['Net Amount']) / (row['Quantity'] + tot)
    if row['Action'] == 'Sell' and tot <= 0: # Sell to Open
        data.at[index, 'Action'] = 'Sell to Open'
    if row['Action'] == 'Buy' and tot < 0: # we shored and are in the process of closing the short
        if(type == 'Option'):
            avg = row['Price'] + row['Commission']/100
        else:
            avg = row['Price'] + row['Commission']
        data.at[index, 'Action'] = 'Buy to close'
    if row['Action'] == 'REV': # reverse split
        try:
            fractionString = re.findall('[1-9]+:[1-9]+', row['Description'])[0]
            numerator = int(fractionString.split(':')[0])
            denominator = int(fractionString.split(':')[1])
            fraction = numerator / denominator
            tot *= fraction
            avg /= fraction
            otherSymbols = re.findall('TO [0-9]{3,5}G[0-4]{3,5}', row['Description'])
            sym = np.append(sym, otherSymbols)
            data.at[index, 'Other Symbols'] += ''.join((otherSymbol) for otherSymbol in otherSymbols)
            print('Calculated')
        except:
            data.at[index,'Errors'] = 'Could not calculate stock split'
    if row['Action'] == 'ADJ': # option split or reverse option split
        try:
            fractionString = re.findall('[1-9]+:[1-9]+', row['Description'])[0]
            numerator = int(fractionString.split(':')[0])
            denominator = int(fractionString.split(':')[1])
            fraction = numerator / denominator
            tot *= fraction
            avg /= fraction
            otherSymbols = re.findall('[0-9][A-Z0-9]{6}', row['Description'])
            sym = np.append(sym, otherSymbols)
            data.at[index, 'Other Symbols'] += ''.join((otherSymbol) for otherSymbol in otherSymbols)
        except:
            data.at[index,'Errors'] = 'Could not calculate option split'
    tot = row['Quantity'] + tot
    data.at[index,'average cost'] = avg
    data.at[index, 'total ammount of shares'] = tot
    data.at[index, 'Type'] = type
    
# sort by date
# data.sort_values(by=['Transaction Date'], ascending=[True], inplace=True)
# remove all buy transactions
# data = data.drop(data[data['Action'] == 'Buy'].index)

CAD = data[(data['Currency'] == 'CAD')]
USD = data[(data['Currency'] == 'USD')]

CAD.to_excel ('CAD.xlsx', index = None) 
USD.to_excel ('USD.xlsx', index = None) 

# print(data[['Transaction Date', 'Symbol','Action', 'Quantity', 'Price', 'total ammount of shares', 'average cost']])