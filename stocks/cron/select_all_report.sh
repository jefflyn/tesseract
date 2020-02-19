#!/usr/bin/env bash

source ~/.bash_profile

echo -e "###### select_all start @ `date`"
python3 $STOCKS_HOME/app/selection/select_all.py
echo -e "###### select_all end @ `date` \n"

echo -e "###### report_select start @ `date`"
python3 $STOCKS_HOME/app/report/report_select.py
echo -e "###### report_select end @ `date` \n"
