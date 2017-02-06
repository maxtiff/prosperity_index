import pandas as pd, os, sys, functools as ft, pycurl as pyc, datetime as dt, re, numpy as np
pd.options.mode.chained_assignment = None  # default='warn'

def preventable_care(file,names,date):
    df = pd.read_excel(file,skiprows={0, 1}, parse_cols={0, 68}, skip_footer=1)
    df.columns = [names]
    df['fips'] = df['fips'].apply(lambda x: "%06d" % (x,))
    df['date'] = date

    return df

def multi_ordered_merge(lst_dfs):
    reduce_func = lambda left,right: pd.ordered_merge(left, right)

    return ft.reduce(reduce_func, lst_dfs)

def main():
    names = ['fips','rate']
    counties = pd.read_table('..\\national_county.txt', dtype=str, sep=';')
    data_dir = os.getcwd() + '\\data\\'

    pc_08 = preventable_care(data_dir+'PC_County_rates_2008.xls',names,'2008')
    pc_09 = preventable_care(data_dir+'PC_County_rates_2009.xls',names,'2009')
    pc_10 = preventable_care(data_dir+'PC_County_rates_2010.xls',names,'2010')
    pc_11 = preventable_care(data_dir+'PC_County_rates_2011.xls',names,'2011')
    pc_12 = preventable_care(data_dir+'PC_County_rates_2012.xls',names,'2012')
    pc_13 = preventable_care(data_dir+'PC_County_rates_2013.xls',names,'2013')
    pc_14 = preventable_care(data_dir+'PC_County_rates_2014.xls',names,'2014')

    dfs = [pc_08,pc_09,pc_10,pc_11,pc_12,pc_13,pc_14]

    df = multi_ordered_merge(dfs)

    df = pd.merge(df, counties, on='fips')

    df = df.sort_values(['fips','date'])

    for series in pd.unique(df['fips'].ravel()):
        frame = df[df['fips'] == series]
        series_id = 'DMPCRATE' + series
        frame.reset_index(inplace=True)
        frame = frame[['date','rate']]
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
    # units = 'Rate'
    # keywords = ''
    # notes = 'The Dartmouth Atlas of Healthcare calculates preventable hospital '\
    #         'admissions by considering the discharges for ambulatory care '\
    #         'sensitive conditions per 1,000 medicare enrollees.'\
    #         '####See http://www.dartmouthatlas.org/downloads/reports/Primary_care_report_090910.pdf for more information.'
    # period = ''
    # g_rate = 'TRUE'
    # obs_vsd = 'TRUE'
    # vsd = '2017-02-03'
    # r_id = '417'
    #
    # non_geo_fips = '002020|002110|002220|002230|002275|006075|008014|015003|042101'
    #
    # non_geo_cats = {'002020': '27406', '002110': '27412', '002220': '27422', \
    #                 '002230': '33516', '002275': '33518', '006075': '27559', \
    #                 '008014': '32077', '015003': '27889', '042101': '29664'}

    #     title = 'Rate of Preventable Hospital Admissions in ' + \
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
