import stocks.util.db_util as _dt
from stocks.util import date_const
from stocks.util._utils import timer

one_year_ago = date_const.ONE_YEAR_AGO_YYYYMMDD


@timer
def select_combo():
    print('start select combo ...')
    # 建立数据库连接
    db = _dt.get_db()
    # 使用cursor()方法创建一个游标对象
    cursor = db.cursor()
    select_sql = "select lus.code,lus.name,lus.industry,sra.concepts,sra.pe,sra.wave_a,sra.wave_b,lus.combo,lus.count," \
                 "sra.map,sra.list_date,sra.issue_price,sra.issue_space,lus.fire_price," \
                 "round((lus.price - lus.fire_price) / lus.fire_price * 100, 2) fs,1 on_target, sra.wave_detail, " \
                 "'combo' select_type," \
                 "sra.trade_date, sra.select_time as update_time " \
                 "from limit_up_stat lus left join select_result_all sra on lus.code = sra.code where lus.combo > 4 " \
                 "and sra.name not like :name and sra.list_date < :list_date and lus.code not like '688%' " \
                 "and (sra.wave_b < -33 or (sra.wave_b > 0 and sra.wave_b < 10) or (sra.wave_a < -40 and sra.wave_b < 15)) " \
                 "order by lus.wave_a;"
    params = {"name": "%ST%", "list_date": one_year_ago}
    select_df = _dt.read_sql(select_sql, params)
    if select_df.empty is True:
        return
    for index, row in select_df.iterrows():
        try:
            insert_sql = "INSERT INTO select_x VALUES " \
                         "('%s', '%s', '%s', '%s', '%.2f', '%.2f','%.2f','%i','%i'," \
                        "'%.2f','%i','%.2f', '%.2f', '%.2f', '%.2f', '%i', '%s', '%s', '%s', '%s')" \
                         % (str(row["code"]), row["name"], row["industry"], row["concepts"], float(row["pe"]),
                            float(row["wave_a"]), float(row["wave_b"]), int(row["combo"]), int(row["count"]),
                            float(row["map"]), int(row["list_date"]), float(row["issue_price"]), float(row["issue_space"]),
                            float(row["fire_price"]), float(row["fs"]), int(row["on_target"]), row["wave_detail"],
                            row["select_type"], row["trade_date"], row["update_time"])
            cursor.execute(insert_sql)
            db.commit()
        except Exception as err:
            print('insert failed:', err)
            db.rollback()
            continue
    update_sql = "update select_x sx join select_result_all sra on sx.code=sra.code " \
                 "join limit_up_stat lus on sx.code=lus.code " \
                 "set sx.name=sra.name, sx.industry=sra.industry, sx.concept=sra.concepts," \
                 "sx.pe=sra.pe,sx.wave_a=sra.wave_a,sx.wave_b=sra.wave_b, sx.l_count=sra.count," \
                 "sx.map=sra.map,sx.issue_date=sra.list_date,sx.issue_price=sra.issue_price,sx.combo=lus.combo, " \
                 "sx.fire_price=lus.fire_price,sx.fire_space=round((lus.price - lus.fire_price) / lus.fire_price * 100, 2), " \
                 "sx.on_target=case when (sra.wave_b < -33 or (sra.wave_b > 0 and sra.wave_b < 10) or (sra.wave_a < -40 and sra.wave_b < 15)) then 1 else 0 end, " \
                 "update_time=now(),sx.wave_str=sra.wave_detail where sx.select_type='combo';"
    print('update select combo:', cursor.execute(update_sql))
    db.commit()
    # 关闭游标和数据库的连接
    cursor.close()
    db.close()


@timer
def select_map():
    print('start select map ...')
    # 建立数据库连接
    db = _dt.get_db()
    # 使用cursor()方法创建一个游标对象
    cursor = db.cursor()
    select_sql = "select lus.code,lus.name,lus.industry,sra.concepts,sra.pe,sra.wave_a,sra.wave_b,lus.combo,lus.count," \
                 "sra.map,sra.list_date,sra.issue_price,sra.issue_space,lus.fire_price," \
                 "round((lus.price - lus.fire_price) / lus.fire_price * 100, 2) fs,1 on_target, sra.wave_detail, " \
                 "'map' select_type," \
                 "sra.trade_date, sra.select_time as update_time " \
                 "from limit_up_stat lus left join select_result_all sra on lus.code = sra.code " \
                 "where sra.name not like :name and sra.list_date > 0 and sra.list_date < :list_date " \
                 "and lus.code not like '688%' and lus.count > 1" \
                 "and (sra.map > 10.9 or (sra.map > 10 and sra.wave_a < -33 and sra.wave_b < 40)) " \
                 "order by sra.map desc;"
    params = {"name": "%ST%", "list_date": one_year_ago}
    select_df = _dt.read_sql(select_sql, params)
    if select_df.empty is True:
        return
    for index, row in select_df.iterrows():
        try:
            insert_sql = "INSERT INTO select_x VALUES " \
                         "('%s', '%s', '%s', '%s', '%.2f', '%.2f','%.2f','%i','%i'," \
                        "'%.2f','%i','%.2f', '%.2f', '%.2f', '%.2f', '%i', '%s', '%s', '%s', '%s')" \
                         % (str(row["code"]), row["name"], row["industry"], row["concepts"], float(row["pe"]),
                            float(row["wave_a"]), float(row["wave_b"]), int(row["combo"]), int(row["count"]),
                            float(row["map"]), int(row["list_date"]), float(row["issue_price"]), float(row["issue_space"]),
                            float(row["fire_price"]), float(row["fs"]), int(row["on_target"]), row["wave_detail"],
                            row["select_type"], row["trade_date"], row["update_time"])
            cursor.execute(insert_sql)
            db.commit()
        except Exception as err:
            print('insert failed:', err)
            db.rollback()
            continue
    update_sql = "update select_x sx join select_result_all sra on sx.code=sra.code " \
                 "join limit_up_stat lus on sx.code=lus.code " \
                 "set sx.name=sra.name, sx.industry=sra.industry, sx.concept=sra.concepts," \
                 "sx.pe=sra.pe,sx.wave_a=sra.wave_a,sx.wave_b=sra.wave_b, sx.l_count=sra.count," \
                 "sx.map=sra.map,sx.issue_date=sra.list_date,sx.issue_price=sra.issue_price,sx.combo=lus.combo, " \
                 "sx.fire_price=lus.fire_price,sx.fire_space=round((lus.price - lus.fire_price) / lus.fire_price * 100, 2), " \
                 "sx.on_target=case when (sra.map > 10.9 or (sra.map > 10 and sra.wave_a < -33 and sra.wave_b < 40)) then 1 else 0 end, " \
                 "update_time=now(),sx.wave_str=sra.wave_detail where sx.select_type='map';"
    print('update select map:', cursor.execute(update_sql))
    db.commit()
    # 关闭游标和数据库的连接
    cursor.close()
    db.close()


