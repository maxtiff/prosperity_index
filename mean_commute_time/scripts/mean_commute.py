import pandas as pd, os, sys, functools as ft, pycurl as pyc, datetime as dt, re, numpy as np
pd.options.mode.chained_assignment = None  # default='warn'

def mean_commute(wf_file,workforce_filter,workforce_names,cm_file,\
                 commute_filter,commute_names,date):

    df_wf = pd.read_csv(wf_file,encoding='windows-1252',skiprows={1})
    df_wf = df_wf.filter(workforce_filter, axis=1)
    df_wf.columns = [workforce_names]
    df_wf['fips'] = df_wf['fips'].apply(lambda x: "%06d" % (x,))

    df_cm = pd.read_csv(cm_file,encoding='windows-1252', skiprows={1})
    df_cm = df_cm.filter(commute_filter,axis=1)
    df_cm.columns = [commute_names]
    df_cm['fips'] = df_cm['fips'].apply(lambda x: "%06d" % (x,))

    df = pd.merge(df_wf, df_cm,on=['fips'])

    df['avg_commute'] = df['commute_time'] / df['commuters']

    df['date'] = date

    return df

def multi_ordered_merge(lst_dfs):
    reduce_func = lambda left,right: pd.ordered_merge(left, right)

    return ft.reduce(reduce_func, lst_dfs)


def main():
    wf_filter = ['GEO.id2','HD01_VD01']
    wf_names = ['fips', 'commuters']

    cm_filter = ['GEO.id2', 'HD01_VD01']
    cm_names= ['fips', 'commute_time']

    data_dir = os.getcwd() + '\\data\\'
    counties = pd.read_table('..\\national_county.txt', dtype=str, sep=';')

    commute_09 = mean_commute(data_dir+'workforce_09.csv',wf_filter,wf_names,\
                              data_dir+'aggregate_commute_09.csv',cm_filter,\
                              cm_names,'2009')
    commute_10 = mean_commute(data_dir+'workforce_10.csv',wf_filter,wf_names,\
                              data_dir+'aggregate_commute_10.csv',cm_filter,\
                              cm_names,'2010')
    commute_11 = mean_commute(data_dir+'workforce_11.csv',wf_filter,wf_names,\
                              data_dir+'aggregate_commute_11.csv',cm_filter,\
                              cm_names,'2011')
    commute_12 = mean_commute(data_dir+'workforce_12.csv',wf_filter,wf_names,\
                              data_dir+'aggregate_commute_12.csv',cm_filter,\
                              cm_names,'2012')
    commute_13 = mean_commute(data_dir+'workforce_13.csv',wf_filter,wf_names,\
                              data_dir+'aggregate_commute_13.csv',cm_filter,\
                              cm_names,'2013')
    commute_14 = mean_commute(data_dir+'workforce_14.csv',wf_filter,wf_names,\
                              data_dir+'aggregate_commute_14.csv',cm_filter,\
                              cm_names,'2014')
    commute_15 = mean_commute(data_dir+'workforce_15.csv',wf_filter,wf_names,\
                              data_dir+'aggregate_commute_15.csv',cm_filter,\
                              cm_names,'2015')

    dfs = [commute_09,commute_10,commute_11,commute_12,commute_13,commute_14,commute_15]

    df = multi_ordered_merge(dfs)

    df = pd.merge(df, counties, on='fips')

    df = df.sort_values(['fips','date'])

    md_names = ['series_id', 'title', 'season', 'frequency', 'units', \
                'keywords', 'notes', 'period_description', 'growth_rates', \
                'obs_vsd_use_release_date', 'valid_start_date', 'release_id']
    fsr_names = ['fred_release_id', 'fred_series_id', 'official',
                 'valid_start_date']
    cat_names = ['series_id', 'cat_id']

    geo_md = pd.DataFrame(columns=md_names)
    fred_md = pd.DataFrame(columns=md_names)
    fsr_geo = pd.DataFrame(columns=fsr_names)
    fsr = pd.DataFrame(columns=fsr_names)
    fred_cat = pd.DataFrame(columns=cat_names)
    titles = pd.DataFrame()

    season = 'Not Seasonally Adjusted'
    freq = 'Annual'
    units = 'Minutes'
    keywords = ''
    notes = 'This series is calculated by dividing the aggregate travel time to '\
            'work for all workers by the total number of workers, 16-years old '\
            'and older, who commute. The data is comprised of estimates found in '\
            'tables B08013 and B08012 of the American Community Survey, respectively.'\
            '####The date of the data is the end of the 5-year period. For '\
            'example, a value dated 2015 represents data from 2010 to 2015.'
    period = ''
    g_rate = 'TRUE'
    obs_vsd = 'TRUE'
    vsd = '2017-02-03'
    r_id = '415'

    non_geo_fips = '002020|002110|002220|002230|002275|006075|008014|015003|042101'

    non_geo_cats = {'002020': '27406', '002110': '27412', '002220': '27422', \
                    '002230': '33516', '002275': '33518', '006075': '27559', \
                    '008014': '32077', '015003': '27889', '042101': '29664'}

    for series in pd.unique(df.fips.ravel()):
        frame = df[df['fips'] == series]
        series_id = 'B080ACS' + series
        frame.reset_index(inplace=True)
        frame = frame[['date', 'avg_commute']]
        frame.set_index('date', inplace=True)
        frame.columns = [series_id]
        frame.to_csv('output\\' + series_id, sep='\t')

        title = 'Mean Commuting Time for Workers in ' + \
                pd.unique(df[df['fips'] == series]['county'])[0]

        # Create metadata files
        if bool(re.search(non_geo_fips, series)):
            row = pd.DataFrame(data=[
                [series_id, title, season, freq, units, keywords, notes, period,
                 g_rate, obs_vsd, vsd, r_id]], columns=md_names)
            fred_md = fred_md.append(row)

            row = pd.DataFrame(data=[[r_id, series_id, 'TRUE', vsd]],
                               columns=fsr_names)
            fsr = fsr.append(row)

            cat_id = non_geo_cats[series]
            row = pd.DataFrame(data=[[series_id, cat_id]], columns=cat_names)
            fred_cat = fred_cat.append(row)
        else:
            row = pd.DataFrame(data=[[series_id, title, season, freq, units, \
                                      keywords, notes, period, g_rate, obs_vsd, \
                                      vsd, r_id]], columns=md_names)
            geo_md = geo_md.append(row)

            row = pd.DataFrame(data=[[r_id, series_id, 'TRUE', vsd]],
                               columns=fsr_names)
            fsr_geo = fsr_geo.append(row)

        title = pd.DataFrame(data=[[title]])
        titles = titles.append(title)

    geo_md.to_csv('fred_series_geo.txt', sep='\t', index=False)
    fsr_geo.to_csv('fred_series_release_geo.txt', sep='\t', index=False)

    fred_md.to_csv('fred_series.txt', sep='\t', index=False)
    fsr.to_csv('fred_series_release.txt', sep='\t', index=False)
    fred_cat.to_csv('fred_series_in_category.txt', sep='\t', index=False)
    titles.to_csv('title.txt', sep='\t', index=False, header=False)

if __name__ == '__main__':
    main()