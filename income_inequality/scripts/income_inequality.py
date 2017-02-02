import pandas as pd, os, sys, functools as ft, pycurl as pyc, datetime as dt, re, numpy as np
pd.options.mode.chained_assignment = None  # default='warn'

def inequality(file,filter,names,date):
    df = pd.read_csv(file,encoding='windows-1252',skiprows={1})
    df = df.filter(filter,axis=1)
    df.columns=[names]
    df['fips'] = df['fips'].apply(lambda x: "%06d" % (x,))
    df['date'] = date

    df['20_20'] = (df['high_20'] / df['low_20'])

    return df.filter(['fips','date','20_20','county'],axis=1)

def multi_ordered_merge(lst_dfs):
    reduce_func = lambda left,right: pd.ordered_merge(left, right)

    return ft.reduce(reduce_func, lst_dfs)

def main():
    filter = ['GEO.id2', 'HD01_VD02', 'HD01_VD06']
    names = ['fips', 'low_20', 'high_20']
    counties = pd.read_table('..\\national_county.txt', dtype=str, sep=';')
    data_dir = os.getcwd() + '\\data\\'

    gini_10 = inequality(data_dir + 'income_inequality_10.csv', filter, names,'2010')
    gini_11 = inequality(data_dir + 'income_inequality_11.csv', filter, names,'2011')
    gini_12 = inequality(data_dir + 'income_inequality_12.csv', filter, names,'2012')
    gini_13 = inequality(data_dir + 'income_inequality_13.csv', filter, names,'2013')
    gini_14 = inequality(data_dir + 'income_inequality_14.csv', filter, names,'2014')
    gini_15 = inequality(data_dir + 'income_inequality_15.csv', filter, names,'2015')

    dfs = [gini_10,gini_11,gini_12,gini_13,gini_14,gini_15]

    df = multi_ordered_merge(dfs)
    df = pd.merge(df, counties, on='fips')
    df = df.sort_values(['fips','date'])

    for series in pd.unique(df.fips.ravel()):
        frame = df[df['fips'] == series]
        series_id = '2020RATIO' + series
        frame.reset_index(inplace=True)
        frame = frame[['date', '20_20']]
        frame.set_index('date', inplace=True)
        frame.columns = [series_id]
        frame.to_csv('output\\' + series_id, sep='\t')

if __name__ == '__main__':
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
    # units = 'Ratio'
    # keywords = ''
    # notes = 'This data represents the ratio of the mean income for the highest '\
    #         'quintile (top 20 percent) of earners divided by the mean income of the '\
    #         'lowest quintile (bottom 20 percent) of earners in a particular county.'
    # period = ''
    # g_rate = 'TRUE'
    # obs_vsd = 'TRUE'
    # vsd = '2017-01-27'
    # r_id = '414'
    #
    # non_geo_fips = '002020|002110|002220|002230|002275|006075|008014|015003|042101'
    #
    # non_geo_cats = {'002020': '27406', '002110': '27412', '002220': '27422', \
    #                 '002230': '33516', '002275': '33518', '006075': '27559', \
    #                 '008014': '32077', '015003': '27889', '042101': '29664'}
    #
    # for series in pd.unique(df.fips.ravel()):
    #     frame = df[df['fips'] == series]
    #     series_id = '2020RATIO' + series
    #     frame.reset_index(inplace=True)
    #     frame = frame[['date', '20_20']]
    #     frame.set_index('date', inplace=True)
    #     frame.columns = [series_id]
    #     frame.to_csv('output\\' + series_id, sep='\t')
    #
    #     title = 'Income Inequality in ' + \
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
    # titles.to_csv('titles.txt', sep='\t', index=False, header=False)