import sys
from sys import argv

from stocks.app import _utils

default_commission = 5.0
commission_rate = 0.00025  # bs
transfer_rate = 0.00002  # bs
tax_rate = 0.001  # s


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


if len(argv) < 5:
    print("Invalid args! At least 5 args like: python cost.py [cost,share,price,share]")
    sys.exit(-1)
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

print("(%.3f*%d+%.3f*%d+%.3f+%.3f) / (%d+%d)" % (
origincost, ownshare, buyprice, buyshare, commission, transferfee, ownshare, buyshare))
print("need: %.3f" % dealamt)
print("new cost: %.3f" % cost)
print("balance price: %.3f" % balanceprice)
print("loss: %.2f%%" % ((balanceprice - buyprice) / buyprice * 100))
print("total amount: %.3f " % totalamt)
print("total tax: %.3f" % tax)
