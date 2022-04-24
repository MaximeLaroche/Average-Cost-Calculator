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
    def __init__(self, code: str, description: str, currency: str):
        self.codes = [code]
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
        if 'CALL' not in description and 'PUT' not in description:
            return False
        exp = description.split(' ')[2]
        expi: datetime = datetime.datetime.strptime(exp,'%m/%d/%y')
        
        if self.type in description:
            if self.exp == expi:
                for ticker in self.getTicker():
                    if ticker in description:
                        if str(self.strike) in description:
                            self.codes.append(symbol)
                            return True
    
        for code in self.codes:
            if code in description:
                self.codes.append(symbol)
                return True
            if code in symbol:
                return True
        if super().isRightSecurity(symbol, description):
            return True
        return False
        


        