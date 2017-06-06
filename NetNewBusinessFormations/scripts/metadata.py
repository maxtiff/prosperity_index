import pandas as pd, os, re
pd.options.mode.chained_assignment = None  # default='warn'

def main():
    data_dir = os.getcwd() + '\\data\\'
    counties = pd.read_table('..\\national_county.txt', dtype=str, sep=';')
    fips = pd.read_table(data_dir+'fips_list.txt',dtype=str)
    series_ids = pd.read_table(data_dir+'qcew_list.txt',dtype=str)
    fips_ids = pd.concat([fips,series_ids],axis=1)
    df = pd.merge(fips_ids,counties)


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
    freq = 'Quarterly'
    units = 'Establishments'
    keywords = ''
    notes = 'An establishment is an economic unit, such as a factory, mine, store, or office that produces goods or services. It generally is at a single location and is engaged predominantly in one type of economic activity. Where a single location encompasses two or more distinct activities, these are treated as separate establishments, if separate payroll records are available, and the various activities are classified under different industry codes.'
    period = ''
    g_rate = 'TRUE'
    obs_vsd = 'TRUE'
    vsd = '2017-03-07'
    r_id = '362'

    non_geo_fips = '002020|002110|011001|002220|002230|002275|006075|008014|015003|042101'

    non_geo_cats = {'002020': '27406', '002110': '27412', '002220': '27422', \
                    '002230': '33516', '002275': '33518', '006075': '27559', \
                    '008014': '32077', '015003': '27889', '042101': '29664', \
                    '011001': '33508'}


    for series in pd.unique(df['fips'].ravel()):
        frame = df[df['fips'] == series]
        series_id = frame['series_id'].values[0]

        title = 'Number of Private Establishments for All Industries in ' + \
                pd.unique(frame['county'])[0]

        # Create metadata files
        row = pd.DataFrame(data=[[series_id, title, season, freq, units, \
                                  keywords, notes, period, g_rate, obs_vsd, \
                                  vsd, r_id]], columns=md_names)

        # Check if series geography exists in FRED
        if bool(re.search(non_geo_fips, series)):

            fred_md = fred_md.append(row)

            row = pd.DataFrame(data=[[r_id, series_id, 'TRUE', vsd]], \
                               columns=fsr_names)
            fsr = fsr.append(row)

            cat_id = non_geo_cats[series]
            row = pd.DataFrame(data=[[series_id, cat_id]], columns=cat_names)
            fred_cat = fred_cat.append(row)

        else:

            geo_md = geo_md.append(row)

            row = pd.DataFrame(data=[[r_id, series_id, 'TRUE', vsd]],columns=fsr_names)
            fsr_geo = fsr_geo.append(row)

        title = pd.DataFrame(data=[[title]])
        titles=titles.append(title)

    geo_md.to_csv('fred_series_geo.txt', sep='\t', index=False)
    fsr_geo.to_csv('fred_series_release_geo.txt', sep='\t', index=False)

    fred_md.to_csv('fred_series.txt', sep='\t', index=False)
    fsr.to_csv('fred_series_release.txt', sep='\t', index=False)
    fred_cat.to_csv('fred_series_in_category.txt', sep='\t', index=False)
    titles.to_csv('titles.txt', sep='\t', index=False, header=False)


if __name__=='__main__':
    main()