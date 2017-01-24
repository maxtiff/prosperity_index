import pandas as pd, os, sys, functools as ft, pycurl as pyc, datetime as dt, re, numpy as np
pd.options.mode.chained_assignment = None  # default='warn'

data_dir = os.getcwd() + '\\data\\'

keep_tract = ['GEO.id2','HD01_VD01','HD01_VD03','HD01_VD04','HD01_VD06','HD01_VD12']
tract_names = ['fips','pop','white','black','asian','hispanic']
county_names = ['fips','total','white_total','black_total','asian_total','hispanic_total']

tract_09 = pd.read_csv(data_dir + 'race_tract_09.csv',encoding='windows-1252',skiprows={1})
tract_09 = tract_09.filter(keep_tract,axis=1)
tract_09.columns = [tract_names]
tract_09['fips']=tract_09['fips'].astype(str)
tract_09['tract']=tract_09.fips.str.extract('(?P<tract>\d{5}$)')
tract_09['fips']=tract_09['fips'].str[:-6].astype(np.int64)
tract_09['fips']=tract_09['fips'].apply(lambda x:"%06d" % (x,))
# tract_09=tract_09.groupby(tract_09.fips).sum()
# tract_09.reset_index(level=0,inplace=True)

county_09 = pd.read_csv(data_dir + 'race_county_09.csv',encoding='windows-1252',skiprows={1})
county_09 = county_09.filter(keep_tract,axis=1)
county_09.columns = [county_names]
county_09['fips']=county_09['fips'].apply(lambda x:"%06d" % (x,))


test = pd.merge(tract_09,county_09,on='fips')