import pandas as pd, os, sys, functools as ft, pycurl as pyc, datetime as dt, re, numpy as np
pd.options.mode.chained_assignment = None  # default='warn'

keep_workforce = ['GEO.id2','GEO.display-label','HD01_VD01']
names_workforce= ['fips','county','commuters']

keep_aggregate_commute = ['GEO.id2','GEO.display-label','HD01_VD01']
names_aggregate_commute = ['fips','county','commute_time']

data_dir = os.getcwd() + '\\data\\'

#2009
workforce_09 = pd.read_csv(data_dir+'workforce_09.csv',encoding='windows-1252',skiprows={1})
workforce_09 = workforce_09.filter(keep_workforce,axis=1)
workforce_09.columns=[names_workforce]
workforce_09['fips']=workforce_09['fips'].apply(lambda x:"%06d" % (x,))
workforce_09['date'] = '2009'

aggregate_commute_09 = pd.read_csv(data_dir+'aggregate_commute_09.csv',encoding='windows-1252',skiprows={1})
aggregate_commute_09 = aggregate_commute_09.filter(keep_aggregate_commute,axis=1)
aggregate_commute_09.columns=[names_aggregate_commute]
aggregate_commute_09['fips']=aggregate_commute_09['fips'].apply(lambda x:"%06d" % (x,))
aggregate_commute_09['date'] = '2009'

commute_09 = pd.merge(workforce_09,aggregate_commute_09,on=['fips','county','date'])

# 2010
workforce_10 = pd.read_csv(data_dir+'workforce_10.csv',encoding='windows-1252',skiprows={1})
workforce_10 = workforce_10.filter(keep_workforce,axis=1)
workforce_10.columns=[names_workforce]
workforce_10['fips']=workforce_10['fips'].apply(lambda x:"%06d" % (x,))
workforce_10['date'] = '2010'

aggregate_commute_10 = pd.read_csv(data_dir+'aggregate_commute_10.csv',encoding='windows-1252',skiprows={1})
aggregate_commute_10 = aggregate_commute_10.filter(keep_aggregate_commute,axis=1)
aggregate_commute_10.columns=[names_aggregate_commute]
aggregate_commute_10['fips']=aggregate_commute_10['fips'].apply(lambda x:"%06d" % (x,))
aggregate_commute_10['date'] = '2010'

commute_10 = pd.merge(workforce_10,aggregate_commute_10,on=['fips','county','date'])

#2011
workforce_11 = pd.read_csv(data_dir+'workforce_11.csv',encoding='windows-1252',skiprows={1})
workforce_11 = workforce_11.filter(keep_workforce,axis=1)
workforce_11.columns=[names_workforce]
workforce_11['fips']=workforce_11['fips'].apply(lambda x:"%06d" % (x,))
workforce_11['date'] = '2011'

aggregate_commute_11 = pd.read_csv(data_dir+'aggregate_commute_11.csv',encoding='windows-1252',skiprows={1})
aggregate_commute_11 = aggregate_commute_11.filter(keep_aggregate_commute,axis=1)
aggregate_commute_11.columns=[names_aggregate_commute]
aggregate_commute_11['fips']=aggregate_commute_11['fips'].apply(lambda x:"%06d" % (x,))
aggregate_commute_11['date'] = '2011'

commute_11 = pd.merge(workforce_11,aggregate_commute_11,on=['fips','county','date'])

#2012
workforce_12 = pd.read_csv(data_dir+'workforce_12.csv',encoding='windows-1252',skiprows={1})
workforce_12 = workforce_12.filter(keep_workforce,axis=1)
workforce_12.columns=[names_workforce]
workforce_12['fips']=workforce_12['fips'].apply(lambda x:"%06d" % (x,))
workforce_12['date'] = '2012'

aggregate_commute_12 = pd.read_csv(data_dir+'aggregate_commute_12.csv',encoding='windows-1252',skiprows={1})
aggregate_commute_12 = aggregate_commute_12.filter(keep_aggregate_commute,axis=1)
aggregate_commute_12.columns=[names_aggregate_commute]
aggregate_commute_12['fips']=aggregate_commute_12['fips'].apply(lambda x:"%06d" % (x,))
aggregate_commute_12['date'] = '2012'

commute_12 = pd.merge(workforce_12,aggregate_commute_12,on=['fips','county','date'])

#2013
workforce_13 = pd.read_csv(data_dir+'workforce_13.csv',encoding='windows-1252',skiprows={1})
workforce_13 = workforce_13.filter(keep_workforce,axis=1)
workforce_13.columns=[names_workforce]
workforce_13['fips']=workforce_13['fips'].apply(lambda x:"%06d" % (x,))
workforce_13['date'] = '2013'

aggregate_commute_13 = pd.read_csv(data_dir+'aggregate_commute_13.csv',encoding='windows-1252',skiprows={1})
aggregate_commute_13 = aggregate_commute_13.filter(keep_aggregate_commute,axis=1)
aggregate_commute_13.columns=[names_aggregate_commute]
aggregate_commute_13['fips']=aggregate_commute_13['fips'].apply(lambda x:"%06d" % (x,))
aggregate_commute_13['date'] = '2013'

commute_13 = pd.merge(workforce_13,aggregate_commute_13,on=['fips','county','date'])

#2014
workforce_14 = pd.read_csv(data_dir+'workforce_14.csv',encoding='windows-1252',skiprows={1})
workforce_14 = workforce_14.filter(keep_workforce,axis=1)
workforce_14.columns=[names_workforce]
workforce_14['fips']=workforce_14['fips'].apply(lambda x:"%06d" % (x,))
workforce_14['date'] = '2014'

aggregate_commute_14 = pd.read_csv(data_dir+'aggregate_commute_14.csv',encoding='windows-1252',skiprows={1})
aggregate_commute_14 = aggregate_commute_14.filter(keep_aggregate_commute,axis=1)
aggregate_commute_14.columns=[names_aggregate_commute]
aggregate_commute_14['fips']=aggregate_commute_14['fips'].apply(lambda x:"%06d" % (x,))
aggregate_commute_14['date'] = '2014'

commute_14 = pd.merge(workforce_14,aggregate_commute_14,on=['fips','county','date'])



def multi_ordered_merge(lst_dfs):
    reduce_func = lambda left,right: pd.ordered_merge(left, right)

    return ft.reduce(reduce_func, lst_dfs)

dfs = [commute_09,commute_10,commute_11,commute_12,commute_13,commute_14]

df = multi_ordered_merge(dfs)
df = df.sort_values(['fips','date'])

df['avg_commute']=df['commute_time']/df['commuters']

for l in pd.unique(df.fips.ravel()):
    series = l
    frame = df[df['fips'] == series]
    series_id = 'B080ACS' + series
    frame.reset_index(inplace=True)
    # frame = frame.sort_values(['date'])
    # frame.drop(['index'], axis=1, inplace=True)
    frame = frame[['date', 'avg_commute']]
    frame.set_index('date', inplace=True)
    frame.columns = [series_id]
    frame.to_csv('output\\' + series_id, sep='\t')
