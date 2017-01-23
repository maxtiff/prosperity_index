import pandas as pd, os, sys, functools as ft, pycurl as pyc, datetime as dt, re, numpy as np
pd.options.mode.chained_assignment = None  # default='warn'

'''
Housing Burden is defined as a household spending more than 30% of their monthly income on a rent or mortgage.
'''

keep_old = ['GEO.id2','GEO.display-label','HC01_VC155','HC01_VC164','HC01_VC191','HC01_VC159','HC01_VC160',\
            'HC01_VC170','HC01_VC171','HC01_VC196','HC01_VC197']

keep_new = ['GEO.id2','GEO.display-label','HC01_VC157','HC01_VC167','HC01_VC196','HC01_VC161','HC01_VC162',\
            'HC01_VC173','HC01_VC174','HC01_VC201','HC01_VC202']

names = ['fips','county','mortgages','non_mortgages','rent','mort_30_34','mort_35','no_mort_30_34','no_mort_35','rent_30_34','rent_35']

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

# df = pd.ordered_merge(test_result,test6)
df['HD01_VD01'] = pd.to_numeric(df['HD01_VD01'])
df['HD01_VD02'] = pd.to_numeric(df['HD01_VD02'])
df['rate'] = df['HD01_VD02']/df['HD01_VD01']

def multiple_merge(lst_dfs, on):
    reduce_func = lambda left,right: pd.merge(left, right, on=on)

    return ft.reduce(reduce_func, lst_dfs)

dfs = [df_flow_09,df_flow_10,df_net_11,df_net_12,df_net_13]

test = multiple_merge(dfs,'fips')
test = pd.melt(test, id_vars='fips',var_name='Date').sort_values(['fips','Date'])

levels = test['fips'].unique()
