import pandas as pd, os, sys, functools as ft, pycurl as pyc, datetime as dt, re, numpy as np
pd.options.mode.chained_assignment = None  # default='warn'

def mean_commute(wf_file,workforce_filter,workforce_names,cm_file,\
                 commute_filter,commute_names,date):

    df_wf = pd.read_csv(wf_file,encoding='windows-1252',skiprows={1})
    df_wf = df_wf.filter(workforce_filter, axis=1)
    df_wf.columns = [workforce_names]
    df_wf['fips'] = df_wf['fips'].apply(lambda x: "%06d" % (x,))

    df_cm = pd.read_csv(cm_file,encoding='windows-1252', skiprows={1})
    df_cm = df_cm.filter(commute_filter,axis=1)
    df_cm.columns = [commute_names]
    df_cm['fips'] = df_cm['fips'].apply(lambda x: "%06d" % (x,))

    df = pd.merge(df_wf, df_cm,on=['fips'])

    df['avg_commute'] = df['commute_time'] / df['commuters']

    df['date'] = date

    return df

def multi_ordered_merge(lst_dfs):
    reduce_func = lambda left,right: pd.ordered_merge(left, right)

    return ft.reduce(reduce_func, lst_dfs)


def main():
    wf_filter = ['GEO.id2','HD01_VD01']
    wf_names = ['fips', 'commuters']

    cm_filter = ['GEO.id2', 'HD01_VD01']
    cm_names= ['fips', 'commute_time']

    data_dir = os.getcwd() + '\\data\\'
    counties = pd.read_table('..\\national_county.txt', dtype=str, sep=';')

    commute_09 = mean_commute(data_dir+'workforce_09.csv',wf_filter,wf_names,\
                              data_dir+'aggregate_commute_09.csv',cm_filter,\
                              cm_names,'2009')
    commute_10 = mean_commute(data_dir+'workforce_10.csv',wf_filter,wf_names,\
                              data_dir+'aggregate_commute_10.csv',cm_filter,\
                              cm_names,'2010')
    commute_11 = mean_commute(data_dir+'workforce_11.csv',wf_filter,wf_names,\
                              data_dir+'aggregate_commute_11.csv',cm_filter,\
                              cm_names,'2011')
    commute_12 = mean_commute(data_dir+'workforce_12.csv',wf_filter,wf_names,\
                              data_dir+'aggregate_commute_12.csv',cm_filter,\
                              cm_names,'2012')
    commute_13 = mean_commute(data_dir+'workforce_13.csv',wf_filter,wf_names,\
                              data_dir+'aggregate_commute_13.csv',cm_filter,\
                              cm_names,'2013')
    commute_14 = mean_commute(data_dir+'workforce_14.csv',wf_filter,wf_names,\
                              data_dir+'aggregate_commute_14.csv',cm_filter,\
                              cm_names,'2014')
    commute_15 = mean_commute(data_dir+'workforce_15.csv',wf_filter,wf_names,\
                              data_dir+'aggregate_commute_15.csv',cm_filter,\
                              cm_names,'2015')

    dfs = [commute_09,commute_10,commute_11,commute_12,commute_13,commute_14,commute_15]

    df = multi_ordered_merge(dfs)

    df = pd.merge(df, counties, on='fips')

    df = df.sort_values(['fips','date'])

    for l in pd.unique(df.fips.ravel()):
        series = l
        frame = df[df['fips'] == series]
        series_id = 'B080ACS' + series
        frame.reset_index(inplace=True)
        frame = frame[['date', 'avg_commute']]
        frame.set_index('date', inplace=True)
        frame.columns = [series_id]
        frame.to_csv('output\\' + series_id, sep='\t')

if __name__ == '__main__':
    main()