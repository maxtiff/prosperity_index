import pandas as pd, os, sys, functools as ft, pycurl as pyc, datetime as dt, re, numpy as np
pd.options.mode.chained_assignment = None  # default='warn'

# def __main__():

# Import data
data_dir = os.getcwd() + '\\data\\'

df = pd.read_csv(data_dir + 'equifax.csv',parse_dates=['qtr'],low_memory=False,memory_map=True)
df.fillna(0,axis=1,inplace=True)

# Get states fips codes and merge with df
states = pd.read_table('..\\state_fips.txt',dtype=str)

df = pd.merge(df, states, on='state')
df = df.sort_values(['fips','county_code','qtr'])

#Drop rows with too small of sample
df = df[df.num_total >= 20]

# Clean dates
df['date'] = df['qtr'].dt.year.astype(str)+'.0'+df['qtr'].dt.quarter.astype(str)
df.drop(['qtr'],axis=1,inplace=True)

# Get pct of subprime creditors
df['pct_below660'] = df['num_below660']/df['num_total']
df.reset_index(inplace=True)
df.drop(['index'], axis=1, inplace=True)

# Create one fips code
df.county_code = df.county_code.astype(int)
df['county_code']=df['county_code'].apply(lambda x:"%03d" % (x,))
df.county_code = df.county_code.astype(str)

df.fips = df.fips.astype(int)
df['fips']=df['fips'].apply(lambda x:"%03d" % (x,))
df.fips = df.fips.astype(str)

df.fips = df.fips + df.county_code

# Remove unnecessary, non-county series
counties = pd.read_table('..\\national_county.txt',dtype=str,sep=';')
df = pd.merge(df, counties, on='fips')

for l in pd.unique(df.fips.ravel()):
    series_id = 'EQFXSUBPRIME' + l
    frame = df[df['fips'] == l]
    # frame.reset_index(inplace=True)
    # frame = frame.sort_values(['date'])
    # frame.drop(['index'], axis=1, inplace=True)
    output = frame[['date', 'pct_below660']]
    output.set_index('date', inplace=True)
    output.columns = [series_id]
    output.to_csv('output\\' + series_id, sep='\t')



