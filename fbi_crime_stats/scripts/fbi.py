import pandas as pd, os, sys, functools as ft, pycurl as pyc, datetime as dt, re
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

# Import data
data_dir = os.getcwd() + '\\data\\'

test = pd.read_excel(data_dir + 'crime_15.xls',skiprows={0,1},header=2,skip_footer=8)
test['State'].replace(to_replace='\s\-\s\w+\sCounties', value='',inplace=True,regex=True)
test = test.fillna(method='ffill')
test['date']='2015'
test=test.filter(keep,axis=1)
test = pd.merge(test,state_frame,left_on='State',right_on='name')
test['County'].replace(to_replace='County Police Department|County Unified Police Department|Public Safety|Police Department|\d$', value='',inplace=True,regex=True)
test['locale'] = test['County'] + ', ' + test['state']
test.drop(['State', 'County','state','name'], axis=1, inplace=True)
counties['test'] = counties['county'].apply(lambda x: difflib.get_close_matches(x, test['locale'])[:1] or [None])[0]

test1 = pd.read_excel(data_dir + 'crime_14.xls',skiprows={0,1},header=2,skip_footer=8)

test2 = pd.read_table(data_dir + 'crime_05.txt',skiprows={0,1},header=2,skip_footer=6)

test3 = pd.read_excel(data_dir + 'crime_05.xls',skiprows={0,1})