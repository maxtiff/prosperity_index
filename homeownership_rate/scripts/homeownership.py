import pandas as pd, os, sys, functools as ft, pycurl as pyc, datetime as dt, re
pd.options.mode.chained_assignment = None  # default='warn'

dir = os.getcwd()+'\\data\\'


test1 = pd.read_csv(dir+'housingtenure_09.csv',encoding='windows-1252',\
													 skiprows={1})
test1['date'] = '2009'

test2 = pd.read_csv(dir+'housingtenure_10.csv',encoding='windows-1252',\
													 skiprows={1})
test2['date'] = '2010'

test3 = pd.read_csv(dir+'housingtenure_11.csv',encoding='windows-1252',skiprows={1})
test3['date'] = '2011'

test4 = pd.read_csv(dir+'housingtenure_12.csv',encoding='windows-1252',skiprows={1})
test4['date'] = '2012'

test5 = pd.read_csv(dir+'housingtenure_13.csv',encoding='windows-1252',skiprows={1})
test5['date'] = '2013'

test6 = pd.read_csv(dir+'housingtenure_14.csv',encoding='windows-1252',skiprows={1})
test6['date'] = '2014'

test7 = pd.read_csv(dir+'housingtenure_15.csv',encoding='windows-1252',skiprows={1})
test7['date'] = '2015'

# df = pd.ordered_merge(test_result,test6)
# df['HD01_VD01'] = pd.to_numeric(df['HD01_VD01'])
# df['HD01_VD02'] = pd.to_numeric(df['HD01_VD02'])
# df['rate'] = df['HD01_VD02']/df['HD01_VD01']

def multi_ordered_merge(lst_dfs):
    reduce_func = lambda left,right: pd.ordered_merge(left, right)

    return ft.reduce(reduce_func, lst_dfs)

dfs = [test1,test2,test3,test4,test5,test6,test7]

df = multi_ordered_merge(dfs)
df = df.sort_values(['GEO.id2','date'])

df['HD01_VD01'] = pd.to_numeric(df['HD01_VD01'])
df['HD01_VD02'] = pd.to_numeric(df['HD01_VD02'])
df['rate'] = (df['HD01_VD02']/df['HD01_VD01'])*100
df['GEO.id2'] = df['GEO.id2'].astype(int).astype(str)
levels = df['GEO.id2'].unique()

# dates = ['2009','2010','2011','2012','2013','2014']

for series in levels:
	if bool(re.search('\d{5}',series)):
		fips = '0'+series
	elif bool(re.search('\d{4}',series)):
		fips = '00'+series
	series_id = 'hownrateacs' + fips
	frame = df[df['GEO.id2'] == series]
	frame = frame[['date','rate']]
	# frame['date'] = dates
	frame.set_index('date',inplace=True)
	frame.columns = [series_id]
	frame.to_csv('output\\'+series_id,sep='\t')
