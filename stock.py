

from datetime import datetime
from sqlite3 import Date
from tabnanny import check
from typing import Dict
from numpy import number, short
import pandas as pd
import yfinance as yf

class ACTIONS:
    buy = 'Buy'
    buyToClose = 'Buy to close'
    sell = 'Sell'
    shortSell = 'Short sell'
    split = 'split'

class NAMES:
    date = 'Date'
    action = 'Action'
    price = 'Price'
    ticker = 'Symbol'
    quantity = 'Quantity'
    index = 'Index'
    avg = 'Average cost'
    tot = 'Total Amount of shares'


def initDf() -> pd.DataFrame:
    df = pd.DataFrame(columns=[
        NAMES.date, 
        NAMES.action, 
        NAMES.ticker ,
        NAMES.price, 
        NAMES.index,
        NAMES.quantity, 
        NAMES.avg, 
        NAMES.tot])
    return df


df = initDf()
class Stock:
    index: number = 0
    df = initDf()
    def __init__(self, ticker: str):
        self.avg: number = 0
        self.total: number = 0
        self.ticker: str = ticker
        self.prev_date = None
        self._getSplits()
    def _getSplits(self):
        ticker = yf.Ticker(self.ticker)
        self.splits = ticker.splits
    def checkSplits(self, date: Date)->number:
        ratio = 1
        dateTime = datetime.strptime(date, '%Y-%m-%d')
        if self.prev_date is None:
            self.prev_date = dateTime
            return ratio
        for i in range(len(self.splits)):
            splitDate = datetime.strptime(str(self.splits.index[i]), '%y-%m-%d')
            if self.prev_date <= splitDate <= dateTime:
                ratio = self.splits[i]
                avg /= ratio
                tot *= ratio
                self._add({
                    ACTIONS.split: ratio,
                    NAMES.date: self.splits.index[i]
                })
                return ratio

        return ratio
    def getTicker(self) ->str:
        return self.ticker
    def _getAdjCommision(self, commission: number)-> number:
        return commission
    def buy(self, quantity: number, price: number, commission: number, date: Date):
        self.checkSplits(date)
        quantity = abs(quantity)
        commission = abs(commission)
        commission = self._getAdjCommision(commission)
        price = price + commission/quantity
        if(self.total < 0):
            buyToCloseQty = min(abs(self.total), quantity)
            quantity -= buyToCloseQty
            self._buyToClose(buyToCloseQty, price, date)
        if(quantity != 0): # the buy to closde may have put the remaining to 0
            self.avg = (self.total * self.avg + price * quantity) / (self.total + quantity)
            self.total += quantity
            data = {
                NAMES.date: date, 
                NAMES.action: ACTIONS.buy, 
                NAMES.quantity: quantity, 
                NAMES.price: price, 
                }
            self._add(data)
    def _buyToClose(self, quantity: number, price: number, date: Date):
        quantity = abs(quantity)
        self.avg = price
        self.total += quantity
        data = {
            NAMES.date: date, 
            NAMES.action: ACTIONS.buyToClose, 
            NAMES.quantity: quantity, 
            NAMES.price: price, 
            }
        self._add(data)
    def sell(self, quantity: number, price: number, commission: number, date: Date):
        self.checkSplits(date)
        commission = abs(commission)
        quantity = abs(quantity)
        commission = self._getAdjCommision(commission)
        price = price - commission/quantity
        if(self.total - quantity < 0):
            shortQty = quantity - self.total
            quantity -= shortQty
            self._shortSell(shortQty, price, date)
        if(quantity != 0):
            self.total -= quantity
            data = {
                NAMES.date: date, 
                NAMES.action: ACTIONS.sell, 
                NAMES.quantity: quantity, 
                NAMES.price: price, 
                }
            self._add(data)
    def _shortSell(self, quantity: number, price: number, date: Date):
        self.total -= quantity
        data = {
            NAMES.date: date, 
            NAMES.action: ACTIONS.shortSell, 
            NAMES.quantity: quantity, 
            NAMES.price: price, 
            }
        self._add(data)
    def _add(self, obj: Dict):
        obj[NAMES.ticker] = self.ticker
        obj[NAMES.avg] = self.avg
        obj[NAMES.tot] = self.total
        self.index += 1
        obj[NAMES.index] = self.index
        Stock.df = pd.concat(
            [
                Stock.df, 
                pd.DataFrame.from_records(
                    [
                        obj
                    ]
                )
            ]
        )
    def split(self, ratio: number):
        self.avg /= ratio
        self.total *= ratio
    def _sort(df: pd.DataFrame)-> pd.DataFrame:
        df.sort_values(by=[NAMES.ticker, NAMES.date, NAMES.index], ascending=[True,True, True], inplace=True)
        return df
    def export():
        Stock.df = Stock._sort(Stock.df)
        Stock.df.to_excel('Stocks.xlsx', index = None) 

    
