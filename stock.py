

from datetime import datetime
from sqlite3 import Date
from tabnanny import check
from typing import Dict, List
from numpy import number, short
import pandas as pd
import yfinance as yf
import csv

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
    def __init__(self, ticker: str, currency: str):
        self.avg: number = 0
        self.total: number = 0
        self.ticker: str = self._adjTickerName(ticker, currency)
        self.currency = currency
        
        self.prev_date = None
        self._getSplits()
    def _adjTickerName(self, ticker: str, currency: str)-> str:
        if(ticker.startswith('.')):
            ticker = ticker.split('.',1)[1]
        ticker = ticker.replace('.','-')
        ticker = ticker.replace('-TO', '.TO')
        if(ticker == 'SQQQ1'):
            ticker = 'SQQQ'
        
        return ticker
    def _getSplits(self):
        folder = 'market_data/'
        if 'invalid' in self.ticker:
            return
        try:
            df = pd.read_csv(folder + self.ticker + '.csv')
            self.splits = df
            
        except:
            ticker = yf.Ticker(self.ticker)
            try:
                df = pd.DataFrame(ticker.splits, index=ticker.splits.index)
                self.splits = df
                df.to_csv(folder + self.ticker + '.csv', index=True)
            except Exception as e:
                print(e)
                print("error getting splits for " + self.ticker)
    def checkSplits(self, dateTime: datetime)->number:
        ratio = 1
        try:    
            if self.prev_date is None:
                self.prev_date = dateTime
                return ratio
            for index, row in self.splits.iterrows():
                splitDate = row['Date']
                splitDateTime = datetime.strptime(splitDate, '%Y-%m-%d')
                if self.prev_date <= splitDateTime <= dateTime:
                    ratio = row['Stock Splits']
                    self.avg /= ratio
                    self.total *= ratio
                    self._add({
                        ACTIONS.split: ratio,
                        NAMES.action: ACTIONS.split,
                        NAMES.date: splitDateTime
                    })
                    return ratio
        except:
            pass
        return ratio
    def getTicker(self) ->str:
        return self.ticker
    def _getAdjCommision(self, commission: number)-> number:
        return commission
    def buy(self, quantity: number, price: number, commission: number, date: str):
        dateTime = datetime.strptime(date, '%Y-%m-%d %H:%M:%S %p')
        self.checkSplits(dateTime)
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
                NAMES.date: dateTime, 
                NAMES.action: ACTIONS.buy, 
                NAMES.quantity: quantity, 
                NAMES.price: price, 
                }
            self._add(data)
    def _buyToClose(self, quantity: number, price: number, date: str):
        dateTime = datetime.strptime(date, '%Y-%m-%d %H:%M:%S %p')
        quantity = abs(quantity)
        self.avg = price
        self.total += quantity
        data = {
            NAMES.date: dateTime, 
            NAMES.action: ACTIONS.buyToClose, 
            NAMES.quantity: quantity, 
            NAMES.price: price, 
            }
        self._add(data)
    def sell(self, quantity: number, price: number, commission: number, date: str):
        dateTime = datetime.strptime(date, '%Y-%m-%d %H:%M:%S %p')
        self.checkSplits(dateTime)
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
                NAMES.date: dateTime, 
                NAMES.action: ACTIONS.sell, 
                NAMES.quantity: quantity, 
                NAMES.price: price, 
                }
            self._add(data)
    def _shortSell(self, quantity: number, price: number, date: str):
        self.total -= quantity
        dateTime = datetime.strptime(date, '%Y-%m-%d %H:%M:%S %p')
        data = {
            NAMES.date: dateTime, 
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

    
