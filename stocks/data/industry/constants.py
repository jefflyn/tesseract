import os

INDUSTRY_ZY = '中药.txt'
INDUSTRY_HXZY = '化学制药.txt'
INDUSTRY_YLQX = '医疗器械.txt'
INDUSTRY_YYSY = '医药商业.txt'
INDUSTRY_BDT = '半导体.txt'
INDUSTRY_GFJG = '国防军工.txt'
INDUSTRY_JZCL = '建筑材料.txt'
INDUSTRY_FDC = '房地产.txt'
INDUSTRY_YSYL = '有色冶炼.txt'
INDUSTRY_FZJF = '服装家纺.txt'
INDUSTRY_JCHY = '机场航运.txt'
INDUSTRY_QCZC = '汽车整车.txt'
INDUSTRY_FJR = '泛金融.txt'
INDUSTRY_GKHY = '港口航运.txt'
INDUSTRY_MTKC = '煤炭开采.txt'
INDUSTRY_RQSW = '燃气水务.txt'
INDUSTRY_HBGC = '环保工程.txt'
INDUSTRY_DQSB = '电气设备.txt'
INDUSTRY_BSJD = '白色家电.txt'
INDUSTRY_SYKY = '石油矿业.txt'
INDUSTRY_ZQ = '证券.txt'
INDUSTRY_GT = '钢铁.txt'
INDUSTRY_YH = '银行.txt'
INDUSTRY_SPJG = '食品加工.txt'
INDUSTRY_YLZZ = '饮料制造.txt'





def file_name(file_dir):
    for root, dirs, files in os.walk(file_dir):
        print(root)  # 当前目录路径
        print(dirs)  # 当前路径下所有子目录
        print(files)  # 当前路径下所有非目录子文件

if __name__ == '__main__':
    file_name('.')












