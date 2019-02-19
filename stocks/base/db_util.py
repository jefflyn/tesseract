import pandas as pd
import sqlalchemy as sa
from sqlalchemy import create_engine
import pymysql
from stocks.base.logging import logger

engine = create_engine("mysql+pymysql://linjingu:linjingu@127.0.0.1:3306/stocks?charset=utf8")


def get_db():
    db = pymysql.connect(host='127.0.0.1', user='linjingu', passwd='linjingu', db='stocks', charset='utf8')
    return db


# save to db
def to_db(data=None, tbname=None, if_exists='replace'):
    data.to_sql(name=tbname, con=engine, if_exists=if_exists, index=False, index_label=None)
    logger.info('%s save to db successfully.' % tbname)


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
    # df = read_table('hist_data_month')
    # df = read_query('select code, date, p_change from hist_data_month')
    df = read_sql('select code, date, p_change from hist_data_month where code=:code', params={'code': '600680'})
    print(df)
