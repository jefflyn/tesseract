import sys
from sys import argv

from stocks.app import _utils

default_commision = 5.0
commision_rate = 0.00025
transfer_rate = 0.00002
tax_rate = 0.001


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
commision = dealamt * commision_rate
if commision < default_commision:
    commision = default_commision;
# SH & SZ same
transferfee = dealamt * transfer_rate
totalamt = dealamt + commision + transferfee

totalamt = origincost * ownshare + buyprice * buyshare + commision + transferfee
cost = totalamt / (ownshare + buyshare)
tax = totalamt * tax_rate

# sell fee
scommision = totalamt * commision_rate
if scommision < default_commision:
    scommision = default_commision
# SH & SZ same
stransferfee = totalamt * transfer_rate
safeamt = totalamt + scommision + stransferfee + tax
balanceprice = safeamt / (ownshare + buyshare)

print("(%.3f*%d+%.3f*%d+%.3f+%.3f) / (%d+%d)" % (
origincost, ownshare, buyprice, buyshare, commision, transferfee, ownshare, buyshare))
print("need: %.3f" % dealamt)
print("new cost: %.3f" % cost)
print("balance price: %.3f" % balanceprice)
print("loss: %.2f%%" % ((balanceprice - buyprice) / buyprice * 100))
print("total amount: %.3f " % totalamt)
print("total tax: %.3f" % tax)
