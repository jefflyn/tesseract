import configparser
import os

cf = configparser.ConfigParser()
path = os.path.abspath('./stocks.conf')

cf.read(path)
host = cf.get('bluetooth', 'host')
base_url = cf.get('bluetooth', 'base_url')
home_path = cf.get('bluetooth', 'stocks_home')
print(host, base_url, home_path)
print(cf.sections())
