def open_loc(file_loc,file_url):
    with open(file_loc, 'wb') as f:
        c = pyc.Curl()
        c.setopt(c.URL, file_url)
        c.setopt(c.WRITEDATA, f)
        c.perform()
        c.close()

data_dir = os.getcwd()+'\\data\\'
base_url = 'https://api.stlouisfed.org/'
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