import pandas as pd
import pymysql
import sqlalchemy as sa
from sqlalchemy import create_engine

engine_rds = create_engine(
    "mysql+pymysql://ruian:jefflyn0423@rm-bp1z8b6f51h4ujmz4co.mysql.rds.aliyuncs.com:3306/zillion?charset=UTF8MB4")
engine = create_engine("mysql+pymysql://linjingu:linjingu@127.0.0.1:3306/future?charset=UTF8MB4")


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
    df = read_sql('select code, trade_date, close from hist_trade_day where code in :code',
                  params={'code': ['600680', '600126']})
    print(df)
