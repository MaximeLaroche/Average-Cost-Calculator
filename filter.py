import pandas as pd

    

def _removeTFSA(df: pd.DataFrame) -> pd.DataFrame:
    df = df.drop(df[df["Account Type"] == "Individual TFSA"].index)
    return df

def _removeUnsupportedData(df: pd.DataFrame) -> pd.DataFrame:
    df = _removeTFSA(df)
    
    df = df.drop(df[df["Action"] == "BRW"].index) # only occured in 2020
    df = df.drop(df[df["Action"] == "CON"].index) # TFSA Contribution. Not a taxable event
    df = df.drop(df[df["Action"] == "DEP"].index) # Deposit. Not a taxable event
    df = df.drop(df[df["Action"] == "EFT"].index) # Electronic fund transfer. Not a taxable event
    df = df.drop(df[df["Action"] == "DIS"].index) # 2020 term for dividend
    df = df.drop(df[df["Action"] == "FEE"].index) # only occured in 2020 (Borrow fees)
    df = df.drop(df[df["Action"] == "FXT"].index) # Forein exchange, only done in 2020
    df = df.drop(df[df["Action"] == "CIL"].index) # 2020 term for ADJ
    df = df.drop(df[df["Action"] == "FCH"].index) # Only on 2020 (Data fees, rebates etc)
    df = df.drop(df[df["Action"] == "TF6"].index) # Only happened in TFSA
    df = df.drop(df[df["Action"] == "REV"].index) # 2020 SQQQ reverse split (position closed in 2020)
    df = df.drop(df[df["Activity Type"] == "Interest"].index) # only in 2020, not a transaction
    df = df.drop(df[df["Activity Type"] == "Dividends"].index) # Dividends and interests
    df = df.drop(df[df["Action"] == "MKT"].index) # only in 2020, not a transaction
    
    
    return df



def removeBadData(df: pd.DataFrame)-> pd.DataFrame:
    df = _removeUnsupportedData(df)
    # df.to_excel("Input copy.xlsx", index = None)
    return df