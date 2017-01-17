import pandas as pd, os, sys, functools as ft, pycurl as pyc, datetime as dt, re, numpy as np
pd.options.mode.chained_assignment = None  # default='warn'

keepers_09 = ['GEO.id2','GEO.display-label','HC01_EST_VC11','HC01_EST_VC12','HC01_EST_VC13']
keepers_rest = ['GEO.id2','GEO.display-label','HC01_EST_VC12','HC01_EST_VC13','HC01_EST_VC14']

names = ['fips','county','assc','bach','grad']

dir = os.getcwd()+'\\data\\'

test1 = pd.read_csv(dir+'educational_attainment_09.csv',encoding='windows-1252',\
													 skiprows={1},na_values=['(X)','*****'])
# test1.replace(np.nan,'.', regex=True,inplace=True)
test1['GEO.id2'] = test1['GEO.id2'].astype(int).astype(str)
test1 = test1.filter(keepers_09,axis=1)
test1.columns=[names]
test1['date'] = '2009'

test2 = pd.read_csv(dir+'educational_attainment_10.csv',encoding='windows-1252',\
													 skiprows={1},na_values=['(X)','*****'])
# test1.replace(np.nan,'.', regex=True,inplace=True)
test2['GEO.id2'] = test2['GEO.id2'].astype(int).astype(str)
test2 = test2.filter(keepers_rest,axis=1)
test2.columns=[names]
test2['date'] = '2010'

test3 = pd.read_csv(dir+'educational_attainment_11.csv',encoding='windows-1252',\
													 skiprows={1},na_values=['(X)','*****'])
# test1.replace(np.nan,'.', regex=True,inplace=True)
test3['GEO.id2'] = test3['GEO.id2'].astype(int).astype(str)
test3 = test3.filter(keepers_rest,axis=1)
test3.columns=[names]
test3['date'] = '2011'

test4 = pd.read_csv(dir+'educational_attainment_12.csv',encoding='windows-1252',\
													 skiprows={1},na_values=['(X)','*****'])
# test1.replace(np.nan,'.', regex=True,inplace=True)
test4['GEO.id2'] = test4['GEO.id2'].astype(int).astype(str)
test4 = test4.filter(keepers_rest,axis=1)
test4.columns=[names]
test4['date'] = '2012'

test5 = pd.read_csv(dir+'educational_attainment_13.csv',encoding='windows-1252',\
													 skiprows={1},na_values=['(X)','*****'])
# test1.replace(np.nan,'.', regex=True,inplace=True)
test5['GEO.id2'] = test5['GEO.id2'].astype(int).astype(str)
test5 = test5.filter(keepers_rest,axis=1)
test5.columns=[names]
test5['date'] = '2013'

test6 = pd.read_csv(dir+'educational_attainment_14.csv',encoding='windows-1252',\
													 skiprows={1},na_values=['(X)','*****'])
# test1.replace(np.nan,'.', regex=True,inplace=True)
test6['GEO.id2'] = test6['GEO.id2'].astype(int).astype(str)
test6= test6.filter(keepers_rest,axis=1)
test6.columns=[names]
test6['date'] = '2014'

def multi_ordered_merge(lst_dfs):
    reduce_func = lambda left,right: pd.ordered_merge(left, right)

    return ft.reduce(reduce_func, lst_dfs)

dfs = [test1,test2,test3,test4,test5,test6]

df = multi_ordered_merge(dfs)

df.fips = df.fips.astype(int)
df = df.sort_values(['fips','date'])
df.fips = df.fips.astype(str)
levels = df['fips'].unique()

for series in levels:
	if bool(re.search('\d{5}',series)):
		fips = '0'+series
	elif bool(re.search('\d{4}',series)):
		fips = '00'+series

	frame = df[df['fips'] == series]
	frame.reset_index(inplace=True)
	# frame = frame.sort_values(['date'])
	frame.drop(['index'], axis=1, inplace=True)
	frame['total_third'] = frame.sum(axis=1)

	for c in ['assc','bach','grad','total_third']:
		output = frame[['date', c]]
		# frame['date'] = dates
		output.set_index('date', inplace=True)
		series_id = 'HC01'
		if c is 'assc':
			series_id = series_id+ 'ASSOC' + fips
		elif c is 'bach':
			series_id = series_id+ 'BACH' + fips
		elif c is 'grad':
			series_id = series_id+ 'GRAD' + fips
		elif c is 'total_third':
			series_id = series_id+ 'TOTAL'+ fips
		output.columns = [series_id]
		output.to_csv('output\\' + series_id, sep='\t')
