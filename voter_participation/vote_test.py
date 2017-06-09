import dbf, os, pandas as pd, re, functools as ft
pd.options.mode.chained_assignment = None  # default='warn'

filelist = [
    ['2014_EAVS_DBF_Files1.zip', '2014_EAVS_DBF_Files1.zip', '2014_EAVS_DBF_Files1', \
     'EAVS_Section_F-Part1.dbf','2014','EAVS_Section_A-Part1.dbf'],
    ['DBF Files.zip', 'DBF Files.zip', 'DBF Files', 'DBF Files\\Section F_F1-F3.dbf','2012', ''],\
    ['Sections C to F_DBF.zip', 'Final EAVS Data - Sections C to F_DBF.zip', \
     'Final EAVS Data - Sections C to F_DBF', 'EAVS Section F_part1.dbf', '2010', '']]

input_dir = os.path.join(os.getcwd(),'download\\2008 eavs dbf august 11 2010\\County_DBF')

table = dbf.Table(os.path.join(input_dir,'combined_sectionf.dbf'))