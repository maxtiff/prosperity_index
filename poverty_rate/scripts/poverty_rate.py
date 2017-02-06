import pandas as pd, os, sys, functools as ft, pycurl as pyc, datetime as dt, re, numpy as np
pd.options.mode.chained_assignment = None  # default='warn'

def poverty(file,filter,names,date):
    df = pd.read_csv(file,encoding='windows-1252', skiprows={1},\
                     low_memory=False)
    df = df.filter(filter, axis=1)
    df.columns = [names]
    df['fips'] = df['fips'].apply(lambda x: "%06d" % (x,))
    df['date'] = date

    return df

def multi_ordered_merge(lst_dfs):
    reduce_func = lambda left,right: pd.ordered_merge(left, right)

    return ft.reduce(reduce_func, lst_dfs)

def main():
    filter = ['GEO.id2', 'HC03_EST_VC01']
    names = ['fips','poverty']
    counties = pd.read_table('..\\national_county.txt', dtype=str, sep=';')
    data_dir = os.getcwd() + '\\data\\'

    poverty_12 = poverty(data_dir + 'povertyrate_12.csv', filter, names, '2012')
    poverty_13 = poverty(data_dir + 'povertyrate_13.csv', filter, names, '2013')
    poverty_14 = poverty(data_dir + 'povertyrate_14.csv', filter, names, '2014')
    poverty_15 = poverty(data_dir + 'povertyrate_15.csv', filter, names, '2015')

    dfs = [poverty_12,poverty_13,poverty_14,poverty_15]

    df = multi_ordered_merge(dfs)

    df = pd.merge(df, counties, on='fips')

    df = df.sort_values(['fips', 'date'])

    for l in pd.unique(df['fips'].ravel()):
        series = l
        frame = df[df['fips'] == series]
        series_id = 'S1701ACS' + series
        frame.reset_index(inplace=True)
        frame = frame[['date','poverty']]
        frame.set_index('date', inplace=True)
        frame.columns = [series_id]
        frame.to_csv('output\\' + series_id, sep='\t')

if __name__=='__main__':
    main()

    # md_names = ['series_id', 'title', 'season', 'frequency', 'units', \
    #             'keywords', 'notes', 'period_description', 'growth_rates', \
    #             'obs_vsd_use_release_date', 'valid_start_date', 'release_id']
    # fsr_names = ['fred_release_id', 'fred_series_id', 'official',\
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
    # notes = 'This data comes from Table S1701 of the American Community Survey.####The date of the data is the end of the 5-year period. For example, a value dated 2015 represents data from 2010 to 2015.'
    # period = ''
    # g_rate = 'TRUE'
    # obs_vsd = 'TRUE'
    # vsd = '2017-02-03'
    # r_id = '416'
    #
    # non_geo_fips = '002020|002110|002220|002230|002275|006075|008014|015003|042101'
    #
    # non_geo_cats = {'002020': '27406', '002110': '27412', '002220': '27422', \
    #                 '002230': '33516', '002275': '33518', '006075': '27559', \
    #                 '008014': '32077', '015003': '27889', '042101': '29664'}

    #     title = 'Percent of Population Below the Poverty Level in  ' + \
    #             pd.unique(df[df['fips'] == series]['county'])[0]
    #
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