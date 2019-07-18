#!/usr/bin/env bash

export PYTHONPATH=/Users/linjingu/work/machine-learning/
export STOCKS_HOME=/Users/linjingu/work/machine-learning/stocks

/anaconda/bin/python /Users/linjingu/work/machine-learning/stocks/data/etl/trading/collect_index_data.py
/anaconda/bin/python /Users/linjingu/work/machine-learning/stocks/data/etl/trading/collect_trade_daily.py
/anaconda/bin/python /Users/linjingu/work/machine-learning/stocks/data/etl/basic_data/collect_basic_daily.py
/anaconda/bin/python /Users/linjingu/work/machine-learning/stocks/app/shell/select_all.py
/anaconda/bin/python /Users/linjingu/work/machine-learning/stocks/data/etl/trading/collect_trade_daily_again.py
/anaconda/bin/python /Users/linjingu/work/machine-learning/stocks/app/shell/select_all.py