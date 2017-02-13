def open_loc(file_loc,file_url):
    with open(file_loc, 'wb') as f:
        c = pyc.Curl()
        c.setopt(c.URL, file_url)
        c.setopt(c.WRITEDATA, f)
        c.perform()
        c.close()

'''
First: take release_ids -> 148,330,399,406,408,409,410,412,413,414,415,416,417,419,421

Make get request for each id:
'https://api.stlouisfed.org/fred/release/series?release_id=RELEASE_ID_HERE'\
'&api_key=7945c845bf4a1f2f7293f551db41d5df&tag_names=prosperity%20scorecard&limit=1'

Grab series ids (one from each release) from returned item and then insert series_id into the following query:
'https://api.stlouisfed.org/geofred/series/group?series_id=SERIES_ID_HERE'\
'&api_key=7945c845bf4a1f2f7293f551db41d5df&file_type=json'

Grab min and max dates from the response and insert them into the date(MAX_DATE) and start_date(MIN_DATE) query parameters:
Then->
'https://api.stlouisfed.org/geofred/series/data?series_id=SERIES_ID_HERE'\
'&api_key=7945c845bf4a1f2f7293f551db41d5df&file_type=json&date=MAX_DATE'\
'&start_date=MIN_DATE'

Read through to grab dates and values
'''

import requests as req, os, json

# data_dir = os.getcwd()+'\\data\\'
api_key = '7945c845bf4a1f2f7293f551db41d5df'
base_url = 'https://api.stlouisfed.org/'
fred_dir=['fred/','geofred/']
type_dir=['release/','series/']
query_start=['series?','group?','data?']

api_key_param = {'api_key': api_key}
file_type_param={'file_type':'json'}
tag_param={'tag_names':'prosperity%20scorecard'}
limit_param = {'limit':'1'}
start_date={'start_date':''}
date={'date':''}

release_ids=['148','330','399','406','408','409','410','412','413','414','415','416','417','419','421']
series_ids=[] # populate with get response from release calls
series_param={'series_id':''}
release_param={'release_id':''}

release_url = base_url + fred_dir[0] + type_dir[0] + query_start[0] + release_param \
    + release_ids[0] + '&' + api_key_param + api_key + '&' + tag_param \
    + tags[0] + '&' + file_type + '&' + limit_param

url = base_url + fred_dir[0] + type_dir[0] + query_start[0]
test_params = params
r = req.get(url,params=params,timeout=None)

id = list(r.json().values())[5][0]['id']


# Get data
def series_id_get(url,params,release_id):
    '''
    This functions takes the following parameters --
    :param url:
    :param params:
    :param release_id:
    :return:
    '''
    try:
        r = req.get(url,params=params,timeout=None)
    except req.exceptions.ConnectionError:
        req.status_code = "Connection refused"

    return list(r.json().values())[5][0]['id']

def date_range_get(url,params,series_id):

    try:
        r=req.get(url,params=params,timerout=None)
    except req.exception.ConnectionError:
        req.status_code = "Connection refused"

    date = list(r.json().values())[0][0]['max_date']
    start_date = list(r.json().values())[0][0]['min_date']

    return[date,start_date]

def release_obs_get(url,params,dates):

    try:
        r=req.get(url,params=params,timeout=None)
    except req.exception.ConnectionError:
        req.status_code = 'Connection refused'

    return r.json()



for release_id in release_ids:
    series_id=series_id_get(release_url,payload)
    series_ids.append(series_id)

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
