import pandas as pd

df = pd.read_csv('basic_daily.csv', encoding='utf-8')
# 使用某列（字符串）作为索引
df.index = df['code'].astype('str').str.zfill(6)
print(df)
print("df index:", df.index.to_numpy())

# 重置索引，并删除索引列
df2 = df.reset_index(drop=True)
print("df2 index:", df2.index.array)
print(df2)

# [], loc, iloc, at, iat, ix（相当于loc和iloc的一个混合方法，0.20.0版本后已经弃用）
# 1、 loc和iloc函数都是用来选择某行的，iloc与loc的不同是：iloc是按照行索引所在的位置来选取数据，参数只能是整数。而loc是按照索引名称来选取数据，参数类型依索引类型而定；
# 2、 at是用来选择单个值的，at和iat函数是只能选择某个位置的值，iat是按照行索引和列索引的位置来选取数据的，而at是按照行索引和列索引来选取数据；
# 3、 loc和iloc函数的功能包含at和iat函数的功能。
# 选择某行某列数据
row = df[2:10][['code', 'trade_date']]
row2 = df2[2:10][['code', 'trade_date']]
print(row, row2)

code = row.loc['002401', 'code']
code2 = row2.loc[2, 'code']
print("row.loc['002401', 'code']=" + str(code), "row2.loc[2, 'code']=" + str(code2), sep=' || ')

# iloc接受的是一个数字，代表着要选择数据的位置，是按数据行取的（从0开始表示第一行），不是索引值
code = row.iloc[0, 0]
code2 = row2.iloc[2, 0]
print("row.iloc[0, 0]=" + str(code))
print("row2.iloc[2, 0]=" + str(code2))

code = row.at['002401', 'code']
code2 = row2.at[2, 'code']
print("row.at['002401', 'code']=" + str(code))
print("row2.at[2, 'code']=" + str(code2))

code = row.iat[0, 0]
code2 = row2.iloc[2, 0]
print("row.iat[0, 0]=" + str(code))
print("row2.iat[2, 0]=" + str(code2))

