import pandas as pd

def process_data(df):
    df_price = df[['date', 'branch_number', 'branch', 'category', 'ItemCode', 'ItemName', 'ItemPrice']]
    return df_price
