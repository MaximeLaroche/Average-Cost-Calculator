
from stock import Stock, ACTIONS, NAMES
from sqlite3 import Date
from typing import Dict
from numpy import number
import pandas as pd
from datetime import datetime
import re

class OPTION_NAMES(NAMES):
    strike = 'Strike Price'
    exp = 'Expiry Date'
    type = 'Option Type'
    codes = 'Other symbols'
def initDf() -> pd.DataFrame:
    df = pd.DataFrame(columns=[
        NAMES.date, 
        NAMES.action, 
        NAMES.ticker,
        OPTION_NAMES.type,
        OPTION_NAMES.strike,
        OPTION_NAMES.exp,
        NAMES.currency,
        NAMES.price, 
        NAMES.quantity, 
        NAMES.avg, 
        NAMES.tot])
    return df

class Option(Stock):
    df = initDf()
    def __init__(self, code: str, currency: str, type: str, ticker: str, exp: datetime, strike: number):
        self.splitDates = []
        self.codes = [code]
        self.currency = currency
        self.type = type
        self.ticker = ticker
        self.exp = exp
        self.strike = strike
        Stock.__init__(self, ticker, currency)
    def getDf(self)->pd.DataFrame:
        return Option.df
    def setDf(self,df: pd.DataFrame):
        Option.df = df
    def getTicker(self) -> str:
        return self.codes
    def _getAdjCommision(self, commission: number)-> number:
        return commission/100
    def _add(self, obj: dict):
        obj[OPTION_NAMES.strike] = self.strike
        obj[OPTION_NAMES.exp] = self.exp
        obj[OPTION_NAMES.type] = self.type
        obj[OPTION_NAMES.codes] = self.codes
        
        super()._add(obj)
    def export():
        Option.df = Option._sort(Option.df)
        Option.df.to_excel('Option.xlsx', index = None) 

    def isRightSecurity(self, symbol: str, description: str)->bool:

        for code in self.codes:
            if code == symbol or code in description:
                return True
        
        return False
    def checkSplits(self, dateTime: datetime)->number:
        return 1
    def getTotalOverall(self, quantity: number)->number:
        return 100 * super().getTotalOverall(quantity)
    def getTransactionTotal(self, price: number, quantity: number)-> number:
        return 100 * super().getTransactionTotal(price, quantity)
    def getProfit(self, buyPrice: number, sellPrice, quantity: number)->number:
        return 100 * super().getProfit(buyPrice, sellPrice, quantity)
    def sort()-> pd.DataFrame:
        return Option._sort(Option.df)

    def addSymbols(self, symbols):
        for symbol in symbols:
            self.codes.append(symbol)
        self.codes = sorted(set(self.codes))
    def adj(self,date: datetime, description: str, ratio: number):
            
        if date not in self.splitDates:
            self.splitDates.append(date)
            
            self.avg /= ratio
            self.total *= ratio
            self.strike /= ratio
            self._add({
                NAMES.date: date,
                ACTIONS.split: ratio,
                NAMES.action: ACTIONS.split,
                NAMES.description: description,
                OPTION_NAMES.strike: self.strike
            })

    def expire(self, quantity: number, date: datetime, description: str):
        quantity = abs(quantity)
        price = 0
        commission = 0
        if(self.total > 0):
            self.sell(quantity, price,commission, date, description)
        elif(self.total < 0):
            self._buyToClose(quantity,price,date,description)
    def assign(self, quantity: number, date: datetime, description: str):
        self.expire(quantity, date, description)


        