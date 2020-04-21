ENERGY_CHEMICAL = {
    "SC0": "原油",
    "EG0": "乙二醇",
    "EB0": "苯乙烯",
    "FU0": "燃油"
}

PRECIOUS_METAL = {
    "AG0": "沪金",
    "AU0": "沪银"
}

FERROUS_METAL = {
    "I0": "铁矿石",
    "RB0": "螺纹",
    "SF0": "硅铁"
}

NON_FERROUS_METAL = {
    "AL0": "沪铝",
    "PB0": "沪铅",
    "NI0": "沪镍",
    "CU0": "沪铜",
    "SN0": "沪锡",
    "ZN0": "沪锌",
}

AGRICULTURAL_PRODUCTS = {
    "CF0": "棉花",
    "C0": "玉米",
    "CJ0": "红枣",
    "JD0": "鸡蛋",
    "AP0": "苹果",
    "CS0": "淀粉",
    "OI0": "菜油",
    "RM0": "菜粕",
    "RI0": "早稻",
    "LR0": "晚稻",
    "JR0": "粳稻",
    "CY0": "棉纱",
    "PM0": "普麦",
    "A0": "豆一",
    "B0": "豆二",
    "SR0": "白糖"

}

FINANCIAL = {
    "IC2005": "中证",
    "IF2005": "沪深",
    "IH2005": "上证"
}


def dict_key_to_str(items=list()):
    return ','.join(items)
