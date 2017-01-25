import pandas as pd, os, sys, functools as ft, pycurl as pyc, datetime as dt, re, numpy as np
pd.options.mode.chained_assignment = None  # default='warn'

def single_parent(file,keep,names,date):
    df = pd.read_csv(file,encoding='windows-1252',\
                     skiprows={1, 2})
    df = df.filter(keep, axis=1)
    df['GEO.id2'] = df['GEO.id2'].apply(lambda x: "%06d" % (x,))
    df.columns = [names]
    df['date'] = date

    return df

def multi_ordered_merge(lst_dfs):
    reduce_func = lambda left,right: pd.ordered_merge(left, right)

    return ft.reduce(reduce_func, lst_dfs)

def main():
    keep = ['GEO.id2', 'GEO.display-label', 'HC01_EST_VC08', 'HC03_EST_VC08',
            'HC04_EST_VC08']
    keep_10 = ['GEO.id2', 'GEO.display-label', 'HC01_EST_VC11', 'HC03_EST_VC11',
               'HC04_EST_VC11']
    keep_13 = ['GEO.id2', 'GEO.display-label', 'HC01_EST_VC10', 'HC03_EST_VC10',
               'HC04_EST_VC10']

    names = ['fips', 'county', 'total', 'male', 'female']

    data_dir = os.getcwd() + '\\data\\'

    single_09 = single_parent(data_dir+'head_of_household_09.csv',keep,names,\
                              '2009')
    single_10 = single_parent(data_dir+'head_of_household_10.csv',keep_10,names,\
                              '2010')
    single_11 = single_parent(data_dir+'head_of_household_11.csv',keep_10,names,\
                              '2011')
    single_12 = single_parent(data_dir+'head_of_household_12.csv', keep_10,names,\
                              '2012')
    single_13 = single_parent(data_dir+'head_of_household_13.csv', keep_13,names,\
                              '2013')
    single_14 = single_parent(data_dir+'head_of_household_14.csv', keep_13,names,\
                              '2014')

    dfs = [single_09,single_10,single_11,single_12,single_13,single_14]

    df = multi_ordered_merge(dfs)

    df = df.sort_values(['fips','date'])
    df['singles'] = ((df['male'] + df['female'])/df['total'])*100

    for l in pd.unique(df['fips'].ravel()):
        series = l
        frame = df[df['fips'] == series]
        series_id = 'SPHOUSE' + series
        frame.reset_index(inplace=True)
        # frame = frame.sort_values(['date'])
        # frame.drop(['index'], axis=1, inplace=True)
        frame = frame[['date','singles']]
        frame.set_index('date', inplace=True)
        frame.columns = [series_id]
        frame.to_csv('output\\' + series_id, sep='\t')

if __name__ == '__main__':
    main()


# single_09 = pd.read_csv(data_dir+'head_of_household_09.csv',encoding='windows-1252',skiprows={1,2})
# single_09 = single_09.filter(keep,axis=1)
# single_09['GEO.id2']=single_09['GEO.id2'].apply(lambda x:"%06d" % (x,))
# single_09.columns=[names]
# single_09['date'] = '2009'
#
# single_10 = pd.read_csv(data_dir+'head_of_household_10.csv',encoding='windows-1252',skiprows={1,2})
# single_10 = single_10.filter(keep_10,axis=1)
# single_10['GEO.id2']=single_10['GEO.id2'].apply(lambda x:"%06d" % (x,))
# single_10.columns=[names]
# single_10['date'] = '2010'
#
# single_11 = pd.read_csv(data_dir+'head_of_household_11.csv',encoding='windows-1252',skiprows={1,2})
# single_11 = single_11.filter(keep_10,axis=1)
# single_11['GEO.id2']=single_11['GEO.id2'].apply(lambda x:"%06d" % (x,))
# single_11.columns=[names]
# single_11['date'] = '2011'
#
# single_12 = pd.read_csv(data_dir+'head_of_household_12.csv',encoding='windows-1252',skiprows={1,2})
# single_12 = single_12.filter(keep_10,axis=1)
# single_12['GEO.id2']=single_12['GEO.id2'].apply(lambda x:"%06d" % (x,))
# single_12.columns=[names]
# single_12['date'] = '2012'
#
# single_13 = pd.read_csv(data_dir+'head_of_household_13.csv',encoding='windows-1252',skiprows={1,2})
# single_13 = single_13.filter(keep_13,axis=1)
# single_13['GEO.id2']=single_13['GEO.id2'].apply(lambda x:"%06d" % (x,))
# single_13.columns=[names]
# single_13['date'] = '2013'
#
# single_14 = pd.read_csv(data_dir+'head_of_household_14.csv',encoding='windows-1252',skiprows={1,2})
# single_14 = single_14.filter(keep_13,axis=1)
# single_14['GEO.id2']=single_14['GEO.id2'].apply(lambda x:"%06d" % (x,))
# single_14.columns=[names]
# single_14['date'] = '2014'