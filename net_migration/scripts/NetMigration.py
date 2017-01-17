import os, sys, NetMigration_modules as nm, NetMigration_configuration as \
    config

def __main__():
    '''
    Function that writes data files to output folder.

    :return:    Nothing.
    '''

    path = str(sys.argv[1])

    # List of DFs to merge to create time series
    dfs = []

    for file in os.listdir(path + "\\downloads\\"):
        # read in and run through data parser
        if file:
            nm.parse_flow_data()
        else:
            nm.parse_net_data
        dfs=[]


    df = nm.multiple_merge(dfs, 'fips')
    df = nm.shape(df,'fips','Date')

    levels = df['fips'].unique()

    for series in levels:
        id = 'netmignacs' + series
        frame = df[df['fips'] == series]
        frame.drop('fips',axis=1,inplace=True)
        frame.columns=['Date',id]
        frame.to_csv('..\\output\\'+id, index=False, sep='\t')

if __name__ == '__main__':
    main()



for series in levels:
    id = 'netmignacs' + series
    frame = test[test['fips'] == series]
    frame.drop('fips',axis=1,inplace=True)
    frame.columns=['Date',id]
    frame.to_csv('..\\output\\'+id, index=False, sep='\t')