import stocks.base.db_util as _dt
import time
from stocks.base.pro_util import pro
import datetime
from datetime import timedelta
from stocks.base.db_util import get_db
from stocks.base.logging import logger

if __name__ == '__main__':
    # df = pro.concept()
    # _dt.to_db(df, 'concept')

    db = get_db()
    cursor = db.cursor()
    total = cursor.execute("select code from concept")
    if total == 0:
        logger.info("no concept found, process end!")
        exit(0)
    concept_ids = [id_tuple[0] for id_tuple in cursor.fetchall()]
    begin_time = datetime.datetime.now()
    for i in range(len(concept_ids)):
        id = concept_ids[i]
        try:
            # 打印进度
            logger.info('Seq: ' + str(i + 1) + ' of ' + str(total) + '   Code: ' + id)
            if i > 0 and i % 100 == 0:
                end_time = datetime.datetime.now()
                time_diff = (end_time - begin_time).seconds
                sleep_time = 60 - time_diff
                if sleep_time > 0:
                    logger.info('sleep for ' + str(sleep_time) + ' seconds ...')
                    time.sleep(sleep_time)
                begin_time = datetime.datetime.now()
            df = pro.concept_detail(id=id)
            if df is None:
                continue
        except Exception as e:
            logger.info('Exception found when id = : ' + id)
            print(e)
            time.sleep(60)
            df = pro.concept_detail(id=id)
            # 打印进度
            logger.info('redo Seq: ' + str(i + 1) + ' of ' + str(total) + '   Code: ' + id)

        c_len = df.shape[0]
        for j in range(c_len):
            resu0 = list(df.iloc[c_len - 1 - j])
            resu = []
            for k in range(len(resu0)):
                if str(resu0[k]) == 'nan':
                    resu.append(-1)
                else:
                    resu.append(resu0[k])
            logger.debug(resu)
            try:
                sql_insert = "INSERT INTO concept_detail(concept_code, ts_code, code, name) " \
                             "VALUES ('%s', '%s', '%s', '%s')" % (resu[0], resu[1], str(resu[1])[0:6], resu[2])
                cursor.execute(sql_insert)
                db.commit()
            except Exception as err:
                logger.error(err)
                continue
    cursor.close()
    db.close()
    logger.info('All Finished!')