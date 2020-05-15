import pandas as pd 

df = pd.read_csv('2020-05-14 00-50-all.csv')
df_new = df[['ID', 'ROADID', 'lat', 'lon']]

print(df_new.head(5))

df_new.to_csv('轉換表.csv')