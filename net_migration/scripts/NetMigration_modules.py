import pandas as pd, functools as ft

class Reader():

    def __init__(self, data,specs,names):
        '''
        :param data:    (STR) The location of the fixed-width file to source data.

        :param specs:   (LST, INT) A two-item list of integers representing the
                        column specs to read data from. specs[0] is the FIPS
                        code; specs[1] is the net migration data.

        :param names:    (LST, STR) A list of strings to be used as column names
                         for the data frame.
        '''
        self.data = data
        self.specs = specs
        self.names = names

    def parse_net_data(self):
        '''
        Function reads in a fixed-width file of data that has no column
        headers and returns a data frame.

        :return:        (DF) A data frame with an index, two columns and 3143
                        rows. Column[0] contains county and state FIPS
                        codes; Column[1] contains net migration level for
                        the :param year:

        :example:       >>> df = Reader(data='net_gross_us_2013.txt',specs=[(
                                0,6),(180,190)],['fips','2013'])
                            df.parse_net_data()

                                fips  2013
                        0     001001  -264
                        1     001003  3414
                        2     001005   565
                        3     001007  -500
                        4     001009   -96
                              ......   ...
                        3138  056037  -125
                        3139  056039 -1397
                        3140  056041   135
                        3141  056043   -57
                        3142  056045  -162

                        [3143 rows x 2 columns]
        '''
        df = pd.read_fwf(self.data, colspecs=self.specs, header=None,
                         names=self.names, converters={self.names[0]:
                                                           str})

        # Organize and clean data.
        df = df[~df[self.names[0]].str.contains('^072|^\w{3}000')]
        df[self.names[0]]=df[self.names[0]].astype('category')
        df[self.names[1]].fillna(value=0, inplace=True)

        return df.groupby(by=[self.names[0]])[self.names[1]].sum().to_frame().reset_index()


    def parse_flow_data(self):
        '''
        Function reads in a fixed-width file of data that has no column
        headers and returns a data frame.

        :param data:    (STR) The location of the fixed width file to source data.

        :param specs:   (LST, INT) A three-item list of integers representing the
                        column specs to read data from. specs[0] is the FIPS
                        code; specs[1] is the number of people who have moved to
                        a location, and specs[2] is the number of people who
                        have moved from a location.

        :param year:    (STR) A 4-character string of the year that the data
                        represents.

        :return:        (DF) A data frame with an index, two columns and 3143
                        rows. Column[0] contains county and state FIPS codes;
                        Column[1] contains net migration level for the :param year:

        :example:       >>> df = Reader(data='ctyxcty_us_2010.txt',specs=[(
                                 0,6),(6,12),(374,380)],['fips_crnt',
                                 'fips_prev','2010');
                            df.parse_flow_data()

                                fips  2010
                        0     001001   160
                        1     001003  4644
                        2     001005   593
                        3     001007  -331
                        4     001009   553
                              ......   ...
                        3138  056039  -519
                        3139  056041   -72
                        3140  056043   -54
                        3141  056045   494
                        3142  048261   -36

                        [3143 rows x 2 columns]
        '''
        raw = pd.read_fwf(self.data, colspecs=self.specs, header=None,
                          names=self.names, converters={self.names[0]: str,
                                                        self.names[1]: str}).fillna(value=0)

        # Organize and clean
        raw = raw[~raw.fips.str.contains('^072|^\w{3}000')]
        raw['fips_current'] = raw['fips_current'].astype('category')
        raw['fips_previous'] = raw['fips_previous'].astype('category')

        # Get total movers by current and previous residence
        current = raw.groupby(self.names[0])['movers'].sum()
        previous = raw.groupby(self.names[1])['movers'].sum().ix[:-10]

        df = pd.concat([current, previous], axis=1, keys=['in', 'out'])
        df.fillna(value=0, inplace=True)
        df[self.names[2]] = df['in'] - df['out']
        df.drop(['in','out'],axis=1,inplace=True)

        return df.reset_index().rename(columns={'index':'fips'})

class shape()
    def __init__(self,):

     def multiple_merge(lst_dfs, on):
        '''
        Function that returns a data frame of time series data for each FIPS code.

        :param lst_dfs: (LST) A list of the data frames that will be merged
                        into one data frame.

        :param on:      (STR) The column name to merge items on.

        :return:        (DF) A wide data frame of time series data.

        :example: >>> multiple_merge(dfs,'fips')

                                fips  2009  2010  2011  2012  2013
                        0     001001   569   160   978   -90  -264
                        1     001003  4955  4644  2126  2996  3414
                        2     001005   348   593   756   702   565
                        3     001007  -329  -331 -1000  -946  -500
                        4     001009   862   553    15   148   -96
                                 ...   ...   ...   ...   ...   ...
                        3138  056039  -581  -519 -1384 -1637 -1397
                        3139  056041   -71   -72  -309   118   135
                        3140  056043   -94   -54  -122    10   -57
                        3141  056045   491   494   118   -93  -162
                        3142  048261   -23   -36   -29   -27   -17

                        [3143 rows x 6 columns]
        '''
        reduce_func = lambda left, right: pd.merge(left, right, on=on)

        return ft.reduce(reduce_func, lst_dfs)

    def shape(df,id,var):
        '''
        Function that shapes a data frame from wide to long. Function then sorts
        data frame by id, and then variable.

        :param df:      (DF) A wide-set data frame.
        :param id:      (STR) The identity of the identifier column.
        :param var:     (STR) The identity of the variable column.
        :return:        (DF) A long-set data frame.

        :example: >>> shape(df,'fips','date')

                                 fips  Date  value
                        0      001001  2009    569
                        3143   001001  2010    160
                        6286   001001  2011    978
                        9429   001001  2012    -90
                        12572  001001  2013   -264
                        1      001003  2009   4955
                        3144   001003  2010   4644
                        6287   001003  2011   2126
                        9430   001003  2012   2996
                        12573  001003  2013   3414
                                  ...   ...    ...
                        3140   056043  2009    -94

                        6283   056043  2010    -54
                        9426   056043  2011   -122
                        12569  056043  2012     10
                        15712  056043  2013    -57
                        3141   056045  2009    491
                        6284   056045  2010    494
                        9427   056045  2011    118
                        12570  056045  2012    -93
                        15713  056045  2013   -162

                        [15715 rows x 3 columns]
        '''
        return pd.melt(df, id_vars=id, var_name=var).sort_values([id, var])





