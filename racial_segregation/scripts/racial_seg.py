import pandas as pd, os, sys, functools as ft, pycurl as pyc, datetime as dt, re, numpy as np,math
pd.options.mode.chained_assignment = None  # default='warn'


def diss_index(county_file,tract_file,date):
    keep_header = ['GEO.id2','HD01_VD01','HD01_VD03','HD01_VD04','HD01_VD06','HD01_VD12']
    tract_names = ['fips','pop','white','black','asian','hispanic']
    county_names = ['fips','total','white_total','black_total','asian_total','hispanic_total']
    # keep_diss = ['blk_diss','asn_diss','esp_diss','nwt_diss']
    keep_diss = ['nwt_diss']

    # Process census tracts
    df_tract = pd.read_csv(tract_file,encoding='windows-1252',skiprows={1},\
                           low_memory=False)
    df_tract = df_tract.filter(keep_header,axis=1)
    df_tract.columns = [tract_names]
    df_tract['fips']=df_tract['fips'].astype(str)
    df_tract['tract']=df_tract.fips.str.extract('(?P<tract>\d{5}$)')
    df_tract['fips']=df_tract['fips'].str[:-6].astype(np.int64)
    df_tract['fips']=df_tract['fips'].apply(lambda x:"%06d" % (x,))

    # Process counties
    df_county= pd.read_csv(county_file,encoding='windows-1252',skiprows={1},\
                           low_memory=False)
    df_county= df_county.filter(keep_header,axis=1)
    df_county.columns = [county_names]
    df_county['fips']=df_county['fips'].apply(lambda x:"%06d" % (x,))

    # Many-to-one merge tracts into counties
    df= pd.merge(df_tract,df_county,on='fips')

    df['pct_white'] = df['white']/df['white_total']
    df['pct_nonwhite'] = (df['black'] + df['asian'] + df['hispanic'])/(df['black_total']+df['asian_total']+df['hispanic_total'])
    df['nonwhite_white'] = abs(df['pct_nonwhite']-df['pct_white'])

    # df['pct_black'] = df['black']/df['black_total']
    # df['pct_asian'] = df['asian']/df['asian_total']
    # df['pct_hispanic'] = df['hispanic']/df['hispanic_total']

    # df['black_white'] = abs(df['pct_black']-df['pct_white'])
    # df['asian_white'] = abs(df['pct_asian']-df['pct_white'])
    # df['hispanic_white'] = abs(df['pct_hispanic']-df['pct_white'])

    # Combine by FIPS
    df=df.groupby(df.fips).sum()

    # Calculate racial disparity
    df['nwt_diss'] = (.5*df['nonwhite_white'])*100
    # df['blk_diss'] = .5*df['black_white']
    # df['asn_diss'] = .5*df['asian_white']
    # df['esp_diss'] = .5*df['hispanic_white']

    # Clean up data frame
    df = df.filter(keep_diss, axis=1)
    df['date']=date
    df.reset_index(level=0, inplace=True)

    return df

def multi_ordered_merge(lst_dfs):
    reduce_func = lambda left,right: pd.ordered_merge(left, right)

    return ft.reduce(reduce_func, lst_dfs)

def main():
    data_dir = os.getcwd() + '\\data\\'
    counties = pd.read_table('..\\national_county.txt', dtype=str, sep=';')

    df_09 = diss_index(data_dir + 'race_county_09.csv',data_dir + 'race_tract_09.csv','2009')
    df_10 = diss_index(data_dir + 'race_county_10.csv',data_dir + 'race_tract_10.csv','2010')
    df_11 = diss_index(data_dir + 'race_county_11.csv',data_dir + 'race_tract_11.csv','2011')
    df_12 = diss_index(data_dir + 'race_county_12.csv',data_dir + 'race_tract_12.csv','2012')
    df_13 = diss_index(data_dir + 'race_county_13.csv',data_dir + 'race_tract_13.csv','2013')
    df_14 = diss_index(data_dir + 'race_county_14.csv',data_dir + 'race_tract_14.csv','2014')
    df_15 = diss_index(data_dir + 'race_county_15.csv',data_dir + 'race_tract_15.csv','2015')

    dfs = [df_09,df_10,df_11,df_12,df_13,df_14,df_15]

    df = multi_ordered_merge(dfs)
    df = pd.merge(df,counties,on='fips')
    df = df.sort_values(['fips','date'])
    df.fillna('.',axis=1,inplace=True)

    for series in pd.unique(df['fips'].ravel()):
        series_id = 'RACEDISPARITY' + series
        frame = df[df['fips'] == series]
        frame.reset_index(inplace=True)
        frame = frame[['date','nwt_diss']]
        frame.set_index('date', inplace=True)
        frame.columns = [series_id]
        frame.to_csv('output\\' + series_id, sep='\t')

