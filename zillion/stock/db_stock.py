import pandas as pd
import pymysql
import sqlalchemy as sa
from sqlalchemy import create_engine

from utils.DbManager import DbManager

engine = create_engine("mysql+pymysql://linjingu:linjingu@127.0.0.1:3306/stock?charset=UTF8MB4")

db_manager = DbManager(
    host="localhost",
    username="linjingu",
    password="linjingu",
    database="stock"
)


def get_db():
    db = pymysql.connect(host='127.0.0.1', user='linjingu', passwd='linjingu', db='stock', charset='UTF8MB4')
    return db


# save to db
def to_db(data=None, tbname=None, if_exists='replace', db_engine=None):
    if db_engine == 'local':
        data.to_sql(name=tbname, con=engine, if_exists=if_exists, index=False, index_label=None)
    elif db_engine == 'rds':
        print("service expired")
        # data.to_sql(name=tbname, con=engine_rds, if_exists=if_exists, index=False, index_label=None)
    else:
        data.to_sql(name=tbname, con=engine, if_exists=if_exists, index=False, index_label=None)
        # data.to_sql(name=tbname, con=engine_rds, if_exists=if_exists, index=False, index_label=None)


def read_table(tbname):
    """
    Read SQL database table into a DataFrame.
    :param tbname:
    :return:
    """
    return pd.read_sql_table(tbname, engine)


def read_query(sql):
    """
    Read SQL query into a DataFrame
    :param sql:
    :return:
    """
    return pd.read_sql_query(sql, engine)


def read_sql(sql, params):
    """
    use SQLAlchemy constructs to describe your query
    :param sql: 'SELECT * FROM data where Col_1=:col1'
    :param params: map {'col1': 'X'}
    :return:
    """
    return pd.read_sql(sa.text(sql), engine, params=params)


if __name__ == '__main__':
    # df = read_table('hist_trade_day')
    # df = read_query('select code, trade_date, close from hist_trade_day')
    df_data = read_sql(
        'select ts_code code, trade_date date, open, high, low, close from stock_daily_us order by trade_date',
        params={})
    print(df_data)
