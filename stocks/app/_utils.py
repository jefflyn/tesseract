import os

import sqlite3

import pdfkit

conn = sqlite3.connect('./trade/trade.db')

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


def save_to_pdf(htmlstr=None, desc=None):
    options = {
        'page-size': 'Letter',
        'margin-top': '0.75in',
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
        'encoding': "UTF-8",
        'custom-header': [
            ('Accept-Encoding', 'gzip')
        ],
        'no-outline': None
    }
    config=pdfkit.configuration(wkhtmltopdf=r'D:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')
    pdfkit.from_string(htmlstr,desc,options=options,configuration=config)
    # pdfkit.from_string(htmlstr, desc, options=options)
    print('save to pdf successfully')