from zillion.stock.data.service import limit_up_service
from zillion.utils import date_util

if __name__ == '__main__':
    limit_up_service.collect_daily_limit_up(target_date=date_util.get_this_week_start())
    limit_up_service.update_latest_limit_up_stat()
    # limit_up_service.sync_rds_limit_up_stat()
