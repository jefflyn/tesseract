#!/usr/bin/env bash

source ~/.bash_profile

cd $STOCKS_HOME/data/etl/trading

echo -e "###### collect_ma_daily start @ `date`"
python3 ./collect_ma_daily.py
echo -e "###### collect_ma_daily end @ `date` \n"
