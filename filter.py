import pandas as pd

    

def _removeTFSA(df: pd.DataFrame) -> pd.DataFrame:
    df = df.drop(df[df["Account Type"] == "Individual TFSA"].index)
    return df

def _removeUnsupportedData(df: pd.DataFrame) -> pd.DataFrame:
    df = _removeTFSA(df)
    
    df = df.drop(df[df["Action"] == "BRW"].index)
    df = df.drop(df[df["Action"] == "CON"].index)
    df = df.drop(df[df["Action"] == "DEP"].index)
    df = df.drop(df[df["Action"] == "DIS"].index)
    df = df.drop(df[df["Action"] == "FEE"].index)
    df = df.drop(df[df["Action"] == "FXT"].index)
    df = df.drop(df[df["Action"] == "CIL"].index)
    df = df.drop(df[df["Action"] == "FCH"].index)
    df = df.drop(df[df["Action"] == "TF6"].index)
    return df

def _removeUnusedCol(df: pd.DataFrame) -> pd.DataFrame:
    df.drop(['Account #', 'Activity Type', 'Account Type','Settlement Date'], axis = 1, inplace = True) 
    return df

def removeBadData(df: pd.DataFrame)-> pd.DataFrame:
    df = _removeUnsupportedData(df)
    df = _removeUnusedCol(df)
    return df