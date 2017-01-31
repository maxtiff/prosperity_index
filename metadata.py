md_names = ['series_id', 'title', 'season', 'frequency', 'units',
            'keywords','notes', 'period_description', 'growth_rates',\
            'obs_vsd_use_release_date', 'valid_start_date', 'release_id']
fsr_names = ['fred_release_id', 'fred_series_id', 'official',
             'valid_start_date']
cat_names = ['series_id', 'cat_id']

geo_md = pd.DataFrame(columns=md_names)
fred_md = pd.DataFrame(columns=md_names)
fsr_geo = pd.DataFrame(columns=fsr_names)
fsr = pd.DataFrame(columns=fsr_names)
fred_cat = pd.DataFrame(columns=cat_names)
titles =pd.DataFrame()

season = 'Not Seasonally Adjusted'
freq = '5-years'
units = 'Percent'
keywords = ''
notes = 'Estimate of educational attainment using 5 years of data. '\
        'For more information see Appendix 1 of the ACS General '\
        'Handbook (http://www.census.gov/content/dam/Census/library/publications/2008/acs/ACSGeneralHandbook.pdf). '\
        '####The date of the data is the end of the 5-year period. ' \
        'For example, a value dated 2015 represents data from 2010 to 2015.'
period = ''
g_rate = 'TRUE'
obs_vsd = 'TRUE'
vsd = '2017-01-27'
r_id = '330'

non_geo_fips = '002020|002110|002220|002230|002275|006075|008014|015003|042101'

non_geo_cats = {'002020': '27406', '002110': '27412', '002220': '27422', \
                '002230': '33516', '002275': '33518', '006075': '27559', \
                '008014': '32077', '015003': '27889', '042101': '29664'}

title = 'People 25 Years and Over Who Have Completed an Associate\'s Degree or Higher (5-year estimate) in ' + \
        pd.unique(df[df['fips'] == series]['county'])[0]

# Create metadata files
if bool(re.search(non_geo_fips, series)):
    row = pd.DataFrame(
        data=[[series_id, title, season, freq, units, keywords,notes, \
               period, g_rate, obs_vsd, vsd, r_id]],columns=md_names)
    fred_md = fred_md.append(row)

    row = pd.DataFrame(data=[[r_id, series_id, 'TRUE', vsd]],
                       columns=fsr_names)
    fsr = fsr.append(row)

    cat_id = non_geo_cats[series]
    row = pd.DataFrame(data=[[series_id, cat_id]], columns=cat_names)
    fred_cat = fred_cat.append(row)
else:
    row = pd.DataFrame(data=[[series_id, title, season, freq, units, \
                              keywords,notes, period, g_rate, obs_vsd, \
                              vsd, r_id]],columns=md_names)
    geo_md = geo_md.append(row)

    row = pd.DataFrame(data=[[r_id, series_id, 'TRUE', vsd]],columns=fsr_names)
    fsr_geo = fsr_geo.append(row)
