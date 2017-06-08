import functools as ft, pandas as pd, os,re
pd.options.mode.chained_assignment = None  # default='warn'

def main():
    output_dir = os.path.join(os.getcwd(),'output')
    input_dir = os.path.join(os.getcwd(),'download')
    files = os.listdir(input_dir)
    states = pd.read_table('..\\state_fips.txt')

    for st in states.state:
        # Initialize empty list to append panda series to.
        df_lst = []

        # Select only files pertaining to the current state during iteration
        ptn = '\w{5}' + st + '\d{4}'
        regex = re.compile(ptn)
        selected_files = list(filter(regex.search,files))

        for f in selected_files:
            wf = pd.read_table(os.path.join(input_dir,f),sep='\t',dtype='str')
            df_lst.append(wf)

        # Bring it all together using reduce function
        frame = multi_merge(df_lst)

        # Create FRED data files
        for i in range(len(frame)):
            fips = '0{}'.format(frame.iloc[i][0])
            id = 'INCSEG{}'.format(fips)

            series = pd.DataFrame(frame.iloc[i].drop('COUNTY')).reset_index()
            series.columns = ['date', id]
            series.to_csv(os.path.join(output_dir, id), sep='\t', index=False)

def multi_merge(lst_dfs):
    reduce_func = lambda left,right: pd.merge(left, right)
    return ft.reduce(reduce_func, lst_dfs)

if __name__=='__main__':
    main()


# Test section
# output_dir = os.path.join(os.getcwd(),'output')
# files = os.listdir(output_dir)
#
# counties = pd.read_table('..\\national_county.txt', dtype=str, sep=';')
# states = pd.read_table('..\\state_fips.txt')
#
# df = pd.DataFrame()
# df_lst = []
#
# ptn = '\w{5}AK\d{4}'
#
# regex = re.compile(ptn)
#
# selected_files = list(filter(regex.search, files))
#
# for f in selected_files:
#     wf = pd.read_table(os.path.join(output_dir, f), sep='\t', dtype='str')
#     df_lst.append(wf)
#
# frame = multi_merge(df_lst)
#
# for i in range(len(frame)):
#     fips = '0{}'.format(frame.iloc[i][0])
#     id = 'INCSEG{}'.format(fips)
#     series = pd.DataFrame(frame.iloc[i].drop('COUNTY')).reset_index()
#     series.columns = ['date',id]
#     series.to_csv(os.path.join(output_dir, id), sep='\t',index=False)

