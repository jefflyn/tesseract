cd /Users/linjingu/work/machine-learning/stocks
cd data
python _fundamental.py >> ./log/etl.log
python _trade.py >> ./log/etl.log