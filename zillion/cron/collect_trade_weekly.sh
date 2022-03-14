#!/usr/bin/env bash

source ~/.bash_profile

cd $STOCKS_HOME/data/etl/trading

echo -e "###### collect_trade_weekly start @ `date`"
python3 ./collect_trade_weekly.py
echo -e "###### collect_trade_weekly end @ `date` \n"
