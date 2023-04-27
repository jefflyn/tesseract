import zillion.utils.db_util as _dt

# 建立数据库连接
db = _dt.get_db()
# 使用cursor()方法创建一个游标对象
cursor = db.cursor()

class Nstat(object):
    pass


def get_all_stat():
    sql = "select * from n_stat"
    df = read_query(sql)
    df.index = df["code"]
    for index, row in df.iterrows():

    return df

if __name__ == '__main__':
    print(get_all_stat())
