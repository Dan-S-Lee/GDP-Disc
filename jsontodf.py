# -*- coding: utf-8 -*-
"""
Created on Tue Jan 14 09:17:16 2020

@author: daniel_lee
"""

import json
import pandas as pd
from pandas.io.json import json_normalize
import numpy as np
import pygal
import csv

file_string = 'gdp_json.json'
with open(file_string) as json_file:
    gdp_json = json.load(json_file)
gdp_df = json_normalize(gdp_json)

gdp_df['GDP'] = gdp_df['GDP(nominal 2017)'].str.strip('$').astype(float)

#code_df = pd.read_csv('Codes.csv', encoding = "ISO-8859-1")
code_dict_reader = csv.DictReader(open('Codes.csv'))
code_dict = dict((rows['Country'], rows['Code']) for rows in code_dict_reader)
gdp_df['Country Code'] = gdp_df['Country'].map(code_dict)
gdp_df.dropna(axis = 0, how = 'any', inplace = True)
gdp_df['GDP %'] = 100 * gdp_df['GDP'] / sum(gdp_df['GDP'])

#create percentiles for GDP
per_list = [0, .33, .66, 1]
per_vals = [gdp_df['GDP'].quantile(p) for p in per_list]
per_names = ['Low', 'Med', 'High']

#generate map
from pygal.style import CleanStyle
worldmap_gdp = pygal.maps.world.World(style = CleanStyle)
worldmap_gdp.title = 'GDP'

#add percentiles data to map
for i in range(len(per_vals) - 1):
    temp_df = gdp_df[(gdp_df.GDP >= per_vals[i]) & (gdp_df.GDP <= per_vals[i + 1])]
    temp_dict = pd.Series(temp_df['GDP'].values,
                          index = temp_df['Country Code']).to_dict()
    worldmap_gdp.add(per_names[i], temp_dict)

worldmap_gdp.render_to_file('GDP.svg')
