import pandas as pd, os,multi_ordered_merge as merger
pd.options.mode.chained_assignment = None  # default='warn'

def make_request(url,payload):

    r = req.get(url,params=payload,stream=True)

    return r.json()


def racial_pop(county_file,date):



    pass
def main():
    demos = ['B03002_003E','B03002_004E','B03002_005E','B03002_006E','B03002_012E']

    payload = {'get': ['NAME',demos[n]], 'for': 'county:*','key': 'abeed2f8242a2f5fc4f5b8c1ff0ad4a49dd1b76a'}

    df = make_request('http://api.census.gov/data/2009/acs5',params=payload)


    for series in pd.unique(df['fips'].ravel()):
        frame = df[df['fips'] == series]
        frame.reset_index(inplace=True)
        frame.drop(['index'], axis=1, inplace=True)
        for c in demos:
            # for c in ['HD01_VD03','HD01_VD04','HD01_VD05','HD01_VD06','HD01_VD12']:
            series_id = 'B03002' + frame[c].name[-4:] + series
            output = frame[['date', c]]
            output.set_index('date', inplace=True)
            output.columns = [series_id]
            output.to_csv('output\\' + series_id, sep='\t')


if __name__ == '__main__':
    main()
