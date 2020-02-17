#!/usr/bin/env bash

source ~/.bash_profile

cd $STOCKS_HOME/data/etl/basic_data
python3 ./collect_today_all.py
echo "  collect_today_all end " && date "+%Y-%m-%d %H:%M:%S"
echo
python3 $STOCKS_HOME/data/service/limit_up_service.py
echo "  limit_up_service end " && date "+%Y-%m-%d %H:%M:%S"
echo
