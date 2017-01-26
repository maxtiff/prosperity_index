import pandas as pd, os, sys, functools as ft, pycurl as pyc, datetime as dt, re, numpy as np
pd.options.mode.chained_assignment = None  # default='warn'

def preventable_care(file,names,date):
    df = pd.read_excel(file,skiprows={0, 1}, parse_cols={0, 68}, skip_footer=1)
    df.columns = [names]
    df['fips'] = df['fips'].apply(lambda x: "%06d" % (x,))
    df['date'] = date

    return df

def multi_ordered_merge(lst_dfs):
    reduce_func = lambda left,right: pd.ordered_merge(left, right)

    return ft.reduce(reduce_func, lst_dfs)

def main():
    names = ['fips','rate']

    data_dir = os.getcwd() + '\\data\\'

    pc_08 = preventable_care(data_dir+'PC_County_rates_2008.xls',names,'2008')
    pc_09 = preventable_care(data_dir+'PC_County_rates_2009.xls',names,'2009')
    pc_10 = preventable_care(data_dir+'PC_County_rates_2010.xls',names,'2010')
    pc_11 = preventable_care(data_dir+'PC_County_rates_2011.xls',names,'2011')
    pc_12 = preventable_care(data_dir+'PC_County_rates_2012.xls',names,'2012')
    pc_13 = preventable_care(data_dir+'PC_County_rates_2013.xls',names,'2013')
    pc_14 = preventable_care(data_dir+'PC_County_rates_2014.xls',names,'2014')

    dfs = [pc_08,pc_09,pc_10,pc_11,pc_12,pc_13,pc_14]

    df = multi_ordered_merge(dfs)

    df = df.sort_values(['fips','date'])

    for l in pd.unique(df['fips'].ravel()):
        series = l
        frame = df[df['fips'] == series]
        series_id = 'DMPCRATE' + series
        frame.reset_index(inplace=True)
        frame = frame[['date','rate']]
        frame.set_index('date', inplace=True)
        frame.columns = [series_id]
        frame.to_csv('output\\' + series_id, sep='\t')

if __name__=='__main__':
    main()
