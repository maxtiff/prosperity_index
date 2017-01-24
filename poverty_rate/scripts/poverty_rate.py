import pandas as pd, os, sys, functools as ft, pycurl as pyc, datetime as dt, re, numpy as np
pd.options.mode.chained_assignment = None  # default='warn'

keep = ['GEO.id2','GEO.display-label','HC03_EST_VC01']

data_dir = os.getcwd() + '\\data\\'

poverty_12 = pd.read_csv(data_dir+'povertyrate_12.csv',encoding='windows-1252',skiprows={1})
poverty_12 = poverty_12.filter(keep,axis=1)
poverty_12['GEO.id2']=poverty_12['GEO.id2'].apply(lambda x:"%06d" % (x,))
# poverty_12.columns=[names]
poverty_12['date'] = '2012'

poverty_13 = pd.read_csv(data_dir+'povertyrate_13.csv',encoding='windows-1252',skiprows={1})
poverty_13 = poverty_13.filter(keep,axis=1)
poverty_13['GEO.id2']=poverty_13['GEO.id2'].apply(lambda x:"%06d" % (x,))
# poverty_13.columns=[names]
poverty_13['date'] = '2013'

poverty_14 = pd.read_csv(data_dir+'povertyrate_14.csv',encoding='windows-1252',skiprows={1})
poverty_14 = poverty_14.filter(keep,axis=1)
poverty_14['GEO.id2']=poverty_14['GEO.id2'].apply(lambda x:"%06d" % (x,))
# poverty_14.columns=[names]
poverty_14['date'] = '2014'

def multi_ordered_merge(lst_dfs):
    reduce_func = lambda left,right: pd.ordered_merge(left, right)

    return ft.reduce(reduce_func, lst_dfs)

dfs = [poverty_12,poverty_13,poverty_14]

df = multi_ordered_merge(dfs)

df = df.sort_values(['GEO.id2','date'])

for l in pd.unique(df['GEO.id2'].ravel()):
    series = l
    frame = df[df['GEO.id2'] == series]
    series_id = 'S1701ACS' + series
    frame.reset_index(inplace=True)
    # frame = frame.sort_values(['date'])
    # frame.drop(['index'], axis=1, inplace=True)
    frame = frame[['date','HC03_EST_VC01']]
    frame.set_index('date', inplace=True)
    frame.columns = [series_id]
    frame.to_csv('output\\' + series_id, sep='\t')
