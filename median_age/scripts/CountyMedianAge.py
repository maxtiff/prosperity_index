import pandas as pd, requests as req, os
pd.options.mode.chained_assignment = None  # default='warn'

def make_request(url,payload):

    r = req.get(url,params=payload,stream=True)

    return r.json()


def build_df_from_api(api_id,date,key):
    frame = pd.DataFrame(columns=['fips'])
    payload = {'get': ['NAME,' + api_id], 'for': 'county:*',
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

def output_series_files(df,api_id,date):
    directory = 'output_test'

    try:
        os.stat(directory)
    except:
        os.mkdir(directory)

    for series in pd.unique(df['fips'].ravel()):
        frame = df[df['fips'] == series]
        frame.reset_index(inplace=True)
        frame.drop(['index'], axis=1, inplace=True)
        series_id = api_id + series
        frame['date'] = date
        output = frame[['date', c]]
        output.set_index('date', inplace=True)
        output.columns = [series_id]
        output.to_csv(os.path.join(directory,series_id), sep='\t')

    pass
def main():

    # demos = cf.DEMOGRPAHICS
    # date = cf.DATE
    # api_key = cf.API_KEY

    api_id='B01002_001E'
    date='2015'
    api_key = 'abeed2f8242a2f5fc4f5b8c1ff0ad4a49dd1b76a'
    racial_population = build_df_from_api(api_id,date,api_key)
    output_series_files(racial_population,api_id,date)


if __name__ == '__main__':
    main()
