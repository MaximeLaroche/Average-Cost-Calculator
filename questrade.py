import json
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
from CostBasis import *


data = pd.read_excel("questrade.xlsx", sheet_name="Activities")
data["Transaction Date"] = data["Transaction Date"].apply(
    lambda date: datetime.strptime(date, "%Y-%m-%d %H:%M:%S %p")
)

data = filter.removeBadData(data)
data.sort_values(by=["Transaction Date"], ascending=[True], inplace=True)


stocks = [Stock("invalid", "CAD")]
options = [Option("invalid", "CAD", "CALL", "invalid", datetime.now(), 0)]


def extractOptionParams(description: str, currency: str):
    type: str = description.split(" ")[0]
    ticker = description.split(" ")[1]
    expString = description.split(" ")[2]
    try:
        exp: datetime = datetime.strptime(expString, "%m/%d/%y")
    except:
        print("except in ", expString)
    strike: number = float(description.split(" ")[3])
    return ticker, strike, type, exp


def makeOption(symbol: str, description: str, currency: str) -> Option:
    ticker, strike, type, exp = extractOptionParams(description, currency)
    if "SQQQ" in ticker and exp.date() == datetime(2022, 6, 17).date():
        error_message = "There was a reverse split on SQQQ stock, but not the option. The underlying symbol changed so the system does not recognise the transactions from before and after the sotck split to be from the same security. You must calculate your profits and losses manually by looking at the transactions values in 'QuestradeOptions.xslx"
        print("-------------------------------------")
        print(error_message)
        print(f"{ticker}\t{strike}\t{type}\t{exp}")
    option = Option(symbol, currency, type, ticker, exp, strike)
    return option


def getOption(
    symbol: str, description, currency: str, transactionDate: datetime
) -> Option:
    ticker, strike, type, exp = extractOptionParams(description, currency)
    for item in options:
        if item.isRightOption(ticker, strike, exp, type, transactionDate, symbol, currency):
            item.isRightOption(ticker, strike, exp, type, transactionDate, symbol, currency)
            return item

    secu = makeOption(symbol, description, currency)
    options.append(secu)

    return secu


def getStock(symbol: str, description, currency: str) -> Stock:
    for item in stocks:
        if item.isRightSecurity(symbol, currency):
            item.isRightSecurity(symbol, currency)
            return item

    secu = Stock(symbol, currency)
    stocks.append(secu)
    return secu


type = ""
for index, row in data.iterrows():
    if "PUT" in row["Description"] or (
        "CALL" in row["Description"]
        and "BMO COVERED CALL UTILITIES ETF" not in row["Description"]
    ):
        type = "Option"
    else:
        type = "Stock"
    date = row["Transaction Date"]
    if date.year == 2023:
        print("2023")
    if type == "Option":
        if row["Action"] == "Buy":
            option = getOption(row["Symbol"], row["Description"], row["Currency"], date)
            option.buy(
                row["Quantity"],
                row["Price"],
                row["Commission"],
                date,
                row["Description"],
            )
        elif row["Action"] == "Sell":
            option = getOption(row["Symbol"], row["Description"], row["Currency"], date)
            option.sell(
                row["Quantity"],
                row["Price"],
                row["Commission"],
                date,
                row["Description"],
            )
        elif row["Action"] == "ADJ":
            option = getOption(row["Symbol"], row["Description"], row["Currency"], date)
            newSym = row["Description"].split(" ")[-1]
            symbols = [row["Symbol"], newSym]
            option.addSymbols(symbols)
        elif row["Action"] == "EXP":
            option = getOption(row["Symbol"], row["Description"], row["Currency"], date)
            option.expire(row["Quantity"], date, row["Description"])
        elif row["Action"] == "ASN":
            option = getOption(row["Symbol"], row["Description"], row["Currency"], date)
            option.assign(row["Quantity"], date, row["Description"])
        else:
            print("not processed", row)
    elif type == "Stock":
        if row["Action"] == "Buy":
            option = getStock(row["Symbol"], row["Description"], row["Currency"])
            option.buy(
                row["Quantity"],
                row["Price"],
                row["Commission"],
                date,
                row["Description"],
            )
        elif row["Action"] == "Sell":
            option = getStock(row["Symbol"], row["Description"], row["Currency"])
            option.sell(
                row["Quantity"],
                row["Price"],
                row["Commission"],
                date,
                row["Description"],
            )
        elif row["Action"] == "CON" and row["Activity Type"] == "Withdrawals" and row["Symbol"] is not np.nan: 
            # Made a contribution to another account so basically transfered money or securities to another account. Can consider it as selling
            # Check if there is a symbol. When only money is transfered, no symbol and also not relevant/taxable
            option = getStock(row["Symbol"], row["Description"], row["Currency"])
            value = float(row["Description"].split("BOOK VALUE $")[1].replace(",",""))
            row["Price"] = abs(value/row["Quantity"])
            option.sell(
                row["Quantity"],
                row["Price"],
                row["Commission"],
                date,
                row["Description"],
            )
        else:
            print("not processed", row)

        calc_cost_basis(date, stocks, stocks)

with open("costs_basis.json", 'w') as file:
    json.dump(snapshots, file, indent=4, default=str)
export("Questrade")
