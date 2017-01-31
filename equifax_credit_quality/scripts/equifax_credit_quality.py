import pandas as pd, os, sys, functools as ft, pycurl as pyc, datetime as dt, re, numpy as np
pd.options.mode.chained_assignment = None  # default='warn'

def main():

    states = pd.read_table('..\\state_fips.txt',dtype=str)
    counties = pd.read_table('..\\national_county.txt',dtype=str,sep=';')

    # Import data
    data_dir = os.getcwd() + '\\data\\'

    df = pd.read_csv(data_dir + 'equifax.csv',parse_dates=['qtr'],low_memory=False,memory_map=True)
    df.fillna(0,axis=1,inplace=True)

    # Get states fips codes and merge with df

    df = pd.merge(df, states, on='state')
    df = df.sort_values(['fips','county_code','qtr'])

    #Drop rows with too small of sample
    df = df[df.num_total >= 20]

    # Clean dates
    df['date'] = df['qtr'].dt.year.astype(str)+'.0'+df['qtr'].dt.quarter.astype(str)
    df.drop(['qtr'],axis=1,inplace=True)

    # Get pct of subprime creditors
    df['pct_below660'] = (df['num_below660']/df['num_total'])*100
    df.reset_index(inplace=True)
    df.drop(['index'], axis=1, inplace=True)

    # Create one fips code
    df.county_code = df.county_code.astype(int)
    df['county_code']=df['county_code'].apply(lambda x:"%03d" % (x,))
    df.county_code = df.county_code.astype(str)

    df.fips = df.fips.astype(int)
    df['fips']=df['fips'].apply(lambda x:"%03d" % (x,))
    df.fips = df.fips.astype(str)

    df.fips = df.fips + df.county_code

    # Remove unnecessary, non-county series
    df = pd.merge(df, counties, on='fips')

    for l in pd.unique(df.fips.ravel()):
        series_id = 'EQFXSUBPRIME' + l
        frame = df[df['fips'] == l]
        output = frame[['date', 'pct_below660']]
        output.set_index('date', inplace=True)
        output.columns = [series_id]
        output.to_csv('output\\' + series_id, sep='\t')

    ### Metadata
    # md_names = ['series_id', 'title', 'season', 'frequency', 'units','keywords',\
    #             'notes', 'period_description', 'growth_rates',\
    #             'obs_vsd_use_release_date', 'valid_start_date', 'release_id']
    # fsr_names = ['fred_release_id', 'fred_series_id', 'official',\
    #              'valid_start_date']
    # cat_names = ['series_id', 'cat_id']
    # titles = pd.DataFrame()
    # geo_md = pd.DataFrame(columns=md_names)
    # fred_md = pd.DataFrame(columns=md_names)
    # fsr_geo = pd.DataFrame(columns=fsr_names)
    # fsr = pd.DataFrame(columns=fsr_names)
    # fred_cat = pd.DataFrame(columns=cat_names)
    #
    # season = 'Not Seasonally Adjusted'
    # freq = 'Quarterly'
    # units = 'Percent'
    # keywords = ''
    # notes = 'Percentage of population sample with a credit score below 660. '\
    #         'Counties with fewer than 20 people in the sample are not reported for privacy reasons.'
    # period = ''
    # g_rate = 'TRUE'
    # obs_vsd = 'TRUE'
    # vsd = '2017-01-27'
    # r_id = '409'
    #
    # non_geo_fips = '002020|002110|002220|002230|002275|006075|008014|015003|042101'
    #
    # non_geo_cats = {'002020': '27406', '002110': '27412', '002220': '27422', \
    #                 '002230': '33516', '002275': '33518', '006075': '27559', \
    #                 '008014': '32077', '015003': '27889', '042101': '29664'}

    # for l in pd.unique(df.fips.ravel()):
    #     series_id = 'EQFXSUBPRIME' + l
    #     frame = df[df['fips'] == l]
    #     output = frame[['date', 'pct_below660']]
    #     output.set_index('date', inplace=True)
    #     output.columns = [series_id]
    #     output.to_csv('output\\' + series_id, sep='\t')

        # Create metadata files
    #     title = 'Equifax Subprime Credit Population for ' + \
    #             pd.unique(df[df['fips'] == l]['county'])[0]
    #
    #     # title = pd.DataFrame(data=[[title]])
    #     # titles = titles.append(title)
    #
    #
    #     if bool(re.search(non_geo_fips, l)):
    #         row = pd.DataFrame(data=[[series_id, title, season, freq, units, keywords, \
    #                    notes, period, g_rate, obs_vsd, vsd, r_id]], \
    #             columns=md_names)
    #         fred_md = fred_md.append(row)
    #
    #         row = pd.DataFrame(data=[[r_id, series_id, 'TRUE', vsd]], \
    #                            columns=fsr_names)
    #         fsr = fsr.append(row)
    #
    #         cat_id = non_geo_cats[l]
    #         row = pd.DataFrame(data=[[series_id, cat_id]], columns=cat_names)
    #         fred_cat = fred_cat.append(row)
    #
    #
    #     else:
    #         row = pd.DataFrame(data=[[series_id, title, season, freq, units, keywords, \
    #                    notes, period, g_rate, obs_vsd, vsd, r_id]], \
    #             columns=md_names)
    #         geo_md = geo_md.append(row)
    #         row = pd.DataFrame(data=[[r_id, series_id, 'TRUE', vsd]],\
    #                                columns=fsr_names)
    #         fsr_geo = fsr_geo.append(row)
    #
    #         # Write metadata files
    #
    # geo_md.to_csv('fred_series_geo.txt', sep='\t', index=False)
    # fsr_geo.to_csv('fred_series_release_geo.txt', sep='\t', index=False)
    #
    # fred_md.to_csv('fred_series.txt', sep='\t', index=False)
    # fsr.to_csv('fred_series_release.txt', sep='\t', index=False)
    # fred_cat.to_csv('fred_series_in_category.txt', sep='\t', index=False)
    # titles.to_csv('titles.txt', index=False, sep='\t', header=False)

if __name__ == '__main__':
    main()


