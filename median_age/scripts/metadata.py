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

def median_age(file,column_name,date):
    df = pd.read_csv(file, encoding='windows-1252', skiprows={1}, \
                         low_memory=False)
    df = df.filter(regex='GEO.id2|'+column_name,axis=1)
    df.rename(columns={'GEO.id2': 'fips',column_name:'median_age'},inplace=True)
    df['fips'] = df['fips'].apply(lambda x: "%06d" % (x,))
    df['date'] = date

    return df

def multi_ordered_merge(lst_dfs):
    reduce_func = lambda left,right: pd.ordered_merge(left, right)

    return ft.reduce(reduce_func, lst_dfs)

def main():
    data_dir = os.getcwd() + '\\data\\'
    counties = pd.read_table('..\\national_county.txt', dtype=str, sep=';')

    df_09 = median_age(data_dir + 'age_09.csv','HC01_EST_VC33','2009')
    df_10 = median_age(data_dir + 'age_10.csv','HC01_EST_VC35','2010')
    df_11 = median_age(data_dir + 'age_11.csv','HC01_EST_VC35','2011')
    df_12 = median_age(data_dir + 'age_12.csv','HC01_EST_VC35','2012')
    df_13 = median_age(data_dir + 'age_13.csv','HC01_EST_VC35','2013')
    df_14 = median_age(data_dir + 'age_14.csv','HC01_EST_VC35','2014')
    df_15 = median_age(data_dir + 'age_15.csv','HC01_EST_VC35','2015')

    dfs = [df_09,df_10,df_11,df_12,df_13,df_14,df_15]

    df = multi_ordered_merge(dfs)
    df = pd.merge(df,counties,on='fips')
    df = df.sort_values(['fips','date'])
    df.fillna('.',axis=1,inplace=True)

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
    units = 'Median Age'
    keywords = ''
    notes = ''
    period = ''
    g_rate = 'TRUE'
    obs_vsd = 'TRUE'
    vsd = '2017-05-17'
    r_id = '430'

    non_geo_fips = '002020|002110|002220|002230|002275|006075|008014|015003|042101'

    non_geo_cats = {'002020': '27406', '002110': '27412', '002220': '27422', \
                    '002230': '33516', '002275': '33518', '006075': '27559', \
                    '008014': '32077', '015003': '27889', '042101': '29664'}


    for series in pd.unique(df['fips'].ravel()):
        frame = df[df['fips'] == series]
        frame.reset_index(inplace=True)
        frame.drop(['index'], axis=1, inplace=True)
        series_id = 'B01002001E' + series
        title = 'Median Age of the Population in ' + \
                pd.unique(df[df['fips'] == series]['county'])[0]
        # Create metadata files
        if bool(re.search(non_geo_fips, series)):
            row = pd.DataFrame(data=[[series_id, title, season, freq, units, \
                                      keywords,notes,period, g_rate, obs_vsd, \
                                      vsd, r_id]],columns=md_names)
            fred_md = fred_md.append(row)

            row = pd.DataFrame(data=[[r_id, series_id, 'TRUE', vsd]], \
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

            # output.columns = [series_id]
            # output.to_csv('output\\' + series_id, sep='\t')

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