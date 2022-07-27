#!/usr/bin/env bash

export PYTHONPATH=/Users/ruian/work/my-git/tesseract/

echo -e "###### update wave start @ `date`"
/Users/ruian/.conda/envs/tesseract/bin/python /Users/ruian/work/my-git/tesseract/zillion/future/future_wave.py
/Users/ruian/.conda/envs/tesseract/bin/python /Users/ruian/work/my-git/tesseract/zillion/future/app/nday_stat.py
echo -e "###### update wave end @ `date` \n"
