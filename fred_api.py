def open_loc(file_loc,file_url):
    with open(file_loc, 'wb') as f:
        c = pyc.Curl()
        c.setopt(c.URL, file_url)
        c.setopt(c.WRITEDATA, f)
        c.perform()
        c.close()

import requests as req, json,os, pandas as pd

data_dir = os.getcwd()+'\\data\\'
base_url = 'https://api.stlouisfed.org/'
fred_dir=['fred/','geofred/']
type_dir=['release/','series/']
query_start=['series?','group?','data?']
api_key_param = 'api_key='
series_param='series_id='
release_param='release_id='
file_type_param='file_type=json'
tag_param='tag_names='
tags = ['prosperity%20scorecard']
limit_param = 'limit=1'
date_params=['date=','start_date=']
release_ids=['116','148','330','399','406','408','409','410','412','413','414','415','416','417','419','421']
series_ids=list() # populate with get response from release calls

api_key = '7945c845bf4a1f2f7293f551db41d5df'
'''

Take release_ids: 116,148,330,399,406,408,409,410,412,413,414,415,416,417,419,421
https://api.stlouisfed.org/fred/release/series?
                                               release_id=RELEASE_ID_HERE
                                               &api_key=7945c845bf4a1f2f7293f551db41d5df
                                               &tag_names=prosperity%20scorecard
                                               &limit=1

Grab series ids (one from each release) from response and
then insert series_id into:
https://api.stlouisfed.org/geofred/series/group?
                                                series_id=SERIES_ID_HERE
                                                &api_key=7945c845bf4a1f2f7293f551db41d5df
                                                &file_type=json

Grab min and max dates and then insert them into:
https://api.stlouisfed.org/geofred/series/data?
                                               series_id=SERIES_ID_HERE
                                               &api_key=7945c845bf4a1f2f7293f551db41d5df
                                               &file_type=json
                                               &date=MAX_DATE
                                               &start_date=MIN_DATE


'''
payload = {'get': ['NAME,B03002_003E'], 'for': 'county:*','key': 'abeed2f8242a2f5fc4f5b8c1ff0ad4a49dd1b76a'}
r = req.get('http://api.census.gov/data/2015/acs5',params=payload)

# Get data
release_url = base_url + fred_dir[0] + type_dir[0] + query_start[0] + release_param \
    + release_ids[0] + '&' + api_key_param + api_key + '&' + tag_param \
    + tags[0] + '&' + file_type_param + '&' + limit_param

r = req.get(release_url)
r.json()
id = list(r.json().values())[3][0]['id']

# series_ids.append(id)

series_url = base_url + fred_dir[1] + type_dir[1] + query_start[1] + series_param \
    + series_id + '&' + api_key_param + api_key + '&' + file_type_param

s = req.get(series_url)
s.json()
dates ={}
dates['date'] = list(s.json().values())[0][0]['max_date']
dates['start_date'] = list(s.json().values())[0][0]['min_date']

obs_url = base_url + fred_dir[1] + type_dir[1] + query_start[2] + series_param \
    + series_ids[0] + '&' + api_key_param + api_key + '&' + file_type_param + '&' \
    + date_params[0] + list(dates.values())[0] + '&' + date_params[1] \
    + list(dates.values())[1]

obs = req.get(obs_url)

with open('data.txt', 'w') as outfile:
    json.dump(obs.json(),outfile,indent=4, sort_keys=True,\
                      separators=(',', ':'), ensure_ascii=False)

