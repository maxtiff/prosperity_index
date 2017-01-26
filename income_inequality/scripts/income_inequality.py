import pandas as pd, os, sys, functools as ft, pycurl as pyc, datetime as dt, re, numpy as np
pd.options.mode.chained_assignment = None  # default='warn'

def inequality(file,filter,names,date):
    df = pd.read_csv(file,encoding='windows-1252',skiprows={1})
    df = df.filter(filter,axis=1)
    df.columns=[names]
    df['fips'] = df['fips'].apply(lambda x: "%06d" % (x,))
    df['date'] = date

    df['20_20'] = (df['high_20'] / df['low_20'])

    return df.filter(['fips','date','20_20','county'],axis=1)

def multi_ordered_merge(lst_dfs):
    reduce_func = lambda left,right: pd.ordered_merge(left, right)

    return ft.reduce(reduce_func, lst_dfs)

def main():
    filter = ['GEO.id2', 'GEO.display-label', 'HD01_VD02', 'HD01_VD06']

    names = ['fips', 'county', 'low_20', 'high_20']

    data_dir = os.getcwd() + '\\data\\'

    gini_10 = inequality(data_dir + 'income_inequality_10.csv', filter, names, \
                         '2010')
    gini_11 = inequality(data_dir + 'income_inequality_11.csv', filter, names, \
                         '2011')
    gini_12 = inequality(data_dir + 'income_inequality_12.csv', filter, names, \
                         '2012')
    gini_13 = inequality(data_dir + 'income_inequality_13.csv', filter, names, \
                         '2013')
    gini_14 = inequality(data_dir + 'income_inequality_14.csv', filter, names, \
                         '2014')
    gini_15 = inequality(data_dir + 'income_inequality_15.csv', filter, names, \
                         '2015')

    dfs = [gini_10,gini_11,gini_12,gini_13,gini_14,gini_15]

    df = multi_ordered_merge(dfs)
    df = df.sort_values(['fips','date'])

    # df['20_20'] = (df['high_20']/df['low_20'])

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

    return df

if __name__ == '__main__':
    main()
