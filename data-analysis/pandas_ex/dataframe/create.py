import pandas as pd

df = pd.read_csv('basics.csv', encoding='utf-8')

# [], loc, iloc, at, iat, ix
#select row
row13 = df[:]
print(len(row13.index.to_numpy()))