import pandas as pd, requests as req, os, argparse
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
    directory = 'output'

    try:
        os.stat(directory)
    except:
        os.mkdir(directory)

    for series in pd.unique(df['fips'].ravel()):
        series_id = api_id + series
        frame = df[df['fips'] == series]
        frame.reset_index(inplace=True)
        frame.drop(['index'], axis=1, inplace=True)
        frame['date'] = date
        output = frame[['date', series]]
        output.set_index('date', inplace=True)
        output.columns = [series_id]
        output.to_csv(os.path.join(directory,series_id), sep='\t')

    pass
def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('id',help='This would be the Census code for the indicator that you want to retrieve.')
    parser.add_argument('year',help='This would be the observation year for the data that you want to retrieve')
    args = parser.parse_args()

    api_key = 'abeed2f8242a2f5fc4f5b8c1ff0ad4a49dd1b76a'

    racial_population = build_df_from_api(args.id,args.id,api_key)
    output_series_files(racial_population,args.id,args.id)

if __name__ == '__main__':
    main()
