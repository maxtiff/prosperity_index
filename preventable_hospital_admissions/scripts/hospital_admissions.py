import pandas as pd, os, sys, functools as ft, pycurl as pyc, datetime as dt, re, numpy as np
pd.options.mode.chained_assignment = None  # default='warn'

names=['fips','rate']


data_dir = os.getcwd() + '\\data\\'

pc_08= pd.read_excel(data_dir + 'PC_County_rates_2008.xls',skiprows={0,1},parse_cols={0,68},skip_footer=1)
pc_08.columns=[names]
pc_08['fips']=pc_08['fips'].apply(lambda x:"%06d" % (x,))
pc_08['date']='2008'

pc_09= pd.read_excel(data_dir + 'PC_County_rates_2009.xls',skiprows={0,1},parse_cols={0,68},skip_footer=1)
pc_09.columns=[names]
pc_09['fips']=pc_09['fips'].apply(lambda x:"%06d" % (x,))
pc_09['date']='2009'

pc_10= pd.read_excel(data_dir + 'PC_County_rates_2010.xls',skiprows={0,1},parse_cols={0,68},skip_footer=1)
pc_10.columns=[names]
pc_10['fips']=pc_10['fips'].apply(lambda x:"%06d" % (x,))
pc_10['date']='2010'

pc_11= pd.read_excel(data_dir + 'PC_County_rates_2011.xls',skiprows={0,1},parse_cols={0,68},skip_footer=1)
pc_11.columns=[names]
pc_11['fips']=pc_11['fips'].apply(lambda x:"%06d" % (x,))
pc_11['date']='2011'

pc_12= pd.read_excel(data_dir + 'PC_County_rates_2012.xls',skiprows={0,1},parse_cols={0,68},skip_footer=1)
pc_12.columns=[names]
pc_12['fips']=pc_12['fips'].apply(lambda x:"%06d" % (x,))
pc_12['date']='2012'

pc_13= pd.read_excel(data_dir + 'PC_County_rates_2013.xls',skiprows={0,1},parse_cols={0,68},skip_footer=1)
pc_13.columns=[names]
pc_13['fips']=pc_13['fips'].apply(lambda x:"%06d" % (x,))
pc_13['date']='2013'

pc_14= pd.read_excel(data_dir + 'PC_County_rates_2014.xls',skiprows={0,1},parse_cols={0,68},skip_footer=1)
pc_14.columns=[names]
pc_14['fips']=pc_14['fips'].apply(lambda x:"%06d" % (x,))
pc_14['date']='2014'

def multi_ordered_merge(lst_dfs):
    reduce_func = lambda left,right: pd.ordered_merge(left, right)

    return ft.reduce(reduce_func, lst_dfs)

dfs = [pc_08,pc_09,pc_10,pc_11,pc_12,pc_13,pc_14]

df = multi_ordered_merge(dfs)

df = df.sort_values(['fips','date'])

for l in pd.unique(df['fips'].ravel()):
    series = l
    frame = df[df['fips'] == series]
    series_id = 'DMHPARATE' + series
    frame.reset_index(inplace=True)
    # frame = frame.sort_values(['date'])
    # frame.drop(['index'], axis=1, inplace=True)
    frame = frame[['date','rate']]
    frame.set_index('date', inplace=True)
    frame.columns = [series_id]
    frame.to_csv('output\\' + series_id, sep='\t')
