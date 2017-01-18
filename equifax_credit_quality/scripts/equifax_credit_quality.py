import pandas as pd, os, sys, functools as ft, pycurl as pyc, datetime as dt, re, numpy as np
pd.options.mode.chained_assignment = None  # default='warn'

# Import data
data_dir = os.getcwd() + '\\data\\'

df = pd.read_csv(data_dir + 'equifax.csv',parse_dates=['qtr'],low_memory=False,memory_map=True)
df.fillna(0,axis=1,inplace=True)

# Get states fips codes and merge with  df
states = pd.read_table('..\\state_fips.txt',dtype=str)

df = pd.merge(df, states, on='state')
df = df.sort_values(['fips','county_code','qtr'])

#Drop rows with small sample
df = df[df.num_below660 >= 20]

# Clean dates
df['date'] = df['qtr'].dt.year.astype(str)+'.0'+df['qtr'].dt.quarter.astype(str)
df.drop(['qtr'],axis=1,inplace=True)

# Get pct of subprime credit
df['pct_below660'] = df['num_below660']/df['num_total']


