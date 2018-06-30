cd /Users/linjingu/work/machine-learning/stocks
cd data
python _fundamental.py >> ./log/etl.log
echo 'fundamental etl done!'
python _trade.py >> ./log/etl.log
echo 'trade data etl done!'