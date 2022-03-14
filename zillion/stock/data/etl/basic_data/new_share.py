from zillion.utils.pro_util import pro

if __name__ == '__main__':
    df = pro.new_share(start_date='20190101', end_date='20201231')
    print(df)

