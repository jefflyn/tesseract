#!/usr/bin/env bash

source ~/.bash_profile

cd $STOCKS_HOME/data/etl/trading

echo -e "###### collect_trade_daily_init start @ `date`"
python3 ./init/init_trade_data.py
echo -e "###### collect_trade_daily_init end @ `date` \n"
