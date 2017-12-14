import os

import sqlite3

conn = sqlite3.connect('../data/trade.db')

def isnumber(a):
    try:
        float(a)
        return True
    except:
        return False

def chdir(path=None):
    if path is None:
        return os.getcwd()
    os.chdir(path)

def get_connection():
    return conn

def get_cursor():
    return conn.cursor()

def get_cursor():
    return conn.cursor()