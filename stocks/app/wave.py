import sys
from sys import argv

import numpy as np
import pandas as pd

import pymysql
from sqlalchemy import create_engine

from stocks.gene import limitup
from stocks.gene import wave

pd.set_option('display.width', 600)

if __name__ == '__main__':
    if len(argv) < 2:
        print("Invalid args! At least 2 args like: python xxx.py code1[,code2,...]")
        sys.exit(0)
    codes = argv[1]
    index = (argv[2] == 'true')

    code_list = codes.split(',')
    print(code_list)

    result = wave.get_wave(code_list, index=index, start='2016-01-01')
    print(result)