import pandas as pd, os, sys, functools as ft, pycurl as pyc, datetime as dt, re, numpy as np
pd.options.mode.chained_assignment = None  # default='warn'

def edu_attain(file, cols, names, date):

	df = pd.read_csv(file,encoding='windows-1252',skiprows={1},na_values=['(X)','*****'])
	# test1.replace(np.nan,'.', regex=True,inplace=True)
	df['GEO.id2'] = df['GEO.id2'].apply(lambda x: "%06d" % (x,))
	df = df.filter(cols,axis=1)
	df.columns=[names]
	df['date'] = date

	return df

def multi_ordered_merge(lst_dfs):
    reduce_func = lambda left,right: pd.ordered_merge(left, right)

    return ft.reduce(reduce_func, lst_dfs)

keep_09 = ['GEO.id2','GEO.display-label','HC01_EST_VC11','HC01_EST_VC12','HC01_EST_VC13']
keep = ['GEO.id2','GEO.display-label','HC01_EST_VC12','HC01_EST_VC13',\
		   'HC01_EST_VC14']
names = ['fips','county','assc','bach','grad']

data_dir = os.getcwd()+'\\data\\'

edu_09 = edu_attain(data_dir+'educational_attainment_09.csv',keep_09,\
					names,'2009')
edu_10 = edu_attain(data_dir+'educational_attainment_10.csv',keep,\
					names,'2010')
edu_11 = edu_attain(data_dir+'educational_attainment_11.csv',keep,\
					names,'2011')
edu_12 = edu_attain(data_dir+'educational_attainment_11.csv',keep,\
					names,'2012')
edu_13 = edu_attain(data_dir+'educational_attainment_11.csv',keep,\
					names,'2012')
edu_14 = edu_attain(data_dir+'educational_attainment_11.csv',keep,\
					names,'2014')

dfs = [edu_09,edu_10,edu_11,edu_12,edu_13,edu_14]

df = multi_ordered_merge(dfs)

# df.fips = df.fips.astype(int)
df = df.sort_values(['fips','date'])
df.fips = df.fips.astype(str)
# levels = df['fips'].unique()

for series in pd.unique(df['fips'].ravel()):
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
			series_id = series_id+ 'ASSOC' + series
		elif c is 'bach':
			series_id = series_id+ 'BACH' + series
		elif c is 'grad':
			series_id = series_id+ 'GRAD' + series
		elif c is 'total_third':
			series_id = series_id+ 'TOTAL'+ series
		output.columns = [series_id]
		output.to_csv('output\\' + series_id, sep='\t')
