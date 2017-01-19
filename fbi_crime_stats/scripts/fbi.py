import pandas as pd, os, sys, functools as ft, pycurl as pyc, datetime as dt, re, difflib as dl
pd.options.mode.chained_assignment = None  # default='warn'.

# def __main__():

state_abbrs = {
        'AK': 'ALASKA',
        'AL': 'ALABAMA',
        'AR': 'ARKANSAS',
        'AS': 'AMERICAN SAMOA',
        'AZ': 'ARIZONA',
        'CA': 'CALIFORNIA',
        'CO': 'COLORADO',
        'CT': 'CONNECTICUT',
        'DC': 'DISTRICT OF COLUMBIA',
        'DE': 'DELAWARE',
        'FL': 'FLORIDA',
        'GA': 'GEORGIA',
        'GU': 'GUAM',
        'HI': 'HAWAII',
        'IA': 'IOWA',
        'ID': 'IDAHO',
        'IL': 'ILLINOIS',
        'IN': 'INDIANA',
        'KS': 'KANSAS',
        'KY': 'KENTUCKY',
        'LA': 'LOUISIANA',
        'MA': 'MASSACHUSETTS',
        'MD': 'MARYLAND',
        'ME': 'MAINE',
        'MI': 'MICHIGAN',
        'MN': 'MINNESOTA',
        'MO': 'MISSOURI',
        'MP': 'NORTHERN MARIANA ISLANDS',
        'MS': 'MISSISSIPPI',
        'MT': 'MONTANA',
        'NA': 'NATIONAL',
        'NC': 'NORTH CAROLINA',
        'ND': 'NORTH DAKOTA',
        'NE': 'NEBRASKA',
        'NH': 'NEW HAMPSHIRE',
        'NJ': 'NEW JERSEY',
        'NM': 'NEW MEXICO',
        'NV': 'NEVADA',
        'NY': 'NEW YORK',
        'OH': 'OHIO',
        'OK': 'OKLAHOMA',
        'OR': 'OREGON',
        'PA': 'PENNSYLVANIA',
        'PR': 'PUERTO RICO',
        'RI': 'RHODE ISLAND',
        'SC': 'SOUTH CAROLINA',
        'SD': 'SOUTH DAKOTA',
        'TN': 'TENNESSEE',
        'TX': 'TEXAS',
        'UT': 'UTAH',
        'VA': 'VIRGINIA',
        'VI': 'VIRGIN ISLANDS',
        'VT': 'VERMONT',
        'WA': 'WASHINGTON',
        'WI': 'WISCONSIN',
        'WV': 'WEST VIRGINIA',
        'WY': 'WYOMING'
}

abr = pd.DataFrame(list(state_abbrs.items()),columns=['state','name'])
states = pd.read_table('..\\state_fips.txt',dtype=str)
state_frame = pd.merge(states, abr, on='state')
counties = pd.read_table('..\\national_county.txt',dtype=str,sep=';')

keep = ['State','County','Violent\ncrime','Property\ncrime','date']
keep_alt = ['State','County','Violent \ncrime','Property \ncrime','date']
keep_alt_2 = ['State','County','Violent Crime','Property Crime','date']
keep_alt_3 = ['State','County','Violent crime','Property crime','date']
# Import data
data_dir = os.getcwd() + '\\data\\'

# Clean data
crime_2015 = pd.read_excel(data_dir + 'crime_15.xls',skiprows={0,1},header=2,skip_footer=8)
crime_2015['State'].replace(to_replace='\s\-\s\w+\sCounties|\d$', value='',inplace=True,regex=True)
crime_2015 = crime_2015.fillna(method='ffill')
crime_2015['date']='2015'
crime_2015=crime_2015.filter(keep,axis=1)
crime_2015=pd.merge(crime_2015,state_frame,left_on='State',right_on='name')
crime_2015['County'].replace(to_replace='County Police Department|County Unified Police Department|Public Safety|Police Department|\d$', value='',inplace=True,regex=True)
crime_2015['locale'] = crime_2015['County'] + ', ' + crime_2015['state']
crime_2015.drop(['State','County','state','name'], axis=1, inplace=True)
crime_2015['locale'] = crime_2015['locale'].apply(lambda x: (dl.get_close_matches(x, counties['county'])[:1] or [None])[0])
crime_2015=pd.merge(crime_2015,counties,left_on='locale',right_on='county')
crime_2015['crime'] = crime_2015.sum(axis=1)

