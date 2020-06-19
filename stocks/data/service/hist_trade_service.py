from stocks.util import db_util
from stocks.util.redis_util import redis_client


def get_new_open_date(refresh=False):
    key = 'open_date_map'
    open_date_map = redis_client.get(key)
    if open_date_map is None or refresh is True:
        open_date_map = {}
        sql = "select ht.code, min(ht.trade_date) open_date from hist_trade_day ht left join basics b on ht.code = b.code " \
              "where b.list_date > :list_date and ht.code not like :ckb and ht.pct_change < 11 and ht.low <> ht.high group by ht.code"
        df = db_util.read_sql(sql, {'ckb': '688%', 'list_date': 20150101})
        for index, row in df.iterrows():
            code = row['code']
            open_date = row['open_date']
            open_date_map[code] = open_date
        redis_client.set(key, open_date_map)
        return open_date_map
    else:
        return eval(open_date_map)


def get_last_close():
    sql = "select h.trade_date, h.code, h.close from hist_trade_day h " \
          "inner join (select code, max(trade_date) late_date from hist_trade_day where code like :sz or code like :cyb group by code) mt " \
          "on h.code = mt.code and h.trade_date = mt.late_date"

    df = db_util.read_sql(sql, params={"sz": "0%", "cyb": "3%"})
    df.index = list(df['code'])
    return df


if __name__ == '__main__':
    result = get_new_open_date()
    print(result)
