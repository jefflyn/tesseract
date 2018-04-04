import os

ZY = '中药.txt'
HXZY = '化学制药.txt'
YLQX = '医疗器械.txt'
YYSY = '医药商业.txt'
BDT = '半导体.txt'
GFJG = '国防军工.txt'
JZCL = '建筑材料.txt'
FDC = '房地产.txt'
YSYL = '有色冶炼.txt'
FZJF = '服装家纺.txt'
JCHY = '机场航运.txt'
QCZC = '汽车整车.txt'
FJR = '泛金融.txt'
GKHY = '港口航运.txt'
MTKC = '煤炭开采.txt'
RQSW = '燃气水务.txt'
HBGC = '环保工程.txt'
DQSB = '电气设备.txt'
BSJD = '白色家电.txt'
SYKY = '石油矿业.txt'
ZQ = '证券.txt'
GT = '钢铁.txt'
YH = '银行.txt'
SPJG = '食品加工.txt'
YLZZ = '饮料制造.txt'





def file_name(file_dir):
    for root, dirs, files in os.walk(file_dir):
        print(root)  # 当前目录路径
        print(dirs)  # 当前路径下所有子目录
        print(files)  # 当前路径下所有非目录子文件

if __name__ == '__main__':
    file_name('.')






















