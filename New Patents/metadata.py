import pandas as pd, os,multi_ordered_merge as merger,functools as ft, re
pd.options.mode.chained_assignment = None  # default='warn'

# payload = {'get': ['NAME,B03002_003E'], 'for': 'county:*','key': 'abeed2f8242a2f5fc4f5b8c1ff0ad4a49dd1b76a'}

# def make_request(url,payload):
#
#     r = req.get(url,params=payload,stream=True)
#
#     return r.json()

# demos = ['B03002_003E','B03002_004E','B03002_005E','B03002_006E','B03002_012E']
#
# payload = {'get': ['NAME',demos[n]], 'for': 'county:*','key': 'abeed2f8242a2f5fc4f5b8c1ff0ad4a49dd1b76a'}
# r = req.get('http://api.census.gov/data/2009/acs5',params=payload)

def main():
    counties = pd.read_table('..\\national_county.txt', dtype=str, sep=';')
    fips = pd.read_table('list.txt', dtype=str)

    df = pd.merge(counties, fips)

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
    freq = 'Monthly'
    units = 'Patents'
    keywords = ''
    notes = ''
    period = ''
    g_rate = 'TRUE'
    obs_vsd = 'TRUE'
    vsd = '2017-06-06'
    r_id = '432'

    non_geo_fips = '002020|002110|011001|002220|002230|002275|006075|008014|015003|042101'

    non_geo_cats = {'002020': '27406', '002110': '27412', '002220': '27422', \
                    '002230': '33516', '002275': '33518', '006075': '27559', \
                    '008014': '32077', '015003': '27889', '042101': '29664', \
                    '011001': '33508'}


    for series in pd.unique(df['fips'].ravel()):
        frame = df[df['fips'] == series]
        frame.reset_index(inplace=True)
        frame.drop(['index'], axis=1, inplace=True)
        series_id = 'USPTOISSUED' + series
        title = 'New Patent Assignments in ' + \
                pd.unique(df[df['fips'] == series]['county'])[0]
        # Create metadata files
        row = pd.DataFrame(data=[[series_id, title, season, freq, units, \
                                  keywords, notes, period, g_rate, obs_vsd, \
                                  vsd, r_id]], columns=md_names)
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