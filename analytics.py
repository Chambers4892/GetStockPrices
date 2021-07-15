import pandas as pd
import numpy as np
from datetime import date
from datetime import datetime
from dateutil.relativedelta import relativedelta
import constants
import requests



def get_stock_range(df, stock, time):
    pd.options.mode.chained_assignment = None
    df = df.tail(time)
    df.loc[:, stock] = pd.to_numeric(df[stock])
    row = {
    "Stock": stock, 
    "Current": df[stock].iloc[-1],
    'Min': df[stock].min(),
    'Max': df[stock].max(),
    'Mean': round(df[stock].mean(), 3),
    'From': df['Date'].iloc[0] + " "+ df['Time'].iloc[0],
    'To': df['Date'].iloc[-1] + " " + df['Time'].iloc[-1]
    }
    row['Range'] = round(row['Max'] - row['Min'], 2)
    row['Pct_Range'] = round((row['Max']-row['Min'])/row['Min']*100, 4)
    row['Volatility'] = round((df[stock].pct_change().mean()-df[stock].pct_change()).pow(2).mean()**.5*1000,3)
    
    return row

def get_ranges(df, time):
#Gets all ranges for full data frame
    pd.options.mode.chained_assignment = None
    df = df.tail(time)
    df_ranges = pd.DataFrame()#columns=['Stock', 'Current', 'Min', 'Max', 'Mean', 'Range', 'Pct_Range'])
    ranges = list
    for stock in constants.df_header:
        df.loc[:, stock] = pd.to_numeric(df[stock])
        row = {
        "Stock": stock, 
        "Current": df[stock].iloc[-1],
        'Min': df[stock].min(),
        'Max': df[stock].max(),
        'Mean': round(df[stock].mean(), 3)
        
        }
        row['Range'] = (row['Max'] - row['Min'])
        row['LM'] = round(df[stock].pct_change().sum(), 3)
        row['Pct_Range'] = round((row['Max']-row['Min'])/row['Min']*100, 4)
        row['Volatility'] = round((df[stock].pct_change().mean()-df[stock].pct_change()).pow(2).mean()**.5*1000,3)
        
        del row['Min']
        del row['Max']
        del row['Range']

        df_ranges = df_ranges.append(row, df[stock].iloc[-1])
    #print(df_ranges)
        
    df_ranges = df_ranges.sort_values('Volatility', ascending=False)
    #df_ranges.concat(ranges)
    return df_ranges