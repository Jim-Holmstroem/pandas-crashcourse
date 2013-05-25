from __future__ import print_function
import sqlite3
from glob import glob
from functools import partial
import csv
import itertools as it

conn = sqlite3.connect('data/data.db')
cur = conn.cursor()
cur.execute(
    '''CREATE TABLE IF NOT EXISTS stocks (token text, date text, open real, high real, low real, close real, volume real, adjclose real)'''
)

def render_csv_to_sql(cur, csv_filename):
    with open(csv_filename, 'rb') as f:
        print("read({})".format(csv_filename))
        cur.executemany(
            'INSERT INTO stocks VALUES ("{token}",?,?,?,?,?,?,?)'.format(
                token=csv_filename.split('/')[-1].split('.')[0] #REALLY UNSAFE
            ),
            list(it.islice(csv.reader(f), 1, None))
        )

list(map( #map filenames to database entries
    partial(
        render_csv_to_sql,
        cur
    ),
    glob('data/*.csv')
))
conn.commit()

