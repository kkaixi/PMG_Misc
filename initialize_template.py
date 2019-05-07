# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 11:06:40 2019
Template for loading data
@author: tangk
"""
from PMG.read_data import PMGDataset
from PMG.COM.get_props import get_peaks
import json
import pandas as pd


directory = ''
cutoff = range(100, 1600)
channels = []
table_filters = {'drop': []}
preprocessing = None


#%% initialize the dataset and specify channels, filters, and preprocessing
dataset = PMGDataset(directory, channels=channels, cutoff=cutoff, verbose=False)
dataset.table_filters = table_filters
dataset.preprocessing = preprocessing


#%% write data 
if __name__=='__main__': 
    # if running the script, get the data
    dataset.get_data(['timeseries'])
    table = dataset.table
    features = get_peaks(dataset.timeseries)
    features = pd.concat((features, table), axis=1)
    features.to_csv(directory + 'features.csv')

    # json file specifying statistical tests to be done
    to_JSON = {'project_name': '',
               'directory'   : directory,
               'cat'     : {'group_1': [],
                            'group_2': []},
               'test'    : [{'name': 'two_sample_t',
                             'test1': 'group_1',
                             'test2': 'group_2',
                             'testname': 't.test',
                             'data': 'features',
                             'args': 'paired=FALSE, exact=FALSE, correct=TRUE, conf.level=0.95'},
                            {'name': 'one_sample_t',
                             'test1': 'group_1',
                             'testname': 't.test',
                             'data': 'features',
                             'args': 'exact=FALSE, correct=TRUE, conf.level=0.95'},
                            {'name': 'LME',
                             'test1': 'group_1',
                             'variables': ['var_1','var_2'],
                             'formula': 'var_1 + (1|var_2)',
                             'null_formula': '(1|var_2)',
                             'testname': 'lmer',
                             'data': 'features',
                             'model_args': None,
                             'test_args': None},
                             {'name': 'LM',
                              'test1': 'group_1',
                              'variables': ['var_1','var_2'],
                              'formula': 'var_1 + var_2',
                              'testname': 'lm',
                              'data': 'features',
                              'model_args': None,
                              'test_args': None}],
                'test2'  : None}    
    
    for test in to_JSON['test']:
        test['test1'] = to_JSON['cat'][test['test1']]
        if 'test2' in test:
            test['test2'] = to_JSON['cat'][test['test2']]
    with open(directory+'params.json','w') as json_file:
        json.dump(to_JSON,json_file)


