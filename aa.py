

import requests
import json
import pandas as pd
n1 = 'ADS'
api_url = 'https://www.quandl.com/api/v3/datasets/WIKI/%s.csv' % n1
df = pd.read_csv(api_url)
df = df.head(100)
print(df.head())
#print(list(data))
