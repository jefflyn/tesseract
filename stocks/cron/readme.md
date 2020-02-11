
30 16 * * 1-5 /Users/ruian/work/my-git/tesseract/stocks/cron/collect_basic_daily.sh >~/stocks.log 2>&1
30 16 * * 1-5 /Users/ruian/work/my-git/tesseract/stocks/cron/collect_trade_data.sh >~/stocks.log 2>&1
30 16 * * 1-5 /Users/ruian/work/my-git/tesseract/stocks/cron/collect_ma_data.sh >~/stocks.log 2>&1
10 17 * * 1-5 /Users/ruian/work/my-git/tesseract/stocks/cron/select_all.sh >>~/stocks.log 2>&1
20 10,15 * * 1 /Users/ruian/work/my-git/tesseract/stocks/cron/collect_trade_weekly.sh >>~/stocks.log 2>&1
