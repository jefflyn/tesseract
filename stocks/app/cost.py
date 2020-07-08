import sys
from sys import argv

from stocks.util import _utils

default_commission = 5.0 # 最低佣金
commission_rate = 0.00025  # bs 佣金比率 总金额 万2.5
transfer_rate = 0.00002  # bs 过户手续费比率 总金额 万0.2
tax_rate = 0.001  # s 卖出印花税比例 总金额 千1


def is_valid_price(price):
    if _utils.isnumber(price) is False or float(price) < 0:
        print('price must be numeric and not negative')
        return False
    return True


def is_valid_share(share):
    if str(share).isdecimal() is False or float(share) < 0:
        print('share must be numeric and not negative')
        return False
    return True


def calc_buy_cost_info(argv=None):
    origincost = float(argv[1])
    ownshare = int(argv[2])
    buyprice = float(argv[3])
    buyshare = int(argv[4])
    if (is_valid_price(origincost) or is_valid_price(buyprice)) is False:
        sys.exit(-1)
    if (is_valid_share(ownshare) or is_valid_share(buyshare)) is False:
        sys.exit(-1)

    # buy fee
    dealamt = buyprice * buyshare
    commission = dealamt * commission_rate
    if commission < default_commission:
        commission = default_commission
    # SH & SZ same
    transferfee = dealamt * transfer_rate
    totalamt = dealamt + commission + transferfee

    totalamt = origincost * ownshare + buyprice * buyshare + commission + transferfee
    cost = totalamt / (ownshare + buyshare)
    tax = totalamt * tax_rate

    # sell fee
    scommission = totalamt * commission_rate
    if scommission < default_commission:
        scommission = default_commission
    # SH & SZ same
    stransferfee = totalamt * transfer_rate
    safeamt = totalamt + scommission + stransferfee + tax
    balanceprice = safeamt / (ownshare + buyshare)

    print("(%.3f*%d+%.3f*%d+%.3f+%.3f) / (%d+%d)" % (origincost, ownshare, buyprice, buyshare,
                                                     commission, transferfee, ownshare, buyshare))
    print("need: %.3f" % dealamt)
    print("new cost: %.3f" % cost)
    print("balance price: %.3f" % balanceprice)
    print("loss: %.2f%%" % ((balanceprice - buyprice) / buyprice * 100))
    print("total amount: %.3f " % totalamt)
    print("total tax: %.3f" % tax)


def get_buy_fee(buy_price=0, share=0):
    buy_total = buy_price * share
    buy_commission = buy_total * commission_rate
    if buy_commission < default_commission:
        buy_commission = default_commission
    # SH & SZ same
    transfer_fee = buy_total * transfer_rate
    total_buy_fee = buy_commission + transfer_fee
    # print(buy_commission, transfer_fee)
    return round(total_buy_fee, 2)


def get_sell_fee(sell_price=0, share=0):
    # 卖出佣金和过户费和买入一样，另外还有印花税
    sell_fee = get_buy_fee(sell_price, share)
    sell_total = sell_price * share
    sell_tax = sell_total * tax_rate
    # print(sell_tax)
    return round(sell_fee + sell_tax, 2)


if __name__ == '__main__':
    if len(argv) >= 5:
        calc_buy_cost_info(argv)
        sys.exit(0)
    sell_fee = get_sell_fee(6.71, 15800)
    print(sell_fee)

