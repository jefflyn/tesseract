#!/usr/bin/env bash

source ~/.bash_profile

echo -e "###### collect_today_all start @ `date`"
python3 $STOCKS_HOME/data/etl/basic_data/collect_today_all.py
echo -e "###### collect_today_all end @ `date` \n"
