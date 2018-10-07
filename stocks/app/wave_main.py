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
    code_list = ['601216']
    result = wave.get_wave(code_list, index=False, start='2015-01-01')
    bottom = wave.get_bottom(result, 15)
    print(result)
    print(bottom)
