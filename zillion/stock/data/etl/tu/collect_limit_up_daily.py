from utils.datetime import date_util
from zillion.stock.app.cn.service import limit_up_service

if __name__ == '__main__':
    limit_up_service.collect_daily_limit_up(target_date=date_util.get_this_week_start())
    limit_up_service.update_latest_limit_up_stat()
    # limit_up_service.sync_rds_limit_up_stat()
