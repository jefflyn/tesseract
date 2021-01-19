# log type
LOG_TYPE_CONTRACT_NEW_HIGH = '合约新高'
LOG_TYPE_CONTRACT_NEW_LOW = '合约新低'
LOG_TYPE_DAY_NEW_HIGH = '日内新高'
LOG_TYPE_DAY_NEW_LOW = '日内新低'
LOG_TYPE_PRICE_UP = '快速拉升'
LOG_TYPE_PRICE_DOWN = '快速下跌'

# 商品类型
ENERGY = '能源'
CHEMICAL1 = '化工1'
CHEMICAL2 = '化工2'
CHEMICAL3 = '化工3'

COAL_FERROUS_METAL = '黑色'  # '煤炭\黑色金属'
PRECIOUS_METAL = '贵金属'
OIL_MATERIAL = '油脂油料'
NON_FERROUS_METAL = '有色金属'
AGRICULTURAL_PRODUCTS = '农产品'
FINANCIAL = '金融板块'
GOODS_TYPE_MAP = {
    'ag': AGRICULTURAL_PRODUCTS,
    'om': OIL_MATERIAL,
    'ch1': CHEMICAL1,
    'ch2': CHEMICAL2,
    'ch3': CHEMICAL3,
    'en': ENERGY,
    'bk': COAL_FERROUS_METAL,
    'pm': PRECIOUS_METAL,
    'nfm': NON_FERROUS_METAL,
    'fi': FINANCIAL
}
