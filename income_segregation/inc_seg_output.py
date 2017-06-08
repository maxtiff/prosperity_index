import functools as ft, pandas as pd, os,re
pd.options.mode.chained_assignment = None  # default='warn'

def multi_ordered_merge(lst_dfs):

    reduce_func = lambda left,right: pd.ordered_merge(left, right)

    return ft.reduce(reduce_func, lst_dfs)

def main():

    output_dir = os.path.join(os.getcwd(),'output')
    files = os.listdir(output_dir)

    counties = pd.read_table('..\\national_county.txt', dtype=str, sep=';')
    states = pd.read_table('..\\state_fips.txt')

    df = pd.DataFrame()

    wf = pd.read_table(os.path.join(output_dir,files[0]),sep='\t',dtype='str')
    wf2 = pd.read_table(os.path.join(output_dir,files[1]),sep='\t',dtype='str')

    # for st in states.state:
    #     ptn = '\w{5}' + st + '\d{4}'
    #
    #     regex = re.compile(ptn)
    #
    #     selected_files = list(filter(regex.search,files))
    #
    #     print(selected_files)

if __name__ = '__main__':
    main()


# Test section
ptn = '\w{5}AL\d{4}'
    
regex = re.compile(ptn)

selected_files = list(filter(regex.search,files))

print(selected_files)

for i in selected_files:
    df_lst = []
    wf = pd.read_table(os.path.join(output_dir,i),sep='\t',dtype='str')