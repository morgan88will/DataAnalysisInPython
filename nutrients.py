#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  3 16:10:04 2019

@author: Will Morgan
"""

import json
import pandas as pd
import numpy as np

db = json.load(open('database.json'))

#print len(db)

print db[0].keys()

#nutrients = pd.DataFrame(db[0]['nutrients'])

#print nutrients[:7]

info_keys = ['description', 'group', 'id', 'manufacturer']

info = pd.DataFrame(db, columns=info_keys)


#print info

#print pd.value_counts(info.group)[:10]

nutrients = []
for rec in db: 
    fnuts = pd.DataFrame(rec['nutrients'])
    fnuts['id'] = rec['id']
    nutrients.append(fnuts)
nutrients = pd.concat(nutrients, ignore_index=True)

#print nutrients

#print nutrients.duplicated().sum()

nutrients = nutrients.drop_duplicates()

col_mapping = {'description' : 'food', 'group' : 'fgroup'}

info = info.rename(columns=col_mapping, copy=False)

#print info

col_mapping = {'description' : 'nutrient', 'group' : 'nutgroup'}

nutrients = nutrients.rename(columns=col_mapping, copy=False)

#print "printing nutrients", nutrients

ndata = pd.merge(nutrients, info, on='id',how='outer')

#print ndata

ndata.ix[30000]

result = ndata.groupby(['nutrient', 'fgroup'])['value'].quantile(0.5)
#print "printing result", result
result['Protein'].sort_values().plot(kind='barh')
#result.title("Protein")

by_nutrient = ndata.groupby(['nutgroup', 'nutrient'])

get_maximum = lambda x: x.xs(x.value.idxmax())
get_minimum = lambda x: x.xs(x.value.idxmin())

max_foods = by_nutrient.apply(get_maximum)[['value', 'food']]

max_foods.food = max_foods.food.str[:50]

print max_foods.ix['Amino Acids']['food']

