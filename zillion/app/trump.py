import sys
from sys import argv

import pandas as pd

from zillion.gene import trump

pd.set_option('display.width', 600)

if __name__ == '__main__':
    if len(argv) < 2:
        print("Invalid args! At least 2 args like: python xxx.py code1[,code2,...]")
        sys.exit(0)
    codes = argv[1]
    index = False
    try:
        index = (argv[2] == 'true')
    except Exception as e:
        index = False

    code_list = codes.split(',')
    print(code_list)

    result = trump.get_trump(code_list)
    print(result)
