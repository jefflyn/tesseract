from stocks.data.service import limit_up_service
from stocks.util import date_util

if __name__ == '__main__':
    limit_up_service.collect_limit_up_stat(target_date=date_util.get_this_week_start())
    limit_up_service.update_latest_limit_up_stat()

