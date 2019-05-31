# -*- coding: utf-8 -*-
"""
Created on Thu May 30 10:30:59 2019

@author: tangk
"""

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import *

X = pd.read_csv('C:\\Users\\tangk\\Desktop\\displacement.csv')

search_params = {'rise': {'poly': [1, 2, 3],
                          'start_time': [0],
                          'end_time': range(100, 601)},
                 'fall': {'poly': [1, 2, 3, 4, 5],
                          'start_time': range(1100,3601),
                          'end_time': [len(X)-1]}}

slopes = {}

linear_model = LinearRegression()

for k, params in search_params.items():
    slopes[k] = pd.DataFrame(columns=['slope','r2','mse'],
                             index=pd.MultiIndex.from_product(params.values(), names=params.keys()))
    for t0 in params['start_time']:
        for tend in params['end_time']:
            for n in params['poly']:
                #preprocess the data
                poly = PolynomialFeatures(degree=n)
                y = X['x2'][t0:tend].to_frame()
                x = poly.fit_transform(X['t'][t0:tend].to_frame())
                
                #get fits
                linear_model = linear_model.fit(x, y)
                y_pred = linear_model.predict(x)
                
                if n==1 or k=='rise':
                    slope = linear_model.coef_[0][1]
                else:
                    slope = sum(np.arange(1,n+1)*linear_model.coef_[0][1:]*x[-1][:n])
                r2 = r2_score(y, y_pred)
                mse = mean_squared_error(y, y_pred)
                slopes[k].loc[n, t0, tend] = [slope, r2, mse]

print(slopes['rise'].sort_values('mse').head(10))
print(slopes['fall'].sort_values('mse').head(10))


avg_slopes = pd.DataFrame(columns=range(1, search_params['fall']['poly'][-1]+1))
for n in range(1, search_params['fall']['poly'][-1]+1):
    t0 = 1350
    tend = len(X)-1
    poly = PolynomialFeatures(degree=n)
    y = X['x1'][t0:tend].to_frame()
    x = poly.fit_transform(X['t'][t0:tend].to_frame())
    
    linear_model = linear_model.fit(x, y)
    slope = np.sum(np.arange(1,n+1)*linear_model.coef_[0][1:]*x[:, :n], axis=1)
    avg_slopes[n] = slope

print((avg_slopes.max()-avg_slopes.min())/avg_slopes.mean())
#for k, params in search_params.items():
#    
#    fig, axs = plt.subplots(nrows=2, ncols=2, figsize=(12,8))
#    for n in params['poly']:
#        print(['range in slope: ', max(slopes[k].loc[n, 'slope'].values)-min(slopes[k].loc[n, 'slope'].values)])
#        axs[0][0].plot(slopes[k].loc[n, 'slope'].values, label=n)
#        axs[0][0].set_title((k, 'slope'))
##        axs[0][0].set_xlim([0, 100])
#        
#        axs[0][1].plot(slopes[k].loc[n, 'r2'].values, label=n)
#        axs[0][1].set_title((k, 'r2'))
#        axs[0][1].set_ylim([0.99, 1])
##        axs[0][1].set_xlim([0, 100])
#        
#        axs[1][0].plot(slopes[k].loc[n, 'mse'].values, label=n)
#        axs[1][0].set_title((k, 'mse'))
#        axs[1][0].set_ylim([0, 1])
##        axs[1][0].set_xlim([0, 100])
#    axs[0][0].legend()
#    axs[0][1].legend()
#    axs[1][0].legend()
