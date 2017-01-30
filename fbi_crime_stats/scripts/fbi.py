import pandas as pd, os, sys, functools as ft, pycurl as pyc, datetime as dt, re, difflib as dl
pd.options.mode.chained_assignment = None  # default='warn'.

def fbi_crime_stats(file, footer, date,states,counties):
   keep = 'State|County|Violent|Property|date'
   names = ['violent', 'property', 'date', 'county', 'fips', 'crime']
   df = pd.read_excel(file, skiprows={0, 1}, header=2, skip_footer=footer)

   df['State'].replace(to_replace='[^\x00-\x7F]\w+\sCounties|\s\-\s\w+\sCounties'\
                                  '|\-\w+\sCounties|\d|\n|\s$',value='', \
                       inplace=True, regex=True)

   df = df.fillna(method='ffill')

   df['date'] = date

   df = df.filter(regex=keep, axis=1)

   df = pd.merge(df, states, left_on='State', right_on='name')

   df['County'].replace(to_replace='\d|County Police Department|'\
           'County Unified Police Department|Public Safety|Police Department|\d+|\n$',\
                        value='', inplace=True, regex=True)

   df['locale'] = df['County'] + ', ' + df['state']

   df.drop(['State', 'County', 'state', 'name'], axis=1, inplace=True)

   df['locale'] = df['locale'].apply(lambda x: (dl.get_close_matches(x,counties['county'])[:1] or [None])[0])

   df = pd.merge(df, counties, left_on='locale', right_on='county')

   df['crime'] = df.sum(axis=1)

   df = df.filter(regex=('Violent|Property|date|fips_y|crime|locale'), axis=1)

   df.columns = [names]

   return df

def multi_ordered_merge(lst_dfs):
   reduce_func = lambda left,right: pd.ordered_merge(left, right)

   return ft.reduce(reduce_func, lst_dfs)

