import pandas as pd, os, sys, functools as ft, pycurl as pyc, datetime as dt, re, numpy as np
pd.options.mode.chained_assignment = None  # default='warn'

def edu_attain(file, cols, names, date):

	df = pd.read_csv(file,encoding='windows-1252',skiprows={1},na_values=['(X)','*****'],low_memory=False)
	df['GEO.id2'] = df['GEO.id2'].apply(lambda x: "%06d" % (x,))
	df = df.filter(cols,axis=1)
	df.columns=[names]
	df['date'] = date

	return df

def multi_ordered_merge(lst_dfs):
    reduce_func = lambda left,right: pd.ordered_merge(left, right)

    return ft.reduce(reduce_func, lst_dfs)

def main():
    keep_09 = ['GEO.id2','GEO.display-label','HC01_EST_VC11','HC01_EST_VC12','HC01_EST_VC13']
    keep = ['GEO.id2','GEO.display-label','HC01_EST_VC12','HC01_EST_VC13',\
               'HC01_EST_VC14']
    keep_15=['GEO.id2','GEO.display-label','HC02_EST_VC13','HC02_EST_VC14',\
               'HC02_EST_VC15']
    names = ['fips','county','assc','bach','grad']

    data_dir = os.getcwd()+'\\data\\'

    edu_09 = edu_attain(data_dir+'educational_attainment_09.csv',keep_09,\
                        names,'2009')
    edu_10 = edu_attain(data_dir+'educational_attainment_10.csv',keep,\
                        names,'2010')
    edu_11 = edu_attain(data_dir+'educational_attainment_11.csv',keep,\
                        names,'2011')
    edu_12 = edu_attain(data_dir+'educational_attainment_12.csv',keep,\
                        names,'2012')
    edu_13 = edu_attain(data_dir+'educational_attainment_13.csv',keep,\
                        names,'2013')
    edu_14 = edu_attain(data_dir+'educational_attainment_14.csv',keep,\
                        names,'2014')
    edu_15 = edu_attain(data_dir+'educational_attainment_15.csv',keep_15,\
                        names, '2015')

    dfs = [edu_09,edu_10,edu_11,edu_12,edu_13,edu_14,edu_15]

    df = multi_ordered_merge(dfs)

    df = df.sort_values(['fips','date'])
    df.fips = df.fips.astype(str)

    ### Metadata
    md_names = ['series_id', 'title', 'season', 'frequency', 'units',
                'keywords','notes', 'period_description', 'growth_rates',\
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
    notes = 'Estimate of educational attainment using 5 years of data. '\
            'For more information see Appendix 1 of the ACS General '\
            'Handbook (http://www.census.gov/content/dam/Census/library/publications/2008/acs/ACSGeneralHandbook.pdf). '\
            '####The date of the data is the end of the 5-year period. ' \
            'For example, a value dated 2015 represents data from 2010 to 2015.'
    period = ''
    g_rate = 'TRUE'
    obs_vsd = 'TRUE'
    vsd = '2017-01-27'
    r_id = '330'

    non_geo_fips = '002020|002110|002220|002230|002275|006075|008014|015003|042101'

    non_geo_cats = {'002020': '27406', '002110': '27412', '002220': '27422', \
                    '002230': '33516', '002275': '33518', '006075': '27559', \
                    '008014': '32077', '015003': '27889', '042101': '29664'}

    # Create output files
    for series in pd.unique(df['fips'].ravel()):
        frame = df[df['fips'] == series]
        frame.reset_index(inplace=True)
        # frame = frame.sort_values(['date'])
        frame.drop(['index'], axis=1, inplace=True)
        frame['total_third'] = frame.sum(axis=1)

        for c in ['assc','bach','grad','total_third']:
            output = frame[['date', c]]
            # frame['date'] = dates
            output.set_index('date', inplace=True)
            series_id = 'S1501ACS'
            if c is 'assc':
                series_id = series_id+ 'ASSOC' + series

                # title = 'People 25 Years and Over Who Have Completed an Associate\'s Degree (5-year estimate) in ' + \
                #         pd.unique(df[df['fips'] == l]['county'])[0]

            elif c is 'bach':
                series_id = series_id+ 'BACH' + series

                # title = 'People 25 Years and Over Who Have Completed a Bachelor\'s Degree (5-year estimate) in ' + \
                #         pd.unique(df[df['fips'] == l]['county'])[0]

            elif c is 'grad':
                series_id = series_id+ 'GRAD' + series

                # title = 'People 25 Years and Over Who Have Completed a Graduate\'s Degree (5-year estimate) in ' + \
                #         pd.unique(df[df['fips'] == l]['county'])[0]

            elif c is 'total_third':
                series_id = series_id+ 'TOTAL'+ series

                title = 'People 25 Years and Over Who Have Completed an Associate\'s Degree or Higher (5-year estimate) in ' + \
                        pd.unique(df[df['fips'] == series]['county'])[0]

                # Create metadata files
                if bool(re.search(non_geo_fips, series)):
                    row = pd.DataFrame(
                        data=[[series_id, title, season, freq, units, keywords,notes,\
                               period, g_rate, obs_vsd, vsd, r_id]],columns=md_names)
                    fred_md = fred_md.append(row)

                    row = pd.DataFrame(data=[[r_id, series_id, 'TRUE', vsd]],
                                       columns=fsr_names)
                    fsr = fsr.append(row)

                    cat_id = non_geo_cats[series]
                    row = pd.DataFrame(data=[[series_id, cat_id]],columns=cat_names)
                    fred_cat = fred_cat.append(row)

                else:
                    row = pd.DataFrame(data=[[series_id, title, season, freq, units,\
                                              keywords,notes, period, g_rate, obs_vsd,\
                                              vsd, r_id]],columns=md_names)
                    geo_md = geo_md.append(row)

                    row = pd.DataFrame(data=[[r_id, series_id, 'TRUE', vsd]],columns=fsr_names)
                    fsr_geo = fsr_geo.append(row)

                output.columns = [series_id]
                output.to_csv('output\\' + series_id, sep='\t')

            # Write metadata files
    geo_md.to_csv('fred_series_geo.txt', sep='\t', index=False)
    fsr_geo.to_csv('fred_series_release_geo.txt', sep='\t', index=False)

    fred_md.to_csv('fred_series.txt', sep='\t', index=False)
    fsr.to_csv('fred_series_release.txt', sep='\t', index=False)
    fred_cat.to_csv('fred_series_in_category.txt', sep='\t',index=False)

        #     # Create metadata files
        #     if bool(re.search(non_geo_fips, series)):
        #         row = pd.DataFrame(
        #             data=[[series_id, title, season, freq, units, keywords,\
        #                    notes, period, g_rate, obs_vsd, vsd, r_id]],\
        #             columns=md_names)
        #         fred_md = fred_md.append(row)
        #
        #         row = pd.DataFrame(data=[[r_id, series_id, 'TRUE', vsd]],
        #                            columns=fsr_names)
        #         fsr = fsr.append(row)
        #
        #         cat_id = non_geo_cats[l]
        #         row = pd.DataFrame(data=[[series_id, cat_id]],
        #                            columns=cat_names)
        #         fred_cat = fred_cat.append(row)
        #
        #     else:
        #         row = pd.DataFrame(
        #             data=[[series_id, title, season, freq, units, keywords,\
        #                    notes, period, g_rate, obs_vsd, vsd, r_id]],\
        #             columns=md_names)
        #         geo_md = geo_md.append(row)
        #
        #         row = pd.DataFrame(data=[[r_id, series_id, 'TRUE', vsd]],
        #                            columns=fsr_names)
        #         fsr_geo = fsr_geo.append(row)
        #
        # # Write metadata files
        # geo_md.to_csv('fred_series_geo.txt', sep='\t', index=False)
        # fsr_geo.to_csv('fred_series_release_geo.txt', sep='\t', index=False)
        #
        # fred_md.to_csv('fred_series.txt', sep='\t', index=False)
        # fsr.to_csv('fred_series_release.txt', sep='\t', index=False)
        # fred_cat.to_csv('fred_series_in_category.txt', sep='\t', index=False)

if __name__=='__main__':
    main()