import pandas as pd, requests as req, os, CountyPopulationEstimatesByRaceAndEthnicity_config.py as cf
pd.options.mode.chained_assignment = None  # default='warn'

def make_request(url,payload):

    r = req.get(url,params=payload,stream=True)

    return r.json()


def build_df_from_api(demos,date,key):
    frame = pd.DataFrame(columns=['fips'])
    for d in demos:
        payload = {'get': ['NAME,' + d], 'for': 'county:*',
                   'key': key}

        r = make_request('http://api.census.gov/data/' + date + '/acs5',
                         payload=payload)

        df = pd.DataFrame(r, columns=r[0]).drop(0)
        df = df[df.state != '72']
        df['fips'] = df['state'] + df['county']
        df.fips = df.fips.astype(int)
        df.fips = df.fips.apply(lambda x: "%06d" % (x,))
        df.drop(df.filter(regex=('state|county|NAME')), axis=1, inplace=True)
        frame = pd.merge(frame, df, how='outer', on=['fips'])

    return frame

def output_series_files(df,demos,date):
    os.chdir('..')
    print(os.getcwd())
    for series in pd.unique(df['fips'].ravel()):
        frame = df[df['fips'] == series]
        frame.reset_index(inplace=True)
        frame.drop(['index'], axis=1, inplace=True)
        for c in demos:
            series_id = 'B03002' + frame[c].name[-4:] + series
            frame['date'] = date
            output = frame[['date', c]]
            output.set_index('date', inplace=True)
            output.columns = [series_id]
            output.to_csv(os.getcwd()+'\\output\\' + series_id, sep='\t')

    pass
def main():

    demos = cf.DEMOGRPAHICS
    date = cf.DATE
    api_key = cf.API_KEY

    # demos = ['B03002_003E','B03002_004E','B03002_005E','B03002_006E','B03002_012E']
    # date='2015'
    # api_key = 'abeed2f8242a2f5fc4f5b8c1ff0ad4a49dd1b76a'
    racial_population = build_df_from_api(demos,date,api_key)
    output_series_files(racial_population,demos,date)


if __name__ == '__main__':
    main()
