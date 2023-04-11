from datetime import datetime
import pandas as pd
import yfinance as yf
import requests
import os

folder = "market_data"
if not os.path.exists(folder):
    os.makedirs(folder)


class YahooRate:
    YEARLY = "FXAUSDCAD"
    DAILY = "FXUSDCAD"

    def __init__(self, currency="USDCAD=X") -> None:
        folder = "market_data/"
        self.currency = currency

        try:
            df = pd.read_csv(folder + self.currency + ".csv", index_col="Date")
            self.data = df
        except:
            ticker = yf.Ticker(self.currency)
            try:
                prices = ticker.history(period="max")["Close"]
                df = pd.DataFrame(prices, index=prices.index)
                self.data = df
                df.to_csv(folder + self.currency + ".csv", index=True)
            except Exception as e:
                print(e)
                print("error getting currency data for " + self.currency)

    def getRate(self, currency: str, date: datetime, precision=DAILY):
        if currency == "CAD":
            return 1
        if precision == YahooRate.YEARLY:
            return self._getYearlyRate(date)
        if precision == YahooRate.DAILY:
            return self._getDailyRate(date)
        raise Exception(
            "Invalid precision in exchange rate. use ExchangeRate.DAILY or ExchangeRate.YEARLY as precision"
        )

    def _getDailyRate(self, date: datetime):
        rate = self.data.loc[str(date.date()), "Close"]
        return rate

    def _getYearlyRate(self, date: datetime):
        endOfYear = datetime(year=date.year, month=12, day=31)
        if endOfYear > date:
            endOfYear = date
        rate = self.data.loc[str(endOfYear.date()), "Close"]
        return rate


class BankOfCanadaRate:
    YEARLY = "FXAUSDCAD"
    DAILY = "FXUSDCAD"
    _YEARLY_FILE_NAME = "FX_RATES_ANNUAL.csv"
    _DAILY_FILE_NAME = "FX_RATES_DAILY.csv"
    _DAILY_URL = (
        "https://www.banqueducanada.ca/valet/observations/group/FX_RATES_DAILY/csv"
    )
    _YEARLY_URL = (
        "https://www.banqueducanada.ca/valet/observations/group/FX_RATES_ANNUAL/csv"
    )
    backupRate = YahooRate()
    folder = "market_data/"

    def __init__(self, dailyLabel="FXUSDCAD", yearlyLabel="FXAUSDCAD") -> None:
        self.dailyLabel = dailyLabel
        self.yearlyLabel = yearlyLabel

        try:
            self.readFiles()
        except Exception as e:
            self.fetchFromURL()

    def readFiles(self):
        self.daily = pd.read_csv(
            BankOfCanadaRate.folder + BankOfCanadaRate._DAILY_FILE_NAME,
            index_col="date",
        )
        self.yearly = pd.read_csv(
            BankOfCanadaRate.folder + BankOfCanadaRate._YEARLY_FILE_NAME,
            index_col="date",
        )

    def fetchFromURL(self):
        dailyRes = requests.get(BankOfCanadaRate._DAILY_URL)
        content = dailyRes.content
        content = content.split(b'"OBSERVATIONS"')[1]
        open(BankOfCanadaRate.folder + BankOfCanadaRate._DAILY_FILE_NAME, "wb").write(
            content
        )

        yearlyRes = requests.get(BankOfCanadaRate._YEARLY_URL)
        content = yearlyRes.content.split(b'"OBSERVATIONS"')[1]
        open(BankOfCanadaRate.folder + BankOfCanadaRate._YEARLY_FILE_NAME, "wb").write(
            content
        )
        self.readFiles()

    def getRate(self, currency: str, date: datetime, precision=YEARLY):
        if currency == "CAD":
            return 1
        try:
            if precision == BankOfCanadaRate.YEARLY:
                return self._getYearlyRate(date)
            if precision == BankOfCanadaRate.DAILY:
                return self._getDailyRate(date)
        except:
            return self.backupRate.getRate(currency, date, precision)

    def _getDailyRate(self, date: datetime):
        self.checkMax(self.daily, date)
        rate = self.daily.loc[str(date.date()), self.dailyLabel]
        return rate

    def _getYearlyRate(self, date: datetime):
        beginingOfYear = datetime(year=date.year, month=1, day=1)
        if beginingOfYear.year >= datetime.now().year:
            return self._getDailyRate(date)
        self.checkMax(self.yearly, beginingOfYear)
        rate = self.yearly.loc[str(beginingOfYear.date()), self.yearlyLabel]
        return rate

    def checkMax(self, df: pd.DataFrame, date: datetime):
        max = df.index[-1]
        maxDate = datetime.strptime(max, "%Y-%m-%d")
        if date > maxDate and date < datetime.now():
            self.fetchFromURL()
