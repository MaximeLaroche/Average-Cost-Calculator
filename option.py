
from stock import Stock
from sqlite3 import Date
from typing import Dict
from numpy import number
import pandas as pd
from datetime import datetime
import re
from labels import DESCRIPTION_LABELS, OPTION_LABELS, LABELS, ACTIONS_LABELS

def initDf() -> pd.DataFrame:
    df = pd.DataFrame(columns=[
        LABELS.date, LABELS.action, LABELS.ticker, LABELS.description, LABELS.quantity, LABELS.aquisitionCost,LABELS.aquisitionRate, LABELS.dispotitionValue, LABELS.dispositionRate, OPTION_LABELS.exp, OPTION_LABELS.strike, LABELS.price, LABELS.transactionValue,LABELS.avg, LABELS.tot, LABELS.profit,LABELS.currency, LABELS.rate, LABELS.id, LABELS.index, ACTIONS_LABELS.split])
    return df

class Option(Stock):
    df = initDf()
    def __init__(self, code: str, currency: str, type: str, ticker: str, exp: datetime, strike: number):
        if ticker == 'FB':
            ticker = 'META'
        self.splitDates = []
        self.codes = [code]
        self.currency = currency
        self.type = type
        self.ticker = ticker
        if(exp.year < 100):
            exp = datetime(year = 2000 + exp.year, month=exp.month, day=exp.day)
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
        obj[OPTION_LABELS.strike] = self.strike
        obj[OPTION_LABELS.exp] = self.exp
        obj[OPTION_LABELS.type] = self.type
        obj[OPTION_LABELS.codes] = self.codes
        
        super()._add(obj)
    def export():
        Option.df = Option._sort(Option.df)
        Option.df.to_excel('Option.xlsx', index = None) 

    def isRightSecurity(self, symbol: str, description: str)->bool:

        for code in self.codes:
            if code == symbol or code in description:
                return True
        
        return False
    def isRightOption(self, ticker: str, strike: number, exp: datetime, type: str, transactionDate: datetime, symbol: str):
        self.checkSplits(transactionDate)
        if (self.ticker == ticker or self.ticker == self._adjTickerName(ticker, self.currency)) and self.strike == strike and self.exp == exp and self.type == type or symbol in self.codes:
            return True
        return False
   
    def split(self, ratio: number):
        self.strike /= ratio
        super().split(ratio)
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

    def maybeExpire(self, date: datetime):
        """
        Disnat odes not have an "expire" signal. So, at the end of iteration (last possible date), we check if options were not manually closed and past their expiration date. If so, we make them "expire"
        """
        if self.total != 0 and date > self.exp:
            self.expire(self.total, self.exp, self.description)
    def expire(self, quantity: number, date: datetime, description: str):
        quantity = abs(quantity)
        price = 0
        commission = 0
        description = DESCRIPTION_LABELS.expiration + self.description
        if(self.total > 0):
            self.sell(quantity, price,commission, date, description)
        elif(self.total < 0):
            self.buy(quantity,price, 0, date,description)
    def assign(self, quantity: number, date: datetime, description: str):
        self.expire(quantity, date, description)


        