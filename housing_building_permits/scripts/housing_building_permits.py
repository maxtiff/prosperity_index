import pandas as pd, os, sys, functools as ft, pycurl as pyc, datetime as dt, re
pd.options.mode.chained_assignment = None  # default='warn'

def main():
    names=['date','fips_state','fips_county','region_code','division_code','county_name','1_unit_bldgs','1_unit_units',
           '1_unit_value','2_unit_bldgs','2_unit_units','2_unit_value','34_unit_bldgs','34_unit_units','34_unit_value',
           '5_unit_bldgs','5_unit_units','5_unit_value','1_unit_bldgs_rep','1_unit_units_rep','1_unit_value_rep',
           '2_unit_bldgs_rep','2_unit_units_rep','2_unit_value_rep','34_unit_bldgs_rep','34_unit_units_rep',
           '34_unit_value_rep','5_unit_bldgs_rep','5_unit_units_rep','5_unit_value_rep']

    # states = pd.read_table('..\\state_fips.txt',dtype=str)
    states = pd.read_table('..\\state_fips.txt',dtype=str)

    df = pd.DataFrame(columns=names)

    for f in os.listdir(os.getcwd()+'\\data\\'):
        if bool(re.search('co\d+a', f)):
            # permits = pd.read_table(os.getcwd() + '\\data\\'+f,sep='\,',engine='python',header=None,skiprows=[0,1],names=names)
            permits = pd.read_table(os.getcwd() + '\\data\\' + f, sep=',', converters={'fips_county':str,'fips_state':str}, header=None, skiprows=[0, 1],
                                    names=names)
            # for i, d in enumerate(permits['date']):
            #     if bool(re.search(ptn, permits['date'][i])):
            #         permits['date'][i] = re.sub(ptn, '19' + re.search(ptn, permits['date'][i]).group()[0:2], permits['date'][i])
            df = df.append(permits)
    #
    # df.fips_county= df.fips_county.astype(int).astype(str)
    # df.fips_state = df.fips_state.astype(int).astype(str)
    df.fips_state = df.fips_state.str.strip()
    df.fips_county = df.fips_county.str.strip()

    df = pd.merge(df, states, left_on='fips_state', right_on='fips')
    df['county_name'] = df['county_name'].str.strip()
    df['county_name'] = df['county_name'] + ', ' + df['state']
    df.date = df.date.astype(int).astype(str)
    df['fips'] = df['fips_state'] + df['fips_county']
    df.drop(['region_code', 'division_code','state','fips_county','fips_state'], axis=1, inplace=True)
    df.drop(df.filter(regex=('value|rep|units')),axis=1,inplace=True)
    # df = df.sort_values(['fips','date'])

    levels = df['fips'].unique()

    # dates = ['2009','2010','2011','2012','2013','2014']
    ptn = '9\d99'

    for series in levels:
        fips = '0'+series

        frame = df[df['fips'] == series]
        frame.reset_index(inplace=True)
        # frame = frame.sort_values(['date'])
        frame.drop(['index'], axis=1, inplace=True)
        # frame.reset_index(inplace=True)
        for i, d in enumerate(frame['date']):
            if bool(re.search(ptn, d)):
                frame['date'][i] = re.sub(ptn, '19' + re.search(ptn, d).group()[0:2], d)
        frame = frame.sort_values(['date'])
        frame['total_bldgs'] = frame.sum(axis=1)
        frame = frame[['date', 'total_bldgs']]
        # frame['date'] = dates
        frame.set_index('date', inplace=True)
        series_id = 'BPPRIV' + fips
        frame.columns = [series_id]
        frame.to_csv('output\\' + series_id, sep='\t')

if __name__='__main__':
    main()

# def open_loc(file_loc,file_url):
#     with open(file_loc, 'wb') as f:
#         c = pyc.Curl()
#         c.setopt(c.URL, file_url)
#         c.setopt(c.WRITEDATA, f)
#         c.perform()
#         c.close()
#
#
#
# data_dir = os.getcwd()+'\\data\\'
# base_url = 'http://www2.census.gov/econ/bps/County/'
# county = 'co'
# short_year = dt.datetime.today().strftime('%y')
# long_year = dt.datetime.today().year
# type = ['c','a']
# ext = 'txt'
#
# # Get data
# for y in range(int(short_year)):
#     if y >= 10:
#         year = (str(y))
#     else:
#         year = ('0' + str(y))
#     for m in range(1, 13):
#         if m >= 10:
#             month = (str(m))
#         else:
#             month = ('0'+str(m))
#         filename = county + year + month + type[0] + '.' + ext
#         full_url = base_url + filename
#
#         with open(data_dir + filename, 'wb') as f:
#             c = pyc.Curl()
#             c.setopt(c.URL, full_url)
#             c.setopt(c.WRITEDATA, f)
#             c.perform()
#             c.close()
#
# for l in range(1990,long_year-1):
#     year = str(l)
#     filename = county + year + type[1] + '.' + ext
#     full_url = base_url + filename
#
#     with open(data_dir + filename, 'wb') as f:
#         c = pyc.Curl()
#         c.setopt(c.URL, full_url)
#         c.setopt(c.WRITEDATA, f)
#         c.perform()
#         c.close()
