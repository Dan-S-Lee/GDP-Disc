# -*- coding: utf-8 -*-
"""
Created on Fri Mar  6 15:50:59 2020

@author: danie
"""

import pandas as pd
from datetime import datetime

history_df = pd.read_csv('timeline50000.csv')

history_df['Latitude'] = history_df['Latitude'] / 10000000
history_df['Longitude'] = history_df['Longitude'] / 10000000
history_df['TimeDate'] = history_df['TimeStamp'] // 1000
history_df['TimeDate'] = history_df['TimeDate'].apply(datetime.fromtimestamp)

offset_df = history_df[1:len(history_df)].copy()
last_row = history_df.tail(1).values.tolist()
offset_df.loc[len(offset_df)+1] = last_row[0]
offset_df.reset_index(inplace = True)

history_df['lat_from'] = history_df['Latitude']
history_df['lat_to'] = offset_df['Latitude']

history_df['lon_from'] = history_df['Longitude']
history_df['lon_to'] = offset_df['Longitude']

history_df['start_time'] = history_df['TimeDate'].isoformat()
history_df['end_time'] = offset_df['TimeDate'].isoformat()

filter_df = history_df[['lat_from', 'lat_to', 'lon_from', 'lon_to', 'start_time', 'end_time']].copy()
filter_df['dist'] = abs(filter_df['lat_from'] - filter_df['lat_to']) + abs(filter_df['lon_from'] - filter_df['lon_to'])

filtered_df = filter_df[filter_df['dist'] > .0001]

lines = []
# longitude, latitude order
for index, row in filtered_df.iterrows():
    ll_dict = {
        'coordinates': [
            [row['lon_from'], row['lat_from']],
            [row['lon_to'], row['lat_to']]
            ],
        'dates': [
            row['start_time'], row['end_time']
            ],
        'color': 'blue'
            }
    lines.append(ll_dict)

features = [
    {
        'type': 'Feature',
        'geometry': {
            'type': 'LineString',
            'coordinates': line['coordinates'],
        },
        'properties': {
            'times': line['dates'],
            'style': {
                'color': line['color'],
                'weight': 1
            }
        }
    }
    for line in lines
    ]

