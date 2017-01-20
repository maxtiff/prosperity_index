import pandas as pd, os, sys, functools as ft, pycurl as pyc, datetime as dt, re, numpy as np
pd.options.mode.chained_assignment = None  # default='warn'

keep = ['geoid2','geodisplaylabel','hd01_vd01','hd01_vd10','hd01_vd11','hd01_vd14','hd01_vd15','hd01_vd24',\
        'hd01_vd25','hd01_vd28','hd01_vd29']