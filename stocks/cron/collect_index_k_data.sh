#!/usr/bin/env bash

source ~/.bash_profile

echo -e "###### collect_index_k_data start @ `date`"
python3 $STOCKS_HOME/data/etl/trading/collect_index_hist_k.py
echo -e "###### collect_index_k_data end @ `date` \n"
