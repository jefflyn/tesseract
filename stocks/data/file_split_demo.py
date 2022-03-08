import pandas as pd

if __name__ == '__main__':
    file_name = 'id.csv'
    data = pd.read_csv(file_name, sep=' ')
    step1 = 280000
    times = 0
    sql = "update device_relation set spu_code='PB000001' where id="
    for i in range(0, data.index.size, step1):
        df_pt = data[i:i + step1]
        df_pt['id'] = df_pt['id'].apply(lambda x: sql + str(x) + ";")
        df_pt = df_pt.reset_index(drop=True)
        step2 = 1000
        for j in range(0, df_pt.index.size, step2):
            print(j + step2)
            df_pt.loc[j + step2] = "select sleep(1);"
        times += 1
        df_pt.to_csv(str(times) + "_update.sql", index=False, header=False)
