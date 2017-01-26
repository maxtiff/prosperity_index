import pandas as pd, os, sys, functools as ft, pycurl as pyc, datetime as dt, re, numpy as np,math
pd.options.mode.chained_assignment = None  # default='warn'


def diss_index(county_file,tract_file,date):
    keep_tract = ['GEO.id2','HD01_VD01','HD01_VD03','HD01_VD04','HD01_VD06','HD01_VD12']
    tract_names = ['fips','pop','white','black','asian','hispanic']
    county_names = ['fips','total','white_total','black_total','asian_total','hispanic_total']
    # keep_diss = ['blk_diss','asn_diss','esp_diss','nwt_diss']
    keep_diss = ['nwt_diss']

    # Process census tracts
    df_tract = pd.read_csv(tract_file,encoding='windows-1252',skiprows={1})
    df_tract = df_tract.filter(keep_tract,axis=1)
    df_tract.columns = [tract_names]
    df_tract['fips']=df_tract['fips'].astype(str)
    df_tract['tract']=df_tract.fips.str.extract('(?P<tract>\d{5}$)')
    df_tract['fips']=df_tract['fips'].str[:-6].astype(np.int64)
    df_tract['fips']=df_tract['fips'].apply(lambda x:"%06d" % (x,))

    # Process counties
    df_county= pd.read_csv(county_file,encoding='windows-1252',skiprows={1})
    df_county= df_county.filter(keep_tract,axis=1)
    df_county.columns = [county_names]
    df_county['fips']=df_county['fips'].apply(lambda x:"%06d" % (x,))

    # Many-to-one merge tracts into counties
    df= pd.merge(df_tract,df_county,on='fips')

    df['pct_white'] = df['white']/df['white_total']
    df['pct_nonwhite'] = (df['black'] + df['asian'] + df['hispanic'])/(df['black_total']+df['asian_total']+df['hispanic_total'])
    df['nonwhite_white'] = abs(df['pct_nonwhite']-df['pct_white'])

    # df['pct_black'] = df['black']/df['black_total']
    # df['pct_asian'] = df['asian']/df['asian_total']
    # df['pct_hispanic'] = df['hispanic']/df['hispanic_total']

    # df['black_white'] = abs(df['pct_black']-df['pct_white'])
    # df['asian_white'] = abs(df['pct_asian']-df['pct_white'])
    # df['hispanic_white'] = abs(df['pct_hispanic']-df['pct_white'])

    # Combine by FIPS
    df=df.groupby(df.fips).sum()

    # Calculate racial disparity
    df['nwt_diss'] = .5*df['nonwhite_white']
    # df['blk_diss'] = .5*df['black_white']
    # df['asn_diss'] = .5*df['asian_white']
    # df['esp_diss'] = .5*df['hispanic_white']

    # Clean up data frame
    # df.fillna(0,axis=1,inplace=True)
    df = df.filter(keep_diss, axis=1)
    df['date']=date
    df.reset_index(level=0, inplace=True)

    return df

def multi_ordered_merge(lst_dfs):
    reduce_func = lambda left,right: pd.ordered_merge(left, right)

    return ft.reduce(reduce_func, lst_dfs)

def racial_segregation():
    data_dir = os.getcwd() + '\\data\\'

    df_09 = diss_index(data_dir + 'race_county_09.csv',data_dir + 'race_tract_09.csv','2009')
    df_10 = diss_index(data_dir + 'race_county_10.csv',data_dir + 'race_tract_10.csv','2010')
    df_11 = diss_index(data_dir + 'race_county_11.csv',data_dir + 'race_tract_11.csv','2011')
    df_12 = diss_index(data_dir + 'race_county_12.csv',data_dir + 'race_tract_12.csv','2012')
    df_13 = diss_index(data_dir + 'race_county_13.csv',data_dir + 'race_tract_13.csv','2013')
    df_14 = diss_index(data_dir + 'race_county_14.csv',data_dir + 'race_tract_14.csv','2014')
    df_15 = diss_index(data_dir + 'race_county_15.csv',data_dir + 'race_tract_15.csv','2015')

    dfs = [df_09,df_10,df_11,df_12,df_13,df_14,df_15]

    df = multi_ordered_merge(dfs)
    df = df.sort_values(['fips','date'])
    df.fillna('.',axis=1,inplace=True)

    for l in pd.unique(df['fips'].ravel()):
        series = l
        frame = df[df['fips'] == series]
        series_id = 'RACEDISPARITY' + series
        frame.reset_index(inplace=True)
        # frame = frame.sort_values(['date'])
        # frame.drop(['index'], axis=1, inplace=True)
        frame = frame[['date','nwt_diss']]
        frame.set_index('date', inplace=True)
        frame.columns = [series_id]
        frame.to_csv('output\\' + series_id, sep='\t')

if __name__=='__main__':
    main()