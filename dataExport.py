import pandas as pd
from stock import Stock
from option import Option


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
    stockDf = Stock.sort()

    _createBook(optionDf, 'Options')
    _createBook(stockDf, 'Stocks')
    