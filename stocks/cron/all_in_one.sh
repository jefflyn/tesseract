#!/usr/bin/env bash

source ~/.bash_profile

cd $STOCKS_HOME/data/etl/basic_data

echo -e "###### collect_hist_trade_date start @ `date`"
python3 ./collect_hist_trade_date.py
echo -e "###### collect_hist_trade_date end @ `date` \n"

echo -e "###### collect_basics start @ `date`"
python3 ./collect_basic.py
python3 ./collect_basics.py
echo -e "###### collect_basics end @ `date` \n"

cd $STOCKS_HOME/data/etl/trading

echo -e "###### collect_trade_weekly start @ `date`"
python3 ./collect_trade_weekly.py
echo -e "###### collect_trade_weekly end @ `date` \n"

echo -e "###### collect_ma_daily start @ `date`"
python3 ./collect_ma_daily.py
echo -e "###### collect_ma_daily end @ `date` \n"

echo -e "###### collect_index_k_data start @ `date`"
python3 $STOCKS_HOME/data/etl/trading/collect_index_hist_k.py
echo -e "###### collect_index_k_data end @ `date` \n"

echo -e "###### collect_today_all start @ `date`"
python3 $STOCKS_HOME/data/etl/basic_data/collect_today_all.py
echo -e "###### collect_today_all end @ `date` \n"

echo -e "###### collect_limit_up_daily start @ `date`"
python3 $STOCKS_HOME/data/etl/trading/collect_limit_up_daily.py
echo -e "###### collect_limit_up_daily end @ `date` \n"

echo -e "###### select_all start @ `date`"
python3 $STOCKS_HOME/app/selection/select_all.py
echo -e "###### select_all end @ `date` \n"

echo -e "###### report_select start @ `date`"
python3 $STOCKS_HOME/app/report/report_select.py
echo -e "###### report_select end @ `date` \n"