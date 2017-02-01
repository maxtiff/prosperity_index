import pandas as pd, os, sys, functools as ft, pycurl as pyc, datetime as dt, re, numpy as np
pd.options.mode.chained_assignment = None  # default='warn'

'''
Housing Burden is defined as a household spending more than 30% of their monthly income on a rent or mortgage.
'''

def burden(file,filter,names,date):
    # read
    df = pd.read_csv(file,encoding='windows-1252', skiprows={1},\
                     low_memory=False)

    # clean
    df = df.filter(filter, axis=1)
    df.columns = [names]
    df['fips'] = df['fips'].apply(lambda x: "%06d" % (x,))

    # calculate
    df['burdened'] = (df['mort_30_34']+df['mort_35']+df['no_mort_30_34']+\
                      df['no_mort_35']+df['rent_30_34']+df['rent_35'])/\
                     (df['mortgages']+df['non_mortgages']+df['rent'])*100

    # throw in the date
    df['date'] = date

    # return the frame
    return df.filter(['fips','burdened','date'],axis=1)

def multi_ordered_merge(lst_dfs):
    reduce_func = lambda left,right: pd.ordered_merge(left, right)

    return ft.reduce(reduce_func, lst_dfs)

def main():

    keep_10_12 = ['GEO.id2','HC01_VC155','HC01_VC164',\
                'HC01_VC191','HC01_VC159','HC01_VC160','HC01_VC170',\
                'HC01_VC171','HC01_VC196','HC01_VC197']

    keep_13_14 = ['GEO.id2','HC01_VC157','HC01_VC167',\
                'HC01_VC196','HC01_VC161','HC01_VC162','HC01_VC173',\
                'HC01_VC174','HC01_VC201','HC01_VC202']

    keep_15 = ['GEO.id2','HC01_VC159','HC01_VC169', \
               'HC01_VC198','HC01_VC163','HC01_VC164','HC01_VC175',
               'HC01_VC176','HC01_VC203','HC01_VC204']

    names = ['fips','mortgages','non_mortgages','rent','mort_30_34',\
             'mort_35','no_mort_30_34','no_mort_35','rent_30_34','rent_35']

    counties = pd.read_table('..\\national_county.txt', dtype=str, sep=';')

    data_dir = os.getcwd()+'\\data\\'


    burden_10 = burden(data_dir+'housing_affordability_10.csv',keep_10_12,\
                       names,'2010')
    burden_11 = burden(data_dir+'housing_affordability_11.csv',keep_10_12,\
                       names, '2011')
    burden_12 = burden(data_dir+'housing_affordability_12.csv',keep_10_12,\
                       names,'2012')
    burden_13 = burden(data_dir+'housing_affordability_13.csv',keep_13_14,\
                       names, '2013')
    burden_14 = burden(data_dir+'housing_affordability_14.csv',keep_13_14,\
                       names,'2014')
    burden_15 = burden(data_dir+'housing_affordability_15.csv',keep_15,\
                       names, '2015')

    dfs = [burden_10, burden_11,burden_12,burden_13,burden_14,burden_15]

    df = multi_ordered_merge(dfs)

    df = pd.merge(df, counties, on='fips')

    df = df.sort_values(['fips', 'date'])

    for series in pd.unique(df['fips'].ravel()):
        frame = df[df['fips'] == series]
        series_id = 'DP04ACS' + series
        frame.reset_index(inplace=True)
        frame = frame[['date','burdened']]
        frame.set_index('date', inplace=True)
        frame.columns = [series_id]
        frame.to_csv('output\\' + series_id, sep='\t')

# run the code
if __name__ == '__main__':
    main()
