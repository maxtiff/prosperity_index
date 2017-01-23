import pandas as pd, os, sys, functools as ft, pycurl as pyc, datetime as dt, re, numpy as np
pd.options.mode.chained_assignment = None  # default='warn'

keep = ['GEO.id2','GEO.display-label','HD01_VD02','HD01_VD06']

names = ['fips','county','low_20','high_20']

data_dir = os.getcwd() + '\\data\\'

gini_10 = pd.read_csv(data_dir+'income_inequality_10.csv',encoding='windows-1252',skiprows={1})
gini_10 = gini_10.filter(keep,axis=1)
gini_10.columns=[names]
gini_10['fips']=gini_10['fips'].apply(lambda x:"%06d" % (x,))
gini_10['date'] = '2010'

gini_11 = pd.read_csv(data_dir+'income_inequality_11.csv',encoding='windows-1252',skiprows={1})
gini_11 = gini_11.filter(keep,axis=1)
gini_11.columns=[names]
gini_11['fips']=gini_11['fips'].apply(lambda x:"%06d" % (x,))
gini_11['date'] = '2011'

gini_12 = pd.read_csv(data_dir+'income_inequality_12.csv',encoding='windows-1252',skiprows={1})
gini_12 = gini_12.filter(keep,axis=1)
gini_12.columns=[names]
gini_12['fips']=gini_12['fips'].apply(lambda x:"%06d" % (x,))
gini_12['date'] = '2012'

gini_13 = pd.read_csv(data_dir+'income_inequality_13.csv',encoding='windows-1252',skiprows={1})
gini_13 = gini_13.filter(keep,axis=1)
gini_13.columns=[names]
gini_13['fips']=gini_13['fips'].apply(lambda x:"%06d" % (x,))
gini_13['date'] = '2013'

gini_14 = pd.read_csv(data_dir+'income_inequality_14.csv',encoding='windows-1252',skiprows={1})
gini_14 = gini_14.filter(keep,axis=1)
gini_14.columns=[names]
gini_14['fips']=gini_14['fips'].apply(lambda x:"%06d" % (x,))
gini_14['date'] = '2014'

def multi_ordered_merge(lst_dfs):
    reduce_func = lambda left,right: pd.ordered_merge(left, right)

    return ft.reduce(reduce_func, lst_dfs)

dfs = [gini_10,gini_11,gini_12,gini_13,gini_14]

df = multi_ordered_merge(dfs)

df['20_20'] = (df['high_20']/df['low_20'])

for l in pd.unique(df.fips.ravel()):
    series = l
    frame = df[df['fips'] == series]
    series_id = '2020RATIO' + series
    frame.reset_index(inplace=True)
    # frame = frame.sort_values(['date'])
    # frame.drop(['index'], axis=1, inplace=True)
    frame = frame[['date', '20_20']]
    frame.set_index('date', inplace=True)
    frame.columns = [series_id]
    frame.to_csv('output\\' + series_id, sep='\t')
