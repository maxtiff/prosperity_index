import pandas as pd, os, sys, functools as ft, pycurl as pyc, datetime as dt, re
pd.options.mode.chained_assignment = None  # default='warn'

# os.chdir(os.getcwd())

def main():
    names=['date','fips_state','fips_county','region_code','division_code','county_name','1_unit_bldgs','1_unit_units',
           '1_unit_value','2_unit_bldgs','2_unit_units','2_unit_value','34_unit_bldgs','34_unit_units','34_unit_value',
           '5_unit_bldgs','5_unit_units','5_unit_value','1_unit_bldgs_rep','1_unit_units_rep','1_unit_value_rep',
           '2_unit_bldgs_rep','2_unit_units_rep','2_unit_value_rep','34_unit_bldgs_rep','34_unit_units_rep',
           '34_unit_value_rep','5_unit_bldgs_rep','5_unit_units_rep','5_unit_value_rep']

    states = pd.read_table('..\\state_fips.txt',dtype=str)
    counties = pd.read_table('..\\national_county.txt', dtype=str, sep=';')

    df = pd.DataFrame(columns=names)

    for f in os.listdir(os.getcwd()+'\\data\\'):
        if bool(re.search('co\d+a', f)):
            permits = pd.read_table(os.getcwd() + '\\data\\' + f, sep=',',\
                                    converters={'fips_county':str,'fips_state':str},\
                                    header=None, skiprows=[0, 1],names=names)
            df = df.append(permits)

    # Clean some fields
    df.fips_state = df.fips_state.str.strip()
    df.fips_county = df.fips_county.str.strip()
    df.date = df.date.astype(int).astype(str)

    df = pd.merge(df, states, left_on='fips_state', right_on='fips')
    # df['county_name'] = df['county_name'].str.strip()
    # df['county_name'] = df['county_name'] + ', ' + df['state']

    df['fips'] = df['fips_state'] + df['fips_county']
    df.fips = df.fips.astype(int)
    df['fips'] = df['fips'].apply(lambda x: "%06d" % (x,))


    df.drop(['region_code', 'division_code','state','fips_county','fips_state','county_name'], axis=1, inplace=True)
    df.drop(df.filter(regex=('value|rep|units')),axis=1,inplace=True)

    df = pd.merge(df, counties, on='fips')

    md_names = ['series_id', 'title', 'season', 'frequency', 'units', \
                'keywords', 'notes', 'period_description', 'growth_rates', \
                'obs_vsd_use_release_date', 'valid_start_date', 'release_id']
    fsr_names = ['fred_release_id', 'fred_series_id', 'official',\
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
    units = 'Units'
    keywords = ''
    notes = ''
    period = ''
    g_rate = 'TRUE'
    obs_vsd = 'TRUE'
    vsd = '2017-01-27'
    r_id = '148'

    non_geo_fips = '002020|002110|002220|002230|002275|006075|008014|015003|042101'

    non_geo_cats = {'002020': '27406', '002110': '27412', '002220': '27422', \
                    '002230': '33516', '002275': '33518', '006075': '27559', \
                    '008014': '32077', '015003': '27889', '042101': '29664'}

    # Regex pattern to reformat dates before year 2000
    ptn = '9\d99'

    for series in pd.unique(df.fips.ravel()):
        frame = df[df['fips'] == series]
        frame.reset_index(inplace=True)

        for i, d in enumerate(frame['date']):
            if bool(re.search(ptn, d)):
                frame['date'][i] = re.sub(ptn,'19' + re.search(ptn, d).group()[0:2],d)

        frame = frame.sort_values(['date'])
        frame['total_bldgs'] = frame.sum(axis=1)
        frame = frame[['date', 'total_bldgs']]
        frame.set_index('date', inplace=True)
        series_id = 'BPPRIV' + series
        frame.columns = [series_id]
        frame.to_csv('output\\' + series_id, sep='\t')

        title = 'New Private Housing Units Authorized by Building Permits for ' + \
                pd.unique(df[df['fips'] == series]['county'])[0]

        if bool(re.search(non_geo_fips, series)):
            row = pd.DataFrame(
                data=[[series_id, title, season, freq, units, keywords, notes, \
                       period, g_rate, obs_vsd, vsd, r_id]], columns=md_names)
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

if __name__=='__main__':
    main()

# def open_loc(file_loc,file_url):
#     with open(file_loc, 'wb') as f:
#         c = pyc.Curl()
#         c.setopt(c.URL, file_url)
#         c.setopt(c.WRITEDATA, f)
#         c.perform()
#         c.close()
#
#
#
# data_dir = os.getcwd()+'\\data\\'
# base_url = 'http://www2.census.gov/econ/bps/County/'
# county = 'co'
# short_year = dt.datetime.today().strftime('%y')
# long_year = dt.datetime.today().year
# type = ['c','a']
# ext = 'txt'
#
# # Get data
# for y in range(int(short_year)):
#     if y >= 10:
#         year = (str(y))
#     else:
#         year = ('0' + str(y))
#     for m in range(1, 13):
#         if m >= 10:
#             month = (str(m))
#         else:
#             month = ('0'+str(m))
#         filename = county + year + month + type[0] + '.' + ext
#         full_url = base_url + filename
#
#         with open(data_dir + filename, 'wb') as f:
#             c = pyc.Curl()
#             c.setopt(c.URL, full_url)
#             c.setopt(c.WRITEDATA, f)
#             c.perform()
#             c.close()
#
# for l in range(1990,long_year-1):
#     year = str(l)
#     filename = county + year + type[1] + '.' + ext
#     full_url = base_url + filename
#
#     with open(data_dir + filename, 'wb') as f:
#         c = pyc.Curl()
#         c.setopt(c.URL, full_url)
#         c.setopt(c.WRITEDATA, f)
#         c.perform()
#         c.close()

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
    # units = 'Units'
    # keywords = ''
    # notes = ''
    # period = ''
    # g_rate = 'TRUE'
    # obs_vsd = 'TRUE'
    # vsd = '2017-01-27'
    # r_id = '148'
    #
    # non_geo_fips = '002020|002110|002220|002230|002275|006075|008014|015003|042101'
    #
    # non_geo_cats = {'002020': '27406', '002110': '27412', '002220': '27422', \
    #                 '002230': '33516', '002275': '33518', '006075': '27559', \
    #                 '008014': '32077', '015003': '27889', '042101': '29664'}
    #
    # ptn = '9\d99'
    #
    # for series in pd.unique(df.fips.ravel()):
    #     fips = '0'+series
    #
    #     frame = df[df['fips'] == series]
    #     frame.reset_index(inplace=True)
    #     # frame = frame.sort_values(['date'])
    #     frame.drop(['index'], axis=1, inplace=True)
    #     # frame.reset_index(inplace=True)
    #     for i, d in enumerate(frame['date']):
    #         if bool(re.search(ptn, d)):
    #             frame['date'][i] = re.sub(ptn, '19' + re.search(ptn, d).group()[0:2], d)
    #     frame = frame.sort_values(['date'])
    #     frame['total_bldgs'] = frame.sum(axis=1)
    #     frame = frame[['date', 'total_bldgs']]
    #     # frame['date'] = dates
    #     frame.set_index('date', inplace=True)
    #     series_id = 'BPPRIV' + fips
    #     frame.columns = [series_id]
    #     frame.to_csv('output\\' + series_id, sep='\t')
    #
    #     title = 'New Private Housing Units Authorized by Building Permits for ' + \
    #             pd.unique(df[df['fips'] == series]['county_name'])[0]
    #     if bool(re.search(non_geo_fips, series)):
    #         row = pd.DataFrame(
    #             data=[[series_id, title, season, freq, units, keywords, notes, \
    #                    period, g_rate, obs_vsd, vsd, r_id]], columns=md_names)
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