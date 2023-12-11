import pandas as pd
import pymysql
import sqlalchemy as sa
from sqlalchemy import create_engine

rds_zillion = "mysql+pymysql://ruian:jefflyn0423@rm-bp1z8b6f51h4ujmz4co.mysql.rds.aliyuncs.com:3306/zillion?charset=UTF8MB4"
local_future = "mysql+pymysql://linjingu:linjingu@127.0.0.1:3306/future?charset=UTF8MB4"
local_stock = "mysql+pymysql://linjingu:linjingu@127.0.0.1:3306/future?charset=UTF8MB4"
local_test = "mysql+pymysql://linjingu:linjingu@127.0.0.1:3306/test?charset=UTF8MB4"

DB_STOCK = 'stock'
DB_FUTURE = 'future'
DB_TEST = 'test'

def get_db():
    db = pymysql.connect(host='127.0.0.1', user='linjingu', passwd='linjingu', db='future', charset='UTF8MB4')
    return db


def get_db(db_name=None):
    db = pymysql.connect(host='127.0.0.1', user='linjingu', passwd='linjingu', db=db_name, charset='UTF8MB4')
    return db


def get_rds_db():
    db = pymysql.connect(host='rm-bp1z8b6f51h4ujmz4co.mysql.rds.aliyuncs.com', user='ruian', passwd='jefflyn0423',
                         db='zillion', charset='UTF8MB4')
    return db


def get_engine(db_name):
    if db_name == 'zillion':
        return create_engine(
        "mysql+pymysql://ruian:jefflyn0423@rm-bp1z8b6f51h4ujmz4co.mysql.rds.aliyuncs.com:3306/zillion?charset=UTF8MB4")
    elif db_name == 'future':
        return create_engine("mysql+pymysql://linjingu:linjingu@127.0.0.1:3306/future?charset=UTF8MB4")
    elif db_name == 'stock':
        return create_engine("mysql+pymysql://linjingu:linjingu@127.0.0.1:3306/stock?charset=UTF8MB4")
    elif db_name == 'test':
        return create_engine("mysql+pymysql://linjingu:linjingu@127.0.0.1:3306/test?charset=UTF8MB4")
    else:
        return create_engine("mysql+pymysql://linjingu:linjingu@127.0.0.1:3306/test?charset=UTF8MB4")


# save to db
def to_db(data=None, tb_name=None, if_exists='replace', db_name=None):
    data.to_sql(name=tb_name, con=get_engine(db_name), if_exists=if_exists, index=False, index_label=None)


def read_table(db_name, tb_name):
    """
    Read SQL database table into a DataFrame.
    :param tbname:
    :return:
    """
    return pd.read_sql_table(tb_name, get_engine(db_name))


def read_query(db_name, sql):
    """
    Read SQL query into a DataFrame
    :param sql:
    :return:
    """
    return pd.read_sql_query(sql, get_engine(db_name))


def read_sql(db_name, sql, params):
    """
    use SQLAlchemy constructs to describe your query
    :param sql: 'SELECT * FROM data where Col_1=:col1'
    :param params: map {'col1': 'X'}
    :return:
    """
    return pd.read_sql(sa.text(sql), get_engine(db_name), params=params)


if __name__ == '__main__':
    # df = read_table('hist_trade_day')
    # df = read_query('select code, trade_date, close from hist_trade_day')
    df = read_sql('future', 'select code, trade_date, close from hist_trade_day where code in :code',
                  params={'code': ['600680', '600126']})
    print(df)
