#!/usr/bin/env bash

source ~/.bash_profile

cd $STOCKS_HOME/data/etl/basic_data

echo -e "###### collect_hist_trade_date start @ `date`"
python3 ./collect_hist_trade_date.py
echo -e "###### collect_hist_trade_date end @ `date` \n"

echo -e "###### collect_basics start @ `date`"
python3 ./collect_basics.py
echo -e "###### collect_basics end @ `date` \n"