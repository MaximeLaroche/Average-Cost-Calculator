

from datetime import datetime
from exchangeRate import BankOfCanadaRate
from typing import Dict
from numpy import number
import pandas as pd
import yfinance as yf
from labels import LABELS, ACTIONS_LABELS, DESCRIPTION_LABELS



def initDf() -> pd.DataFrame:
    df = pd.DataFrame(columns=[
        LABELS.date,
        LABELS.action,
        LABELS.price,
        LABELS.ticker,
        LABELS.quantity,
        LABELS.currency,
        LABELS.rate,
        LABELS.id,
        LABELS.description,
        LABELS.index,
        LABELS.avg,
        LABELS.tot,
        LABELS.transactionValue,
        LABELS.averageValue,
        LABELS.profit,
        LABELS.aquisitionCost,
        LABELS.aquisitionRate,
        LABELS.dispotitionValue,
        LABELS.dispositionRate])
    return df

RATE = BankOfCanadaRate()
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
        self.description = ''
        Stock.counter += 1
        self.ticker: str = self._adjTickerName(ticker, currency)
        self.currency = currency
        
        self.prev_date = None
        self._getSplits()
    def _adjTickerName(self, ticker: str, currency: str)-> str:
        ticker = ticker.replace('-U', '') # Disnat currency identification
        if ticker.startswith('.'):
            ticker = ticker.split('.',1)[1] # Questrade bad symbols
        elif ticker.startswith('XTSE:'):
            ticker = ticker.split('XTSE:',1)[1] # Disnat prix de succession entré avec excel
            ticker += '.TO'
        ticker = ticker.replace('.','-') 
        ticker = ticker.replace('-TO', '.TO')
        ticker = ticker.replace('-C', '.TO')
        if(ticker == 'SQQQ1'):
            ticker = 'SQQQ'
        
        return ticker
    def _getSplits(self):
        folder = 'market_data/'
        if 'invalid' in self.ticker or 'H038778' or 'NMX' in self.ticker:
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
                    self.split(ratio)
                    if(self.total != 0):
                        self._add({
                            ACTIONS_LABELS.split: ratio,
                            LABELS.action: ACTIONS_LABELS.split,
                            LABELS.date: splitDateTime,
                            LABELS.avg: self.avg
                        })
            self.prev_date = dateTime
        except:
            pass
        return ratio
    def getTicker(self) ->str:
        return self.ticker
    def _getAdjCommision(self, commission: number)-> number:
        return commission
    def buy(self, quantity: number, price: number, commission: number, date: datetime, description: str):
        self.description = description
        
        self.checkSplits(date)
        quantity = abs(quantity)
        commission = abs(commission)
        commission = self._getAdjCommision(commission)
        price = price + commission/quantity
        if(self.total < 0):
            buyToCloseQty = min(abs(self.total), quantity)
            quantity -= buyToCloseQty
            self._buyToClose(buyToCloseQty, price, date, description)
        if(quantity != 0): # the buy to closde may have put the remaining to 0
            self._updateRate(quantity, price, date)
            self.avg = (self.total * self.avg + price * quantity) / (self.total + quantity)
            self.total += quantity
            data = {
                LABELS.date: date, 
                LABELS.action: ACTIONS_LABELS.buy, 
                LABELS.quantity: quantity, 
                LABELS.price: price,
                LABELS.transactionValue: self.getTransactionTotal(price, quantity),
                LABELS.avg: self.avg
                }
            self._add(data)
    def _buyToClose(self, quantity: number, price: number, date: datetime, description: str):
        self.description = description
        
        quantity = abs(quantity)
        
        self.total += quantity
        data = {
            LABELS.date: date, 
            LABELS.action: ACTIONS_LABELS.buyToClose, 
            LABELS.quantity: quantity, 
            LABELS.price: price, 
            LABELS.transactionValue: self.getTransactionTotal(price, quantity),
            LABELS.profit: self.getProfit(price, self.avg, quantity),
            LABELS.avg: self.avg,
            LABELS.aquisitionCost: self.getTransactionTotal(price, quantity),
            LABELS.aquisitionRate: RATE.getRate(self.currency, date),
            LABELS.dispotitionValue: self.getTransactionTotal(self.avg, quantity),
            LABELS.dispositionRate: self.avgRate
            }
        self._add(data)
    def getTotalOverall(self, quantity)->number:
        return quantity * self.avg
    def getTransactionTotal(self, price: number, quantity: number)-> number:
        return price * quantity
    def getProfit(self, buyPrice: number, sellPrice, quantity: number)->number:
        return quantity * (sellPrice - buyPrice)
    def sell(self, quantity: number, price: number, commission: number, date: datetime, description: str):
        self.description = description
        
        self.checkSplits(date)
        commission = abs(commission)
        quantity = abs(quantity)
        commission = self._getAdjCommision(commission)
        price = price - commission/quantity
        short = False
        shortQty = quantity - self.total
        if(self.total - quantity < 0):
            short = True
            quantity -= shortQty
            
        if(quantity != 0):
            self.total -= quantity
            data = {
                LABELS.date: date, 
                LABELS.action: ACTIONS_LABELS.sell, 
                LABELS.quantity: quantity, 
                LABELS.price: price,
                LABELS.transactionValue: self.getTransactionTotal(price, quantity),
                LABELS.profit: self.getProfit(self.avg, price, quantity),
                LABELS.avg: self.avg,
                LABELS.aquisitionCost: self.getTransactionTotal(self.avg, quantity),
                LABELS.aquisitionRate: self.avgRate,
                LABELS.dispotitionValue: self.getTransactionTotal(price, quantity),
                LABELS.dispositionRate: RATE.getRate(self.currency, date)
                }
            self._add(data)
        if short:
            self._shortSell(shortQty, price, date, description)
    def getDf(self)->pd.DataFrame:
        return Stock.df
    def setDf(self, df: pd.DataFrame):
        Stock.df = df
    def changeTicker(self, newTicker, date):
        oldTicker = self.ticker
        self.ticker = self._adjTickerName(newTicker, self.currency)
        self.description = oldTicker + DESCRIPTION_LABELS.nameChange + self.ticker
        data = {
            LABELS.date: date,
            LABELS.action: ACTIONS_LABELS.nameChange,
        }
        self._add(data)
    def _shortSell(self, quantity: number, price: number, date: datetime, description: str):
        self._updateRate(quantity, price, date)
        self.avg = (self.avg * self.total + quantity * price) / (abs(self.total) + quantity)
        self.description = description
        self.total -= quantity
        data = {
            LABELS.date: date, 
            LABELS.action: ACTIONS_LABELS.shortSell, 
            LABELS.quantity: quantity,
            LABELS.price: price, 
            LABELS.avg: self.avg,
            LABELS.transactionValue: self.getTransactionTotal(price, quantity)
            }
        self._add(data)
    def _add(self, obj: Dict):
        obj[LABELS.ticker] = self.ticker
        obj[LABELS.tot] = self.total
        obj[LABELS.currency] = self.currency
        self.index += 1
        obj[LABELS.description] = self.description
        obj[LABELS.index] = self.index
        obj[LABELS.id] = self.id
        obj[LABELS.rate] = self.avgRate

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

        df.sort_values(by=[LABELS.id, LABELS.date, LABELS.index], ascending=[True,True, True], inplace=True)
        return df
    def sort()-> pd.DataFrame:
        return Stock._sort(Stock.df)
    def isRightSecurity(self, symbol: str, description: str)->bool:
        if symbol in self.ticker or self._adjTickerName(symbol, self.currency) in self.ticker:
            return True
        return False
    def _updateRate(self, quantity: number, price: number, date: datetime):
        rate = RATE.getRate(self.currency, date)
        total = abs(self.total)
        quantity = abs(quantity)
        if (self.avg * total + quantity * price) == 0:
            print('Debug')
        self.avgRate = (self.avgRate * self.avg * total + rate * quantity * price) / (self.avg * total + quantity * price)

    
