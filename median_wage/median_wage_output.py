import pandas as pd, os

raw_file = os.path.join(os.getcwd(),'output','medianwage.txt')

raw = pd.read_csv(raw_file)

