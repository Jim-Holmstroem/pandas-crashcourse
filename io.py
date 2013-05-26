from __future__ import print_function
import sqlite3

import matplotlib.pyplot as plt

import numpy as np
import pandas as pd
from pandas.io import sql

conn = sqlite3.connect('data/data.db')
data = sql.read_frame(
    "SELECT date, token, open, close FROM stocks WHERE date >= '2013-01-01' ORDER BY date",
    conn,
    index_col = ['date'],
    #parse_dates = True, #will be supported soon
)
data.index = pd.DatetimeIndex(data.index) #parse_dates fix

print(data.ix['2013-02-01':'2013-02-28'])
print(data.open)
print(data[['open', 'close']])

data['diff'] = pd.Series(data['close']-data['open'], index=data.index)

#GROUPBY
groups = data.groupby('token')

#AGGREGATIONS
print(groups.mean())
print(groups['close'].aggregate(
    {
        'minimum':  np.mean,
        'variance': np.var,
        'mean':     np.mean,
    }
))
print(groups.aggregate(
    [
        np.mean,
        np.var
    ]
))

#RENDERING

data[['open', 'close']].hist()
plt.figure()
data.boxplot()
pd.tools.plotting.scatter_matrix(data, diagonal='kde')
pd.tools.plotting.lag_plot(data['close'])
pd.tools.plotting.autocorrelation_plot(groups.get_group('GOOG')['close'])
pd.rolling_mean(groups.get_group('GOOG')[['close','open']], 3, 3).plot()
groups.get_group('GOOG')[['close','open']].plot()
plt.show()
