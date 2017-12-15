import sys
from sys import argv
import pandas as pd
from stocks.app.trade import dealer
from stocks.app import _utils

pd.set_option('display.width',800)

def isvalidprice(price):
    if _utils.isnumber(price) == False or float(price) < 0:
        print('price must be numeric and not negative')
        return False
    return True

def isvalidshare(share):
    if str(share).isdecimal() == False or float(share) < 0:
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
if (isvalidprice(origincost) or isvalidprice(buyprice)) == False:
    sys.exit(-1)
if (isvalidshare(ownshare) or isvalidshare(buyshare)) == False:
    sys.exit(-1)

dealamt = buyprice * buyshare
commision = dealamt * dealer.commisionrate
if commision < dealer.defaultcommision:
    commision = dealer.defaultcommision;
# SH & SZ same
transferfee = dealamt * dealer.transferrate
totalamt = dealamt + commision + transferfee

totalamt = origincost * ownshare + buyprice * buyshare + commision + transferfee
cost = totalamt / (ownshare + buyshare)
tax = totalamt * dealer.taxrate

print("(%.3f*%d+%.3f*%d+%.3f+%.3f) / (%d+%d)" % (origincost, ownshare, buyprice, buyshare, commision, transferfee, ownshare, buyshare))
print("new cost: %.3f" % cost)
print("loss: %.2f%%" % ((cost - buyprice) / buyprice * 100))
print("total amount: %.3f " % totalamt)
print("total tax: %.3f" % tax)




