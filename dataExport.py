import pandas as pd
from stock import Stock, NAMES
from option import Option, OPTION_NAMES


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
    optionDf = optionDf[[NAMES.date, NAMES.action, NAMES.ticker, NAMES.description, NAMES.quantity, NAMES.aquisitionCost,NAMES.aquisitionRate, NAMES.dispotitionValue, NAMES.dispositionRate, OPTION_NAMES.exp, OPTION_NAMES.strike, NAMES.price, NAMES.transactionValue,NAMES.avg, NAMES.tot, NAMES.profit,NAMES.currency, NAMES.rate, NAMES.id, NAMES.index]]
    stockDf = Stock.sort()
    stockDf = stockDf[[NAMES.date, NAMES.action, NAMES.ticker, NAMES.description, NAMES.quantity, NAMES.aquisitionCost,NAMES.aquisitionRate, NAMES.dispotitionValue, NAMES.dispositionRate, NAMES.price, NAMES.transactionValue,NAMES.avg, NAMES.tot, NAMES.profit,NAMES.currency, NAMES.rate, NAMES.id, NAMES.index]]
    _createBook(optionDf, 'Options')
    _createBook(stockDf, 'Stocks')
    