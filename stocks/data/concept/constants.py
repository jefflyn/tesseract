import os
from stocks.data import _datautils as dt

WUG = '5G.txt'
BMG = '白马股.txt'
CDZ = '充电桩.txt'
CJPP = '超级品牌.txt'
DJS = '独角兽.txt'
DSJ = '大数据.txt'
GDZMQ = '广东自贸区.txt'
GYHLW = '工业互联网.txt'
HN = '海南.txt'
JG = '军工.txt'
JMRH = '军民融合.txt'
JYYC = '基因预测.txt'
LDC = '锂电池.txt'
NDSD = '宁德时代.txt'
QKL = '区块链.txt'
RGZN = '人工智能.txt'
RLSB = '人脸识别.txt'
SGZGG = '深圳国资改革.txt'
SHGZGG = '上海国资改革.txt'
SHZMQ = '上海自贸区.txt'
SMX = '石墨烯.txt'
SN = '水泥.txt'
SWYY = '生物医药.txt'
TJZMQ = '天津自贸区.txt'
WLAQ = '网络安全.txt'
WRJS = '无人驾驶.txt'
WRLS = '无人零售.txt'
WXCD = '无线充电.txt'
XAXQ = '雄安新区.txt'
XBMYZL = '细胞免疫治疗.txt'
XC = '西藏.txt'
XJ = '新疆.txt'
XJS = '小金属.txt'
XJZX = '新疆振兴.txt'
XLS = '新零售.txt'
XNYQC = '新能源汽车.txt'
XP = '芯片.txt'
XQZY = '稀缺资源.txt'
XTYC = '稀土永磁.txt'
YGA = '粤港澳.txt'
YJS = '云计算.txt'
YLGG = '医疗改革.txt'
YLQX = '医疗器械.txt'
YQGZGG = '央企国资改革.txt'
ZNYL = '智能医疗.txt'
ZQ = '足球.txt'
ZSTQ = '租售同权.txt'
ZYMYG = '自由贸易港.txt'
ZZT = '中字头.txt'


def file_name(file_dir):
    for root, dirs, files in os.walk(file_dir):
        # print(root)  # 当前目录路径
        # print(dirs)  # 当前路径下所有子目录
        for str in files:
            if str == 'constants.py':
                continue
            filename = str.split('.')[0]
            nameletter = dt.get_letter(filename)
            print("%s = '%s'" %(nameletter, str))  # 当前路径下所有非目录子文件
        break

if __name__ == '__main__':
    file_name('.')





































