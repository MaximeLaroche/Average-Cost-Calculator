

from datetime import datetime
from exchangeRate import ExchangeRate
from typing import Dict
from numpy import number
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
    currency = 'Currency'
    rate = 'Exchange rate'
    id = 'ID'
    description = 'Description'
    index = 'Index'
    avg = 'Average position price'
    tot = 'Total Amount of shares'


def initDf() -> pd.DataFrame:
    df = pd.DataFrame(columns=[
        NAMES.date, 
        NAMES.action, 
        NAMES.ticker ,
        NAMES.price, 
        NAMES.index,
        NAMES.quantity, 
        NAMES.description,
        NAMES.currency,
        NAMES.avg, 
        NAMES.tot])
    return df

RATE = ExchangeRate()
class Stock:
    index: number = 0
    counter: number = 0
    df = initDf()
    def __init__(self, ticker: str, currency: str):
        self.avgRate: number = 1
        self.avg: number = 0
        self.avgShort: number = 0
        self.total: number = 0
        self.id = Stock.counter
        Stock.counter += 1
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
                    if(self.total != 0):
                        self._add({
                            ACTIONS.split: ratio,
                            NAMES.action: ACTIONS.split,
                            NAMES.date: splitDateTime,
                            NAMES.avg: self.avg
                        })
            self.prev_date = dateTime
        except:
            pass
        return ratio
    def getTicker(self) ->str:
        return self.ticker
    def _getAdjCommision(self, commission: number)-> number:
        return commission
    def buy(self, quantity: number, price: number, commission: number, date: str, description: str):
        self.description = description
        dateTime = datetime.strptime(date, '%Y-%m-%d %H:%M:%S %p')
        self.checkSplits(dateTime)
        quantity = abs(quantity)
        commission = abs(commission)
        commission = self._getAdjCommision(commission)
        price = price + commission/quantity
        if(self.total < 0):
            buyToCloseQty = min(abs(self.total), quantity)
            quantity -= buyToCloseQty
            self._buyToClose(buyToCloseQty, price, date, description)
        if(quantity != 0): # the buy to closde may have put the remaining to 0
            self._updateRate(quantity, price, dateTime)
            self.avg = (self.total * self.avg + price * quantity) / (self.total + quantity)
            self.total += quantity
            data = {
                NAMES.date: dateTime, 
                NAMES.action: ACTIONS.buy, 
                NAMES.quantity: quantity, 
                NAMES.price: price,
                NAMES.avg: self.avg
                }
            self._add(data)
    def _buyToClose(self, quantity: number, price: number, date: str, description: str):
        self.description = description
        dateTime = datetime.strptime(date, '%Y-%m-%d %H:%M:%S %p')
        quantity = abs(quantity)
        
        self.total += quantity
        data = {
            NAMES.date: dateTime, 
            NAMES.action: ACTIONS.buyToClose, 
            NAMES.quantity: quantity, 
            NAMES.price: self.avg, 
            NAMES.avg: price
            }
        self._add(data)
    def sell(self, quantity: number, price: number, commission: number, date: str, description: str):
        self.description = description
        dateTime = datetime.strptime(date, '%Y-%m-%d %H:%M:%S %p')
        self.checkSplits(dateTime)
        commission = abs(commission)
        quantity = abs(quantity)
        commission = self._getAdjCommision(commission)
        price = price - commission/quantity
        if(self.total - quantity < 0):
            shortQty = quantity - self.total
            quantity -= shortQty
            self._shortSell(shortQty, price, date, description)
        if(quantity != 0):
            self.total -= quantity
            data = {
                NAMES.date: dateTime, 
                NAMES.action: ACTIONS.sell, 
                NAMES.quantity: quantity, 
                NAMES.price: price,
                NAMES.avg: self.avg
                }
            self._add(data)
    def getDf(self)->pd.DataFrame:
        return Stock.df
    def setDf(self, df: pd.DataFrame):
        Stock.df = df
    def _shortSell(self, quantity: number, price: number, date: str, description: str):
        dateTime = datetime.strptime(date, '%Y-%m-%d %H:%M:%S %p')
        self._updateRate(quantity, price, dateTime)
        self.avg = (self.avg * self.total + quantity * price) / (abs(self.total) + quantity)
        self.description = description
        self.total -= quantity
        data = {
            NAMES.date: dateTime, 
            NAMES.action: ACTIONS.shortSell, 
            NAMES.quantity: quantity,
            NAMES.price: price, 
            NAMES.avg: self.avg
            }
        self._add(data)
    def _add(self, obj: Dict):
        obj[NAMES.ticker] = self.ticker
        obj[NAMES.tot] = self.total
        obj[NAMES.currency] = self.currency
        self.index += 1
        obj[NAMES.index] = self.index
        obj[NAMES.id] = self.id
        obj[NAMES.rate] = self.avgRate
        df = self.getDf()
        df = pd.concat(
            [
                df, 
                pd.DataFrame.from_records(
                    [
                        obj
                    ]
                )
            ]
        )
        self.setDf(df)
        
    def split(self, ratio: number):
        self.avg /= ratio
        self.total *= ratio
    def _sort(df: pd.DataFrame)-> pd.DataFrame:
        df.sort_values(by=[NAMES.ticker, NAMES.date, NAMES.index], ascending=[True,True, True], inplace=True)
        return df
    def export():
        Stock.df = Stock._sort(Stock.df)
        Stock.df.to_excel('Stocks.xlsx', index = None)
    def isRightSecurity(self, symbol: str, description: str)->bool:
        if symbol in self.ticker:
            return True
        if self._adjTickerName(symbol, self.currency) in self.ticker:
            return True
        return False
    def _updateRate(self, quantity: number, price: number, date: datetime):
        rate = RATE.getRate(self.currency, date)
        self.avgRate = (self.avgRate * self.avg * self.total + rate * quantity * price) / (self.avg * self.total + quantity * price)

    