@timer
def select_new():
    print('start select new ...')
    # 建立数据库连接
    db = _dt.get_db()
    # 使用cursor()方法创建一个游标对象
    cursor = db.cursor()
    select_sql = "select lus.code,lus.name,lus.industry,sra.concepts,sra.pe,sra.wave_a,sra.wave_b,lus.combo,lus.count," \
                 "sra.map,sra.list_date,sra.issue_price,sra.issue_space,lus.fire_price," \
                 "round((lus.price - lus.fire_price) / lus.fire_price * 100, 2) fs,1 on_target, sra.wave_detail, " \
                 "'new' select_type," \
                 "sra.trade_date, sra.select_time as update_time " \
                 "from limit_up_stat lus left join select_result_all sra on lus.code = sra.code " \
                 "where sra.name not like :name and sra.list_date > :list_date and lus.code not like '688%' " \
                 "    and (sra.issue_space < 15 or (sra.wave_b < -33 or (sra.wave_b > 0 and sra.wave_b < 10) or (sra.wave_a < -40 and sra.wave_b < 15))) " \
                 "order by lus.wave_a;"
    params = {"name": "%ST%", "list_date": date_const.SIX_MONTHS_AGO_YYYYMMDD}
    select_df = _dt.read_sql(select_sql, params)
    if select_df.empty is True:
        return
    for index, row in select_df.iterrows():
        try:
            insert_sql = "INSERT INTO select_x VALUES " \
                         "('%s', '%s', '%s', '%s', '%.2f', '%.2f','%.2f','%i','%i'," \
                        "'%.2f','%i','%.2f', '%.2f', '%.2f', '%.2f', '%i', '%s', '%s', '%s', '%s')" \
                         % (str(row["code"]), row["name"], row["industry"], row["concepts"], float(row["pe"]),
                            float(row["wave_a"]), float(row["wave_b"]), int(row["combo"]), int(row["count"]),
                            float(row["map"]), int(row["list_date"]), float(row["issue_price"]), float(row["issue_space"]),
                            float(row["fire_price"]), float(row["fs"]), int(row["on_target"]), row["wave_detail"],
                            row["select_type"], row["trade_date"], row["update_time"])
            cursor.execute(insert_sql)
            db.commit()
        except Exception as err:
            print('insert failed:', err)
            db.rollback()
            continue
    update_sql = "update select_x sx join select_result_all sra on sx.code=sra.code " \
                 "join limit_up_stat lus on sx.code=lus.code " \
                 "set sx.name=sra.name, sx.industry=sra.industry, sx.concept=sra.concepts," \
                 "sx.pe=sra.pe,sx.wave_a=sra.wave_a,sx.wave_b=sra.wave_b, sx.l_count=sra.count," \
                 "sx.map=sra.map,sx.issue_date=sra.list_date,sx.issue_price=sra.issue_price,sx.combo=lus.combo, " \
                 "sx.fire_price=lus.fire_price,sx.fire_space=round((lus.price - lus.fire_price) / lus.fire_price * 100, 2), " \
                 "sx.on_target=case when (sra.wave_b < -33 or (sra.wave_b > 0 and sra.wave_b < 10) or (sra.wave_a < -40 and sra.wave_b < 15)) then 1 else 0 end, " \
                 "update_time=now(),sx.wave_str=sra.wave_detail where sx.select_type='new';"
    print('update select new:', cursor.execute(update_sql))
    db.commit()
    # 关闭游标和数据库的连接
    cursor.close()
    db.close()


def select_x():
    select_combo()
    select_map()
    select_new()


if __name__ == '__main__':
    select_combo()
    select_map()
    select_new()

