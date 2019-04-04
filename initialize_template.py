# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 11:06:40 2019
Template for loading data
@author: tangk
"""
import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
from PMG.read_data import initialize
from PMG.COM.plotfuns import *
from PMG.COM.get_props import *
from PMG.COM.arrange import *

directory = ''
cutoff = range(100, 1600)

channels = []

table, t, chdata = initialize(directory,channels, cutoff)

#%% feature extraction
def get_all_features(write_csv=False):
    i_to_t = get_i_to_t(t)
    feature_funs = {'Min_': [get_min],
                    'Max_': [get_max],
                    'Tmin_': [get_argmin,i_to_t],
                    'Tmax_': [get_argmax,i_to_t]} 
    features = pd.concat(chdata.chdata.get_features(feature_funs).values(),axis=1,sort=True)

    if write_csv:
        features.to_csv(directory + 'features.csv')
    return features

features = get_all_features(write_csv=False)
