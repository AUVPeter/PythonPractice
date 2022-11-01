import pandas as pd
from glob import glob

'''
Single file
'''
log_001 = pd.read_csv('logfiles/log_20220408_001.csv', delimiter=',',header=2,skipinitialspace=True)

'''
Multiple files
'''
# get all filenames
filenames = glob('logfiles/log_*.csv')
# construct a list of DataFrames for each file
log_list = [pd.read_csv(f,delimiter=',',header=2,skipinitialspace=True) for f in filenames]
# concatenate into a single DataFrame
log_all = pd.concat(sub_frames, ignore_index=True)