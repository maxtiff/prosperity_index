def open_loc(file_loc,file_url):
    with open(file_loc, 'wb') as f:
        c = pyc.Curl()
        c.setopt(c.URL, file_url)
        c.setopt(c.WRITEDATA, f)
        c.perform()
        c.close()

data_dir = os.getcwd()+'\\data\\'
base_url = 'https://api.stlouisfed.org/'
key_param = 'api_key='
api_key = '7945c845bf4a1f2f7293f551db41d5df'
'''

Take release_ids -> 148,330,399,403
https://api.stlouisfed.org/fred/release/series?release_id=330'\
&api_key=7945c845bf4a1f2f7293f551db41d5df&tag_names=prosperity%20scorecard&limit=1

Take tag (prosperity scorecard)

Grab series ids (one from each release)

Then ->
'https://api.stlouisfed.org/geofred/series/group?series_id=netmignacs001001'\
'&api_key=7945c845bf4a1f2f7293f551db41d5df&file_type=json'

Grab min and max dates

Then->
'https://api.stlouisfed.org/geofred/series/data?series_id=netmignacs001001'\
'&api_key=7945c845bf4a1f2f7293f551db41d5df&file_type=json&date=2013-01-01'\
'&start_date=2009-01-01'

Grab dates and values a
'''
county = 'co'
short_year = dt.datetime.today().strftime('%y')
long_year = dt.datetime.today().year
type = ['c','a']
ext = 'txt'

# Get data
for y in range(int(short_year)):
    if y >= 10:
        year = (str(y))
    else:
        year = ('0' + str(y))
    for m in range(1, 13):
        if m >= 10:
            month = (str(m))
        else:
            month = ('0'+str(m))
        filename = county + year + month + type[0] + '.' + ext
        full_url = base_url + filename

        with open(data_dir + filename, 'wb') as f:
            c = pyc.Curl()
            c.setopt(c.URL, full_url)
            c.setopt(c.WRITEDATA, f)
            c.perform()
            c.close()

for l in range(1990,long_year-1):
    year = str(l)
    filename = county + year + type[1] + '.' + ext
    full_url = base_url + filename

    with open(data_dir + filename, 'wb') as f:
        c = pyc.Curl()
        c.setopt(c.URL, full_url)
        c.setopt(c.WRITEDATA, f)
        c.perform()
        c.close()