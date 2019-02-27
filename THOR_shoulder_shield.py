# -*- coding: utf-8 -*-
"""
Spyder Editor

Comparing responses of the THOR with prototype shoulder shields

"""

import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
from PMG.read_data import initialize
from PMG.COM.plotfuns import *
from PMG.COM.get_props import *
from PMG.COM.arrange import *
from PMG.COM.easyname import renameISO

directory = 'P:\\Data Analysis\\Projects\\AHEC\\THOR\\Prototype Shoulder\\'
cutoff = range(100, 1600)

channels = ['11HEAD0000THACXA',
            '11NECKUP00THFOXA',
            '11NECKUP00THFOYA',
            '11NECKUP00THFOZA',
            '11NECKLO00THFOXA',
            '11NECKLO00THFOYA',
            '11NECKLO00THFOZA',
            '11CLAVLEOUTHFOXA',
            '11CLAVLEINTHFOXA',
            '11SPIN0100THACXC',
            '11SPIN0100THACYC',
            '11CHST0000THACXC',
            '11CHST0000THACYC',
            '11CHSTLEUPTHDSXB',
            '11CHSTRILOTHDSXB',
            '11CHSTLELOTHDSXB',
            '11CHSTRIUPTHDSXB',
            '11THSP0100THAVZA',
            '11PELV0000THACXA',
            '11FEMRLE00THFOZB',
            '11FEMRRI00THFOZB']

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

#%% plot overlays
plot_channels = channels

for sh in ['HUMANETICS']:
    subset = (table.loc[~table['SHOULDER'].isna()]
                   .query('BELT_SLIP!=\'SLIDE\'')
                   .table.query_list('SHOULDER', ['ORIGINAL', sh]))
    subset = subset.replace('HUMANETICS','NEW HUMANETICS')
    subset['CONDITION'] = subset[['SHOULDER','BELT_SLIP']].apply(tuple, axis=1).astype(str)
    for ch in plot_channels:
        x = arrange_by_group(subset, chdata[ch], 'CONDITION')
        if len(x)==0: continue
        fig, ax = plt.subplots()
        ax = plot_bands(ax, t, x, ci=90)
        ax = set_labels(ax, {'title': '{0} ({1})'.format(renameISO(ch), ch), 'legend': {'bbox_to_anchor': (1,1)}})
        fig.savefig(directory + ch + '.png', bbox_inches='tight')
        plt.show()
        plt.close(fig)

#%% plot peaks--bar plots
plot_channels = ['Min_11HEAD0000THACXA',
                'Min_11NECKUP00THFOXA',
                'Max_11NECKUP00THFOXA',
                'Max_11NECKUP00THFOYA',
                'Max_11NECKUP00THFOZA',
                'Max_11NECKLO00THFOXA',
                'Max_11NECKLO00THFOYA',
                'Max_11NECKLO00THFOZA',
                'Min_11CLAVLEOUTHFOXA',
                'Min_11CLAVLEINTHFOXA',
                'Min_11SPIN0100THACXC',
                'Max_11SPIN0100THACYC',
                'Min_11CHST0000THACXC',
                'Max_11CHST0000THACYC',
                'Min_11CHSTLEUPTHDSXB',
                'Min_11CHSTRILOTHDSXB',
                'Min_11CHSTRIUPTHDSXB',
                'Max_11THSP0100THAVZA',
                'Min_11PELV0000THACXA',
                'Min_11FEMRLE00THFOZB',
                'Min_11FEMRRI00THFOZB']
for sh in ['HUMANETICS']:
    subset = (table.loc[~table['SHOULDER'].isna()]
                   .query('BELT_SLIP!=\'SLIDE\'')
                   .table.query_list('SHOULDER', ['ORIGINAL', sh]))
    subset['CONDITION'] = subset[['SHOULDER','BELT_SLIP']].apply(tuple, axis=1).astype(str)
    for ch in plot_channels:
        x = arrange_by_group(subset, features[ch], 'CONDITION')
        for k in x: 
            x[k] = x.pop(k).abs().to_frame()
        if len(x)==0: continue
        fig, ax = plt.subplots()
        ax = plot_bar(ax, x)
        ax = set_labels(ax, {'title': ch, 'legend': {'bbox_to_anchor': (1,1)}})
        plt.show()
        plt.close(fig)