# -*- coding: utf-8 -*-
"""
Created on Tue Sep 18 15:23:57 2018

Convert all the data from Tests.h5

@author: tangk
"""
import pandas as pd
import h5py
import numpy as np

directory = 'P:\\Data Analysis\\Data\\'
path_old = 'Tests_2.h5'
path_new = 'Tests.h5'

#rewrite with h5py
with pd.HDFStore(directory+path_old) as test_store_old, h5py.File(directory+path_new) as test_store_new:
    for test in test_store_old.keys():
        print(test)
        print('Reading...')
        df = test_store_old[test]
        df.columns = ['X' + i for i in df.columns]
        types = [(i, np.float64) for i in df.columns]
        print('Writing...')
        ds = test_store_new.create_dataset(test,shape=(df.shape[0],),dtype=types)
        ds[...] = df.apply(tuple,axis=1).values
        
#rewrite with pandas
#with pd.HDFStore(directory+path_old) as test_store_old, pd.HDFStore(directory+path_new) as test_store_new:
#    for test in test_store_old.keys()[:10]:
#        print(test)
#        print('Reading...')
#        df = test_store_old[test]
#        df.columns = ['X' + i for i in df.columns]
#        print('Writing...')   
#        test_store_new.append(test,
#                              df,
#                              data_columns=df.columns)
    
