from __future__ import print_function
import sqlite3

import matplotlib.pyplot as plt

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


