from datetime import datetime
import pandas as pd
import yfinance as yf

class ExchangeRate:
    YEARLY = 'FXAUSDCAD'
    DAILY = 'FXUSDCAD'
    _YEARLY_FILE_NAME = 'FX_RATES_ANNUAL.csv'
    _DAILY_FILE_NAME = 'FX_RATES_DAILY.csv'
    def __init__(self, dailyLabel = 'FXUSDCAD', yearlyLabel = 'FXAUSDCAD') -> None:
        folder = 'market_data/'
        self.dailyLabel = dailyLabel
        self.yearlyLabel = yearlyLabel

        try:
            self.daily = pd.read_csv(folder + ExchangeRate._DAILY_FILE_NAME, index_col='date')
            self.yearly = pd.read_csv(folder + ExchangeRate._YEARLY_FILE_NAME, index_col='date')
        except Exception as e:
            raise e
        
    def getRate(self, currency: str, date: datetime, precision = DAILY):
        if currency == 'CAD':
            return 1
        if precision == ExchangeRate.YEARLY:
            return self._getYearlyRate(date)
        if precision == ExchangeRate.DAILY:
            return self._getDailyRate(date)
        raise Exception("Invalid precision in exchange rate. use ExchangeRate.DAILY or ExchangeRate.YEARLY as precision")
    def _getDailyRate(self, date: datetime):
        rate = self.daily.loc[str(date.date()),self.dailyLabel]
        return rate

    def _getYearlyRate(self, date: datetime):
        beginingOfYear = datetime(year=date.year, month=1, day=1)
        if beginingOfYear.year >= datetime.now().year:
            return self._getDailyRate(date)
        rate = self.yearly.loc[str(beginingOfYear.date()),self.yearlyLabel]
        return rate

d = datetime(year=2021, month=5, day=4)
x=ExchangeRate()
print(x.getRate('USD', d, precision=ExchangeRate.DAILY))
print(x.getRate('USD', d, precision=ExchangeRate.YEARLY))
d = datetime(year=2022, month=3, day=4)
print(x.getRate('USD', d, precision=ExchangeRate.DAILY))
print(x.getRate('USD', d, precision=ExchangeRate.YEARLY))
