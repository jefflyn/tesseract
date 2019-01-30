import os
from stocks.data import _datautils as dt

BDTYJ = '半导体元件.txt'
BSJD = '白色家电.txt'
DQSB = '电气设备.txt'
FDC = '房地产.txt'
FZJF = '服装家纺.txt'
GFJG = '国防军工.txt'
GKHY = '港口航运.txt'
GT = '钢铁.txt'
GXGDZ = '光学光电子.txt'
HBGC = '环保工程.txt'
HXZY = '化学制药.txt'
JCHY = '机场航运.txt'
JSJSB = '计算机设备.txt'
JSJYY = '计算机应用.txt'
JZCL = '建筑材料.txt'
MSKC = '煤炭开采.txt'
NCPJG = '农产品加工.txt'
QCZC = '汽车整车.txt'
RQSW = '燃气水务.txt'
SPJG = '食品加工.txt'
SPYL = '食品饮料.txt'
SYKY = '石油矿业.txt'
TXFW = '通讯服务.txt'
TXSB = '通讯设备.txt'
YLQX = '医疗器械.txt'
YLZZ = '饮料制造.txt'
YS = '有色冶炼.txt'
YH = '银行.txt'
YYSY = '医药商业.txt'
ZQ = '证券.txt'
ZY = '中药.txt'


def file_name(file_dir):
    for root, dirs, files in os.walk(file_dir):
        # print(root)  # 当前目录路径
        # print(dirs)  # 当前路径下所有子目录
        for str in files:
            if str == 'constants.py':
                continue
            filename = str.split('.')[0]
            nameletter = dt.get_letter(filename)
            print("%s = '%s'" % (nameletter, str))  # 当前路径下所有非目录子文件
        break

if __name__ == '__main__':
    file_name('.')






