crime_2014= pd.read_excel(data_dir + 'crime_14.xls',skiprows={0,1},header=2,skip_footer=8)
crime_2014['State'].replace(to_replace='\s\-\s\w+\sCounties|\d$', value='',inplace=True,regex=True)
crime_2014= crime_2014.fillna(method='ffill')
crime_2014['date']='2014'
crime_2014=crime_2014.filter(keep,axis=1)
crime_2014=pd.merge(crime_2014,state_frame,left_on='State',right_on='name')
crime_2014['County'].replace(to_replace='County Police Department|County Unified Police Department|Public Safety|Police Department|\d$', value='',inplace=True,regex=True)
crime_2014['locale'] = crime_2014['County'] + ', ' + crime_2014['state']
crime_2014.drop(['State','County','state','name'], axis=1, inplace=True)
crime_2014['locale'] = crime_2014['locale'].apply(lambda x: (dl.get_close_matches(x, counties[\
        'county'])[:1] or [None])[0])
crime_2014=pd.merge(crime_2014,counties,left_on='locale',right_on='county')
crime_2014['crime'] = crime_2014.sum(axis=1)

crime_2013= pd.read_excel(data_dir + 'crime_13.xls',skiprows={0,1},header=2,skip_footer=7)
crime_2013['State'].replace(to_replace='\s\-\s\w+\sCounties|\d$', value='',inplace=True,regex=True)
crime_2013= crime_2013.fillna(method='ffill')
crime_2013['date']='2013'
crime_2013=crime_2013.filter(keep,axis=1)
crime_2013=pd.merge(crime_2013,state_frame,left_on='State',right_on='name')
crime_2013['County'].replace(to_replace='County Police Department|County Unified Police Department|Public Safety|Police Department|\d$', value='',inplace=True,regex=True)
crime_2013['locale'] = crime_2013['County'] + ', ' + crime_2013['state']
crime_2013.drop(['State','County','state','name'], axis=1, inplace=True)
crime_2013['locale'] = crime_2013['locale'].apply(lambda x: (dl.get_close_matches(x, counties[\
        'county'])[:1] or [None])[0])
crime_2013=pd.merge(crime_2013,counties,left_on='locale',right_on='county')
crime_2013['crime'] = crime_2013.sum(axis=1)

crime_2012= pd.read_excel(data_dir + 'crime_12.xls',skiprows={0,1},header=2,skip_footer=7)
crime_2012['State'].replace(to_replace='\s\-\s\w+\sCounties|\d$', value='',inplace=True,regex=True)
crime_2012= crime_2012.fillna(method='ffill')
crime_2012['date']='2012'
crime_2012=crime_2012.filter(keep_alt,axis=1)
crime_2012=pd.merge(crime_2012,state_frame,left_on='State',right_on='name')
crime_2012['County'].replace(to_replace='County Police Department|County Unified Police Department|Public Safety|Police Department|\d$', value='',inplace=True,regex=True)
crime_2012['locale'] = crime_2012['County'] + ', ' + crime_2012['state']
crime_2012.drop(['State','County','state','name'], axis=1, inplace=True)
crime_2012['locale'] = crime_2012['locale'].apply(lambda x: (dl.get_close_matches(x, counties[\
        'county'])[:1] or [None])[0])
crime_2012=pd.merge(crime_2012,counties,left_on='locale',right_on='county')
crime_2012['crime'] = crime_2012.sum(axis=1)

