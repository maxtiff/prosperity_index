import pandas as pd, os, multi_ordered_merge as merger, functools as ft, pycurl as pyc, datetime as dt, re, numpy as np,math
pd.options.mode.chained_assignment = None  # default='warn'

def median_age(file,column_name,date):
    keep_header = ['GEO.id2', column_name]

    df = pd.read_csv(file, encoding='windows-1252', skiprows={1}, \
                         low_memory=False)
    df = df.filter(regex='GEO.id2|'+column_name,axis=1)
    df.rename(columns={'GEO.id2': 'fips',column_name:'median_age'},inplace=True)
    df['fips'] = df['fips'].apply(lambda x: "%06d" % (x,))
    df['date'] = date

    return df

def main():
    data_dir = os.getcwd() + '\\data\\'
    counties = pd.read_table('..\\national_county.txt', dtype=str, sep=';')

    df_09 = median_age(data_dir + 'age_09.csv','HC01_EST_VC33','2009')
    df_10 = median_age(data_dir + 'age_10.csv','HC01_EST_VC35','2010')
    df_11 = median_age(data_dir + 'age_11.csv','HC01_EST_VC35','2011')
    df_12 = median_age(data_dir + 'age_12.csv','HC01_EST_VC35','2012')
    df_13 = median_age(data_dir + 'age_13.csv','HC01_EST_VC35','2013')
    df_14 = median_age(data_dir + 'age_14.csv','HC01_EST_VC35','2014')
    df_15 = median_age(data_dir + 'age_15.csv','HC01_EST_VC35','2015')

    dfs = [df_09,df_10,df_11,df_12,df_13,df_14,df_15]

    df = merger.multi_ordered_merge(dfs)
    df = pd.merge(df,counties,on='fips')
    df = df.sort_values(['fips','date'])


if __name__=='__main__':
    main()


