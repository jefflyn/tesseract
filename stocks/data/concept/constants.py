import os

CONCEPT_5G = '5G.txt'
CONCEPT_LDC = '锂电池.txt'
CONCEPT_RGZN = '人工智能.txt'
CONCEPT_CDZ = '充电桩.txt'
CONCEPT_DJS = '独角兽.txt'
CONCEPT_JG =  '军工.txt'
CONCEPT_JMRH =  '军民融合.txt'
CONCEPT_NDSD = '宁德时代.txt'
CONCEPT_QKL =  '区块链.txt'
CONCEPT_YLQX =  '医疗器械.txt'
CONCEPT_DSJ =  '大数据.txt'
CONCEPT_XJS =  '小金属.txt'
CONCEPT_XNYQC =  '新能源汽车.txt'
CONCEPT_WRLS =  '无人零售.txt'
CONCEPT_WRJS =  '无人驾驶.txt'
CONCEPT_WXCD =  '无线充电.txt'
CONCEPT_SN =  '水泥.txt'
CONCEPT_SZ =  '深圳.txt'
CONCEPT_BMG =  '白马股.txt'
CONCEPT_SMX =  '石墨烯.txt'
CONCEPT_ZSTQ =  '租售同权.txt'
CONCEPT_XTYC =  '稀土永磁.txt'
CONCEPT_XQZY =  '稀缺资源.txt'
CONCEPT_YGA =  '粤港澳.txt'
CONCEPT_WLAQ =  '网络安全.txt'
CONCEPT_XP =  '芯片.txt'
CONCEPT_CJPP =  '超级品牌.txt'
CONCEPT_XAXQ =  '雄安新区.txt'


def file_name(file_dir):
    for root, dirs, files in os.walk(file_dir):
        print(root)  # 当前目录路径
        print(dirs)  # 当前路径下所有子目录
        print(files)  # 当前路径下所有非目录子文件

if __name__ == '__main__':
    file_name('.')












