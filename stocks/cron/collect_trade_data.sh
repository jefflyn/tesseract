#!/usr/bin/env bash

source ~/.bash_profile

cd $STOCKS_HOME/data/etl/trading

echo -e "###### collect_trade_daily start @ `date` \n"
python3 ./collect_trade_daily.py
echo -e "###### collect_trade_daily end @ `date` \n"
