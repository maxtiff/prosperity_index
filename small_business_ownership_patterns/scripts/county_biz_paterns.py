import pandas as pd, os, sys, functools as ft, pycurl as pyc, datetime as dt, re, numpy as np,math
pd.options.mode.chained_assignment = None  # default='warn'

def multi_ordered_merge(lst_dfs):
    reduce_func = lambda left,right: pd.ordered_merge(left, right)

    return ft.reduce(reduce_func, lst_dfs)

def small_biz_rate(biz_ptrns,lf,date):

    biz_keep = 'fips|n1_4|n5_9|n10_19|n20_49|n50_99|n100_249|n250_499'
    biz_drop = 'fips$|small_biz'
    biz_df = pd.read_table(biz_ptrns,sep=',',memory_map=True)

    biz_df = biz_df[biz_df.naics == '------']

    biz_df['fipstate']=biz_df['fipstate'].astype(int)
    biz_df['fipstate']=biz_df['fipstate'].apply(lambda x:"%03d" % (x,))
    biz_df['fipstate']=biz_df['fipstate'].astype(str)

    biz_df['fipscty']=biz_df['fipscty'].astype(int)
    biz_df['fipscty']=biz_df['fipscty'].apply(lambda x:"%03d" % (x,))
    biz_df['fipscty']=biz_df['fipscty'].astype(str)

    biz_df['fips']=biz_df['fipstate']+biz_df['fipscty']

    biz_df=biz_df.filter(regex=biz_keep,axis=1)
    biz_df['small_biz']=biz_df.sum(axis=1)
    biz_df.reset_index(level=0, inplace=True)
    biz_df=biz_df.filter(regex=biz_drop,axis=1)

    lf_keep='GEO.id2|HC02_EST_VC01|HC01_EST_VC01'
    lf_drop=['pop','lf_pt']
    lf_names = ['fips','pop','lf_pt']
    lf_df = pd.read_csv(lf,encoding='windows-1252',skiprows={1},\
                        low_memory=False)
    lf_df=lf_df.filter(regex=lf_keep,axis=1)
    lf_df.columns=[lf_names]
    lf_df['fips']=lf_df['fips'].apply(lambda x:"%06d" % (x,))
    lf_df['lf'] = (lf_df['pop'] * lf_df['lf_pt'])/100
    lf_df.drop(lf_drop,axis=1,inplace=True)

    df = pd.merge(lf_df,biz_df,on='fips')
    df['rate'] = (df['small_biz']/df['lf'])*100
    df['date'] = date

    return df

def main():
    data_dir = os.getcwd() + '\\data\\'
    counties = pd.read_table('..\\national_county.txt', dtype=str, sep=';')

    # Read in and process data
    df_09 = small_biz_rate(data_dir+'cbp09co.txt',data_dir+'laborforce_09.csv','2009')
    df_10 = small_biz_rate(data_dir+'cbp10co.txt',data_dir+'laborforce_10.csv','2010')
    df_11 = small_biz_rate(data_dir+'cbp11co.txt',data_dir+'laborforce_11.csv','2011')
    df_12 = small_biz_rate(data_dir+'cbp12co.txt',data_dir+'laborforce_12.csv','2012')
    df_13 = small_biz_rate(data_dir+'cbp13co.txt',data_dir+'laborforce_13.csv','2013')
    df_14 = small_biz_rate(data_dir+'cbp14co.txt',data_dir+'laborforce_14.csv','2014')

    dfs = [df_09,df_10,df_11,df_12,df_13,df_14]

    df = multi_ordered_merge(dfs)
    df = pd.merge(df, counties, on='fips')
    df = df.sort_values(['fips','date'])
    df.fillna('.',axis=1,inplace=True)

    # Create output files
    for series in pd.unique(df['fips'].ravel()):
        frame = df[df['fips'] == series]
        series_id = 'SMLBIZOWN' + series
        frame.reset_index(inplace=True)
        frame = frame[['date','rate']]
        frame.set_index('date', inplace=True)
        frame.columns = [series_id]
        frame.to_csv('output\\' + series_id, sep='\t')

if __name__=='__main__':
    main()

#     md_names = ['series_id', 'title', 'season', 'frequency', 'units', \
#                 'keywords', 'notes', 'period_description', 'growth_rates', \
#                 'obs_vsd_use_release_date', 'valid_start_date', 'release_id']
#     fsr_names = ['fred_release_id', 'fred_series_id', 'official','valid_start_date']
#     cat_names = ['series_id', 'cat_id']
#
#     geo_md = pd.DataFrame(columns=md_names)
#     fred_md = pd.DataFrame(columns=md_names)
#     fsr_geo = pd.DataFrame(columns=fsr_names)
#     fsr = pd.DataFrame(columns=fsr_names)
#     fred_cat = pd.DataFrame(columns=cat_names)
#     titles = pd.DataFrame()
#
#     season = 'Not Seasonally Adjusted'
#     freq = 'Annual'
#     units = 'Rate'
#     keywords = ''
#     notes = 'The small business ownership rate is the number of firms which employ fewer than 500 people, divided by the number of people in the labor force.'
#     period = ''
#     g_rate = 'TRUE'
#     obs_vsd = 'TRUE'
#     vsd = '2017-02-07'
#     r_id = '421'
#
#     non_geo_fips = '002020|002110|002220|002230|002275|006075|008014|015003|042101'
#
#     non_geo_cats = {'002020': '27406', '002110': '27412', '002220': '27422', \
#                     '002230': '33516', '002275': '33518', '006075': '27559', \
#                     '008014': '32077', '015003': '27889', '042101': '29664'}
#         title = 'Small Business Ownership Rate for ' + \
#                 pd.unique(df[df['fips'] == series]['county'])[0]
#
#         # Create metadata files
#         if bool(re.search(non_geo_fips, series)):
#             row = pd.DataFrame(data=[
#                 [series_id, title, season, freq, units, keywords, notes, period,
#                  g_rate, obs_vsd, vsd, r_id]], columns=md_names)
#             fred_md = fred_md.append(row)
#
#             row = pd.DataFrame(data=[[r_id, series_id, 'TRUE', vsd]],
#                                columns=fsr_names)
#             fsr = fsr.append(row)
#
#             cat_id = non_geo_cats[series]
#             row = pd.DataFrame(data=[[series_id, cat_id]], columns=cat_names)
#             fred_cat = fred_cat.append(row)
#         else:
#             row = pd.DataFrame(data=[[series_id, title, season, freq, units, \
#                                       keywords, notes, period, g_rate, obs_vsd, \
#                                       vsd, r_id]], columns=md_names)
#             geo_md = geo_md.append(row)
#
#             row = pd.DataFrame(data=[[r_id, series_id, 'TRUE', vsd]],
#                                columns=fsr_names)
#             fsr_geo = fsr_geo.append(row)
#
#         title = pd.DataFrame(data=[[title]])
#         titles = titles.append(title)
#
#     geo_md.to_csv('fred_series_geo.txt', sep='\t', index=False)
#     fsr_geo.to_csv('fred_series_release_geo.txt', sep='\t', index=False)
#
#     fred_md.to_csv('fred_series.txt', sep='\t', index=False)
#     fsr.to_csv('fred_series_release.txt', sep='\t', index=False)
#     fred_cat.to_csv('fred_series_in_category.txt', sep='\t', index=False)
#     titles.to_csv('title.txt', sep='\t', index=False, header=False)