import sys
from sys import argv

from zillion.gene import wave

if __name__ == '__main__':
    if len(argv) < 2:
        print("Invalid args! At least 2 args like: python xxx.py code1[,code2,...]")
        sys.exit(0)
    codes = argv[1]
    index = False
    try:
        index = (argv[2] == 'true')
    except:
        index = False

    code_list = codes.split(',')
    # print(code_list)

    result = wave.get_wave(code_list, is_index=index, start='2015-01-01')
    print(result)
