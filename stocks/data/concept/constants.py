import os

FIFTHG = '5G.txt'
LDC = '锂电池.txt'
RGZN = '人工智能.txt'
CDZ = '充电桩.txt'
DJS = '独角兽.txt'
HN = '海南.txt'
JG =  '军工.txt'
JMRH =  '军民融合.txt'
GYHLW = '工业互联网.txt'
NDSD = '宁德时代.txt'
QKL =  '区块链.txt'
YLQX =  '医疗器械.txt'
DSJ =  '大数据.txt'
XJS =  '小金属.txt'
XNYQC =  '新能源汽车.txt'
WRLS =  '无人零售.txt'
WRJS =  '无人驾驶.txt'
WXCD =  '无线充电.txt'
SN =  '水泥.txt'
SZ =  '深圳.txt'
BMG =  '白马股.txt'
SMX =  '石墨烯.txt'
ZSTQ =  '租售同权.txt'
XTYC =  '稀土永磁.txt'
XQZY =  '稀缺资源.txt'
YGA =  '粤港澳.txt'
WLAQ =  '网络安全.txt'
XLS = '新零售.txt'
XP =  '芯片.txt'
CJPP =  '超级品牌.txt'
XAXQ =  '雄安新区.txt'


def file_name(file_dir):
    for root, dirs, files in os.walk(file_dir):
        # print(root)  # 当前目录路径
        # print(dirs)  # 当前路径下所有子目录
        print(files)  # 当前路径下所有非目录子文件
        print('size: %d' %len(files))

if __name__ == '__main__':
    file_name('.')





































