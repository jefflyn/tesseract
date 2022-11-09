#!/usr/bin/env bash

source ~/.bash_profile

cd $STOCKS_HOME/future

echo -e "###### collect_trade_daily start @ `date`"
python3 ./future_trade_daily.py
echo -e "###### collect_trade_daily end @ `date` \n"
