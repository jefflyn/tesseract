#!/usr/bin/env bash

source ~/.bash_profile

cd $STOCKS_HOME/data/etl/trading

echo -e "###### collect_trade_daily_again start @ `date`"
python3 ./collect_trade_daily_replace.py
echo -e "###### collect_trade_daily_again end @ `date` \n"
