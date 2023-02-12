import pandas as pd
from get_coordinates import get_coordinates

def add_coordinates(df_price):
    df_branches = df_price[['branch_number', 'branch']].drop_duplicates()
    df_branches['branch'] = df_branches['branch'].str.split(" ").str[1:].apply(' '.join)
    df_branches = df_branches.reset_index(drop=True)
    print('Get Geo')
    df_branches['coordinates'] = df_branches['branch'].apply(get_coordinates)
    df_branches[['latitude', 'longitude']] = df_branches['coordinates'].apply(pd.Series, dtype=float)
    df_price_coordinates = df_price.merge(df_branches, how='left', left_on='branch_number', right_on='branch_number')
    df_price_coordinates = df_price_coordinates[['date',
                                                 'branch_number',
                                                 'branch_x',
                                                 'coordinates',
                                                 'latitude',
                                                 'longitude',
                                                 'category',
                                                 'ItemCode',
                                                 'ItemName',
                                                 'ItemPrice']].rename(columns={'branch_x': 'branch_name'})
    return df_price_coordinates
