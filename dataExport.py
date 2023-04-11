import pandas as pd
from labels import ACTIONS_LABELS
from stock import Stock, LABELS
from option import Option, OPTION_LABELS


def _createBook(df: pd.DataFrame, name: str):
    # Taken from https://xlsxwriter.readthedocs.io/example_pandas_table.html#ex-pandas-table
    writer = pd.ExcelWriter(name + ".xlsx", engine="xlsxwriter")
    df.to_excel(writer, sheet_name=name, startrow=1, header=False, index=False)
    worksheet = writer.sheets[name]

    # Get the dimensions of the dataframe.
    (max_row, max_col) = df.shape

    # Create a list of column headers, to use in add_table().
    column_settings = [{"header": column} for column in df.columns]

    # Add the Excel table structure. Pandas will add the data.
    worksheet.add_table(0, 0, max_row, max_col - 1, {"columns": column_settings})

    # Make the columns wider for clarity.
    worksheet.set_column(0, max_col - 1, 12)

    # Close the Pandas Excel writer and output the Excel file.
    writer.save()


def calcCADProfits(df: pd.DataFrame) -> pd.DataFrame:
    df[LABELS.profitCAD] = (
        df[LABELS.dispotitionValue] * df[LABELS.dispositionRate]
        - df[LABELS.aquisitionCost] * df[LABELS.aquisitionRate]
    )
    return df


def export(name: str):
    optionDf = Option.sort()
    stockDf = Stock.sort()

    optionDf = calcCADProfits(optionDf)
    stockDf = calcCADProfits(stockDf)

    optionDf = optionDf[
        [
            LABELS.date,
            LABELS.action,
            LABELS.ticker,
            LABELS.description,
            LABELS.quantity,
            LABELS.aquisitionCost,
            LABELS.aquisitionRate,
            LABELS.dispotitionValue,
            LABELS.dispositionRate,
            LABELS.profit,
            LABELS.profitCAD,
            OPTION_LABELS.exp,
            OPTION_LABELS.strike,
            LABELS.price,
            LABELS.transactionValue,
            LABELS.avg,
            LABELS.tot,
            LABELS.currency,
            LABELS.rate,
            LABELS.id,
            LABELS.index,
            ACTIONS_LABELS.split,
            OPTION_LABELS.codes,
        ]
    ]
    stockDf = stockDf[
        [
            LABELS.date,
            LABELS.action,
            LABELS.ticker,
            LABELS.description,
            LABELS.quantity,
            LABELS.aquisitionCost,
            LABELS.aquisitionRate,
            LABELS.dispotitionValue,
            LABELS.dispositionRate,
            LABELS.profit,
            LABELS.profitCAD,
            LABELS.price,
            LABELS.transactionValue,
            LABELS.avg,
            LABELS.tot,
            LABELS.currency,
            LABELS.rate,
            LABELS.id,
            LABELS.index,
            ACTIONS_LABELS.split,
        ]
    ]
    _createBook(optionDf, name + "Options")
    _createBook(stockDf, name + "Stocks")
