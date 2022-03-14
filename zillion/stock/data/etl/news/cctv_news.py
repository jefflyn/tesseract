from zillion.utils import db_util
from zillion.utils.pro_util import pro

if __name__ == '__main__':
    df = pro.cctv_news(date='20190820')
    print(df)
    db_util.to_db(df, 'cctv_news', if_exists='replace')

