import pandas as pd, os, sys, functools as ft, pycurl as pyc, datetime as dt, re, numpy as np
pd.options.mode.chained_assignment = None  # default='warn'

def dc_youth(dy_data,date):

    keep = ['GEO.id2','GEO.display-label','HD01_VD01','HD01_VD10','HD01_VD11',\
            'HD01_VD14','HD01_VD15','HD01_VD24','HD01_VD25','HD01_VD28','HD01_VD29']
    regex = ('GEO.id2|GEO.display-label|disconnected_youth|date')

    #import data
    df = pd.read_csv(dy_data,encoding='windows-1252',skiprows={1})
    df = df.filter(keep,axis=1)
    df['GEO.id2']=df['GEO.id2'].apply(lambda x:"%06d" % (x,))
    df['date'] = date

    # Calculate disconnected youth
    df['disconnected_youth']=((df['HD01_VD10'] +df['HD01_VD11'] + df['HD01_VD14'] \
                               +df['HD01_VD15'] + df['HD01_VD24'] + df['HD01_VD25'] \
                               +df['HD01_VD28'] + df['HD01_VD29'])/df['HD01_VD01'])*100

    return df.filter(regex=regex, axis=1)

def multi_ordered_merge(lst_dfs):
        reduce_func = lambda left,right: pd.ordered_merge(left, right)

        return ft.reduce(reduce_func, lst_dfs)

def main():
    data_dir = os.getcwd() + '\\data\\'

    youth_09 = dc_youth(data_dir+'disconnected_youth_09.csv','2009')
    youth_10 = dc_youth(data_dir+'disconnected_youth_10.csv','2010')
    youth_11 = dc_youth(data_dir+'disconnected_youth_11.csv','2011')
    youth_12 = dc_youth(data_dir+'disconnected_youth_12.csv','2012')
    youth_13 = dc_youth(data_dir+'disconnected_youth_13.csv','2013')
    youth_14 = dc_youth(data_dir+'disconnected_youth_14.csv','2014')

    dfs = [youth_09,youth_10,youth_11,youth_12,youth_13,youth_14]

    df = multi_ordered_merge(dfs)

    df = df.sort_values(['GEO.id2','date'])

    ### Metadata
    md_names = ['series_id','title','season','frequency','units','keywords',\
                'notes','period_description','growth_rates',\
                'obs_vsd_use_release_date','valid_start_date','release_id']
    fsr_names = ['fred_release_id','fred_series_id','official','valid_start_date']
    cat_names = ['series_id','cat_id']

    geo_md = pd.DataFrame(columns=md_names)
    fred_md = pd.DataFrame(columns=md_names)
    fsr_geo = pd.DataFrame(columns=fsr_names)
    fsr = pd.DataFrame(columns=fsr_names)
    fred_cat = pd.DataFrame(columns=cat_names)

    season = 'Not Seasonally Adjusted'
    freq = '5-years'
    units = 'Percent'
    keywords = ''
    notes = 'Disconnected Youth represents the percentage of youth in a ' \
            'county who are between the ages of 16 and 19 who are not ' \
            'enrolled in school and who are unemployed or not in the labor ' \
            'force.####The date of the data is the end of the 5-year period. ' \
            'For example, a value dated 2015 represents data from 2010 to 2015.'
    period = ''
    g_rate = 'TRUE'
    obs_vsd = 'TRUE'
    vsd = '2017-01-27'
    r_id = '408'


    non_geo_fips = '002020|002110|002220|002230|002275|006075|008014|015003|042101'

    non_geo_cats = {'002020':'27406','002110':'27412','002220':'27422',\
                    '002230':'33516','002275':'33518','006075':'27559',\
                    '008014':'32077','015003':'27889','042101':'29664'}
    ###

    # Create output files
    for l in pd.unique(df['GEO.id2'].ravel()):
        frame = df[df['GEO.id2'] == l]
        series_id = 'B14005DCYACS' + l
        frame.reset_index(inplace=True)
        frame = frame[['date','disconnected_youth']]
        frame.set_index('date', inplace=True)
        frame.columns = [series_id]
        frame.to_csv('output\\' + series_id, sep='\t')

        # Create metadata files
        title = 'Disconnected Youth (5-year estimate) for ' + \
                pd.unique(df[df['GEO.id2'] == l]['GEO.display-label'])[0]

        if bool(re.search(non_geo_fips, l)):
            row=pd.DataFrame(data=[[series_id, title, season,freq, units,keywords,\
                                    notes, period, g_rate, obs_vsd, vsd, r_id]],\
                             columns=md_names)
            fred_md = fred_md.append(row)

            row = pd.DataFrame(data=[[r_id,series_id,'TRUE',vsd]],columns=fsr_names)
            fsr = fsr.append(row)

            cat_id = non_geo_cats[l]
            row = pd.DataFrame(data=[[series_id,cat_id]],columns=cat_names)
            fred_cat = fred_cat.append(row)

        else:
            row = pd.DataFrame(data=[[series_id, title, season,freq, units,keywords,\
                                      notes, period, g_rate, obs_vsd, vsd, r_id]],\
                               columns=md_names)
            geo_md = geo_md.append(row)

            row = pd.DataFrame(data=[[r_id, series_id,'TRUE', vsd]],columns=fsr_names)
            fsr_geo = fsr_geo.append(row)

    # Write metadata files
    geo_md.to_csv('fred_series_geo.txt',sep='\t',index=False)
    fsr_geo.to_csv('fred_series_release_geo.txt',sep='\t',index=False)

    fred_md.to_csv('fred_series.txt',sep='\t',index=False)
    fsr.to_csv('fred_series_release.txt',sep='\t',index=False)
    fred_cat.to_csv('fred_series_in_category.txt',sep='\t',index=False)


if __name__=='__main__':
    main()