import functools as ft, pandas as pd, os

def multi_ordered_merge(lst_dfs):

    reduce_func = lambda left,right: pandas.ordered_merge(left, right)

    return ft.reduce(reduce_func, lst_dfs)

output_dir = os.path.join(os.getcwd(),'output')
files = os.listdir(output_dir)

counties = pd.read_table('..\\national_county.txt', dtype=str, sep=';')
states = pd.read_table('..\\state_fips.txt')


df = pd.DataFrame()


wf = pd.read_table(os.path.join(output_dir,files[0]),sep='\t',dtype='str')
wf2 = pd.read_table(os.path.join(output_dir,files[1]),sep='\t',dtype='str')