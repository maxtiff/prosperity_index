import pandas as pd, os, sys, functools as ft, pycurl as pyc, datetime as dt, re
pd.options.mode.chained_assignment = None  # default='warn'

def homeown_rate(file,date):
	df = pd.read_csv(file, encoding='windows-1252',\
						skiprows={1})

	filter = 'GEO.id2|date|rate'

	df['GEO.id2'] = df['GEO.id2'].apply(lambda x: "%06d" % (x,))

	df['HD01_VD01'] = pd.to_numeric(df['HD01_VD01'])
	df['HD01_VD02'] = pd.to_numeric(df['HD01_VD02'])
	df['rate'] = (df['HD01_VD02'] / df['HD01_VD01']) * 100

	df['date'] = date

	return df.filter(regex=filter,axis=1)


def multi_ordered_merge(lst_dfs):
    reduce_func = lambda left,right: pd.ordered_merge(left, right)

    return ft.reduce(reduce_func, lst_dfs)

def main():

	data_dir = os.getcwd()+'\\data\\'

	hown_09 = homeown_rate(data_dir+'housingtenure_09.csv','2009')
	hown_10 = homeown_rate(data_dir+'housingtenure_10.csv','2010')
	hown_11 = homeown_rate(data_dir+'housingtenure_11.csv','2011')
	hown_12 = homeown_rate(data_dir+'housingtenure_12.csv','2012')
	hown_13 = homeown_rate(data_dir+'housingtenure_13.csv','2013')
	hown_14 = homeown_rate(data_dir+'housingtenure_14.csv','2014')
	hown_15 = homeown_rate(data_dir+'housingtenure_15.csv','2015')

	dfs = [hown_09,hown_10,hown_11,hown_12,hown_13,hown_14,hown_15]

	df = multi_ordered_merge(dfs)
	df = df.sort_values(['GEO.id2','date'])

	# levels = df['GEO.id2'].unique()


	for series in pd.unique(df['GEO.id2'].ravel()):
		series_id = 'HOWNRATEACS' + series
		frame = df[df['GEO.id2'] == series]
		frame = frame[['date','rate']]
		# frame['date'] = dates
		frame.set_index('date',inplace=True)
		frame.columns = [series_id]
		frame.to_csv('output\\'+series_id,sep='\t')

if __name__ == '__main__':
	main()


# data_dir = os.getcwd()+'\\data\\'
#
#
# test1 = pd.read_csv(dir+'housingtenure_09.csv',encoding='windows-1252',\
# 													 skiprows={1})
# test1['date'] = '2009'
#
# test2 = pd.read_csv(dir+'housingtenure_10.csv',encoding='windows-1252',\
# 													 skiprows={1})
# test2['date'] = '2010'
#
# test3 = pd.read_csv(dir+'housingtenure_11.csv',encoding='windows-1252',skiprows={1})
# test3['date'] = '2011'
#
# test4 = pd.read_csv(dir+'housingtenure_12.csv',encoding='windows-1252',skiprows={1})
# test4['date'] = '2012'
#
# test5 = pd.read_csv(dir+'housingtenure_13.csv',encoding='windows-1252',skiprows={1})
# test5['date'] = '2013'
#
# test6 = pd.read_csv(dir+'housingtenure_14.csv',encoding='windows-1252',skiprows={1})
# test6['date'] = '2014'
#
# test7 = pd.read_csv(dir+'housingtenure_15.csv',encoding='windows-1252',skiprows={1})
# test7['date'] = '2015'
#
# # df = pd.ordered_merge(test_result,test6)
# # df['HD01_VD01'] = pd.to_numeric(df['HD01_VD01'])
# # df['HD01_VD02'] = pd.to_numeric(df['HD01_VD02'])
# # df['rate'] = df['HD01_VD02']/df['HD01_VD01']