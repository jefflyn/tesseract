#!/usr/bin/env bash

source ~/.bash_profile

cd $STOCKS_HOME/data/etl/trading
echo -e "###### collect_index_data start @ `date`"
python3 ./collect_index_data.py
echo -e "###### collect_index_data end @ `date` \n"
