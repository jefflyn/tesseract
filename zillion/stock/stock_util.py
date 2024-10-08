from utils import datetime


def is_halting(code, latest_date_str=None):
    starttime = datetime.now()
    latest_date = datetime.strptime(latest_date_str, '%Y-%m-%d')
    delta = starttime - latest_date
    # excluding halting
    if delta.days > 4:
        print(code + ' halting...')
        return True
    else:
        return False

