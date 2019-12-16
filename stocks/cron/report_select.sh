#!/usr/bin/env bash
#30 16 * * 1-5 /Users/ruian/work/my-git/tesseract/stocks/cron/collect_all.sh >~/stocks.log 2>&1
#30 17 * * 1-5 /Users/ruian/work/my-git/tesseract/stocks/cron/select_all.sh >~/stocks.log 2>&1
#50 17 * * 1-5 /Users/ruian/work/my-git/tesseract/stocks/cron/report_select.sh >~/stocks.log 2>&1

source ~/.bash_profile

python3 $STOCKS_HOME/app/report/report_select.py
date "+%Y-%m-%d %H:%M:%S"
echo "finished all"
