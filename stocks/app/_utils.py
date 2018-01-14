import os
import platform
import sqlite3
from datetime import datetime
import pdfkit

conn = sqlite3.connect('./trade/trade.db')



def is_halting(code, latest_date_str=None):
    starttime = datetime.now()
    latest_date = datetime.strptime(latest_date_str, '%Y-%m-%d')
    delta = starttime - latest_date
    # excluding halting
    if (delta.days > 3):
        print(code + ' halting...')
        return True
    else:
        return False

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
    sysstr = platform.system()
    if (sysstr == "Windows"):
        config=pdfkit.configuration(wkhtmltopdf=r'D:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')
        pdfkit.from_string(htmlstr, desc, options=options, configuration=config)
    elif (sysstr == "Linux"):
        print("Call Linux tasks")
    else:
        pdfkit.from_string(htmlstr, desc, options=options)

    print('save to pdf successfully')