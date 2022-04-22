

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
    quantity = 'Quantity'
    avg = 'Average cost'
    tot = 'Total Amount of shares'


def initDf() -> pd.DataFrame:
    df = pd.DataFrame(columns=[NAMES.date, NAMES.action, NAMES.price, NAMES.quantity, NAMES.avg, NAMES.tot])
    return df


df = initDf()
class Security:
    df = initDf()
    def __init__(self, ticker: str):
        self.avg = 0
        self.total = 0
        self.ticker = ticker
    def _getAdjCommision(self, commision: number)-> number:
        return 0
        pass
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
            NAMES.avg: self.avg, 
            NAMES.tot: self.total
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
            NAMES.avg: self.avg, 
            NAMES.tot: self.total
            }
        self._add(data)
    def _add(self, obj: Dict):
        Security.df = pd.concat(
            [
                Security.df, 
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
