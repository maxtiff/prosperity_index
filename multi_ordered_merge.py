import functools as ft, pandas

def multi_ordered_merge(lst_dfs):

    reduce_func = lambda left,right: pandas.ordered_merge(left, right)

    return ft.reduce(reduce_func, lst_dfs)