

from sqlite3 import Date
from typing import Dict
from numpy import number
import pandas as pd

class ACTIONS:
    buy = 'Buy'
    sell = 'Sell'
    split = 'split'

class NAMES:
    date = 'Date'
    action = 'Action'
    price = 'Price'
    ticker = 'Symbol'
    quantity = 'Quantity'
    avg = 'Average cost'
    tot = 'Total Amount of shares'


def initDf() -> pd.DataFrame:
    df = pd.DataFrame(columns=[
        NAMES.date, 
        NAMES.action, 
        NAMES.ticker ,
        NAMES.price, 
        NAMES.quantity, 
        NAMES.avg, 
        NAMES.tot])
    return df


df = initDf()
class Stock:
    df = initDf()
    def __init__(self, ticker: str):
        self.avg: number = 0
        self.total: number = 0
        self.ticker: str = ticker
    def _getAdjCommision(self, commission: number)-> number:
        return commission
    def buy(self, quantity: number, price: number, commission: number, date: Date):
        commission = self._getAdjCommision(commission)
        price = price + commission/quantity
        self.avg = (self.total * self.avg + price * quantity) / (self.total + quantity)
        self.total += quantity
        data = {
            NAMES.date: date, 
            NAMES.action: ACTIONS.buy, 
            NAMES.quantity: quantity, 
            NAMES.price: price, 
            }
        self._add(data)

    def sell(self, quantity: number, price: number, commission: number, date: Date):
        commission = self._getAdjCommision(commission)
        price = price - commission/quantity
        
        self.total += quantity
        data = {
            NAMES.date: date, 
            NAMES.action: ACTIONS.sell, 
            NAMES.quantity: quantity, 
            NAMES.price: price, 
            }
        self._add(data)
    def _add(self, obj: Dict):
        obj[NAMES.ticker] = self.ticker
        obj[NAMES.avg] = self.avg
        obj[NAMES.tot] = self.total
        
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
