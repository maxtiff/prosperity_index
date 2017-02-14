import pandas as pd, os, sys, functools as ft, multi_ordered_merge as merger as pyc, datetime as dt, re, numpy as np,math
pd.options.mode.chained_assignment = None  # default='warn'

def racial_pop(county_file,date):
    keep_header = ['GEO.id2','HD01_VD03','HD01_VD04','HD01_VD05','HD01_VD06','HD01_VD12']

    df = pd.read_csv(county_file, encoding='windows-1252', skiprows={1},\
                            low_memory=False)
    df = df.filter(keep_header, axis=1)
    df.rename(columns={'GEO.id2': 'fips'},inplace=True)
    df['fips'] = df['fips'].apply(lambda x: "%06d" % (x,))
    df['date'] = date

    return df

# def multi_ordered_merge(lst_dfs):
#     reduce_func = lambda left,right: pd.ordered_merge(left, right)
#
#     return ft.reduce(reduce_func, lst_dfs)

def main():
    data_dir = os.getcwd() + '\\data\\'
    counties = pd.read_table('..\\national_county.txt', dtype=str, sep=';')

    df_09 = racial_pop(data_dir + 'race_county_09.csv','2009')
    df_10 = racial_pop(data_dir + 'race_county_10.csv','2010')
    df_11 = racial_pop(data_dir + 'race_county_11.csv','2011')
    df_12 = racial_pop(data_dir + 'race_county_12.csv','2012')
    df_13 = racial_pop(data_dir + 'race_county_13.csv','2013')
    df_14 = racial_pop(data_dir + 'race_county_14.csv','2014')
    df_15 = racial_pop(data_dir + 'race_county_15.csv','2015')

    dfs = [df_09,df_10,df_11,df_12,df_13,df_14,df_15]

    df = merger.multi_ordered_merge(dfs)
    df = pd.merge(df,counties,on='fips')
    df = df.sort_values(['fips','date'])
    df.fillna('.',axis=1,inplace=True)

    for series in pd.unique(df['fips'].ravel()):
        frame = df[df['fips'] == series]
        frame.reset_index(inplace=True)
        frame.drop(['index'], axis=1, inplace=True)
        for c in ['HD01_VD03','HD01_VD04','HD01_VD05','HD01_VD06','HD01_VD12']:
            series_id = 'B03002' + frame[c].name[-4:] + series
            output = frame[['date',c]]
            output.set_index('date', inplace=True)
            output.columns = [series_id]
            output.to_csv('output\\' + series_id, sep='\t')

if __name__=='__main__':
    main()