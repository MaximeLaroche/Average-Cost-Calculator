from datetime import datetime
import pandas as pd
import yfinance as yf








class YahooRate:
    YEARLY = 'FXAUSDCAD'
    DAILY = 'FXUSDCAD'
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
    def getRate(self, currency: str, date: datetime, precision = DAILY):
        if currency == 'CAD':
            return 1
        if precision == YahooRate.YEARLY:
            return self._getYearlyRate(date)
        if precision == YahooRate.DAILY:
            return self._getDailyRate(date)
        raise Exception("Invalid precision in exchange rate. use ExchangeRate.DAILY or ExchangeRate.YEARLY as precision")
    def _getDailyRate(self, date: datetime):
        rate = self.data.loc[str(date.date()),'Close']
        return rate

    def _getYearlyRate(self, date: datetime):
        endOfYear = datetime(year=date.year, month=12, day=31)
        if endOfYear > date:
            endOfYear = date
        rate = self.data.loc[str(endOfYear.date()),'Close']
        return rate


class BankOfCanadaRate:
    YEARLY = 'FXAUSDCAD'
    DAILY = 'FXUSDCAD'
    _YEARLY_FILE_NAME = 'FX_RATES_ANNUAL.csv'
    _DAILY_FILE_NAME = 'FX_RATES_DAILY.csv'
    backupRate = YahooRate()
    def __init__(self, dailyLabel = 'FXUSDCAD', yearlyLabel = 'FXAUSDCAD') -> None:
        folder = 'market_data/'
        self.dailyLabel = dailyLabel
        self.yearlyLabel = yearlyLabel

        try:
            self.daily = pd.read_csv(folder + BankOfCanadaRate._DAILY_FILE_NAME, index_col='date')
            self.yearly = pd.read_csv(folder + BankOfCanadaRate._YEARLY_FILE_NAME, index_col='date')
        except Exception as e:
            raise e
        
    def getRate(self, currency: str, date: datetime, precision = DAILY):
        if currency == 'CAD':
            return 1
        try:
            if precision == BankOfCanadaRate.YEARLY:
                return self._getYearlyRate(date)
            if precision == BankOfCanadaRate.DAILY:
                return self._getDailyRate(date)
        except:
            return self.backupRate.getRate(currency, date, precision)
    def _getDailyRate(self, date: datetime):
        rate = self.daily.loc[str(date.date()),self.dailyLabel]
        return rate

    def _getYearlyRate(self, date: datetime):
        beginingOfYear = datetime(year=date.year, month=1, day=1)
        if beginingOfYear.year >= datetime.now().year:
            return self._getDailyRate(date)
        rate = self.yearly.loc[str(beginingOfYear.date()),self.yearlyLabel]
        return rate


