import pandas as pd
import numpy as np

dtype={'category': 'float64',
       'county_number': 'float64'}

df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/liquor_iowa_2021.csv",encoding='utf8',dtype=dtype)

df['county'] = df['county'].str.title()
df['store_location'] = df.groupby('store_name')['store_location'].transform(lambda g: g.ffill().bfill())

df['date'] = pd.to_datetime(df['date'])
season=[['Mar','Apr','May'],['Jun','Jul','Aug',],['Sep','Oct','Nov'],['Dec','Jan','Feb']]
df['Season']=np.select(
    [(df['date'].dt.strftime('%b').isin(season[0])),
     (df['date'].dt.strftime('%b').isin(season[1])),
     (df['date'].dt.strftime('%b').isin(season[2])),
     (df['date'].dt.strftime('%b').isin(season[3]))],
    ['Spring','Summer','Autumn','Winter'])

df['revenues'] = df['sale_dollars'] - (df['state_bottle_cost']*df['bottles_sold'])
df["lon"] = df["store_location"].str.split(' ').str[1]
df["lon"] = df["lon"].str.split('(').str[1]
df["lon"].fillna(0,inplace=True)
df["lat"] = df["store_location"].str.split(' ').str[2]
df["lat"] = df["lat"].str.split(')').str[0]
df["lat"].fillna(0,inplace=True)
df["lat"] = df["lat"].astype(float)
df["lon"] = df["lon"].astype(float)

print(df)
df2 = pd.read_csv('https://raw.githubusercontent.com/hoatranobita/app_to_cloud_4/main/uscities.csv')
