import math

import pandas as pd


def insert_sleep():
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


def split_sql():
    ids = []
    total = len(ids)
    page_size = 20000
    pages = int(math.ceil(total / page_size))
    for i in range(0, pages):
        id_list = tuple(ids[i * page_size:page_size * i + page_size])
        print("select distinct shop_id, seller_id from device_box where status<>-1 and shop_id in " + str(id_list) + ";")


if __name__ == '__main__':
    split_sql()
