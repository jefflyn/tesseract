#!/usr/bin/env bash

source ~/.bash_profile

echo -e "###### collect_limit_up_daily start @ `date`"
python3 $STOCKS_HOME/data/etl/trading/collect_limit_up_daily.py
echo -e "###### collect_limit_up_daily end @ `date` \n"

