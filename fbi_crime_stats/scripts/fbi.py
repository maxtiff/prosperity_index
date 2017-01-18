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

# Import data
data_dir = os.getcwd() + '\\data\\'

test = pd.read_excel(data_dir + 'crime_15.xls',skiprows={0,1},header=2,skip_footer=8)

test1 = pd.read_excel(data_dir + 'crime_14.xls',skiprows={0,1},header=2,skip_footer=8)

test2 = pd.read_table(data_dir + 'crime_05.txt',skiprows={0,1},header=2)