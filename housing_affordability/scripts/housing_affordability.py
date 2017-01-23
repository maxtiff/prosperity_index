import pandas as pd, os, sys, functools as ft, pycurl as pyc, datetime as dt, re, numpy as np
pd.options.mode.chained_assignment = None  # default='warn'

'''
Housing Burden is defined as a household spending more than 30% of their monthly income on a rent or mortgage.
'''

def multi_ordered_merge(lst_dfs):
    reduce_func = lambda left,right: pd.ordered_merge(left, right)

    return ft.reduce(reduce_func, lst_dfs)

keep_old = ['GEO.id2','GEO.display-label','HC01_VC155','HC01_VC164','HC01_VC191','HC01_VC159','HC01_VC160',\
            'HC01_VC170','HC01_VC171','HC01_VC196','HC01_VC197']

keep_new = ['GEO.id2','GEO.display-label','HC01_VC157','HC01_VC167','HC01_VC196','HC01_VC161','HC01_VC162',\
            'HC01_VC173','HC01_VC174','HC01_VC201','HC01_VC202']

names = ['fips','county','mortgages','non_mortgages','rent','mort_30_34','mort_35','no_mort_30_34','no_mort_35',\
         'rent_30_34','rent_35']

data_dir = os.getcwd()+'\\data\\'

house_10 = pd.read_csv(data_dir + 'housing_affordability_10.csv',encoding='windows-1252',skiprows={1})
house_10 = house_10.filter(keep_old,axis=1)
house_10['GEO.id2']=house_10['GEO.id2'].apply(lambda x:"%06d" % (x,))
house_10.columns=[names]
house_10['date'] = '2010'

house_11 = pd.read_csv(data_dir + 'housing_affordability_11.csv',encoding='windows-1252',skiprows={1})
house_11 = house_11.filter(keep_old,axis=1)
house_11['GEO.id2']=house_11['GEO.id2'].apply(lambda x:"%06d" % (x,))
house_11.columns=[names]
house_11['date'] = '2011'

house_12 = pd.read_csv(data_dir + 'housing_affordability_12.csv',encoding='windows-1252',skiprows={1})
house_12 = house_12.filter(keep_old,axis=1)
house_12['GEO.id2']=house_12['GEO.id2'].apply(lambda x:"%06d" % (x,))
house_12.columns=[names]
house_12['date'] = '2012'

house_13 = pd.read_csv(data_dir + 'housing_affordability_13.csv',encoding='windows-1252',skiprows={1})
house_13 = house_13.filter(keep_new,axis=1)
house_13['GEO.id2']=house_13['GEO.id2'].apply(lambda x:"%06d" % (x,))
house_13.columns=[names]
house_13['date'] = '2013'

house_14 = pd.read_csv(data_dir + 'housing_affordability_14.csv',encoding='windows-1252',skiprows={1})
house_14 = house_14.filter(keep_new,axis=1)
house_14['GEO.id2']=house_14['GEO.id2'].apply(lambda x:"%06d" % (x,))
house_14.columns=[names]
house_14['date'] = '2014'

dfs = [house_10,house_11,house_12,house_13,house_14]

df = multi_ordered_merge(dfs,'fips')
df = df.sort_values(['fips','date'])

df['burdened'] = (df['mort_30_34'] + df['mort_35'] + df['no_mort_30_34'] + df['no_mort_35'] + df['rent_30_34'] \
                  + df['rent_35'])/(df['mortgages'] + df['non_mortgages'] + df['rent'])*100

for l in pd.unique(df['fips'].ravel()):
    series = l
    frame = df[df['fips'] == series]
    series_id = 'BURDENED' + series
    frame.reset_index(inplace=True)
    # frame = frame.sort_values(['date'])
    # frame.drop(['index'], axis=1, inplace=True)
    frame = frame[['date','burdened']]
    frame.set_index('date', inplace=True)
    frame.columns = [series_id]
    frame.to_csv('output\\' + series_id, sep='\t')