if __name__=='__main__':
    main()


    # md_names = ['series_id', 'title', 'season', 'frequency', 'units', \
    #             'keywords', 'notes', 'period_description', 'growth_rates', \
    #             'obs_vsd_use_release_date', 'valid_start_date', 'release_id']
    # fsr_names = ['fred_release_id', 'fred_series_id', 'official',
    #              'valid_start_date']
    # cat_names = ['series_id', 'cat_id']
    #
    # geo_md = pd.DataFrame(columns=md_names)
    # fred_md = pd.DataFrame(columns=md_names)
    # fsr_geo = pd.DataFrame(columns=fsr_names)
    # fsr = pd.DataFrame(columns=fsr_names)
    # fred_cat = pd.DataFrame(columns=cat_names)
    # titles = pd.DataFrame()
    #
    # season = 'Not Seasonally Adjusted'
    # freq = 'Annual'
    # units = 'Percent'
    # keywords = ''
    # notes = 'The Racial Dissimilarity Index measures the percentage of the non-hispanic white population in a county which would have to change Census tracts to equalize the racial distribution between white and non-white population groups across all tracts in the county.'
    # period = ''
    # g_rate = 'TRUE'
    # obs_vsd = 'TRUE'
    # vsd = '2017-02-07'
    # r_id = '419'
    #
    # non_geo_fips = '002020|002110|002220|002230|002275|006075|008014|015003|042101'
    #
    # non_geo_cats = {'002020': '27406', '002110': '27412', '002220': '27422', \
    #                 '002230': '33516', '002275': '33518', '006075': '27559', \
    #                 '008014': '32077', '015003': '27889', '042101': '29664'}

    #     title = 'White to Non-White Racial Dissimilarity Index for ' + \
    #             pd.unique(df[df['fips'] == series]['county'])[0]
    #
    #     # Create metadata files
    #     if bool(re.search(non_geo_fips, series)):
    #         row = pd.DataFrame(data=[
    #             [series_id, title, season, freq, units, keywords, notes, period,
    #              g_rate, obs_vsd, vsd, r_id]], columns=md_names)
    #         fred_md = fred_md.append(row)
    #
    #         row = pd.DataFrame(data=[[r_id, series_id, 'TRUE', vsd]],
    #                            columns=fsr_names)
    #         fsr = fsr.append(row)
    #
    #         cat_id = non_geo_cats[series]
    #         row = pd.DataFrame(data=[[series_id, cat_id]], columns=cat_names)
    #         fred_cat = fred_cat.append(row)
    #     else:
    #         row = pd.DataFrame(data=[[series_id, title, season, freq, units, \
    #                                   keywords, notes, period, g_rate, obs_vsd, \
    #                                   vsd, r_id]], columns=md_names)
    #         geo_md = geo_md.append(row)
    #
    #         row = pd.DataFrame(data=[[r_id, series_id, 'TRUE', vsd]],
    #                            columns=fsr_names)
    #         fsr_geo = fsr_geo.append(row)
    #
    #     title = pd.DataFrame(data=[[title]])
    #     titles = titles.append(title)
    #
    # geo_md.to_csv('fred_series_geo.txt', sep='\t', index=False)
    # fsr_geo.to_csv('fred_series_release_geo.txt', sep='\t', index=False)
    #
    # fred_md.to_csv('fred_series.txt', sep='\t', index=False)
    # fsr.to_csv('fred_series_release.txt', sep='\t', index=False)
    # fred_cat.to_csv('fred_series_in_category.txt', sep='\t', index=False)
    # titles.to_csv('title.txt', sep='\t', index=False, header=False)