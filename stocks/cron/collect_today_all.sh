#!/usr/bin/env bash

source ~/.bash_profile

echo -e "###### collect_today_all start @ `date`"
python3 $STOCKS_HOME/data/etl/basic_data/collect_today_all.py
echo -e "###### collect_today_all end @ `date` \n"

echo -e "###### limit_up_service start @ `date`"
python3 $STOCKS_HOME/data/service/limit_up_service.py
echo -e "###### limit_up_service end @ `date` \n"
