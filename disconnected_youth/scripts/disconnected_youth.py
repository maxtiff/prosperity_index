import pandas as pd, os, sys, functools as ft, pycurl as pyc, datetime as dt, re, numpy as np
pd.options.mode.chained_assignment = None  # default='warn'

def dc_youth(dy_data,date):

    keep = ['GEO.id2','GEO.display-label','HD01_VD01','HD01_VD10','HD01_VD11',\
            'HD01_VD14','HD01_VD15','HD01_VD24','HD01_VD25','HD01_VD28','HD01_VD29']
    regex = ('GEO.id2|GEO.display-label|disconnected_youth|date')

    #import data
    df = pd.read_csv(dy_data,encoding='windows-1252',skiprows={1})
    df = df.filter(keep,axis=1)
    df['GEO.id2']=df['GEO.id2'].apply(lambda x:"%06d" % (x,))
    df['date'] = date

    # Calculate disconnected youth
    df['disconnected_youth']=((df['HD01_VD10'] +df['HD01_VD11'] + df['HD01_VD14'] \
                               +df['HD01_VD15'] + df['HD01_VD24'] + df['HD01_VD25'] \
                               +df['HD01_VD28'] + df['HD01_VD29'])/df['HD01_VD01'])*100

    return df.filter(regex=regex, axis=1)

def multi_ordered_merge(lst_dfs):
        reduce_func = lambda left,right: pd.ordered_merge(left, right)

        return ft.reduce(reduce_func, lst_dfs)

def main():
    data_dir = os.getcwd() + '\\data\\'

    youth_09 = dc_youth(data_dir+'disconnected_youth_09.csv','2009')
    youth_10 = dc_youth(data_dir+'disconnected_youth_10.csv','2010')
    youth_11 = dc_youth(data_dir+'disconnected_youth_11.csv','2011')
    youth_12 = dc_youth(data_dir+'disconnected_youth_12.csv','2012')
    youth_13 = dc_youth(data_dir+'disconnected_youth_13.csv','2013')
    youth_14 = dc_youth(data_dir+'disconnected_youth_14.csv','2014')

    dfs = [youth_09,youth_10,youth_11,youth_12,youth_13,youth_14]

    df = multi_ordered_merge(dfs)

    df = df.sort_values(['GEO.id2','date'])

    geo_md = pd.DataFrame(columns=)
    fred_md = pd.DataFrame(columns=)

    for l in pd.unique(df['GEO.id2'].ravel()):
        series = l
        frame = df[df['GEO.id2'] == series]
        series_id = 'HD01YOUTHACS' + series
        frame.reset_index(inplace=True)
        # frame = frame.sort_values(['date'])
        # frame.drop(['index'], axis=1, inplace=True)
        frame = frame[['date','disconnected_youth']]
        frame.set_index('date', inplace=True)
        frame.columns = [series_id]
    frame.to_csv('output\\' + series_id, sep='\t')

if __name__='__main__':
    main()