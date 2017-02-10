def open_loc(file_loc,file_url):
    with open(file_loc, 'wb') as f:
        c = pyc.Curl()
        c.setopt(c.URL, file_url)
        c.setopt(c.WRITEDATA, f)
        c.perform()
        c.close()

import requests as req, json

data_dir = os.getcwd()+'\\data\\'
base_url = 'https://api.stlouisfed.org/'
fred_dir=['fred/','geofred/']
type_dir=['release/','series/']
query_start=['series?','group?','data?']
api_key_param = 'api_key='
series_param='series_id='
release_param='release_id='
file_type='file_type=json'
tag_param='tag_names='
tags = ['prosperity%20scorecard']
limit_param = 'limit=1'
date_params=['date','start_date']
release_ids=['148','330','399','406','408','409','410','412','413','414','415','416','417','419','421']
series_ids=[] # populate with get response from release calls

api_key = '7945c845bf4a1f2f7293f551db41d5df'
'''

Take release_ids -> 148,330,399,406,408,409,410,412,413,414,415,416,417,419,421

https://api.stlouisfed.org/fred/release/series?release_id=RELEASE_ID_HERE'\
&api_key=7945c845bf4a1f2f7293f551db41d5df&tag_names=prosperity%20scorecard&limit=1

Grab series ids (one from each release) from returned item

Then insert series_id into ->
'https://api.stlouisfed.org/geofred/series/group?series_id=SERIES_ID_HERE'\
'&api_key=7945c845bf4a1f2f7293f551db41d5df&file_type=json'

Grab min and max dates

Then->
'https://api.stlouisfed.org/geofred/series/data?series_id=SERIES_ID_HERE'\
'&api_key=7945c845bf4a1f2f7293f551db41d5df&file_type=json&date=MAX_DATE'\
'&start_date=MIN_DATE'

Read through to grab dates and values
'''

# Get data
release_url = base_url + fred_dir[0] + type_dir[0] + query_start[0] + release_param \
    + release_ids[0] + '&' + api_key_param + api_key + '&' + tag_param \
    + tags[0] + '&' + file_type + '&' + limit_param

r = req.get(release_url)
r.json()
id = list(r.json().values())[5][0]['id']

series_ids.append(id)

series_url = base_url + fred_dir[1] + type_dir[0] + query_start[1] + series_param \
    + series_ids[0] + '&' + api_key_param + api_key + '&' + file_type

s = req.get(series_url)
s.json()
dates ={}
dates['date'] = list(s.json().values())[0][0]['max_date']
dates['start_date'] = list(s.json().values())[0][0]['min_date']

obs_url = base_url + fred_dir[1] + type_dir[1] + query_start[2] + series_param \
    + series_ids[0] + '&' + api_key_param + api_key + '&' + file_type + '&' \
    + date_params[0] + list(dates.values())[0] + '&' + date_params[1] \
    + list(dates.values())[1]

obs = req.get(obs_url)
