import zillion.utils.db_util as _dt

# 建立数据库连接
db = _dt.get_db()
# 使用cursor()方法创建一个游标对象
cursor = db.cursor()

nstat_map = {}


class NStat:
    def __init__(self):
        pass


def set_attr(nstat_obj, attr_names, values):
    for i in range(0, len(attr_names)):
        setattr(nstat_obj, attr_names[i], values[i])


def get_attr(nstat_obj, attr_name):
    return getattr(nstat_obj, attr_name)


def get_all_stat():
    sql = "select * from n_stat"
    df = _dt.read_query(sql)
    df.index = df["code"]
    for index, row in df.iterrows():
        # print(row.index.values)
        # print(row.values)
        nstat_obj = NStat()
        set_attr(nstat_obj, row.index.values, row.values)
        nstat_map[row['code']] = nstat_obj


get_all_stat()

if __name__ == '__main__':
    get_all_stat()
