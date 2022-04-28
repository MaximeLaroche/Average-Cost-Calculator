import pandas as pd
from labels import ACTIONS_LABELS
from stock import Stock, LABELS
from option import Option, OPTION_LABELS


def _createBook(df: pd.DataFrame, name: str):
    # Taken from https://xlsxwriter.readthedocs.io/example_pandas_table.html#ex-pandas-table
    writer = pd.ExcelWriter(name + '.xlsx', engine='xlsxwriter')
    df.to_excel(writer, sheet_name=name, startrow=1, header=False, index=False)
    worksheet = writer.sheets[name]

    # Get the dimensions of the dataframe.
    (max_row, max_col) = df.shape

    # Create a list of column headers, to use in add_table().
    column_settings = [{'header': column} for column in df.columns]

    # Add the Excel table structure. Pandas will add the data.
    worksheet.add_table(0, 0, max_row, max_col - 1, {'columns': column_settings})

    # Make the columns wider for clarity.
    worksheet.set_column(0, max_col - 1, 12)

    # Close the Pandas Excel writer and output the Excel file.
    writer.save()
def export():
    optionDf = Option.sort()
    optionDf = optionDf[[LABELS.date, LABELS.action, LABELS.ticker, LABELS.description, LABELS.quantity, LABELS.aquisitionCost,LABELS.aquisitionRate, LABELS.dispotitionValue, LABELS.dispositionRate, OPTION_LABELS.exp, OPTION_LABELS.strike, LABELS.price, LABELS.transactionValue,LABELS.avg, LABELS.tot, LABELS.profit,LABELS.currency, LABELS.rate, LABELS.id, LABELS.index, ACTIONS_LABELS.split]]
    stockDf = Stock.sort()
    stockDf = stockDf[[LABELS.date, LABELS.action, LABELS.ticker, LABELS.description, LABELS.quantity, LABELS.aquisitionCost,LABELS.aquisitionRate, LABELS.dispotitionValue, LABELS.dispositionRate, LABELS.price, LABELS.transactionValue,LABELS.avg, LABELS.tot, LABELS.profit,LABELS.currency, LABELS.rate, LABELS.id, LABELS.index, ACTIONS_LABELS.split]]
    _createBook(optionDf, 'Options')
    _createBook(stockDf, 'Stocks')
    