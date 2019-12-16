#!/usr/bin/env bash

cd $STOCKS_HOME/data/etl/trading
python3 ./collect_index_data.py
echo "finished collect_index_data"