crime_2011= pd.read_excel(data_dir + 'crime_11.xls',skiprows={0,1},header=2,skip_footer=7)
crime_2011['State'].replace(to_replace='\s\-\s+\w+\sCounties|\d$', value='',inplace=True,regex=True)
crime_2011= crime_2011.fillna(method='ffill')
crime_2011['date']='2011'
crime_2011=crime_2011.filter(keep_alt,axis=1)
crime_2011=pd.merge(crime_2011,state_frame,left_on='State',right_on='name')
crime_2011['County'].replace(to_replace='County Police Department|County Unified Police Department|Public Safety|Police Department|\d$', value='',inplace=True,regex=True)
crime_2011['locale'] = crime_2011['County'] + ', ' + crime_2011['state']
crime_2011.drop(['State','County','state','name'], axis=1, inplace=True)
crime_2011['locale'] = crime_2011['locale'].apply(lambda x: (dl.get_close_matches(x, counties[\
        'county'])[:1] or [None])[0])
crime_2011=pd.merge(crime_2011,counties,left_on='locale',right_on='county')
crime_2011['crime'] = crime_2011.sum(axis=1)

crime_2010= pd.read_excel(data_dir + 'crime_10.xls',skiprows={0,1},header=2,skip_footer=7)
crime_2010['State'].replace(to_replace='\s\-\s\w+\sCounties|\d|\n$', value='',inplace=True,regex=True)
crime_2010= crime_2010.fillna(method='ffill')
crime_2010['date']='2010'
crime_2010=crime_2010.filter(keep_alt,axis=1)
crime_2010=pd.merge(crime_2010,state_frame,left_on='State',right_on='name')
crime_2010['County'].replace(to_replace='County Police Department|County Unified Police Department|Public Safety|Police Department|\d$', value='',inplace=True,regex=True)
crime_2010['locale'] = crime_2010['County'] + ', ' + crime_2010['state']
crime_2010.drop(['State','County','state','name'], axis=1, inplace=True)
crime_2010['locale'] = crime_2010['locale'].apply(lambda x: (dl.get_close_matches(x, counties[\
        'county'])[:1] or [None])[0])
crime_2010=pd.merge(crime_2010,counties,left_on='locale',right_on='county')
crime_2010['crime'] = crime_2010.sum(axis=1)

crime_2009= pd.read_excel(data_dir + 'crime_09.xls',skiprows={0,1},header=2,skip_footer=7)
crime_2009['State'].replace(to_replace='\s\-\s\w+\sCounties|\d$', value='',inplace=True,regex=True)
crime_2009= crime_2009.fillna(method='ffill')
crime_2009['date']='2009'
crime_2009=crime_2009.filter(keep_alt_2,axis=1)
crime_2009=pd.merge(crime_2009,state_frame,left_on='State',right_on='name')
crime_2009['County'].replace(to_replace='County Police Department|County Unified Police Department|Public Safety|Police Department|\d$', value='',inplace=True,regex=True)
crime_2009['locale'] = crime_2009['County'] + ', ' + crime_2009['state']
crime_2009.drop(['State','County','state','name'], axis=1, inplace=True)
crime_2009['locale'] = crime_2009['locale'].apply(lambda x: (dl.get_close_matches(x, counties[\
        'county'])[:1] or [None])[0])
crime_2009=pd.merge(crime_2009,counties,left_on='locale',right_on='county')
crime_2009['crime'] = crime_2009.sum(axis=1)

crime_2008= pd.read_excel(data_dir + 'crime_08.xls',skiprows={0,1},header=2,skip_footer=7)
crime_2008['State'].replace(to_replace='\-\w+\sCounties|[^\x00-\x7F]\w+\sCounties|\d|\s$',value='',inplace=True,regex=True)
crime_2008= crime_2008.fillna(method='ffill')
crime_2008['date']='2008'
crime_2008=crime_2008.filter(keep_alt_3,axis=1)
crime_2008=pd.merge(crime_2008,state_frame,left_on='State',right_on='name')
crime_2008['County'].replace(to_replace='County Police Department|County Unified Police Department|Public Safety|Police Department|\d$', value='',inplace=True,regex=True)
crime_2008['locale'] = crime_2008['County'] + ', ' + crime_2008['state']
crime_2008.drop(['State','County','state','name'], axis=1, inplace=True)
crime_2008['locale'] = crime_2008['locale'].apply(lambda x: (dl.get_close_matches(x, counties[\
        'county'])[:1] or [None])[0])
