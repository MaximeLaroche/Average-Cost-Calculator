from datetime import datetime
import pandas as pd
import yfinance as yf

class ExchangeRate:
    YEARLY = 'y'
    DAILY = 'd'
    def __init__(self, currency = 'USDCAD=X') -> None:
        folder = 'market_data/'
        self.currency = currency

        try:
            df = pd.read_csv(folder + self.currency + '.csv', index_col='Date')
            self.data = df
        except:
            ticker = yf.Ticker(self.currency)
            try:
                prices = ticker.history(period='max')['Close']
                print(prices)
                df = pd.DataFrame(prices, index=prices.index)
                self.data = df
                df.to_csv(folder + self.currency + '.csv', index=True)
            except Exception as e:
                print(e)
                print("error getting currency data for " + self.currency)
    def getRate(self, currency: str, date: datetime, precision = YEARLY):
        if currency == 'CAD':
            return 1
        if precision == ExchangeRate.YEARLY:
            return self._getYearlyRate(date)
        if precision == ExchangeRate.DAILY:
            return self._getDailyRate(date)
        raise Exception("Invalid precision in exchange rate. use ExchangeRate.DAILY or ExchangeRate.YEARLY as precision")
    def _getDailyRate(self, date: datetime):
        rate = self.data.loc[str(date.date()),'Close']
        return rate

    def _getYearlyRate(self, date: datetime):
        endOfYear = datetime(year=date.year, month=12, day=31)
        rate = self.data.loc[str(endOfYear.date()),'Close']
        return rate
