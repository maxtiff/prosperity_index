def open_loc(file_loc,file_url):
    with open(file_loc, 'wb') as f:
        c = pyc.Curl()
        c.setopt(c.URL, file_url)
        c.setopt(c.WRITEDATA, f)
        c.perform()
        c.close()

data_dir = os.getcwd()+'\\data\\'
base_url = 'https://api.stlouisfed.org/'
fred_dir=['fred/','geofred/']
type_dir=['series/','release/']
query_start=['series?','group?','data?']
key_param = 'api_key='
series_param='series_id='
release_param='release_id='
file_type='file_type=json'
tag_param='tag_names='
tags = ['prosperity%20scorecard']
date_params=['date','start_date']
release_ids=['148','330','399','406','408','409','410','412','413','414','415','416','417','419','421']
series_ids=[] # populate with calls to releases


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
filename = county + year + month + type[0] + '.' + ext
full_url = base_url + filename
with open(data_dir + filename, 'wb') as f:
    c = pyc.Curl()
    c.setopt(c.URL, full_url)
    c.setopt(c.WRITEDATA, f)
    c.perform()
    c.close()