crime_2008=pd.merge(crime_2008,counties,left_on='locale',right_on='county')
crime_2008['crime'] = crime_2008.sum(axis=1)

crime_2007= pd.read_excel(data_dir + 'crime_07.xls',skiprows={0,1},header=2,skip_footer=7)
crime_2007['State'].replace(to_replace='\-\w+\sCounties|[^\x00-\x7F]\w+\sCounties|\d|\s$',value='',inplace=True,regex=True)
crime_2007= crime_2007.fillna(method='ffill')
crime_2007['date']='2007'
crime_2007=crime_2007.filter(keep_alt_3,axis=1)
crime_2007=pd.merge(crime_2007,state_frame,left_on='State',right_on='name')
crime_2007['County'].replace(to_replace='County Police Department|County Unified Police Department|Public Safety|Police Department|\d$', value='',inplace=True,regex=True)
crime_2007['locale'] = crime_2007['County'] + ', ' + crime_2007['state']
crime_2007.drop(['State','County','state','name'], axis=1, inplace=True)
crime_2007['locale'] = crime_2007['locale'].apply(lambda x: (dl.get_close_matches(x, counties[\
        'county'])[:1] or [None])[0])
crime_2007=pd.merge(crime_2007,counties,left_on='locale',right_on='county')
crime_2007['crime'] = crime_2007.sum(axis=1)

crime_2006= pd.read_excel(data_dir + 'crime_06.xls',skiprows={0,1},header=2,skip_footer=8)
crime_2006['State'].replace(to_replace='\-\w+\sCounties|[^\x00-\x7F]\w+\sCounties|\d|\s$',value='',inplace=True,regex=True)
crime_2006= crime_2006.fillna(method='ffill')
crime_2006['date']='2006'
crime_2006=crime_2006.filter(keep_alt_3,axis=1)
crime_2006=pd.merge(crime_2006,state_frame,left_on='State',right_on='name')
crime_2006['County'].replace(to_replace='County Police Department|County Unified Police Department|Public Safety|Police Department|\d$', value='',inplace=True,regex=True)
crime_2006['locale'] = crime_2006['County'] + ', ' + crime_2006['state']
crime_2006.drop(['State','County','state','name'], axis=1, inplace=True)
crime_2006['locale'] = crime_2006['locale'].apply(lambda x: (dl.get_close_matches(x, counties[\
        'county'])[:1] or [None])[0])
crime_2006=pd.merge(crime_2006,counties,left_on='locale',right_on='county')
crime_2006['crime'] = crime_2006.sum(axis=1)

crime_2005= pd.read_excel(data_dir + 'crime_05.xls',skiprows={0,1},header=2,skip_footer=8)
crime_2005['State'].replace(to_replace='\-\w+\sCounties|[^\x00-\x7F]\w+\sCounties|\d|\s$',value='',inplace=True,regex=True)
crime_2005= crime_2005.fillna(method='ffill')
crime_2005['date']='2005'
crime_2005=crime_2005.filter(keep_alt_3,axis=1)
crime_2005=pd.merge(crime_2005,state_frame,left_on='State',right_on='name')
crime_2005['County'].replace(to_replace='County Police Department|County Unified Police Department|Public Safety|Police Department|\d$', value='',inplace=True,regex=True)
crime_2005['locale'] = crime_2005['County'] + ', ' + crime_2005['state']
crime_2005.drop(['State','County','state','name'], axis=1, inplace=True)
crime_2005['locale'] = crime_2005['locale'].apply(lambda x: (dl.get_close_matches(x, counties[\
        'county'])[:1] or [None])[0])
crime_2005=pd.merge(crime_2005,counties,left_on='locale',right_on='county')
crime_2005['crime'] = crime_2005.sum(axis=1)

dfs = ['crime_2015','crime_2014','crime_2013','crime_2012','crime_2011','crime_2010',
       'crime_2009','crime_2008','crime_2007','crime_2006','crime_2005']