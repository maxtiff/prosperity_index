import pandas as pd, os, sys, functools as ft, pycurl as pyc, datetime as dt, re, numpy as np
pd.options.mode.chained_assignment = None  # default='warn'

keep = ['GEO.id2','GEO.display-label','HD01_VD01','HD01_VD10','HD01_VD11','HD01_VD14','HD01_VD15','HD01_VD24',\
        'HD01_VD25','HD01_VD28','HD01_VD29']

regex = ('GEO.id2|GEO.display-label|disconnected_youth|date')

data_dir = os.getcwd() + '\\data\\'

youth_09 = pd.read_csv(data_dir+'disconnected_youth_09.csv',encoding='windows-1252',skiprows={1})
youth_09 = youth_09.filter(keep,axis=1)
youth_09['GEO.id2']=youth_09['GEO.id2'].apply(lambda x:"%06d" % (x,))
youth_09['date'] = '2009'
# youth_09['disconnected_youth']=((youth_09['HD01_VD10'] + youth_09['HD01_VD11'] + youth_09['HD01_VD14'] \
#                                 +youth_09['HD01_VD15'] + youth_09['HD01_VD24'] + youth_09['HD01_VD25'] \
#                                 +youth_09['HD01_VD28'] + youth_09['HD01_VD29'])/youth_09['HD01_VD01'])*100
# youth_09 = youth_09.filter(regex=regex,axis=1)

youth_10 = pd.read_csv(data_dir+'disconnected_youth_10.csv',encoding='windows-1252',skiprows={1})
youth_10 = youth_10.filter(keep,axis=1)
youth_10['GEO.id2']=youth_10['GEO.id2'].apply(lambda x:"%06d" % (x,))
youth_10['date'] = '2010'
# youth_10['disconnected_youth']=((youth_10['HD01_VD10'] + youth_10['HD01_VD11'] + youth_10['HD01_VD14'] \
#                                 +youth_10['HD01_VD15'] + youth_10['HD01_VD24'] + youth_10['HD01_VD25'] \
#                                 +youth_10['HD01_VD28'] + youth_10['HD01_VD29'])/youth_10['HD01_VD01'])*100
# youth_10 = youth_10.filter(regex=regex,axis=1)

youth_11 = pd.read_csv(data_dir+'disconnected_youth_11.csv',encoding='windows-1252',skiprows={1})
youth_11 = youth_11.filter(keep,axis=1)
youth_11['GEO.id2']=youth_11['GEO.id2'].apply(lambda x:"%06d" % (x,))
youth_11['date'] = '2011'
# youth_11['disconnected_youth']=((youth_11['HD01_VD10'] + youth_11['HD01_VD11'] + youth_11['HD01_VD14'] \
#                                 +youth_11['HD01_VD15'] + youth_11['HD01_VD24'] + youth_11['HD01_VD25'] \
#                                 +youth_11['HD01_VD28'] + youth_11['HD01_VD29'])/youth_11['HD01_VD01'])*100
# youth_11 = youth_11.filter(regex=regex,axis=1)

youth_12 = pd.read_csv(data_dir+'disconnected_youth_12.csv',encoding='windows-1252',skiprows={1})
youth_12 = youth_12.filter(keep,axis=1)
youth_12['GEO.id2']=youth_12['GEO.id2'].apply(lambda x:"%06d" % (x,))
youth_12['date'] = '2012'
# youth_12['disconnected_youth']=((youth_12['HD01_VD10'] + youth_12['HD01_VD11'] + youth_12['HD01_VD14'] \
#                                 +youth_12['HD01_VD15'] + youth_12['HD01_VD24'] + youth_12['HD01_VD25'] \
#                                 +youth_12['HD01_VD28'] + youth_12['HD01_VD29'])/youth_12['HD01_VD01'])*100
# youth_12 = youth_12.filter(regex=regex,axis=1)

youth_13 = pd.read_csv(data_dir+'disconnected_youth_13.csv',encoding='windows-1252',skiprows={1})
youth_13 = youth_13.filter(keep,axis=1)
youth_13['GEO.id2']=youth_13['GEO.id2'].apply(lambda x:"%06d" % (x,))
youth_13['date'] = '2013'
# youth_13['disconnected_youth']=((youth_13['HD01_VD10'] + youth_13['HD01_VD11'] + youth_13['HD01_VD14'] \
#                                 +youth_13['HD01_VD15'] + youth_13['HD01_VD24'] + youth_13['HD01_VD25'] \
#                                 +youth_13['HD01_VD28'] + youth_13['HD01_VD29'])/youth_13['HD01_VD01'])*100
# youth_13 = youth_13.filter(regex=regex,axis=1)

youth_14 = pd.read_csv(data_dir+'disconnected_youth_14.csv',encoding='windows-1252',skiprows={1})
youth_14 = youth_14.filter(keep,axis=1)
youth_14['GEO.id2']=youth_14['GEO.id2'].apply(lambda x:"%06d" % (x,))
youth_14['date'] = '2014'
# youth_14['disconnected_youth']=((youth_14['HD01_VD10'] + youth_14['HD01_VD11'] + youth_14['HD01_VD14'] \
#                                 +youth_14['HD01_VD15'] + youth_14['HD01_VD24'] + youth_14['HD01_VD25'] \
#                                 +youth_14['HD01_VD28'] + youth_14['HD01_VD29'])/youth_14['HD01_VD01'])*100
# youth_14 = youth_14.filter(regex=regex,axis=1)

def multi_ordered_merge(lst_dfs):
    reduce_func = lambda left,right: pd.ordered_merge(left, right)

    return ft.reduce(reduce_func, lst_dfs)

dfs = [youth_09,youth_10,youth_11,youth_12,youth_13,youth_14]

df = multi_ordered_merge(dfs)

df['disconnected_youth']=((df['HD01_VD10'] +df['HD01_VD11'] + df['HD01_VD14'] \
                                +df['HD01_VD15'] + df['HD01_VD24'] + df['HD01_VD25'] \
                                +df['HD01_VD28'] + df['HD01_VD29'])/df['HD01_VD01'])*100
df = df.filter(regex=regex, axis=1)
df = df.sort_values(['GEO.id2','date'])

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
