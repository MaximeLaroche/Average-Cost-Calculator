from math import factorial
import pandas as pd
import re
import numpy as np
from stock import Stock
from option import Option
from datetime import datetime
from numpy import number
from labels import makeFrench
from dataExport import export
import copy

snapshots = {}


def calc_cost_basis(
    date: datetime, stocks_list: list[Stock], options_list: list[Option]
):
    stocks: list[Stock] = copy.deepcopy(stocks_list)
    stocks = list(filter(lambda sec: sec.total > 0 and sec.currency == "USD", stocks))
    options: list[Option] = copy.deepcopy(options_list)
    options = list(filter(lambda sec: sec.total > 0 and sec.currency == "USD", options))
    cost = 0
    securities = []
    for sec in stocks:
        sec_cost = sec.avg * sec.total * sec.avgRate
        cost += sec_cost
        securities.append({"Ticker": sec.ticker, "Average_price (CAD$)": sec.avg*sec.avgRate, "Amount": sec.total, "Total value (CAD$)": sec_cost} )
    for sec in options:
        sec_cost = sec.avg * sec.total * sec.avgRate
        cost -= sec_cost
        securities.append({"Ticker": sec.ticker, "Average_price (CAD$)": sec.avg*sec.avgRate, "Amount": sec.total, "Total value (CAD$)": sec_cost} )
    
   

    max_cost = 100_000
    if cost > max_cost:
        print(f"Exceeded max cost ({max_cost}) on {date.date()}. Toal value is {round(cost,2)}")

    snapshots[date.strftime('%Y-%m-%d')] = {"cost": cost, "positions": securities}
