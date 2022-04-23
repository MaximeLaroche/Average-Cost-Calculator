from stock import Stock, ACTIONS, NAMES
from sqlite3 import Date
from typing import Dict
from numpy import number
import pandas as pd
import datetime

class OPTION_NAMES(NAMES):
    strike = 'Strike Price'
    exp = 'Expiry Date'
    type = 'Option Type'
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
    def __init__(self, code: str, description: str, currency: str):
        self.code = code
        self.type: str = description.split(' ')[0]
        ticker = description.split(' ')[1]
        exp = description.split(' ')[2]
        self.exp: datetime = datetime.datetime.strptime(exp,'%m/%d/%y')
        self.strike: number = float(description.split(' ')[3])
        Stock.__init__(self, ticker, currency)
    def getDf(self)->pd.DataFrame:
        return Option.df
    def setDf(self,df: pd.DataFrame):
        Option.df = df
    def getTicker(self) -> str:
        return self.code
    def _getAdjCommision(self, commission: number)-> number:
        return commission/100
    def _add(self, obj: dict):
        obj[OPTION_NAMES.strike] = self.strike
        obj[OPTION_NAMES.exp] = self.exp
        obj[OPTION_NAMES.type] = self.type
        obj[NAMES.ticker] = self.ticker
        obj[NAMES.currency] = self.currency
        obj[NAMES.avg] = self.avg
        obj[NAMES.tot] = self.total
        self.index += 1
        obj[NAMES.index] = self.index
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
    def export():
        Option.df = Option._sort(Option.df)
        Option.df.to_excel('Option.xlsx', index = None) 


        