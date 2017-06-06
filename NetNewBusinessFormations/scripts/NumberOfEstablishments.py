import requests as req, xml.etree.ElementTree as ET, pandas as pd, re, time, os, sys

def request_xml(url,payload):

    MAX_TRIES = 100
    r = None

    for i in range(MAX_TRIES):
        r = req.get(url,params=payload,stream=True)
        try:
            r.raise_for_status() is None
        except:
            r.status_code == 500
            continue
        else:
            break
    else:
        sys.exit()

    return r.text

def load_xml(content):
    return ET.fromstring(content)

def xml_df(xml_data):

    all_records = []
    headers = []

    sentinal = bool(xml_data.findall('record'))
    while sentinal:
        for i, child in enumerate(xml_data):
            record = []
            for subchild in child:
                if bool(re.search('fips|noOfEstablishments', subchild.tag)):
                    record.append(subchild.text)
                    if subchild.tag not in headers:
                        headers.append(subchild.tag)
            all_records.append(record)

        df = pd.DataFrame(all_records, columns=headers)
        df.fips = df.fips.astype(int)
        df.fips = df.fips.apply(lambda x: "%06d" % (x,))

        sentinal = False

    try:
        df
        if isinstance(df,pd.DataFrame):
            return df
    except:
        return pd.DataFrame()

def output_series_files(df):
    directory = 'output'

    try:
        os.stat(directory)
    except:
        os.mkdir(directory)

    for series in pd.unique(df['fips'].ravel()):
        series_id = 'PRIVESTBLMNT' + series
        frame = df[df['fips'] == series]
        frame.drop(['fips'], axis=1, inplace=True)
        output = frame[['date', 'noOfEstablishments']]
        output.set_index('date', inplace=True)
        output.columns = [series_id]
        output.to_csv(os.path.join(directory,series_id), sep='\t')

def main():

    state_df = pd.DataFrame()

    quarters = ['Q1','Q2','Q3','Q4']

    states = ['AK','AL','AR','AZ','CA','CO','CT','DC','DE',\
              'FL','GA','HI','IA','ID','IL','IN','KS','KY',\
              'LA','MA','MD','ME','MI','MN','MO','MS','MT',\
              'NC','ND','NE','NH','NJ','NM','NV','NY','OH',\
              'OK','OR','PA','RI','SC','SD','TN','TX','UT',\
              'VA','VT','WA','WI','WV','WY']

    for s in states:
        for y in range(2001,int(time.strftime('%Y'))):
            for q in quarters:
                payload = {'period': str(y)+'-'+q, 'industry': '10', 'ownerType': '5', \
                       'distribution': 'Quantiles', 'req_type': 'xml'}

                r = request_xml('https://beta.bls.gov/maps/cew/'+s,payload)
                df = xml_df(load_xml(r))

                if not df.empty:
                    print('Processing: ' + s + ' | ' + str(y) + q + '...')
                    df['date'] = str(y)+q
                    df.loc[df['noOfEstablishments'].isnull(), 'noOfEstablishments'] = '.'

                    state_df = state_df.append(df)
                elif df.empty:
                    pass

        state_df = state_df.sort_values(['fips', 'date'])
        output_series_files(state_df)

if __name__ == '__main__':
    main()


