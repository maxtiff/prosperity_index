import pandas as pd, os, sys, functools as ft, pycurl as pyc, datetime as dt, re, numpy as np
pd.options.mode.chained_assignment = None  # default='warn'

# os.chdir(os.getcwd()+'\\..\\head_of_household')

def single_parent(file,keep,names,date):
    df = pd.read_csv(file,encoding='windows-1252', \
                     skiprows={1})
    df = df.filter(keep, axis=1)
    df['GEO.id2'] = df['GEO.id2'].apply(lambda x: "%06d" % (x,))
    df.columns = [names]
    df['date'] = date

    return df

def multi_ordered_merge(lst_dfs):
    reduce_func = lambda left,right: pd.ordered_merge(left, right)

    return ft.reduce(reduce_func, lst_dfs)

def main():
    keep = ['GEO.id2', 'HC01_EST_VC08', 'HC03_EST_VC08','HC04_EST_VC08']
    keep_10 = ['GEO.id2', 'HC01_EST_VC11', 'HC03_EST_VC11','HC04_EST_VC11']
    keep_13 = ['GEO.id2', 'HC01_EST_VC10', 'HC03_EST_VC10','HC04_EST_VC10']
    names = ['fips', 'total', 'male', 'female']
    counties = pd.read_table('..\\national_county.txt', dtype=str, sep=';')

    data_dir = os.getcwd() + '\\data\\'

    single_09 = single_parent(data_dir+'head_of_household_09.csv',keep,names,'2009')
    single_10 = single_parent(data_dir+'head_of_household_10.csv',keep_10,names,'2010')
    single_11 = single_parent(data_dir+'head_of_household_11.csv',keep_10,names,'2011')
    single_12 = single_parent(data_dir+'head_of_household_12.csv',keep_10,names,'2012')
    single_13 = single_parent(data_dir+'head_of_household_13.csv',keep_13,names,'2013')
    single_14 = single_parent(data_dir+'head_of_household_14.csv',keep_13,names,'2014')
    single_15 = single_parent(data_dir+'head_of_household_15.csv',keep_13,names,'2015')

    dfs = [single_09,single_10,single_11,single_12,single_13,single_14,single_15]

    df = multi_ordered_merge(dfs)

    df = pd.merge(df, counties, on='fips')

    df = df.sort_values(['fips','date'])

    df['singles'] = ((df['male'] + df['female'])/df['total'])*100

    for l in pd.unique(df['fips'].ravel()):
        series = l
        frame = df[df['fips'] == series]
        series_id = 'S1101SPHOUSE' + series
        frame.reset_index(inplace=True)
        frame = frame[['date','singles']]
        frame.set_index('date', inplace=True)
        frame.columns = [series_id]
        frame.to_csv('output\\' + series_id, sep='\t')


if __name__ == '__main__':
    main()

# Metadata
    # md_names = ['series_id', 'title', 'season', 'frequency', 'units', \
    #             'keywords', 'notes', 'period_description', 'growth_rates', \
    #             'obs_vsd_use_release_date', 'valid_start_date', 'release_id']
    # fsr_names = ['fred_release_id', 'fred_series_id', 'official', \
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
    # notes = 'These data represent single-parent households with their own children '\
    #         'who are younger than 18-years of age as percentage of total households '\
    #         'with their own children who are younger than 18-years of age.####The date '\
    #         'of the data is the end of the 5-year period. For example, a value dated 2015 '\
    #         'represents data from 2010 to 2015.####American Community Survey Table S1101.'
    # period = ''
    # g_rate = 'TRUE'
    # obs_vsd = 'TRUE'
    # vsd = '2017-01-27'
    # r_id = '412'
    #
    # non_geo_fips = '002020|002110|002220|002230|002275|006075|008014|015003|042101'
    #
    # non_geo_cats = {'002020': '27406', '002110': '27412', '002220': '27422', \
    #                 '002230': '33516', '002275': '33518', '006075': '27559', \
    #                 '008014': '32077', '015003': '27889', '042101': '29664'}
    #
    # for l in pd.unique(df['fips'].ravel()):
    #     series = l
    #     frame = df[df['fips'] == series]
    #     series_id = 'S1101SPHOUSE' + series
    #     frame.reset_index(inplace=True)
    #     frame = frame[['date','singles']]
    #     frame.set_index('date', inplace=True)
    #     frame.columns = [series_id]
    #     frame.to_csv('output\\' + series_id, sep='\t')
    #
    #     title = 'Single-parent Households with Children as a Percentage of Households with Children in ' + \
    #             pd.unique(df[df['fips'] == series]['county'])[0]
    #
    #
    #
    #     if bool(re.search(non_geo_fips, series)):
    #         row = pd.DataFrame(
    #             data=[[series_id, title, season, freq, units, keywords, \
    #                    notes, period, g_rate, obs_vsd, vsd, r_id]],\
    #             columns=md_names)
    #         fred_md = fred_md.append(row)
    #
    #         row = pd.DataFrame(data=[[r_id, series_id, 'TRUE', vsd]],\
    #                            columns=fsr_names)
    #         fsr = fsr.append(row)
    #
    #         cat_id = non_geo_cats[series]
    #         row = pd.DataFrame(data=[[series_id, cat_id]], columns=cat_names)
    #         fred_cat = fred_cat.append(row)
    #
    #     else:
    #         row = pd.DataFrame(data=[[series_id, title, season, freq, units, \
    #                                   keywords, notes, period, g_rate, obs_vsd, \
    #                                   vsd, r_id]], \
    #                            columns=md_names)
    #         geo_md = geo_md.append(row)
    #
    #         row = pd.DataFrame(data=[[r_id, series_id, 'TRUE', vsd]], \
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