def main():
   state_abbrs = {
       'AK': 'ALASKA','AL': 'ALABAMA','AR': 'ARKANSAS','AS': 'AMERICAN SAMOA','AZ': 'ARIZONA',
       'CA': 'CALIFORNIA','CO': 'COLORADO','CT': 'CONNECTICUT','DC': 'DISTRICT OF COLUMBIA',
       'DE': 'DELAWARE','FL': 'FLORIDA','GA': 'GEORGIA','GU': 'GUAM','HI': 'HAWAII',
       'IA': 'IOWA','ID': 'IDAHO','IL': 'ILLINOIS','IN': 'INDIANA','KS': 'KANSAS',
       'KY': 'KENTUCKY','LA': 'LOUISIANA','MA': 'MASSACHUSETTS','MD': 'MARYLAND',
       'ME': 'MAINE','MI': 'MICHIGAN','MN': 'MINNESOTA','MO': 'MISSOURI',
       'MP': 'NORTHERN MARIANA ISLANDS','MS': 'MISSISSIPPI','MT': 'MONTANA','NA': 'NATIONAL',
       'NC': 'NORTH CAROLINA','ND': 'NORTH DAKOTA','NE': 'NEBRASKA','NH': 'NEW HAMPSHIRE',
       'NJ': 'NEW JERSEY','NM': 'NEW MEXICO','NV': 'NEVADA','NY': 'NEW YORK','OH': 'OHIO',
       'OK': 'OKLAHOMA','OR': 'OREGON','PA': 'PENNSYLVANIA','PR': 'PUERTO RICO',
       'RI': 'RHODE ISLAND','SC': 'SOUTH CAROLINA','SD': 'SOUTH DAKOTA','TN': 'TENNESSEE',
       'TX': 'TEXAS','UT': 'UTAH','VA': 'VIRGINIA','VI': 'VIRGIN ISLANDS','VT': 'VERMONT',
       'WA': 'WASHINGTON','WI': 'WISCONSIN','WV': 'WEST VIRGINIA','WY': 'WYOMING'
   }

   abr = pd.DataFrame(list(state_abbrs.items()), columns=['state', 'name'])
   states = pd.read_table('..\\state_fips.txt', dtype=str)
   state_frame = pd.merge(states, abr, on='state')
   counties = pd.read_table('..\\national_county.txt', dtype=str, sep=';')
   data_dir = os.getcwd() + '\\data\\'

   # Import data
   crime_15 = fbi_crime_stats(data_dir + 'crime_15.xls',8,'2015',state_frame,counties)
   crime_14 = fbi_crime_stats(data_dir + 'crime_14.xls',8,'2014',state_frame,counties)
   crime_13 = fbi_crime_stats(data_dir + 'crime_13.xls',7,'2013',state_frame,counties)
   crime_12 = fbi_crime_stats(data_dir + 'crime_12.xls',7,'2012',state_frame,counties)
   crime_11 = fbi_crime_stats(data_dir + 'crime_11.xls',7,'2011',state_frame,counties)
   crime_10 = fbi_crime_stats(data_dir + 'crime_10.xls',7,'2010',state_frame,counties)
   crime_09 = fbi_crime_stats(data_dir + 'crime_09.xls',7,'2009',state_frame,counties)
   crime_08 = fbi_crime_stats(data_dir + 'crime_08.xls',7,'2008',state_frame,counties)
   crime_07 = fbi_crime_stats(data_dir + 'crime_07.xls',7,'2007',state_frame,counties)
   crime_06 = fbi_crime_stats(data_dir + 'crime_06.xls',8,'2006',state_frame,counties)
   crime_05 = fbi_crime_stats(data_dir + 'crime_05.xls',8,'2005',state_frame,counties)

   dfs = [crime_15,crime_14,crime_13,crime_12,crime_11,crime_10,crime_09,crime_08,crime_07,crime_06,crime_05]

   df = multi_ordered_merge(dfs)
   df = df.sort_values(['fips','date'])


   # Metadata section
   md_names = ['series_id', 'title', 'season', 'frequency', 'units',
               'keywords', 'notes', 'period_description', 'growth_rates', \
               'obs_vsd_use_release_date', 'valid_start_date', 'release_id']
   fsr_names = ['fred_release_id', 'fred_series_id', 'official',
                'valid_start_date']
   cat_names = ['series_id', 'cat_id']

   geo_md = pd.DataFrame(columns=md_names)
   fred_md = pd.DataFrame(columns=md_names)
   fsr_geo = pd.DataFrame(columns=fsr_names)
   fsr = pd.DataFrame(columns=fsr_names)
   fred_cat = pd.DataFrame(columns=cat_names)

   season = 'Not Seasonally Adjusted'
   freq = '5-years'
   units = 'Percent'
   keywords = ''
   notes = ''
   period = ''
   g_rate = 'TRUE'
   obs_vsd = 'TRUE'
   vsd = '2017-01-27'
   r_id = '330'

   non_geo_fips = '002020|002110|002220|002230|002275|006705|008014|015003|042101'

   non_geo_cats = {'002020': '27406', '002110': '27412', '002220': '27422', \
                   '002230': '33516', '002275': '33518', '006075': '27559', \
                   '008014': '32077', '015003': '27889', '042101': '29664'}

   for series in pd.unique(df.fips.ravel()):
       fips = series
       frame = df[df['fips'] == series]
       frame.reset_index(inplace=True)
       frame.drop(['index'], axis=1, inplace=True)
       for c in ['violent', 'property', 'crime']:
           output = frame[['date', c]]
           output.set_index('date', inplace=True)
           series_id = 'FBI'
           if c is 'violent':
               series_id = series_id + 'VC' + fips
           elif c is 'property':
               series_id = series_id + 'PC' + fips
           elif c is 'crime':
               series_id = series_id + 'TC' + fips
               output.columns = [series_id]
               output.to_csv('output\\' + series_id, sep='\t')

if __name__=='__main__':
   main()