'''
Housing Burden is defined as a household spending more than 30% of their monthly income on a rent or mortgage.
'''

import pandas as pd
from os import *
from sys import *

dir = '\\data'

test1 = pd.read_csv('housing_affordability_10.csv',encoding='windows-1252',skiprows={1})
test2 = pd.read_csv('housing_affordability_11.csv',encoding='windows-1252',skiprows={1})
test_result = pd.ordered_merge(test1,test2)

test3 = pd.read_csv('housing_affordability_12.csv',encoding='windows-1252',
                    skiprows={1})
test_result = pd.ordered_merge(test_result,test3)

test4 = pd.read_csv('housing_affordability_13.csv',encoding='windows-1252',
                    skiprows={1})
test_result = pd.ordered_merge(test_result,test4)

test5 = pd.read_csv('housing_affordability_14.csv',encoding='windows-1252',
                    skiprows={1})
test_result = pd.ordered_merge(test_result,test5)

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
