import pandas as pd, os, sys, functools as ft, pycurl as pyc, datetime as dt, re, numpy as np,math
pd.options.mode.chained_assignment = None  # default='warn'

data_dir = os.getcwd() + '\\data\\'

def multi_ordered_merge(lst_dfs):
    reduce_func = lambda left,right: pd.ordered_merge(left, right)

    return ft.reduce(reduce_func, lst_dfs)


def small_biz_rate(biz_ptrns,lf,date):

    biz_keep = 'fips|n1_4|n5_9|n10_19|n20_49|n50_99|n100_249|n250_499'
    biz_drop = 'fips|small_biz'
    biz_df = pd.read_table(biz_ptrns,sep=',')

    biz_df['fipstate']=biz_df['fipstate'].astype(int)
    biz_df['fipstate']=biz_df['fipstate'].apply(lambda x:"%03d" % (x,))
    biz_df['fipstate']=biz_df['fipstate'].astype(str)

    biz_df['fipscty']=biz_df['fipscty'].astype(int)
    biz_df['fipscty']=biz_df['fipscty'].apply(lambda x:"%03d" % (x,))
    biz_df['fipscty']=biz_df['fipscty'].astype(str)

    biz_df['fips']=biz_df['fipstate']+biz_df['fipscty']

    biz_df=biz_df.groupby(biz_df.fips).sum()
    biz_df.reset_index(level=0, inplace=True)
    biz_df=biz_df.filter(regex=biz_keep,axis=1)
    biz_df['small_biz']=biz_df.sum(axis=1)
    biz_df=biz_df.filter(regex=biz_drop,axis=1)

    lf_keep='GEO.id2|GEO.display-label|HC02_EST_VC01|HC01_EST_VC01'
    lf_drop=['pop','lf_pt']
    lf_names = ['fips','county','pop','lf_pt']
    lf_df = pd.read_csv(lf,encoding='windows-1252',skiprows={1})
    lf_df=lf_df.filter(regex=lf_keep,axis=1)
    lf_df.columns=[lf_names]
    lf_df['fips']=lf_df['fips'].apply(lambda x:"%06d" % (x,))
    lf_df['lf'] = (lf_df['pop'] * lf_df['lf_pt'])/100
    lf_df.drop(lf_drop,axis=1,inplace=True)

    df = pd.merge(lf_df,biz_df,on='fips')
    df['rate'] = (df['small_biz']/df['lf'])*100
    df['date'] = date

    return df

# Read in and process data
df_09 = small_biz_rate(data_dir+'cbp09co.txt',data_dir+'laborforce_09.csv','2009')
df_10 = small_biz_rate(data_dir+'cbp10co.txt',data_dir+'laborforce_10.csv','2010')
df_11 = small_biz_rate(data_dir+'cbp11co.txt',data_dir+'laborforce_11.csv','2011')
df_12 = small_biz_rate(data_dir+'cbp12co.txt',data_dir+'laborforce_12.csv','2012')
df_13 = small_biz_rate(data_dir+'cbp13co.txt',data_dir+'laborforce_13.csv','2013')
df_14 = small_biz_rate(data_dir+'cbp14co.txt',data_dir+'laborforce_14.csv','2014')

dfs = [df_09,df_10,df_11,df_12,df_13,df_14]

df = multi_ordered_merge(dfs)
df = df.sort_values(['fips','date'])
df.fillna('.',axis=1,inplace=True)

# Create output files
for l in pd.unique(df['fips'].ravel()):
    series = l
    frame = df[df['fips'] == series]
    series_id = 'SMLBIZOWN' + series
    frame.reset_index(inplace=True)
    frame = frame[['date','rate']]
    frame.set_index('date', inplace=True)
    frame.columns = [series_id]
    frame.to_csv('output\\' + series_id, sep='\t')
