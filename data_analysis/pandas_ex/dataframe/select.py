import pandas as pd

if __name__ == '__main__':
    df = pd.read_csv('basics.csv')
    df['code'] = df['code'].astype('str').str.zfill(6)
    df = df[['code','pe','timeToMarket']]

    # select row
    print(df[0:5])
    # select column
    print(df[['pe']])
    # select slice
    print(df[1:2]['pe'])

    idf = df.set_index('code')
    # select row
    print(idf.loc['000158': '600158'])
    # select column
    print(idf.loc[:, 'pe'])
    # select slice
    print(idf.loc['603709':, 'pe'])

    #select row
    print(idf.iloc[0:5])
    #select column
    print(idf.iloc[:,[0,1]])
    #select slice
    print(idf.iloc[3000:,[0]])

    #at
    print(idf.at['000511','pe'])

    # iat
    print(idf.iat[3000, 0])

    #ix
    print(idf.ix[1:5])
    print(idf.ix[100, 'pe'])
    print(idf.ix[100:105, ['pe','timeToMarket']])
    print(idf.ix[100:105, [0, 1]])
    print(idf.ix['300216', 'pe'])
    val = idf.ix['300216', 0]
    print(val)