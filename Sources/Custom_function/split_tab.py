import pandas as pd

def split_tab(df, feature, label, exist_col):
    df[feature] = df[exist_col].str.split(pat='\t').str[0]
    df[label] = df[exist_col].str.split(pat='\t').str[1]
    df.drop(columns=[exist_col], inplace=True)
    return df