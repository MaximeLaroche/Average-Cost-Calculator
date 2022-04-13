import pandas as pd

raw = pd.read_excel('Activities_for_10Sep2019_to_12Apr2022.xlsx', sheet_name='Activities')


def removeTFSA(df: pd.DataFrame) -> pd.DataFrame:
    df = df.drop(df[df["Account Type"] == "Individual TFSA"].index)
    return df

def removeUnusedCol(df: pd.DataFrame) -> pd.DataFrame:
    df.drop(['Account #', 'Activity Type', 'Account Type'], axis = 1, inplace = True) 
    return df

data = removeTFSA(raw)
data = removeUnusedCol(data)
data.sort_values(by=['Symbol', 'Transaction Date'], ascending=[True,True], inplace=True)

# CAD = data[(data["Currency"] == 'CAD')]
# USD = data[(data["Currency"] == 'USD')]

data["average cost"] = 0
data["total ammount of shares"] = 0


# Calculate cumulative averave cost

avg = 0
tot = 0
sym = ''
for index, row in data.iterrows():
    if row['Symbol'] != sym :
        sym = row['Symbol']
        avg = 0
        tot = 0
    if row['Action'] == 'Buy' and tot >= 0: # we have some and are buying
        avg = (avg * tot - row['Net Amount']) / (row['Quantity'] + tot)
    if row['Action'] == 'Buy' and tot < 0: # we shoted and are in the process of closing the short
        avg = row['Price'] + row['Commission']
        
    tot = row['Quantity'] + tot
    data.at[index,'average cost'] = avg
    data.at[index, 'total ammount of shares'] = tot
    
    
# sort by date
# data.sort_values(by=['Transaction Date'], ascending=[True], inplace=True)
# remove all buy transactions
# data = data.drop(data[data['Action'] == 'Buy'].index)

CAD = data[(data['Currency'] == 'CAD')]
USD = data[(data['Currency'] == 'USD')]

CAD.to_excel ('CAD.xlsx', index = None) 
USD.to_excel ('USD.xlsx', index = None) 

print(data[['Transaction Date', 'Symbol','Action', 'Quantity', 'Price', 'total ammount of shares', 'average cost']])